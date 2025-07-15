from dagster import Definitions
from telegram_pipeline.jobs import telegram_data_pipeline

defs = Definitions(jobs=[telegram_data_pipeline])
