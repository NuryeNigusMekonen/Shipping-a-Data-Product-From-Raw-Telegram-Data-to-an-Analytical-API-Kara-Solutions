from dagster import op, Out, Nothing
import subprocess
import logging
import os

logger = logging.getLogger(__name__)

# Set your project root here (adjust if needed)
PROJECT_ROOT = "/home/nurye/Desktop/10_Academy/week_7/Shipping-a-Data-Product-From-Raw-Telegram-Data-to-an-Analytical-API-Kara-Solutions"

def run_command(command, cwd=PROJECT_ROOT):
    logger.info(f"Running command: {' '.join(command)} in {cwd}")
    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            cwd=cwd,
        )
        logger.info(f"Command succeeded: {' '.join(command)}")
        logger.info(f"STDOUT:\n{result.stdout}")
        logger.info(f"STDERR:\n{result.stderr}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {' '.join(command)}")
        logger.error(f"Exit code: {e.returncode}")
        logger.error(f"STDOUT:\n{e.stdout}")
        logger.error(f"STDERR:\n{e.stderr}")
        raise e

@op(out=Out(Nothing))
def scrape_telegram_data():
    run_command(["python3", "src/telegram_scraper.py"])

@op(out=Out(Nothing))
def load_raw_to_postgres():
    run_command(["python3", "load_to_postgres.py"])

@op(out=Out(Nothing))
def run_dbt_transformations():
    run_command(["dbt", "run", "--project-dir=telegram_dbt/telegram_project"])

@op(out=Out(Nothing))
def run_yolo_enrichment():
    run_command(["python3", "detect_objects.py"])

@op(out=Out(Nothing))
def load_yolo_results_to_postgres():
    run_command(["python3", "load_image_detections.py"])
