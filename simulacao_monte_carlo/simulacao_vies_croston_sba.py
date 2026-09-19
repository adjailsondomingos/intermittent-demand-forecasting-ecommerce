"""Simulacao de Monte Carlo do vies do metodo de Croston e da correcao do SBA.

Reproduz o Apendice C do trabalho. Gera uma serie de demanda intermitente com
parametros conhecidos -- e, portanto, com demanda media teorica conhecida de
antemao --, aplica o metodo de Croston (Equacoes 2.9-2.11) e a correcao de
Syntetos-Boylan (fator 1 - alpha/2, Equacao 2.12) e compara a previsao media
com a demanda media teorica.

Processo gerador:
  - venda ocorre com probabilidade p = 0,25 em cada periodo;
  - quando ocorre, o tamanho segue distribuicao uniforme discreta em
    {1, ..., 7} (media mu = 4), de modo que a demanda media teorica e
    p x mu = 1,00 unidade por periodo;
  - 2.000.000 de periodos, descartando os 1.000 primeiros como aquecimento;
  - alpha = 0,2 para o Croston e para o SBA.

Sementes fixas: a principal (20260829) e cinco sementes do teste de
robustez (1, 7, 42, 12345 e 99). Os resultados sao deterministicos.

Saidas (gravadas na mesma pasta deste script):
  - resultados_simulacao_vies_sba.csv   resultados de todas as sementes
  - resultados_simulacao_vies_sba.json  os mesmos resultados, com a trajetoria
                                        de convergencia da semente principal
  - grafico_convergencia_vies_sba.png   convergencia da previsao media

Uso:
    python3 simulacao_vies_croston_sba.py

Requer apenas a biblioteca padrao do Python e o matplotlib (usado so no
grafico).
"""
import csv
import json
import random
from pathlib import Path

P_VENDA = 0.25
TAMANHO_MIN, TAMANHO_MAX = 1, 7
ALPHA = 0.2
N_PERIODOS = 2_000_000
AQUECIMENTO = 1_000
SEMENTE_PRINCIPAL = 20260829
SEMENTES_ROBUSTEZ = (1, 7, 42, 12345, 99)
PONTOS_CONVERGENCIA = (2_000, 5_000, 10_000, 20_000, 50_000, 100_000,
                       200_000, 500_000, 1_000_000, 2_000_000)

MU = (TAMANHO_MIN + TAMANHO_MAX) / 2
DEMANDA_MEDIA_TEORICA = P_VENDA * MU
FATOR_SBA = 1 - ALPHA / 2

PASTA_SAIDA = Path(__file__).resolve().parent


def gerar_demanda(semente: int) -> list[int]:
    """Serie de demanda intermitente: Bernoulli(p) x Uniforme discreta{1..7}."""
    rng = random.Random(semente)
    return [rng.randint(TAMANHO_MIN, TAMANHO_MAX) if rng.random() < P_VENDA else 0
            for _ in range(N_PERIODOS)]


def previsao_media_croston(demanda: list[int]) -> tuple[float, dict[int, float]]:
    """Media da previsao de Croston (z_hat / x_hat) apos o aquecimento.

    z_hat (tamanho da demanda) e x_hat (intervalo entre demandas) sao
    atualizados apenas nos periodos com demanda. Devolve a media final e a
    media acumulada em cada ponto de PONTOS_CONVERGENCIA."""
    z_hat = x_hat = None
    q = 0
    soma, n = 0.0, 0
    trajetoria = {}
    for t, d in enumerate(demanda):
        q += 1
        if d > 0:
            if z_hat is None:
                z_hat, x_hat = float(d), float(q)
            else:
                z_hat = ALPHA * d + (1 - ALPHA) * z_hat
                x_hat = ALPHA * q + (1 - ALPHA) * x_hat
            q = 0
        if z_hat is not None and t >= AQUECIMENTO:
            soma += z_hat / x_hat
            n += 1
        if t + 1 in PONTOS_CONVERGENCIA:
            trajetoria[t + 1] = soma / n
    return soma / n, trajetoria


