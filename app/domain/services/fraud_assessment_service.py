from app.domain.entities.fraud_decision import FraudDecision, Decision
from app.domain.entities.transaction import Transaction


class FraudAssessmentService:
    @staticmethod
    def determine_decision(risk_score: float) -> Decision:
        if risk_score < 0.3:
            return Decision.APPROVE
        elif risk_score < 0.7:
            return Decision.REVIEW
        else:
            return Decision.BLOCK

