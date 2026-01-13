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
ENV GTT_USER="app"
ENV GTT_USER_HOME="/home/${GTT_USER}"
ENV GTT_APP_HOME="${GTT_USER_HOME}/web"
ENV GTT_APP_PORT=5001
ENV FLASK_APP=src.main:api

# Create new user "app" with group and home directory
RUN useradd --create-home --shell /bin/bash app

# Uncomment alias from user "app" .bashrc file
RUN sed -i -r 's/^#(alias|export|eval)/\1/' "$GTT_USER_HOME/.bashrc"

# Create the web app directory and set it as the working directory
WORKDIR $GTT_APP_HOME

# Install additional packages
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive \
        apt-get install -y --quiet --no-install-recommends \
        curl \
    && apt-get -y autoremove \
    && apt-get clean autoclean \
    && rm -fr /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy the entrypoint script and make it executable
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE $GTT_APP_PORT


# +----------------------------------------------------------------------+
# DEVELOPMENT
FROM base AS development

# Copy the application source code
COPY . .

# Install dependencies for development in editable mode
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -e ."[dev]" \
    && chown -R app:app $GTT_APP_HOME

# Run the Flask development server.
# The shell form of CMD is used here so that the shell can expand $APP_PORT
# before passing the command to the entrypoint. The entrypoint's `exec` will then
# ensure the flask process becomes PID 1.
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD flask run --host=0.0.0.0 --port=$GTT_APP_PORT --debug

USER $GTT_USER

# +----------------------------------------------------------------------+
# PRODUCTION
FROM base AS production

# Copy application and dependencies from the builder stage
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/VERSION.txt .

# Copy files needed at runtime by the application (Alembic migrations, pyproject.toml)
# At runtime Alembic searches for the "migrations" directory in the current working directory
# which is set to APP_HOME (/home/app/web) !
COPY pyproject.toml .
COPY migrations/ migrations/

# Install the application and its dependencies from the wheel
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --user gunicorn==21.2.0 \
    && pip install --no-cache-dir /wheels/* \
    && rm -rf /wheels \
    && chown -R app:app $GTT_APP_HOME

ENV PATH="$PATH:${GTT_USER_HOME}/.local/bin"

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
# The shell form is used here for consistency and to allow expansion of APP_PORT.
CMD gunicorn --bind "0.0.0.0:$GTT_APP_PORT" src.main:api

USER $GTT_USER

HEALTHCHECK \
    --interval=30s \
    --timeout=30s \
    --start-period=5s \
    --retries=3 \
    CMD curl --fail --silent http://localhost:${GTT_APP_PORT}/health || exit 1
