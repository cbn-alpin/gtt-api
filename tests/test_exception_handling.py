from gtt.api.exception import DeleteError


def test_api_error_handler_returns_business_error_payload(app):
    @app.route("/boom")
    def boom():
        raise DeleteError("Impossible de supprimer cet élément")

    with app.test_client() as client:
        response = client.get("/boom")

    assert response.status_code == 409
    assert response.get_json()["status"] == "error"
    assert response.get_json()["type"] == "CONFLICT"
    assert response.get_json()["code"] == "DELETE_FORBIDDEN"
    assert response.get_json()["message"] == "Impossible de supprimer cet élément"
