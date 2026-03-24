"""
Script de download dos dados socioeconômicos via API SIDRA/IBGE (Censo 2022).

Fontes:
- IBGE SIDRA API v3 — Censo Demográfico 2022
- Sinesp/MJ — homicídios dolosos por município (já baixado como xlsx)
- IBGE FTP — PIB per capita municipal 2023 (já baixado como xlsx)
- IBGE FTP — áreas territoriais 2024 (já baixado como xls)

Variáveis NÃO disponíveis no Censo 2022 a nível municipal via SIDRA:
- Índice de Gini → usar Atlas Brasil (Censo 2010)
- IDHM (geral + 3 sub) → usar Atlas Brasil (Censo 2010)
- % de pobres → usar Atlas Brasil (Censo 2010)

Executar a partir da raiz do projeto:
    python data/download_sidra.py
"""

import json
import time
from pathlib import Path

import pandas as pd
import requests

RAW_DIR = Path(__file__).parent / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://servicodados.ibge.gov.br/api/v3/agregados"
PERIODO = "2022"

# ---------------------------------------------------------------------------
# Utilitários
# ---------------------------------------------------------------------------

def fetch_sidra(
    tabela: int,
    variavel: int,
    classificacao: str | None = None,
    periodo: str = PERIODO,
) -> dict[str, str | None]:
    """Busca uma variável do SIDRA para todos os municípios (N6).

    Args:
        tabela: Código da tabela SIDRA.
        variavel: Código da variável desejada.
        classificacao: String de classificação no formato 'id[cat1,cat2]' (opcional).
        periodo: Ano de referência.

    Returns:
        Dicionário {cod_ibge_7dig: valor_str}.
    """
    url = (
        f"{BASE_URL}/{tabela}/periodos/{periodo}/variaveis/{variavel}"
        f"?localidades=N6%5Ball%5D"
    )
    if classificacao:
        url += f"&classificacao={classificacao}"

    resp = requests.get(url, timeout=120)
    resp.raise_for_status()
    data = resp.json()

    result: dict[str, str | None] = {}
    for bloco in data[0]["resultados"]:
        for item in bloco["series"]:
            cod = item["localidade"]["id"]
            valor = item["serie"].get(periodo)
            result[cod] = valor

    return result


def to_float(val: str | None) -> float | None:
    """Converte valor string do SIDRA para float, tratando casos especiais."""
    if val in (None, "-", "...", "X"):
        return None
    try:
        return float(str(val).replace(",", "."))
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Downloads
# ---------------------------------------------------------------------------

def download_populacao_total() -> dict[str, float | None]:
    """Tab 9514 — População residente total por município (Censo 2022)."""
    print("[1/8] Baixando população total...")
    data = fetch_sidra(9514, 93)
    time.sleep(1)
    return {k: to_float(v) for k, v in data.items()}


def download_populacao_faixas_etarias() -> dict[str, dict[str, float | None]]:
    """Tab 9514 — População por faixa etária 15-29 anos (Censo 2022).

    Categorias:
        93086 = 15 a 19 anos
        93087 = 20 a 24 anos
        93088 = 25 a 29 anos
    """
    print("[2/8] Baixando faixas etárias 15-29 anos...")
    result: dict[str, dict[str, float | None]] = {}

    faixas = {
        "pop_15_19": 93086,
        "pop_20_24": 93087,
        "pop_25_29": 93088,
    }
    for col, cat_id in faixas.items():
        data = fetch_sidra(9514, 93, classificacao=f"287[{cat_id}]%7C286[113635]%7C2[6794]")
        for cod, val in data.items():
            if cod not in result:
                result[cod] = {}
            result[cod][col] = to_float(val)
        time.sleep(1)

    return result


def download_urbanizacao() -> dict[str, float | None]:
    """Tab 9923 — Proporção da população urbana por município (Censo 2022).

    Categoria 1 = Urbana (situação do domicílio).
    """
    print("[3/8] Baixando urbanização (pop urbana)...")
    # Total
    data_total = fetch_sidra(9923, 93, classificacao="1[6795]")
    time.sleep(1)
    # Urbana
    data_urbana = fetch_sidra(9923, 93, classificacao="1[1]")
    time.sleep(1)

    result: dict[str, float | None] = {}
    for cod in data_total:
        total = to_float(data_total.get(cod))
        urbana = to_float(data_urbana.get(cod))
        if total and urbana and total > 0:
            result[cod] = round(urbana / total * 100, 4)
        else:
            result[cod] = None
    return result


def download_esgotamento_sanitario() -> dict[str, float | None]:
    """Tab 6805 — % de domicílios com esgotamento sanitário adequado (Censo 2022).

    Adequado = 'Rede geral, rede pluvial ou fossa ligada à rede' (cat 46290).
    """
    print("[4/8] Baixando esgotamento sanitário...")
    # Total de domicílios
    data_total = fetch_sidra(6805, 381, classificacao="11558[46292]")
    time.sleep(1)
    # Com esgotamento adequado
    data_adequado = fetch_sidra(6805, 381, classificacao="11558[46290]")
    time.sleep(1)

    result: dict[str, float | None] = {}
    for cod in data_total:
        total = to_float(data_total.get(cod))
        adequado = to_float(data_adequado.get(cod))
        if total and adequado and total > 0:
            result[cod] = round(adequado / total * 100, 4)
        else:
            result[cod] = None
    return result


