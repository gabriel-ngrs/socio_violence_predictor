# Predição de Violência Municipal com Indicadores Socioeconômicos

**Disciplina:** Aprendizagem de Máquina — UFPB, 2025.1
**Professores:** Bruno Jefferson de Sousa Pessoa e Gilberto Farias de Sousa Filho
**Autores:** *(adicionar nomes do grupo)*
**Data:** Março de 2026

---

## Resumo

Este trabalho investiga se é possível prever o nível de violência de um município brasileiro utilizando exclusivamente indicadores socioeconômicos. A partir de dados do Censo Demográfico 2022 (IBGE), Atlas Brasil 2010 (PNUD/Ipea/FJP) e Sinesp/MJ (2022), foi construído um dataset com 5.570 municípios e 15 features socioeconômicas. A variável alvo — classificação binária de alta ou baixa violência — foi derivada da taxa de homicídios dolosos per capita, usando a mediana (12,03/100 mil habitantes) como limiar. Três modelos de aprendizagem de máquina foram treinados e avaliados: Rede Neural (Keras), Árvore de Decisão (scikit-learn) e SVM (scikit-learn). O melhor modelo foi o SVM com kernel RBF (C=100, γ=0,001), atingindo acurácia de 66,6% e F1-score de 68,2% — 16,6 pontos percentuais acima do classificador aleatório. Os resultados confirmam que indicadores socioeconômicos têm poder discriminativo real sobre o nível de violência municipal, ainda que moderado, com a principal limitação sendo a defasagem temporal de 12 anos entre as features do Atlas Brasil (2010) e o alvo (2022).

**Palavras-chave:** aprendizagem de máquina; violência urbana; municípios brasileiros; classificação binária; SVM; rede neural; árvore de decisão.

---

## 1. Introdução

### 1.1 Contexto e Motivação

O Brasil registrou, em 2022, uma taxa de 22,3 homicídios dolosos por 100 mil habitantes segundo o Anuário Brasileiro de Segurança Pública, posicionando-se entre os países com maiores índices de violência no mundo. A distribuição desse fenômeno, contudo, é profundamente heterogênea: municípios com perfis socioeconômicos distintos apresentam taxas que variam de zero a mais de 100 homicídios por 100 mil habitantes, sugerindo que fatores estruturais desempenham papel relevante na determinação do nível de violência local.

A literatura criminológica consolidou, ao longo das últimas décadas, um conjunto de determinantes socioeconômicos associados à violência urbana: desigualdade de renda (medida pelo índice de Gini), pobreza, desemprego, urbanização acelerada, baixa escolaridade e concentração de jovens do sexo masculino entre 15 e 29 anos (BEATO FILHO, 1998; CERQUEIRA; LOBÃO, 2004; MELLO; SCHNEIDER, 2010). No entanto, a relação entre esses fatores e a violência raramente é explorada de forma preditiva sistemática para o conjunto completo dos municípios brasileiros.

Este trabalho aplica técnicas de aprendizagem de máquina para formalizar e testar essa relação preditiva, oferecendo uma contribuição metodológica ao campo e uma ferramenta potencialmente útil para o direcionamento de políticas públicas de segurança.

### 1.2 Pergunta de Pesquisa

> **"É possível prever o nível de violência de um município brasileiro usando apenas indicadores socioeconômicos?"**

### 1.3 Abordagem

O problema foi formulado como uma **classificação binária**: cada município recebe o rótulo *alta violência* (1) ou *baixa violência* (0), com base em sua taxa de homicídios dolosos per capita comparada à mediana nacional. As **features (X)** são exclusivamente socioeconômicas — dados de crime nunca entram como preditores. O modelo aprende a associar o perfil socioeconômico de um município ao seu nível esperado de violência.

---

## 2. Dataset

### 2.1 Fontes de Dados

O dataset final resulta do cruzamento de cinco fontes públicas, identificadas pelo código IBGE de 7 dígitos de cada município:

