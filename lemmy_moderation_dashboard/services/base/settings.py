import os
from shutil import which

import environ

env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)

SECRET_KEY = env.str("LEMMY_ADMIN_SECRET_KEY")

DEBUG = env.bool("LEMMY_ADMIN_DEBUG", default=False)
TEST_MODE = "LEMMY_ADMIN_TEST" in os.environ

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    it for it in env.str("LEMMY_ADMIN_CSRF_TRUSTED_ORIGINS", default="").split(",") if it
]

LEMMY_APPLICATION = {
    "0.18.5": "lemmy_moderation_dashboard.apps.lemmy_0.18",
}[env.str("LEMMY_ADMIN_VERSION", default="0.18.5")]

# Application definition
DJANGO_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
)

THIRD_PARTY_APPS = (
    "django_celery_beat",
    "django_celery_results",
    "django_extensions",
    "compressor",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.reddit",
)

INTERNAL_APPS = (
    LEMMY_APPLICATION,
    "lemmy_moderation_dashboard.apps.core",
)

INSTALLED_APPS = INTERNAL_APPS + THIRD_PARTY_APPS + DJANGO_APPS
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

# This ensures that requests are seen as secure when the proxy sets the header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CORS_ALLOW_ALL_ORIGINS = True
ROOT_URLCONF = env.str(
    "LEMMY_ADMIN_ROOT_URLCONF", default="lemmy_moderation_dashboard.services.admin.urls"
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "lemmy_moderation_dashboard.services.base.wsgi.application"

# Cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env.str("LEMMY_ADMIN_CACHE_LOCATION", default="redis://redis:6379/1"),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

# Celery

CELERY_BROKER_URL = env.str("LEMMY_ADMIN_BROKER_URL", default="redis://redis:6379/0")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env.str("LEMMY_ADMIN_DATABASE_NAME", default="lemmy_moderation_dashboard"),
        "USER": env.str("LEMMY_ADMIN_DATABASE_USER", default="lemmy_moderation_dashboard"),
        "PASSWORD": env.str("LEMMY_ADMIN_DATABASE_PASSWORD"),
        "HOST": env.str("LEMMY_ADMIN_DATABASE_HOST", default="db"),
        "PORT": env.str("LEMMY_ADMIN_DATABASE_PORT", default=5432),
    },
    "lemmy": {
        "ENGINE": env.str(
            "LEMMY_DATABASE_ENGINE", default="django.db.backends.postgresql_psycopg2"
        ),
        "NAME": env.str("LEMMY_DATABASE_NAME", default="lemmy"),
        "USER": env.str("LEMMY_DATABASE_USER", default="lemmy"),
        "PASSWORD": env.str("LEMMY_DATABASE_PASSWORD", default=None),
        "HOST": env.str("LEMMY_DATABASE_HOST", default="lemmy-db"),
        "PORT": env.str("LEMMY_DATABASE_PORT", default=5432),
    },
}
DATABASE_ROUTERS = ("lemmy_moderation_dashboard.services.base.database_router.InternalRouter",)

# Authentication and Account Management
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Email
DEFAULT_FROM_EMAIL = env.str(
    "LEMMY_ADMIN_EMAIL_MAILER_ADDRESS", default="mailer@lemmy_moderation_dashboard"
)
EMAIL_BACKEND = env.str(
    "LEMMY_ADMIN_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = env.str("LEMMY_ADMIN_EMAIL_HOST", default=None)
EMAIL_PORT = env.str("LEMMY_ADMIN_EMAIL_PORT", default=None)
EMAIL_HOST_USER = env.str("LEMMY_ADMIN_EMAIL_SMTP_USERNAME", default=None)
EMAIL_HOST_PASSWORD = env.str("LEMMY_ADMIN_EMAIL_SMTP_PASSWORD", default=None)
EMAIL_TIMEOUT = env.str("LEMMY_ADMIN_EMAIL_TIMEOUT", 5)


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_PRESERVE_USERNAME_CASING = False

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)


MEDIA_ROOT = os.getenv("LEMMY_ADMIN_MEDIA_ROOT", os.path.abspath(os.path.join(BASE_DIR, "media")))
MEDIA_URL = os.getenv("LEMMY_ADMIN_MEDIA_URL", "/media/")


# Logging Configuration
LOG_LEVEL = os.getenv("LEMMY_ADMIN_LOG_LEVEL", "DEBUG" if DEBUG else "INFO")
LOGGING_HANDLERS = {
    "null": {"level": "DEBUG", "class": "logging.NullHandler"},
    "console": {"level": LOG_LEVEL, "class": "logging.StreamHandler", "formatter": "verbose"},
}

LOGGING_HANDLER_METHODS = ["console"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": "LEMMY_ADMIN_LOG_DISABLE_EXISTING_LOGGERS" in os.environ,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s %(levelname)s:%(pathname)s %(process)d %(lineno)d %(message)s"
        },
        "simple": {"format": "%(levelname)s:%(module)s %(lineno)d %(message)s"},
    },
    "handlers": LOGGING_HANDLERS,
    "loggers": {
        "django": {"handlers": ["null"], "propagate": True, "level": "INFO"},
    },
}


# Set up loggers for our own apps
for app in INTERNAL_APPS:
    LOGGING["loggers"][app] = {
        "handlers": LOGGING_HANDLER_METHODS,
        "level": LOG_LEVEL,
        "propagate": False,
    }


# Lemmy
LEMMY_INSTANCE_DOMAIN = env.str("LEMMY_ADMIN_LEMMY_MIRROR_INSTANCE", default=None)
