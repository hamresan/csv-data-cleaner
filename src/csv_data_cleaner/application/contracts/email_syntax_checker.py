"""Email syntax checking application contract."""

from typing import Protocol


class EmailSyntaxChecker(Protocol):
    """Check email syntax without exposing a concrete validation library."""

    def is_valid(self, value: str) -> bool:
        """Return whether the email address has valid syntax."""
        ...
