import os

import heroku_deploy

heroku_deploy.initalize(
    heroku_api_key=os.getenv('HEROKU_API_KEY'),
    heroku_app_name=os.getenv('HEROKU_APP_NAME')
)

DATABASE_PLAN = 'heroku-postgresql:mini'

CONFIG_VARS = {
    'ENV': 'PRODUCTION',
    'DJANGO_SECRET_KEY': os.getenv('DJANGO_SECRET_KEY'),
    'SENTRY_DSN': os.getenv('SENTRY_DSN')
}

if not heroku_deploy.commands.is_app_exist():
    heroku_deploy.commands.create_app()

if not heroku_deploy.commands.is_addon_exist(DATABASE_PLAN):
    heroku_deploy.commands.create_addon(DATABASE_PLAN)

if not heroku_deploy.commands.check_config_vars(CONFIG_VARS):
    heroku_deploy.commands.patch_config_vars(CONFIG_VARS)

heroku_deploy.commands.push_to_git_heroku()

heroku_deploy.commands.run_command('migrate', 300)
