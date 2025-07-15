# telegram_pipeline/jobs.py
from dagster import job
from .ops import scrape_telegram_data, load_raw_to_postgres, run_dbt_transformations, run_yolo_enrichment, load_yolo_results_to_postgres

@job
def scrape_job():
    scrape_telegram_data()

@job
def load_postgres_job():   # 👈 This should exactly be here
    load_raw_to_postgres()

@job
def dbt_run_job():
    run_dbt_transformations()

@job
def yolo_enrich_job():
    run_yolo_enrichment()

@job
def load_yolo_job():
    load_yolo_results_to_postgres()
