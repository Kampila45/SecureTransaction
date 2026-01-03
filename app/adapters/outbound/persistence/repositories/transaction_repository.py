from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.outbound.persistence.models import TransactionModel
from app.domain.entities.transaction import Transaction, TransactionMetadata
from app.domain.ports.transaction_repository_port import TransactionRepositoryPort
from app.domain.value_objects.merchant_id import MerchantId
from app.domain.value_objects.transaction_amount import TransactionAmount
from app.domain.value_objects.transaction_id import TransactionId
from app.domain.value_objects.user_id import UserId


class TransactionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, transaction: Transaction) -> None:
        import json

        model = TransactionModel(
            transaction_id=str(transaction.transaction_id.value),
            user_id=transaction.user_id.value,
            merchant_id=transaction.merchant_id.value,
            amount=str(transaction.amount.value),
            timestamp=transaction.timestamp,
            transaction_metadata=json.dumps(transaction.metadata) if transaction.metadata else None,
        )
        self._session.add(model)
        await self._session.commit()

    async def find_by_id(self, transaction_id: TransactionId) -> Transaction | None:
        stmt = select(TransactionModel).where(
            TransactionModel.transaction_id == str(transaction_id.value)
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._to_domain(model)

    def _to_domain(self, model: TransactionModel) -> Transaction:
        import json

        metadata: TransactionMetadata | None = None
        if model.transaction_metadata:
            metadata = json.loads(model.transaction_metadata)
        return Transaction(
            transaction_id=TransactionId.create(model.transaction_id),
            user_id=UserId.create(model.user_id),
            merchant_id=MerchantId.create(model.merchant_id),
            amount=TransactionAmount.create(model.amount),
            timestamp=model.timestamp,
            metadata=metadata,
        )

