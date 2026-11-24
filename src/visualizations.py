"""Visualizações padronizadas em Matplotlib e Seaborn para o dataset Gapminder."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure

from src.data_loader import PROJECT_ROOT

FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"
SOURCE_FOOTER = "Fonte: Gapminder Foundation (1952–2007)"

# Paleta colorblind-safe (Okabe-Ito) fixa por continente para consistência entre gráficos
CONTINENT_PALETTE: dict[str, str] = {
    "Africa": "#E69F00",
    "Americas": "#009E73",
    "Asia": "#D55E00",
    "Europe": "#0072B2",
    "Oceania": "#CC79A7",
}

CONTINENT_LABELS_PT: dict[str, str] = {
    "Africa": "África",
    "Americas": "Américas",
    "Asia": "Ásia",
    "Europe": "Europa",
    "Oceania": "Oceania",
}


def configure_theme() -> None:
    """Aplica o tema visual padrão do projeto."""
    sns.set_theme(style="whitegrid", context="notebook", font_scale=1.05)
    plt.rcParams.update(
        {
            "axes.titlesize": 13,
            "axes.titleweight": "bold",
            "axes.labelsize": 11,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "grid.alpha": 0.35,
        }
    )


def _finalize_and_save(fig: Figure, output_path: Path | None, footer: str = SOURCE_FOOTER) -> None:
    fig.text(0.01, -0.02, footer, fontsize=9, color="#555555", ha="left")
    if output_path is not None:
        dest = Path(output_path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(dest, dpi=300, bbox_inches="tight")


def plot_life_expectancy_evolution(
    df: pd.DataFrame,
    output_path: Path | None = None,
) -> Figure:
    """Gráfico 1: Evolução da expectativa de vida média por continente (1952–2007)."""
    configure_theme()
    fig, ax = plt.subplots(figsize=(10.5, 6))

    continent_yearly = (
        df.groupby(["year", "continent"], as_index=False)["lifeExp"].mean()
    )
    global_weighted = (
        df.groupby("year")
        .apply(
            lambda g: float(np.average(g["lifeExp"], weights=g["pop"])),
            include_groups=False,
        )
        .reset_index(name="lifeExp")
    )

    for continent, color in CONTINENT_PALETTE.items():
        subset = continent_yearly[continent_yearly["continent"] == continent]
        label = CONTINENT_LABELS_PT[continent]
        ax.plot(
            subset["year"],
            subset["lifeExp"],
            marker="o",
            linewidth=2.4,
            markersize=5,
            color=color,
            label=label,
        )
        last = subset.iloc[-1]
        ax.annotate(
            f"{label} ({last['lifeExp']:.1f})",
            xy=(last["year"], last["lifeExp"]),
            xytext=(6, 0),
            textcoords="offset points",
            va="center",
            fontsize=9.5,
            fontweight="bold",
            color=color,
        )

    ax.plot(
        global_weighted["year"],
        global_weighted["lifeExp"],
        linestyle="--",
        linewidth=2.0,
        color="#333333",
        label="Média Global (ponderada por pop.)",
    )

    ax.set_title(
        "Evolução da Expectativa de Vida por Continente (1952–2007)\n"
        "Avanço generalizado em todas as regiões, com estagnação na África a partir dos anos 1990",
        loc="left",
        pad=14,
    )
    ax.set_xlabel("Ano")
    ax.set_ylabel("Expectativa de Vida Média (anos)")
    ax.set_xlim(1950, 2016)
    ax.set_ylim(35, 86)
    ax.set_xticks(sorted(df["year"].unique()))
    ax.legend(loc="lower right", frameon=True, framealpha=0.92, fontsize=9)
    sns.despine(ax=ax)

    _finalize_and_save(fig, output_path)
    return fig


def plot_gdp_vs_life_expectancy_2007(
    df: pd.DataFrame,
    output_path: Path | None = None,
) -> Figure:
    """Gráfico 2: PIB per capita (escala log) vs. expectativa de vida em 2007."""
    configure_theme()
    df_2007 = df[df["year"] == 2007].copy()

    fig, ax = plt.subplots(figsize=(10.5, 6.2))
    sizes = np.sqrt(df_2007["pop"]) / 65.0

    for continent, color in CONTINENT_PALETTE.items():
        subset = df_2007[df_2007["continent"] == continent]
        sub_sizes = sizes.loc[subset.index]
        ax.scatter(
            subset["gdpPercap"],
            subset["lifeExp"],
            s=sub_sizes,
            color=color,
            alpha=0.78,
            edgecolors="white",
            linewidth=0.8,
            label=CONTINENT_LABELS_PT[continent],
        )

    ax.set_xscale("log")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${int(x):,}"))
    ax.set_xticks([500, 1000, 2000, 5000, 10000, 20000, 50000])

    highlights = {
        "Brazil": (8, -12),
        "China": (10, -4),
        "India": (10, -10),
        "Japan": (-36, 6),
        "Norway": (-42, -14),
        "United States": (-60, -16),
        "Swaziland": (8, 4),
    }
    for country, offset in highlights.items():
        row = df_2007[df_2007["country"] == country]
        if not row.empty:
            r = row.iloc[0]
            ax.annotate(
                country,
                xy=(r["gdpPercap"], r["lifeExp"]),
                xytext=offset,
                textcoords="offset points",
                fontsize=9,
                fontweight="bold",
                color="#222222",
                arrowprops={"arrowstyle": "-", "color": "#888888", "lw": 0.8},
            )

    ax.set_title(
        "PIB per Capita vs. Expectativa de Vida em 2007 (Escala Logarítmica)\n"
        "Relação log-linear com retornos decrescentes acima de US$ 15 mil; bolhas = população",
        loc="left",
        pad=14,
    )
    ax.set_xlabel("PIB per Capita em USD (PPP, escala logarítmica)")
    ax.set_ylabel("Expectativa de Vida (anos)")
    ax.set_ylim(35, 87)
    legend = ax.legend(title="Continente", loc="lower right", frameon=True, framealpha=0.92)
    for handle in legend.legend_handles:
        handle._sizes = [70]
    sns.despine(ax=ax)

    _finalize_and_save(fig, output_path)
    return fig


def plot_life_expectancy_distribution_comparison(
    df: pd.DataFrame,
    output_path: Path | None = None,
) -> Figure:
    """Gráfico 3: Distribuição e desigualdade intra-continental em 1952 vs. 2007."""
    configure_theme()
    subset = df[df["year"].isin([1952, 2007])].copy()
    subset["continent_pt"] = subset["continent"].map(CONTINENT_LABELS_PT)
    subset["year_str"] = subset["year"].astype(str)

    order = ["África", "Ásia", "Américas", "Europa", "Oceania"]

    fig, ax = plt.subplots(figsize=(10.5, 6))
    sns.boxplot(
        data=subset,
        x="continent_pt",
        y="lifeExp",
        hue="year_str",
        order=order,
        palette={"1952": "#A6CEE3", "2007": "#1F78B4"},
        width=0.6,
        linewidth=1.3,
        fliersize=4,
        ax=ax,
    )

    ax.set_title(
        "Distribuição da Expectativa de Vida por Continente: 1952 vs. 2007\n"
        "Europa e Américas reduziram drasticamente a dispersão; África manteve alta desigualdade",
        loc="left",
        pad=14,
    )
    ax.set_xlabel("Continente")
    ax.set_ylabel("Expectativa de Vida (anos)")
    ax.set_ylim(25, 88)
    ax.legend(title="Ano", loc="lower right", frameon=True)
    sns.despine(ax=ax)

    _finalize_and_save(fig, output_path)
    return fig


def plot_top_life_expectancy_gains(
    df: pd.DataFrame,
    top_n: int = 10,
    output_path: Path | None = None,
) -> Figure:
    """Gráfico 4: Top países com maior ganho absoluto de expectativa de vida (1952–2007)."""
    configure_theme()
    y1952 = df[df["year"] == 1952][["country", "continent", "lifeExp"]].rename(
        columns={"lifeExp": "lifeExp_1952"}
    )
    y2007 = df[df["year"] == 2007][["country", "lifeExp"]].rename(
        columns={"lifeExp": "lifeExp_2007"}
    )
    gains = y1952.merge(y2007, on="country")
    gains["gain"] = gains["lifeExp_2007"] - gains["lifeExp_1952"]
    top = gains.nlargest(top_n, "gain").sort_values("gain", ascending=True)

    fig, ax = plt.subplots(figsize=(10.5, 6))
    colors = [CONTINENT_PALETTE[c] for c in top["continent"]]
    bars = ax.barh(top["country"], top["gain"], color=colors, edgecolor="white", height=0.7)

    for bar, (_, row) in zip(bars, top.iterrows(), strict=True):
        ax.text(
            bar.get_width() + 0.5,
            bar.get_y() + bar.get_height() / 2,
            f"+{row['gain']:.1f} anos ({row['lifeExp_1952']:.1f} → {row['lifeExp_2007']:.1f})",
            va="center",
            fontsize=9.2,
            color="#222222",
        )

    ax.set_title(
        f"Top {top_n} Países com Maior Ganho em Expectativa de Vida (1952–2007)\n"
        "Países da Ásia e do Norte da África lideram a transição demográfica no período",
        loc="left",
        pad=14,
    )
    ax.set_xlabel("Ganho Absoluto em Expectativa de Vida (anos)")
    ax.set_ylabel("")
    ax.set_xlim(0, float(top["gain"].max()) + 14)

    handles = [
        plt.Line2D([0], [0], color=CONTINENT_PALETTE[c], lw=8, label=CONTINENT_LABELS_PT[c])
        for c in sorted(top["continent"].unique())
    ]
    ax.legend(handles=handles, title="Continente", loc="lower right", frameon=True)
    sns.despine(ax=ax)

    _finalize_and_save(fig, output_path)
    return fig


def plot_historical_drops_outliers(
    df: pd.DataFrame,
    top_n: int = 5,
    output_path: Path | None = None,
) -> Figure:
    """Gráfico 5: Maiores quedas abruptas em expectativa de vida (intervalos de 5 anos)."""
    configure_theme()
    ranked = df.dropna(subset=["lifeExp_diff_5y"]).sort_values("lifeExp_diff_5y")
    worst_events = ranked.drop_duplicates(subset=["country"], keep="first").head(top_n)
    target_countries = list(worst_events["country"])

    fig, ax = plt.subplots(figsize=(10.5, 6))
    palette = sns.color_palette("colorblind", n_colors=len(target_countries))

    for color, (_, event) in zip(palette, worst_events.iterrows(), strict=True):
        country = str(event["country"])
        series = df[df["country"] == country].sort_values("year")
        ax.plot(
            series["year"],
            series["lifeExp"],
            marker="o",
            linewidth=2.3,
            markersize=5,
            color=color,
            label=f"{country} ({int(event['year'])}: {event['lifeExp_diff_5y']:.1f} anos)",
        )
        ax.scatter(
            [event["year"]],
            [event["lifeExp"]],
            color=color,
            s=95,
            zorder=5,
            edgecolors="#111111",
            linewidth=1.2,
        )

    ax.set_title(
        f"Top {top_n} Quedas Abruptas de Expectativa de Vida em Intervalos de 5 Anos (1952–2007)\n"
        "Conflitos (Ruanda, Camboja) e epidemia de HIV/AIDS na África Austral dominam os outliers",
        loc="left",
        pad=14,
    )
    ax.set_xlabel("Ano")
    ax.set_ylabel("Expectativa de Vida (anos)")
    ax.set_xticks(sorted(df["year"].unique()))
    ax.set_ylim(20, 72)
    ax.legend(
        title="País (ano e maior queda em 5 anos)",
        loc="lower left",
        frameon=True,
        fontsize=9,
    )
    sns.despine(ax=ax)

    _finalize_and_save(fig, output_path)
    return fig


def generate_all_figures(df: pd.DataFrame, output_dir: Path = FIGURES_DIR) -> list[Path]:
    """Gera e salva todos os 5 gráficos oficiais do projeto em 300 DPI."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    specs = [
        ("01_evolucao_expectativa_vida_continentes.png", plot_life_expectancy_evolution),
        ("02_pib_vs_expectativa_vida_2007.png", plot_gdp_vs_life_expectancy_2007),
        (
            "03_distribuicao_expectativa_vida_decadas.png",
            plot_life_expectancy_distribution_comparison,
        ),
        ("04_top_paises_ganho_expectativa_vida.png", plot_top_life_expectancy_gains),
        ("05_outliers_quedas_historicas.png", plot_historical_drops_outliers),
    ]

    saved_paths: list[Path] = []
    for filename, plot_fn in specs:
        target = out / filename
        fig = plot_fn(df, output_path=target)
        plt.close(fig)
        saved_paths.append(target)

    return saved_paths
