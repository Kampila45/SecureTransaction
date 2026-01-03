import asyncio
from typing import Any

from app.domain.entities.transaction import Transaction
from app.domain.ports.fraud_scoring_port import FraudScoringPort


class FraudScoringService:
    def __init__(self, model: Any) -> None:
        self._model = model

    async def score_transaction(self, transaction: Transaction) -> float:
        features = self._extract_features(transaction)
        score = await asyncio.to_thread(self._model.predict_proba, [features])
        return float(score[0][1])

    def _extract_features(self, transaction: Transaction) -> list[float]:
        amount = float(transaction.amount.value)
        hour = transaction.timestamp.hour
        day_of_week = transaction.timestamp.weekday()
        metadata = transaction.metadata
        return [
            amount,
            hour,
            day_of_week,
            float(len(metadata.get("ip_address", "")) > 0),
            float(len(metadata.get("device_id", "")) > 0),
        ]

