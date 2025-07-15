from dagster import job
from .ops import (
    scrape_telegram_data,
    load_raw_to_postgres,
    run_dbt_transformations,
    run_yolo_enrichment,
    load_yolo_results_to_postgres,
)

@job
def telegram_data_pipeline():
    scrape = scrape_telegram_data()
    load_raw = load_raw_to_postgres(scrape)
    dbt = run_dbt_transformations(load_raw)
    yolo = run_yolo_enrichment(dbt)
    load_yolo = load_yolo_results_to_postgres(yolo)


