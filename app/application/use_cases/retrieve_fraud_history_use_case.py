from app.domain.entities.fraud_decision import FraudDecision
from app.domain.ports.fraud_decision_repository_port import FraudDecisionRepositoryPort
from app.domain.value_objects.user_id import UserId


class RetrieveFraudHistoryUseCase:
    def __init__(self, fraud_decision_repository: FraudDecisionRepositoryPort) -> None:
        self._fraud_decision_repository = fraud_decision_repository

    async def execute(self, user_id: UserId) -> list[FraudDecision]:
        return await self._fraud_decision_repository.find_by_user_id(user_id)

