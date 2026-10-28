"""
config/settings.py

This is the "control panel" of the whole Django project. Every setting that affects
the entire application lives here: which apps are installed, how to connect to the
database, security settings, REST Framework defaults, etc.

Nothing in this file runs business logic — it only *configures* Django.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load variables from a local .env file (if present) into os.environ.
# This lets us keep secrets/config OUT of the source code, and load different
# values on your laptop vs. in Docker vs. in Kubernetes.
load_dotenv()

# BASE_DIR points to the ford_platform/ folder itself. Used to build absolute file paths.
BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------------------------
# SECURITY / CORE SETTINGS
# --------------------------------------------------------------------------------------

# Secret key Django uses for cryptographic signing (sessions, CSRF tokens, etc).
# In real production this MUST come from a secrets manager, never hardcoded.
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-only-secret-change-me")

# DEBUG=True shows detailed error pages — great for learning, DANGEROUS in production
# (it can leak internal code/paths). Always False in a real deployment.
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

# Which hostnames are allowed to serve this app (protects against Host header attacks).
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# --------------------------------------------------------------------------------------
# APPLICATIONS
# --------------------------------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",         # Built-in admin panel UI (http://.../admin/)
    "django.contrib.auth",          # User accounts, login, permissions
    "django.contrib.contenttypes",  # Framework used internally by admin/auth
    "django.contrib.sessions",      # Session support (used by the admin login)
    "django.contrib.messages",      # One-time flash messages (used by admin)
    "django.contrib.staticfiles",   # Serves CSS/JS for the admin panel

    "rest_framework",               # Django REST Framework — turns Django into a REST API toolkit

    "vehicle_service",              # OUR app: vehicles, dealers, appointments, diagnostics
]

MIDDLEWARE = [
    # Middleware = code that runs on EVERY request/response, in this order, before/after your view.
    "django.middleware.security.SecurityMiddleware",   # Adds security-related HTTP headers
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",        # Cross-Site Request Forgery protection
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # Attaches request.user
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"   # Tells Django where the top-level URL routing table lives

TEMPLATES = [
    {
        # Needed for Django admin's HTML pages to render correctly.
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# --------------------------------------------------------------------------------------
# DATABASE
# --------------------------------------------------------------------------------------
# This project supports two modes, controlled by DB_ENGINE in your .env file:
#   "sqlite"   -> zero setup, single file (db.sqlite3) — DEFAULT, great for learning
#   "postgres" -> matches the production architecture described in the interview guide
#
# Notice that vehicle_service/models.py NEVER changes based on this — that's the whole
# point of Django's ORM: your Python code is database-agnostic.

if os.getenv("DB_ENGINE", "sqlite") == "postgres":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ["DB_NAME"],
            "USER": os.environ["DB_USER"],
            "PASSWORD": os.environ["DB_PASSWORD"],
            "HOST": os.environ["DB_HOST"],
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",   # A single file in the project folder
        }
    }

# --------------------------------------------------------------------------------------
# PASSWORD VALIDATION (for the built-in admin/auth user accounts)
# --------------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --------------------------------------------------------------------------------------
# INTERNATIONALIZATION
# --------------------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --------------------------------------------------------------------------------------
# STATIC FILES (needed so the Django admin panel looks styled)
# --------------------------------------------------------------------------------------
STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --------------------------------------------------------------------------------------
# DJANGO REST FRAMEWORK CONFIG
# --------------------------------------------------------------------------------------
REST_FRAMEWORK = {
    # How DRF figures out WHO is calling the API.
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",  # Login via /admin/, browsable API
        "rest_framework.authentication.BasicAuthentication",    # username/password over HTTPS — simple for local testing
        # In a real enterprise deployment, this list points at an OAuth2/JWT
        # validator that checks tokens issued by an identity provider (e.g. Okta,
        # Azure AD, Auth0) instead of Django managing passwords itself.
    ],
    # By default, every endpoint requires the caller to be authenticated.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    # Basic abuse protection: limits how many requests one user can make.
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {"user": "1000/day"},
    # Pagination keeps large result sets from overwhelming clients/DB.
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

# --------------------------------------------------------------------------------------
# PRODUCTION-STYLE SECURITY HEADERS
# --------------------------------------------------------------------------------------
# These are only enforced when DEBUG=False (i.e., in a real deployment), since they
# require HTTPS, which you don't have on localhost during development.
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
