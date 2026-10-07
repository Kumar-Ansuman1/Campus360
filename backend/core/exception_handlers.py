from fastapi import Request
from fastapi.responses import JSONResponse

from backend.core.exceptions import (
    DatabaseException,
    ResourceConflictException,
    ResourceNotFoundException,
    ResourceValidationException,
)


async def resource_not_found_handler(
    request: Request,
    exc: ResourceNotFoundException,
):
    return JSONResponse(
        status_code=404,
        content={
            "status": "ERROR",
            "message": exc.message,
        },
    )


async def resource_conflict_handler(
    request: Request,
    exc: ResourceConflictException,
):
    return JSONResponse(
        status_code=409,
        content={
            "status": "ERROR",
            "message": exc.message,
        },
    )


async def resource_validation_handler(
    request: Request,
    exc: ResourceValidationException,
):
    return JSONResponse(
        status_code=400,
        content={
            "status": "ERROR",
            "message": exc.message,
        },
    )


async def database_exception_handler(
    request: Request,
    exc: DatabaseException,
):
    return JSONResponse(
        status_code=500,
        content={
            "status": "ERROR",
            "message": "A database error occurred",
        },
    )