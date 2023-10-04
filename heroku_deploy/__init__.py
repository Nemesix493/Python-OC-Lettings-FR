from . import commands  # noqa: F401


def initalize(heroku_api_key: str, heroku_app_name: str):
    from . import settings
    settings.HEROKU_API_KEY = heroku_api_key
    settings.HEROKU_APP_NAME = heroku_app_name
