# ROADMAP — Socio Violence Predictor

Guia de estado e próximos passos do projeto. **Leia este arquivo ao iniciar qualquer sessão.**

---

## Contexto rápido

Projeto acadêmico da disciplina de Aprendizagem de Máquina — UFPB (2025.1).
**Pergunta central:** "É possível prever o nível de violência de um município brasileiro usando apenas indicadores socioeconômicos?"
**Abordagem:** Classificação binária sobre ~5.570 municípios brasileiros.
**Apresentação:** 31 de março de 2026.

---

## Documentos importantes — leia antes de agir

| Arquivo | O que contém |
|---------|-------------|
| `CLAUDE.md` | Regras críticas do projeto, modelos obrigatórios, convenções de código, fluxo de branches e Conventional Commits |
| `README.md` | Visão geral do projeto, fontes de dados, metodologia |
| `data/README.md` | Onde cada arquivo raw foi baixado e como usar |
| `data/processed/dataset_municipios.csv` | Dataset final pronto para uso (gerado pelo notebook 01) |

---

## Estado atual do projeto

### ✅ Concluído

- [x] **Setup do repositório** — branches `main`, `dev`, `dev-gabriel`; `.gitignore`; `requirements.txt`
- [x] **CLAUDE.md** — regras, fluxo Git, Conventional Commits
- [x] **Download dos dados brutos** (`data/raw/`)
  - `censo2022_municipios.csv` — 7 features via IBGE SIDRA (script: `data/download_sidra.py`)
  - `atlas_brasil_municipios.xlsx` — IDHM ×4, Gini, % pobres via Atlas Brasil (script: `data/download_atlas_brasil.py`)
  - `sinesp_municipios.xlsx` — homicídios dolosos 2018–2022 por município (variável alvo)
  - `pib_municipios_sidra_2021.csv` — PIB per capita via SIDRA tabela 5938 (baixado no notebook 01)
  - `areas_municipios_2024.xls` — áreas territoriais IBGE 2024 (para densidade)
  - `ibge_municipios_ref.csv` — lookup nome+UF → código IBGE (gerado no notebook 01)
- [x] **Notebook 01 — Coleta e Limpeza** (`notebooks/01_coleta_e_limpeza.ipynb`)
  - Lê e cruza todos os datasets pelo `cod_ibge`
  - Resolve lookup nome → código IBGE para o Atlas Brasil (26 municípios com nome divergente imputados pela mediana)
  - Constrói variável alvo: taxa homicídios / 100k hab → mediana (12,03) → binário
  - Imputa nulos pela mediana (máx. 0,59% de nulos por coluna)
  - Salva `data/processed/dataset_municipios.csv`: **5570 municípios × 18 colunas, zero nulos, 50%/50%**

---

### 🔲 Pendente — em ordem de execução

#### Etapa 2 — Análise Exploratória
- [x] **Notebook 02** (`notebooks/02_analise_exploratoria.ipynb`)
  - Distribuições de cada feature (histogramas, boxplots)
  - Matriz de correlação entre features
  - Análise bivariada: cada feature vs. `alta_violencia`
  - Identificar features com maior poder discriminativo
  - Todo texto explicativo em markdown (exigência do relatório)

#### Etapa 3 — Pré-processamento
- [x] **Notebook 03** (`notebooks/03_preprocessamento.ipynb`)
  - Split treino/teste **80/20 estratificado** por `alta_violencia` — **não tocar no teste até a etapa final**
  - Normalização/padronização: StandardScaler justificado (obrigatório para SVM e NN)
  - Salvo em `data/processed/`: `X_train.npy`, `X_test.npy`, `y_train.npy`, `y_test.npy`, `feature_names.txt`
  - Scaler salvo em `models/scaler.joblib`

#### Etapa 4 — Modelos (notebooks independentes)
- [x] **Notebook 04** (`notebooks/04_modelo_rede_neural.ipynb`) — Keras/TensorFlow
  - Arquitetura [15→16→8→1]: d_VC=401, N/d_VC=11.1 — satisfaz Regra de Ouro
  - Regularização L2 (λ=0.0001) + Dropout (10%) + Early Stopping (parou na época 110, melhor=85)
  - E_in=30.25%, E_out=33.48%, Gap=3.23% (sem overfitting)
  - Acurácia=66.5%, Precisão=65.6%, Recall=69.5%, F1=67.5%
