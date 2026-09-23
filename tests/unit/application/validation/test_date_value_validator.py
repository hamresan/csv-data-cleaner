"""Behavioral tests for date-value validation."""

import pytest

from csv_data_cleaner.application.dates import DateParser
from csv_data_cleaner.application.validation import DateValueValidator
from csv_data_cleaner.domain import DataRow, DateValidationRule

RULE = DateValidationRule(
    column="created_at",
    formats=("%Y-%m-%d", "%d/%m/%Y"),
)


@pytest.mark.parametrize("value", ["2026-09-23", "23/09/2026"])
def test_validator_accepts_each_configured_date_format(value: str) -> None:
    row = DataRow(number=2, values={"created_at": value})

    assert DateValueValidator(date_parser=DateParser()).validate(row, (RULE,)) == ()


@pytest.mark.parametrize("value", ["09-23-2026", "2026-02-30", "not-a-date"])
def test_validator_reports_invalid_date(value: str) -> None:
    row = DataRow(number=6, values={"created_at": value})

    issues = DateValueValidator(date_parser=DateParser()).validate(row, (RULE,))

    assert len(issues) == 1
    assert issues[0].row_number == 6
    assert issues[0].column == "created_at"
    assert issues[0].code == "invalid_date"


def test_validator_skips_empty_optional_date() -> None:
    row = DataRow(number=2, values={"created_at": None})

    assert DateValueValidator(date_parser=DateParser()).validate(row, (RULE,)) == ()
