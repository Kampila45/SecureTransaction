from typing import Protocol

from app.domain.entities.transaction import Transaction
from app.domain.value_objects.transaction_id import TransactionId


class TransactionRepositoryPort(Protocol):
    async def save(self, transaction: Transaction) -> None:
        ...

    async def find_by_id(self, transaction_id: TransactionId) -> Transaction | None:
        ...

