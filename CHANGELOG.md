# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Add logger management. [@jpm-cbna]
- Add daily hours limit by project. [@jpm-cbna]
- Add naming convention for constraints. [@jpm-cbna]
- Add new db sub-commands `status` and `autoupgrade`. [@jpm-cbna]

### Changed

- Improve README. [@jpm-cbna]
- Improve settings for Ruff. [@jpm-cbna]
- Exclude certain files from display and search in VSCode. [@jpm-cbna]
- Merge old Alembic revisions. [@jpm-cbna]

### Fixed

- Correctly handle `id_project` during bulk import. [@jpm-cbna]
- Increase user email field size. [@jpm-cbna]
- Fix Alembic downgrades. [@jpm-cbna]

## [1.1.4] - 2026-02-02

### Fixed

- Force end date to project. [@jpm-cbna]

## [1.1.3] - 2026-02-02

### Fixed

- Handle empty project end date. [@jpm-cbna]
- Set project default end date. [@jpm-cbna]

## [1.1.2] - 2026-01-23

### Added

- Add default projects, actions and users migrations. [@jpm-cbna]

### Fixed

- Use bigger varchar for project & action names. [@jpm-cbna]

## [1.1.1] - 2026-01-22

### Fixed

- Use latest with prod deployment. [@jpm-cbna]

## [1.1.0] - 2026-01-22

### Added

- Add default user(s). [@jpm-cbna]
- Add VSCode configuration and extensions file. [@jpm-cbna]
- Handle all Flask required variables in `.env` and cast environment variables for config. [@jpm-cbna]
- Build production image during tag pushing action. [@jpm-cbna]

### Changed

- Improve Dockerfile, add Docker Compose file. [@jpm-cbna]
- Improve the default config loading. [@jpm-cbna]
- Move all source code in `src/gtt/`. [@jpm-cbna]
- Refactor database management and move `create_api` to main file. [@jpm-cbna]
- Use pattern Application Factory to use with tests. [@jpm-cbna]
- Replace Black, Pylint, iSort by Ruff and uv. [@jpm-cbna]
- Use `pyproject.toml` instead of `requirements.txt` and `alembic.ini`. [@jpm-cbna]
- Improve Docker images builds (use psycopg binary, handle project version from Git tag). [@jpm-cbna]
- Update README with uv usage, Docker section, and English translation. [@jpm-cbna]

### Fixed

- Restore use of Flask-Migrate. [@jpm-cbna]
- Finalize the authorization of date ranges over several years for project action display. [@jpm-cbna]
- Send error 404 if user not found. [@jpm-cbna]
- Improve project dependencies syntax. [@jpm-cbna]
- Copy `src` to production image for Alembic. [@jpm-cbna]

### Removed

- Remove database session closures to let Flask-SQLAlchemy handle them. [@jpm-cbna]
- Remove deprecated `FLASK_ENV`, auto db upgrade from API, and useless files/directories. [@jpm-cbna]

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
