import requests
import re
import time
import subprocess

from .base import HerokuAPICall, need_initialization
from . import settings


@need_initialization
def is_app_exist() -> bool:
    apps = HerokuAPICall.app_list(token=settings.HEROKU_API_KEY).json()
    for app in apps:
        if app['name'] == settings.HEROKU_APP_NAME:
            return True
    return False


@need_initialization
def create_app() -> requests.models.Response:
    return HerokuAPICall.app_post(
        token=settings.HEROKU_API_KEY,
        data={
            'name': settings.HEROKU_APP_NAME,
            'region': 'eu'
        }
    )


@need_initialization
def is_addon_exist(plan_name: str) -> bool:
    addon_list = HerokuAPICall.addon_list_app(
        token=settings.HEROKU_API_KEY,
        app_name=settings.HEROKU_APP_NAME
    ).json()
    for addon in addon_list:
        if addon['plan']['name'] == plan_name:
            return True
    return False


@need_initialization
def create_addon(plan_name: str) -> requests.models.Response:
    return HerokuAPICall.addon_post(
        token=settings.HEROKU_API_KEY,
        app_name=settings.HEROKU_APP_NAME,
        plan_name=plan_name
    )


@need_initialization
def check_config_vars(expected_config_vars: dict) -> bool:
    config_vars = HerokuAPICall.config_vars_list_app(
        token=settings.HEROKU_API_KEY,
        app_name=settings.HEROKU_APP_NAME,
    ).json()
    for key, val in expected_config_vars.items():
        if config_vars.get(key, None) != val:
            return False
    return True


@need_initialization
def patch_config_vars(config_vars):
    return HerokuAPICall.config_vars_patch(
        token=settings.HEROKU_API_KEY,
        app_name=settings.HEROKU_APP_NAME,
        config_vars=config_vars
    )


def get_exit_code(logplex_url: str, command: str) -> int | None:
    session_logs = requests.get(url=logplex_url)
    is_match = len(re.findall(
        pattern='Process exited with status',
        string=str(session_logs.content)
    )) >= 1
    if is_match:
        exit_code = re.findall(
            pattern='Process exited with status {1}([0-9])',
            string=str(session_logs.content)
        )[0]
        if exit_code == '0':
            return 0
        else:
            raise Exception(f'Command ({command}) failed: exited with code {exit_code}')
    else:
        return None


@need_initialization
def run_command(command: str, max_time: int = 900) -> None:
    dyno_name = HerokuAPICall.dyno_post(
        token=settings.HEROKU_API_KEY,
        app_name=settings.HEROKU_APP_NAME,
        command=command,
        max_time=max_time
    ).json()['name']

    logplex_url = HerokuAPICall.log_session_post(
        token=settings.HEROKU_API_KEY,
        app_name=settings.HEROKU_APP_NAME,
        dyno_name=dyno_name
    ).json()['logplex_url']

    for i in range(20):
        time.sleep(max_time / 20)
        exit_code = get_exit_code(
            logplex_url=logplex_url,
            command=command
        )
        if exit_code is not None:
            return None
    raise Exception(f'Command ({command}) did not finish in time : {max_time}s')


@need_initialization
def push_to_git_heroku():
    command = f'git push https://heroku:{settings.HEROKU_API_KEY}'\
        f'@git.heroku.com/{settings.HEROKU_APP_NAME}.git master'
    try:
        output = subprocess.check_output(command, shell=True, universal_newlines=True)
        print("Git push output:")
        print(output)
    except subprocess.CalledProcessError as e:
        raise Exception("Git push failed with return code:", e.returncode)
