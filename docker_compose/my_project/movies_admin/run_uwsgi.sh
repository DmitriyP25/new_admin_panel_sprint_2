#!/usr/bin/env bash

while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
done

python manage.py migrate --no-input

python manage.py collectstatic --no-input

set -e

chown root:root /var/log

uwsgi --strict --ini uwsgi.ini
