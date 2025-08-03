# myproject/settings.py
import os
from pathlib import Path


import environ
from dotenv import load_dotenv

# ──────────────────────────────────────────────
# Env & paths
# ──────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# Read .env (for local dev)
load_dotenv(BASE_DIR / ".env")

# django-environ
env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, "insecure-dev-key"),
    DATABASE_URL=(str, f"sqlite:///{BASE_DIR/'db.sqlite3'}"),
    GOOGLE_MAPS_API_KEY=(str, ""),
)
environ.Env.read_env()          # also parse .env if present

DEBUG       = env("DEBUG")
SECRET_KEY  = env("SECRET_KEY")
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

print("GOOGLE_KEY:", env("GOOGLE_MAPS_API_KEY"))

# ──────────────────────────────────────────────
# Django basics
# ──────────────────────────────────────────────
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third-party
    "whitenoise.runserver_nostatic",   # <── before django staticfiles
    # local
    "django_places_autocomplete.addresses",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",   # <── serves compressed static
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "django_places_autocomplete.myproject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "addresses.context_processors.google_maps_api_key",
            ],
        },
    },
]

WSGI_APPLICATION = "django_places_autocomplete.myproject.wsgi.application"

# ──────────────────────────────────────────────
# Database
# ──────────────────────────────────────────────
DATABASES = {
    "default": env.db(),   # picks up DATABASE_URL or falls back to SQLite
}

# ──────────────────────────────────────────────
# Internationalization
# ──────────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE     = "UTC"
USE_I18N      = True
USE_TZ        = True

# ──────────────────────────────────────────────
# Static files
# ──────────────────────────────────────────────

STATIC_URL = "/static/"

# Tell Django “look for static in /app/static, not inside the app folder.”
STATICFILES_DIRS = [
    BASE_DIR.parent / "static",
]

# Collect into /app/staticfiles
STATIC_ROOT = BASE_DIR.parent / "staticfiles"

# tell WhiteNoise to gzip/brotli
STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)

# ──────────────────────────────────────────────
# API keys
# ──────────────────────────────────────────────
GOOGLE_MAPS_API_KEY = env("GOOGLE_MAPS_API_KEY")
