"""
Load layer: writes the cleaned DataFrame into Postgres (RDS in prod, local
Postgres in dev/CI) as an idempotent full-refresh into a staging table, then
swaps it into place - so a failed run never leaves the target table half
written.
"""
from __future__ import annotations

import logging
import os

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)

TABLE_NAME = "nyc_property_sales"
STAGING_TABLE_NAME = f"{TABLE_NAME}_staging"


def get_engine() -> Engine:
    """
    Build a SQLAlchemy engine from a DB_CONN_STRING env var, e.g.:
    postgresql://user:password@host:5432/dbname
    Set this in Airflow via an .env file / Airflow Connection, never hardcode it.
    """
    conn_string = os.environ.get("DB_CONN_STRING")
    if not conn_string:
        raise RuntimeError("DB_CONN_STRING environment variable is not set.")
    return create_engine(conn_string)


def load(df: pd.DataFrame, engine: Engine | None = None) -> int:
    engine = engine or get_engine()

    logger.info("Loading %d rows into staging table '%s'", len(df), STAGING_TABLE_NAME)
    df.to_sql(STAGING_TABLE_NAME, engine, if_exists="replace", index=False, chunksize=5000)

    with engine.begin() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS {TABLE_NAME}_old"))
        conn.execute(text(
            f"ALTER TABLE IF EXISTS {TABLE_NAME} RENAME TO {TABLE_NAME}_old"
        ))
        conn.execute(text(
            f"ALTER TABLE {STAGING_TABLE_NAME} RENAME TO {TABLE_NAME}"
        ))
        conn.execute(text(f"DROP TABLE IF EXISTS {TABLE_NAME}_old"))

    logger.info("Load complete: '%s' now has %d rows", TABLE_NAME, len(df))
    return len(df)


if __name__ == "__main__":
    from extract import extract
    from transform import transform
    from data_quality import run_data_quality_checks

    logging.basicConfig(level=logging.INFO)
    clean = transform(extract())
    run_data_quality_checks(clean)
    load(clean)
