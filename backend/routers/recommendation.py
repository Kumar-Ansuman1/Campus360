from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.core.exceptions import ResourceNotFoundException
from backend.schemas.common import ApiResponse
from backend.schemas.recommendation import (
    RecommendationCreate,
    RecommendationResponse,
    RecommendationUpdate,
)
from backend.services.recommendation_service import RecommendationService


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


@router.post(
    "",
    response_model=ApiResponse[RecommendationResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_recommendation(
    data: RecommendationCreate,
    db: Session = Depends(get_db),
):
    recommendation = RecommendationService.create(db, data)

    return ApiResponse(
        status="SUCCESS",
        message="Recommendation created successfully",
        data=recommendation,
    )


@router.get(
    "",
    response_model=ApiResponse[list[RecommendationResponse]],
)
def get_recommendations(
    db: Session = Depends(get_db),
):
    recommendations = RecommendationService.get_all(db)

    return ApiResponse(
        status="SUCCESS",
        message="Recommendations retrieved successfully",
        data=recommendations,
    )


@router.get(
    "/facility/{facility_id}",
    response_model=ApiResponse[list[RecommendationResponse]],
)
def get_recommendations_by_facility(
    facility_id: UUID,
    db: Session = Depends(get_db),
):
    recommendations = RecommendationService.get_by_facility(
        db,
        facility_id,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Recommendations retrieved successfully",
        data=recommendations,
    )


@router.get(
    "/alert/{alert_id}",
    response_model=ApiResponse[list[RecommendationResponse]],
)
def get_recommendations_by_alert(
    alert_id: UUID,
    db: Session = Depends(get_db),
):
    recommendations = RecommendationService.get_by_alert(
        db,
        alert_id,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Recommendations retrieved successfully",
        data=recommendations,
    )


@router.get(
    "/status/{recommendation_status}",
    response_model=ApiResponse[list[RecommendationResponse]],
)
def get_recommendations_by_status(
    recommendation_status: str,
    db: Session = Depends(get_db),
):
    recommendations = RecommendationService.get_by_status(
        db,
        recommendation_status,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Recommendations retrieved successfully",
        data=recommendations,
    )


@router.get(
    "/{recommendation_id}",
    response_model=ApiResponse[RecommendationResponse],
)
def get_recommendation(
    recommendation_id: UUID,
    db: Session = Depends(get_db),
):
    recommendation = RecommendationService.get_by_id(
        db,
        recommendation_id,
    )

    if recommendation is None:
        raise ResourceNotFoundException(
            f"Recommendation not found: {recommendation_id}"
        )

    return ApiResponse(
        status="SUCCESS",
        message="Recommendation retrieved successfully",
        data=recommendation,
    )


@router.put(
    "/{recommendation_id}",
    response_model=ApiResponse[RecommendationResponse],
)
def update_recommendation(
    recommendation_id: UUID,
    data: RecommendationUpdate,
    db: Session = Depends(get_db),
):
    recommendation = RecommendationService.get_by_id(
        db,
        recommendation_id,
    )

    if recommendation is None:
        raise ResourceNotFoundException(
            f"Recommendation not found: {recommendation_id}"
        )

    updated_recommendation = RecommendationService.update(
        db,
        recommendation,
        data,
    )

    return ApiResponse(
        status="SUCCESS",
        message="Recommendation updated successfully",
        data=updated_recommendation,
    )


@router.delete(
    "/{recommendation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_recommendation(
    recommendation_id: UUID,
    db: Session = Depends(get_db),
):
    recommendation = RecommendationService.get_by_id(
        db,
        recommendation_id,
    )

    if recommendation is None:
        raise ResourceNotFoundException(
            f"Recommendation not found: {recommendation_id}"
        )

    RecommendationService.delete(
        db,
        recommendation,
    )