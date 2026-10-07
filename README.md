# EcoFacility AI — Backend

## 1. Project Overview

EcoFacility AI is a sustainable facility and estate intelligence platform designed for a company campus environment.

The backend provides the central API and data layer for the system.

It is responsible for:

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
- Resource validation
- Database persistence
- REST APIs
- Error handling
- Database migrations
- Integration contracts

The backend provides APIs for the Virtual Campus Simulator, Analytics/AI layer, and Dashboard.

---

# 2. Backend Responsibility

The backend acts as the central integration layer:

```text
Virtual Campus / IoT Simulator
             │
             ▼
      ┌──────────────┐
      │   FastAPI    │
      │   Backend    │
      └──────┬───────┘
             │
       Validation
             │
             ▼
         SQLite DB
             │
      ┌──────┼──────┐
      ▼      ▼      ▼
 Analytics Alerts Dashboard
    / AI       │
               ▼
        Recommendations

```
## The backend does NOT own:

Machine-learning model training
Anomaly-detection algorithms
Forecasting algorithms
IoT simulation
Dashboard UI
Generative-AI reasoning

Those responsibilities belong to their respective teams.

## 3. Technology Stack
Technology	Version / Purpose
Python	3.12.5
FastAPI	0.141.1
Uvicorn	0.52.4
SQLAlchemy	2.1.1
Alembic	1.20.0
SQLite	Development database
Pydantic	2.13.5
Pydantic Settings	2.15.0
python-dotenv	1.2.3
pytest	9.1.1
HTTPX	0.28.1

Dependencies are defined in:

requirements.txt
## 4. Project Structure
```
ecofacilityAI/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── exceptions.py
│   │   └── exception_handlers.py
│   │
│   ├── models/
│   │   ├── facility.py
│   │   ├── building.py
│   │   ├── device.py
│   │   ├── telemetry.py
│   │   ├── energy.py
│   │   ├── water.py
│   │   ├── waste.py
│   │   ├── traffic.py
│   │   ├── air_quality.py
│   │   ├── asset.py
│   │   ├── alert.py
│   │   └── recommendation.py
│   │
│   ├── routers/
│   │   ├── facility.py
│   │   ├── building.py
│   │   ├── device.py
│   │   ├── telemetry.py
│   │   ├── energy.py
│   │   ├── water.py
│   │   ├── waste.py
│   │   ├── traffic.py
│   │   ├── air_quality.py
│   │   ├── asset.py
│   │   ├── alert.py
│   │   └── recommendation.py
│   │
│   ├── schemas/
│   │   ├── common.py
│   │   ├── facility.py
│   │   ├── building.py
│   │   ├── device.py
│   │   ├── telemetry.py
│   │   ├── energy.py
│   │   ├── water.py
│   │   ├── waste.py
│   │   ├── traffic.py
│   │   ├── air_quality.py
│   │   ├── asset.py
│   │   ├── alert.py
│   │   └── recommendation.py
│   │
│   ├── services/
│   │   ├── facility_service.py
│   │   ├── building_service.py
│   │   ├── device_service.py
│   │   ├── telemetry_service.py
│   │   ├── energy_service.py
│   │   ├── water_service.py
│   │   ├── waste_service.py
│   │   ├── traffic_service.py
│   │   ├── air_quality_service.py
│   │   ├── asset_service.py
│   │   ├── alert_service.py
│   │   └── recommendation_service.py
│   │
│   ├── integrations/
│   │   ├── __init__.py
│   │   └── API_INTEGRATION.md
│   │
│   ├── storage/
│   │   └── ecofacility.db
│   │
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_health.py
│   │   ├── test_facility.py
│   │   ├── test_building.py
│   │   ├── test_device.py
│   │   ├── test_telemetry.py
│   │   ├── test_energy.py
│   │   ├── test_water.py
│   │   ├── test_waste.py
│   │   ├── test_traffic.py
│   │   ├── test_air_quality.py
│   │   ├── test_asset.py
│   │   ├── test_alert.py
│   │   └── test_recommendation.py
│   │
│   └── utils/
│       └── resource_validator.py
│
├── migrations/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│
├── alembic.ini
├── requirements.txt
├── .env.example
└── README.md
```
## 5. Prerequisites

Install:

        Python 3.12+
        pip

Verify Python:

    python --version

Expected development version:

    Python 3.12.5

Verify pip:

        pip --version
## 6. Installation

Clone the repository and enter the project directory.

Example:

    cd D:\Project\ecofacilityAI

Install dependencies:

    pip install -r requirements.txt
