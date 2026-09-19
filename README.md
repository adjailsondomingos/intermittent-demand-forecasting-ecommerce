# Previsão de Demanda Intermitente de Produtos de Cauda Longa no Comércio Eletrônico Brasileiro

[![DOI](https://zenodo.org/badge/1336365989.svg)](https://doi.org/10.5281/zenodo.22847653)

*(English version: [README.en.md](README.en.md))*

Código-fonte e dados de apoio do trabalho de conclusão de curso "Previsão de demanda intermitente de produtos de cauda longa no comércio eletrônico brasileiro: uma comparação entre modelos de aprendizado de máquina e métodos estatísticos especializados" (MBA em Inteligência Artificial e Big Data, ICMC-USP, 2026).

## Estrutura do repositório

- `TCC_Pipeline_Colab.ipynb` — pipeline completo dos experimentos. Ao ser executado, gera o pacote `src/` (extração, pré-processamento, construção de variáveis, treinamento dos modelos, cálculo de métricas e testes estatísticos) e produz os resultados reportados no trabalho. Cada execução grava um `METADATA.md` próprio, com os parâmetros efetivos, as janelas de treino/teste e as versões das bibliotecas carregadas. As sementes aleatórias estão fixadas em `src/config.py` (`RANDOM_STATE = 42`).
- `TCC_Pipeline_Anonimizacao_Colab-v1.ipynb` — gera a versão anonimizada da base de vendas a partir da extração original.
- `data/base_venda.csv` — base de vendas anonimizada, com a mesma estrutura, tipos e quantidade de linhas da base original. Os identificadores de produto (`Prod_SKU`, `Prod_Id`), de parceiro comercial (`Ped_Campanha`) e de categoria (`Cat_CategoriaNome`, `Cat_CategoriaId`) foram substituídos por códigos sintéticos.
- `data/calendario_diario_wide.csv` — calendário diário de feriados nacionais e datas comemorativas brasileiras. O Cenário 2 (calendário rico) utiliza um subconjunto de 14 colunas deste arquivo, definido em `src/config.py` (`COLUNAS_CALENDARIO_RICO`), das quais 7 são mantidas após a seleção descrita no trabalho (`EXOGENAS_EXCLUIDAS`).
- `simulacao_monte_carlo/` — simulação de Monte Carlo do viés do método de Croston e da correção do SBA (Apêndice C do trabalho), com código, resultados e gráfico de convergência; ver o `README.md` da pasta.

## Confidencialidade dos dados

A base de vendas original é coberta por acordo de confidencialidade com a empresa parceira e não é distribuída. O arquivo `data/base_venda.csv` traz uma versão anonimizada, com estrutura idêntica à original e identificadores trocados por código sintético, suficiente para reproduzir o fluxo metodológico de ponta a ponta.

## Ambiente e reprodução

Pipeline executado em Python 3.12.13, sistema operacional Ubuntu 22.04.5 LTS (Google Colab). As versões das bibliotecas de referência estão em `requirements.txt`; cada execução registra as versões efetivamente carregadas no `METADATA.md` gerado localmente (não versionado neste repositório).

Para reproduzir os experimentos no Google Colab:

1. Clonar este repositório no ambiente de execução (`/content`), de modo que os caminhos padrão da célula de parâmetros (`REPO`, `DADOS` e `CALENDARIO_EXOGENAS`) apontem para `data/`. Ajustar `DRIVE_OUT` para a pasta de saída desejada.
2. Instalar as dependências listadas em `requirements.txt`.
3. Executar `TCC_Pipeline_Colab.ipynb` de ponta a ponta. A configuração padrão reproduz a execução dos resultados principais (Experimentos 1 e 2, SBA com parâmetro de suavização fixo). A execução completa, com 3.684 SKUs, levou cerca de 22 horas no ambiente descrito.
4. Para a análise de sensibilidade do SBA (Seção 5.6), definir `SBA_MODO = "otimizado"`; com `RODAR_MODELOS_ML = False` e `EXPERIMENTOS = ("1",)`, apenas SBA, TSB e o controle de previsão nula são reexecutados.

A simulação do Apêndice C é independente do pipeline: `python3 simulacao_monte_carlo/simulacao_vies_croston_sba.py` (requer apenas a biblioteca padrão do Python e o `matplotlib`).

## Licença

Distribuído sob licença MIT (ver `LICENSE`).
