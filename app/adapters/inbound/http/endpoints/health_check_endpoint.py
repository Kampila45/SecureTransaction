from typing import TypedDict

from fastapi import APIRouter, Depends, Request

from app.composition.dependency_registry import DependencyRegistry

router = APIRouter()


class HealthStatus(TypedDict):
    status: str
    database: str
    ml_model: str


def get_registry(request: Request) -> DependencyRegistry:
    return request.app.state.registry


@router.get("/health")
async def health_check(
    registry: DependencyRegistry = Depends(get_registry),
) -> HealthStatus:
    database_status = "healthy"
    if not await registry.test_database_connection():
        database_status = "unhealthy"

    ml_model_status = "healthy"
    try:
        registry.get_fraud_scoring_service()
    except Exception:
        ml_model_status = "unhealthy"

    overall_status = "healthy" if database_status == "healthy" and ml_model_status == "healthy" else "unhealthy"

    return HealthStatus(
        status=overall_status,
        database=database_status,
        ml_model=ml_model_status,
    )

