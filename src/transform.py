"""
Transform layer for the NYC Real Estate pipeline.

Handles the real-world messiness of the DOF rolling sales export:
- SALE PRICE / LAND SQUARE FEET / GROSS SQUARE FEET arrive as strings with
  placeholder values like " -  " instead of true nulls.
- Many "sales" are $0 or nominal-dollar transfers (family transfers, estate
  settlements) rather than arm's-length market transactions - these are kept
  but flagged, not silently dropped, since dropping them would misrepresent
  the source data.
- BOROUGH ships as an integer code and is mapped to its name for readability.
- Duplicate rows exist in the raw export and are removed.
"""
from __future__ import annotations

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

BOROUGH_MAP = {
    1: "Manhattan",
    2: "Bronx",
    3: "Brooklyn",
    4: "Queens",
    5: "Staten Island",
}

_NUMERIC_STRING_COLUMNS = ["SALE PRICE", "LAND SQUARE FEET", "GROSS SQUARE FEET"]


def _clean_numeric_string_column(series: pd.Series) -> pd.Series:
    """Turn columns like ' -  ' / '1,234' / '  8000000' into proper floats."""
    cleaned = (
        series.astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
        .replace({"": np.nan, "-": np.nan})
    )
    return pd.to_numeric(cleaned, errors="coerce")


def transform(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Transforming %d raw rows", len(df))
    df = df.copy()

    # --- Standardize whitespace in string/object columns
    obj_cols = df.select_dtypes(include=["object", "str"]).columns
    for col in obj_cols:
        df[col] = df[col].astype(str).str.strip()

    # --- Coerce known-messy numeric-as-string columns
    for col in _NUMERIC_STRING_COLUMNS:
        df[col] = _clean_numeric_string_column(df[col])

    # --- Parse sale date
    df["SALE DATE"] = pd.to_datetime(df["SALE DATE"], errors="coerce")

    # --- Human-readable borough name alongside the raw code
    df["BOROUGH_NAME"] = df["BOROUGH"].map(BOROUGH_MAP)

    # --- Flag non-arm's-length transfers instead of dropping them
    df["IS_ARMS_LENGTH_SALE"] = df["SALE PRICE"].fillna(0) >= 10_000

    # --- Drop exact duplicate rows introduced by the source export
    before = len(df)
    df = df.drop_duplicates()
    logger.info("Dropped %d exact duplicate rows", before - len(df))

    # --- Drop rows with no sale date or missing borough - unusable for analysis
    before = len(df)
    df = df.dropna(subset=["SALE DATE", "BOROUGH"])
    logger.info("Dropped %d rows with unusable core fields", before - len(df))

    # --- Sanity-bound year built (source has some 0 / clearly-wrong values)
    current_year = pd.Timestamp.now().year
    df.loc[(df["YEAR BUILT"] < 1800) | (df["YEAR BUILT"] > current_year), "YEAR BUILT"] = np.nan

    df = df.rename(columns=lambda c: c.strip().lower().replace(" ", "_").replace("-", "_"))

    logger.info("Transform complete: %d clean rows, %d columns", len(df), len(df.columns))
    return df


if __name__ == "__main__":
    from extract import extract

    logging.basicConfig(level=logging.INFO)
    raw = extract()
    clean = transform(raw)
    print(clean.head())
    print(clean.dtypes)
