"""
Funções utilitárias do projeto.

Helpers para I/O, formatação e operações comuns.
"""

import os
import joblib
import pandas as pd
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).parent.parent
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
MODELS_DIR = PROJECT_ROOT / "models"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"


def save_model(model: Any, filename: str) -> Path:
    """Salva um modelo treinado em disco.

    Args:
        model: Modelo treinado.
        filename: Nome do arquivo (sem extensão).

    Returns:
        Caminho completo do arquivo salvo.
    """
    filepath = MODELS_DIR / f"{filename}.joblib"
    joblib.dump(model, filepath)
    return filepath


def load_model(filename: str) -> Any:
    """Carrega um modelo salvo do disco.

    Args:
        filename: Nome do arquivo (sem extensão).

    Returns:
        Modelo carregado.
    """
    filepath = MODELS_DIR / f"{filename}.joblib"
    return joblib.load(filepath)


def save_processed_data(df: pd.DataFrame, filename: str = "dataset_municipios.csv") -> Path:
    """Salva o dataset processado.

    Args:
        df: DataFrame processado.
        filename: Nome do arquivo.

    Returns:
        Caminho completo do arquivo salvo.
    """
    filepath = DATA_PROCESSED / filename
    df.to_csv(filepath, index=False)
    return filepath


def load_processed_data(filename: str = "dataset_municipios.csv") -> pd.DataFrame:
    """Carrega o dataset processado.

    Args:
        filename: Nome do arquivo.

    Returns:
        DataFrame com o dataset processado.
    """
    filepath = DATA_PROCESSED / filename
    return pd.read_csv(filepath)


def ensure_dirs_exist() -> None:
    """Garante que todos os diretórios necessários existam."""
    for d in [DATA_RAW, DATA_PROCESSED, MODELS_DIR, FIGURES_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def standardize_ibge_code(code: Any) -> int:
    """Padroniza o código IBGE para inteiro de 7 dígitos.

    Args:
        code: Código IBGE em qualquer formato.

    Returns:
        Código IBGE como inteiro.
    """
    return int(str(code).strip().replace(".0", ""))
