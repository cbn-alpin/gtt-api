# gtt-api

Backend for the *Gestion du Temps de Travail* (GTT) Tool.

## Installation and Usage

⚠️ Warning: This project only works with Python v3.x.

To install this project:

Clone the project into your local workspace:

```bash
    git clone https://github.com/cbn-alpin/gtt-api.git
```

Navigate to the cloned project folder:

```bash
cd gtt-api/
```

## Dependencies

Install Python dependencies defined in *pyproject.toml*:

Install _uv_. See: https://docs.astral.sh/uv/getting-started/installation/

Synchronise the app (install the `.venv` and dependencies):
```bash
# Install applications dependencies
uv sync
# Install development dependencies
uv sync --extra dev
```

**Note**: we don't use *requirements.txt* file in this project.

Then, run command inside the `.venv` with:

```bash
uv run <command>
```

## Configuration file

Create a *.env* configuration file and **adapt it to your configuration**:

```bash
cp .env.sample .env
```

If you change the location of the *.env* file, you must specify the path to the new location using the `GTT_CONFIG_PATH` environment variable.

## Database

We use Postgresql and you need to add a new user and crate a new database.
Connect to Psql terminal with a superadmin user:

```bash
sudo -u postgres psql
```

In Psql terminal, create a new user (`<user-name>`) with password (`<user-password>`) and a new database (`<new-database-name>`):
```sql
CREATE USER <user-name> WITH ENCRYPTED PASSWORD '<user-password>';
CREATE DATABASE <new-database-name> WITH TEMPLATE template0 OWNER <user-name>;
GRANT ALL PRIVILEGES ON DATABASE <new-database-name> TO <user-name> ;
```

The database content is installed by default when the Docker container is launch
in production if it doesn't exist. The same applies to the migrations.

In development, use the command: `flask db upgrade`

Run Flask development server with :

```bash
uv run flask run
```

You will see:

```
INFO in __init__: No previous migrations found. Running all migrations...
INFO in __init__: Database is up to date
```

If a manual update is required, use the following command:

```bash
uv run alembic upgrade head
# If you had change the .env location used:
# GTT_CONFIG_PATH=/new/location/.env alembic upgrade head
```

**Note**: we used *pyproject.toml* instead of *alembic.ini*. See [Using pyproject.toml for configuration](https://alembic.sqlalchemy.org/en/latest/tutorial.html#using-pyproject-toml-for-configuration). So, the project has no *alembic.ini* file.

Alembic was originaly initialize with this command :

```bash
alembic init --template pyproject migrations
```

With the database created, you must add at least one admin user:

```sql
-- Switch to the new database:
\c <new-database-name>

INSERT INTO "user" (last_name, first_name, email, is_admin, "password")
SELECT
  '<LASTNAME>',
  '<Firstname>',
  '<me@example.com>',
  TRUE,
  md5('<password>') ;
```

Then, you can link the users with the default global project (`id=0`) with :
```sql
INSERT INTO user_action (id_user, id_action)
  SELECT
    u.id_user,
    a.id_action
  FROM public."user" AS u
    CROSS JOIN public."action" AS a
  WHERE a.id_project = 0
    AND NOT EXISTS (
      SELECT 1
      FROM public."user_action" ua
      WHERE ua.id_user = u.id_user
        AND ua.id_action = a.id_action
    );
```

## Running Flask

Launch the Flask framework in development mode:

```bash
uv run flask run
```
**Note**: For production, we will use Gunicorn and Nginx within a Docker container.

## Running Tests

```bash
ur runn pytest
```

## Generate a Database Revision with Alembic

To generate a new Alembic revision with the message `<my-revision-message>` :

```bash
# Create new Alembic revision:
uv run alembic revision --autogenerate -m "<my-revision-message>"
```

## Docker

This project is configured to be used with Docker and Docker Compose.

### Development Environment with Docker

#### Docker only

You can build the image :

```bash
docker build -t gtt-api:develop --target development .
```

Then, from the root directory of the project, you can run the application with:

```bash
docker run --rm -it -e GTT_DATABASE_IP="host.docker.internal" -e GTT_APP_PORT=5000 --volume .:/home/app/web/ gtt-api:develop
```

You can override the config file `.env` paremeters used by the Flask application with env variables using the same name prefixed by `GTT_`. Ex.: `GTT_DATABASE_IP`.

Also, you can use:
- `GTT_API_HOST_PORT`: to change the port of the API on the host machine.
- `GTT_CONFIG_PATH`: to change the path of the `.env` file.
- `GTT_APP_PORT`: to change the default port `5001` of the API.

#### Docker Compose
To easily launch the application in a development environment, use Docker Compose. This will build the `development` image and run it with your local source code mounted for hot-reloading.

1.  Make sure you have a `.env` file (you can copy `.env.sample`).
2.  Run the following command:

```bash
# Build and start the container in the background
docker-compose up --build -d
```

The API will be available on your local machine at the port specified by `GTT_API_HOST_PORT` in your `docker-compose.yml` (default: `http://localhost:5001`). Use the `.env` file to change the port.

To view the logs: `docker-compose logs -f`
To stop the container: `docker-compose down`

### Production Environment

To build the production-ready image:

```bash
docker build -t gtt-api:latest --target production .
```
