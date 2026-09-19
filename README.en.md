# Intermittent Demand Forecasting for Long-Tail Products in Brazilian E-Commerce

[![DOI](https://zenodo.org/badge/1336365989.svg)](https://doi.org/10.5281/zenodo.22847653)

*(Versão em português: [README.md](README.md))*

Source code and supporting data for the capstone thesis "Previsão de demanda intermitente de produtos de cauda longa no comércio eletrônico brasileiro: uma comparação entre modelos de aprendizado de máquina e métodos estatísticos especializados" ("Intermittent demand forecasting for long-tail products in Brazilian e-commerce: a comparison between machine learning models and specialized statistical methods") (MBA in Artificial Intelligence and Big Data, ICMC-USP, 2026).

## Repository structure

- `TCC_Pipeline_Colab.ipynb` — the full experiment pipeline. Running it generates the `src/` package (extraction, preprocessing, feature engineering, model training, metric computation and statistical tests) and produces the results reported in the thesis. Each run writes its own `METADATA.md`, with the effective parameters, train/test windows and the library versions loaded. Random seeds are fixed in `src/config.py` (`RANDOM_STATE = 42`).
- `TCC_Pipeline_Anonimizacao_Colab-v1.ipynb` — generates the anonymized sales dataset from the original extraction.
- `data/base_venda.csv` — anonymized sales dataset, with the same structure, types and row count as the original. Product identifiers (`Prod_SKU`, `Prod_Id`), business-partner identifiers (`Ped_Campanha`) and category identifiers (`Cat_CategoriaNome`, `Cat_CategoriaId`) were replaced with synthetic codes.
- `data/calendario_diario_wide.csv` — daily calendar of Brazilian national holidays and commemorative dates. Scenario 2 (rich calendar) uses a 14-column subset of this file, defined in `src/config.py` (`COLUNAS_CALENDARIO_RICO`), of which 7 are kept after the feature-selection step described in the thesis (`EXOGENAS_EXCLUIDAS`).
- `simulacao_monte_carlo/` — Monte Carlo simulation of Croston's bias and the SBA correction (thesis Appendix C), with code, results and a convergence plot; see that folder's own `README.md`.

## Data confidentiality

The original sales dataset is covered by a confidentiality agreement with the partner company and is not distributed. `data/base_venda.csv` provides an anonymized version, with the same structure as the original and identifiers replaced by synthetic codes — sufficient to reproduce the full methodological pipeline end to end.

## Environment and reproduction

Pipeline run on Python 3.12.13, Ubuntu 22.04.5 LTS (Google Colab). Reference library versions are in `requirements.txt`; each run records the versions actually loaded in its own locally generated `METADATA.md` (not tracked in this repository).

To reproduce the experiments in Google Colab:

1. Clone this repository into the runtime environment (`/content`), so that the default paths in the parameters cell (`REPO`, `DADOS` and `CALENDARIO_EXOGENAS`) point to `data/`. Set `DRIVE_OUT` to the desired output folder.
2. Install the dependencies listed in `requirements.txt`.
3. Run `TCC_Pipeline_Colab.ipynb` end to end. The default configuration reproduces the main results (Experiments 1 and 2, SBA with a fixed smoothing parameter). The full run, covering 3,684 SKUs, took about 22 hours in the environment described above.
4. For the SBA sensitivity analysis (thesis Section 5.6), set `SBA_MODO = "otimizado"`; with `RODAR_MODELOS_ML = False` and `EXPERIMENTOS = ("1",)`, only SBA, TSB and the naive/zero-forecast control are re-run.

The Appendix C simulation is independent of the pipeline: `python3 simulacao_monte_carlo/simulacao_vies_croston_sba.py` (requires only the Python standard library and `matplotlib`).

## License

Distributed under the MIT license (see `LICENSE`).
