from dagster import ScheduleDefinition
from .jobs import full_pipeline

daily_schedule = ScheduleDefinition(
    job=full_pipeline,
    cron_schedule="0 5 * * *",  # everyday at 5 AM
    name="daily_pipeline_schedule"
)
