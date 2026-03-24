"""
Módulo de pré-processamento de dados.

Funções para normalização, padronização, split treino/teste
e engenharia de features.
"""

import numpy as np
import pandas as pd
from typing import Tuple
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler


def split_features_target(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Separa o DataFrame em matriz de features X e vetor alvo y.

    Remove colunas não-feature (cod_ibge, alta_violencia, taxa_homicidios, etc.).

    Args:
        df: DataFrame completo com features e variável alvo.

    Returns:
        Tupla (X, y) onde X são as features e y é a variável alvo.
    """
    raise NotImplementedError("TODO: Implementar separação X/y")


def split_train_test(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.2,
    random_state: int = 42,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Divide os dados em treino e teste.

    A proporção deve ser justificada no relatório considerando
    o número de amostras disponíveis (~5.570).

    Args:
        X: Matriz de features.
        y: Vetor alvo.
        test_size: Proporção do conjunto de teste.
        random_state: Seed para reprodutibilidade.

    Returns:
        Tupla (X_train, X_test, y_train, y_test).
    """
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)


def normalize_features(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    method: str = "standard",
) -> Tuple[np.ndarray, np.ndarray, object]:
    """Aplica normalização/padronização nos dados.

    IMPORTANTE: O scaler é ajustado APENAS nos dados de treino
    e aplicado em ambos (treino e teste) para evitar data leakage.

    Args:
        X_train: Features de treino.
        X_test: Features de teste.
        method: 'standard' (z-score) ou 'minmax' (0-1).

    Returns:
        Tupla (X_train_scaled, X_test_scaled, scaler).
    """
    if method == "standard":
        scaler = StandardScaler()
    elif method == "minmax":
        scaler = MinMaxScaler()
    else:
        raise ValueError(f"Método desconhecido: {method}. Use 'standard' ou 'minmax'.")

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, scaler


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Trata valores ausentes no dataset.

    Estratégia a ser definida após análise exploratória.

    Args:
        df: DataFrame com possíveis valores ausentes.

    Returns:
        DataFrame sem valores ausentes.
    """
    raise NotImplementedError("TODO: Implementar tratamento de missing values")


def get_dataset_info(X: pd.DataFrame, y: pd.Series) -> dict:
    """Retorna informações sobre o dataset para o relatório.

    Args:
        X: Matriz de features.
        y: Vetor alvo.

    Returns:
        Dicionário com N (amostras), p (parâmetros), balance (distribuição de classes).
    """
    return {
        "N": len(X),
        "p": X.shape[1],
        "feature_names": list(X.columns),
        "class_balance": y.value_counts().to_dict(),
        "class_balance_pct": y.value_counts(normalize=True).to_dict(),
    }
