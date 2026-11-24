"""Testes unitários para estatísticas analíticas e geração de gráficos."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import pandas as pd  # noqa: E402
import pytest  # noqa: E402

from src.analysis import (  # noqa: E402
    build_summary_metrics,
    continent_summary,
    detect_sharpest_drops,
    gdp_life_expectancy_correlations,
    global_weighted_life_expectancy,
    top_life_expectancy_gains,
)
from src.data_cleaning import add_derived_metrics, clean_gapminder  # noqa: E402
from src.data_loader import RAW_DATA_PATH, load_raw_gapminder  # noqa: E402
from src.visualizations import generate_all_figures  # noqa: E402


@pytest.fixture(scope="module")
def enriched_df() -> pd.DataFrame:
    raw = load_raw_gapminder(path=RAW_DATA_PATH, download_if_missing=False)
    return add_derived_metrics(clean_gapminder(raw))


def test_continent_summary_has_expected_rows(enriched_df: pd.DataFrame) -> None:
    summary = continent_summary(enriched_df, years=(1952, 2007))
    assert len(summary) == 10
    assert {"continent", "year", "lifeExp_mean", "lifeExp_std", "gdpPercap_median"} <= set(
        summary.columns
    )


def test_global_weighted_life_expectancy_increases_over_time(enriched_df: pd.DataFrame) -> None:
    weighted = global_weighted_life_expectancy(enriched_df)
    assert len(weighted) == 12
    assert weighted.iloc[-1]["lifeExp_weighted"] > weighted.iloc[0]["lifeExp_weighted"] + 15.0


def test_gdp_life_expectancy_correlations_log_stronger_than_linear(
    enriched_df: pd.DataFrame,
) -> None:
    corrs = gdp_life_expectancy_correlations(enriched_df, year=2007)
    assert 0.5 < corrs["pearson_linear"] < corrs["pearson_log10"]
    assert corrs["spearman"] > 0.8


def test_top_life_expectancy_gains_returns_sorted_top_n(enriched_df: pd.DataFrame) -> None:
    top = top_life_expectancy_gains(enriched_df, top_n=10)
    assert len(top) == 10
    assert top["lifeExp_gain"].is_monotonic_decreasing
    assert top.iloc[0]["country"] == "Oman"


def test_detect_sharpest_drops_identifies_rwanda(enriched_df: pd.DataFrame) -> None:
    drops = detect_sharpest_drops(enriched_df, top_n=5)
    assert len(drops) == 5
    assert drops.iloc[0]["country"] == "Rwanda"
    assert drops.iloc[0]["year"] == 1992
    assert drops.iloc[0]["lifeExp_diff_5y"] < -20.0


def test_build_summary_metrics_keys(enriched_df: pd.DataFrame) -> None:
    metrics = build_summary_metrics(enriched_df)
    assert metrics["top_gain_country"] == "Oman"
    assert metrics["worst_drop_country"] == "Rwanda"
    assert metrics["global_weighted_gain"] > 15.0


def test_generate_all_figures_creates_five_pngs(
    enriched_df: pd.DataFrame, tmp_path: Path
) -> None:
    paths = generate_all_figures(enriched_df, output_dir=tmp_path)
    assert len(paths) == 5
    for path in paths:
        assert path.exists()
        assert path.suffix == ".png"
        assert path.stat().st_size > 10_000
