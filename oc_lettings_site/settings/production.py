import os

import dj_database_url

from .base import *  # noqa: F401, F403


DEBUG = False

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
)

ALLOWED_HOSTS = ["*"]

# White noise configuration
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES = {
    'default': db_from_env
}
