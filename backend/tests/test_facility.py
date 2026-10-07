def test_create_facility(client):
    payload = {
        "facility_code": "TEST-FAC-001",
        "name": "Test Smart Campus",
        "location": "Test Location",
        "city": "Bhubaneswar",
        "state": "Odisha",
        "country": "India",
    }

    response = client.post("/facilities", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Facility created successfully"

    facility = data["data"]

    assert facility["facility_code"] == "TEST-FAC-001"
    assert facility["name"] == "Test Smart Campus"
    assert facility["city"] == "Bhubaneswar"


def test_get_facilities(client):
    payload = {
        "facility_code": "TEST-FAC-002",
        "name": "Another Test Campus",
        "location": "Test Location",
        "city": "Bhubaneswar",
        "state": "Odisha",
        "country": "India",
    }

    create_response = client.post("/facilities", json=payload)

    assert create_response.status_code == 201

    response = client.get("/facilities")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Facilities retrieved successfully"
    assert len(data["data"]) == 1

    facility = data["data"][0]

    assert facility["facility_code"] == "TEST-FAC-002"
    assert facility["name"] == "Another Test Campus"


def test_get_facility_not_found(client):
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.get(f"/facilities/{fake_id}")

    assert response.status_code == 404

    data = response.json()

    assert data["status"] == "ERROR"
    assert "Facility not found" in data["message"]


def test_create_duplicate_facility(client):
    payload = {
        "facility_code": "TEST-FAC-DUPLICATE",
        "name": "Duplicate Test Campus",
        "location": "Test Location",
        "city": "Bhubaneswar",
        "state": "Odisha",
        "country": "India",
    }

    first_response = client.post("/facilities", json=payload)

    assert first_response.status_code == 201

    second_response = client.post("/facilities", json=payload)

    assert second_response.status_code == 409

    data = second_response.json()

    assert data["status"] == "ERROR"