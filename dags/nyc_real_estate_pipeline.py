"""
NYC Real Estate Sales Pipeline
===============================
Extract -> Transform -> Data Quality Gate -> Load (RDS Postgres)

Runs weekly, matching the cadence of the NYC DOF rolling-sales publication.
Each stage is a separate task using XCom to pass the DataFrame reference
(as parquet on disk) rather than the DataFrame itself, so tasks stay
independently retryable and inspectable.
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

import pendulum
from airflow.decorators import dag, task

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

logger = logging.getLogger(__name__)

INTERMEDIATE_DIR = Path("/tmp/nyc_real_estate_pipeline")
INTERMEDIATE_DIR.mkdir(parents=True, exist_ok=True)

default_args = {
    "owner": "marwa",
    "retries": 2,
    "retry_delay": pendulum.duration(minutes=5),
}


@dag(
    dag_id="nyc_real_estate_pipeline",
    description="Extract, clean, quality-check, and load NYC DOF rolling property sales into RDS Postgres",
    schedule="@weekly",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
    default_args=default_args,
    tags=["portfolio", "real-estate", "postgres", "terraform"],
)
def nyc_real_estate_pipeline():

    @task
    def extract_task() -> str:
        from extract import extract

        df = extract()
        out_path = INTERMEDIATE_DIR / "raw.parquet"
        df.to_parquet(out_path)
        return str(out_path)

    @task
    def transform_task(raw_path: str) -> str:
        import pandas as pd
        from transform import transform

        df = pd.read_parquet(raw_path)
        clean = transform(df)
        out_path = INTERMEDIATE_DIR / "clean.parquet"
        clean.to_parquet(out_path)
        return str(out_path)

    @task
    def data_quality_task(clean_path: str) -> str:
        import pandas as pd
        from data_quality import run_data_quality_checks

        df = pd.read_parquet(clean_path)
        run_data_quality_checks(df)  # raises DataQualityError on failure, fails the task
        return clean_path

    @task
    def load_task(clean_path: str) -> int:
        import pandas as pd
        from load import load

        df = pd.read_parquet(clean_path)
        return load(df)

    raw = extract_task()
    clean = transform_task(raw)
    validated = data_quality_task(clean)
    load_task(validated)


nyc_real_estate_pipeline()
