# Socio Violence Predictor

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Licença](https://img.shields.io/badge/licença-acadêmico-green)

Predição do nível de violência de municípios brasileiros usando indicadores socioeconômicos.

## Sobre o Projeto

**Pergunta central:** "É possível prever o nível de violência de um município brasileiro usando apenas indicadores socioeconômicos?"

Este projeto investiga a relação entre condições socioeconômicas e violência nos ~5.570 municípios brasileiros. A abordagem é de **classificação binária**: prever se um município tem "alta violência" ou "baixa violência" (threshold = mediana nacional da taxa de homicídios dolosos per capita), utilizando **exclusivamente** indicadores socioeconômicos como features.

A premissa é que, se o modelo conseguir boa acurácia, a violência é fortemente determinada por fatores estruturais (desigualdade, pobreza, urbanização). Se errar bastante, existem fatores não capturados por indicadores socioeconômicos (facções, tráfico, gestão local). Em ambos os cenários, a conclusão é relevante para políticas públicas.

## Dados

### Variável Alvo (y)

| Dado | Fonte | Link |
|------|-------|------|
| Homicídios dolosos por município | Sinesp / Ministério da Justiça | [dados.mj.gov.br](http://dados.mj.gov.br/dataset/210b9ae2-21fc-4986-89c6-2006eb4db247/resource/03af7ce2-174e-4ebd-b085-384503cfb40f/download/indicadoressegurancapublicamunic.xlsx) |

> **Nota:** Os dados de crime são usados **apenas** para construir a variável alvo. Nunca entram como features.

### Features (X) — Indicadores Socioeconômicos

| Feature | Fonte |
|---------|-------|
| PIB per capita | IBGE PIB Municípios (SIDRA Tabela 5938) |
| IDHM (geral + 3 subíndices) | Atlas Brasil (PNUD/IPEA/FJP) |
| Índice de Gini | Atlas Brasil |
| Taxa de urbanização | IBGE Censo 2022 |
| Densidade demográfica | IBGE (população / área) |
| Taxa de analfabetismo 15+ | Atlas Brasil |
| Renda per capita | Atlas Brasil |
| % de pobres | Atlas Brasil |
| Taxa de desemprego 18+ | Atlas Brasil |
| % população jovem 15-29 | IBGE Censo 2022 (SIDRA) |
| % com esgotamento sanitário | Atlas Brasil |
| População total | IBGE Censo 2022 (SIDRA Tabela 9514) |

Detalhes completos em [`data/README.md`](data/README.md).

## Metodologia

### Pipeline

1. **Coleta e limpeza** — download e padronização dos dados de múltiplas fontes
2. **Análise exploratória** — distribuições, correlações, análise espacial
3. **Pré-processamento** — normalização/padronização, split treino/teste, tratamento de missing values
4. **Modelagem** — treinar e avaliar 3 modelos
5. **Comparação** — selecionar o melhor modelo via estratégia de validação

### Modelos

| Modelo | Biblioteca | Regularização |
|--------|-----------|---------------|
| Rede Neural | Keras/TensorFlow | Arquitetura via dimensão VC e Regra de Ouro |
| Árvore de Decisão | Scikit-Learn | Minimal Cost-Complexity (alpha) + cross validation |
| SVM | Scikit-Learn | GridSearchCV para C e gamma |

### Métricas

- Acurácia, Precisão, Recall, F1-Score
- E_in e E_out para análise de overfitting
- E_out esperado (SVM, baseado em vetores de suporte)

## Estrutura do Repositório

```
socio-violence-predictor/
├── CLAUDE.md                    # Instruções para o Claude Code
├── README.md                    # Este arquivo
├── requirements.txt             # Dependências Python
├── docs/                        # Documento da disciplina
├── data/
│   ├── raw/                     # Dados brutos (gitignored)
│   ├── processed/               # Dados limpos e cruzados (gitignored)
│   └── README.md                # Instruções de download
├── notebooks/
│   ├── 01_coleta_e_limpeza.ipynb
│   ├── 02_analise_exploratoria.ipynb
│   ├── 03_preprocessamento.ipynb
│   ├── 04_modelo_rede_neural.ipynb
│   ├── 05_modelo_arvore_decisao.ipynb
│   ├── 06_modelo_svm.ipynb
│   └── 07_comparacao_modelos.ipynb
├── src/
│   ├── data_loader.py           # Carregar e cruzar datasets
│   ├── preprocessing.py         # Normalização, split, feature engineering
│   ├── models.py                # Definição dos 3 modelos
│   ├── evaluation.py            # Métricas e plots
│   └── utils.py                 # Funções auxiliares
├── reports/
│   ├── figures/                 # Gráficos gerados
│   └── relatorio.md             # Relatório final
└── models/                      # Modelos salvos (gitignored)
```

## Como Executar

### 1. Clonar e instalar dependências

```bash
git clone <url-do-repositorio>
cd socio-violence-predictor
pip install -r requirements.txt
```

### 2. Baixar os dados

Siga as instruções em [`data/README.md`](data/README.md) para baixar todos os datasets necessários e colocá-los em `data/raw/`.

### 3. Executar os notebooks

Abra o Jupyter e execute os notebooks **em ordem numérica**:

```bash
jupyter notebook notebooks/
```

1. `01_coleta_e_limpeza.ipynb` — Carrega, limpa e cruza os dados
2. `02_analise_exploratoria.ipynb` — Análise exploratória e visualizações
3. `03_preprocessamento.ipynb` — Normalização e split treino/teste
4. `04_modelo_rede_neural.ipynb` — Treina e avalia a rede neural
5. `05_modelo_arvore_decisao.ipynb` — Treina e avalia a árvore de decisão
6. `06_modelo_svm.ipynb` — Treina e avalia o SVM
7. `07_comparacao_modelos.ipynb` — Compara os 3 modelos e seleciona o melhor

## Resultados

> *Seção a ser preenchida após a execução dos modelos.*

## Disciplina

- **Universidade:** Universidade Federal da Paraíba (UFPB)
- **Centro:** Centro de Informática (CI)
- **Disciplina:** Aprendizagem de Máquina
- **Semestre:** 2025.1
- **Professores:** Bruno Jefferson de Sousa Pessoa e Gilberto Farias de Sousa Filho

## Autores

> *Adicionar nomes dos integrantes do grupo.*
