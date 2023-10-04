import os
import json
import time
import re

import requests


HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')
HEROKU_API_KEY = os.getenv('HEROKU_API_KEY')


def get_start_command_content(command: str, max_time: int = 900) -> dict:
    start_command_response = requests.post(
        url=f'https://api.heroku.com/apps/{HEROKU_APP_NAME}/dynos',
        headers={
            "Authorization": f'Bearer {HEROKU_API_KEY}',
            "Accept": "application/vnd.heroku+json; version=3",
            "Content-Type": "application/json"
        },
        data=json.dumps({
            "command": command,
            "time_to_live": max_time
        })
    )
    if not(200 <= start_command_response.status_code < 300):
        raise Exception(
            f'start command failed : status_code = {start_command_response.status_code}'
        )
    return start_command_response.json()


def init_log_session(dyno_name: str) -> dict:
    init_log_session_response = requests.post(
        url=f'https://api.heroku.com/apps/{HEROKU_APP_NAME}/log-sessions',
        headers={
            "Authorization": f'Bearer {HEROKU_API_KEY}',
            "Accept": "application/vnd.heroku+json; version=3",
            "Content-Type": "application/json"
        },
        data=json.dumps({
            "dyno": dyno_name,
            "lines": 10
        })
    )
    if not(200 <= init_log_session_response.status_code < 300):
        raise Exception(
            f'init log session failed : status_code = {init_log_session_response.status_code}'
        )
    return init_log_session_response.json()


def get_exit_code(logplex_url: str, command: str) -> int | None:
    log_session_logs = requests.get(url=logplex_url)
    is_match = len(re.findall(
        pattern='Process exited with status',
        string=str(log_session_logs.content)
    )) >= 1
    if is_match:
        exit_code = re.findall(
            pattern='Process exited with status {1}([0-9])',
            string=str(log_session_logs.content)
        )[0]
        if exit_code == '0':
            return 0
        else:
            raise Exception(f'Command ({command}) failed: exited with code {exit_code}')
    else:
        return None


def run_command_with_exit_code(command: str, max_time: int = 900) -> int:
    start_command_content = get_start_command_content(command, max_time)
    log_session = init_log_session(dyno_name=start_command_content['name'])
    for i in range(20):
        time.sleep(max_time / 20)
        exit_code = get_exit_code(
            logplex_url=log_session['logplex_url'],
            command=command
        )
        if exit_code is not None:
            exit(0)
    raise Exception(f'Command ({command}) did not finish in time : {max_time}s')
