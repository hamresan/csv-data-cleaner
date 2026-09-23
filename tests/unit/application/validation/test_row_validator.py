"""Behavioral tests for row validation orchestration."""

from csv_data_cleaner.application.dates import DateParser
from csv_data_cleaner.application.validation import (
    DateValueValidator,
    EmailValueValidator,
    RequiredValueValidator,
    RowValidator,
)
from csv_data_cleaner.domain import (
    DataRow,
    DateValidationRule,
    NormalizationPolicy,
    OutputFormat,
    ProcessingConfig,
)
from tests.unit.application.validation.fakes import FakeEmailSyntaxChecker


def build_config() -> ProcessingConfig:
    return ProcessingConfig(
        required_columns=("name", "email"),
        email_columns=("email",),
        date_rules=(
            DateValidationRule(
                column="created_at",
                formats=("%Y-%m-%d", "%d/%m/%Y"),
            ),
        ),
        normalization=NormalizationPolicy(),
        deduplication=None,
        sorting=(),
        output_format=OutputFormat.CSV,
    )


def build_validator() -> RowValidator:
    return RowValidator(
        required_validator=RequiredValueValidator(),
        email_validator=EmailValueValidator(
            syntax_checker=FakeEmailSyntaxChecker({"user@example.com"})
        ),
        date_validator=DateValueValidator(date_parser=DateParser()),
    )


def test_validator_accumulates_multiple_failures_deterministically() -> None:
    row = DataRow(
        number=8,
        values={
            "name": None,
            "email": "invalid-email",
            "created_at": "2026-02-30",
        },
    )

    issues = build_validator().validate(row, build_config())

    assert [(issue.column, issue.code) for issue in issues] == [
        ("name", "required"),
        ("email", "invalid_email"),
        ("created_at", "invalid_date"),
    ]


def test_validator_does_not_duplicate_required_and_format_errors_for_empty_values() -> None:
    row = DataRow(
        number=3,
        values={"name": None, "email": None, "created_at": None},
    )

    issues = build_validator().validate(row, build_config())

    assert [(issue.column, issue.code) for issue in issues] == [
        ("name", "required"),
        ("email", "required"),
    ]
