import os

import heroku_deploy

heroku_deploy.initalize(
    heroku_api_key=os.getenv('HEROKU_API_KEY'),
    heroku_app_name=os.getenv('HEROKU_APP_NAME')
)

heroku_deploy.commands.run_command(
    'python manage.py loaddata dumped_data/data.json --format=json',
    300
)