## 7. Configuration

The backend uses Pydantic Settings.

Example configuration is provided in:

.env.example

Current example:

APP_NAME=EcoFacility AI Backend
APP_VERSION=0.1.0
DEBUG=true
DATABASE_URL=sqlite:///./backend/storage/ecofacility.db

For local development, the application has default values, so a .env file is not required when using the default configuration.

Do not commit a real .env file containing environment-specific or secret values.

## 8. Database

The development database is SQLite.

Database location:

backend/storage/ecofacility.db

The backend uses:

SQLAlchemy for ORM/database access
Alembic for migrations

SQLite foreign-key enforcement is enabled by the backend database configuration.

## 9. Database Migrations

Check migration status:

alembic current

Check whether model changes require a new migration:

alembic check

Apply migrations:

alembic upgrade head

Create a new migration after an intentional model change:

alembic revision --autogenerate -m "describe change"

Then review the generated migration before applying it.

## 10. Run the Backend

From the project root:

uvicorn backend.main:app --reload --port 8001

The backend will be available at:

http://127.0.0.1:8001
## 11. Swagger / OpenAPI

Interactive API documentation:

http://127.0.0.1:8001/docs

OpenAPI specification:

http://127.0.0.1:8001/openapi.json

Swagger can be used by developers to understand and manually exercise the API when required.

The authoritative integration contract is:

backend/integrations/API_INTEGRATION.md
## 12. Health Checks

Application health:

GET /health

Database health:

GET /health/database

Example application response:

{
  "status": "UP",
  "service": "EcoFacility AI Backend",
  "version": "0.1.0"
}
## 13. API Modules

The backend currently exposes these modules:

       1.Facilities
       2. Buildings
       3. Devices
       4. Telemetry
       5. Energy
       6. Water
       7. Waste
       8. Traffic
       9. Air Quality
       10. Assets
       11. Alerts
       12. Recommendations

Detailed API integration information is available in:

backend/integrations/API_INTEGRATION.md
## 14. Resource Hierarchy

The core hierarchy is:
````

Facility
   │
   └── Building
          │
          └── Device
                 │
                 └── Telemetry

Operational records use the facility/building/device hierarchy where applicable:

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
          
````          

The backend validates resource relationships before persistence.

## 15. API Response Format

Successful JSON responses follow:

{
  "status": "SUCCESS",
  "message": "Request successful",
  "data": {}
}

Error responses follow:

{
  "status": "ERROR",
  "message": "Error description"
}

Common HTTP statuses:

200  Successful request
201  Resource created
204  Resource deleted
400  Invalid request / relationship
404  Resource not found
409  Resource conflict
500  Database/server error
16. Testing

The backend uses pytest.

Run the complete test suite:

pytest -v

Current verified result:

90 passed
0 failed

The automated tests cover:

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

Tests use an isolated test database so the production/development SQLite database is not used by the test suite.

## 17. Test Database

The test suite uses an isolated in-memory SQLite database.

This prevents automated tests from modifying:

backend/storage/ecofacility.db

Each test database is created and cleaned up as part of the test fixture lifecycle.

## 18. Integration With the Simulator

The Virtual Campus Simulator is responsible for generating simulated measurements.

The simulator can send data through:

POST /telemetry
POST /energy
POST /water
POST /waste
POST /traffic
POST /air-quality

The simulator must provide valid resource identifiers and measurement data.

The backend handles:

Validation
Persistence
UUID generation
Response generation
Error handling

The backend does not generate simulated sensor values.

## 19. Integration With Analytics / AI

The Analytics/AI layer consumes backend data through GET APIs.

Examples:

GET /telemetry/device/{device_id}

GET /telemetry/range/{start_time}/{end_time}

GET /energy/facility/{facility_id}

GET /water/facility/{facility_id}

GET /waste/facility/{facility_id}

GET /traffic/facility/{facility_id}

GET /air-quality/facility/{facility_id}

The Analytics/AI team owns:

Anomaly detection
Forecasting
Prediction
Pattern analysis
Model processing

The backend provides the data-access layer for these operations.

## 20. Alerts and Recommendations

The conceptual flow is:

Measurements
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

Alerts and recommendations are persisted through backend APIs.

The backend provides storage and retrieval APIs; it does not own the underlying ML/anomaly-detection logic.

## 21. Dashboard Integration

The Dashboard consumes backend GET APIs.

Typical requests include:

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

For historical data:

GET /energy/range/{start_time}/{end_time}

GET /water/range/{start_time}/{end_time}

GET /waste/range/{start_time}/{end_time}

