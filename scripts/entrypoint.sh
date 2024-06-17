#!/bin/sh

# exiting the secript if any error occured
set -e 
#collecting statics
python manage.py collectstatic --noinput 
#setting up uWSGI
uwsgi --socket :8000 --master --enable-threads --module config.wsgi