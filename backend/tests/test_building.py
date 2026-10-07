def test_create_building(client):
    facility_payload = {
        "facility_code": "TEST-FAC-BLD-001",
        "name": "Test Facility",
        "location": "Test Location",
        "city": "Bhubaneswar",
        "state": "Odisha",
        "country": "India",
    }

    facility_response = client.post(
        "/facilities",
        json=facility_payload,
    )

    assert facility_response.status_code == 201

    facility = facility_response.json()["data"]

    building_payload = {
        "building_code": "TEST-BLD-001",
        "facility_id": facility["id"],
        "name": "Test Administration Building",
        "building_type": "OFFICE",
        "floor_count": 4,
        "area_sq_m": 5000,
    }

    response = client.post(
        "/buildings",
        json=building_payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Building created successfully"

    building = data["data"]

    assert building["building_code"] == "TEST-BLD-001"
    assert building["facility_id"] == facility["id"]
    assert building["name"] == "Test Administration Building"


def test_get_buildings(client):
    facility_payload = {
        "facility_code": "TEST-FAC-BLD-002",
        "name": "Test Facility",
        "location": "Test Location",
        "city": "Bhubaneswar",
        "state": "Odisha",
        "country": "India",
    }

    facility_response = client.post(
        "/facilities",
        json=facility_payload,
    )

    assert facility_response.status_code == 201

    facility_id = facility_response.json()["data"]["id"]

    building_payload = {
        "building_code": "TEST-BLD-002",
        "facility_id": facility_id,
        "name": "Test Office Building",
        "building_type": "OFFICE",
        "floor_count": 3,
        "area_sq_m": 3000,
    }

    create_response = client.post(
        "/buildings",
        json=building_payload,
    )

    assert create_response.status_code == 201

    response = client.get("/buildings")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Buildings retrieved successfully"
    assert len(data["data"]) == 1

    building = data["data"][0]

    assert building["building_code"] == "TEST-BLD-002"
    assert building["facility_id"] == facility_id


def test_get_buildings_by_facility(client):
    facility_payload = {
        "facility_code": "TEST-FAC-BLD-003",
        "name": "Test Facility",
        "location": "Test Location",
        "city": "Bhubaneswar",
        "state": "Odisha",
        "country": "India",
    }

    facility_response = client.post(
        "/facilities",
        json=facility_payload,
    )

    facility_id = facility_response.json()["data"]["id"]

    building_payload = {
        "building_code": "TEST-BLD-003",
        "facility_id": facility_id,
        "name": "Test Engineering Building",
        "building_type": "OFFICE",
        "floor_count": 5,
        "area_sq_m": 4500,
    }

    client.post(
        "/buildings",
        json=building_payload,
    )

    response = client.get(
        f"/buildings/facility/{facility_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Buildings retrieved successfully"
    assert len(data["data"]) == 1
    assert data["data"][0]["facility_id"] == facility_id


def test_get_building_not_found(client):
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.get(
        f"/buildings/{fake_id}"
    )

    assert response.status_code == 404

    data = response.json()

    assert data["status"] == "ERROR"
    assert "Building not found" in data["message"]


def test_create_building_with_invalid_facility(client):
    fake_facility_id = "00000000-0000-0000-0000-000000000000"

    building_payload = {
        "building_code": "TEST-BLD-INVALID",
        "facility_id": fake_facility_id,
        "name": "Invalid Building",
        "building_type": "OFFICE",
        "floor_count": 2,
        "area_sq_m": 1000,
    }

    response = client.post(
        "/buildings",
        json=building_payload,
    )

    assert response.status_code == 404

    data = response.json()

    assert data["status"] == "ERROR"
    assert "Facility not found" in data["message"]