"""
Script de download do Gini 2022 (aproximado) e % pobres 2022 via Censo 2022 / SIDRA.

Fontes:
- Tabela 10296 — Moradores por classes de rendimento domiciliar per capita (Censo 2022)

Metodologia % pobres 2022:
    % de moradores com rendimento domiciliar per capita "Até 1/4 do salário mínimo"
    (≤ R$303/mês em 2022) mais "Sem rendimento", sobre o total de moradores.
    A linha de pobreza oficial de 2022 (Decreto 11.150/2022, R$218/mês per capita)
    está contida na faixa "Até 1/4 SM", tornando esse o proxy mais próximo disponível.

Metodologia Gini 2022 (aproximação por curva de Lorenz):
    O IBGE publica Gini 2022 apenas até nível estadual via API SIDRA (tabela 10301).
    Calculamos uma aproximação para cada município usando a distribuição por faixas de
    renda da tabela 10296, com o método da curva de Lorenz discreta:
      1. Midpoint de cada faixa como estimativa de renda média do grupo
      2. Construção da curva de Lorenz (população acumulada vs. renda acumulada)
      3. Gini = 1 - 2 × AUC_Lorenz (regra do trapézio)
    Para a faixa aberta ">20 SM", a renda média é estimada como 2× o limite inferior
    (R$24.240), o que é conservador e consiste com a literatura (equivalente a α=2
    na distribuição de Pareto).
    Esta aproximação é padrão na literatura econométrica quando microdados não estão
    disponíveis (Anand & Kanbur 1993; Deininger & Squire 1996).

Executar a partir da raiz do projeto:
    python3 data/download_gini_pobres_2022.py
"""

import time
from pathlib import Path

import numpy as np
import pandas as pd
import requests

RAW_DIR = Path(__file__).parent / "raw"
BASE_URL = "https://servicodados.ibge.gov.br/api/v3/agregados"
PERIODO = "2022"

# Salário mínimo 2022 (Decreto 10.854/2021): R$ 1.212,00
SM_2022 = 1212.0

# Faixas de renda: (cat_id, midpoint_R$, descricao)
# Midpoints: média entre extremos. Para ">20 SM" usa-se 2x o limite inferior.
FAIXAS = [
    (9692, 0.0,              "Sem rendimento"),
    (9681, SM_2022 * 0.125,  "Até 1/4 SM"),           # 0 a 303 → mid 151.5
    (9682, SM_2022 * 0.375,  "1/4 a 1/2 SM"),          # 303 a 606 → mid 454.5
    (9683, SM_2022 * 0.75,   "1/2 a 1 SM"),            # 606 a 1212 → mid 909
    (9684, SM_2022 * 1.5,    "1 a 2 SM"),              # 1212 a 2424 → mid 1818
    (9685, SM_2022 * 2.5,    "2 a 3 SM"),              # 2424 a 3636 → mid 3030
    (9686, SM_2022 * 4.0,    "3 a 5 SM"),              # 3636 a 6060 → mid 4848
    (9687, SM_2022 * 7.5,    "5 a 10 SM"),             # 6060 a 12120 → mid 9090
    (9688, SM_2022 * 12.5,   "10 a 15 SM"),            # 12120 a 18180 → mid 15150
    (9689, SM_2022 * 17.5,   "15 a 20 SM"),            # 18180 a 24240 → mid 21210
    (9690, SM_2022 * 40.0,   ">20 SM (2× lower)"),     # >24240 → estimativa conservadora
]

CAT_TOTAL = 9692 + 1  # Não existe — o total é cat 9680
CAT_POBRES = [9692, 9681]  # Sem rendimento + Até 1/4 SM


# ---------------------------------------------------------------------------
# Utilitários
# ---------------------------------------------------------------------------

def fetch_sidra(
    tabela: int,
    variavel: int,
    classificacao: str,
    periodo: str = PERIODO,
) -> dict[str, float | None]:
    """Busca uma variável do SIDRA para todos os municípios (N6[all]).

    Args:
        tabela: Código da tabela SIDRA.
        variavel: Código da variável desejada.
        classificacao: String de classificação no formato 'cls[cat]|...'
        periodo: Ano de referência.

    Returns:
        Dicionário {cod_ibge_7dig: float | None}.
    """
    url = (
        f"{BASE_URL}/{tabela}/periodos/{periodo}/variaveis/{variavel}"
        f"?localidades=N6%5Ball%5D&classificacao={classificacao}"
    )
    resp = requests.get(url, timeout=120)
    resp.raise_for_status()
    data = resp.json()

    result: dict[str, float | None] = {}
    for bloco in data[0]["resultados"]:
        for item in bloco["series"]:
            cod = item["localidade"]["id"]
            val = item["serie"].get(periodo)
            if val in (None, "-", "...", "X", ""):
                result[cod] = None
            else:
                try:
                    result[cod] = float(str(val).replace(",", "."))
                except ValueError:
                    result[cod] = None
    return result


# ---------------------------------------------------------------------------
# Downloads
# ---------------------------------------------------------------------------

