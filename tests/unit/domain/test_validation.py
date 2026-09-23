"""Behavioral tests for validation domain models."""

from csv_data_cleaner.domain import ValidationIssue


def test_validation_issue_preserves_source_context() -> None:
    issue = ValidationIssue(2, "email", "invalid_email", "Email is invalid")

    assert issue.row_number == 2
    assert issue.column == "email"
    assert issue.code == "invalid_email"
