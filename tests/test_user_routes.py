import pytest

from tests.conftest import TEST_DATABASE_URL


@pytest.fixture
def create_user(admin_client):
    """Create a user and return the user ID."""
    user_data = {
        "email": "user1@example.com",
        "first_name": "User",
        "last_name": "One",
        "password": "password123",
        "is_admin": False,
    }
    response = admin_client.post("/api/users", json=user_data)
    assert response.status_code == 201
    return response.get_json()["user"]


@pytest.fixture
def create_actions(admin_client, sample_project):
    """Create actions and return their IDs."""
    admin_client.post("/api/projects", json=sample_project)
    action_ids = []
    for i in range(1, 4):
        action_data = {"numero_action": i, "name": f"Action {i}", "id_project": 1}

        response = admin_client.post("/api/actions", json=action_data)
        assert response.status_code == 201
        action_ids.append(response.get_json()["action_id"])
    return action_ids


@pytest.fixture
def link_user_actions(user_client, create_user, create_actions):
    """Link user with actions."""
    user_id = create_user
    for action_id in create_actions:
        link_data = {"user_id": user_id, "action_id": action_id}
        response = user_client.post(f"/api/user/{user_id}/action/{action_id}", json=link_data)
        assert response.status_code == 201
    return user_id


@pytest.fixture
def create_user_action(user_client, create_user, create_actions):
    """Create a user action and return its ID."""
    user_id = create_user
    action_id = create_actions[0]  # Use the first action for simplicity
    link_data = {"user_id": user_id, "action_id": action_id}
    response = user_client.post(f"/api/user/{user_id}/action/{action_id}", json=link_data)
    assert response.status_code == 201
    return response.get_json()["user_action"]


def test_get_user_projects(user_client, link_user_actions):
    """Test getting projects by user ID"""
    user_id = link_user_actions
    response = user_client.get(f"/api/user/{user_id}/project")
    assert response.status_code == 200, response.get_data(as_text=True)

    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1


@pytest.mark.skipif(
    TEST_DATABASE_URL.startswith("sqlite"),
    reason="SQLite can't use generate_series function used in the code.",
)
@pytest.mark.parametrize(
    ("date_start", "date_end", "expected_status"),
    [
        ("2024-01-01", "2024-12-31", 200),
        ("invalid-date", "2024-12-31", 400),
    ],
)
def test_get_user_projects_time(
    user_client, link_user_actions, date_start, date_end, expected_status
):
    """Test getting projects by user ID with time range"""
    user_id = link_user_actions
    response = user_client.get(
        f"/api/user/{user_id}/projects/times",
        query_string={"date_start": date_start, "date_end": date_end},
    )
    assert response.status_code == expected_status, response.get_data(as_text=True)

    if expected_status == 200:
        data = response.get_json()
        assert isinstance(data, list)


def test_delete_user_action(user_client, create_user_action):
    """Test deleting a user action."""
    user_id = create_user_action["id_user"]
    action_id = create_user_action["id_action"]

    response = user_client.delete(f"/api/user/{user_id}/action/{action_id}")
    assert response.status_code == 204, response.get_data(as_text=True)

    response = user_client.delete(f"/api/user/{user_id}/action/{action_id}")
    assert response.status_code == 404, response.get_data(as_text=True)


def test_delete_nonexistent_user_action(user_client):
    """Test deleting a nonexistent user action."""
    user_id = user_client.user_id
    response = user_client.delete(f"/api/user/{user_id}/action/999")
    assert response.status_code == 404, response.get_data(as_text=True)

    response = user_client.delete("/api/user/999/action/999")
    assert response.status_code == 403, response.get_data(as_text=True)
