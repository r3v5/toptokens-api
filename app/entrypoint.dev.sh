#!/bin/sh

# This work is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
# https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input --clear

exec "$@"