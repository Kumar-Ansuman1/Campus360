def test_create_device(client):
    facility_payload = {
        "facility_code": "TEST-FAC-DEV-001",
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
        "building_code": "TEST-BLD-DEV-001",
        "facility_id": facility_id,
        "name": "Test Device Building",
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
        "device_code": "TEST-DEV-001",
        "building_id": building_id,
        "name": "Test Energy Meter",
        "device_type": "ENERGY_METER",
        "category": "ENERGY",
        "unit": "kWh",
    }

    response = client.post(
        "/devices",
        json=device_payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Device created successfully"

    device = data["data"]

    assert device["device_code"] == "TEST-DEV-001"
    assert device["building_id"] == building_id
    assert device["name"] == "Test Energy Meter"


def test_get_devices(client):
    facility_payload = {
        "facility_code": "TEST-FAC-DEV-002",
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
        "building_code": "TEST-BLD-DEV-002",
        "facility_id": facility_id,
        "name": "Test Building",
        "building_type": "OFFICE",
        "floor_count": 2,
        "area_sq_m": 2000,
    }

    building_response = client.post(
        "/buildings",
        json=building_payload,
    )

    building_id = building_response.json()["data"]["id"]

    device_payload = {
        "device_code": "TEST-DEV-002",
        "building_id": building_id,
        "name": "Test Water Meter",
        "device_type": "WATER_METER",
        "category": "WATER",
        "unit": "L",
    }

    create_response = client.post(
        "/devices",
        json=device_payload,
    )

    assert create_response.status_code == 201

    response = client.get("/devices")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Devices retrieved successfully"
    assert len(data["data"]) == 1

    device = data["data"][0]

    assert device["device_code"] == "TEST-DEV-002"
    assert device["building_id"] == building_id


def test_get_devices_by_building(client):
    facility_payload = {
        "facility_code": "TEST-FAC-DEV-003",
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
        "building_code": "TEST-BLD-DEV-003",
        "facility_id": facility_id,
        "name": "Test Building",
        "building_type": "OFFICE",
        "floor_count": 2,
        "area_sq_m": 2000,
    }

    building_response = client.post(
        "/buildings",
        json=building_payload,
    )

    building_id = building_response.json()["data"]["id"]

    device_payload = {
        "device_code": "TEST-DEV-003",
        "building_id": building_id,
        "name": "Test Air Quality Sensor",
        "device_type": "AIR_QUALITY_SENSOR",
        "category": "AIR_QUALITY",
        "unit": "AQI",
    }

    client.post(
        "/devices",
        json=device_payload,
    )

    response = client.get(
        f"/devices/building/{building_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Devices retrieved successfully"
    assert len(data["data"]) == 1
    assert data["data"][0]["building_id"] == building_id


def test_get_device_by_category(client):
    facility_payload = {
        "facility_code": "TEST-FAC-DEV-004",
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
        "building_code": "TEST-BLD-DEV-004",
        "facility_id": facility_id,
        "name": "Test Building",
        "building_type": "OFFICE",
        "floor_count": 2,
        "area_sq_m": 2000,
    }

    building_response = client.post(
        "/buildings",
        json=building_payload,
    )

    building_id = building_response.json()["data"]["id"]

    device_payload = {
        "device_code": "TEST-DEV-004",
        "building_id": building_id,
        "name": "Test Energy Meter",
        "device_type": "ENERGY_METER",
        "category": "ENERGY",
        "unit": "kWh",
    }

    client.post(
        "/devices",
        json=device_payload,
    )

    response = client.get(
        "/devices/category/ENERGY"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Devices retrieved successfully"
    assert len(data["data"]) == 1
    assert data["data"][0]["category"] == "ENERGY"


def test_get_device_not_found(client):
    fake_id = "00000000-0000-0000-0000-000000000000"

    response = client.get(
        f"/devices/{fake_id}"
    )

    assert response.status_code == 404

    data = response.json()

    assert data["status"] == "ERROR"
    assert "Device not found" in data["message"]


def test_create_device_with_invalid_building(client):
    fake_building_id = "00000000-0000-0000-0000-000000000000"

    device_payload = {
        "device_code": "TEST-DEV-INVALID",
        "building_id": fake_building_id,
        "name": "Invalid Device",
        "device_type": "ENERGY_METER",
        "category": "ENERGY",
        "unit": "kWh",
    }

    response = client.post(
        "/devices",
        json=device_payload,
    )

    assert response.status_code == 404

    data = response.json()

    assert data["status"] == "ERROR"
    assert "Building not found" in data["message"]