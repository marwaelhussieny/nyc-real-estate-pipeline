"""
Extract layer for the NYC Real Estate pipeline.

Source: NYC Department of Finance - Citywide Rolling Sales
(https://www.nyc.gov/site/finance/property/property-rolling-sales-data.page)

In production this would hit the NYC Open Data Socrata API directly. This
module abstracts the source behind `extract()` so swapping the CSV for a
live API call later is a one-function change, not a pipeline rewrite.
"""
from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

RAW_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "nyc-rolling-sales.csv"

EXPECTED_COLUMNS = [
    "BOROUGH", "NEIGHBORHOOD", "BUILDING CLASS CATEGORY", "TAX CLASS AT PRESENT",
    "BLOCK", "LOT", "EASE-MENT", "BUILDING CLASS AT PRESENT", "ADDRESS",
    "APARTMENT NUMBER", "ZIP CODE", "RESIDENTIAL UNITS", "COMMERCIAL UNITS",
    "TOTAL UNITS", "LAND SQUARE FEET", "GROSS SQUARE FEET", "YEAR BUILT",
    "TAX CLASS AT TIME OF SALE", "BUILDING CLASS AT TIME OF SALE",
    "SALE PRICE", "SALE DATE",
]


def extract(path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Read the raw rolling-sales CSV and do a light schema sanity check."""
    logger.info("Extracting raw sales data from %s", path)
    df = pd.read_csv(path)

    # The source CSV ships an unlabeled index column - drop it if present.
    unnamed_cols = [c for c in df.columns if c.startswith("Unnamed")]
    if unnamed_cols:
        df = df.drop(columns=unnamed_cols)

    missing = set(EXPECTED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Source schema drift detected, missing columns: {missing}")

    logger.info("Extracted %d raw rows, %d columns", len(df), len(df.columns))
    return df


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    frame = extract()
    print(frame.head())
