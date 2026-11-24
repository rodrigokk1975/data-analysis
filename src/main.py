"""Ponto de entrada CLI para executar o pipeline completo de análise Gapminder."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

from src.analysis import (  # noqa: E402
    build_summary_metrics,
    continent_summary,
    detect_sharpest_drops,
    top_life_expectancy_gains,
)
from src.data_cleaning import (  # noqa: E402
    generate_quality_report,
    run_cleaning_pipeline,
)
from src.data_loader import download_gapminder  # noqa: E402
from src.visualizations import generate_all_figures  # noqa: E402


def main() -> None:
    """Executa ingestão, limpeza, estatísticas e geração de gráficos."""
    raw_path = download_gapminder()
    df = run_cleaning_pipeline(raw_path=raw_path)
    quality = generate_quality_report(df)
    summary = build_summary_metrics(df)
    figures = generate_all_figures(df)

    print("=== Pipeline Gapminder Concluído ===")
    print(f"Registros processados: {quality['rows']} ({quality['countries']} países)")
    print(
        "Expectativa de vida global ponderada: "
        f"{summary['global_weighted_lifeExp_1952']} (1952) -> "
        f"{summary['global_weighted_lifeExp_2007']} (2007) "
        f"[+{summary['global_weighted_gain']} anos]"
    )
    print(f"Correlações PIB vs. lifeExp (2007): {summary['correlations_2007']}")
    print(
        f"Maior ganho (1952-2007): {summary['top_gain_country']} "
        f"(+{summary['top_gain_years']} anos)"
    )
    print(
        f"Maior queda quinquenal: {summary['worst_drop_country']} "
        f"em {summary['worst_drop_year']} ({summary['worst_drop_years']} anos)"
    )
    print(f"Gráficos gerados ({len(figures)}): {[p.name for p in figures]}")
    print("\n--- Resumo por Continente (1952 vs. 2007) ---")
    print(continent_summary(df).round(2).to_string(index=False))
    print("\n--- Top 5 Ganhos de Expectativa de Vida (1952-2007) ---")
    print(
        top_life_expectancy_gains(df, top_n=5)[
            ["country", "continent", "lifeExp_1952", "lifeExp_2007", "lifeExp_gain"]
        ]
        .round(2)
        .to_string(index=False)
    )
    print("\n--- Top 5 Quedas Quinquenais ---")
    print(detect_sharpest_drops(df, top_n=5).round(2).to_string(index=False))


if __name__ == "__main__":
    main()
