# Socio Violence Predictor (Versao Apresentacao)

Projeto da disciplina de Aprendizagem de Maquina (UFPB, 2025.1), consolidado em 2 notebooks enxutos.

Objetivo: prever `alta_violencia` em municipios brasileiros com indicadores socioeconomicos.

## Estrutura

```
notebooks/
├── 01_dados_eda_preprocessamento.ipynb
└── 02_modelagem_e_validacao.ipynb
```

- Notebook 01:
  - carrega todos os dados em `data/raw/`
  - faz tratamento e cruzamento por `cod_ibge`
  - constroi o dataset final
  - executa EDA (distribuicoes, histogramas, boxplots, correlacoes, top features)
  - gera split/padronizacao e salva artefatos em `data/processed/`
- Notebook 02:
  - treina Rede Neural, Arvore de Decisao e SVM
  - calcula `E_in`, `E_out` e metricas
  - gera plots de validacao (overfitting, confusao, ROC, comparativos, threshold)
  - salva modelos em `models/` e resumo em `data/processed/model_results.csv`

## Como executar

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
jupyter notebook notebooks/
```

Ordem de execucao:
1. `01_dados_eda_preprocessamento.ipynb`
2. `02_modelagem_e_validacao.ipynb`

## Checklist da atividade

- Pre-processamento: `X`, `y`, `N`, `p`, split treino/teste, padronizacao.
- Rede Neural: dimensao VC, regra de ouro, overfitting, `E_in`/`E_out`, metricas.
- Arvore: sem poda, poda por `ccp_alpha` com CV, `E_in`/`E_out`, metricas.
- SVM: tuning de `C` e `gamma` por CV, `E_in`, `E_out`, `E_out` esperado.
- Comparacao final: escolha do melhor modelo por F1 no teste.

## Dados e artefatos

- `data/raw/`: contem somente os 6 arquivos usados no pipeline.
- `data/processed/`: artefatos gerados em tempo de execucao (nao versionados, exceto `.gitkeep`).
- `reports/figures/`: figuras geradas durante os notebooks (nao versionadas).
