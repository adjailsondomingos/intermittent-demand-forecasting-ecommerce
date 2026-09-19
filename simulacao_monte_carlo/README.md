# Simulação de Monte Carlo — viés do método de Croston e correção do SBA

Código e resultados do **Apêndice C** do trabalho. A simulação gera uma série de demanda intermitente com parâmetros conhecidos — e, portanto, com demanda média teórica conhecida de antemão — e mede o quanto a previsão do método de Croston se afasta desse valor e o quanto a correção do SBA (Syntetos; Boylan, 2001, 2005) o aproxima.

## Como reproduzir

```bash
python3 simulacao_vies_croston_sba.py
```

Requer apenas a biblioteca padrão do Python e o `matplotlib` (usado só no gráfico). As sementes aleatórias estão fixadas no código, de modo que os resultados são determinísticos. A execução leva poucos segundos e regrava os três arquivos de saída desta pasta.

## Parâmetros do processo gerador

| Parâmetro | Valor | Significado |
|---|---|---|
| p | 0,25 | probabilidade de venda em cada período (ADI teórico = 1/p = 4) |
| tamanho da venda | uniforme discreta {1, …, 7} | média μ = 4 unidades quando há venda |
| demanda média teórica | p × μ = 1,00 unidade/período | valor de referência |
| α | 0,2 | parâmetro de suavização do Croston e do SBA |
| períodos simulados | 2.000.000 | após descarte de 1.000 períodos de aquecimento |

## Resultados

Semente principal (20260829):

| Método | Previsão média | Viés sobre o valor teórico |
|---|---|---|
| Croston | 1,082317 | +8,23% |
| SBA | 0,974085 | −2,59% |

Robustez com cinco sementes independentes (1, 7, 42, 12345, 99): viés do Croston entre +8,09% e +8,45%; viés do SBA entre −2,71% e −2,39%.

## Arquivos

- `simulacao_vies_croston_sba.py` — código-fonte comentado.
- `resultados_simulacao_vies_sba.csv` — resultados de todas as sementes.
- `resultados_simulacao_vies_sba.json` — os mesmos resultados, com a trajetória de convergência usada no gráfico.
- `grafico_convergencia_vies_sba.png` — convergência da previsão média do Croston e do SBA em função do número de períodos simulados.