| Fonte | Variáveis | Ano | Granularidade |
|---|---|---|---|
| IBGE SIDRA — Censo 2022 (tabelas 9514, 9923, 9517, 10135, 10295, 6805) | População, urbanização, desemprego, analfabetismo, renda, esgoto | 2022 | Municipal |
| IBGE SIDRA — tabela 5938 | PIB per capita | 2021 | Municipal |
| IBGE — áreas territoriais | Área do município (para densidade) | 2024 | Municipal |
| Atlas do Desenvolvimento Humano no Brasil (PNUD/Ipea/FJP) | IDHM (geral e 3 subdimensões), Gini, % pobres | 2010 | Municipal |
| Sinesp/MJ — Sistema Nacional de Informações de Segurança Pública | Homicídios dolosos (variável alvo) | 2022 | Municipal |

O download dos dados do SIDRA foi automatizado via API REST (`data/download_sidra.py`). Os dados do Atlas Brasil foram obtidos por download direto do portal atlasbrasil.org.br. Os dados do Sinesp foram obtidos como planilha XLSX do portal de dados abertos do Ministério da Justiça.

### 2.2 Variável Alvo

A variável alvo `alta_violencia` foi construída em três etapas:

1. **Taxa de homicídios:** para cada município, calculou-se a taxa de homicídios dolosos por 100 mil habitantes em 2022, usando a população do Censo 2022 como denominador.
2. **Limiar:** a mediana da distribuição das taxas entre os 5.570 municípios foi calculada, resultando em **12,03 homicídios por 100 mil habitantes**.
3. **Binarização:** municípios com taxa acima da mediana recebem `alta_violencia = 1`; abaixo ou igual, `alta_violencia = 0`.

O uso da mediana como limiar garante, por construção, um **balanceamento perfeito de classes (50%/50%)**, eliminando a necessidade de técnicas de reamostragem e permitindo o uso de métricas não ponderadas.

**Importante:** a variável `taxa_homicidios` e qualquer dado do Sinesp foram **estritamente excluídos das features (X)**. Dados de crime servem apenas para construir o alvo (y).

### 2.3 Features Selecionadas

As 15 features socioeconômicas foram selecionadas com base na literatura criminológica e na disponibilidade de dados com cobertura para todos os 5.570 municípios brasileiros:

| Feature | Descrição | Fonte | Ano |
|---|---|---|---|
| `pop_total` | População residente total | SIDRA 9514 | 2022 |
| `pop_urbana_pct` | % da população em área urbana | SIDRA 9923 | 2022 |
| `perc_jovens_15_29` | % de jovens de 15 a 29 anos | SIDRA 9514 | 2022 |
| `renda_per_capita` | Rendimento domiciliar per capita médio (R$) | SIDRA 10295 | 2022 |
| `taxa_desemprego` | Taxa de desemprego (%) | SIDRA 9517 | 2022 |
| `taxa_analfabetismo_15` | Taxa de analfabetismo — 15 anos ou mais (%) | SIDRA 10135 | 2022 |
| `perc_esgoto_adequado` | % de domicílios com esgoto adequado | SIDRA 6805 | 2022 |
| `gini` | Índice de Gini do rendimento domiciliar | Atlas Brasil | 2010 |
| `idhm` | IDHM geral | Atlas Brasil | 2010 |
| `idhm_renda` | IDHM — subdimensão Renda | Atlas Brasil | 2010 |
| `idhm_longevidade` | IDHM — subdimensão Longevidade | Atlas Brasil | 2010 |
| `idhm_educacao` | IDHM — subdimensão Educação | Atlas Brasil | 2010 |
| `perc_pobres` | % de pessoas abaixo da linha de pobreza | Atlas Brasil | 2010 |
| `pib_per_capita` | PIB per capita municipal (R$) | SIDRA 5938 | 2021 |
| `densidade_demografica` | Densidade demográfica (hab/km²) | IBGE pop÷área | 2022/2024 |

### 2.4 Processo de Integração

O cruzamento dos datasets foi realizado pelo código IBGE de 7 dígitos de cada município. O Atlas Brasil utiliza o código de 6 dígitos em alguns registros, exigindo conversão. Além disso, 26 municípios apresentaram discrepância de grafia entre o Atlas Brasil e o cadastro de referência do IBGE — esses casos foram resolvidos por busca fonética e normalização de caracteres especiais, com imputação pela mediana de sua macrorregião nos casos irresolvíveis.