def resultado_semente(semente: int) -> tuple[dict, dict[int, float]]:
    croston, trajetoria = previsao_media_croston(gerar_demanda(semente))
    sba = croston * FATOR_SBA
    linha = {
        "semente": semente,
        "previsao_media_croston": round(croston, 6),
        "vies_relativo_croston_pct": round(100 * (croston / DEMANDA_MEDIA_TEORICA - 1), 4),
        "previsao_media_sba": round(sba, 6),
        "vies_relativo_sba_pct": round(100 * (sba / DEMANDA_MEDIA_TEORICA - 1), 4),
    }
    return linha, trajetoria


def gerar_grafico(trajetoria: dict[int, float], caminho: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    x = list(trajetoria)
    croston = list(trajetoria.values())
    sba = [v * FATOR_SBA for v in croston]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.axhline(DEMANDA_MEDIA_TEORICA, color="0.25", linestyle="--",
               label="Demanda média teórica (p × μ = 1,00)")
    ax.plot(x, croston, marker="o", color="#c0392b", label="Previsão média — Croston")
    ax.plot(x, sba, marker="s", color="#2471a3", label="Previsão média — SBA")
    ax.set_xscale("log")
    ax.set_xlabel("Períodos simulados (escala log)")
    ax.set_ylabel("Previsão média (unidades/período)")
    ax.set_title("Convergência da previsão média: Croston vs. SBA\n"
                 f"(simulação de Monte Carlo, p = 0,25, α = 0,2, semente = {SEMENTE_PRINCIPAL})")
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(
        lambda v, _: f"{v:.2f}".replace(".", ",")))
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=1, frameon=False)
    fig.tight_layout()
    fig.savefig(caminho, dpi=150)
    plt.close(fig)


def main() -> None:
    principal, trajetoria = resultado_semente(SEMENTE_PRINCIPAL)
    robustez = [resultado_semente(s)[0] for s in SEMENTES_ROBUSTEZ]
    linhas = [dict(principal, tipo="principal")] + [dict(r, tipo="robustez") for r in robustez]

    colunas = ["tipo", "semente", "previsao_media_croston", "vies_relativo_croston_pct",
               "previsao_media_sba", "vies_relativo_sba_pct"]
    with open(PASTA_SAIDA / "resultados_simulacao_vies_sba.csv", "w",
              newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=colunas)
        escritor.writeheader()
        escritor.writerows(linhas)

    reducao = 1 - abs(principal["vies_relativo_sba_pct"]) / abs(principal["vies_relativo_croston_pct"])
    saida = {
        "parametros": {
            "p_venda": P_VENDA,
            "tamanho_venda": f"uniforme discreta {{{TAMANHO_MIN}, ..., {TAMANHO_MAX}}}",
            "demanda_media_teorica": DEMANDA_MEDIA_TEORICA,
            "alpha": ALPHA,
            "fator_correcao_sba": FATOR_SBA,
            "n_periodos": N_PERIODOS,
            "periodos_aquecimento": AQUECIMENTO,
            "semente_principal": SEMENTE_PRINCIPAL,
            "sementes_robustez": list(SEMENTES_ROBUSTEZ),
        },
        "principal": principal,
        "reducao_magnitude_vies_pct": round(100 * reducao, 2),
        "robustez": robustez,
        "convergencia_semente_principal": [
            {"periodos": k, "previsao_media_croston": round(v, 6),
             "previsao_media_sba": round(v * FATOR_SBA, 6)}
            for k, v in trajetoria.items()
        ],
    }
    with open(PASTA_SAIDA / "resultados_simulacao_vies_sba.json", "w", encoding="utf-8") as f:
        json.dump(saida, f, ensure_ascii=False, indent=2)

    gerar_grafico(trajetoria, PASTA_SAIDA / "grafico_convergencia_vies_sba.png")

    print(f"Semente principal ({SEMENTE_PRINCIPAL}): "
          f"Croston {principal['previsao_media_croston']:.6f} "
          f"({principal['vies_relativo_croston_pct']:+.2f}%) | "
          f"SBA {principal['previsao_media_sba']:.6f} "
          f"({principal['vies_relativo_sba_pct']:+.2f}%) | "
          f"reducao do vies: {100 * reducao:.1f}%")
    vc = [r["vies_relativo_croston_pct"] for r in robustez]
    vs = [r["vies_relativo_sba_pct"] for r in robustez]
    print(f"Robustez {SEMENTES_ROBUSTEZ}: Croston {min(vc):+.2f}% a {max(vc):+.2f}% | "
          f"SBA {min(vs):+.2f}% a {max(vs):+.2f}%")


if __name__ == "__main__":
    main()
