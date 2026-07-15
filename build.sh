#!/usr/bin/env bash
# Optional local helper. On Vercel, migrate runs via pyproject.toml [tool.vercel.scripts].
# collectstatic is run automatically by Vercel when STATIC_ROOT is set.
set -euo pipefail

python manage.py migrate --noinput
echo "✓ Migrations complete."