def download_desemprego() -> dict[str, float | None]:
    """Tab 9517 — Taxa de desemprego (pessoas 14+ desocupadas / força de trabalho) (Censo 2022).

    Categoria 32386 = Força de trabalho total.
    Categoria 32446 = Desocupada.
    """
    print("[5/8] Baixando desemprego (força de trabalho)...")
    # Força de trabalho total
    forca = fetch_sidra(
        9517, 1641,
        classificacao="629[32386]%7C2[6794]%7C86[95251]%7C1568[120704]"
    )
    time.sleep(1)
    # Desocupados
    desoc = fetch_sidra(
        9517, 1641,
        classificacao="629[32446]%7C2[6794]%7C86[95251]%7C1568[120704]"
    )
    time.sleep(1)

    result: dict[str, float | None] = {}
    for cod in forca:
        ft = to_float(forca.get(cod))
        d = to_float(desoc.get(cod))
        if ft and d and ft > 0:
            result[cod] = round(d / ft * 100, 4)
        else:
            result[cod] = None
    return result


def download_renda_per_capita() -> dict[str, float | None]:
    """Tab 10295 — Rendimento domiciliar per capita médio mensal (Censo 2022).

    Variável 13431 = Valor do rendimento nominal médio mensal domiciliar per capita.
    """
    print("[6/8] Baixando renda per capita domiciliar...")
    data = fetch_sidra(10295, 13431)
    time.sleep(1)
    return {k: to_float(v) for k, v in data.items()}


def download_analfabetismo() -> dict[str, float | None]:
    """Tab 10135 — Taxa de analfabetismo das pessoas de 15+ anos (Censo 2022).

    Variável 10267 = Taxa de analfabetismo 15+.
    """
    print("[7/8] Baixando taxa de analfabetismo 15+...")
    data = fetch_sidra(10135, 10267)
    time.sleep(1)
    return {k: to_float(v) for k, v in data.items()}


def download_jovens_15_29(
    pop_total: dict[str, float | None],
    faixas: dict[str, dict[str, float | None]],
) -> dict[str, float | None]:
    """Calcula % jovens 15-29 anos a partir dos dados de faixas etárias."""
    print("[8/8] Calculando % jovens 15-29 anos...")
    result: dict[str, float | None] = {}
    for cod, total in pop_total.items():
        f = faixas.get(cod, {})
        p15 = f.get("pop_15_19")
        p20 = f.get("pop_20_24")
        p25 = f.get("pop_25_29")
        if total and p15 is not None and p20 is not None and p25 is not None and total > 0:
            jovens = p15 + p20 + p25
            result[cod] = round(jovens / total * 100, 4)
        else:
            result[cod] = None
    return result


# ---------------------------------------------------------------------------
# Montagem do dataset
# ---------------------------------------------------------------------------

def build_dataset(
    pop_total: dict,
    faixas: dict,
    urbanizacao: dict,
    esgoto: dict,
    desemprego: dict,
    renda: dict,
    analfabetismo: dict,
    jovens: dict,
) -> pd.DataFrame:
    """Monta DataFrame com todos os municípios e variáveis coletadas."""
    all_cods = sorted(pop_total.keys())

    rows = []
    for cod in all_cods:
        rows.append({
            "cod_ibge": cod,
            "pop_total": pop_total.get(cod),
            "pop_urbana_pct": urbanizacao.get(cod),
            "perc_jovens_15_29": jovens.get(cod),
            "renda_per_capita": renda.get(cod),
            "taxa_desemprego": desemprego.get(cod),
            "taxa_analfabetismo_15": analfabetismo.get(cod),
            "perc_esgoto_adequado": esgoto.get(cod),
        })

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("=== Download de dados socioeconômicos — Censo IBGE 2022 ===\n")

    pop_total = download_populacao_total()
    faixas = download_populacao_faixas_etarias()
    urbanizacao = download_urbanizacao()
    esgoto = download_esgotamento_sanitario()
    desemprego = download_desemprego()
    renda = download_renda_per_capita()
    analfabetismo = download_analfabetismo()
    jovens = download_jovens_15_29(pop_total, faixas)

    df = build_dataset(
        pop_total, faixas, urbanizacao, esgoto,
        desemprego, renda, analfabetismo, jovens,
    )

    out_path = RAW_DIR / "censo2022_municipios.csv"
    df.to_csv(out_path, index=False, encoding="utf-8")

    print(f"\n✓ Salvo: {out_path}")
    print(f"  Shape: {df.shape}")
    print(f"  Municípios: {len(df)}")
    print(f"\n  Nulos por coluna:")
    print(df.isnull().sum().to_string())

    print("\n=== Variáveis pendentes (requerem Atlas Brasil — Censo 2010) ===")
    print("  - idhm_geral")
    print("  - idhm_educacao")
    print("  - idhm_longevidade")
    print("  - idhm_renda")
    print("  - gini")
    print("  - perc_pobres")
    print("  Baixar manualmente em: http://www.atlasbrasil.org.br/consulta/planilha")
    print("  Salvar como: data/raw/atlas_brasil_municipios.csv")


if __name__ == "__main__":
    main()
