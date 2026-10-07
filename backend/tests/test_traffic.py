def create_test_device(client):
    facility_response = client.post(
        "/facilities",
        json={
            "facility_code": "FAC-TRAFFIC-001",
            "name": "Traffic Test Facility",
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
            "building_code": "BLD-TRAFFIC-001",
            "facility_id": facility_id,
            "name": "Traffic Test Building",
            "building_type": "OFFICE",
            "floor_count": 4,
            "area_sq_m": 4000,
        },
    )
    building_id = building_response.json()["data"]["id"]

    device_response = client.post(
        "/devices",
        json={
            "device_code": "DEV-TRAFFIC-001",
            "building_id": building_id,
            "name": "Traffic Monitoring Device",
            "device_type": "TRAFFIC_SENSOR",
            "category": "TRAFFIC",
            "unit": "vehicles",
        },
    )

    return facility_id, building_id, device_response.json()["data"]["id"]


def create_traffic(client):
    facility_id, building_id, device_id = create_test_device(client)

    response = client.post(
        "/traffic",
        json={
            "facility_id": facility_id,
            "building_id": building_id,
            "device_id": device_id,
            "vehicle_count": 48,
            "parking_occupancy": 72.5,
            "average_speed": 22.8,
            "recorded_at": "2026-09-29T10:00:00",
        },
    )

    return response, facility_id, building_id, device_id


def test_create_traffic(client):
    response, _, _, _ = create_traffic(client)

    assert response.status_code == 201

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Traffic record created successfully"
    assert data["data"]["vehicle_count"] == 48
    assert data["data"]["parking_occupancy"] == 72.5
    assert data["data"]["average_speed"] == 22.8


def test_get_traffic_by_facility(client):
    _, facility_id, _, _ = create_traffic(client)

    response = client.get(f"/traffic/facility/{facility_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert len(data["data"]) == 1
    assert data["data"][0]["vehicle_count"] == 48


def test_get_traffic_by_building(client):
    _, _, building_id, _ = create_traffic(client)

    response = client.get(f"/traffic/building/{building_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert len(data["data"]) == 1


def test_get_traffic_by_device(client):
    _, _, _, device_id = create_traffic(client)

    response = client.get(f"/traffic/device/{device_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert len(data["data"]) == 1


def test_get_traffic_by_time_range(client):
    create_traffic(client)

    response = client.get(
        "/traffic/range/2026-09-29T09:00:00/2026-09-29T11:00:00"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert len(data["data"]) == 1


def test_get_traffic_by_id(client):
    response, _, _, _ = create_traffic(client)

    traffic_id = response.json()["data"]["id"]

    response = client.get(f"/traffic/{traffic_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["data"]["id"] == traffic_id


def test_invalid_traffic_time_range(client):
    response = client.get(
        "/traffic/range/2026-09-29T11:00:00/2026-09-29T09:00:00"
    )

    assert response.status_code == 400

    data = response.json()

    assert data["status"] == "ERROR"


def test_invalid_traffic_hierarchy(client):
    _, facility_id, building_id, device_id = create_traffic(client)

    second_facility = client.post(
        "/facilities",
        json={
            "facility_code": "FAC-TRAFFIC-002",
            "name": "Second Traffic Facility",
            "location": "Patia",
            "city": "Bhubaneswar",
            "state": "Odisha",
            "country": "India",
        },
    )

    second_facility_id = second_facility.json()["data"]["id"]

    response = client.post(
        "/traffic",
        json={
            "facility_id": second_facility_id,
            "building_id": building_id,
            "device_id": device_id,
            "vehicle_count": 30,
            "parking_occupancy": 50.0,
            "average_speed": 25.0,
            "recorded_at": "2026-09-29T12:00:00",
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert data["status"] == "ERROR"