import os

import heroku_deploy


heroku_app_name_git = os.getenv('HEROKU_APP_NAME')
heroku_deploy.initalize(
    heroku_api_key=os.getenv('HEROKU_API_KEY'),
    heroku_app_name=heroku_app_name_git
)

DATABASE_PLAN = 'heroku-postgresql:mini'

CONFIG_VARS = {
    'ENV': 'PRODUCTION',
    'DJANGO_SECRET_KEY': os.getenv('DJANGO_SECRET_KEY'),
    'SENTRY_DSN': os.getenv('SENTRY_DSN')
}

# Full deploy with git

if not heroku_deploy.commands.is_app_exist():
    heroku_deploy.commands.create_app()

if not heroku_deploy.commands.is_addon_exist(DATABASE_PLAN):
    heroku_deploy.commands.create_addon(DATABASE_PLAN)

if not heroku_deploy.commands.check_config_vars(CONFIG_VARS):
    heroku_deploy.commands.patch_config_vars(CONFIG_VARS)

heroku_deploy.commands.push_to_git_heroku()

heroku_deploy.commands.run_command('migrate', 300)


# Full deploy with docker 
# Was deactivate !

# heroku_app_name_docker = heroku_app_name_git + '-2'

# heroku_deploy.initalize(
#    heroku_api_key=os.getenv('HEROKU_API_KEY'),
#    heroku_app_name=heroku_app_name_docker
#)


#if not heroku_deploy.commands.is_app_exist():
#    heroku_deploy.commands.create_app(
#        additional_data={
#            'stack': 'container'
#        }
#    )

#if not heroku_deploy.commands.is_addon_exist(DATABASE_PLAN):
#    heroku_deploy.commands.create_addon(DATABASE_PLAN)

#if not heroku_deploy.commands.check_config_vars(CONFIG_VARS):
#    heroku_deploy.commands.patch_config_vars(CONFIG_VARS)

#heroku_deploy.commands.run_terminal_command(
#    command='heroku login',
#    command_name='Login to heroku'
#)
#heroku_deploy.commands.run_terminal_command(
#    command='heroku container:login',
#    command_name='Login to container registry'
#)
#heroku_deploy.commands.run_terminal_command(
#    command=f'heroku container:push web --app {heroku_app_name_docker}',
#    command_name='Push to container registry'
#)
#heroku_deploy.commands.run_terminal_command(
#    command=f'heroku container:release web --app {heroku_app_name_docker}',
#    command_name='Release to container registry'
#)
