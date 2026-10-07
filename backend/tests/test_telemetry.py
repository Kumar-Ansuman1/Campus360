def create_test_device(client):
    facility_payload = {
        "facility_code": "TEST-FAC-TEL-001",
        "name": "Telemetry Test Facility",
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
        "building_code": "TEST-BLD-TEL-001",
        "facility_id": facility_id,
        "name": "Telemetry Test Building",
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
        "device_code": "TEST-DEV-TEL-001",
        "building_id": building_id,
        "name": "Telemetry Energy Meter",
        "device_type": "ENERGY_METER",
        "category": "ENERGY",
        "unit": "kWh",
    }

    device_response = client.post(
        "/devices",
        json=device_payload,
    )

    assert device_response.status_code == 201

    return device_response.json()["data"]["id"]


def test_create_telemetry(client):
    device_id = create_test_device(client)

    payload = {
        "device_id": device_id,
        "metric": "power_consumption",
        "value": 47.3,
        "unit": "kWh",
        "timestamp": "2026-09-29T17:15:00",
    }

    response = client.post(
        "/telemetry",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Telemetry created successfully"

    telemetry = data["data"]

    assert telemetry["device_id"] == device_id
    assert telemetry["metric"] == "power_consumption"
    assert telemetry["value"] == 47.3
    assert telemetry["unit"] == "kWh"


def test_get_telemetry_by_device(client):
    device_id = create_test_device(client)

    payload = {
        "device_id": device_id,
        "metric": "power_consumption",
        "value": 50.5,
        "unit": "kWh",
        "timestamp": "2026-09-29T18:00:00",
    }

    create_response = client.post(
        "/telemetry",
        json=payload,
    )

    assert create_response.status_code == 201

    response = client.get(
        f"/telemetry/device/{device_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Telemetry records retrieved successfully"
    assert len(data["data"]) == 1
    assert data["data"][0]["device_id"] == device_id


def test_get_telemetry_by_metric(client):
    device_id = create_test_device(client)

    payload = {
        "device_id": device_id,
        "metric": "temperature",
        "value": 27.5,
        "unit": "C",
        "timestamp": "2026-09-29T18:10:00",
    }

    client.post(
        "/telemetry",
        json=payload,
    )

    response = client.get(
        "/telemetry/metric/temperature"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Telemetry records retrieved successfully"
    assert len(data["data"]) == 1
    assert data["data"][0]["metric"] == "temperature"


def test_get_telemetry_by_time_range(client):
    device_id = create_test_device(client)

    payload = {
        "device_id": device_id,
        "metric": "power_consumption",
        "value": 55.2,
        "unit": "kWh",
        "timestamp": "2026-09-29T19:00:00",
    }

    client.post(
        "/telemetry",
        json=payload,
    )

    response = client.get(
        "/telemetry/range/"
        "2026-09-29T18:00:00/"
        "2026-09-29T20:00:00"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Telemetry records retrieved successfully"
    assert len(data["data"]) == 1


def test_get_telemetry_by_id(client):
    device_id = create_test_device(client)

    payload = {
        "device_id": device_id,
        "metric": "humidity",
        "value": 60.2,
        "unit": "%",
        "timestamp": "2026-09-29T19:15:00",
    }

    create_response = client.post(
        "/telemetry",
        json=payload,
    )

    telemetry_id = create_response.json()["data"]["id"]

    response = client.get(
        f"/telemetry/{telemetry_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Telemetry record retrieved successfully"
    assert data["data"]["id"] == telemetry_id


def test_invalid_telemetry_time_range(client):
    response = client.get(
        "/telemetry/range/"
        "2026-09-30T10:00:00/"
        "2026-09-29T10:00:00"
    )

    assert response.status_code == 400

    data = response.json()

    assert data["status"] == "ERROR"
    assert data["message"] == "start_time must be before end_time"


def test_create_telemetry_with_invalid_device(client):
    fake_device_id = "00000000-0000-0000-0000-000000000000"

    payload = {
        "device_id": fake_device_id,
        "metric": "power_consumption",
        "value": 50.0,
        "unit": "kWh",
        "timestamp": "2026-09-29T20:00:00",
    }

    response = client.post(
        "/telemetry",
        json=payload,
    )

    assert response.status_code == 404

    data = response.json()

    assert data["status"] == "ERROR"
    assert "Device not found" in data["message"]
