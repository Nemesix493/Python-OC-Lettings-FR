import os


from .base import *  # noqa: F401, F403


DEBUG = False

SECRET_KEY = 'fp$9^593hsriajg$_%=5trot9g!1qa@ew(o-1#@=&4%=hp46(s'

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
