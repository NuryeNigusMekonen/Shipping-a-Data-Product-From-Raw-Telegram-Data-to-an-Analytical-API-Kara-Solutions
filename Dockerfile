FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt


COPY . .

# Make necessary init files (optional)
RUN touch src/__init__.py && touch src/api/__init__.py && touch src/db/__init__.py

RUN chmod +x ./start.sh

CMD ["./start.sh"]
