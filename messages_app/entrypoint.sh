#!/bin/sh

until PGPASSWORD=$DB_PASSWORD psql "${DB_NAME}"  -h "${DB_HOST}" -U "${DB_USER}" -c '\q'; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Postgres is up - executing command"

python manage.py makemigrations --noinput

python manage.py migrate --noinput

python manage.py collectstatic --noinput --skip-checks

exec "$@"