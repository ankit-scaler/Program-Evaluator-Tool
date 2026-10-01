# Scaler Program Evaluator - Production Container
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY src/ ./src/
COPY web/ ./web/
COPY output/ ./output/
COPY metabase_config.json .
COPY run_app.py .

# Create volume for persistent SQLite leads store and logs
VOLUME ["/app/output"]

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Start production server (respects Railway's dynamic PORT variable)
CMD sh -c "uvicorn src.server:app --host 0.0.0.0 --port ${PORT:-8000} --workers 2"
