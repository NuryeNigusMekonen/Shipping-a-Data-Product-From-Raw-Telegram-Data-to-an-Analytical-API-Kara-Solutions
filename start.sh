#!/bin/bash
echo "Starting Telegram Scraper API..."
exec uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --no-access-log
