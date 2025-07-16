FROM python:3.10-slim

WORKDIR /usr/app

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir dbt-postgres

COPY telegram_dbt/telegram_project ./telegram_project

WORKDIR /usr/app/telegram_project

CMD ["dbt", "run"]
