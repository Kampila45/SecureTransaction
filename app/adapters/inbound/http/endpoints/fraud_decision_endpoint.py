from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.inbound.http.models.fraud_decision_response import FraudDecisionResponse
from app.composition.dependency_registry import DependencyRegistry
from app.domain.value_objects.transaction_id import TransactionId

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


@router.get("/fraud-decisions/{transaction_id}", response_model=FraudDecisionResponse)
async def get_fraud_decision(
    transaction_id: str,
    session: AsyncSession = Depends(get_db_session),
    registry: DependencyRegistry = Depends(get_registry),
) -> FraudDecisionResponse:
    try:
        tx_id = TransactionId.create(transaction_id)
        use_case = registry.get_retrieve_fraud_decision_use_case(session)
        fraud_decision = await use_case.execute(tx_id)
        return FraudDecisionResponse(
            transaction_id=str(fraud_decision.transaction_id.value),
            risk_score=fraud_decision.risk_score,
            decision=fraud_decision.decision.value,
            timestamp=fraud_decision.timestamp,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

