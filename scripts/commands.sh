#!usr/bin/bash

set -e

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    echo "Waiting for postgress Database Start up ($POSTGRES_HOST $POSTGRES_PORT)"
    sleep 1

done

echo "Postgress started successfuly ($POSTGRES_HOST:$POSTGRES_PORT)"

python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000
