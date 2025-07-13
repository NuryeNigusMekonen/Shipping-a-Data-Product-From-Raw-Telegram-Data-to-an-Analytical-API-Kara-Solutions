FROM python:3.10-slim

# Install system dependencies for PostgreSQL and build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dbt-postgres
RUN pip install --no-cache-dir dbt-postgres

# Create app directory and set it as working directory
WORKDIR /usr/app

# Copy your project files (optional here; you can also mount later)
# COPY . /usr/app

# Default command (optional, you can override in docker-compose or CLI)
# ENTRYPOINT ["dbt"]
