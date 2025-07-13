# Telegram Health Data Pipeline — Kara Solutions

## Overview
End-to-end pipeline for scraping, modeling, enriching, and serving Telegram data related to Ethiopian medical businesses.

## Tech Stack
- **Telethon**: Telegram scraping
- **PostgreSQL**: Data warehouse
- **dbt**: Transformation and modeling
- **YOLOv8 (Ultralytics)**: Object detection
- **FastAPI**: Analytical API
- **Dagster**: Pipeline orchestration
- **Docker**: Environment management

## Setup Instructions

### 1. Clone & Setup
```bash
git clone https://github.com/your-username/telegram-health-data-pipeline.git
cd telegram-health-data-pipeline
cp .env.example .env  
