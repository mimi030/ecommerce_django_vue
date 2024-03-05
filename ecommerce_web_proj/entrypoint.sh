#!/bin/sh

# Set environment variables from .env.dev file
if [ -f ../.env.dev ]; then
  export $(cat ../.env.dev | xargs)
fi

# Wait for PostgreSQL to be ready
if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for PostgreSQL..."

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi

# Apply database migrations
python manage.py migrate --noinput

# Create superuser (noinput to avoid interactive prompts)
python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL

# Start the Django development server
exec "$@"