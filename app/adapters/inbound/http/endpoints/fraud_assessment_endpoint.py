from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.inbound.http.models.fraud_assessment_request import FraudAssessmentRequest
from app.adapters.inbound.http.models.fraud_assessment_response import FraudAssessmentResponse
from app.composition.dependency_registry import DependencyRegistry
from app.domain.value_objects.merchant_id import MerchantId
from app.domain.value_objects.transaction_amount import TransactionAmount
from app.domain.value_objects.transaction_id import TransactionId
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


@router.post("/assess-fraud", response_model=FraudAssessmentResponse, status_code=status.HTTP_201_CREATED)
async def assess_fraud(
    request: FraudAssessmentRequest,
    session: AsyncSession = Depends(get_db_session),
    registry: DependencyRegistry = Depends(get_registry),
) -> FraudAssessmentResponse:
    try:
        transaction_id = TransactionId.create(uuid4())
        user_id = UserId.create(request.user_id)
        merchant_id = MerchantId.create(request.merchant_id)
        amount = TransactionAmount.create(request.amount)
        use_case = registry.get_assess_fraud_risk_use_case(session)
        fraud_decision = await use_case.execute(
            transaction_id=transaction_id,
            user_id=user_id,
            merchant_id=merchant_id,
            amount=amount,
            timestamp=request.timestamp,
            metadata=request.metadata,
        )
        return FraudAssessmentResponse(
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

