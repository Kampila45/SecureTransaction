from typing import Protocol

from app.domain.entities.fraud_decision import FraudDecision
from app.domain.value_objects.transaction_id import TransactionId
from app.domain.value_objects.user_id import UserId


class FraudDecisionRepositoryPort(Protocol):
    async def save(self, fraud_decision: FraudDecision) -> None:
        ...

    async def find_by_transaction_id(self, transaction_id: TransactionId) -> FraudDecision | None:
        ...

    async def find_by_user_id(self, user_id: UserId) -> list[FraudDecision]:
        ...

