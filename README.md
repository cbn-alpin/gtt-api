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

The database is installed by default when Flask is launch if it doesn't exist. The same applies to the migrations.
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

## Running Flask

Launch the Flask framework in development mode:

```bash
FLASK_APP=src/main.py flask run
# If you had change the .env location used:
# CONFIG_PATH=/new/location/.env FLASK_APP=src/main.py flask run
```
**Note**: For production, we will use Gunicorn and Nginx within a Docker container.

## Running Tests

```bash
PYTHONPATH=$PYTHONPATH:. FLASK_ENV=test pytest tests/test.py
```

## Generate a Database Revision with Alembic

```bash
alembic revision --autogenerate -m "My revision message"
```