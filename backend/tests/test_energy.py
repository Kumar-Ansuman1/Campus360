def create_test_device(client):
    facility_payload = {
        "facility_code": "TEST-FAC-ENG-001",
        "name": "Energy Test Facility",
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
        "building_code": "TEST-BLD-ENG-001",
        "facility_id": facility_id,
        "name": "Energy Test Building",
        "building_type": "OFFICE",
        "floor_count": 4,
        "area_sq_m": 4000,
    }

    building_response = client.post(
        "/buildings",
        json=building_payload,
    )

    assert building_response.status_code == 201

    building_id = building_response.json()["data"]["id"]

    device_payload = {
        "device_code": "TEST-DEV-ENG-001",
        "building_id": building_id,
        "name": "Energy Meter",
        "device_type": "ENERGY_METER",
        "category": "ENERGY",
        "unit": "kWh",
    }

    device_response = client.post(
        "/devices",
        json=device_payload,
    )

    assert device_response.status_code == 201

    device_id = device_response.json()["data"]["id"]

    return facility_id, building_id, device_id


def test_create_energy(client):
    facility_id, building_id, device_id = create_test_device(client)

    payload = {
        "facility_id": facility_id,
        "building_id": building_id,
        "device_id": device_id,
        "consumption": 45.8,
        "unit": "kWh",
        "recorded_at": "2026-09-29T16:00:00",
    }

    response = client.post(
        "/energy",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Energy record created successfully"

    energy = data["data"]

    assert energy["facility_id"] == facility_id
    assert energy["building_id"] == building_id
    assert energy["device_id"] == device_id
    assert energy["consumption"] == 45.8
    assert energy["unit"] == "kWh"


def test_get_energy_by_facility(client):
    facility_id, building_id, device_id = create_test_device(client)

    payload = {
        "facility_id": facility_id,
        "building_id": building_id,
        "device_id": device_id,
        "consumption": 42.7,
        "unit": "kWh",
        "recorded_at": "2026-09-29T14:30:00",
    }

    client.post("/energy", json=payload)

    response = client.get(
        f"/energy/facility/{facility_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Energy records retrieved successfully"
    assert len(data["data"]) == 1
    assert data["data"][0]["facility_id"] == facility_id


def test_get_energy_by_building(client):
    facility_id, building_id, device_id = create_test_device(client)

    payload = {
        "facility_id": facility_id,
        "building_id": building_id,
        "device_id": device_id,
        "consumption": 43.5,
        "unit": "kWh",
        "recorded_at": "2026-09-29T15:00:00",
    }

    client.post("/energy", json=payload)

    response = client.get(
        f"/energy/building/{building_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Energy records retrieved successfully"
    assert len(data["data"]) == 1
    assert data["data"][0]["building_id"] == building_id


def test_get_energy_by_device(client):
    facility_id, building_id, device_id = create_test_device(client)

    payload = {
        "facility_id": facility_id,
        "building_id": building_id,
        "device_id": device_id,
        "consumption": 47.3,
        "unit": "kWh",
        "recorded_at": "2026-09-29T17:15:00",
    }

    client.post("/energy", json=payload)

    response = client.get(
        f"/energy/device/{device_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Energy records retrieved successfully"
    assert len(data["data"]) == 1
    assert data["data"][0]["device_id"] == device_id


def test_get_energy_by_time_range(client):
    facility_id, building_id, device_id = create_test_device(client)

    payload = {
        "facility_id": facility_id,
        "building_id": building_id,
        "device_id": device_id,
        "consumption": 50.0,
        "unit": "kWh",
        "recorded_at": "2026-09-29T18:00:00",
    }

    client.post("/energy", json=payload)

    response = client.get(
        "/energy/range/"
        "2026-09-29T17:00:00/"
        "2026-09-29T19:00:00"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Energy records retrieved successfully"
    assert len(data["data"]) == 1


def test_get_energy_by_id(client):
    facility_id, building_id, device_id = create_test_device(client)

    payload = {
        "facility_id": facility_id,
        "building_id": building_id,
        "device_id": device_id,
        "consumption": 51.2,
        "unit": "kWh",
        "recorded_at": "2026-09-29T19:00:00",
    }

    create_response = client.post(
        "/energy",
        json=payload,
    )

    assert create_response.status_code == 201

    energy_id = create_response.json()["data"]["id"]

    response = client.get(
        f"/energy/{energy_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Energy record retrieved successfully"
    assert data["data"]["id"] == energy_id


def test_invalid_energy_time_range(client):
    response = client.get(
        "/energy/range/"
        "2026-09-30T10:00:00/"
        "2026-09-29T10:00:00"
    )

    assert response.status_code == 400

    data = response.json()

    assert data["status"] == "ERROR"
    assert data["message"] == "start_time must be before end_time"


def test_create_energy_with_invalid_hierarchy(client):
    fake_facility_id = "00000000-0000-0000-0000-000000000000"
    fake_building_id = "00000000-0000-0000-0000-000000000001"
    fake_device_id = "00000000-0000-0000-0000-000000000002"

    payload = {
        "facility_id": fake_facility_id,
        "building_id": fake_building_id,
        "device_id": fake_device_id,
        "consumption": 45.0,
        "unit": "kWh",
        "recorded_at": "2026-09-29T20:00:00",
    }

    response = client.post(
        "/energy",
        json=payload,
    )

    assert response.status_code == 404

    data = response.json()

    assert data["status"] == "ERROR"
    assert "Facility not found" in data["message"]