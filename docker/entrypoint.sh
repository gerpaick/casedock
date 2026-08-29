#!/usr/bin/env bash
set -euo pipefail

echo "→ migrate"
python manage.py migrate --noinput

echo "→ collectstatic (WhiteNoise manifest)"
python manage.py collectstatic --noinput --clear

echo "→ exec: $*"
exec "$@"
