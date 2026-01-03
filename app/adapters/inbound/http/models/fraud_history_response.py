from datetime import datetime

from pydantic import BaseModel, Field


class FraudHistoryItem(BaseModel):
    transaction_id: str = Field(description="Transaction ID")
    risk_score: float = Field(ge=0.0, le=1.0, description="Fraud risk score")
    decision: str = Field(description="Fraud decision")
    timestamp: datetime = Field(description="Decision timestamp")


class FraudHistoryResponse(BaseModel):
    user_id: str = Field(description="User ID")
    decisions: list[FraudHistoryItem] = Field(description="List of fraud decisions")

