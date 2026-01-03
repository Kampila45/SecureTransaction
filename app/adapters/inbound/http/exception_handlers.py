from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    DomainException,
    FraudDecisionNotFoundError,
    InvalidMerchantIdError,
    InvalidTransactionAmountError,
    InvalidTransactionIdError,
    InvalidUserIdError,
)


async def domain_exception_handler(request: Request, exc: DomainException) -> JSONResponse:
    status_code = status.HTTP_400_BAD_REQUEST
    if isinstance(exc, FraudDecisionNotFoundError):
        status_code = status.HTTP_404_NOT_FOUND
    return JSONResponse(
        status_code=status_code,
        content={"error": exc.__class__.__name__, "message": str(exc)},
    )


async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "ValueError", "message": str(exc)},
    )

