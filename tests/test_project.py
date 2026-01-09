def test_create_project(admin_client, sample_project):
    """Test creating a new project"""
    response = admin_client.post("/api/projects", json=sample_project)
    assert response.status_code == 201, response.get_data(as_text=True)
    data = response.get_json()
    assert "project" in data
    assert "message" in data
    assert data["message"] == "Project created"


def test_create_project_invalid_dates(admin_client, sample_project):
    """Test creating a project with invalid dates"""
    sample_project["start_date"] = "invalid-date"
    response = admin_client.post("/api/projects", json=sample_project)
    assert response.status_code == 400


def test_create_project_end_date_before_start_date(admin_client, sample_project):
    """Test creating a project with end date before start date"""
    sample_project["start_date"] = "31/12/2024"
    sample_project["end_date"] = "01/01/2024"
    response = admin_client.post("/api/projects", json=sample_project)
    assert response.status_code == 400


def test_create_project_with_minimal_data(admin_client):
    """Test creating a project with only required fields"""
    minimal_project = {"name": "Minimal Project", "start_date": "01/03/2024", "code": 54321}
    response = admin_client.post("/api/projects", json=minimal_project)
    assert response.status_code == 201


def test_create_project_missing_all_required_fields(admin_client):
    """Test creating a project with missing all required fields"""
    invalid_data = {"description": "Missing required fields"}
    response = admin_client.post("/api/projects", json=invalid_data)
    assert response.status_code == 400


def test_create_project_with_missing_stard_date_field(admin_client):
    """Test creating a project with missing required fields"""
    minimal_project = {"name": "Minimal Project", "code": 54321}
    response = admin_client.post("/api/projects", json=minimal_project)
    assert response.status_code == 400
