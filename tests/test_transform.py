import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from transform import transform, _clean_numeric_string_column  # noqa: E402
from data_quality import run_data_quality_checks, DataQualityError  # noqa: E402


def _make_raw_frame(n=1500):
    return pd.DataFrame({
        "BOROUGH": [1] * n,
        "NEIGHBORHOOD": ["ALPHABET CITY"] * n,
        "BUILDING CLASS CATEGORY": ["07 RENTALS"] * n,
        "TAX CLASS AT PRESENT": ["2A"] * n,
        "BLOCK": list(range(n)),
        "LOT": [6] * n,
        "EASE-MENT": [" "] * n,
        "BUILDING CLASS AT PRESENT": ["C2"] * n,
        "ADDRESS": ["153 AVENUE B"] * n,
        "APARTMENT NUMBER": [" "] * n,
        "ZIP CODE": [10009] * n,
        "RESIDENTIAL UNITS": [5] * n,
        "COMMERCIAL UNITS": [0] * n,
        "TOTAL UNITS": [5] * n,
        "LAND SQUARE FEET": ["1,633"] * n,
        "GROSS SQUARE FEET": [" -  "] * n,
        "YEAR BUILT": [1900] * n,
        "TAX CLASS AT TIME OF SALE": [2] * n,
        "BUILDING CLASS AT TIME OF SALE": ["C2"] * n,
        "SALE PRICE": ["6625000"] * n,
        "SALE DATE": ["2017-07-19 00:00:00"] * n,
    })


def test_clean_numeric_string_column_handles_placeholders():
    s = pd.Series(["6625000", " -  ", "1,234", ""])
    out = _clean_numeric_string_column(s)
    assert out.iloc[0] == 6625000
    assert pd.isna(out.iloc[1])
    assert out.iloc[2] == 1234
    assert pd.isna(out.iloc[3])


def test_transform_produces_expected_columns():
    raw = _make_raw_frame()
    clean = transform(raw)
    assert "borough_name" in clean.columns
    assert "is_arms_length_sale" in clean.columns
    assert clean["borough_name"].iloc[0] == "Manhattan"


def test_transform_drops_rows_missing_sale_date():
    raw = _make_raw_frame()
    raw.loc[0, "SALE DATE"] = None
    clean = transform(raw)
    assert len(clean) == len(raw) - 1


def test_transform_flags_nominal_transfers_not_drops_them():
    raw = _make_raw_frame()
    raw.loc[0, "SALE PRICE"] = "0"
    clean = transform(raw)
    assert len(clean) == len(raw)  # not dropped
    assert clean.loc[clean["sale_price"] == 0, "is_arms_length_sale"].iloc[0] == False  # noqa: E712


def test_data_quality_passes_on_clean_data():
    raw = _make_raw_frame()
    clean = transform(raw)
    results = run_data_quality_checks(clean)
    assert all(r.passed for r in results)


def test_data_quality_fails_on_too_few_rows():
    raw = _make_raw_frame(n=10)
    clean = transform(raw)
    with pytest.raises(DataQualityError):
        run_data_quality_checks(clean)


def test_data_quality_fails_on_negative_sale_price():
    raw = _make_raw_frame()
    clean = transform(raw)
    clean.loc[0, "sale_price"] = -100
    with pytest.raises(DataQualityError):
        run_data_quality_checks(clean)
