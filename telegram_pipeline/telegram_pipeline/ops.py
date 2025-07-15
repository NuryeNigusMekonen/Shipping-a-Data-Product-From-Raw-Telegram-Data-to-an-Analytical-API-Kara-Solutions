from dagster import op, Out, Nothing
import subprocess
import logging

logger = logging.getLogger(__name__)

def run_command(command):
    logger.info(f"Running command: {' '.join(command)}")
    try:
        subprocess.run(command, check=True)
        logger.info(f"Command succeeded: {' '.join(command)}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {' '.join(command)}")
        raise e

@op(out=Out(Nothing))
def scrape_telegram_data():
    run_command(["python3", "src/telegram_scraper.py"])

@op(ins={"start": Nothing}, out=Out(Nothing))
def load_raw_to_postgres(start):
    run_command(["python3", "load_to_postgres.py"])

@op(ins={"start": Nothing}, out=Out(Nothing))
def run_dbt_transformations(start):
    run_command(["dbt", "run", "--project-dir=telegram_dbt/telegram_project"])

@op(ins={"start": Nothing}, out=Out(Nothing))
def run_yolo_enrichment(start):
    run_command(["python3", "detect_objects.py"])

@op(ins={"start": Nothing}, out=Out(Nothing))
def load_yolo_results_to_postgres(start):
    run_command(["python3", "load_image_detections.py"])
