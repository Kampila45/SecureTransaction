from datetime import datetime
from typing import TypedDict

from pydantic import BaseModel, Field


class FraudAssessmentRequest(BaseModel):
    amount: float = Field(gt=0, description="Transaction amount")
    user_id: str = Field(min_length=1, max_length=100, description="User ID")
    merchant_id: str = Field(min_length=1, max_length=100, description="Merchant ID")
    timestamp: datetime = Field(description="Transaction timestamp")
    metadata: dict[str, str] | None = Field(default=None, description="Optional transaction metadata")

