#!/usr/bin/env bash
# Build script for Render and Vercel — runs on every deploy
set -o errexit

if [ -n "${VERCEL:-}" ] || [ -n "${VERCEL_ENV:-}" ]; then
  export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-portfolio.settings.production}"
  PYTHON="${VERCEL_PYTHON_VENV:-.vercel/python/.venv}/bin/python"
  if [ ! -x "$PYTHON" ]; then
    PYTHON="python"
  fi
else
  pip install -r requirements.txt
  PYTHON="python"
fi

"$PYTHON" manage.py collectstatic --no-input

if [ -n "${DATABASE_URL:-}" ]; then
  "$PYTHON" manage.py migrate --no-input
  "$PYTHON" manage.py seed_case_studies
else
  echo "WARNING: DATABASE_URL not set — skipping migrate and seed"
fi
