"""
WSGI entrypoint for Vercel serverless.

Vercel looks for a module-level `app` in api/index.py.
"""

import os
import sys
from pathlib import Path

# Ensure project root (backend/) is importable when running from api/
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
