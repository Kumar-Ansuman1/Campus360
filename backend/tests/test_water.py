def create_test_device(client):
    facility_payload = {
        "facility_code": "TEST-FAC-WAT-001",
        "name": "Water Test Facility",
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
        "building_code": "TEST-BLD-WAT-001",
        "facility_id": facility_id,
        "name": "Water Test Building",
        "building_type": "OFFICE",
        "floor_count": 3,
        "area_sq_m": 3000,
    }

    building_response = client.post(
        "/buildings",
        json=building_payload,
    )

    assert building_response.status_code == 201

    building_id = building_response.json()["data"]["id"]

    device_payload = {
        "device_code": "TEST-DEV-WAT-001",
        "building_id": building_id,
        "name": "Water Meter",
        "device_type": "WATER_METER",
        "category": "WATER",
        "unit": "L",
    }

    device_response = client.post(
        "/devices",
        json=device_payload,
    )

    assert device_response.status_code == 201

    device_id = device_response.json()["data"]["id"]

    return facility_id, building_id, device_id


def test_create_water(client):
    facility_id, building_id, device_id = create_test_device(client)

    payload = {
        "facility_id": facility_id,
        "building_id": building_id,
        "device_id": device_id,
        "consumption": 138.7,
        "unit": "L",
        "recorded_at": "2026-09-29T16:15:00",
    }

    response = client.post(
        "/water",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Water record created successfully"

    water = data["data"]

    assert water["facility_id"] == facility_id
    assert water["building_id"] == building_id
    assert water["device_id"] == device_id
    assert water["consumption"] == 138.7
    assert water["unit"] == "L"


def test_get_water_by_facility(client):
    facility_id, building_id, device_id = create_test_device(client)

    payload = {
        "facility_id": facility_id,
        "building_id": building_id,
        "device_id": device_id,
        "consumption": 125.5,
        "unit": "L",
        "recorded_at": "2026-09-29T14:35:00",
    }

    client.post("/water", json=payload)

    response = client.get(
        f"/water/facility/{facility_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Water records retrieved successfully"
    assert len(data["data"]) == 1
    assert data["data"][0]["facility_id"] == facility_id


def test_get_water_by_building(client):
    facility_id, building_id, device_id = create_test_device(client)

    payload = {
        "facility_id": facility_id,
        "building_id": building_id,
        "device_id": device_id,
        "consumption": 130.0,
        "unit": "L",
        "recorded_at": "2026-09-29T15:00:00",
    }

    client.post("/water", json=payload)

    response = client.get(
        f"/water/building/{building_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Water records retrieved successfully"
    assert len(data["data"]) == 1
    assert data["data"][0]["building_id"] == building_id


def test_get_water_by_device(client):
    facility_id, building_id, device_id = create_test_device(client)

    payload = {
        "facility_id": facility_id,
        "building_id": building_id,
        "device_id": device_id,
        "consumption": 140.0,
        "unit": "L",
        "recorded_at": "2026-09-29T17:00:00",
    }

    client.post("/water", json=payload)

    response = client.get(
        f"/water/device/{device_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Water records retrieved successfully"
    assert len(data["data"]) == 1
    assert data["data"][0]["device_id"] == device_id


def test_get_water_by_time_range(client):
    facility_id, building_id, device_id = create_test_device(client)

    payload = {
        "facility_id": facility_id,
        "building_id": building_id,
        "device_id": device_id,
        "consumption": 150.0,
        "unit": "L",
        "recorded_at": "2026-09-29T18:00:00",
    }

    client.post("/water", json=payload)

    response = client.get(
        "/water/range/"
        "2026-09-29T17:00:00/"
        "2026-09-29T19:00:00"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Water records retrieved successfully"
    assert len(data["data"]) == 1


def test_get_water_by_id(client):
    facility_id, building_id, device_id = create_test_device(client)

    payload = {
        "facility_id": facility_id,
        "building_id": building_id,
        "device_id": device_id,
        "consumption": 155.0,
        "unit": "L",
        "recorded_at": "2026-09-29T19:00:00",
    }

    create_response = client.post(
        "/water",
        json=payload,
    )

    assert create_response.status_code == 201

    water_id = create_response.json()["data"]["id"]

    response = client.get(
        f"/water/{water_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Water record retrieved successfully"
    assert data["data"]["id"] == water_id


def test_invalid_water_time_range(client):
    response = client.get(
        "/water/range/"
        "2026-09-30T10:00:00/"
        "2026-09-29T10:00:00"
    )

    assert response.status_code == 400

    data = response.json()

    assert data["status"] == "ERROR"
    assert data["message"] == "start_time must be before end_time"


def test_create_water_with_invalid_hierarchy(client):
    fake_facility_id = "00000000-0000-0000-0000-000000000000"
    fake_building_id = "00000000-0000-0000-0000-000000000001"
    fake_device_id = "00000000-0000-0000-0000-000000000002"

    payload = {
        "facility_id": fake_facility_id,
        "building_id": fake_building_id,
        "device_id": fake_device_id,
        "consumption": 100.0,
        "unit": "L",
        "recorded_at": "2026-09-29T20:00:00",
    }

    response = client.post(
        "/water",
        json=payload,
    )

    assert response.status_code == 404

    data = response.json()

    assert data["status"] == "ERROR"
    assert "Facility not found" in data["message"]