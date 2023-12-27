#!/usr/bin/env bash

python manage.py migrate --no-input

python manage.py collectstatic --no-input

set -e

chown root:root /var/log

uwsgi --strict --ini /etc/app/uwsgi.ini
