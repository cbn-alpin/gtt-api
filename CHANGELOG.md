# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2026-09-29

### Added

- Add logger management and force Alembic logs to INFO level.
- Add daily hours limit per project.
- Add naming convention for constraints.
- Add new db sub-commands `status` and `autoupgrade`, along with their documentation.
- Add [database documentation](docs/db.md) and a database revisions management in [README](README.md).

### Changed

- Improve README.
- Improve settings for Ruff.
- Exclude certain files from display and search in VSCode.
- Merge old Alembic revisions.
- Add this Changelog file.
- Add support for `SQLALCHEMY_ECHO`.
- Delete the previous timesheet entry if the hours entered by the user are equal to 0.
- Update the Python base image version for the Dockerfile.

### Fixed

- Correctly handle `id_project` during bulk import.
- Increase user email field size.
- Fixing several Alembic migration errors during downgrades.
- Managing hours outside of actions selected by the user in timesheet.
- Improve exception handling when deleting an action or project to preven disconnecting the web application.
- Correctly calculate annual total for each action.

## [1.1.4] - 2026-02-02

### Fixed

- Force end date to project.

## [1.1.3] - 2026-02-02

### Fixed

- Handle empty project end date.
- Set project default end date.

## [1.1.2] - 2026-01-23

### Added

- Add default projects, actions and users migrations.

### Fixed

- Use bigger varchar for project & action names.

## [1.1.1] - 2026-01-22

### Fixed

- Use latest with prod deployment.

## [1.1.0] - 2026-01-22

### Added

- Add default user(s).
- Add VSCode configuration and extensions file.
- Handle all Flask required variables in `.env` and cast environment variables for config.
- Build production image during tag pushing action.

### Changed

- Improve Dockerfile, add Docker Compose file.
- Improve the default config loading.
- Move all source code in `src/gtt/`.
- Refactor database management and move `create_api` to main file.
- Use pattern Application Factory to use with tests.
- Replace Black, Pylint, iSort by Ruff and uv.
- Use `pyproject.toml` instead of `requirements.txt` and `alembic.ini`.
- Improve Docker images builds (use psycopg binary, handle project version from Git tag).
- Update README with uv usage, Docker section, and English translation.

### Fixed

- Restore use of Flask-Migrate.
- Finalize the authorization of date ranges over several years for project action display.
- Send error 404 if user not found.
- Improve project dependencies syntax.
- Copy `src` to production image for Alembic.

### Removed

- Remove database session closures to let Flask-SQLAlchemy handle them.
- Remove deprecated `FLASK_ENV`, auto db upgrade from API, and useless files/directories.

## [1.0.0] - 2025-12-15

### Added

- Initial project structure and API endpoints (User, Project, Action, Travel, Expense). [@floreal15, @1atural, @l3miage-freundgm, @jpm-cbna, @ch-cbna]
- PostgreSQL database integration with SQLAlchemy and Alembic migrations. [@floreal15, @1atural, @l3miage-freundgm, @jpm-cbna, @ch-cbna]
- User action time tracking with durations and multi-year support. [@floreal15, @1atural, @l3miage-freundgm, @jpm-cbna, @ch-cbna]
- Projects and Actions management (create, update, delete, archive). [@floreal15, @1atural, @l3miage-freundgm, @jpm-cbna, @ch-cbna]
- Travel and Expense management (create, update, delete). [@floreal15, @1atural, @l3miage-freundgm, @jpm-cbna, @ch-cbna]
- Authentication system (local authentication and Google OAuth2 tap auth). [@floreal15, @1atural, @l3miage-freundgm, @jpm-cbna, @ch-cbna]
- Docker support for development and production environments. [@floreal15, @1atural, @l3miage-freundgm, @jpm-cbna, @ch-cbna]
- Automatic database initialization and migrations on startup. [@floreal15, @1atural, @l3miage-freundgm, @jpm-cbna, @ch-cbna]
- CORS support and backend security checks. [@floreal15, @1atural, @l3miage-freundgm, @jpm-cbna, @ch-cbna]
- CI/CD setup with GitHub Actions for testing and building images. [@floreal15, @1atural, @l3miage-freundgm, @jpm-cbna, @ch-cbna]
- Unit tests for various endpoints and services. [@floreal15, @1atural, @l3miage-freundgm, @jpm-cbna, @ch-cbna]
