# Relatório — Predição de Violência Municipal com Indicadores Socioeconômicos

**Disciplina:** Aprendizagem de Máquina — UFPB, 2025.1
**Professores:** Bruno Jefferson de Sousa Pessoa e Gilberto Farias de Sousa Filho
**Autores:** *(adicionar nomes)*
**Data:** *(adicionar data)*

---

## 1. Introdução

### 1.1 Contexto e Motivação

*(Descrever o problema: violência urbana no Brasil, relevância para políticas públicas, a pergunta central do projeto.)*

### 1.2 Pergunta de Pesquisa

"É possível prever o nível de violência de um município brasileiro usando apenas indicadores socioeconômicos?"

### 1.3 Abordagem

*(Descrever a abordagem de classificação binária, o uso de indicadores socioeconômicos como features e dados de crime apenas como variável alvo.)*

---

## 2. Dataset

### 2.1 Fontes de Dados

*(Listar todas as fontes utilizadas: Sinesp/MJ, Atlas Brasil, IBGE, SIDRA.)*

### 2.2 Variável Alvo

*(Descrever como a variável alvo foi construída: homicídios dolosos per capita, threshold pela mediana.)*

### 2.3 Features Selecionadas

*(Listar todas as features com justificativa para cada escolha.)*

### 2.4 Processo de Cruzamento

*(Descrever o cruzamento dos datasets pelo código IBGE, tratamento de inconsistências.)*

### 2.5 Estatísticas Descritivas

*(Tabela com estatísticas descritivas de cada feature: média, desvio padrão, min, max.)*

| Feature | N | Média | Desvio Padrão | Mín | Máx |
|---------|---|-------|---------------|-----|-----|
| *(preencher)* | | | | | |

---

## 3. Tratamento de Dados

### 3.1 Construção da Matriz X e Vetor y

- Número de amostras (N): *(preencher)*
- Número de parâmetros (p): *(preencher)*

### 3.2 Separação Treino/Teste

*(Justificar a proporção escolhida. Descrever o stratified split.)*

- Tamanho do treino: *(preencher)*
- Tamanho do teste: *(preencher)*
- Proporção: *(preencher)*

### 3.3 Normalização/Padronização

*(Descrever o método escolhido e justificar. Explicar por que o scaler é ajustado apenas no treino.)*

### 3.4 Tratamento de Valores Ausentes

*(Descrever a estratégia adotada e justificar.)*

---

## 4. Rede Neural

### 4.1 Dimensão VC e Regra de Ouro

*(Calcular a dimensão VC da arquitetura escolhida. Verificar se N ≥ 10·d_VC.)*

- Arquitetura: *(ex: [13, 8, 4, 1])*
- d_VC calculada: *(preencher)*
- N/d_VC = *(preencher)* → *(satisfaz/não satisfaz)*

### 4.2 Arquitetura da Rede

*(Descrever e justificar: número de camadas, neurônios por camada, funções de ativação. Mencionar o Teorema da Aproximação Universal.)*

### 4.3 Parâmetros de Treinamento

*(Justificar batch size, número de épocas, learning rate, otimizador.)*

### 4.4 Análise de Overfitting

- E_in = *(preencher)*
- E_out = *(preencher)*
- Ocorreu overfitting? *(sim/não)*
- A partir de que época? *(preencher)*

*(Inserir gráfico de E_in e E_out por época.)*

![Curva de Overfitting — Rede Neural](../reports/figures/nn_overfitting.png)

### 4.5 Métricas de Qualidade

| Métrica | Valor |
|---------|-------|
| Acurácia | *(preencher)* |
| Precisão | *(preencher)* |
| Recall | *(preencher)* |
| F1-Score | *(preencher)* |

---

## 5. Árvore de Decisão

### 5.1 Árvore Sem Poda

*(Descrever a árvore inicial. Inserir imagem da árvore.)*

![Árvore de Decisão — Sem Poda](../reports/figures/tree_unpruned.png)

- E_in = *(preencher)*
- E_out = *(preencher)*
- Overfitting? *(analisar)*

### 5.2 Regularização via Minimal Cost-Complexity

*(Descrever o processo de pruning. Explicar a relação Pureza(T) + α·#folhas(T). Descrever o cross validation utilizado.)*

- Número de folds: *(preencher)*
- Alpha ótimo: *(preencher)*

### 5.3 Melhor Árvore

*(Inserir imagem da árvore podada.)*

![Árvore de Decisão — Podada](../reports/figures/tree_pruned.png)

### 5.4 Métricas de Qualidade

| Métrica | Valor |
|---------|-------|
| Acurácia | *(preencher)* |
| Precisão | *(preencher)* |
| Recall | *(preencher)* |
| F1-Score | *(preencher)* |

---

## 6. SVM

### 6.1 Configuração do GridSearchCV

*(Descrever os ranges de C e gamma testados. Descrever o cross validation.)*

- Número de folds: *(preencher)*
- Valores de C testados: *(preencher)*
- Valores de gamma testados: *(preencher)*

### 6.2 Melhor Modelo

- C ótimo: *(preencher)*
- Gamma ótimo: *(preencher)*
- Kernel: *(preencher)*

### 6.3 Análise de Overfitting

- E_in = *(preencher)*
- E_out = *(preencher)*
- Número de vetores de suporte: *(preencher)*
- E_out esperado (SV/N): *(preencher)*
- Overfitting? *(analisar)*

### 6.4 Métricas de Qualidade

| Métrica | Valor |
|---------|-------|
| Acurácia | *(preencher)* |
| Precisão | *(preencher)* |
| Recall | *(preencher)* |
| F1-Score | *(preencher)* |

---

## 7. Escolha do Melhor Modelo

### 7.1 Comparação dos Modelos

| Métrica | Rede Neural | Árvore de Decisão | SVM |
|---------|-------------|-------------------|-----|
| Acurácia | *(preencher)* | *(preencher)* | *(preencher)* |
| Precisão | *(preencher)* | *(preencher)* | *(preencher)* |
| Recall | *(preencher)* | *(preencher)* | *(preencher)* |
| F1-Score | *(preencher)* | *(preencher)* | *(preencher)* |
| E_in | *(preencher)* | *(preencher)* | *(preencher)* |
| E_out | *(preencher)* | *(preencher)* | *(preencher)* |

### 7.2 Estratégia de Validação

*(Descrever a estratégia utilizada para escolher o melhor modelo no conjunto de teste.)*

### 7.3 Modelo Escolhido

*(Justificar a escolha do melhor modelo.)*

---

## 8. Conclusão

*(Responder à pergunta central. Discutir implicações para políticas públicas. Limitações do estudo.)*

---

## Referências

*(Listar referências bibliográficas utilizadas.)*
