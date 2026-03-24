"""
Módulo de carregamento e cruzamento de dados.

Funções para carregar os datasets de diferentes fontes e cruzá-los
pelo código IBGE do município (7 dígitos).
"""

import pandas as pd
from pathlib import Path
from typing import Optional


# Caminhos padrão
RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"


def load_crime_data(filepath: Optional[Path] = None) -> pd.DataFrame:
    """Carrega dados de homicídios dolosos do Sinesp/MJ.

    Args:
        filepath: Caminho para o arquivo .xlsx. Se None, usa o padrão.

    Returns:
        DataFrame com colunas: cod_ibge, homicidios_dolosos.
    """
    raise NotImplementedError("TODO: Implementar carregamento dos dados de crime")


def load_atlas_brasil(filepath: Optional[Path] = None) -> pd.DataFrame:
    """Carrega dados do Atlas Brasil (IDHM, Gini, analfabetismo, renda, etc.).

    Args:
        filepath: Caminho para o CSV exportado do Atlas Brasil.

    Returns:
        DataFrame com indicadores socioeconômicos por município.
    """
    raise NotImplementedError("TODO: Implementar carregamento do Atlas Brasil")


def load_pib_municipal(filepath: Optional[Path] = None) -> pd.DataFrame:
    """Carrega dados de PIB per capita municipal do IBGE.

    Args:
        filepath: Caminho para o arquivo de PIB.

    Returns:
        DataFrame com colunas: cod_ibge, pib_per_capita.
    """
    raise NotImplementedError("TODO: Implementar carregamento do PIB municipal")


def load_populacao(filepath: Optional[Path] = None) -> pd.DataFrame:
    """Carrega dados populacionais do Censo 2022 (total, urbanização, faixa etária).

    Args:
        filepath: Caminho para os dados do Censo.

    Returns:
        DataFrame com colunas: cod_ibge, pop_total, taxa_urbanizacao, pct_jovens_15_29.
    """
    raise NotImplementedError("TODO: Implementar carregamento de dados populacionais")


def load_area_municipal(filepath: Optional[Path] = None) -> pd.DataFrame:
    """Carrega dados de área territorial dos municípios.

    Args:
        filepath: Caminho para o arquivo de áreas.

    Returns:
        DataFrame com colunas: cod_ibge, area_km2.
    """
    raise NotImplementedError("TODO: Implementar carregamento de áreas municipais")


def merge_datasets(
    crime: pd.DataFrame,
    atlas: pd.DataFrame,
    pib: pd.DataFrame,
    populacao: pd.DataFrame,
    area: pd.DataFrame,
) -> pd.DataFrame:
    """Cruza todos os datasets pelo código IBGE do município.

    Realiza left joins sucessivos usando cod_ibge como chave.
    Calcula variáveis derivadas (densidade demográfica, taxa de homicídios per capita).
    Cria a variável alvo binária (mediana como threshold).

    Args:
        crime: DataFrame com dados de homicídios.
        atlas: DataFrame com indicadores do Atlas Brasil.
        pib: DataFrame com PIB per capita.
        populacao: DataFrame com dados populacionais.
        area: DataFrame com áreas territoriais.

    Returns:
        DataFrame unificado com features (X) e variável alvo (y).
    """
    raise NotImplementedError("TODO: Implementar cruzamento dos datasets")


def build_target_variable(df: pd.DataFrame) -> pd.DataFrame:
    """Constrói a variável alvo binária a partir da taxa de homicídios.

    Calcula: (homicídios dolosos / população) × 100.000
    Threshold: mediana nacional
    1 = alta violência (acima da mediana)
    0 = baixa violência (abaixo da mediana)

    Args:
        df: DataFrame com colunas homicidios_dolosos e pop_total.

    Returns:
        DataFrame com coluna adicional 'alta_violencia' (0 ou 1).
    """
    raise NotImplementedError("TODO: Implementar construção da variável alvo")


def load_and_merge_all(raw_dir: Optional[Path] = None) -> pd.DataFrame:
    """Pipeline completo: carrega todos os dados e retorna o dataset unificado.

    Args:
        raw_dir: Diretório com os dados brutos. Se None, usa o padrão.

    Returns:
        DataFrame pronto para análise exploratória e modelagem.
    """
    raise NotImplementedError("TODO: Implementar pipeline completo de carregamento")
