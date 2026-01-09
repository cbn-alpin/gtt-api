import hashlib
import os
from unittest.mock import patch

import click
import pytest
from alembic import command
from alembic.config import Config
from flask_jwt_extended import create_access_token

from src.main import create_api, db
from src.models import User

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///:memory:")
USE_ALEMBIC_MIGRATIONS = os.getenv("USE_ALEMBIC_MIGRATIONS", "0").lower() in ("1", "true", "yes")


def pytest_report_header():
    messages = []
    if os.path.exists(".env.test"):
        messages.append("⚙️ .env.test file detected.")
    else:
        messages.append("⚙️ No .env.test file found (using default values).")
    messages.append(f"🛢️ TEST_DATABASE_URL: {TEST_DATABASE_URL}")
    messages.append(f"⚗️ USE_ALEMBIC_MIGRATIONS: {USE_ALEMBIC_MIGRATIONS}")
    return messages


@pytest.fixture(autouse=True, scope="session")
def print_routes_once(app):
    """Autouse session-scoped fixture to print routes once."""
    # This check ensures the routes are printed only one time
    if not hasattr(print_routes_once, "already_run"):
        click.secho("\n🚀 API routes:", fg="cyan", bold=True)
        rules = sorted(app.url_map.iter_rules(), key=lambda r: r.rule)
        for rule in rules:
            methods = ",".join(sorted(rule.methods))
            click.secho(
                f"  - URL: {click.style(rule.rule, fg='yellow')}, Endpoint: {rule.endpoint}, Methods: {methods}"
            )
        click.secho("--------------------------\n", fg="cyan", bold=True)
        print_routes_once.already_run = True


@pytest.fixture(scope="session")
def app():
    # Créer une instance de l'application avec une configuration de test
    app_instance = create_api(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": TEST_DATABASE_URL,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "JWT_SECRET_KEY": "test-secret",  # JWT secret key for tests
        }
    )
    # Create tables
    with app_instance.app_context():
        if USE_ALEMBIC_MIGRATIONS:
            alembic_cfg = Config(toml_file="pyproject.toml")
            command.upgrade(alembic_cfg, "head")
        else:
            db.create_all()

    yield app_instance

    # Clean up after tests
    with app_instance.app_context():
        if USE_ALEMBIC_MIGRATIONS:
            alembic_cfg = Config(toml_file="pyproject.toml")
            command.downgrade(alembic_cfg, "base")
        else:
            db.drop_all()


@pytest.fixture
def db_session(app):
    """
    Gère l'isolation des tests de base de données en utilisant des transactions.
    Pour chaque test, une transaction est démarrée puis annulée (rollback).
    """
    with app.app_context():
        db.session.begin_nested()
        # Patch commit to be a flush, so that commits inside the application code
        # don't ruin the transaction isolation.
        with patch("src.database.db.session.commit", db.session.flush):
            yield db.session
        db.session.rollback()


@pytest.fixture
def client(app):
    """Fournit un client non authentifié de test Flask."""
    with app.test_client() as client:
        yield client


@pytest.fixture
def admin_role(db_session):
    """
    Crée un utilisateur administrateur dans la base de données de test
    et le retourne.
    """
    password = "password123"
    hashed_password = hashlib.md5(password.encode("utf-8")).hexdigest()
    admin_user = User(
        email="admin@example.com",
        first_name="Admin",
        last_name="User",
        password=hashed_password,
        is_admin=True,
    )
    db_session.add(admin_user)
    db_session.flush()
    return admin_user


@pytest.fixture
def user_role(db_session):
    """
    Crée un utilisateur administrateur dans la base de données de test
    et le retourne.
    """
    password = "password123"
    hashed_password = hashlib.md5(password.encode("utf-8")).hexdigest()
    std_user = User(
        email="user@example.com",
        first_name="Standard",
        last_name="User",
        password=hashed_password,
        is_admin=False,
    )
    db_session.add(std_user)
    db_session.flush()
    return std_user


@pytest.fixture
def admin_client(client, app, admin_role):
    """
    Fournit un client de test Flask avec un token JWT d'administrateur
    dans les en-têtes. L'ID de l'admin est attaché au client.
    """
    with app.app_context():
        # Crée un token pour l'utilisateur admin
        identity = admin_role.email
        claims = {"role": "admin", "user_id": admin_role.id_user}
        access_token = create_access_token(identity=identity, additional_claims=claims)

    # Ajoute le token aux en-têtes par défaut du client
    client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"

    # Attache l'ID de l'admin directement au client pour un accès facile dans les tests
    client.user_id = admin_role.id_user
    return client


@pytest.fixture
def user_client(client, app, user_role):
    """
    Fournit un client de test Flask avec un token JWT d'utilisateur standard
    dans les en-têtes. L'ID de l'utilisateur est attaché au client.
    """
    with app.app_context():
        # Crée un token pour l'utilisateur
        identity = user_role.email
        claims = {"role": "user", "user_id": user_role.id_user}
        access_token = create_access_token(identity=identity, additional_claims=claims)

    # Ajoute le token aux en-têtes par défaut du client
    client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"

    # Attache l'ID de l'utilisateur directement au client pour un accès facile dans les tests
    client.user_id = user_role.id_user
    return client


@pytest.fixture
def sample_project():
    return {
        "name": "Test Project",
        "description": "A test project description",
        "start_date": "01/03/2024",
        "end_date": "31/12/2024",
        "code": 12345,
    }
