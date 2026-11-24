"""Limpeza, enriquecimento e verificação de qualidade do dataset Gapminder."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.data_loader import PROJECT_ROOT, RAW_DATA_PATH, load_raw_gapminder

PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "gapminder_clean.csv"


def clean_gapminder(df: pd.DataFrame) -> pd.DataFrame:
    """Padroniza tipos, remove espaços extras/duplicatas e ordena por país e ano."""
    cleaned = df.copy()
    cleaned["country"] = cleaned["country"].astype(str).str.strip()
    cleaned["continent"] = cleaned["continent"].astype(str).str.strip()
    cleaned["year"] = cleaned["year"].astype("int64")
    cleaned["pop"] = cleaned["pop"].astype("int64")
    cleaned["lifeExp"] = cleaned["lifeExp"].astype("float64")
    cleaned["gdpPercap"] = cleaned["gdpPercap"].astype("float64")

    cleaned = (
        cleaned.drop_duplicates(subset=["country", "year"], keep="first")
        .sort_values(["country", "year"], kind="mergesort")
        .reset_index(drop=True)
    )
    return cleaned


def add_derived_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona PIB total, década e variações quinquenais por país sem mutar o original."""
    enriched = df.copy()
    enriched["gdp_total"] = enriched["gdpPercap"] * enriched["pop"]
    enriched["decade"] = (enriched["year"] // 10) * 10
    enriched["lifeExp_diff_5y"] = enriched.groupby("country")["lifeExp"].diff()
    enriched["gdpPercap_pct_change_5y"] = (
        enriched.groupby("country")["gdpPercap"].pct_change() * 100.0
    )
    return enriched


def generate_quality_report(df: pd.DataFrame) -> dict[str, object]:
    """Gera um resumo estruturado de qualidade dos dados."""
    return {
        "rows": int(len(df)),
        "countries": int(df["country"].nunique()),
        "continents": int(df["continent"].nunique()),
        "year_min": int(df["year"].min()),
        "year_max": int(df["year"].max()),
        "duplicate_country_year": int(df.duplicated(subset=["country", "year"]).sum()),
        "nulls_core_columns": {
            col: int(df[col].isna().sum())
            for col in ("country", "continent", "year", "lifeExp", "pop", "gdpPercap")
        },
    }


def run_cleaning_pipeline(
    raw_path: Path = RAW_DATA_PATH,
    output_path: Path = PROCESSED_DATA_PATH,
) -> pd.DataFrame:
    """Executa carregamento, limpeza, enriquecimento e exportação do CSV tratado."""
    raw_df = load_raw_gapminder(path=raw_path, download_if_missing=False)
    cleaned_df = clean_gapminder(raw_df)
    enriched_df = add_derived_metrics(cleaned_df)

    dest = Path(output_path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    enriched_df.to_csv(dest, index=False)
    return enriched_df
