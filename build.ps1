# Optional local helper (Windows).
# On Vercel, migrate runs via pyproject.toml [tool.vercel.scripts].

python manage.py migrate --noinput
Write-Host "Migrations complete."
