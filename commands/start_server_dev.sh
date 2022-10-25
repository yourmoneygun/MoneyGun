#!/bin/bash

echo "Hello MONEY GUN 'Dev'!"

echo "!!! MIGRATIONS !!!"
python manage.py migrate --noinput --settings=money_gun.settings.${MODE}

echo "!!! COLLECTSTATIC !!!"
python manage.py collectstatic --noinput --settings=money_gun.settings.${MODE}

echo "!!! CREATE SUPER USER !!!"
python manage.py create_super_user

echo "!!! RUN SERVER !!!"
python manage.py runserver --settings=money_gun.settings.${MODE} 0:${WSGI_PORT}
