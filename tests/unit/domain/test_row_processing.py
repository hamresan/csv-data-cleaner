"""Behavioral tests for row processing result models."""

from csv_data_cleaner.domain import DataRow, RowProcessingResult, ValidationIssue


def test_result_reports_validity_without_losing_row_references() -> None:
    source = DataRow(number=2, values={"email": " ada@example.com "})
    normalized = DataRow(number=2, values={"email": "ada@example.com"})

    valid = RowProcessingResult(source, normalized, ())
    invalid = RowProcessingResult(
        source,
        normalized,
        (ValidationIssue(2, "email", "invalid_email", "Email is invalid"),),
    )

    assert valid.is_valid is True
    assert invalid.is_valid is False
    assert invalid.source_row is source
    assert invalid.normalized_row is normalized
