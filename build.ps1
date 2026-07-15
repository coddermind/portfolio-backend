# Optional helper for Windows PowerShell builds (local check).
# On Vercel, set Build Command to: bash build.sh

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