def download_faixa(cat_id: int, descricao: str, step: int, total: int) -> dict[str, float | None]:
    """Baixa a contagem de moradores em uma faixa de renda para todos os municípios."""
    print(f"  [{step:2d}/{total}] cat {cat_id} — {descricao}...", end=" ", flush=True)
    cls = f"386[{cat_id}]%7C2[6794]%7C86[95251]"
    data = fetch_sidra(10296, 13604, classificacao=cls)
    n_val = sum(1 for v in data.values() if v is not None)
    print(f"{n_val} municípios com dados")
    time.sleep(1.5)
    return data


def download_total(step: int, total: int) -> dict[str, float | None]:
    """Baixa o total de moradores por município (denominador)."""
    print(f"  [{step:2d}/{total}] cat 9680 — Total de moradores...", end=" ", flush=True)
    cls = "386[9680]%7C2[6794]%7C86[95251]"
    data = fetch_sidra(10296, 13604, classificacao=cls)
    n_val = sum(1 for v in data.values() if v is not None)
    print(f"{n_val} municípios com dados")
    time.sleep(1.5)
    return data


# ---------------------------------------------------------------------------
# Cálculos
# ---------------------------------------------------------------------------

def lorenz_gini(counts: list[float], midpoints: list[float]) -> float | None:
    """Calcula o índice de Gini via curva de Lorenz discreta.

    Args:
        counts: Contagem de pessoas em cada faixa (na ordem crescente de renda).
        midpoints: Renda média estimada em cada faixa (mesma ordem).

    Returns:
        Índice de Gini [0, 1] ou None se os dados forem insuficientes.
    """
    counts = np.array(counts, dtype=float)
    midpoints = np.array(midpoints, dtype=float)

    # Ignorar faixas sem dados (None foi convertido para 0 antes)
    total_pop = counts.sum()
    if total_pop <= 0:
        return None

    total_income = (counts * midpoints).sum()
    if total_income <= 0:
        return None  # município sem renda — Gini indefinido

    # Proporções de população e renda por faixa
    pop_share = counts / total_pop
    inc_share = (counts * midpoints) / total_income

    # Curva de Lorenz: (0,0) → pontos acumulados → (1,1)
    F = np.concatenate([[0.0], np.cumsum(pop_share)])
    L = np.concatenate([[0.0], np.cumsum(inc_share)])

    # Gini = 1 - 2 × área sob a curva (regra do trapézio)
    auc = np.trapz(L, F)
    return round(1.0 - 2.0 * auc, 4)


def compute_metrics(
    faixas_data: dict[int, dict[str, float | None]],
    total_data: dict[str, float | None],
    midpoints: list[float],
    cat_ids: list[int],
) -> pd.DataFrame:
    """Calcula Gini aproximado e % pobres para todos os municípios.

    Args:
        faixas_data: {cat_id: {cod_ibge: contagem}}.
        total_data: {cod_ibge: total de moradores}.
        midpoints: Renda média por faixa (mesma ordem que cat_ids).
        cat_ids: IDs das categorias (na ordem crescente de renda).

    Returns:
        DataFrame com cod_ibge, gini_2022 e perc_pobres_2022.
    """
    all_cods = sorted(total_data.keys())
    rows = []

    for cod in all_cods:
        total = total_data.get(cod) or 0.0

        # % pobres = (Sem rendimento + Até 1/4 SM) / Total
        n_sem_renda = faixas_data.get(9692, {}).get(cod) or 0.0
        n_ate_quarto = faixas_data.get(9681, {}).get(cod) or 0.0
        perc_pobres = (
            round((n_sem_renda + n_ate_quarto) / total * 100, 4)
            if total > 0 else None
        )

        # Gini via Lorenz
        counts = [faixas_data[c].get(cod) or 0.0 for c in cat_ids]
        gini = lorenz_gini(counts, midpoints)

        rows.append({
            "cod_ibge": cod,
            "gini_2022": gini,
            "perc_pobres_2022": perc_pobres,
        })

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("=== Download Gini (aprox.) e % Pobres — Censo IBGE 2022 ===\n")
    print("Tabela 10296 — moradores por faixa de rendimento domiciliar per capita\n")

    cat_ids   = [f[0] for f in FAIXAS]
    midpoints = [f[1] for f in FAIXAS]
    descricoes = [f[2] for f in FAIXAS]
    total_steps = len(FAIXAS) + 1  # faixas + total

    # Total de moradores (denominador)
    total_data = download_total(step=1, total=total_steps)

    # Cada faixa de renda
    faixas_data: dict[int, dict[str, float | None]] = {}
    for i, (cat_id, _, desc) in enumerate(FAIXAS):
        faixas_data[cat_id] = download_faixa(cat_id, desc, step=i + 2, total=total_steps)

    print("\nCalculando métricas por município...")
    df = compute_metrics(faixas_data, total_data, midpoints, cat_ids)

    # Validação
    n_gini_valido  = df["gini_2022"].notna().sum()
    n_pobres_valido = df["perc_pobres_2022"].notna().sum()
    print(f"\n  Municípios com Gini válido:     {n_gini_valido}/{len(df)}")
    print(f"  Municípios com % pobres válido: {n_pobres_valido}/{len(df)}")
    print(f"\n  Estatísticas:")
    print(df[["gini_2022", "perc_pobres_2022"]].describe().round(4).to_string())

    out_path = RAW_DIR / "gini_pobres_censo2022.csv"
    df.to_csv(out_path, index=False, encoding="utf-8")
    print(f"\n✓ Salvo: {out_path}")
    print("=== Concluído ===")


if __name__ == "__main__":
    main()
