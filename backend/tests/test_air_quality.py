def create_test_device(client):
    facility_response = client.post(
        "/facilities",
        json={
            "facility_code": "FAC-AQ-001",
            "name": "Air Quality Test Facility",
            "location": "Infocity",
            "city": "Bhubaneswar",
            "state": "Odisha",
            "country": "India",
        },
    )
    facility_id = facility_response.json()["data"]["id"]

    building_response = client.post(
        "/buildings",
        json={
            "building_code": "BLD-AQ-001",
            "facility_id": facility_id,
            "name": "Air Quality Test Building",
            "building_type": "OFFICE",
            "floor_count": 4,
            "area_sq_m": 4000,
        },
    )
    building_id = building_response.json()["data"]["id"]

    device_response = client.post(
        "/devices",
        json={
            "device_code": "DEV-AQ-001",
            "building_id": building_id,
            "name": "Air Quality Monitoring Device",
            "device_type": "AIR_QUALITY_SENSOR",
            "category": "AIR_QUALITY",
            "unit": "AQI",
        },
    )

    return facility_id, building_id, device_response.json()["data"]["id"]


def create_air_quality(client):
    facility_id, building_id, device_id = create_test_device(client)

    response = client.post(
        "/air-quality",
        json={
            "facility_id": facility_id,
            "building_id": building_id,
            "device_id": device_id,
            "pm25": 29.8,
            "pm10": 54.6,
            "co2": 705.0,
            "temperature": 27.1,
            "humidity": 60.2,
            "aqi": 72.0,
            "recorded_at": "2026-09-29T10:00:00",
        },
    )

    return response, facility_id, building_id, device_id


def test_create_air_quality(client):
    response, _, _, _ = create_air_quality(client)

    assert response.status_code == 201

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Air quality record created successfully"
    assert data["data"]["pm25"] == 29.8
    assert data["data"]["pm10"] == 54.6
    assert data["data"]["co2"] == 705.0
    assert data["data"]["temperature"] == 27.1
    assert data["data"]["humidity"] == 60.2
    assert data["data"]["aqi"] == 72.0


def test_get_air_quality_by_facility(client):
    _, facility_id, _, _ = create_air_quality(client)

    response = client.get(f"/air-quality/facility/{facility_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert len(data["data"]) == 1
    assert data["data"][0]["aqi"] == 72.0


def test_get_air_quality_by_building(client):
    _, _, building_id, _ = create_air_quality(client)

    response = client.get(f"/air-quality/building/{building_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert len(data["data"]) == 1


def test_get_air_quality_by_device(client):
    _, _, _, device_id = create_air_quality(client)

    response = client.get(f"/air-quality/device/{device_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert len(data["data"]) == 1


def test_get_air_quality_by_time_range(client):
    create_air_quality(client)

    response = client.get(
        "/air-quality/range/2026-09-29T09:00:00/2026-09-29T11:00:00"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert len(data["data"]) == 1


def test_get_air_quality_by_id(client):
    response, _, _, _ = create_air_quality(client)

    air_quality_id = response.json()["data"]["id"]

    response = client.get(f"/air-quality/{air_quality_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["data"]["id"] == air_quality_id


def test_invalid_air_quality_time_range(client):
    response = client.get(
        "/air-quality/range/2026-09-29T11:00:00/2026-09-29T09:00:00"
    )

    assert response.status_code == 400

    data = response.json()

    assert data["status"] == "ERROR"


def test_invalid_air_quality_hierarchy(client):
    _, facility_id, building_id, device_id = create_air_quality(client)

    second_facility = client.post(
        "/facilities",
        json={
            "facility_code": "FAC-AQ-002",
            "name": "Second Air Quality Facility",
            "location": "Patia",
            "city": "Bhubaneswar",
            "state": "Odisha",
            "country": "India",
        },
    )

    second_facility_id = second_facility.json()["data"]["id"]

    response = client.post(
        "/air-quality",
        json={
            "facility_id": second_facility_id,
            "building_id": building_id,
            "device_id": device_id,
            "pm25": 35.0,
            "pm10": 60.0,
            "co2": 750.0,
            "temperature": 28.0,
            "humidity": 65.0,
            "aqi": 80.0,
            "recorded_at": "2026-09-29T12:00:00",
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert data["status"] == "ERROR"