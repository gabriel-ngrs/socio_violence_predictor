# Socio Violence Predictor (Versao Apresentacao)

Projeto da disciplina de Aprendizagem de Maquina (UFPB, 2025.1), refatorado para **2 notebooks leves**.

Pergunta central: prever `alta_violencia` com indicadores socioeconomicos dos municipios.

## Estrutura final

```
notebooks/
├── 01_dados_eda_preprocessamento.ipynb
└── 02_modelagem_e_validacao.ipynb
```

- Notebook 01: coleta dos `raw`, tratamento, montagem do dataset, EDA minima, `X` e `y`, `N` e `p`, split e padronizacao.
- Notebook 02: treino e avaliacao de Rede Neural, Arvore de Decisao e SVM, com comparacao final.

## Como rodar

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
jupyter notebook notebooks/
```

Executar em ordem:
1. `01_dados_eda_preprocessamento.ipynb`
2. `02_modelagem_e_validacao.ipynb`

## Checklist do PDF

- Tratamento basico: construcao de `X` e `y`, `N` e `p`, split treino/teste, padronizacao.
- Rede Neural: dimensao VC, regra de ouro, `E_in`/`E_out`, grafico de overfitting, metricas.
- Arvore: arvore sem poda, `E_in`/`E_out`, regularizacao por `ccp_alpha` com cross validation, metricas.
- SVM: ajuste de `C` e `gamma` com cross validation, `E_in`, `E_out`, `E_out` esperado por vetores de suporte, metricas.
- Escolha do melhor modelo: comparacao final por F1 no teste apos validacao dos hiperparametros.

## Dados usados na apresentacao

- `data/raw/`: apenas os arquivos usados no pipeline:
  - `censo2022_municipios.csv`
  - `atlas_brasil_municipios.xlsx`
  - `ibge_municipios_ref.csv`
  - `pib_municipios_sidra_2021.csv`
  - `areas_municipios_2024.xls`
  - `sinesp_municipios.xlsx`
- `data/processed/`: inicia vazio (apenas `.gitkeep`) e e preenchido durante a execucao do notebook 01.
