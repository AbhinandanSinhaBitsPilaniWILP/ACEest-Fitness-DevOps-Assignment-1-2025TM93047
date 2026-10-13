def test_health_endpoint(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_dashboard_requires_login(client):
    response = client.get("/dashboard")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_client_program_and_workout_flow(logged_in):
    response = logged_in.post(
        "/clients",
        json={"name": "Priya Shah", "age": 28, "weight": 63.5},
    )
    assert response.status_code == 201
    client_id = response.get_json()["id"]

    response = logged_in.post(
        f"/clients/{client_id}/program",
        json={"program_type": "Beginner"},
    )
    assert response.status_code == 200
    assert response.get_json()["program"]

    response = logged_in.post(
        f"/clients/{client_id}/workouts",
        json={"workout_type": "Strength", "duration_min": 45},
    )
    assert response.status_code == 201

    response = logged_in.get(f"/api/clients/{client_id}")
    payload = response.get_json()
    assert response.status_code == 200
    assert payload["name"] == "Priya Shah"
    assert len(payload["workouts"]) == 1


def test_duplicate_client_is_rejected(logged_in):
    first = logged_in.post("/clients", json={"name": "Same Name"})
    second = logged_in.post("/clients", json={"name": "Same Name"})
    assert first.status_code == 201
    assert second.status_code == 409


def test_api_requires_authentication(client):
    response = client.get("/api/clients")
    assert response.status_code == 401
    assert response.get_json()["error"] == "Authentication required"

