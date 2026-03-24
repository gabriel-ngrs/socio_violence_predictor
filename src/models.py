"""
Módulo de definição dos modelos de aprendizagem de máquina.

Contém funções para construir, treinar e configurar os 3 modelos
exigidos: Rede Neural, Árvore de Decisão e SVM.
"""

import numpy as np
from typing import Tuple, Optional

from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV


def compute_vc_dimension(n_layers: list[int]) -> int:
    """Calcula a dimensão VC de uma rede neural MLP.

    Para uma rede com L camadas e n_l neurônios na camada l,
    a dimensão VC é aproximadamente o número total de pesos (incluindo bias).

    d_VC ≈ Σ (n_l + 1) * n_{l+1} para l = 0, ..., L-1

    Args:
        n_layers: Lista com o número de neurônios em cada camada
                  (incluindo entrada e saída).

    Returns:
        Estimativa da dimensão VC.
    """
    d_vc = 0
    for i in range(len(n_layers) - 1):
        d_vc += (n_layers[i] + 1) * n_layers[i + 1]  # +1 para o bias
    return d_vc


def golden_rule_check(n_samples: int, d_vc: int) -> dict:
    """Verifica a Regra de Ouro: N >= 10 * d_VC.

    Args:
        n_samples: Número de amostras de treino (N).
        d_vc: Dimensão VC do modelo.

    Returns:
        Dicionário com o resultado da verificação.
    """
    ratio = n_samples / d_vc if d_vc > 0 else float("inf")
    return {
        "N": n_samples,
        "d_vc": d_vc,
        "ratio_N_dvc": ratio,
        "satisfies_golden_rule": ratio >= 10,
        "message": (
            f"N/d_VC = {ratio:.1f} — {'satisfaz' if ratio >= 10 else 'NÃO satisfaz'} "
            f"a Regra de Ouro (N ≥ 10·d_VC)"
        ),
    }


def build_neural_network(
    input_dim: int,
    hidden_layers: list[int],
    learning_rate: float = 0.001,
):
    """Constrói o modelo de rede neural com Keras.

    A arquitetura deve ser justificada pela dimensão VC e Regra de Ouro.
    Usar o Teorema da Aproximação Universal (pelo menos 1 camada oculta).

    Args:
        input_dim: Número de features de entrada.
        hidden_layers: Lista com neurônios por camada oculta.
        learning_rate: Taxa de aprendizado do otimizador.

    Returns:
        Modelo Keras compilado.
    """
    raise NotImplementedError("TODO: Implementar construção da rede neural com Keras")


def train_neural_network(
    model,
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_val: np.ndarray,
    y_val: np.ndarray,
    epochs: int = 100,
    batch_size: int = 32,
):
    """Treina a rede neural e retorna o histórico.

    Args:
        model: Modelo Keras compilado.
        X_train: Features de treino.
        y_train: Alvo de treino.
        X_val: Features de validação.
        y_val: Alvo de validação.
        epochs: Número de épocas.
        batch_size: Tamanho do batch.

    Returns:
        Histórico de treinamento (history object do Keras).
    """
    raise NotImplementedError("TODO: Implementar treinamento da rede neural")


def build_decision_tree(random_state: int = 42) -> DecisionTreeClassifier:
    """Constrói uma árvore de decisão sem poda (para análise inicial de overfitting).

    Args:
        random_state: Seed para reprodutibilidade.

    Returns:
        DecisionTreeClassifier configurado.
    """
    return DecisionTreeClassifier(random_state=random_state)


def prune_decision_tree(
    X_train: np.ndarray,
    y_train: np.ndarray,
    cv_folds: int = 5,
    random_state: int = 42,
) -> Tuple[DecisionTreeClassifier, dict]:
    """Realiza pruning da árvore via Minimal Cost-Complexity com cross validation.

    Encontra o alpha ótimo que minimiza: Pureza(T) + alpha * #folhas(T)

    Args:
        X_train: Features de treino.
        y_train: Alvo de treino.
        cv_folds: Número de folds para cross validation.
        random_state: Seed para reprodutibilidade.

    Returns:
        Tupla (melhor_arvore, resultados_cv).
    """
    raise NotImplementedError("TODO: Implementar pruning com Minimal Cost-Complexity")


def build_svm(
    X_train: np.ndarray,
    y_train: np.ndarray,
    cv_folds: int = 5,
    random_state: int = 42,
) -> Tuple[SVC, GridSearchCV]:
    """Constrói e treina SVM com GridSearchCV para C e gamma.

    Args:
        X_train: Features de treino.
        y_train: Alvo de treino.
        cv_folds: Número de folds para cross validation.
        random_state: Seed para reprodutibilidade.

    Returns:
        Tupla (melhor_svm, grid_search_results).
    """
    raise NotImplementedError("TODO: Implementar SVM com GridSearchCV")


def svm_expected_eout(n_support_vectors: int, n_samples: int) -> float:
    """Calcula o E_out esperado do SVM baseado nos vetores de suporte.

    E_out_esperado ≈ n_support_vectors / n_samples

    Args:
        n_support_vectors: Número de vetores de suporte.
        n_samples: Número total de amostras de treino.

    Returns:
        E_out esperado.
    """
    return n_support_vectors / n_samples