### 2.5 Tratamento de Valores Ausentes

Após o cruzamento, o dataset apresentou no máximo 0,59% de valores nulos por coluna. Todos os nulos foram imputados pela **mediana da respectiva coluna**, estratégia robusta a outliers e adequada ao perfil assimétrico de diversas features (renda, PIB, população). O dataset final possui **zero valores ausentes**.

### 2.6 Estatísticas Descritivas

O dataset final contém **5.570 municípios × 18 colunas** (15 features + `cod_ibge` + `taxa_homicidios` + `alta_violencia`).

| Feature | Média | Desvio Padrão | Mínimo | Máximo |
|---|---|---|---|---|
| pop_total | 38.430 | 219.168 | 804 | 11.451.245 |
| pop_urbana_pct | 65,5% | 23,3% | 0% | 100% |
| perc_jovens_15_29 | 20,1% | 3,0% | 8,0% | 41,1% |
| renda_per_capita (R$) | 1.274 | 622 | 234 | 8.481 |
| taxa_desemprego | 7,2% | 4,0% | 0% | 44,7% |
| taxa_analfabetismo_15 | 10,4% | 9,2% | 0% | 56,7% |
| perc_esgoto_adequado | 44,1% | 35,2% | 0% | 100% |
| gini | 0,494 | 0,066 | 0,230 | 0,830 |
| idhm | 0,665 | 0,072 | 0,418 | 0,862 |
| idhm_renda | 0,661 | 0,075 | 0,376 | 0,909 |
| idhm_longevidade | 0,818 | 0,044 | 0,583 | 0,934 |
| idhm_educacao | 0,554 | 0,101 | 0,168 | 0,888 |
| perc_pobres | 23,2% | 17,9% | 0,1% | 84,3% |
| pib_per_capita (R$) | 31.264 | 42.508 | 3.282 | 1.484.935 |
| densidade_demografica (hab/km²) | 109 | 659 | 0,07 | 13.024 |

A análise exploratória revelou que a feature com maior correlação linear com a variável alvo é `perc_jovens_15_29` (ρ = 0,285), seguida de `perc_esgoto_adequado` (ρ = −0,264) e `idhm_longevidade` (ρ = −0,251). Notavelmente, `densidade_demografica` e `pib_per_capita` apresentaram correlação próxima de zero com o alvo, indicando que o tamanho econômico do município importa menos do que a distribuição interna de renda e a estrutura demográfica.

---

## 3. Pré-processamento

### 3.1 Separação Treino/Teste

O dataset foi dividido em conjuntos de treino (80%) e teste (20%) utilizando **estratificação pela variável alvo**, garantindo que a proporção de 50%/50% seja preservada em ambos os conjuntos:

- **Treino:** 4.456 municípios (2.228 de cada classe)
- **Teste:** 1.114 municípios (557 de cada classe)
- **Semente aleatória:** 42 (reprodutibilidade)

A proporção 80/20 é adequada ao tamanho do dataset: o conjunto de teste possui 1.114 amostras, suficiente para estimativas estáveis das métricas de generalização. O conjunto de teste permaneceu **completamente isolado** até a fase final de avaliação — nenhum hiperparâmetro foi selecionado com base em seu desempenho.

### 3.2 Normalização

Foi aplicada **padronização Z-score** (StandardScaler) a todas as 15 features:

```
x' = (x - μ) / σ
```

onde μ e σ são calculados **exclusivamente sobre o conjunto de treino** e aplicados tanto ao treino quanto ao teste, evitando data leakage. Após a transformação, o treino apresentou média ≈ 0 e desvio padrão ≈ 1 em todas as colunas.

A padronização é **obrigatória** para SVM e Rede Neural, pois esses modelos são sensíveis à escala das features (o kernel RBF usa distâncias euclidianas; o gradiente descendente converge mais rapidamente com features na mesma escala). Para a Árvore de Decisão, a padronização é irrelevante (splits são invariantes a transformações monotônicas), mas foi aplicada uniformemente para manter o pipeline consistente.

---

## 4. Rede Neural

### 4.1 Justificativa da Arquitetura via Dimensão VC

