from app.domain.entities.fraud_decision import FraudDecision
from app.domain.exceptions import FraudDecisionNotFoundError
from app.domain.ports.fraud_decision_repository_port import FraudDecisionRepositoryPort
from app.domain.value_objects.transaction_id import TransactionId


class RetrieveFraudDecisionUseCase:
    def __init__(self, fraud_decision_repository: FraudDecisionRepositoryPort) -> None:
        self._fraud_decision_repository = fraud_decision_repository

    async def execute(self, transaction_id: TransactionId) -> FraudDecision:
        fraud_decision = await self._fraud_decision_repository.find_by_transaction_id(transaction_id)
        if fraud_decision is None:
            raise FraudDecisionNotFoundError(f"Fraud decision not found for transaction ID: {transaction_id}")
        return fraud_decision

