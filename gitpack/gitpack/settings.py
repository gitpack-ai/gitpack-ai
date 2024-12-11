"""
Django settings for gitpack project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from rest_framework.authentication import TokenAuthentication
import dj_database_url
import logging

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-gr^&_jd(pp-6%0qyehq_(y=o(p6dxx3d8gh(3sxa%(s-!7z2kc'

# SECURITY WARNING: don't run with debug turned on in production!
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')
if ENVIRONMENT == 'development':
    DEBUG = True
else:
    DEBUG = False


ALLOWED_HOSTS = ['*']
if ENVIRONMENT == 'development':
    FRONTEND_HOST = 'http://localhost:3000'
else:
    FRONTEND_HOST = 'https://app.gitpack.co'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'allauth',
    'allauth.account',
    'dj_rest_auth.registration',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'drf_yasg'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'gitpack.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'gitpack.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://postgres:postgres@localhost:5432/gitpack',
        conn_max_age=600    
    ) if ENVIRONMENT == 'production' else {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gitpack',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'db',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Loggers
# Logging configuration that logs to console if DEBUG is True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'colored': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s%(levelname)-8s%(reset)s %(log_color)s%(message)s',
            'log_colors': {
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
        },
    },
    'handlers': {
        'console': {
            'class': 'colorlog.StreamHandler',
            'formatter': 'colored',
            'level': 'DEBUG',
        },
    },
    'loggers': {
        '': {  # Root logger
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}




# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
# Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

if ENVIRONMENT == 'production':
    # Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
    # and renames the files with unique names for each version to support long-term caching
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
else:
    # For development, use the default static files storage
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ACCOUNT_EMAIL_VERIFICATION = 'none'

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    }
}

CODE_REVIEW_IGNORE_PATTERNS = [
    '.*\.md',
    '.*\.txt',
    '.*\.json',
    '.*\.yml',
    '.*\.yaml',
    '.*\.ini',
    '.*\.cfg',
    '.*\.conf',
    '.*\.log',
    '.*\.pid',
    '.*\.lock',
    '.*\.tmp',
    '.*\.bak',
    '.*\.old',
    '.*\.save',
    '.*\.backup',
]

GITHUBAPP_ID = os.environ.get('GITHUBAPP_ID')
GITHUBAPP_KEY = os.environ.get('GITHUBAPP_KEY')
if not GITHUBAPP_KEY:
    GITHUBAPP_KEY_PATH = 'gitpack-github-app-key.pem'
    GITHUBAPP_KEY = ''
    with open(GITHUBAPP_KEY_PATH, 'rb') as key_file:
        GITHUBAPP_KEY = key_file.read().decode('utf-8')
GITHUB_WEBHOOK_SECRET = os.environ.get('GITHUB_WEBHOOK_SECRET')

# AI Provider Configuration
AI_PROVIDER = os.environ.get('GITPACK_AI_PROVIDER', 'openai')  # 'openai' or 'claude'

# OpenAI Configuration
OPENAI_ORGANIZATION = os.environ.get('GITPACK_OPENAI_ORGANIZATION')
OPENAI_PROJECT = os.environ.get('GITPACK_OPENAI_PROJECT')
OPENAI_API_KEY = os.environ.get('GITPACK_OPENAI_API_KEY')

# Claude Configuration
ANTHROPIC_API_KEY = os.environ.get('GITPACK_ANTHROPIC_API_KEY')

GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')
GITHUB_CALLBACK_URL = f'{FRONTEND_HOST}/auth/github/callback'

SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'APP': {
            'client_id': GITHUB_CLIENT_ID,
            'secret': GITHUB_CLIENT_SECRET,
            'key': ''
        },
    }
}
SOCIALACCOUNT_STORE_TOKENS = True
SOCIALACCOUNT_ONLY = True

# Add these settings at the end of the file
CORS_ALLOW_ALL_ORIGINS = True  # For development only, not recommended for production
CORS_ALLOW_CREDENTIALS = True

# For more specific control, you can use:
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://gitpack.co",
    "https://app.gitpack.co",
]

# Add this REST_FRAMEWORK configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        # You can include other authentication classes here if needed
    ],
    # You can add other REST_FRAMEWORK settings here as well
}
