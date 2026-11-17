#!/bin/sh
set -e

# Auto-generate metabase_config.json from Render environment variables
# This avoids committing credentials to git
if [ ! -f "/app/metabase_config.json" ] && [ -n "$METABASE_URL" ]; then
    echo ">> Generating metabase_config.json from environment variables..."
    cat > /app/metabase_config.json << EOF
{
  "_comment": "Auto-generated from Render environment variables at container start",
  "metabase_url": "${METABASE_URL}",
  "card_id": "${METABASE_CARD_ID:-28973}",
  "session_token": "${METABASE_SESSION_TOKEN:-}",
  "email_parameter_id": "${METABASE_EMAIL_PARAM_ID:-2dcd8f80-e4b6-46cf-936b-2102140cb7f2}",
  "api_key": "${METABASE_API_KEY:-}",
  "public_uuid": "${METABASE_PUBLIC_UUID:-}",
  "username": "${METABASE_USERNAME:-}",
  "password": "${METABASE_PASSWORD:-}",
  "timeout_seconds": ${METABASE_TIMEOUT:-30}
}
EOF
    echo ">> metabase_config.json generated successfully."
fi

# Ensure required directories exist at runtime
mkdir -p /app/data /app/output

echo ">> Starting Scaler Program Evaluator..."
exec python run_app.py