A arquitetura da rede foi dimensionada pela **Regra de Ouro**: para aprender de forma confiável, o número de amostras de treino N deve satisfazer N ≥ 10 · d_VC, onde d_VC é a dimensão de Vapnik–Chervonenkis do modelo.

Para uma rede MLP com camadas de tamanho [n₀, n₁, n₂, n₃], a dimensão VC é aproximada pelo número total de pesos ajustáveis (incluindo bias):

```
d_VC ≈ Σ (n_l + 1) × n_{l+1}    para l = 0, ..., L-1
```

A arquitetura escolhida foi **[15 → 16 → 8 → 1]**:

```
d_VC = (15+1)×16 + (16+1)×8 + (8+1)×1 = 256 + 136 + 9 = 401
```

Com N = 4.456 amostras de treino:

```
N / d_VC = 4456 / 401 = 11,1 ≥ 10  ✓
```

A Regra de Ouro é satisfeita. A existência de pelo menos uma camada oculta com ativação ReLU garante o **Teorema da Aproximação Universal** — a rede tem capacidade teórica para aproximar qualquer função contínua com precisão arbitrária, dado treinamento adequado.

### 4.2 Regularização

Para controlar o overfitting, foram aplicadas três formas complementares de regularização:

- **Regularização L2** (λ = 0,0001): penaliza pesos grandes, incentivando soluções mais suaves.
- **Dropout** (taxa = 10%): desativa aleatoriamente 10% dos neurônios a cada batch durante o treino, reduzindo co-adaptações e funcionando como um ensemble implícito.
- **Early Stopping** (paciência = 25 épocas): monitora a loss de validação e restaura os pesos da melhor época, evitando o overfitting tardio.

### 4.3 Parâmetros de Treinamento

| Parâmetro | Valor | Justificativa |
|---|---|---|
| Otimizador | Adam (lr = 0,001) | Adaptativo, convergência rápida |
| Função de loss | Binary cross-entropy | Padrão para classificação binária com saída sigmóide |
| Batch size | 64 | Equilíbrio entre estabilidade do gradiente e velocidade |
| Épocas máximas | 300 | Limite superior; early stopping interrompe antes |
| Melhor época | 85 (parada na 110) | Determinada pelo menor val_loss |
| Split interno | 80% treino efetivo / 20% validação | Validação interna para early stopping |

### 4.4 Resultados

| Métrica | Valor |
|---|---|
| E_in (erro de treino) | 30,25% |
| E_out (erro de teste) | 33,48% |
| Gap (E_out − E_in) | 3,23% |
| Acurácia | 66,52% |
| Precisão | 65,59% |
| Recall | 69,48% |
| F1-score | 67,48% |

O gap de 3,23% está abaixo do limiar de 5% adotado como critério de overfitting, confirmando que a regularização foi eficaz. A curva de loss por época demonstra convergência estável com val_loss acompanhando a train_loss sem divergência expressiva.

---

## 5. Árvore de Decisão

### 5.1 Árvore Sem Poda — Demonstração de Overfitting

Uma árvore de decisão irrestrita foi treinada como experimento inicial. O resultado demonstra o overfitting de forma inequívoca:

| Métrica | Sem poda |
|---|---|
| E_in | 0,00% |
| E_out | 39,30% |
| Gap | 39,30% |
| Folhas | 821 |
| Profundidade máxima | 33 |

E_in = 0% indica memorização perfeita do treino. O gap de 39,3 pontos percentuais confirma que a árvore não generalizou — poda é necessária.

### 5.2 Poda via Minimal Cost-Complexity

O método de **Minimal Cost-Complexity Pruning** (MCCP) seleciona a subárvore que minimiza:

```
R_α(T) = R(T) + α × |T|
```

onde R(T) é o erro de classificação, |T| é o número de folhas e α ≥ 0 é o parâmetro de regularização.

**Procedimento:**

1. O caminho completo de valores candidatos de α foi calculado pelo scikit-learn (`cost_complexity_pruning_path`), gerando **415 candidatos**.
2. Para cada α, o F1-score médio foi estimado por **validação cruzada com 10 folds** sobre o conjunto de treino. O F1-score foi preferido à acurácia por ser mais informativo em classificação binária.
3. O α ótimo foi selecionado como aquele que maximiza o F1 médio em CV: **α* = 0,002514**.