GET /traffic/range/{start_time}/{end_time}

GET /air-quality/range/{start_time}/{end_time}

GET /telemetry/range/{start_time}/{end_time}
## 22. Error Handling

The backend uses centralized application exceptions.

Main application exception categories include:

ResourceNotFoundException
ResourceConflictException
ResourceValidationException
DatabaseException

The API converts these exceptions into consistent HTTP responses.

Example:

{
  "status": "ERROR",
  "message": "Building does not belong to the specified facility"
}
## 23. Resource Validation

The backend validates relationships such as:

Facility
   ↓
Building
   ↓
Device

For example:

    A building must belong to the specified facility.
    A device must belong to the specified building.
    Energy data must reference a valid facility/building/device hierarchy.
    Water data must reference a valid hierarchy.
    Waste data must reference a valid hierarchy.
    Traffic data must reference a valid hierarchy.
    Air-quality data must reference a valid hierarchy.
    Assets must reference a valid facility/building relationship.
    Alerts must reference valid resources.
    Recommendations must reference valid resources.

Invalid relationships return:

400 Bad Request

Missing resources return:

404 Not Found
## 24. Historical Data

The following are treated as historical measurement records:

Telemetry
Energy
Water
Waste
Traffic
Air Quality

These records are created through POST APIs and retrieved through GET APIs.

They are not intended to have normal update/delete workflows.

## 25. Development Workflow

Recommended backend workflow:
````
1. Create / modify model
        ↓
2. Update schema
        ↓
3. Update service
        ↓
4. Update router
        ↓
5. Create/update migration
        ↓
6. Add automated tests
        ↓
7. Run pytest
        ↓
8. Run alembic check
        ↓
9. Verify Swagger
        ↓
10. Update API documentation
````

Do not skip database migration review when changing persistent models.

## 26. Verification Before Integration

Before handing a backend change to another team:

Run:

pytest -v

Expected:

90 passed

Then:

alembic check

Expected:

No new upgrade operations detected.

Then verify:

alembic current

The current migration should be at the expected head revision.

## 27. Integration Documentation

The complete API integration contract is located at:

backend/integrations/API_INTEGRATION.md

That document should be used by:

Simulator team
Analytics/AI team
Dashboard team
Backend developers
Integration/testing team
## 28. Team Responsibility
Backend

Owns:

FastAPI
REST APIs
Database
SQLAlchemy models
Pydantic schemas
Services
Validation
Exception handling
Migrations
API documentation
Automated API tests
Integration contracts
Simulator

Owns:

Virtual campus
Sensor simulation
Scenario simulation
Measurement generation
Analytics / AI

Owns:

Data analysis
Anomaly detection
Forecasting
Prediction
ML models
Dashboard

Owns:

UI
Charts
Visualization
Maps
Dashboard interaction
GenAI

Owns:

Natural-language explanations
AI assistant functionality
Conversational interaction
## 29. Current Backend Status

The backend currently has:
``````

REST API                         ✅
SQLite persistence               ✅
SQLAlchemy ORM                   ✅
Alembic migrations               ✅
Pydantic schemas                 ✅
Resource validation              ✅
Central exception handling       ✅
API response standardization    ✅
Swagger/OpenAPI                  ✅
Automated tests                  ✅
API integration contract         ✅
Environment configuration        ✅
Requirements file                ✅
``````

Automated test verification:

90 passed
0 failed

Migration verification:

No new upgrade operations detected.
## 30. Quick Start

For a new developer:

Step 1 — Enter project
cd D:\Project\ecofacilityAI
Step 2 — Install dependencies
pip install -r requirements.txt
Step 3 — Check migrations
alembic check
Step 4 — Apply migrations
alembic upgrade head
Step 5 — Run backend
uvicorn backend.main:app --reload --port 8001
Step 6 — Open Swagger
http://127.0.0.1:8001/docs
Step 7 — Run tests

Stop the development server if necessary, then run:

pytest -v

Expected:

90 passed
## 31. Final Architecture
                         ECOFACILITY AI
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
          Virtual Campus                 Backend API
           / Simulator                      │
                 │                           │
                 │                    ┌──────┴──────┐
                 │                    │             │
                 └──────────────►  FastAPI       SQLite
                                      │
                           ┌──────────┼──────────┐
                           │          │          │
                           ▼          ▼          ▼
                       Analytics    Alerts    Dashboard
                         / AI          │
                           │          ▼
                           │    Recommendations
                           │
                           └──────────────► Dashboard#   e c o f a c i l i t y A I  
 