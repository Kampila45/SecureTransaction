from datetime import datetime

from app.domain.entities.fraud_decision import FraudDecision
from app.domain.entities.transaction import Transaction
from app.domain.ports.fraud_decision_repository_port import FraudDecisionRepositoryPort
from app.domain.ports.fraud_scoring_port import FraudScoringPort
from app.domain.ports.transaction_repository_port import TransactionRepositoryPort
from app.domain.value_objects.merchant_id import MerchantId
from app.domain.value_objects.transaction_amount import TransactionAmount
from app.domain.value_objects.transaction_id import TransactionId
from app.domain.value_objects.user_id import UserId


from app.domain.ports.transaction_repository_port import TransactionRepositoryPort


class AssessFraudRiskUseCase:
    def __init__(
        self,
        fraud_scoring_port: FraudScoringPort,
        fraud_decision_repository: FraudDecisionRepositoryPort,
        transaction_repository: TransactionRepositoryPort,
    ) -> None:
        self._fraud_scoring_port = fraud_scoring_port
        self._fraud_decision_repository = fraud_decision_repository
        self._transaction_repository = transaction_repository

    async def execute(
        self,
        transaction_id: TransactionId,
        user_id: UserId,
        merchant_id: MerchantId,
        amount: TransactionAmount,
        timestamp: datetime,
        metadata: dict[str, str] | None = None,
    ) -> FraudDecision:
        transaction = Transaction(
            transaction_id=transaction_id,
            user_id=user_id,
            merchant_id=merchant_id,
            amount=amount,
            timestamp=timestamp,
            metadata=metadata,
        )
        await self._transaction_repository.save(transaction)
        ml_score = await self._fraud_scoring_port.score_transaction(transaction)
        risk_score = transaction.assess_fraud_risk(ml_score)
        fraud_decision = FraudDecision.create(
            transaction_id=transaction_id,
            risk_score=risk_score,
            timestamp=datetime.utcnow(),
        )
        await self._fraud_decision_repository.save(fraud_decision)
        return fraud_decision

