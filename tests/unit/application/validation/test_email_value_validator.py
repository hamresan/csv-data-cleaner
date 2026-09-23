"""Behavioral tests for email-value validation."""

from csv_data_cleaner.application.validation import EmailValueValidator
from csv_data_cleaner.domain import DataRow
from tests.unit.application.validation.fakes import FakeEmailSyntaxChecker


def test_validator_accepts_email_accepted_by_syntax_checker() -> None:
    row = DataRow(number=2, values={"email": "ada@example.com"})
    validator = EmailValueValidator(
        syntax_checker=FakeEmailSyntaxChecker({"ada@example.com"}),
    )

    assert validator.validate(row, ("email",)) == ()


def test_validator_reports_email_rejected_by_syntax_checker() -> None:
    row = DataRow(number=9, values={"email": "not-an-email"})
    validator = EmailValueValidator(syntax_checker=FakeEmailSyntaxChecker(set()))

    issues = validator.validate(row, ("email",))

    assert len(issues) == 1
    assert issues[0].row_number == 9
    assert issues[0].column == "email"
    assert issues[0].code == "invalid_email"


def test_validator_rejects_non_string_email_without_calling_library_behavior() -> None:
    row = DataRow(number=9, values={"email": 42})
    validator = EmailValueValidator(syntax_checker=FakeEmailSyntaxChecker(set()))

    issues = validator.validate(row, ("email",))

    assert issues[0].code == "invalid_email"


def test_validator_skips_empty_optional_email() -> None:
    row = DataRow(number=2, values={"email": None})
    validator = EmailValueValidator(syntax_checker=FakeEmailSyntaxChecker(set()))

    assert validator.validate(row, ("email",)) == ()
