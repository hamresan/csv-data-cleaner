"""Integration tests for the email-validator syntax checker."""

import pytest

from csv_data_cleaner.infrastructure.validation import EmailValidatorSyntaxChecker


@pytest.mark.parametrize(
    "email",
    ["ada@example.com", "me+tag@example.org", "用户@example.com"],
)
def test_checker_accepts_valid_email_syntax(email: str) -> None:
    assert EmailValidatorSyntaxChecker().is_valid(email) is True


@pytest.mark.parametrize("email", ["not-an-email", "@example.com", "ada@"])
def test_checker_rejects_malformed_email(email: str) -> None:
    assert EmailValidatorSyntaxChecker().is_valid(email) is False
