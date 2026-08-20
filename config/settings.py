import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-0fibzm3mqp630f-ef=gd_8h*c8*^5=3j6@8u65bvl+yl$xbbz$",
)
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if host.strip()
]

USE_R2_STORAGE = os.getenv("USE_R2_STORAGE", "").lower() in ("true", "1", "yes")
CLOUDINARY_URL = os.getenv("CLOUDINARY_URL", "").strip()
USE_CLOUDINARY = bool(CLOUDINARY_URL) and not USE_R2_STORAGE
USE_REMOTE_MEDIA = USE_R2_STORAGE or USE_CLOUDINARY

INSTALLED_APPS = [
    "core",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "storages",
]

if USE_CLOUDINARY:
    INSTALLED_APPS += ["cloudinary_storage", "cloudinary"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ── Database ──────────────────────────────────────────────────────────
# Local: SQLite (default). Production: Postgres or MySQL via DATABASE_URL.
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
if DATABASE_URL:
    from urllib.parse import urlparse

    import dj_database_url

    scheme = urlparse(DATABASE_URL).scheme.lower().split("+")[0]
    is_mysql = scheme in ("mysql", "mysql2")

    if is_mysql:
        import pymysql

        pymysql.install_as_MySQLdb()

    ssl_env = os.getenv("DB_SSL_REQUIRE", "").strip().lower()
    ssl_require = ssl_env in ("true", "1", "yes") if ssl_env else False

    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=ssl_require,
        )
    }

    if is_mysql:
        DATABASES["default"].setdefault("OPTIONS", {})
        DATABASES["default"]["OPTIONS"].setdefault("charset", "utf8mb4")
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_USER_MODEL = "core.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ── Static & Media ───────────────────────────────────────────────────
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []

MEDIA_ROOT = BASE_DIR / "media"
# Serve uploads via /api/media/ so Coolify/proxy routes them like other API paths
MEDIA_URL = "/api/media/" if not USE_REMOTE_MEDIA else "/media/"

DATA_UPLOAD_MAX_MEMORY_SIZE = 52_428_800  # 50 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 52_428_800  # 50 MB

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

if USE_R2_STORAGE:
    from django.core.exceptions import ImproperlyConfigured
    from urllib.parse import urlparse

    _r2_required = {
        "R2_ACCESS_KEY_ID": os.getenv("R2_ACCESS_KEY_ID", "").strip(),
        "R2_SECRET_ACCESS_KEY": os.getenv("R2_SECRET_ACCESS_KEY", "").strip(),
        "R2_BUCKET_NAME": os.getenv("R2_BUCKET_NAME", "").strip(),
        "R2_ENDPOINT_URL": os.getenv("R2_ENDPOINT_URL", "").strip(),
        "R2_PUBLIC_URL": os.getenv("R2_PUBLIC_URL", "").strip(),
    }
    _r2_missing = [name for name, value in _r2_required.items() if not value]
    if _r2_missing:
        raise ImproperlyConfigured(
            "USE_R2_STORAGE is enabled but these env vars are missing: "
            + ", ".join(_r2_missing)
        )

    AWS_ACCESS_KEY_ID = _r2_required["R2_ACCESS_KEY_ID"]
    AWS_SECRET_ACCESS_KEY = _r2_required["R2_SECRET_ACCESS_KEY"]
    AWS_STORAGE_BUCKET_NAME = _r2_required["R2_BUCKET_NAME"]
    AWS_S3_ENDPOINT_URL = _r2_required["R2_ENDPOINT_URL"].rstrip("/")
    AWS_S3_REGION_NAME = os.getenv("R2_REGION", "auto")
    AWS_S3_SIGNATURE_VERSION = "s3v4"
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_FILE_OVERWRITE = False
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=86400",
    }

    _public_url = _r2_required["R2_PUBLIC_URL"].rstrip("/")
    if not _public_url.startswith(("http://", "https://")):
        _public_url = f"https://{_public_url}"
    MEDIA_URL = f"{_public_url}/"
    AWS_S3_CUSTOM_DOMAIN = urlparse(_public_url).netloc

    STORAGES["default"] = {
        "BACKEND": "storages.backends.s3.S3Storage",
    }
elif USE_CLOUDINARY:
    STORAGES["default"] = {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    }
else:
    STORAGES["default"] = {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    }

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ── CORS / CSRF / Frontend ──────────────────────────────────────────
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000",
    ).split(",")
    if origin.strip()
]
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = list(
    dict.fromkeys(
        [
            *CORS_ALLOWED_ORIGINS,
            FRONTEND_URL,
            "http://localhost:8000",
            "http://127.0.0.1:8000",
        ]
    )
)

# Behind reverse proxy (Coolify / Traefik)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# ── REST / JWT ───────────────────────────────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=12),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
}

LOGIN_URL = f"{FRONTEND_URL}/login"
LOGIN_REDIRECT_URL = f"{FRONTEND_URL}/admin"
