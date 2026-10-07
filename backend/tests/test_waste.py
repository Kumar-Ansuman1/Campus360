from datetime import datetime, timedelta


def create_test_device(client):
    facility_response = client.post(
        "/facilities",
        json={
            "facility_code": "FAC-WASTE-001",
            "name": "Waste Test Facility",
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
            "building_code": "BLD-WASTE-001",
            "facility_id": facility_id,
            "name": "Waste Test Building",
            "building_type": "OFFICE",
            "floor_count": 3,
            "area_sq_m": 3000,
        },
    )
    building_id = building_response.json()["data"]["id"]

    device_response = client.post(
        "/devices",
        json={
            "device_code": "DEV-WASTE-001",
            "building_id": building_id,
            "name": "Waste Monitoring Device",
            "device_type": "WASTE_SENSOR",
            "category": "WASTE",
            "unit": "kg",
        },
    )

    return facility_id, building_id, device_response.json()["data"]["id"]


def create_waste(client):
    facility_id, building_id, device_id = create_test_device(client)

    response = client.post(
        "/waste",
        json={
            "facility_id": facility_id,
            "building_id": building_id,
            "device_id": device_id,
            "waste_type": "SOLID",
            "quantity": 25.5,
            "unit": "kg",
            "recorded_at": "2026-09-29T10:00:00",
        },
    )

    return response, facility_id, building_id, device_id


def test_create_waste(client):
    response, _, _, _ = create_waste(client)

    assert response.status_code == 201

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Waste record created successfully"
    assert data["data"]["waste_type"] == "SOLID"
    assert data["data"]["quantity"] == 25.5
    assert data["data"]["unit"] == "kg"


def test_get_waste_by_facility(client):
    _, facility_id, _, _ = create_waste(client)

    response = client.get(f"/waste/facility/{facility_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert len(data["data"]) == 1
    assert data["data"][0]["waste_type"] == "SOLID"


def test_get_waste_by_building(client):
    _, _, building_id, _ = create_waste(client)

    response = client.get(f"/waste/building/{building_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert len(data["data"]) == 1


def test_get_waste_by_device(client):
    _, _, _, device_id = create_waste(client)

    response = client.get(f"/waste/device/{device_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert len(data["data"]) == 1


def test_get_waste_by_type(client):
    create_waste(client)

    response = client.get("/waste/type/SOLID")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert len(data["data"]) == 1
    assert data["data"][0]["waste_type"] == "SOLID"


def test_get_waste_by_time_range(client):
    _, facility_id, _, _ = create_waste(client)

    response = client.get(
        "/waste/range/2026-09-29T09:00:00/2026-09-29T11:00:00"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert len(data["data"]) == 1


def test_get_waste_by_id(client):
    response, _, _, _ = create_waste(client)

    waste_id = response.json()["data"]["id"]

    response = client.get(f"/waste/{waste_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["data"]["id"] == waste_id


def test_invalid_waste_time_range(client):
    response = client.get(
        "/waste/range/2026-09-29T11:00:00/2026-09-29T09:00:00"
    )

    assert response.status_code == 400

    data = response.json()

    assert data["status"] == "ERROR"


def test_invalid_waste_hierarchy(client):
    _, facility_id, building_id, device_id = create_waste(client)

    response = client.post(
        "/waste",
        json={
            "facility_id": facility_id,
            "building_id": building_id,
            "device_id": device_id,
            "waste_type": "SOLID",
            "quantity": 10.0,
            "unit": "kg",
            "recorded_at": "2026-09-29T12:00:00",
        },
    )

    assert response.status_code == 201

    # Create another facility and attempt to associate the existing
    # building/device hierarchy with it.
    second_facility = client.post(
        "/facilities",
        json={
            "facility_code": "FAC-WASTE-002",
            "name": "Second Waste Facility",
            "location": "Patia",
            "city": "Bhubaneswar",
            "state": "Odisha",
            "country": "India",
        },
    )

    second_facility_id = second_facility.json()["data"]["id"]

    response = client.post(
        "/waste",
        json={
            "facility_id": second_facility_id,
            "building_id": building_id,
            "device_id": device_id,
            "waste_type": "SOLID",
            "quantity": 10.0,
            "unit": "kg",
            "recorded_at": "2026-09-29T12:30:00",
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert data["status"] == "ERROR"