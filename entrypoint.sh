#!/bin/sh

# Run database migrations
flask db upgrade

exec gunicorn --bind 0.0.0.0:5001 src.main:api
