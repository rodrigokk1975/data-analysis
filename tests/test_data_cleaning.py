"""Testes unitários para limpeza, métricas derivadas e relatório de qualidade."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from src.data_cleaning import (
    add_derived_metrics,
    clean_gapminder,
    generate_quality_report,
    run_cleaning_pipeline,
)


def _sample_dirty_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "country": [" Brazil ", "Brazil", "Brazil"],
            "continent": [" Americas ", "Americas", "Americas"],
            "year": [1957, 1952, 1952],
            "lifeExp": [53.285, 50.917, 50.917],
            "pop": [65551171, 56602560, 56602560],
            "gdpPercap": [2487.366, 2108.944, 2108.944],
        }
    )


def test_clean_gapminder_strips_deduplicates_and_sorts() -> None:
    cleaned = clean_gapminder(_sample_dirty_df())
    assert len(cleaned) == 2
    assert list(cleaned["year"]) == [1952, 1957]
    assert list(cleaned["country"].unique()) == ["Brazil"]
    assert list(cleaned["continent"].unique()) == ["Americas"]


def test_add_derived_metrics_computes_expected_columns_without_mutating() -> None:
    base = clean_gapminder(_sample_dirty_df())
    original_cols = list(base.columns)

    enriched = add_derived_metrics(base)

    assert list(base.columns) == original_cols
    assert {"gdp_total", "decade", "lifeExp_diff_5y", "gdpPercap_pct_change_5y"} <= set(
        enriched.columns
    )
    assert enriched.loc[0, "decade"] == 1950
    assert pd.isna(enriched.loc[0, "lifeExp_diff_5y"])
    assert enriched.loc[1, "lifeExp_diff_5y"] == pytest.approx(53.285 - 50.917)
    assert enriched.loc[0, "gdp_total"] == pytest.approx(2108.944 * 56602560)


def test_generate_quality_report_detects_clean_dataset() -> None:
    enriched = add_derived_metrics(clean_gapminder(_sample_dirty_df()))
    report = generate_quality_report(enriched)
    assert report["rows"] == 2
    assert report["duplicate_country_year"] == 0
    assert all(v == 0 for v in report["nulls_core_columns"].values())


def test_run_cleaning_pipeline_writes_processed_csv(tmp_path: Path) -> None:
    output_file = tmp_path / "gapminder_clean.csv"
    df = run_cleaning_pipeline(output_path=output_file)
    assert output_file.exists()
    assert len(df) == 1704
    reloaded = pd.read_csv(output_file)
    assert len(reloaded) == 1704
    assert "gdp_total" in reloaded.columns
