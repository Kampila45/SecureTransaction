from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.adapters.outbound.persistence.database import Base


class TransactionModel(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(String, nullable=False, index=True)
    merchant_id = Column(String, nullable=False)
    amount = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    transaction_metadata = Column("metadata", String, nullable=True)

    fraud_decisions = relationship("FraudDecisionModel", back_populates="transaction")


class FraudDecisionModel(Base):
    __tablename__ = "fraud_decisions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, ForeignKey("transactions.transaction_id"), nullable=False, index=True)
    risk_score = Column(Float, nullable=False)
    decision = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    transaction = relationship("TransactionModel", back_populates="fraud_decisions")

