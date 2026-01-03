from contextlib import asynccontextmanager
from typing import TypedDict

from fastapi import FastAPI

from app.adapters.inbound.http.endpoints import (
    fraud_assessment_endpoint,
    fraud_decision_endpoint,
    fraud_history_endpoint,
    health_check_endpoint,
)
from app.adapters.inbound.http.exception_handlers import (
    domain_exception_handler,
    value_error_handler,
)
from app.adapters.outbound.config import Settings
from app.composition.dependency_registry import DependencyRegistry
from app.domain.exceptions import DomainException


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()
    app.state.registry = DependencyRegistry(settings)
    yield
    await app.state.registry.close()


app = FastAPI(
    title="SecureTransaction API",
    description="Production-grade fraud detection API using FastAPI and Hexagonal Architecture",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_exception_handler(DomainException, domain_exception_handler)
app.add_exception_handler(ValueError, value_error_handler)

app.include_router(fraud_assessment_endpoint.router, tags=["Fraud Assessment"])
app.include_router(fraud_decision_endpoint.router, tags=["Fraud Decisions"])
app.include_router(fraud_history_endpoint.router, tags=["Fraud History"])
app.include_router(health_check_endpoint.router, tags=["Health"])


class RootResponse(TypedDict):
    name: str
    version: str
    description: str
    documentation: str
    endpoints: dict[str, str]


@app.get("/", response_model=RootResponse)
async def root() -> RootResponse:
    return RootResponse(
        name="SecureTransaction API",
        version="1.0.0",
        description="Production-grade fraud detection API using FastAPI and Hexagonal Architecture",
        documentation="/docs",
        endpoints={
            "assess_fraud": "POST /assess-fraud",
            "get_fraud_decision": "GET /fraud-decisions/{transaction_id}",
            "get_fraud_history": "GET /fraud-decisions/user/{user_id}",
            "health_check": "GET /health",
        },
    )

