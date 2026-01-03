from typing import final


@final
class DomainException(Exception):
    pass


@final
class InvalidTransactionAmountError(DomainException):
    pass


@final
class InvalidUserIdError(DomainException):
    pass


@final
class InvalidMerchantIdError(DomainException):
    pass


@final
class InvalidTransactionIdError(DomainException):
    pass


@final
class FraudDecisionNotFoundError(DomainException):
    pass


@final
class TransactionNotFoundError(DomainException):
    pass

