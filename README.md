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

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate the virtual environment:

```bash
source ./.venv/bin/activate
```
## Dependencies

Install Python dependencies defined in *pyproject.toml*:

```bash
# In development
pip install -e .
pip install -e .[dev]
# In production
pip install .
```

**Note**: we don't use *requirements.txt* file in this project.

## Configuration file

Create a *.env* configuration file and **adapt it to your configuration**:

```bash
cp .env.sample .env
```

If you change the location of the *.env* file, you must specify the path to the new location using the `CONFIG_PATH` environment variable.

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

The database content is installed by default when Flask is launch if it doesn't exist. The same applies to the migrations.
Run Flask development server with :

```bash
# If necessary, source the venv:
source ./.venv/bin/activate
# Run the Flask development server:
FLASK_APP=src/main.py flask run
```

You will see:

```
INFO in __init__: No previous migrations found. Running all migrations...
INFO in __init__: Database is up to date
```

If a manual update is required, use the following command:

```bash
alembic upgrade head
# If you had change the .env location used:
# CONFIG_PATH=/new/location/.env alembic upgrade head
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
# If necessary, source the venv:
source ./.venv/bin/activate
# Run the Flask development server:
FLASK_APP=src/main.py flask run
# If you had change the .env location used:
# CONFIG_PATH=/new/location/.env FLASK_APP=src/main.py flask run
```
**Note**: For production, we will use Gunicorn and Nginx within a Docker container.

## Running Tests

```bash
# If necessary, source the venv:
source ./.venv/bin/activate
# Run the tests:
FLASK_ENV=test pytest tests/test.py
```

## Generate a Database Revision with Alembic

To generate a new Alembic revision with the message `<my-revision-message>` :

```bash
# If necessary, source the venv:
source ./.venv/bin/activate
# Create new Alembic revision:
alembic revision --autogenerate -m "<my-revision-message>"
```

## Docker

To build an image localy with Flask development server use: `docker build -t gtt-api:develop --target development .`

Then, you can run the this image like this: `docker run -it --rm -p 5001:5001 --env CONFIG_PATH=/home/app/web/.env --volume .env:/home/app/web/.env gtt-api:develop`
