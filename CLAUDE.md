# CLAUDE.md — Instruções para o Claude Code

## Contexto do Projeto

**Projeto acadêmico** da disciplina de Aprendizagem de Máquina — UFPB, semestre 2025.1.
Professores: Bruno Jefferson e Gilberto Farias.
Apresentação: 31 de março de 2026.

**Pergunta central:** "É possível prever o nível de violência de um município brasileiro usando apenas indicadores socioeconômicos?"

**Abordagem:** Classificação binária — prever se um município tem "alta violência" ou "baixa violência" (threshold = mediana da taxa de homicídios dolosos per capita), usando APENAS indicadores socioeconômicos como features.

**Documento da disciplina:** `docs/Projeto_da_disciplina_2025_2__1_.pdf`

## Regras Críticas

1. **Dados de crime NUNCA entram como features (X).** Eles só servem para construir a variável alvo (y). Features são exclusivamente socioeconômicas.
2. **Todos os notebooks devem ter texto explicativo** em markdown — não basta código. O relatório exige descrição em palavras.
3. **Cross validation** deve ser usado para regularização (árvore: alpha via Minimal Cost-Complexity; SVM: C e gamma via GridSearchCV).
4. **Dimensão VC** deve ser calculada para justificar a arquitetura da rede neural (Regra de Ouro + Teorema da Aproximação Universal). Lembrar do bias em cada neurônio.
5. **Conjunto de teste** não deve ser tocado até a fase final de métricas.
6. **Normalização/padronização** deve ser justificada.

## Modelos Obrigatórios

1. **Rede Neural** (Keras/TensorFlow) — arquitetura justificada via dimensão VC e Regra de Ouro
2. **Árvore de Decisão** (Scikit-Learn) — pruning via Minimal Cost-Complexity (alpha) + cross validation
3. **SVM** (Scikit-Learn) — GridSearchCV para C e gamma

## Dados

- **Variável alvo (y):** Sinesp/MJ — homicídios dolosos por município → taxa per capita (×100k) → mediana como threshold → binário
- **Features (X):** PIB per capita, IDHM (geral + 3 sub), Gini, taxa de urbanização, densidade demográfica, analfabetismo 15+, renda per capita, % pobres, desemprego 18+, % jovens 15-29, % esgotamento sanitário, população total
- **Chave de cruzamento:** código IBGE do município (7 dígitos)
- **Dataset final esperado:** ~5.570 linhas × ~13 features + 1 alvo

## Convenções de Código

- Python 3.10+
- Type hints em todas as funções
- Docstrings descritivas (Google style)
- Nomes de variáveis/funções em inglês
- Textos, comentários e documentação em português
- Imports organizados: stdlib → third-party → local

## Estrutura do Projeto

```
socio-violence-predictor/
├── CLAUDE.md                 # Este arquivo
├── README.md                 # Documentação do projeto
├── requirements.txt          # Dependências
├── .gitignore
├── docs/                     # Documento da disciplina
├── data/
│   ├── raw/                  # Dados brutos (gitignored)
│   ├── processed/            # Dados cruzados e limpos (gitignored)
│   └── README.md             # Onde baixar cada dataset
├── notebooks/
│   ├── 01_coleta_e_limpeza.ipynb
│   ├── 02_analise_exploratoria.ipynb
│   ├── 03_preprocessamento.ipynb
│   ├── 04_modelo_rede_neural.ipynb
│   ├── 05_modelo_arvore_decisao.ipynb
│   ├── 06_modelo_svm.ipynb
│   └── 07_comparacao_modelos.ipynb
├── src/
│   ├── data_loader.py        # Carregar e cruzar datasets
│   ├── preprocessing.py      # Normalização, split, feature engineering
│   ├── models.py             # Definição dos 3 modelos
│   ├── evaluation.py         # Métricas e plots
│   └── utils.py              # Funções auxiliares
├── reports/
│   ├── figures/              # Gráficos gerados
│   └── relatorio.md          # Relatório final
└── models/                   # Modelos salvos (gitignored)
```

## Como Rodar

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Baixar dados (ver data/README.md para instruções)

# 3. Executar notebooks em ordem
jupyter notebook notebooks/
```

## Métricas Exigidas

Para cada modelo: acurácia, precisão, recall, F1-score, E_in, E_out.
Para SVM: também E_out esperado baseado no número de vetores de suporte.
