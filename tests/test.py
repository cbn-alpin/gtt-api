import os
from datetime import date

import pytest
from alembic import command
from alembic.config import Config

from src.main import api, db


@pytest.fixture
def app():

    os.environ["CONFIG_PATH"] = ".env"

    app = api
    app.config["TESTING"] = True

    # Create tables
    with app.app_context():
        db.create_all()
        alembic_cfg = Config(toml_file="pyproject.toml")

        command.upgrade(alembic_cfg, "head")

    yield app

    # Clean up after tests
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def sample_project():
    return {
        "name": "Test Project",
        "description": "A test project description",
        "start_date": "2024-03-01",
        "end_date": "2024-12-31",
        "code": 12345,
    }


def test_create_project(client, sample_project):
    """Test creating a new project"""
    response = client.post("/api/projects", json=sample_project)
    assert response.status_code == 201
    data = response.get_json()
    assert "project" in data
    assert "message" in data
    assert data["message"] == "Project created"


def test_create_project_missing_required_fields(client):
    """Test creating a project with missing required fields"""
    invalid_data = {"description": "Missing required fields"}
    response = client.post("/api/projects", json=invalid_data)
    assert response.status_code == 400


''' def test_get_all_projects(client, sample_project):
    """Test getting all projects"""
    # First create a project
    client.post('/api/projects', json=sample_project)

    # Then get all projects
    response = client.get('/api/projects')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0 '''

''' def test_create_duplicate_project(client, sample_project):
    """Test creating a project with duplicate code"""
    # Create first project
    response1 = client.post('/api/projects', json=sample_project)
    assert response1.status_code == 201

    # Try to create second project with same code
    response2 = client.post('/api/projects', json=sample_project)
    assert response2.status_code == 400 '''


def test_create_project_invalid_dates(client, sample_project):
    """Test creating a project with invalid dates"""
    sample_project["start_date"] = "invalid-date"
    response = client.post("/api/projects", json=sample_project)
    assert response.status_code == 400


def test_create_project_end_date_before_start_date(client, sample_project):
    """Test creating a project with end date before start date"""
    sample_project["start_date"] = "2024-12-31"
    sample_project["end_date"] = "2024-01-01"
    response = client.post("/api/projects", json=sample_project)
    assert response.status_code == 400


''' def test_get_projects_empty_db(client):
    """Test getting projects when database is empty"""
    response = client.get('/api/projects')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 0 '''


def test_create_project_with_minimal_data(client):
    """Test creating a project with only required fields"""
    minimal_project = {"name": "Minimal Project", "start_date": "2024-03-01", "code": 54321}
    response = client.post("/api/projects", json=minimal_project)
    assert response.status_code == 201


def test_create_project_without_minimal_data(client):
    """Test creating a project with only required fields"""
    minimal_project = {"name": "Minimal Project", "code": 54321}
    response = client.post("/api/projects", json=minimal_project)
    assert response.status_code == 400
