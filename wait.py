import json
import time
import os

import requests

HEROKU_API_KEY = os.getenv('HEROKU_API_KEY')
HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')


for i in range(12):
    time.sleep(10)
    response = requests.get(
        url=f'https://api.heroku.com/apps/{HEROKU_APP_NAME}/dynos',
        headers={
            "Authorization": f"Bearer {HEROKU_API_KEY}",
            "Accept": "application/vnd.heroku+json; version=3"
        }
    )
    if 200 <= response.status_code < 300:
        if json.loads(response.content)[0]['state'] == 'up':
            break
