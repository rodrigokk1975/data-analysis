"""Testes unitários para ingestão e validação de schema do dataset Gapminder."""

from __future__ import annotations

import pandas as pd
import pytest

from src.data_loader import (
    EXPECTED_COLUMNS,
    RAW_DATA_PATH,
    load_raw_gapminder,
    validate_schema,
)


def _sample_valid_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "country": ["Brazil", "Japan"],
            "continent": ["Americas", "Asia"],
            "year": [1952, 2007],
            "lifeExp": [50.917, 82.603],
            "pop": [56602560, 127467972],
            "gdpPercap": [2108.944, 31656.068],
        }
    )


def test_load_raw_gapminder_real_dataset() -> None:
    df = load_raw_gapminder(path=RAW_DATA_PATH, download_if_missing=False)
    assert list(df.columns) == list(EXPECTED_COLUMNS)
    assert len(df) == 1704
    assert df["country"].nunique() == 142
    assert df["continent"].nunique() == 5
    assert df["year"].nunique() == 12


def test_validate_schema_accepts_valid_dataframe() -> None:
    df = _sample_valid_df()
    validated = validate_schema(df)
    assert len(validated) == 2


def test_validate_schema_raises_on_missing_column() -> None:
    df = _sample_valid_df().drop(columns=["gdpPercap"])
    with pytest.raises(ValueError, match="Colunas obrigatórias ausentes"):
        validate_schema(df)


def test_validate_schema_raises_on_null_values() -> None:
    df = _sample_valid_df()
    df.loc[0, "lifeExp"] = None
    with pytest.raises(ValueError, match="Valores nulos encontrados"):
        validate_schema(df)


def test_validate_schema_raises_on_invalid_continent() -> None:
    df = _sample_valid_df()
    df.loc[0, "continent"] = "Antarctica"
    with pytest.raises(ValueError, match="Continentes inválidos"):
        validate_schema(df)


@pytest.mark.parametrize(
    ("column", "bad_value", "pattern"),
    [
        ("lifeExp", 0.0, "lifeExp"),
        ("lifeExp", 120.0, "lifeExp"),
        ("pop", -10, "pop"),
        ("gdpPercap", 0.0, "gdpPercap"),
        ("year", 1953, "Anos fora do recorte"),
    ],
)
def test_validate_schema_raises_on_domain_violations(
    column: str, bad_value: float | int, pattern: str
) -> None:
    df = _sample_valid_df()
    df.loc[0, column] = bad_value
    with pytest.raises(ValueError, match=pattern):
        validate_schema(df)
