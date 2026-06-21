#!/usr/bin/env bash
set -o errexit

python manage.py collectstatic --no-input
python manage.py migrate --no-input
python manage.py seed_case_studies

exec gunicorn portfolio.wsgi:application \
  --bind "0.0.0.0:${PORT:-8000}" \
  --timeout "${GUNICORN_TIMEOUT:-60}" \
  --graceful-timeout 30
