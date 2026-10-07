# EcoFacility AI — Backend API Integration Contract

## 1. Overview

EcoFacility AI Backend provides REST APIs for receiving, storing, retrieving, and exposing company-campus facility data.

The backend is responsible for:

- Facility management
- Building management
- Device management
- Telemetry ingestion
- Energy data ingestion
- Water data ingestion
- Waste data ingestion
- Traffic data ingestion
- Air-quality data ingestion
- Asset management
- Alert management
- Recommendation management
- Data validation
- Persistence
- API responses
- Error handling

The backend does NOT perform:

- Machine-learning model training
- Anomaly-detection logic
- Forecasting logic
- IoT simulation
- Dashboard rendering
- Generative-AI reasoning

Those responsibilities belong to the respective project teams.

---

# 2. Base URL

Local development:

```text
http://127.0.0.1:8001

Swagger/OpenAPI documentation:

http://127.0.0.1:8001/docs

OpenAPI schema:

http://127.0.0.1:8001/openapi.json
3. Architecture
                    Virtual Campus
                         │
                         ▼
                  IoT/Data Simulator
                         │
                         │ POST
                         ▼
              ┌─────────────────────┐
              │   FastAPI Backend   │
              └──────────┬──────────┘
                         │
                  Validation Layer
                         │
                         ▼
                     SQLite DB
                         │
              ┌──────────┼──────────┐
              │          │          │
              ▼          ▼          ▼
         Analytics     Alerts    Dashboard
           / AI           │
              │           ▼
              │     Recommendations
              │
              └───────────────► Dashboard
4. Resource Hierarchy

The main resource hierarchy is:

Facility
   │
   └── Building
          │
          └── Device
                 │
                 └── Telemetry

Operational and environmental records are associated with the facility/building/device hierarchy:

Facility
   │
   ├── Energy
   ├── Water
   ├── Waste
   ├── Traffic
   ├── Air Quality
   ├── Assets
   └── Alerts
          │
          └── Recommendations
Relationship rules
Facility

Top-level company-campus entity.

Facility 1 ──────── * Building
Building

A building belongs to exactly one facility.

Building → Facility
Device

A device belongs to exactly one building.

Device → Building
Telemetry

Telemetry belongs to exactly one device.

Telemetry → Device
Assets

Assets belong to a facility and building.

Asset → Facility
Asset → Building
Alerts

An alert belongs to a facility and may optionally reference a building and device.

Alert → Facility
Alert → Building (optional)
Alert → Device (optional)
Recommendations

A recommendation belongs to a facility and may optionally reference a building, device, and alert.

Recommendation → Facility
Recommendation → Building (optional)
Recommendation → Device (optional)
Recommendation → Alert (optional)
5. Common API Response Format

All successful JSON responses follow the common response envelope:

{
  "status": "SUCCESS",
  "message": "Request successful",
  "data": {}
}

For collection responses:

{
  "status": "SUCCESS",
  "message": "Records retrieved successfully",
  "data": []
}
Response fields
Field	Type	Description
status	string	SUCCESS or ERROR
message	string	Human-readable result message
data	object/array/null	Response payload
6. Error Response Format

Errors follow:

{
  "status": "ERROR",
  "message": "Error description"
}
HTTP status codes
HTTP Status	Meaning
200	Successful request
201	Resource created
204	Resource deleted successfully
400	Invalid request or resource relationship
404	Resource not found
409	Resource conflict
500	Database/server error

Consumers should use both:

HTTP status code
+
response.status
7. Identifiers

All primary resource identifiers are UUIDs.

Example:

{
  "id": "9c0ba847-3045-4317-afaf-57d19e21fdbb"
}

Consumers must treat IDs as strings.

Do not assume integer IDs.

8. Date and Time

The API uses ISO-style datetime values.

Example:

2026-09-29T17:15:00

Time-range endpoints use:

/range/{start_time}/{end_time}

The backend validates that:

start_time <= end_time

An invalid range returns:

400 Bad Request
9. Health APIs
GET /health

Checks whether the backend service is running.

Response:

{
  "status": "UP",
  "service": "EcoFacility AI Backend",
  "version": "0.1.0"
}
GET /health/database

Checks database connectivity.

Response:

{
  "status": "UP",
  "database": "SQLite"
}
10. Facility APIs
POST /facilities

Create a facility.

Example request:

{
  "facility_code": "FAC-001",
  "name": "EcoFacility Smart Campus",
  "location": "Infocity",
  "city": "Bhubaneswar",
  "state": "Odisha",
  "country": "India"
}
GET /facilities

Retrieve all facilities.

GET /facilities/{facility_id}

Retrieve a specific facility.

PUT /facilities/{facility_id}

Update a facility.

DELETE /facilities/{facility_id}

Delete a facility.

11. Building APIs
POST /buildings

Create a building.

Example:

{
  "building_code": "BLD-001",
  "facility_id": "FACILITY_UUID",
  "name": "Administration Building",
  "building_type": "OFFICE",
  "floor_count": 4,
  "area_sq_m": 5000
}
GET /buildings

Retrieve all buildings.

GET /buildings/{building_id}

Retrieve a specific building.

GET /buildings/facility/{facility_id}

Retrieve buildings belonging to a facility.

PUT /buildings/{building_id}

Update a building.

DELETE /buildings/{building_id}

Delete a building.

12. Device APIs
POST /devices

Create a device.

Example:

{
  "device_code": "DEV-ENERGY-001",
  "building_id": "BUILDING_UUID",
  "name": "Main Energy Meter",
  "device_type": "ENERGY_METER",
  "category": "ENERGY",
  "unit": "kWh"
}
GET /devices

Retrieve all devices.

GET /devices/{device_id}

Retrieve a specific device.

GET /devices/building/{building_id}

Retrieve devices belonging to a building.

GET /devices/category/{category}

Retrieve devices by category.

PUT /devices/{device_id}

Update a device.

DELETE /devices/{device_id}

Delete a device.

13. Telemetry APIs

Telemetry represents raw device-level measurements.

POST /telemetry

Create telemetry.

Request:

{
  "device_id": "DEVICE_UUID",
  "metric": "power_consumption",
  "value": 47.3,
  "unit": "kWh",
  "timestamp": "2026-09-29T17:15:00"
}

Successful response:

{
  "status": "SUCCESS",
  "message": "Telemetry created successfully",
  "data": {
    "id": "TELEMETRY_UUID",
    "device_id": "DEVICE_UUID",
    "metric": "power_consumption",
    "value": 47.3,
    "unit": "kWh",
    "timestamp": "2026-09-29T17:15:00",
    "created_at": "2026-09-29T18:02:18.990888"
  }
}
GET /telemetry/{telemetry_id}

Retrieve telemetry by ID.

GET /telemetry/device/{device_id}

Retrieve telemetry for a device.

GET /telemetry/metric/{metric}

Retrieve telemetry by metric.

GET /telemetry/range/{start_time}/{end_time}

Retrieve telemetry within a time range.

Telemetry rule

The backend validates that the referenced device exists.

14. Energy APIs
POST /energy

Create an energy record.

{
  "facility_id": "FACILITY_UUID",
  "building_id": "BUILDING_UUID",
  "device_id": "DEVICE_UUID",
  "consumption": 45.8,
  "unit": "kWh",
  "recorded_at": "2026-09-29T16:00:00"
}
GET /energy/{energy_id}

Retrieve energy record by ID.

GET /energy/facility/{facility_id}

Retrieve energy records for a facility.

GET /energy/building/{building_id}

Retrieve energy records for a building.

GET /energy/device/{device_id}

Retrieve energy records for a device.

GET /energy/range/{start_time}/{end_time}

Retrieve energy records within a time range.

Energy validation

When facility, building, and device IDs are supplied together:

Facility
   ↓
Building
   ↓
Device

must be a valid hierarchy.

15. Water APIs
POST /water

Create a water record.

{
  "facility_id": "FACILITY_UUID",
  "building_id": "BUILDING_UUID",
  "device_id": "DEVICE_UUID",
  "consumption": 138.7,
  "unit": "L",
  "recorded_at": "2026-09-29T16:15:00"
}
GET /water/{water_id}

Retrieve water record by ID.

GET /water/facility/{facility_id}

Retrieve water records for a facility.

GET /water/building/{building_id}

Retrieve water records for a building.

GET /water/device/{device_id}

Retrieve water records for a device.

GET /water/range/{start_time}/{end_time}

Retrieve water records within a time range.

16. Waste APIs
POST /waste

Create a waste record.

{
  "facility_id": "FACILITY_UUID",
  "building_id": "BUILDING_UUID",
  "device_id": "DEVICE_UUID",
  "waste_type": "SOLID",
  "quantity": 21.4,
  "unit": "kg",
  "recorded_at": "2026-09-29T16:30:00"
}
GET /waste/{waste_id}

Retrieve waste record by ID.

GET /waste/facility/{facility_id}

Retrieve waste records for a facility.

GET /waste/building/{building_id}

Retrieve waste records for a building.

GET /waste/device/{device_id}

Retrieve waste records for a device.

GET /waste/type/{waste_type}

Retrieve waste records by waste type.

GET /waste/range/{start_time}/{end_time}

Retrieve waste records within a time range.

17. Traffic APIs
POST /traffic

Create a traffic record.

{
  "facility_id": "FACILITY_UUID",
  "building_id": "BUILDING_UUID",
  "device_id": "DEVICE_UUID",
  "vehicle_count": 48,
  "parking_occupancy": 72.5,
  "average_speed": 22.8,
  "recorded_at": "2026-09-29T16:45:00"
}

average_speed may be omitted when unavailable.

GET /traffic/{traffic_id}

Retrieve traffic record by ID.

GET /traffic/facility/{facility_id}

Retrieve traffic records for a facility.

GET /traffic/building/{building_id}

Retrieve traffic records for a building.

GET /traffic/device/{device_id}

Retrieve traffic records for a device.

GET /traffic/range/{start_time}/{end_time}

Retrieve traffic records within a time range.

18. Air Quality APIs
POST /air-quality

Create an air-quality record.

{
  "facility_id": "FACILITY_UUID",
  "building_id": "BUILDING_UUID",
  "device_id": "DEVICE_UUID",
  "pm25": 29.8,
  "pm10": 54.6,
  "co2": 705.0,
  "temperature": 27.1,
  "humidity": 60.2,
  "aqi": 72.0,
  "recorded_at": "2026-09-29T17:00:00"
}

The individual air-quality measurements may be nullable when a source does not provide them.

GET /air-quality/{air_quality_id}

Retrieve air-quality record by ID.

GET /air-quality/facility/{facility_id}

Retrieve air-quality records for a facility.

GET /air-quality/building/{building_id}

Retrieve air-quality records for a building.

GET /air-quality/device/{device_id}

Retrieve air-quality records for a device.

GET /air-quality/range/{start_time}/{end_time}

Retrieve air-quality records within a time range.

19. Asset APIs
POST /assets

Create an asset.

Example:

{
  "facility_id": "FACILITY_UUID",
  "building_id": "BUILDING_UUID",
  "asset_code": "AST-HVAC-001",
  "name": "Central HVAC System",
  "asset_type": "HVAC",
  "status": "ACTIVE",
  "manufacturer": "Daikin",
  "model_number": "HVAC-X500",
  "installed_at": "2025-06-15"
}
GET /assets

Retrieve all assets.

GET /assets/{asset_id}

Retrieve asset by ID.

GET /assets/facility/{facility_id}

Retrieve assets by facility.

GET /assets/building/{building_id}

Retrieve assets by building.

GET /assets/type/{asset_type}

Retrieve assets by type.

PUT /assets/{asset_id}

Update an asset.

DELETE /assets/{asset_id}

Delete an asset.

20. Alert APIs

Alerts represent detected operational conditions.

POST /alerts

Create an alert.

Example:

{
  "facility_id": "FACILITY_UUID",
  "building_id": "BUILDING_UUID",
  "device_id": "DEVICE_UUID",
  "alert_type": "HIGH_ENERGY_CONSUMPTION",
  "severity": "HIGH",
  "title": "High Energy Consumption Detected",
  "message": "Energy consumption exceeded the configured threshold.",
  "status": "OPEN",
  "detected_at": "2026-09-29T17:30:00"
}
GET /alerts

Retrieve all alerts.

GET /alerts/{alert_id}

Retrieve alert by ID.

GET /alerts/facility/{facility_id}

Retrieve alerts for a facility.

GET /alerts/status/{status}

Retrieve alerts by status.

GET /alerts/severity/{severity}

Retrieve alerts by severity.

PUT /alerts/{alert_id}

Update an alert.

21. Recommendation APIs

Recommendations represent actions or suggestions associated with operational conditions.

POST /recommendations

Create a recommendation.

Example:

{
  "facility_id": "FACILITY_UUID",
  "building_id": "BUILDING_UUID",
  "device_id": "DEVICE_UUID",
  "alert_id": "ALERT_UUID",
  "recommendation_type": "ENERGY_OPTIMIZATION",
  "priority": "HIGH",
  "title": "Optimize Energy Consumption",
  "description": "Reduce HVAC usage during low occupancy periods.",
  "status": "PENDING"
}
GET /recommendations

Retrieve all recommendations.

GET /recommendations/{recommendation_id}

Retrieve recommendation by ID.

GET /recommendations/facility/{facility_id}

Retrieve recommendations for a facility.

GET /recommendations/alert/{alert_id}

Retrieve recommendations associated with an alert.

GET /recommendations/status/{status}

Retrieve recommendations by status.

PUT /recommendations/{recommendation_id}

Update a recommendation.

DELETE /recommendations/{recommendation_id}

Delete a recommendation.

22. Data Flow

The intended integration flow is:

                VIRTUAL CAMPUS
                     │
                     ▼
              IoT / Simulator
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
      Telemetry             Measurements
          │                     │
          └──────────┬──────────┘
                     ▼
              FastAPI Backend
                     │
                Validation
                     │
                     ▼
                  SQLite
                     │
          ┌──────────┼──────────┐
          │          │          │
          ▼          ▼          ▼
      Analytics    Alerts    Dashboard
          │          │
          │          ▼
          │    Recommendations
          │          │
          └──────────┴──────► Dashboard
23. Simulator Integration

The simulator is responsible for generating virtual-campus measurements.

The simulator should primarily use:

POST /telemetry
POST /energy
POST /water
POST /waste
POST /traffic
POST /air-quality

The simulator should provide valid:

facility_id
building_id
device_id
timestamp / recorded_at
measurement values

The backend is responsible for:

Validation
Persistence
UUID generation
Response generation
Error handling

The backend does not generate simulated sensor values.

24. Analytics / AI Integration

The Analytics/AI team consumes historical data through GET APIs.

Examples:

GET /telemetry/device/{device_id}

GET /telemetry/range/{start_time}/{end_time}

GET /energy/facility/{facility_id}

GET /water/facility/{facility_id}

GET /waste/facility/{facility_id}

GET /traffic/facility/{facility_id}

GET /air-quality/facility/{facility_id}

The Analytics/AI layer can process these datasets for:

Anomaly detection
Forecasting
Pattern analysis
Prediction
Sustainability analysis

The backend itself does not perform those analytics.

25. Alert and Recommendation Flow

The intended conceptual flow is:

Raw Data
   │
   ▼
Analytics / AI
   │
   ▼
Detected Condition
   │
   ▼
Alert
   │
   ▼
Recommendation

Example:

Energy measurements
        │
        ▼
Analytics / AI
        │
        ▼
High energy consumption detected
        │
        ▼
POST /alerts
        │
        ▼
Alert stored
        │
        ▼
Recommendation generated
        │
        ▼
POST /recommendations

The backend provides persistence and APIs for these objects.

26. Dashboard Integration

The Dashboard team primarily consumes GET APIs.

Typical dashboard requests include:

GET /facilities

GET /buildings/facility/{facility_id}

GET /devices/building/{building_id}

GET /energy/facility/{facility_id}

GET /water/facility/{facility_id}

GET /waste/facility/{facility_id}

GET /traffic/facility/{facility_id}

GET /air-quality/facility/{facility_id}

GET /alerts/facility/{facility_id}

GET /recommendations/facility/{facility_id}

For historical charts:

GET /energy/range/{start_time}/{end_time}

GET /water/range/{start_time}/{end_time}

GET /waste/range/{start_time}/{end_time}

GET /traffic/range/{start_time}/{end_time}

GET /air-quality/range/{start_time}/{end_time}

GET /telemetry/range/{start_time}/{end_time}
27. Validation Rules

The backend validates resource relationships before persistence.

Examples:

Building must belong to the specified Facility.

Device must belong to the specified Building.

Energy must reference a valid
Facility → Building → Device hierarchy.

Water must reference a valid
Facility → Building → Device hierarchy.

Waste must reference a valid
Facility → Building → Device hierarchy.

Traffic must reference a valid
Facility → Building → Device hierarchy.

Air Quality must reference a valid
Facility → Building → Device hierarchy.

Asset must reference a valid Facility → Building relationship.

Alert must reference a valid Facility and optional valid Building/Device.

Recommendation must reference a valid Facility and optional valid
Building/Device/Alert.

Invalid relationships return:

400 Bad Request

Missing resources return:

404 Not Found
28. Historical Data

The following are treated as historical measurement records:

Telemetry
Energy
Water
Waste
Traffic
Air Quality

These records are created through POST requests and queried through GET requests.

They are not intended to be modified through normal update APIs.

29. Delete Behavior

DELETE endpoints return:

204 No Content

No JSON response body should be expected after successful deletion.

Example:

DELETE /assets/{asset_id}

Response:

204 No Content
30. API Testing

The backend currently contains automated API tests covering:

Health
Facilities
Buildings
Devices
Telemetry
Energy
Water
Waste
Traffic
Air Quality
Assets
Alerts
Recommendations

Current verification:

90 tests passed
0 tests failed

The automated test suite should be executed before integration changes are merged.

Command:

pytest -v
31. Database Migration Verification

The backend uses Alembic for database migrations.

Check migration consistency:

alembic check

Expected:

No new upgrade operations detected.

Check current migration:

alembic current

Current migration:

176710129d5a (head)
32. Integration Checklist
Simulator Team
 Obtain facility ID
 Obtain building IDs
 Obtain device IDs
 Generate virtual sensor data
 Send telemetry
 Send energy measurements
 Send water measurements
 Send waste measurements
 Send traffic measurements
 Send air-quality measurements
 Handle API errors
 Respect timestamp fields
Analytics / AI Team
 Retrieve historical telemetry
 Retrieve energy data
 Retrieve water data
 Retrieve waste data
 Retrieve traffic data
 Retrieve air-quality data
 Perform analytics/model processing
 Create alerts through the backend API
 Create recommendations through the backend API
Dashboard Team
 Retrieve facility information
 Retrieve buildings
 Retrieve devices
 Retrieve measurements
 Retrieve alerts
 Retrieve recommendations
 Use time-range APIs for historical charts
 Handle API errors
 Respect common response format
33. Backend Responsibility Boundary

The EcoFacility AI backend owns:

API
│
├── Validation
├── Persistence
├── Data retrieval
├── Resource relationships
├── Error handling
├── Alerts persistence
├── Recommendations persistence
├── Database migrations
└── Integration contracts

Other project components own:

Simulator
├── Virtual sensor generation
└── Scenario simulation

Analytics / AI
├── Anomaly detection
├── Forecasting
├── Prediction
└── Model processing

Dashboard
├── Visualization
├── Charts
├── Maps
└── User interface

GenAI
└── Natural-language explanation / assistant

This separation keeps the backend modular and allows each team to work independently against the API contract.

34. Quick API Reference
Module	Create	Main Retrieval
Facility	POST /facilities	/facilities
Building	POST /buildings	/buildings
Device	POST /devices	/devices
Telemetry	POST /telemetry	/telemetry/...
Energy	POST /energy	/energy/...
Water	POST /water	/water/...
Waste	POST /waste	/waste/...
Traffic	POST /traffic	/traffic/...
Air Quality	POST /air-quality	/air-quality/...
Asset	POST /assets	/assets/...
Alert	POST /alerts	/alerts/...
Recommendation	POST /recommendations	/recommendations/...
35. Development Server

Start the backend with:

uvicorn backend.main:app --reload --port 8001

Swagger:

http://127.0.0.1:8001/docs
36. Final Integration Principle

The backend acts as the central data and API layer:

             SIMULATOR
                 │
                 ▼
          ┌─────────────┐
          │   BACKEND   │
          │             │
          │ Validate    │
          │ Store       │
          │ Retrieve    │
          │ Expose API  │
          └──────┬──────┘
                 │
        ┌────────┼────────┐
        ▼        ▼        ▼
    ANALYTICS  ALERTS  DASHBOARD
        │        │
        │        ▼
        │   RECOMMENDATIONS
        │
        └──────────────► DASHBOARD