"""Behavioral tests for immutable domain models."""

import pytest

from csv_data_cleaner.domain import (
    DataRow,
    DeduplicationKeep,
    DeduplicationPolicy,
    InputData,
    OutputFormat,
    ProcessingConfig,
    ProcessingSummary,
    SortRule,
    ValidationIssue,
)


def test_data_row_copies_and_protects_values() -> None:
    values = {"name": "Ada", "active": True}
    row = DataRow(number=2, values=values)

    values["name"] = "Changed"

    assert row.values == {"name": "Ada", "active": True}
    with pytest.raises(TypeError):
        row.values["name"] = "Grace"  # type: ignore[index]


def test_input_and_configuration_models_preserve_canonical_values() -> None:
    row = DataRow(number=2, values={"email": "ada@example.com"})
    data = InputData(columns=("email",), rows=(row,))
    config = ProcessingConfig(
        required_columns=("email",),
        email_columns=("email",),
        date_columns=(),
        deduplication=DeduplicationPolicy(("email",), DeduplicationKeep.LAST),
        sorting=(SortRule("email", ascending=False),),
        output_format=OutputFormat.CSV,
    )

    assert data.rows == (row,)
    assert config.deduplication == DeduplicationPolicy(("email",), DeduplicationKeep.LAST)
    assert config.sorting == (SortRule("email", ascending=False),)


def test_validation_issue_and_summary_are_value_objects() -> None:
    issue = ValidationIssue(2, "email", "invalid_email", "Email is invalid")
    summary = ProcessingSummary("input.csv", 1, 0, 1, 0, None)

    assert issue.row_number == 2
    assert summary.invalid_records == 1
