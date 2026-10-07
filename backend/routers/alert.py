from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.core.exceptions import ResourceNotFoundException
from backend.schemas.alert import (
    AlertCreate,
    AlertResponse,
    AlertUpdate,
)
from backend.schemas.common import ApiResponse
from backend.services.alert_service import AlertService


router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"],
)


@router.post(
    "",
    response_model=ApiResponse[AlertResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_alert(
    data: AlertCreate,
    db: Session = Depends(get_db),
):
    alert = AlertService.create(db, data)

    return ApiResponse(
        status="SUCCESS",
        message="Alert created successfully",
        data=alert,
    )


@router.get(
    "",
    response_model=ApiResponse[list[AlertResponse]],
)
def get_alerts(
    db: Session = Depends(get_db),
):
    alerts = AlertService.get_all(db)

    return ApiResponse(
        status="SUCCESS",
        message="Alerts retrieved successfully",
        data=alerts,
    )


@router.get(
    "/facility/{facility_id}",
    response_model=ApiResponse[list[AlertResponse]],
)
def get_alerts_by_facility(
    facility_id: UUID,
    db: Session = Depends(get_db),
):
    alerts = AlertService.get_by_facility(db, facility_id)

    return ApiResponse(
        status="SUCCESS",
        message="Alerts retrieved successfully",
        data=alerts,
    )


@router.get(
    "/status/{alert_status}",
    response_model=ApiResponse[list[AlertResponse]],
)
def get_alerts_by_status(
    alert_status: str,
    db: Session = Depends(get_db),
):
    alerts = AlertService.get_by_status(db, alert_status)

    return ApiResponse(
        status="SUCCESS",
        message="Alerts retrieved successfully",
        data=alerts,
    )


@router.get(
    "/severity/{severity}",
    response_model=ApiResponse[list[AlertResponse]],
)
def get_alerts_by_severity(
    severity: str,
    db: Session = Depends(get_db),
):
    alerts = AlertService.get_by_severity(db, severity)

    return ApiResponse(
        status="SUCCESS",
        message="Alerts retrieved successfully",
        data=alerts,
    )


@router.get(
    "/{alert_id}",
    response_model=ApiResponse[AlertResponse],
)
def get_alert(
    alert_id: UUID,
    db: Session = Depends(get_db),
):
    alert = AlertService.get_by_id(db, alert_id)

    if alert is None:
        raise ResourceNotFoundException(
            f"Alert not found: {alert_id}"
        )

    return ApiResponse(
        status="SUCCESS",
        message="Alert retrieved successfully",
        data=alert,
    )


@router.put(
    "/{alert_id}",
    response_model=ApiResponse[AlertResponse],
)
def update_alert(
    alert_id: UUID,
    data: AlertUpdate,
    db: Session = Depends(get_db),
):
    alert = AlertService.get_by_id(db, alert_id)

    if alert is None:
        raise ResourceNotFoundException(
            f"Alert not found: {alert_id}"
        )

    updated_alert = AlertService.update(db, alert, data)

    return ApiResponse(
        status="SUCCESS",
        message="Alert updated successfully",
        data=updated_alert,
    )