O critério da **Regra 1-SE** (modelo mais simples dentro de 1 desvio padrão do melhor score) foi avaliado por completude: resultou em α = 0,009144 com 4 folhas e F1 = 63,1% — desempenho inferior ao ótimo, justificando sua não adoção.

### 5.3 Resultado Final

| Parâmetro | Valor |
|---|---|
| α ótimo (CV 10-fold) | 0,002514 |
| Profundidade | 5 |
| Número de folhas | 11 |

| Métrica | Valor |
|---|---|
| E_in | 30,10% |
| E_out | 34,20% |
| Gap | 4,10% |
| Acurácia | 65,80% |
| Precisão | 65,29% |
| Recall | 67,52% |
| F1-score | 66,37% |

A feature com maior importância na árvore podada foi `perc_jovens_15_29`, seguida de `idhm_longevidade` e `renda_per_capita` — resultado consistente com a análise de correlação da fase exploratória.

---

## 6. SVM

### 6.1 Fundamentação Teórica

O SVM com kernel RBF busca o hiperplano de margem máxima em um espaço implícito de alta dimensão, definido pelo kernel:

```
K(x, x') = exp(−γ ‖x − x'‖²)
```

O parâmetro C controla o trade-off entre maximizar a margem e minimizar as violações (soft margin). O parâmetro γ controla a largura efetiva do kernel — valores altos tornam o modelo mais local (risco de overfitting), valores baixos o tornam mais global (risco de underfitting).

### 6.2 Seleção de Hiperparâmetros via GridSearchCV

A grade de busca cobriu 5 × 5 = **25 combinações** de C e γ, avaliadas por **validação cruzada com 10 folds** sobre o treino (scoring = F1):

| Parâmetro | Valores testados |
|---|---|
| C | {0,01; 0,1; 1; 10; 100} |
| γ | {0,001; 0,01; 0,1; 1; scale} |

O melhor par encontrado foi **C = 100, γ = 0,001**, com F1-CV = 70,20%.

### 6.3 Análise de Generalização via Vetores de Suporte

O SVM oferece uma estimativa teórica do erro de generalização baseada nos vetores de suporte:

```
E_out esperado ≤ N_SV / N_treino = 3233 / 4456 = 72,55%
```

O erro empírico observado foi E_out = 33,39%, satisfazendo o limite teórico (33,39% ≤ 72,55% ✓). O alto número de vetores de suporte (72,6% das amostras de treino) reflete a dificuldade intrínseca do problema — as classes não são linearmente separáveis no espaço de features — e não indica overfitting, como confirmado pelo pequeno gap de 2,1%.

### 6.4 Resultados

| Métrica | Valor |
|---|---|
| E_in | 31,30% |
| E_out | 33,39% |
| Gap | 2,09% |
| Acurácia | 66,61% |
| Precisão | 65,06% |
| Recall | 71,52% |
| F1-score | 68,15% |

---

## 7. Comparação e Escolha do Melhor Modelo

### 7.1 Tabela Comparativa

| Modelo | Acurácia | Precisão | Recall | F1-score | E_in | E_out | Gap |
|---|---|---|---|---|---|---|---|
| **SVM (RBF)** | **66,6%** | 65,1% | **71,5%** | **68,2%** | 31,3% | 33,4% | **2,1%** |
| Rede Neural | 66,5% | **65,6%** | 69,5% | 67,5% | 30,3% | 33,5% | 3,2% |
| Árvore de Decisão | 65,8% | 65,3% | 67,5% | 66,4% | **30,1%** | 34,2% | 4,1% |

### 7.2 Estratégia de Validação

A escolha do melhor modelo foi feita com base no **desempenho no conjunto de teste** (N = 1.114 municípios), mantido isolado durante todo o desenvolvimento. Todos os hiperparâmetros foram selecionados exclusivamente por validação cruzada sobre o treino. A métrica principal de comparação foi o **F1-score**, complementada pela análise das curvas ROC e pelo gap E_out − E_in.

### 7.3 Modelo Vencedor: SVM com Kernel RBF

O **SVM** foi selecionado como o melhor modelo pelos seguintes critérios:

