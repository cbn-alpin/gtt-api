# +----------------------------------------------------------------------+
# BUILDER

# Pull official base image
FROM python:3.12.6-slim-bullseye AS builder

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive \
        apt-get install -y --quiet --no-install-recommends \
        git \
    && apt-get -y autoremove \
    && apt-get clean autoclean \
    && rm -fr /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install python dependencies
RUN pip install --upgrade pip

# Copy the entire project context, including the .git directory.
COPY . /usr/src/app/

# Build the wheel archive.
# setuptools-scm will be triggered here, using Git to determine the version
# and embedding it into the wheel's metadata.
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels .


# +----------------------------------------------------------------------+
# BASE

# Pull official base image
FROM python:3.12.6-slim-bullseye AS base

# Set default environment variables
ENV HOME="/home/app"
ENV APP_HOME="/home/app/web"
ENV FLASK_APP=src.main:api
ENV APP_PORT=5001

# Create new user "app" with group and home directory
RUN useradd --create-home --shell /bin/bash app

# Uncomment alias from user "app" .bashrc file
RUN sed -i -r 's/^#(alias|export|eval)/\1/' "$HOME/.bashrc"

# Create the web app directory and set it as the working directory
WORKDIR $APP_HOME

# Install additional packages
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive \
        apt-get install -y --quiet --no-install-recommends \
        curl \
    && apt-get -y autoremove \
    && apt-get clean autoclean \
    && rm -fr /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy application and dependencies from the builder stage
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/VERSION.txt .

# Copy files needed at runtime by the application (Alembic migrations, pyproject.toml)
# At runtime Alembic searches for the "migrations" directory in the current working directory
# which is set to APP_HOME (/home/app/web) !
COPY pyproject.toml .
COPY migrations/ migrations/

# Install the application and its dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir /wheels/* \
    #&& rm -rf /wheels \
    && chown -R app:app $APP_HOME

# Change to the "app" user
USER app

EXPOSE $APP_PORT
VOLUME ./config/
VOLUME ./var/log/


# +----------------------------------------------------------------------+
# DEVELOPMENT
FROM base AS development


CMD flask run -h 0.0.0.0 -p $APP_PORT


# +----------------------------------------------------------------------+
# PRODUCTION
FROM base AS production

RUN pip install --no-cache-dir --user gunicorn==21.2.0

ENV PATH="$PATH:${HOME}/.local/bin"

# Copy files needed to run the container
COPY entrypoint.sh .

ENTRYPOINT ["/home/app/web/entrypoint.sh"]

HEALTHCHECK \
    --interval=30s \
    --timeout=30s \
    --start-period=5s \
    --retries=3 \
    CMD curl --fail --silent http://localhost:${APP_PORT}/health || exit 1
