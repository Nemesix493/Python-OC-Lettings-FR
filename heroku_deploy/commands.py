import requests
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
def create_app(additional_data: dict = {}) -> requests.models.Response:
    return HerokuAPICall.app_post(
        token=settings.HEROKU_API_KEY,
        data={
            'name': settings.HEROKU_APP_NAME,
            'region': 'eu',
            **additional_data
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
    log_lines = session_logs.content.decode('utf-8').split('\n')
    is_match = (
        'Process exited with status' in
        [
            line[-28:-2]
            for line in log_lines
        ]
    )
    if is_match:
        exit_code = None
        for line in log_lines:
            if line[-28:-2] == 'Process exited with status':
                exit_code = line[-1]
        if exit_code == '0':
            return 0
        else:
            raise Exception(
                f'Command ({command}) failed: exited with code {exit_code}\n'
                f'Here is the logs : \n {str(session_logs.content)}'
            )
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


def run_terminal_command(command: str, command_name: str, display_output: bool = True, return_output: bool = False):  # noqa: E501
    try:
        output = subprocess.check_output(command, shell=True, universal_newlines=True)
        if display_output:
            print(f"{command_name} output:")
            print(output)
            if return_output:
                return output
    except subprocess.CalledProcessError as e:
        raise Exception(f"{command_name} failed with return code:", e.returncode)


@need_initialization
def push_to_git_heroku():
    command = f'git push https://heroku:{settings.HEROKU_API_KEY}'\
        f'@git.heroku.com/{settings.HEROKU_APP_NAME}.git master'
    run_terminal_command(
        command=command,
        command_name='Git Push Heroku',
        display_output=False
    )


@need_initialization
def push_to_docker_heroku(circle_sha1: str, dockerhub_username: str, dockerhub_password: str):
    # login to docker hub
    login_docker_hub = f'docker login -u {dockerhub_username} -p {dockerhub_password}'
    run_terminal_command(
        command=login_docker_hub,
        command_name='Login to Docker hub'
    )
    pull_image = f'docker pull {dockerhub_username}/oc-lettings-site:{circle_sha1}'
    run_terminal_command(
        command=pull_image,
        command_name='Pull image from Docker hub'
    )

    build_docker_image = f'docker build -t oc-lettings-site:{circle_sha1} .'
    run_terminal_command(
        command=build_docker_image,
        command_name='Build docker image',
        display_output=False
    )
    # login to heroku docker
    loding_heroku_docker = f'docker login --username={settings.HEROKU_APP_NAME} '\
        f'--password={settings.HEROKU_API_KEY} registry.heroku.com'
    run_terminal_command(
        command=loding_heroku_docker,
        command_name='Login to Docker Heroku'
    )
    # tag the image to heroku docker registry
    tag_image_heroku_docker = f'docker tag oc-lettings-site:{circle_sha1}'\
        f'registry.heroku.com/{settings.HEROKU_APP_NAME}/web'
    run_terminal_command(
        command=tag_image_heroku_docker,
        command_name='Tag Image to Heroku Docker registry'
    )
    # push the image to heroku docker registry
    push_image_heroku_docker = f'docker push registry.heroku.com/{settings.HEROKU_APP_NAME}/web'
    run_terminal_command(
        command=push_image_heroku_docker,
        command_name='Push image to Heroku Docker registry'
    )
