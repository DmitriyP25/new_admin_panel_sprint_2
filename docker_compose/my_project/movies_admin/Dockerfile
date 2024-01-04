FROM python:3.10-alpine3.16

WORKDIR /movies_database

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240

ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY uwsgi/uwsgi.ini uwsgi.ini
COPY requirements.txt requirements.txt
COPY .env .env

RUN apk add --update netcat-openbsd \
     && apk add --update uwsgi-python3 \
     && apk add python3-dev build-base linux-headers pcre-dev

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt


COPY . .

EXPOSE 8000/tcp

ENTRYPOINT ["sh", "run_uwsgi.sh"]
