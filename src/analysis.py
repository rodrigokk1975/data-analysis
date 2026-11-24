"""Síntese estatística, correlações, rankings e detecção de outliers do Gapminder."""

from __future__ import annotations

import numpy as np
import pandas as pd


def continent_summary(
    df: pd.DataFrame,
    years: tuple[int, ...] = (1952, 2007),
) -> pd.DataFrame:
    """Calcula estatísticas descritivas de expectativa de vida e PIB per capita por continente."""
    subset = df[df["year"].isin(years)]
    summary = (
        subset.groupby(["continent", "year"], as_index=False)
        .agg(
            countries=("country", "nunique"),
            lifeExp_mean=("lifeExp", "mean"),
            lifeExp_median=("lifeExp", "median"),
            lifeExp_std=("lifeExp", "std"),
            lifeExp_min=("lifeExp", "min"),
            lifeExp_max=("lifeExp", "max"),
            gdpPercap_median=("gdpPercap", "median"),
        )
        .sort_values(["continent", "year"])
        .reset_index(drop=True)
    )
    return summary


def global_weighted_life_expectancy(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula a expectativa de vida média global ponderada pela população por ano."""
    weighted = (
        df.groupby("year")
        .apply(
            lambda g: float(np.average(g["lifeExp"], weights=g["pop"])),
            include_groups=False,
        )
        .reset_index(name="lifeExp_weighted")
    )
    return weighted


def gdp_life_expectancy_correlations(df: pd.DataFrame, year: int = 2007) -> dict[str, float]:
    """Calcula correlações Pearson (linear e log10) e Spearman entre PIB per capita e lifeExp."""
    subset = df[df["year"] == year]
    if subset.empty:
        raise ValueError(f"Nenhum registro encontrado para o ano {year}.")

    pearson_linear = float(subset["gdpPercap"].corr(subset["lifeExp"], method="pearson"))
    pearson_log10 = float(np.log10(subset["gdpPercap"]).corr(subset["lifeExp"], method="pearson"))
    spearman = float(subset["gdpPercap"].rank().corr(subset["lifeExp"].rank(), method="pearson"))
    return {
        "pearson_linear": round(pearson_linear, 4),
        "pearson_log10": round(pearson_log10, 4),
        "spearman": round(spearman, 4),
    }


def top_life_expectancy_gains(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Retorna os países com maior ganho absoluto e percentual em expectativa de vida."""
    y1952 = df[df["year"] == 1952][["country", "continent", "lifeExp", "gdpPercap"]].rename(
        columns={"lifeExp": "lifeExp_1952", "gdpPercap": "gdpPercap_1952"}
    )
    y2007 = df[df["year"] == 2007][["country", "lifeExp", "gdpPercap"]].rename(
        columns={"lifeExp": "lifeExp_2007", "gdpPercap": "gdpPercap_2007"}
    )
    merged = y1952.merge(y2007, on="country")
    merged["lifeExp_gain"] = merged["lifeExp_2007"] - merged["lifeExp_1952"]
    merged["lifeExp_gain_pct"] = (merged["lifeExp_gain"] / merged["lifeExp_1952"]) * 100.0
    return (
        merged.nlargest(top_n, "lifeExp_gain")
        .reset_index(drop=True)
    )


def detect_sharpest_drops(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Identifica as quedas quinquenais mais severas de expectativa de vida."""
    drops = (
        df.dropna(subset=["lifeExp_diff_5y"])
        .nsmallest(top_n, "lifeExp_diff_5y")[
            ["country", "continent", "year", "lifeExp", "lifeExp_diff_5y"]
        ]
        .reset_index(drop=True)
    )
    return drops


def build_summary_metrics(df: pd.DataFrame) -> dict[str, object]:
    """Consolida os principais indicadores quantitativos para relatório e documentação."""
    weighted = global_weighted_life_expectancy(df)
    w_1952 = float(weighted.loc[weighted["year"] == 1952, "lifeExp_weighted"].iloc[0])
    w_2007 = float(weighted.loc[weighted["year"] == 2007, "lifeExp_weighted"].iloc[0])
    corrs_2007 = gdp_life_expectancy_correlations(df, year=2007)
    top_gain = top_life_expectancy_gains(df, top_n=1).iloc[0]
    worst_drop = detect_sharpest_drops(df, top_n=1).iloc[0]

    return {
        "global_weighted_lifeExp_1952": round(w_1952, 2),
        "global_weighted_lifeExp_2007": round(w_2007, 2),
        "global_weighted_gain": round(w_2007 - w_1952, 2),
        "correlations_2007": corrs_2007,
        "top_gain_country": str(top_gain["country"]),
        "top_gain_years": round(float(top_gain["lifeExp_gain"]), 2),
        "worst_drop_country": str(worst_drop["country"]),
        "worst_drop_year": int(worst_drop["year"]),
        "worst_drop_years": round(float(worst_drop["lifeExp_diff_5y"]), 2),
    }
