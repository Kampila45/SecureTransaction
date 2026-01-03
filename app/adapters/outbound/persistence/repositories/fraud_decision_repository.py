from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.outbound.persistence.models import FraudDecisionModel, TransactionModel
from app.domain.entities.fraud_decision import Decision, FraudDecision
from app.domain.ports.fraud_decision_repository_port import FraudDecisionRepositoryPort
from app.domain.value_objects.transaction_id import TransactionId
from app.domain.value_objects.user_id import UserId


class FraudDecisionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, fraud_decision: FraudDecision) -> None:
        model = FraudDecisionModel(
            transaction_id=str(fraud_decision.transaction_id.value),
            risk_score=fraud_decision.risk_score,
            decision=fraud_decision.decision.value,
            timestamp=fraud_decision.timestamp,
        )
        self._session.add(model)
        await self._session.commit()

    async def find_by_transaction_id(self, transaction_id: TransactionId) -> FraudDecision | None:
        stmt = select(FraudDecisionModel).where(
            FraudDecisionModel.transaction_id == str(transaction_id.value)
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._to_domain(model)

    async def find_by_user_id(self, user_id: UserId) -> list[FraudDecision]:
        stmt = select(FraudDecisionModel).join(
            TransactionModel, FraudDecisionModel.transaction_id == TransactionModel.transaction_id
        ).where(TransactionModel.user_id == user_id.value)
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._to_domain(model) for model in models]

    def _to_domain(self, model: FraudDecisionModel) -> FraudDecision:
        return FraudDecision(
            transaction_id=TransactionId.create(model.transaction_id),
            risk_score=model.risk_score,
            decision=Decision(model.decision),
            timestamp=model.timestamp,
        )

