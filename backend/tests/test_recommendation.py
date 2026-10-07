def create_test_alert(client):
    facility_response = client.post(
        "/facilities",
        json={
            "facility_code": "FAC-REC-001",
            "name": "Recommendation Test Facility",
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
            "building_code": "BLD-REC-001",
            "facility_id": facility_id,
            "name": "Recommendation Test Building",
            "building_type": "OFFICE",
            "floor_count": 4,
            "area_sq_m": 4000,
        },
    )
    building_id = building_response.json()["data"]["id"]

    device_response = client.post(
        "/devices",
        json={
            "device_code": "DEV-REC-001",
            "building_id": building_id,
            "name": "Recommendation Energy Device",
            "device_type": "ENERGY_METER",
            "category": "ENERGY",
            "unit": "kWh",
        },
    )
    device_id = device_response.json()["data"]["id"]

    alert_response = client.post(
        "/alerts",
        json={
            "facility_id": facility_id,
            "building_id": building_id,
            "device_id": device_id,
            "alert_type": "HIGH_ENERGY_CONSUMPTION",
            "severity": "HIGH",
            "title": "High Energy Consumption",
            "message": "Energy consumption exceeded the configured threshold.",
            "status": "OPEN",
            "detected_at": "2026-09-29T10:00:00",
        },
    )

    alert_id = alert_response.json()["data"]["id"]

    return facility_id, building_id, device_id, alert_id


def create_recommendation(client):
    facility_id, building_id, device_id, alert_id = create_test_alert(client)

    response = client.post(
        "/recommendations",
        json={
            "facility_id": facility_id,
            "building_id": building_id,
            "device_id": device_id,
            "alert_id": alert_id,
            "recommendation_type": "ENERGY_OPTIMIZATION",
            "priority": "HIGH",
            "title": "Optimize Energy Consumption",
            "description": "Reduce HVAC usage during low occupancy periods.",
            "status": "PENDING",
        },
    )

    return response, facility_id, building_id, device_id, alert_id


def test_create_recommendation(client):
    response, _, _, _, _ = create_recommendation(client)

    assert response.status_code == 201

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Recommendation created successfully"
    assert data["data"]["recommendation_type"] == "ENERGY_OPTIMIZATION"
    assert data["data"]["priority"] == "HIGH"
    assert data["data"]["status"] == "PENDING"


def test_get_all_recommendations(client):
    create_recommendation(client)

    response = client.get("/recommendations")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert len(data["data"]) == 1


def test_get_recommendation_by_facility(client):
    _, facility_id, _, _, _ = create_recommendation(client)

    response = client.get(f"/recommendations/facility/{facility_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert len(data["data"]) == 1


def test_get_recommendation_by_alert(client):
    _, _, _, _, alert_id = create_recommendation(client)

    response = client.get(f"/recommendations/alert/{alert_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert len(data["data"]) == 1
    assert data["data"][0]["alert_id"] == alert_id


def test_get_recommendation_by_status(client):
    create_recommendation(client)

    response = client.get("/recommendations/status/PENDING")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert len(data["data"]) == 1
    assert data["data"][0]["status"] == "PENDING"


def test_get_recommendation_by_id(client):
    response, _, _, _, _ = create_recommendation(client)

    recommendation_id = response.json()["data"]["id"]

    response = client.get(f"/recommendations/{recommendation_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["data"]["id"] == recommendation_id


def test_update_recommendation(client):
    response, _, _, _, _ = create_recommendation(client)

    recommendation_id = response.json()["data"]["id"]

    response = client.put(
        f"/recommendations/{recommendation_id}",
        json={
            "priority": "CRITICAL",
            "title": "Critical Energy Optimization",
            "description": "Immediately optimize HVAC and lighting schedules.",
            "status": "IN_PROGRESS",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["data"]["priority"] == "CRITICAL"
    assert data["data"]["status"] == "IN_PROGRESS"


def test_delete_recommendation(client):
    response, _, _, _, _ = create_recommendation(client)

    recommendation_id = response.json()["data"]["id"]

    response = client.delete(
        f"/recommendations/{recommendation_id}"
    )

    assert response.status_code == 204

    response = client.get(
        f"/recommendations/{recommendation_id}"
    )

    assert response.status_code == 404


def test_invalid_recommendation_relationship(client):
    _, building_id, device_id, alert_id = create_test_alert(client)

    second_facility = client.post(
        "/facilities",
        json={
            "facility_code": "FAC-REC-002",
            "name": "Second Recommendation Facility",
            "location": "Patia",
            "city": "Bhubaneswar",
            "state": "Odisha",
            "country": "India",
        },
    )

    second_facility_id = second_facility.json()["data"]["id"]

    response = client.post(
        "/recommendations",
        json={
            "facility_id": second_facility_id,
            "building_id": building_id,
            "device_id": device_id,
            "alert_id": alert_id,
            "recommendation_type": "ENERGY_OPTIMIZATION",
            "priority": "HIGH",
            "title": "Invalid Recommendation",
            "description": "Invalid facility relationship.",
            "status": "PENDING",
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert data["status"] == "ERROR"