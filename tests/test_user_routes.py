import pytest
from flask import json
from tests.test import app, client, sample_project

@pytest.fixture
def create_user(client):
    """Create a user and return the user ID."""
    user_data = {
        "email": "user1@example.com",
        "first_name": "User",
        "last_name": "One",
        "password": "password123",
        "is_admin": False
    }
    response = client.post('/api/users', json=user_data)
    assert response.status_code == 201
    return response.get_json()['user']

@pytest.fixture
def create_actions(client, sample_project):
    """Create actions and return their IDs."""
    client.post('/api/projects', json=sample_project)
    action_ids = []
    for i in range(1, 4):
        action_data = {
            "name": f"Action {i}",
            "id_project": 1
        }

        response = client.post('/api/actions', json=action_data)
        assert response.status_code == 201
        action_ids.append(response.get_json()['action_id'])
    return action_ids

@pytest.fixture
def link_user_actions(client, create_user, create_actions):
    """Link user with actions."""
    user_id = create_user
    for action_id in create_actions:
        link_data = {
            "user_id": user_id,
            "action_id": action_id
        }
        response = client.post('/api/user/action', json=link_data)
        assert response.status_code == 201

@pytest.fixture
def create_user_action(client, create_user, create_actions):
    """Create a user action and return its ID."""
    user_id = create_user
    action_id = create_actions[0]  # Use the first action for simplicity
    link_data = {
        "user_id": user_id,
        "action_id": action_id
    }
    response = client.post('/api/user/action', json=link_data)
    assert response.status_code == 201
    return response.get_json()['user_action']

@pytest.mark.parametrize("user_id, expected_status, expected_length", [
    (1, 200, 1),
    (999, 200, 0)
])
def test_get_user_projects(client, link_user_actions, user_id, expected_status, expected_length):
    """Test getting projects by user ID"""
    response = client.get(f'/api/user/{user_id}/project')
    assert response.status_code == expected_status

    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == expected_length


@pytest.mark.parametrize("user_id, date_start, date_end, expected_status", [
    (1, "2024-01-01", "2024-12-31", 200),
    (999, "2024-01-01", "2024-12-31", 404),
    (1, "invalid-date", "2024-12-31", 400),
])
def test_get_user_projects_time(client, link_user_actions, user_id, date_start, date_end, expected_status):
    """Test getting projects by user ID with time range"""
    response = client.get(f'/api/user/{user_id}/projects/times', query_string={'date_start': date_start, 'date_end': date_end})
    assert response.status_code == expected_status

    if expected_status == 200:
        data = response.get_json()
        assert isinstance(data, list)

def test_delete_user_action(client, create_user_action):
    """Test deleting a user action."""
    user_action_id = create_user_action

    response = client.delete(f'/api/user/action/{user_action_id}')
    assert response.status_code == 204

    response = client.delete(f'/api/user/action/{user_action_id}')
    assert response.status_code == 404

def test_delete_nonexistent_user_action(client):
    """Test deleting a nonexistent user action."""

    response = client.delete('/api/user/action/9999')
    assert response.status_code == 404

