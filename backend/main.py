from backend.routers.ai import router as ai_router
from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import settings
from backend.core.database import get_db
from backend.core.exceptions import (
    DatabaseException,
    ResourceConflictException,
    ResourceNotFoundException,
    ResourceValidationException,
)
from backend.core.exception_handlers import (
    database_exception_handler,
    resource_conflict_handler,
    resource_not_found_handler,
    resource_validation_handler,
)

from backend.routers.facility import router as facility_router
from backend.routers.building import router as building_router
from backend.routers.device import router as device_router
from backend.routers.telemetry import router as telemetry_router
from backend.routers.energy import router as energy_router
from backend.routers.water import router as water_router
from backend.routers.waste import router as waste_router
from backend.routers.traffic import router as traffic_router
from backend.routers.air_quality import router as air_quality_router
from backend.routers.asset import router as asset_router
from backend.routers.alert import router as alert_router
from backend.routers.recommendation import router as recommendation_router


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API for EcoFacility AI",
)

# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Exception Handlers
# ============================================================

app.add_exception_handler(
    ResourceNotFoundException,
    resource_not_found_handler,
)

app.add_exception_handler(
    ResourceConflictException,
    resource_conflict_handler,
)

app.add_exception_handler(
    ResourceValidationException,
    resource_validation_handler,
)

app.add_exception_handler(
    DatabaseException,
    database_exception_handler,
)


# ============================================================
# API Routers
# ============================================================

app.include_router(facility_router)
app.include_router(building_router)
app.include_router(device_router)
app.include_router(telemetry_router)
app.include_router(energy_router)
app.include_router(water_router)
app.include_router(waste_router)
app.include_router(traffic_router)
app.include_router(air_quality_router)
app.include_router(asset_router)
app.include_router(alert_router)
app.include_router(recommendation_router)
app.include_router(ai_router)


# ============================================================
# Health Checks
# ============================================================

@app.get("/health")
def health_check():
    return {
        "status": "UP",
        "service": settings.app_name,
        "version": settings.app_version,
    }


@app.get("/health/database")
def database_health(
    db: Session = Depends(get_db),
):
    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "UP",
            "database": "SQLite",
        }

    except Exception as exc:
        raise DatabaseException(
            "Database health check failed"
        ) from exc