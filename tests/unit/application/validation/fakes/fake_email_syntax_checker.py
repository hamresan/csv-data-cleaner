"""Fake email syntax checker for application validation tests."""

from csv_data_cleaner.application.contracts import EmailSyntaxChecker


class FakeEmailSyntaxChecker(EmailSyntaxChecker):
    """Deterministic syntax checker controlled by a set of valid values."""

    def __init__(self, valid_values: set[str]) -> None:
        self.valid_values = valid_values

    def is_valid(self, value: str) -> bool:
        return value in self.valid_values