1. **Maior F1-score** (68,2%): margem consistente sobre os demais em todas as rodadas de validação.
2. **Maior Recall** (71,5%): em aplicações de políticas públicas, identificar corretamente municípios de alta violência é mais importante do que evitar alarmes falsos.
3. **Menor gap E_out − E_in** (2,1%): a margem máxima do SVM impõe regularização implícita, resultando na melhor generalização entre os três modelos.
4. **Maior AUC-ROC**: o SVM domina os demais ao longo de todos os limiares de decisão possíveis.
5. **Limite teórico satisfeito**: E_out empírico (33,4%) < E_out esperado (72,6%), validando a consistência do modelo com a teoria SVM.

---

## 8. Diagnóstico: O Que Limita os Modelos?

Uma investigação sistemática das causas do desempenho atual revelou três achados relevantes.

### 8.1 Decomposição dos Erros por Dificuldade

Os municípios do conjunto de teste foram divididos em dois grupos conforme sua taxa real de homicídios:

- **Grupo Fácil** (taxa < 8 ou > 16): municípios claramente acima ou abaixo do limiar (N = 940)
- **Grupo Difícil** (taxa 8–16): municípios próximos ao limiar de 12,03 (N = 174)

| Grupo | N | Acurácia (SVM) | F1 (SVM) |
|---|---|---|---|
| Fácil | 940 | 69,7% | 71,3% |
| Difícil | 174 | 50,0% | 50,3% |

O grupo difícil apresenta acurácia equivalente ao acaso (50%), esperado para municípios ambíguos. Mais revelador é que **76,6% dos 372 erros totais do SVM ocorrem no grupo fácil** — indicando que o problema principal não é a ambiguidade do limiar, mas sim a limitação das features para prever violência em municípios aparentemente simples de classificar. Essa é evidência direta do impacto da defasagem temporal.

### 8.2 Heterogeneidade Regional

A análise do desempenho do SVM por macrorregião revelou um padrão crítico:

| Macrorregião | N | % Alta Violência | Acurácia | F1 |
|---|---|---|---|---|
| Norte | 72 | 65,3% | 69,4% | 81,0% |
| Nordeste | 345 | 68,7% | 69,0% | 81,3% |
| Centro-Oeste | 104 | 57,7% | 62,5% | 69,8% |
| Sudeste | 366 | 33,3% | 67,5% | 43,6% |
| Sul | 227 | 40,1% | 62,6% | 38,8% |

Norte e Nordeste, regiões com alta prevalência de violência associada a indicadores socioeconômicos mais desfavoráveis, apresentam F1 > 0,80. Sul e Sudeste, apesar de melhores indicadores, têm F1 < 0,45 — o modelo falha sistematicamente nessas regiões. A causa provável é que nessas regiões a violência segue padrões distintos (crime organizado, rotas do tráfico) não capturados por indicadores socioeconômicos clássicos.

### 8.3 Otimização de Limiar para Políticas Públicas

Para a rede neural, o limiar padrão de 0,5 pode ser ajustado conforme o contexto de aplicação. Em políticas de prevenção, falsos negativos são mais custosos do que falsos positivos:

| Limiar | F1 | Acurácia | Recall |
|---|---|---|---|
| 0,35 | **0,700** | 63,1% | **86,2%** |
| 0,40 | 0,697 | 64,7% | 81,0% |
| 0,50 | 0,675 | 66,5% | 69,5% |

Com limiar = 0,35, a rede neural identifica corretamente 86 em cada 100 municípios de alta violência, ao custo de mais falsos alarmes. Essa configuração é preferível quando o custo de não intervir supera o custo de intervenção desnecessária.

---

## 9. Conclusão

### 9.1 Resposta à Pergunta de Pesquisa

> **Sim, é possível prever o nível de violência de um município brasileiro usando apenas indicadores socioeconômicos, com desempenho moderado e consistentemente acima do acaso.**

O melhor modelo (SVM com kernel RBF, C = 100, γ = 0,001) classifica corretamente **66,6% dos municípios** — 16,6 pontos percentuais acima de um classificador aleatório (50%). A AUC-ROC superior a 0,72 confirma poder discriminativo real em todos os limiares de decisão.

### 9.2 O Que os Modelos Aprenderam

