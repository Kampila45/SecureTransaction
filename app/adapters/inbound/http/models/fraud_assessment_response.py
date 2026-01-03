from datetime import datetime

from pydantic import BaseModel, Field

from app.domain.entities.fraud_decision import Decision


class FraudAssessmentResponse(BaseModel):
    transaction_id: str = Field(description="Transaction ID")
    risk_score: float = Field(ge=0.0, le=1.0, description="Fraud risk score")
    decision: str = Field(description="Fraud decision")
    timestamp: datetime = Field(description="Decision timestamp")

