import os


from .base import *  # noqa: F401, F403


DEBUG = False

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
)

ALLOWED_HOSTS = ["*"]

# White noise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']  # noqa: F405

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'oc-lettings-site.sqlite3'),  # noqa: F405
    }
}