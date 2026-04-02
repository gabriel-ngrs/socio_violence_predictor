# Dados do Projeto

Este projeto usa somente os arquivos da pasta `data/raw/` abaixo:

- `censo2022_municipios.csv`
- `atlas_brasil_municipios.xlsx`
- `ibge_municipios_ref.csv`
- `pib_municipios_sidra_2021.csv`
- `areas_municipios_2024.xls`
- `sinesp_municipios.xlsx`

## Regras da branch de apresentacao

- Nao ha scripts `.py` de download em `data/`.
- O pipeline de tratamento e cruzamento acontece no notebook
  `notebooks/01_dados_eda_preprocessamento.ipynb`.
- A chave de integracao entre fontes e `cod_ibge` (7 digitos).

## Saidas geradas em execucao

Ao executar o notebook 01, sao criados em `data/processed/`:

- `dataset_municipios.csv`
- `X_train.npy`
- `X_test.npy`
- `y_train.npy`
- `y_test.npy`
- `feature_names.txt`

Esses artefatos sao temporarios de execucao e nao sao versionados no Git (apenas `.gitkeep` fica no repositório).
