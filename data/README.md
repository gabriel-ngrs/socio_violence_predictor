# Dados — Instruções de Download

Todos os dados brutos devem ser colocados em `data/raw/`. Esta pasta está no `.gitignore`.

## Variável Alvo — Homicídios Dolosos

| Arquivo esperado | `indicadoressegurancapublicamunic.xlsx` |
|------------------|----------------------------------------|
| **Fonte** | Sinesp / Ministério da Justiça |
| **Download** | [dados.mj.gov.br](http://dados.mj.gov.br/dataset/210b9ae2-21fc-4986-89c6-2006eb4db247/resource/03af7ce2-174e-4ebd-b085-384503cfb40f/download/indicadoressegurancapublicamunic.xlsx) |
| **Uso** | Total de homicídios dolosos por município → dividir pela população → ×100.000 → mediana como threshold → binário (0/1) |

> **IMPORTANTE:** Estes dados servem APENAS para construir y. Nunca usar como features em X.

---

## Features — Indicadores Socioeconômicos

### 1. Atlas Brasil (PNUD/IPEA/FJP)

Várias features vêm do Atlas Brasil. Baixe tudo de uma vez.

| Arquivo esperado | `atlas_brasil_municipios.csv` (ou similar) |
|------------------|-------------------------------------------|
| **Fonte** | Atlas do Desenvolvimento Humano no Brasil |
| **Download** | [atlasbrasil.org.br](http://www.atlasbrasil.org.br/) → Consulta → Municípios → selecionar indicadores → Exportar CSV |
| **Indicadores necessários** | |
| - IDHM | Índice de Desenvolvimento Humano Municipal (geral) |
| - IDHM_E | IDHM Educação |
| - IDHM_L | IDHM Longevidade |
| - IDHM_R | IDHM Renda |
| - GINI | Índice de Gini |
| - T_ANALF15M | Taxa de analfabetismo 15+ anos |
| - RDPC | Renda per capita |
| - PMPOB | Proporção de pobres |
| - T_DES18M | Taxa de desemprego 18+ anos |
| - T_AGUA | % com água encanada (ou indicador de saneamento) |

**Como baixar:**
1. Acesse [atlasbrasil.org.br](http://www.atlasbrasil.org.br/)
2. Vá em "Consulta"
3. Selecione "Municípios" como unidade territorial
4. Nas categorias, selecione os indicadores listados acima (Renda, Educação, Trabalho, Habitação)
5. Exporte como CSV
6. Salve em `data/raw/atlas_brasil_municipios.csv`

### 2. PIB per capita Municipal

| Arquivo esperado | `pib_municipios.csv` |
|------------------|---------------------|
| **Fonte** | IBGE — Produto Interno Bruto dos Municípios |
| **Download (opção 1)** | SIDRA — [Tabela 5938](https://sidra.ibge.gov.br/tabela/5938) |
| **Download (opção 2)** | [basedosdados.org](https://basedosdados.org/) — buscar "PIB municípios" |
| **Download (opção 3)** | FTP IBGE: `ftp://ftp.ibge.gov.br/Pib_Municipios/` |
| **Coluna necessária** | PIB per capita (R$) por município |

### 3. Taxa de Urbanização

| Arquivo esperado | `urbanizacao_municipios.csv` |
|------------------|------------------------------|
| **Fonte** | IBGE — Censo Demográfico 2022 |
| **Download** | SIDRA ou FTP: `ftp://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/` |
| **Cálculo** | População urbana / população total × 100 |

### 4. Densidade Demográfica

| Arquivo esperado | `area_municipios.csv` |
|------------------|-----------------------|
| **Fonte** | IBGE — Áreas Territoriais |
| **Download** | [ibge.gov.br](https://www.ibge.gov.br/geociencias/organizacao-do-territorio/estrutura-territorial/15761-areas-dos-municipios.html) |
| **Cálculo** | População total / área territorial (km²) |

### 5. População por Faixa Etária (% jovens 15-29)

| Arquivo esperado | `populacao_faixa_etaria.csv` |
|------------------|------------------------------|
| **Fonte** | IBGE — Censo 2022, população por faixa etária |
| **Download** | SIDRA — população por grupo de idade e município |
| **Cálculo** | Somar pop. 15-19 + 20-24 + 25-29 / pop. total × 100 |

### 6. População Total

| Arquivo esperado | `populacao_total.csv` |
|------------------|-----------------------|
| **Fonte** | IBGE — Censo 2022 |
| **Download** | SIDRA — [Tabela 9514](https://sidra.ibge.gov.br/tabela/9514) |

---

## Chave de Cruzamento

Todas as fontes utilizam o **código IBGE do município (7 dígitos)** como identificador.
Na hora de cruzar os dados, garantir que o código está no mesmo formato em todas as tabelas (inteiro de 7 dígitos, sem zeros à esquerda faltando).

## Nomeação dos Arquivos

Após download, renomear os arquivos conforme a coluna "Arquivo esperado" de cada tabela acima e salvar em `data/raw/`.

## Dataset Final

Após o cruzamento (feito no notebook `01_coleta_e_limpeza.ipynb`), o dataset unificado será salvo em `data/processed/dataset_municipios.csv` com:

- ~5.570 linhas (municípios)
- ~13 colunas de features socioeconômicas
- 1 coluna de variável alvo (alta_violencia: 0 ou 1)
- 1 coluna de código IBGE (para referência)
