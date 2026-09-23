"""Behavioral tests for dataset processing result models."""

from csv_data_cleaner.domain import (
    DataRow,
    DatasetProcessingResult,
    RowProcessingResult,
    ValidationIssue,
)


def test_result_separates_valid_and_invalid_rows_in_source_order() -> None:
    first = RowProcessingResult(
        source_row=DataRow(2, {"name": "Ada"}),
        normalized_row=DataRow(2, {"name": "Ada"}),
        issues=(),
    )
    second = RowProcessingResult(
        source_row=DataRow(3, {"name": ""}),
        normalized_row=DataRow(3, {"name": None}),
        issues=(ValidationIssue(3, "name", "required", "name is required."),),
    )
    third = RowProcessingResult(
        source_row=DataRow(4, {"name": "Grace"}),
        normalized_row=DataRow(4, {"name": "Grace"}),
        issues=(),
    )

    result = DatasetProcessingResult(rows=(first, second, third))

    assert result.valid_rows == (first, third)
    assert result.invalid_rows == (second,)
