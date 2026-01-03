from datetime import datetime
from typing import TypedDict

from app.domain.value_objects.merchant_id import MerchantId
from app.domain.value_objects.transaction_amount import TransactionAmount
from app.domain.value_objects.transaction_id import TransactionId
from app.domain.value_objects.user_id import UserId


class TransactionMetadata(TypedDict, total=False):
    ip_address: str
    device_id: str
    location: str
    payment_method: str


class Transaction:
    def __init__(
        self,
        transaction_id: TransactionId,
        user_id: UserId,
        merchant_id: MerchantId,
        amount: TransactionAmount,
        timestamp: datetime,
        metadata: TransactionMetadata | None = None,
    ) -> None:
        self._transaction_id = transaction_id
        self._user_id = user_id
        self._merchant_id = merchant_id
        self._amount = amount
        self._timestamp = timestamp
        self._metadata = metadata or {}

    @property
    def transaction_id(self) -> TransactionId:
        return self._transaction_id

    @property
    def user_id(self) -> UserId:
        return self._user_id

    @property
    def merchant_id(self) -> MerchantId:
        return self._merchant_id

    @property
    def amount(self) -> TransactionAmount:
        return self._amount

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @property
    def metadata(self) -> TransactionMetadata:
        return self._metadata

    def assess_fraud_risk(self, ml_score: float) -> float:
        if ml_score < 0.0 or ml_score > 1.0:
            raise ValueError("ML score must be between 0.0 and 1.0")
        base_risk = ml_score
        if self._amount.value > 10000:
            base_risk = min(1.0, base_risk + 0.1)
        if self._timestamp.hour < 6 or self._timestamp.hour > 22:
            base_risk = min(1.0, base_risk + 0.05)
        return min(1.0, base_risk)

