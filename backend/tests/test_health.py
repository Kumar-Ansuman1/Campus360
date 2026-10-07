def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "UP"
    assert data["service"] == "EcoFacility AI Backend"
    assert data["version"] == "0.1.0"