# GTT API - AI Assistant Instructions

Backend for **Gestion du Temps de Travail** (GTT) - a time tracking and expense management application.

## Quick Context

- **Stack**: Flask 3.1 REST API with SQLAlchemy 2.0 ORM
- **Database**: PostgreSQL (configurable via `.env`)
- **Authentication**: JWT tokens via `Flask-JWT-Extended`
- **Python**: 3.10+ required
- **Migrations**: Alembic (auto-run on app startup)

## Setup & Execution

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install
pip install -e .              # production
pip install -e .[dev]         # development

# Configure
cp .env.sample .env          # adapt DATABASE_* and JWT_* values

# Run
flask run                     # dev server on port 5000
# OR
python -m src.main           # direct execution
```

## Project Structure

```
src/
├── main.py              # Flask app factory, blueprint registration, error handlers
├── models.py            # SQLAlchemy models (User, Project, Action, Travel, Expense, etc.)
├── database.py          # DB initialization, Alembic migration runner
├── config.py            # Configuration loading (env vars or TOML file)
├── api/                 # Resource-organized blueprints
│   ├── auth/           # JWT authentication (login, logout, token refresh)
│   │   ├── routes.py
│   │   ├── schema.py
│   │   ├── services.py
│   │   └── utils.py
│   ├── user/           # User CRUD and management
│   ├── project/        # Project CRUD with cascade delete
│   ├── action/         # Action management (linked to projects)
│   ├── travel/         # Travel expense tracking
│   ├── expense/        # Mission expense tracking
│   ├── userAction/     # User-Action relationship management
│   ├── userActionTime/ # Time tracking entries
│   └── exception.py     # Custom exceptions (DBInsertException, NotFoundError)
└── migrations/          # Alembic versioned migrations (auto-generated)
```

## Key Patterns

**API Response Format:**
All endpoints return JSON with consistent structure:
```python
# Success (implicit)
{ "data": {...} }

# Error (via error handlers)
{
  "status": "error",
  "type": "ERROR_TYPE",
  "code": "CODE_KEY",
  "message": "Human readable message"
}
```

**Blueprint Structure (per resource):**
```
api/{resource}/
├── routes.py      # Flask Blueprint with @bp.route() handlers
├── schema.py      # Marshmallow schemas for request/response validation
├── services.py    # Business logic (DB queries, transformations)
└── utils.py       # Helper functions specific to resource
```

**Database Models:**
- SQLAlchemy ORM with cascade deletes for referential integrity
- Column naming convention: `id_{entity}` (e.g., `id_user`, `id_project`)
- Timestamps: Check actual models for Date/DateTime fields
- Relationships: Use `back_populates` and `cascade="all, delete-orphan"`

**Error Handling:**
- Raise `DBInsertException(message, status_code)` for DB-related errors
- Raise `NotFoundError()` for 404 responses
- Custom error handlers in `main.py` return consistent JSON

**JWT Authentication:**
- Tokens issued at `/api/auth/login` endpoint
- Validated via `@jwt_required()` decorator on protected routes
- Token blacklist enabled (see `JWT_BLACKLIST_*` config)

## Configuration

**Loading Priority:**
1. Check `CONFIG_PATH` env var for custom `.env` file path
2. Load from `.env` in project root (if exists)
3. Fall back to environment variables
4. `ConfigLoader` class in `config.py` parses TOML or env

**Required Environment Variables (.env):**
```
DATABASE_IP=localhost
DATABASE_PORT=5432
DATABASE_USER=gtt_user
DATABASE_PASSWORD=secure_password
DATABASE_NAME=gtt_db
FLASK_ENV=development
FLASK_DEBUG=1
JWT_SECRET=your_secret_key
JWT_EXPIRES_IN=3600
```

**Optional Variables:**
- `GS_*`: Google Sheets integration (not yet active)
- `GEFIPROJ_*`: GEFIPROJ service credentials (not yet active)

## Database & Migrations

**Auto-Migration on Startup:**
- `init_db_and_migrations()` runs automatically when Flask app starts
- Alembic checks current DB version vs. latest migration
- Idempotent: safe to restart app multiple times

**Creating New Migrations:**
```bash
cd src  # Important: run from src/ directory
alembic revision --autogenerate -m "description of change"
# Review generated migration in migrations/versions/
# Restart Flask to apply automatically
```

**Alembic Configuration:**
- Config: `pyproject.toml` (loaded by `alembic.config.Config`)
- Script directory: `migrations/`
- Migration templates: `migrations/script.py.mako`

## Testing

```bash
# All tests
pytest

# Specific test file
pytest tests/test_user_routes.py -v

# Watch mode
pytest --tb=short
```

**Test Setup:**
- Fixture in `tests/conftest.py` provides Flask app, DB, and authenticated user
- Database: SQLite in-memory by default (`TEST_DATABASE_URL` env var)
- Optional `.env.test` file for test-specific config
- Fixtures available: `app`, `client`, `auth_token`, etc.

**Test Features:**
- Auto-prints all API routes at test start (see `print_routes_once` fixture)
- Supports Alembic migrations in tests via `USE_ALEMBIC_MIGRATIONS` env var
- Test database cleaned up after each test

## Development Workflows

**1. Adding a New API Endpoint:**
```bash
# 1. Create model in src/models.py (or use existing)
# 2. Create migration (if DB schema change needed)
alembic revision --autogenerate -m "add new table"

# 3. Create API blueprint
touch src/api/myresource/routes.py
touch src/api/myresource/schema.py
touch src/api/myresource/services.py

# 4. Register in src/main.py
from src.api.myresource.routes import resources as myresource_resources
app.register_blueprint(myresource_resources, url_prefix="/api")

# 5. Test
pytest tests/test_myresource.py -v
```

**2. Database Changes:**
```bash
# Update model in src/models.py
# Generate migration
alembic revision --autogenerate -m "change description"
# Restart Flask (auto-applies migration)
```

**3. Debugging:**
- Enable Flask debug mode: `FLASK_DEBUG=1` in `.env`
- Check logs for detailed stack traces
- Inspect JWT tokens via `flask_jwt_extended` utilities
- Print available routes: `pytest` shows all endpoints at startup

**4. CORS:**
- Enabled globally via `CORS(api)` in `main.py`
- Supports requests from any origin (adjust in production)

## Naming Conventions

**Python:**
- Functions/variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`

**Database:**
- Tables: singular, lowercase (e.g., `user`, `project`, `action`)
- Columns: `snake_case` with `id_` prefix for PKs (e.g., `id_user`, `created_at`)
- Foreign keys: `id_{table}` pattern

**API Routes:**
- Plural nouns: `/api/users`, `/api/projects`
- Actions: `/api/users/{id}/actions`
- No verbs in URL (use HTTP methods)

## Dependencies

**Core:**
- Flask 3.1
- SQLAlchemy 2.0 + Flask-SQLAlchemy 3.1
- Alembic 1.17 (migrations)
- psycopg2-binary 2.9 (PostgreSQL driver)

**API & Auth:**
- Flask-JWT-Extended 4.7
- Flask-CORS 6.0
- Marshmallow 3.26 (serialization)

**Config & Utils:**
- python-dotenv 1.2
- requests 2.32
- google-auth 2.45 (for Google Sheets integration - not active)

**Development:**
- pytest 9.0
- pytest-dotenv 0.5
- ruff 0.14 (linting)

## Resources

- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [Alembic Migrations](https://alembic.sqlalchemy.org/)
- [Marshmallow](https://marshmallow.readthedocs.io/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
