"""Behavioral tests for row-result mapping."""

from csv_data_cleaner.application.mappers import RowResultMapper
from csv_data_cleaner.domain import DataRow, ValidationIssue


def test_mapper_preserves_source_normalized_row_and_issues() -> None:
    source = DataRow(number=5, values={"email": " invalid "})
    normalized = DataRow(number=5, values={"email": "invalid"})
    issues = (
        ValidationIssue(
            row_number=5,
            column="email",
            code="invalid_email",
            message="email must contain a valid email address.",
        ),
    )

    result = RowResultMapper().map(source, normalized, issues)

    assert result.source_row is source
    assert result.normalized_row is normalized
    assert result.issues is issues
    assert result.is_valid is False
