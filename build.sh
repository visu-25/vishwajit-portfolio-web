#!/usr/bin/env bash
# Build script for Render and Vercel — runs on every deploy
set -o errexit

if [ -n "${VERCEL:-}" ] || [ -n "${VERCEL_ENV:-}" ]; then
  export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-portfolio.settings.production}"
else
  pip install -r requirements.txt
fi

python manage.py collectstatic --no-input
python manage.py migrate --no-input
python manage.py seed_case_studies
