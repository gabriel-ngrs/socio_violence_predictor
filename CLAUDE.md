# CLAUDE.md

Guia rapido para manter a versao de apresentacao enxuta.

## Fonte de verdade

- Documento da disciplina: `docs/Projeto_da_disciplina_2025_2__1_.pdf`
- Estrutura oficial para apresentacao: **2 notebooks**
  - `notebooks/01_dados_eda_preprocessamento.ipynb`
  - `notebooks/02_modelagem_e_validacao.ipynb`

## Regras do projeto

1. `taxa_homicidios` nunca entra em `X`; so serve para derivar/validar `y`.
2. Comentarios e markdowns devem ser curtos e objetivos.
3. Usar cross validation em Arvore (`ccp_alpha`) e SVM (`C`, `gamma`).
4. Mostrar dimensao VC e regra de ouro na Rede Neural.
5. Nao usar o conjunto de teste durante tuning.

## Escopo de cada notebook

- Notebook 01:
  - carga do dataset consolidado
  - checagem rapida (nulos, duplicados)
  - EDA minima
  - construcao de `X`, `y`, `N`, `p`
  - split treino/teste e padronizacao
  - exportacao de `X_train.npy`, `X_test.npy`, `y_train.npy`, `y_test.npy`, `feature_names.txt`, `models/scaler.joblib`

- Notebook 02:
  - treino e avaliacao de Rede Neural, Arvore e SVM
  - `E_in`, `E_out` e metricas
  - grafico de overfitting da Rede Neural
  - poda por Minimal Cost-Complexity na Arvore
  - `E_out` esperado do SVM com vetores de suporte
  - comparacao final e escolha do melhor modelo

## Git

Usar Conventional Commits:

```text
<tipo>(escopo): descricao curta
```
