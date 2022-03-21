"""Мои исключения."""
from __future__ import annotations


class MessageError(Exception):
    """Ошибка при отправке сообщения."""

    pass


class VariablesError(Exception):
    """Ошибка переменных окружения."""

    pass


class StatusCodeError(Exception):
    """Исключение при неверном статусе дз."""

    pass
