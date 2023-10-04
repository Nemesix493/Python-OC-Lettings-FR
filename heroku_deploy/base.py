import enum
import json
from functools import wraps

import requests


class HTTPVerb(enum.Enum):
    POST = enum.auto()
    DELETE = enum.auto()
    GET = enum.auto()
    PATCH = enum.auto()


REQUESTS_FUNCTIONS = {
    HTTPVerb.DELETE: requests.delete,
    HTTPVerb.GET: requests.get,
    HTTPVerb.POST: requests.post,
    HTTPVerb.PATCH: requests.patch
}


def need_initialization(func):
    @wraps(func)
    def wrapped_func(*args, **kwargs):
        from . import settings
        if settings.HEROKU_API_KEY is None or settings.HEROKU_APP_NAME is None:
            raise Exception(
                'You must initialize to set HEROKU_API_KEY and HEROKU_APP_NAME settings !'
            )
        return func(*args, **kwargs)
    return wrapped_func


class HerokuAPICall:
    @staticmethod
    def base_heroku_api_call(url: str, verb: HTTPVerb, token: str, data: list | dict = None) -> requests.models.Response:  # noqa: E501
        response = REQUESTS_FUNCTIONS[verb](
            **{
                "url": url,
                "headers": {
                    "Authorization": f'Bearer {token}',
                    "Accept": "application/vnd.heroku+json; version=3",
                    "Content-Type": "application/json"
                },
                'data': json.dumps(data) if data is not None else None
            }
        )
        if not(200 <= response.status_code < 300):
            raise Exception(
                f'heroku api call failed due this status code : {response.status_code}'
            )
        return response

    @classmethod
    def app_list(cls, token: str) -> requests.models.Response:
        return cls.base_heroku_api_call(
            url='https://api.heroku.com/apps',
            verb=HTTPVerb.GET,
            token=token
        )

    @classmethod
    def app_post(cls, token: str, data: dict) -> requests.models.Response:
        return cls.base_heroku_api_call(
            url='https://api.heroku.com/apps',
            verb=HTTPVerb.POST,
            token=token,
            data=data
        )

    @classmethod
    def addon_list_app(cls, token: str, app_name: str) -> requests.models.Response:
        return cls.base_heroku_api_call(
            url=f'https://api.heroku.com/apps/{app_name}/addons',
            verb=HTTPVerb.GET,
            token=token
        )

    @classmethod
    def addon_post(cls, token: str, app_name: str, plan_name: str) -> requests.models.Response:
        return cls.base_heroku_api_call(
            url=f'https://api.heroku.com/apps/{app_name}/addons',
            verb=HTTPVerb.POST,
            token=token,
            data={
                'plan': plan_name
            }
        )

    @classmethod
    def config_vars_list_app(cls, token: str, app_name: str) -> requests.models.Response:
        return cls.base_heroku_api_call(
            url=f'https://api.heroku.com/apps/{app_name}/config-vars',
            verb=HTTPVerb.GET,
            token=token
        )

    @classmethod
    def config_vars_patch(cls, token: str, app_name: str, config_vars: dict) -> requests.models.Response:  # noqa: E501
        return cls.base_heroku_api_call(
            url=f'https://api.heroku.com/apps/{app_name}/config-vars',
            verb=HTTPVerb.PATCH,
            token=token,
            data=config_vars
        )

    @classmethod
    def dyno_post(cls, token: str, app_name: str, command: str, max_time: int) -> requests.models.Response:  # noqa: E501
        return cls.base_heroku_api_call(
            url=f'https://api.heroku.com/apps/{app_name}/dynos',
            verb=HTTPVerb.POST,
            token=token,
            data={
                'command': command,
                'time_to_live': max_time
            }
        )

    @classmethod
    def log_session_post(cls, token: str, app_name: str, dyno_name: str) -> requests.models.Response:  # noqa: E501
        return cls.base_heroku_api_call(
            url=f'https://api.heroku.com/apps/{app_name}/log-sessions',
            verb=HTTPVerb.POST,
            token=token,
            data={
                "dyno": dyno_name,
                "lines": 10
            }
        )
