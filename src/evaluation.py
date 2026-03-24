"""
Módulo de avaliação e comparação de modelos.

Funções para calcular métricas, plotar curvas de overfitting
e comparar os 3 modelos.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    """Calcula as métricas de qualidade exigidas.

    Args:
        y_true: Valores reais.
        y_pred: Valores preditos.

    Returns:
        Dicionário com acurácia, precisão, recall e F1-score.
    """
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred),
        "recall": recall_score(y_true, y_pred),
        "f1_score": f1_score(y_true, y_pred),
    }


def compute_ein_eout(
    model,
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray,
) -> dict:
    """Calcula E_in (erro no treino) e E_out (erro no teste).

    E_in = 1 - acurácia no treino
    E_out = 1 - acurácia no teste

    Args:
        model: Modelo treinado com método predict().
        X_train: Features de treino.
        y_train: Alvo de treino.
        X_test: Features de teste.
        y_test: Alvo de teste.

    Returns:
        Dicionário com E_in, E_out e indicador de overfitting.
    """
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    ein = 1 - accuracy_score(y_train, y_train_pred)
    eout = 1 - accuracy_score(y_test, y_test_pred)

    return {
        "E_in": ein,
        "E_out": eout,
        "gap": eout - ein,
        "overfitting": eout - ein > 0.05,  # threshold de 5%
    }


def plot_overfitting_curve(
    history,
    save_path: Optional[str] = None,
) -> None:
    """Plota curvas de loss e acurácia por época (E_in vs E_val) para rede neural.

    Identifica visualmente a época de melhor generalização (menor val_loss).

    Args:
        history: Objeto history retornado pelo Keras fit().
        save_path: Caminho para salvar o gráfico. Se None, apenas exibe.
    """
    hist = history.history
    epochs = range(1, len(hist['loss']) + 1)
    best_epoch = int(np.argmin(hist['val_loss'])) + 1

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Loss
    axes[0].plot(epochs, hist['loss'], label='Treino (E_in)', color='steelblue')
    axes[0].plot(epochs, hist['val_loss'], label='Validação (E_val)', color='tomato')
    axes[0].axvline(best_epoch, color='green', linestyle='--', linewidth=1.5,
                    label=f'Melhor época: {best_epoch}')
    axes[0].set_title('Curva de Loss por Época')
    axes[0].set_xlabel('Época')
    axes[0].set_ylabel('Binary Cross-Entropy Loss')
    axes[0].legend()

    # Accuracy
    axes[1].plot(epochs, hist['accuracy'], label='Treino', color='steelblue')
    axes[1].plot(epochs, hist['val_accuracy'], label='Validação', color='tomato')
    axes[1].axvline(best_epoch, color='green', linestyle='--', linewidth=1.5,
                    label=f'Melhor época: {best_epoch}')
    axes[1].set_title('Acurácia por Época')
    axes[1].set_xlabel('Época')
    axes[1].set_ylabel('Acurácia')
    axes[1].legend()

    plt.suptitle('Análise de Overfitting — Rede Neural', fontsize=14)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Melhor época (menor val_loss): {best_epoch} / {len(epochs)}")


def plot_confusion_matrix(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    title: str = "Matriz de Confusão",
    save_path: Optional[str] = None,
) -> None:
    """Plota a matriz de confusão.

    Args:
        y_true: Valores reais.
        y_pred: Valores preditos.
        title: Título do gráfico.
        save_path: Caminho para salvar. Se None, apenas exibe.
    """
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["Baixa Violência", "Alta Violência"],
        yticklabels=["Baixa Violência", "Alta Violência"],
    )
    plt.title(title)
    plt.ylabel("Real")
    plt.xlabel("Predito")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


def compare_models(results: dict) -> None:
    """Compara os 3 modelos lado a lado.

    Args:
        results: Dicionário com resultados de cada modelo.
                 Ex: {"Rede Neural": {...}, "Árvore de Decisão": {...}, "SVM": {...}}
    """
    raise NotImplementedError("TODO: Implementar comparação visual dos modelos")


def print_classification_report(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    model_name: str = "Modelo",
) -> None:
    """Imprime o relatório de classificação formatado.

    Args:
        y_true: Valores reais.
        y_pred: Valores preditos.
        model_name: Nome do modelo para o título.
    """
    print(f"\n{'='*60}")
    print(f"Relatório de Classificação — {model_name}")
    print(f"{'='*60}")
    print(classification_report(
        y_true, y_pred,
        target_names=["Baixa Violência", "Alta Violência"],
    ))
