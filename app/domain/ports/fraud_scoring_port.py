from typing import Protocol

from app.domain.entities.transaction import Transaction


class FraudScoringPort(Protocol):
    async def score_transaction(self, transaction: Transaction) -> float:
        ...

