from collections.abc import AsyncIterator

from app.adapters.outbound.config import Settings
from app.adapters.outbound.logging.logger import StructuredLogger
from app.adapters.outbound.ml.fraud_scoring_service import FraudScoringService
from app.adapters.outbound.ml.model_loader import ModelLoader
from app.adapters.outbound.persistence.database import Database
from app.adapters.outbound.persistence.repositories.fraud_decision_repository import (
    FraudDecisionRepository,
)
from app.adapters.outbound.persistence.repositories.transaction_repository import (
    TransactionRepository,
)
from app.application.use_cases.assess_fraud_risk_use_case import AssessFraudRiskUseCase
from app.application.use_cases.retrieve_fraud_decision_use_case import (
    RetrieveFraudDecisionUseCase,
)
from app.application.use_cases.retrieve_fraud_history_use_case import (
    RetrieveFraudHistoryUseCase,
)
from sqlalchemy.ext.asyncio import AsyncSession


class DependencyRegistry:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._database = Database(settings.database_url)
        self._logger = StructuredLogger()
        self._ml_model = ModelLoader.load_model(settings.model_path)
        self._fraud_scoring_service = FraudScoringService(self._ml_model)

    def get_database_session(self) -> AsyncSession:
        return self._database._session_factory()

    def get_database_session_dependency(self) -> AsyncIterator[AsyncSession]:
        return self._database.get_session()

    def get_assess_fraud_risk_use_case(self, session: AsyncSession) -> AssessFraudRiskUseCase:
        fraud_decision_repo = FraudDecisionRepository(session)
        transaction_repo = TransactionRepository(session)
        return AssessFraudRiskUseCase(
            fraud_scoring_port=self._fraud_scoring_service,
            fraud_decision_repository=fraud_decision_repo,
            transaction_repository=transaction_repo,
        )

    def get_retrieve_fraud_decision_use_case(
        self, session: AsyncSession
    ) -> RetrieveFraudDecisionUseCase:
        fraud_decision_repo = FraudDecisionRepository(session)
        return RetrieveFraudDecisionUseCase(fraud_decision_repository=fraud_decision_repo)

    def get_retrieve_fraud_history_use_case(
        self, session: AsyncSession
    ) -> RetrieveFraudHistoryUseCase:
        fraud_decision_repo = FraudDecisionRepository(session)
        return RetrieveFraudHistoryUseCase(fraud_decision_repository=fraud_decision_repo)

    def get_fraud_scoring_service(self) -> FraudScoringService:
        return self._fraud_scoring_service

    async def test_database_connection(self) -> bool:
        return await self._database.test_connection()

    async def close(self) -> None:
        await self._database.close()

