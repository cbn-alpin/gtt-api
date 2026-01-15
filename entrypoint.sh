#!/bin/sh

GTT_USER_UID=${GTT_USER_UID:-1000}
GTT_USER_GID=${GTT_USER_GID:-1000}

if [ "$FLASK_ENV" = "production" ]; then
    echo "Fixing permissions for migrations/data/ content..."
    chown -R $GTT_USER_UID:$GTT_USER_GID /home/app/web/migrations/data/

    echo "Running database migrations for production..."
    flask db upgrade
fi

exec "$@"
