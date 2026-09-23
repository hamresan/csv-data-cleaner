"""Validation domain models."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """A validation failure associated with one source row."""

    row_number: int
    column: str
    code: str
    message: str
