"""
Script de download dos dados do Atlas Brasil (PNUD/IPEA/FJP).

Baixa os seguintes indicadores para todos os municípios brasileiros (Censo 2010):
- IDHM geral, Renda, Longevidade, Educação
- Índice de Gini
- % de pobres

Executar a partir da raiz do projeto:
    python data/download_atlas_brasil.py
"""

import json
import time
from pathlib import Path
from urllib.parse import unquote

import pandas as pd
import requests

RAW_DIR = Path(__file__).parent / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Configuração da sessão (cookies capturados da sessão do Atlas Brasil)
# ---------------------------------------------------------------------------

BASE_URL = "http://www.atlasbrasil.org.br"

# Mapeamento Atlas Brasil ID → nome do estado
STATES = {
    1: "Rondônia", 2: "Minas Gerais", 3: "Paraná", 4: "Pará",
    5: "Amazonas", 6: "Espírito Santo", 7: "Rio Grande do Sul", 8: "Maranhão",
    9: "Santa Catarina", 10: "Goiás", 11: "Ceará", 12: "Bahia",
    13: "Alagoas", 14: "Pernambuco", 15: "Rio Grande do Norte", 16: "Rio de Janeiro",
    17: "São Paulo", 18: "Mato Grosso", 19: "Roraima", 20: "Paraíba",
    21: "Mato Grosso do Sul", 22: "Sergipe", 23: "Acre", 24: "Tocantins",
    25: "Distrito Federal", 26: "Amapá", 27: "Piauí",
}

# Indicadores selecionados (id_indicador, id_ano=3 = Censo 2010)
# IDs confirmados via inspeção DOM do Atlas Brasil (atlasbrasil.org.br/consulta/planilha):
#   li[name="ind-109-1"] → id_indicador=109, Índice de Gini
#   li[name="ind-196-1"] → id_indicador=196, IDHM geral
#   li[name="ind-197-1"] → id_indicador=197, IDHM Renda
#   li[name="ind-198-1"] → id_indicador=198, IDHM Longevidade
#   li[name="ind-199-1"] → id_indicador=199, IDHM Educação
#   li[name="ind-92-1"]  → id_indicador=92,  % de pobres
INDICADORES_CENSO = [
    {"id_indicador": 109, "id_ano": 3},   # Índice de Gini
    {"id_indicador": 196, "id_ano": 3},   # IDHM geral
    {"id_indicador": 197, "id_ano": 3},   # IDHM Renda
    {"id_indicador": 198, "id_ano": 3},   # IDHM Longevidade
    {"id_indicador": 199, "id_ano": 3},   # IDHM Educação
    {"id_indicador": 92,  "id_ano": 3},   # % de pobres
]


def get_fresh_session() -> requests.Session:
    """Cria uma sessão com cookies frescos do Atlas Brasil."""
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})

    print("  Obtendo sessão do Atlas Brasil...")
    resp = session.get(f"{BASE_URL}/consulta/planilha", timeout=30)
    resp.raise_for_status()

    # Extrair CSRF token do HTML
    import re
    match = re.search(r'<meta name="csrf-token" content="([^"]+)"', resp.text)
    if match:
        csrf_token = match.group(1)
        session.headers.update({"X-XSRF-TOKEN": csrf_token})
        print(f"  Token CSRF obtido: {csrf_token[:20]}...")
    else:
        # Tentar pelo cookie XSRF-TOKEN
        xsrf = session.cookies.get("XSRF-TOKEN", "")
        if xsrf:
            csrf_token = unquote(xsrf)
            session.headers.update({"X-XSRF-TOKEN": csrf_token})
            print(f"  Token XSRF obtido via cookie.")
        else:
            raise RuntimeError("Não foi possível obter o CSRF token.")

    return session


def build_payload(state_ids: list[int]) -> dict:
    """Monta o payload da requisição de download para os estados especificados."""
    return {
        "territorialidades": {
            "entidades": [{
                "e": 2,
                "mun": [],
                "rm": [],
                "est": state_ids,
                "udh": [],
                "l": [f"-{sid}" for sid in state_ids],
            }]
        },
        "indicadores": {
            "cod_indicadores": INDICADORES_CENSO,
            "data_desagregacoes": [],
        },
        "pagination": {
            "current_page": 1,
            "last_page": 0,
            "per_page": 99999,
            "total": 0,
            "from": 0,
            "to": 0,
        },
        "ordenation": {"default": "asc"},
    }


def download_states(session: requests.Session, state_ids: list[int]) -> bytes | None:
    """Faz o download do xlsx para os estados especificados."""
    payload = build_payload(state_ids)
    resp = session.post(
        f"{BASE_URL}/api/dadosgridDowload",
        json=payload,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        timeout=120,
    )
    if resp.status_code == 200 and len(resp.content) > 1000:
        return resp.content
    print(f"  Erro HTTP {resp.status_code}: {resp.text[:200]}")
    return None


def main() -> None:
    print("=== Download Atlas Brasil — IDHM, Gini e % Pobres (Censo 2010) ===\n")

    all_ids = list(STATES.keys())  # 1..27
    session = get_fresh_session()

    # Tenta baixar todos os estados de uma vez
    print(f"\n[1/1] Tentando download de todos os {len(all_ids)} estados de uma vez...")
    content = download_states(session, all_ids)

    if content:
        out_path = RAW_DIR / "atlas_brasil_municipios.xlsx"
        out_path.write_bytes(content)
        print(f"\n✓ Arquivo salvo: {out_path} ({len(content)/1024:.0f} KB)")

        # Verificar conteúdo
        try:
            xl = pd.ExcelFile(out_path)
            print(f"  Abas: {xl.sheet_names}")
            df = xl.parse(xl.sheet_names[0])
            print(f"  Shape: {df.shape}")
            print(f"  Colunas: {list(df.columns)}")
            print(f"\n  Primeiras linhas:")
            print(df.head(3).to_string())
        except Exception as e:
            print(f"  Erro ao inspecionar xlsx: {e}")
    else:
        # Fallback: baixar estado por estado
        print("\nFallback: baixando estado por estado...")
        dfs = []
        for sid, nome in STATES.items():
            print(f"  [{sid}/27] {nome}...")
            content = download_states(session, [sid])
            if content:
                tmp_path = RAW_DIR / f"atlas_tmp_{sid}.xlsx"
                tmp_path.write_bytes(content)
                try:
                    xl = pd.ExcelFile(tmp_path)
                    df = xl.parse(xl.sheet_names[0])
                    dfs.append(df)
                    print(f"    OK — {len(df)} municípios")
                except Exception as e:
                    print(f"    Erro ao ler xlsx: {e}")
            else:
                print(f"    FALHOU")
            time.sleep(0.5)

        if dfs:
            df_all = pd.concat(dfs, ignore_index=True)
            out_path = RAW_DIR / "atlas_brasil_municipios.xlsx"
            df_all.to_excel(out_path, index=False)
            print(f"\n✓ Arquivo consolidado: {out_path} ({len(df_all)} linhas)")

            # Limpar temporários
            for sid in STATES:
                tmp = RAW_DIR / f"atlas_tmp_{sid}.xlsx"
                if tmp.exists():
                    tmp.unlink()


if __name__ == "__main__":
    main()
