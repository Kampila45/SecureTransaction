from dataclasses import dataclass
from datetime import datetime

from app.domain.entities.fraud_decision import Decision
from app.domain.value_objects.transaction_id import TransactionId


@dataclass(frozen=True)
class FraudAssessmentResult:
    transaction_id: TransactionId
    risk_score: float
    decision: Decision
    timestamp: datetime