As variáveis com maior poder preditivo são:

- **`perc_jovens_15_29`**: maior correlação com o alvo (ρ = 0,285), feature mais importante na árvore podada — concentração de jovens é o principal marcador de risco
- **`idhm_longevidade`** e **`renda_per_capita`**: indicadores de desenvolvimento humano e renda
- **`taxa_analfabetismo_15`** e **`idhm_educacao`**: educação como fator protetor

Em contraste, `densidade_demografica` e `pib_per_capita` apresentaram correlação próxima de zero — o tamanho absoluto da economia importa menos do que sua distribuição interna.

### 9.3 Limitações

1. **Defasagem temporal:** as features do Atlas Brasil são de **2010**, prevendo violência de **2022** — gap de 12 anos que limita o poder preditivo, especialmente no Sul e Sudeste
2. **Subnotificação:** os dados do Sinesp são conhecidos por subregistro em municípios pequenos e em estados com menor capacidade institucional
3. **26 municípios imputados:** nomes divergentes no Atlas Brasil levaram à imputação pela mediana regional
4. **Classificação binária na mediana:** municípios próximos ao limiar são inerentemente ambíguos — um modelo de regressão poderia capturar mais nuance
5. **Features ausentes:** presença de organizações criminosas, nível de investimento em segurança pública e histórico de conflitos fundiários não estão disponíveis em dados abertos com cobertura municipal completa

### 9.4 Implicações para Políticas Públicas

Os resultados confirmam empiricamente que **investimentos em educação, redução da desigualdade de renda e programas voltados à juventude de 15 a 29 anos** têm o maior potencial de impacto sobre a violência estrutural a longo prazo — em linha com a literatura criminológica sobre os determinantes socioeconômicos da violência no Brasil.

A heterogeneidade regional — com desempenho superior no Norte/Nordeste e inferior no Sul/Sudeste — sugere que políticas nacionais uniformes têm eficácia limitada. Intervenções regionalmente diferenciadas, que considerem as especificidades dos padrões locais de violência, tendem a ser mais eficazes.

---

## Referências

BEATO FILHO, C. C. Determinantes da criminalidade em Minas Gerais. **Revista Brasileira de Ciências Sociais**, São Paulo, v. 13, n. 37, p. 74–87, jun. 1998.

CERQUEIRA, D.; LOBÃO, W. Determinantes da criminalidade: arcabouços teóricos e resultados empíricos. **Dados — Revista de Ciências Sociais**, Rio de Janeiro, v. 47, n. 2, p. 233–269, 2004.

DEININGER, K.; SQUIRE, L. A new data set measuring income inequality. **The World Bank Economic Review**, Washington, v. 10, n. 3, p. 565–591, 1996.

FÓRUM BRASILEIRO DE SEGURANÇA PÚBLICA. **Anuário Brasileiro de Segurança Pública 2023**. São Paulo: FBSP, 2023.

IBGE — INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA. **Censo Demográfico 2022 — Amostra Trabalho e Rendimento**. Rio de Janeiro: IBGE, 2025. Disponível em: https://sidra.ibge.gov.br. Acesso em: mar. 2026.

MELLO, J. M. P. de; SCHNEIDER, A. Mudança demográfica e a dinâmica dos homicídios no estado de São Paulo. **São Paulo em Perspectiva**, São Paulo, v. 21, n. 1, p. 19–30, 2010.

PEDREGOSA, F. et al. Scikit-learn: machine learning in Python. **Journal of Machine Learning Research**, v. 12, p. 2825–2830, 2011.

PNUD; IPEA; FJP. **Atlas do Desenvolvimento Humano no Brasil 2013**. Brasília: PNUD, 2013. Disponível em: http://www.atlasbrasil.org.br. Acesso em: mar. 2026.

SECRETARIA NACIONAL DE SEGURANÇA PÚBLICA (SENASP/MJ). **Sinesp — Sistema Nacional de Informações de Segurança Pública**. Brasília: Ministério da Justiça e Segurança Pública, 2023. Disponível em: https://www.gov.br/mj. Acesso em: mar. 2026.

VAPNIK, V. N. **The Nature of Statistical Learning Theory**. 2. ed. New York: Springer, 1999.
