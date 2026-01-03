import logging
from typing import Protocol


class LoggerPort(Protocol):
    def info(self, message: str, **kwargs: str | int | float) -> None:
        ...

    def error(self, message: str, **kwargs: str | int | float) -> None:
        ...

    def debug(self, message: str, **kwargs: str | int | float) -> None:
        ...


class StructuredLogger:
    def __init__(self, name: str = "fraud_detection") -> None:
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.INFO)

    def info(self, message: str, **kwargs: str | int | float) -> None:
        extra = {k: v for k, v in kwargs.items()}
        self._logger.info(message, extra=extra)

    def error(self, message: str, **kwargs: str | int | float) -> None:
        extra = {k: v for k, v in kwargs.items()}
        self._logger.error(message, extra=extra)

    def debug(self, message: str, **kwargs: str | int | float) -> None:
        extra = {k: v for k, v in kwargs.items()}
        self._logger.debug(message, extra=extra)

