from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.inbound.http.models.fraud_history_response import (
    FraudHistoryItem,
    FraudHistoryResponse,
)
from app.composition.dependency_registry import DependencyRegistry
from app.domain.value_objects.user_id import UserId

router = APIRouter()


def get_registry(request: Request) -> DependencyRegistry:
    return request.app.state.registry


async def get_db_session(
    registry: DependencyRegistry = Depends(get_registry),
) -> AsyncSession:
    session = registry.get_database_session()
    try:
        yield session
    finally:
        await session.close()


@router.get("/fraud-decisions/user/{user_id}", response_model=FraudHistoryResponse)
async def get_fraud_history(
    user_id: str,
    session: AsyncSession = Depends(get_db_session),
    registry: DependencyRegistry = Depends(get_registry),
) -> FraudHistoryResponse:
    try:
        uid = UserId.create(user_id)
        use_case = registry.get_retrieve_fraud_history_use_case(session)
        decisions = await use_case.execute(uid)
        return FraudHistoryResponse(
            user_id=user_id,
            decisions=[
                FraudHistoryItem(
                    transaction_id=str(d.transaction_id.value),
                    risk_score=d.risk_score,
                    decision=d.decision.value,
                    timestamp=d.timestamp,
                )
                for d in decisions
            ],
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

