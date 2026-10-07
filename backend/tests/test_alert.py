def create_test_device(client):
    facility_response = client.post(
        "/facilities",
        json={
            "facility_code": "FAC-ALERT-001",
            "name": "Alert Test Facility",
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
            "building_code": "BLD-ALERT-001",
            "facility_id": facility_id,
            "name": "Alert Test Building",
            "building_type": "OFFICE",
            "floor_count": 4,
            "area_sq_m": 4000,
        },
    )
    building_id = building_response.json()["data"]["id"]

    device_response = client.post(
        "/devices",
        json={
            "device_code": "DEV-ALERT-001",
            "building_id": building_id,
            "name": "Alert Monitoring Device",
            "device_type": "ENERGY_METER",
            "category": "ENERGY",
            "unit": "kWh",
        },
    )

    device_id = device_response.json()["data"]["id"]

    return facility_id, building_id, device_id


def create_alert(client):
    facility_id, building_id, device_id = create_test_device(client)

    response = client.post(
        "/alerts",
        json={
            "facility_id": facility_id,
            "building_id": building_id,
            "device_id": device_id,
            "alert_type": "HIGH_ENERGY_CONSUMPTION",
            "severity": "HIGH",
            "title": "High Energy Consumption Detected",
            "message": "Energy consumption exceeded the configured threshold.",
            "status": "OPEN",
            "detected_at": "2026-09-29T10:00:00",
        },
    )

    return response, facility_id, building_id, device_id


def test_create_alert(client):
    response, _, _, _ = create_alert(client)

    assert response.status_code == 201

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Alert created successfully"
    assert data["data"]["alert_type"] == "HIGH_ENERGY_CONSUMPTION"
    assert data["data"]["severity"] == "HIGH"
    assert data["data"]["status"] == "OPEN"


def test_get_all_alerts(client):
    create_alert(client)

    response = client.get("/alerts")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert len(data["data"]) == 1


def test_get_alert_by_facility(client):
    _, facility_id, _, _ = create_alert(client)

    response = client.get(f"/alerts/facility/{facility_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert len(data["data"]) == 1
    assert data["data"][0]["alert_type"] == "HIGH_ENERGY_CONSUMPTION"


def test_get_alert_by_status(client):
    create_alert(client)

    response = client.get("/alerts/status/OPEN")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert len(data["data"]) == 1
    assert data["data"][0]["status"] == "OPEN"


def test_get_alert_by_severity(client):
    create_alert(client)

    response = client.get("/alerts/severity/HIGH")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert len(data["data"]) == 1
    assert data["data"][0]["severity"] == "HIGH"


def test_get_alert_by_id(client):
    response, _, _, _ = create_alert(client)

    alert_id = response.json()["data"]["id"]

    response = client.get(f"/alerts/{alert_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["data"]["id"] == alert_id


def test_update_alert(client):
    response, _, _, _ = create_alert(client)

    alert_id = response.json()["data"]["id"]

    response = client.put(
        f"/alerts/{alert_id}",
        json={
            "severity": "CRITICAL",
            "title": "Critical Energy Consumption",
            "message": "Energy consumption is critically high.",
            "status": "OPEN",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["data"]["severity"] == "CRITICAL"
    assert data["data"]["title"] == "Critical Energy Consumption"


def test_invalid_alert_facility(client):
    _, _, building_id, device_id = create_alert(client)

    second_facility = client.post(
        "/facilities",
        json={
            "facility_code": "FAC-ALERT-002",
            "name": "Second Alert Facility",
            "location": "Patia",
            "city": "Bhubaneswar",
            "state": "Odisha",
            "country": "India",
        },
    )

    second_facility_id = second_facility.json()["data"]["id"]

    response = client.post(
        "/alerts",
        json={
            "facility_id": second_facility_id,
            "building_id": building_id,
            "device_id": device_id,
            "alert_type": "HIGH_ENERGY_CONSUMPTION",
            "severity": "HIGH",
            "title": "Invalid Alert",
            "message": "Invalid facility hierarchy.",
            "status": "OPEN",
            "detected_at": "2026-09-29T12:00:00",
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert data["status"] == "ERROR"