"""Behavioral tests for required-value validation."""

from csv_data_cleaner.application.validation import RequiredValueValidator
from csv_data_cleaner.domain import DataRow


def test_validator_reports_required_values_in_configured_order() -> None:
    row = DataRow(number=4, values={"name": None, "email": None})

    issues = RequiredValueValidator().validate(row, ("email", "name"))

    assert [(issue.column, issue.code) for issue in issues] == [
        ("email", "required"),
        ("name", "required"),
    ]


def test_validator_accepts_present_values() -> None:
    row = DataRow(number=2, values={"name": "Ada", "active": False, "score": 0})

    assert RequiredValueValidator().validate(row, ("name", "active", "score")) == ()
