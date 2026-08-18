#!/bin/sh
set -e

mkdir -p /app/media/profiles /app/media/projects
chmod -R 755 /app/media

python manage.py migrate --noinput
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
