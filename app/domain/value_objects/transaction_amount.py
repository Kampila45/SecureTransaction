from dataclasses import dataclass
from decimal import Decimal

from app.domain.exceptions import InvalidTransactionAmountError


@dataclass(frozen=True)
class TransactionAmount:
    value: Decimal

    @classmethod
    def create(cls, value: Decimal | float | int | str) -> "TransactionAmount":
        if isinstance(value, (int, float, str)):
            decimal_value = Decimal(str(value))
        else:
            decimal_value = value
        if decimal_value <= 0:
            raise InvalidTransactionAmountError("Transaction amount must be greater than zero")
        if decimal_value > Decimal("999999999.99"):
            raise InvalidTransactionAmountError("Transaction amount exceeds maximum allowed")
        return cls(value=decimal_value)

    def __post_init__(self) -> None:
        if self.value <= 0:
            raise InvalidTransactionAmountError("Transaction amount must be greater than zero")

