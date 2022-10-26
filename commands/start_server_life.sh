#!/bin/sh

echo "Hello MONEY GUN 'Life'!"

echo "!!! MIGRATIONS !!!"
python manage.py migrate --noinput

echo "!!! COLLECTSTATIC !!!"
python manage.py collectstatic --noinput

echo "!!! CREATE SUPER USER !!!"
python manage.py create_super_user

echo "!!! RUN SERVER !!!"
gunicorn -w ${WSGI_WORKERS} -b 0:${WSGI_PORT} money_gun.wsgi:application --log-level=${WSGI_LOG_LEVEL}
