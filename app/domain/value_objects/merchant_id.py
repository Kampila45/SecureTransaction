from dataclasses import dataclass

from app.domain.exceptions import InvalidMerchantIdError


@dataclass(frozen=True)
class MerchantId:
    value: str

    @classmethod
    def create(cls, value: str) -> "MerchantId":
        if not value or not value.strip():
            raise InvalidMerchantIdError("Merchant ID cannot be empty")
        if len(value) > 100:
            raise InvalidMerchantIdError("Merchant ID exceeds maximum length")
        return cls(value=value.strip())

