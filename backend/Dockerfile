FROM python:3.12-slim

WORKDIR /app

# System dependencies (curl for healthcheck, build essentials for psycopg)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run migrations then start the server
CMD ["sh", "-c", "python -m scripts.migrate && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
