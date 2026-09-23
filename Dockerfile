FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY src/ ./src/
COPY data/raw/merged_df.csv ./data/raw/merged_df.csv

WORKDIR /app/src

EXPOSE 8080

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-8080} app:server"]
