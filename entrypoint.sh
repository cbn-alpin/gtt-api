#!/bin/sh

if [ "$FLASK_ENV" = "production" ]; then
    echo "Running database migrations for production..."
    flask db upgrade
fi

exec "$@"
