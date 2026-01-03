from datetime import datetime
from enum import Enum

from app.domain.value_objects.transaction_id import TransactionId


class Decision(Enum):
    APPROVE = "approve"
    REVIEW = "review"
    BLOCK = "block"


class FraudDecision:
    def __init__(
        self,
        transaction_id: TransactionId,
        risk_score: float,
        decision: Decision,
        timestamp: datetime,
    ) -> None:
        if risk_score < 0.0 or risk_score > 1.0:
            raise ValueError("Risk score must be between 0.0 and 1.0")
        self._transaction_id = transaction_id
        self._risk_score = risk_score
        self._decision = decision
        self._timestamp = timestamp

    @classmethod
    def create(
        cls,
        transaction_id: TransactionId,
        risk_score: float,
        timestamp: datetime,
    ) -> "FraudDecision":
        if risk_score < 0.3:
            decision = Decision.APPROVE
        elif risk_score < 0.7:
            decision = Decision.REVIEW
        else:
            decision = Decision.BLOCK
        return cls(
            transaction_id=transaction_id,
            risk_score=risk_score,
            decision=decision,
            timestamp=timestamp,
        )

    @property
    def transaction_id(self) -> TransactionId:
        return self._transaction_id

    @property
    def risk_score(self) -> float:
        return self._risk_score

    @property
    def decision(self) -> Decision:
        return self._decision

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

