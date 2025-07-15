FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install dagster dagit dagster-postgres

EXPOSE 3000

CMD ["dagit", "-h", "0.0.0.0", "-p", "3000"]
