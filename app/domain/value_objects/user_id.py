from dataclasses import dataclass

from app.domain.exceptions import InvalidUserIdError


@dataclass(frozen=True)
class UserId:
    value: str

    @classmethod
    def create(cls, value: str) -> "UserId":
        if not value or not value.strip():
            raise InvalidUserIdError("User ID cannot be empty")
        if len(value) > 100:
            raise InvalidUserIdError("User ID exceeds maximum length")
        return cls(value=value.strip())

