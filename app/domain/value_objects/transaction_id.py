from dataclasses import dataclass
from uuid import UUID

from app.domain.exceptions import InvalidTransactionIdError


@dataclass(frozen=True)
class TransactionId:
    value: UUID

    @classmethod
    def create(cls, value: str | UUID) -> "TransactionId":
        if isinstance(value, str):
            try:
                uuid_value = UUID(value)
            except ValueError:
                raise InvalidTransactionIdError(f"Invalid transaction ID format: {value}")
        else:
            uuid_value = value
        return cls(value=uuid_value)

    def __str__(self) -> str:
        return str(self.value)

