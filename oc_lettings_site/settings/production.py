import os

import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *  # noqa: F401, F403


DEBUG = False

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
)

ALLOWED_HOSTS = ["*"]

# White noise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']  # noqa: F405

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES = {
    'default': db_from_env
}


sentry_sdk.init(
    dsn=os.getenv('SENTRY_LINK'),
    integrations=[DjangoIntegration()],
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)
