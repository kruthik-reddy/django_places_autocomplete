import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

print("GOOGLE_KEY:", os.getenv("GOOGLE_MAPS_API_KEY"))

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'replace-with-your-secret'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'addresses',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            'addresses.context_processors.google_maps_api_key',
        ]},
    },
]
WSGI_APPLICATION = 'myproject.wsgi.application'
import environ

env = environ.Env(
    # set casting, default value
    DATABASE_URL=(str, 'sqlite:///db.sqlite3') # Default to SQLite if DATABASE_URL not set
)

# Read .env file, if it exists
environ.Env.read_env()


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'default': env.db(),
    }
}

AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
