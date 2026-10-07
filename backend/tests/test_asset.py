def create_test_building(client):
    facility_response = client.post(
        "/facilities",
        json={
            "facility_code": "FAC-ASSET-001",
            "name": "Asset Test Facility",
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
            "building_code": "BLD-ASSET-001",
            "facility_id": facility_id,
            "name": "Asset Test Building",
            "building_type": "OFFICE",
            "floor_count": 4,
            "area_sq_m": 4000,
        },
    )

    building_id = building_response.json()["data"]["id"]

    return facility_id, building_id


def create_asset(client):
    facility_id, building_id = create_test_building(client)

    response = client.post(
        "/assets",
        json={
            "facility_id": facility_id,
            "building_id": building_id,
            "asset_code": "AST-TEST-001",
            "name": "Central HVAC System",
            "asset_type": "HVAC",
            "status": "ACTIVE",
            "manufacturer": "Daikin",
            "model_number": "HVAC-X500",
            "installed_at": "2026-01-15",
        },
    )

    return response, facility_id, building_id


def test_create_asset(client):
    response, _, _ = create_asset(client)

    assert response.status_code == 201

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["message"] == "Asset created successfully"
    assert data["data"]["asset_code"] == "AST-TEST-001"
    assert data["data"]["name"] == "Central HVAC System"
    assert data["data"]["asset_type"] == "HVAC"


def test_get_all_assets(client):
    create_asset(client)

    response = client.get("/assets")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert len(data["data"]) == 1


def test_get_asset_by_facility(client):
    _, facility_id, _ = create_asset(client)

    response = client.get(f"/assets/facility/{facility_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert len(data["data"]) == 1


def test_get_asset_by_building(client):
    _, _, building_id = create_asset(client)

    response = client.get(f"/assets/building/{building_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert len(data["data"]) == 1


def test_get_asset_by_type(client):
    create_asset(client)

    response = client.get("/assets/type/HVAC")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert len(data["data"]) == 1
    assert data["data"][0]["asset_type"] == "HVAC"


def test_get_asset_by_id(client):
    response, _, _ = create_asset(client)

    asset_id = response.json()["data"]["id"]

    response = client.get(f"/assets/{asset_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["data"]["id"] == asset_id


def test_update_asset(client):
    response, _, _ = create_asset(client)

    asset_id = response.json()["data"]["id"]

    response = client.put(
        f"/assets/{asset_id}",
        json={
            "name": "Updated HVAC System",
            "status": "MAINTENANCE",
            "manufacturer": "Daikin",
            "model_number": "HVAC-X500",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["data"]["name"] == "Updated HVAC System"
    assert data["data"]["status"] == "MAINTENANCE"


def test_delete_asset(client):
    response, _, _ = create_asset(client)

    asset_id = response.json()["data"]["id"]

    response = client.delete(f"/assets/{asset_id}")

    assert response.status_code == 204

    response = client.get(f"/assets/{asset_id}")

    assert response.status_code == 404


def test_invalid_asset_building(client):
    facility_id, building_id = create_test_building(client)

    second_facility = client.post(
        "/facilities",
        json={
            "facility_code": "FAC-ASSET-002",
            "name": "Second Asset Facility",
            "location": "Patia",
            "city": "Bhubaneswar",
            "state": "Odisha",
            "country": "India",
        },
    )

    second_facility_id = second_facility.json()["data"]["id"]

    response = client.post(
        "/assets",
        json={
            "facility_id": second_facility_id,
            "building_id": building_id,
            "asset_code": "AST-INVALID-001",
            "name": "Invalid Asset",
            "asset_type": "HVAC",
            "status": "ACTIVE",
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert data["status"] == "ERROR"