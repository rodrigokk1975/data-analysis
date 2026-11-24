"""Ingestão reproduzível e validação de schema do dataset público Gapminder."""

from __future__ import annotations

from pathlib import Path
from urllib.request import urlretrieve

import pandas as pd

GAPMINDER_URL = (
    "https://raw.githubusercontent.com/jennybc/gapminder/main/inst/extdata/gapminder.tsv"
)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "gapminder.tsv"

EXPECTED_COLUMNS: tuple[str, ...] = (
    "country",
    "continent",
    "year",
    "lifeExp",
    "pop",
    "gdpPercap",
)
EXPECTED_CONTINENTS: frozenset[str] = frozenset(
    {"Africa", "Americas", "Asia", "Europe", "Oceania"}
)
EXPECTED_YEARS: frozenset[int] = frozenset(range(1952, 2008, 5))


def download_gapminder(
    dest_path: Path = RAW_DATA_PATH,
    url: str = GAPMINDER_URL,
    force: bool = False,
) -> Path:
    """Baixa o arquivo bruto do Gapminder se ainda não existir localmente."""
    dest = Path(dest_path)
    if dest.exists() and not force:
        return dest

    dest.parent.mkdir(parents=True, exist_ok=True)
    urlretrieve(url, dest)
    return dest


def validate_schema(df: pd.DataFrame) -> pd.DataFrame:
    """Valida colunas obrigatórias, ausência de nulos e regras de domínio."""
    missing = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Colunas obrigatórias ausentes: {missing}")

    if df.empty:
        raise ValueError("O DataFrame está vazio.")

    null_counts = df[list(EXPECTED_COLUMNS)].isna().sum()
    cols_with_nulls = null_counts[null_counts > 0].to_dict()
    if cols_with_nulls:
        raise ValueError(f"Valores nulos encontrados: {cols_with_nulls}")

    invalid_continents = set(df["continent"].unique()) - EXPECTED_CONTINENTS
    if invalid_continents:
        raise ValueError(f"Continentes inválidos encontrados: {sorted(invalid_continents)}")

    invalid_years = set(df["year"].astype(int).unique()) - EXPECTED_YEARS
    if invalid_years:
        raise ValueError(f"Anos fora do recorte esperado (1952-2007, passo 5): {invalid_years}")

    if not ((df["lifeExp"] > 0) & (df["lifeExp"] < 100)).all():
        raise ValueError("Valores de 'lifeExp' fora do intervalo válido (0, 100).")

    if not (df["pop"] > 0).all():
        raise ValueError("Valores de 'pop' devem ser estritamente positivos.")

    if not (df["gdpPercap"] > 0).all():
        raise ValueError("Valores de 'gdpPercap' devem ser estritamente positivos.")

    return df


def load_raw_gapminder(
    path: Path = RAW_DATA_PATH,
    download_if_missing: bool = True,
) -> pd.DataFrame:
    """Carrega e valida o dataset bruto do Gapminder."""
    file_path = Path(path)
    if not file_path.exists():
        if not download_if_missing:
            raise FileNotFoundError(f"Arquivo bruto não encontrado: {file_path}")
        download_gapminder(dest_path=file_path)

    df = pd.read_csv(file_path, sep="\t")
    return validate_schema(df)