- [x] **Notebook 05** (`notebooks/05_modelo_arvore_decisao.ipynb`) — Scikit-Learn
  - Sem poda: E_in=0%, E_out=39.3%, 821 folhas — overfitting severo comprovado
  - α ótimo=0.002514 por CV 10-fold / scoring=F1 (415 candidatos): prof=5, 11 folhas
  - Regra 1-SE avaliada e descartada (α=0.009144, 4 folhas, F1=63.1% — pior)
  - E_in=30.1%, E_out=34.2%, Gap=4.1% (sem overfitting)
  - Acurácia=65.8%, Precisão=65.3%, Recall=67.5%, F1=66.4%
- [x] **Notebook 06** (`notebooks/06_modelo_svm.ipynb`) — Scikit-Learn
  - GridSearchCV 5×5 (C×γ), cv=10-fold, scoring=F1: melhor C=100, γ=0.001
  - Vetores de suporte: 3233/4456 (72.6%) | E_out esperado ≤ 72.6% | E_out empírico=33.4% ✓
  - E_in=31.3%, E_out=33.4%, Gap=2.1% (sem overfitting)
  - Acurácia=66.6%, Precisão=65.1%, Recall=71.5%, F1=68.2% — **melhor modelo**

#### Etapa 5 — Comparação e Relatório
- [x] **Notebook 07** (`notebooks/07_comparacao_modelos.ipynb`)
  - Tabela comparativa: Acurácia, Precisão, Recall, F1, E_in, E_out, Gap
  - Curvas ROC sobrepostas com AUC; heatmap E_in/E_out/Gap
  - Modelo vencedor: SVM (F1=68.2%, AUC maior, gap=2.1%)
  - Resposta à pergunta central: Sim, com desempenho moderado (+16.6pp acima do acaso)
- [ ] **Relatório final** (`reports/relatorio.md`)
  - Descrever metodologia, resultados e conclusões em prosa
  - Mencionar limitações: dados Atlas Brasil são de 2010, 26 municípios imputados, subnotificação no Sinesp
- [ ] **Módulos `src/`** — refatorar funções reutilizadas dos notebooks em:
  - `src/data_loader.py` — carregar e cruzar datasets
  - `src/preprocessing.py` — normalização, split, feature engineering
  - `src/models.py` — definição dos 3 modelos
  - `src/evaluation.py` — métricas e plots padronizados
  - `src/utils.py` — funções auxiliares

---

## Dataset final — referência rápida

**Arquivo:** `data/processed/dataset_municipios.csv`

| Coluna | Descrição | Fonte | Ano |
|--------|-----------|-------|-----|
| `cod_ibge` | Código IBGE 7 dígitos | — | — |
| `pop_total` | População total | SIDRA 9514 | 2022 |
| `pop_urbana_pct` | % população urbana | SIDRA 9923 | 2022 |
| `perc_jovens_15_29` | % jovens 15–29 anos | SIDRA 9514 | 2022 |
| `renda_per_capita` | Rendimento domiciliar per capita (R$) | SIDRA 10295 | 2022 |
| `taxa_desemprego` | Taxa de desemprego (%) | SIDRA 9517 | 2022 |
| `taxa_analfabetismo_15` | Taxa de analfabetismo 15+ (%) | SIDRA 10135 | 2022 |
| `perc_esgoto_adequado` | % domicílios com esgoto adequado | SIDRA 6805 | 2022 |
| `gini` | Índice de Gini | Atlas Brasil | 2010 |
| `idhm` | IDHM geral | Atlas Brasil | 2010 |
| `idhm_renda` | IDHM Renda | Atlas Brasil | 2010 |
| `idhm_longevidade` | IDHM Longevidade | Atlas Brasil | 2010 |
| `idhm_educacao` | IDHM Educação | Atlas Brasil | 2010 |
| `perc_pobres` | % de pobres | Atlas Brasil | 2010 |
| `pib_per_capita` | PIB per capita (R$) | SIDRA 5938 | 2021 |
| `densidade_demografica` | Hab/km² | IBGE pop÷área | 2022/2024 |
| `taxa_homicidios` | Taxa por 100k hab (não usar como feature!) | Sinesp/MJ | 2022 |
| `alta_violencia` | **Variável alvo** — 1 se taxa > mediana (12,03) | Derivado | 2022 |

**Shape:** 5570 × 18 | **Nulos:** 0 | **Balanceamento:** 50% / 50%

---

## Regras que nunca devem ser esquecidas

1. `taxa_homicidios` e dados Sinesp **jamais entram como features (X)**
2. O conjunto de **teste não deve ser tocado** até a etapa final de métricas
3. **Cross-validation** em treino para todos os hiperparâmetros
4. Todos os notebooks precisam de **texto explicativo em markdown**
5. A arquitetura da rede neural deve ser **justificada via dimensão VC e Regra de Ouro**
6. Commits seguem **Conventional Commits** em português, sem mencionar IA
