#!/bin/sh
python3 manage.py migrate
python manage.py loaddata dumped_data/data.json --format=json
if [ $ENV == 'DOCKER_DEV' ]; then
    gunicorn --bind 0.0.0.0:8000 oc_lettings_site.wsgi
elif [ $ENV == 'PRODUCTION' ]; then
    gunicorn --bind 0.0.0.0:$PORT oc_lettings_site.wsgi
fi