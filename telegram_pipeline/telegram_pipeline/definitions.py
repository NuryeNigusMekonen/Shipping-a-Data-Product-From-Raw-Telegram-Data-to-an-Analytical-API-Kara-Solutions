# telegram_pipeline/definitions.py
from dagster import repository
from .jobs import (
    scrape_job,
    load_postgres_job,   #  This import fails if not defined in jobs.py
    dbt_run_job,
    yolo_enrich_job,
    load_yolo_job,
)


@repository
def defs():
    return [
        scrape_job,
        load_postgres_job,
        dbt_run_job,
        yolo_enrich_job,
        load_yolo_job,
    ]
