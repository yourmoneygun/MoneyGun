#!/bin/sh

echo "Hello MONEY GUN 'Dev'!"

echo "!!! MIGRATIONS !!!"
python manage.py migrate --noinput --settings=money_gun.settings.${MODE}

echo "!!! COLLECTSTATIC !!!"
python manage.py collectstatic --noinput --settings=money_gun.settings.${MODE}

echo "!!! CREATE SUPER USER !!!"
python manage.py create_super_user

echo "!!! RUN SERVER !!!"
gunicorn -w ${WSGI_WORKERS} -b 0:${WSGI_PORT} money_gun.wsgi:application --log-level=${WSGI_LOG_LEVEL}
