"""
Lightweight data-quality gate, run between transform and load.

Deliberately dependency-free (no Great Expectations) to keep the project
runnable anywhere, but the structure mirrors an expectation suite: a list of
named checks, each producing a pass/fail + human-readable detail, so the
DAG can fail loudly and specifically instead of a generic "task failed".
"""
from __future__ import annotations

import logging
from dataclasses import dataclass

import pandas as pd

logger = logging.getLogger(__name__)


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str


class DataQualityError(Exception):
    """Raised when one or more data quality checks fail."""


def _check_row_count(df: pd.DataFrame, minimum: int = 1000) -> CheckResult:
    passed = len(df) >= minimum
    return CheckResult(
        "row_count_minimum",
        passed,
        f"expected >= {minimum} rows, got {len(df)}",
    )


def _check_no_null_key_columns(df: pd.DataFrame) -> CheckResult:
    key_cols = ["borough", "sale_date", "block", "lot"]
    null_counts = df[key_cols].isnull().sum()
    passed = bool((null_counts == 0).all())
    return CheckResult(
        "no_nulls_in_key_columns",
        passed,
        f"null counts: {null_counts.to_dict()}",
    )


def _check_sale_price_non_negative(df: pd.DataFrame) -> CheckResult:
    negative = (df["sale_price"] < 0).sum()
    passed = negative == 0
    return CheckResult(
        "sale_price_non_negative",
        passed,
        f"{negative} rows with negative sale price",
    )


def _check_borough_values_valid(df: pd.DataFrame) -> CheckResult:
    valid = {1, 2, 3, 4, 5}
    invalid = set(df["borough"].unique()) - valid
    passed = len(invalid) == 0
    return CheckResult(
        "borough_values_valid",
        passed,
        f"unexpected borough codes: {invalid}" if invalid else "all borough codes valid",
    )


def _check_sale_date_not_future(df: pd.DataFrame) -> CheckResult:
    future_rows = (df["sale_date"] > pd.Timestamp.now()).sum()
    passed = future_rows == 0
    return CheckResult(
        "sale_date_not_in_future",
        passed,
        f"{future_rows} rows with a sale_date in the future",
    )


CHECKS = [
    _check_row_count,
    _check_no_null_key_columns,
    _check_sale_price_non_negative,
    _check_borough_values_valid,
    _check_sale_date_not_future,
]


def run_data_quality_checks(df: pd.DataFrame) -> list[CheckResult]:
    results = [check(df) for check in CHECKS]

    for r in results:
        level = logging.INFO if r.passed else logging.ERROR
        logger.log(level, "[%s] %s - %s", "PASS" if r.passed else "FAIL", r.name, r.detail)

    failed = [r for r in results if not r.passed]
    if failed:
        names = ", ".join(r.name for r in failed)
        raise DataQualityError(f"Data quality checks failed: {names}")

    return results


if __name__ == "__main__":
    from extract import extract
    from transform import transform

    logging.basicConfig(level=logging.INFO)
    clean = transform(extract())
    run_data_quality_checks(clean)
    print("All data quality checks passed.")
