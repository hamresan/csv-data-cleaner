"""Behavioral tests for processing report calculation."""

from pathlib import Path

from csv_data_cleaner.application.reporting import ProcessingReportCalculator
from csv_data_cleaner.domain import DataRow, DatasetProcessingResult, RowProcessingResult
from csv_data_cleaner.domain.deduplication import DuplicateRow
from csv_data_cleaner.domain.validation import ValidationIssue


def row(number: int, *, valid: bool = True) -> RowProcessingResult:
    data = DataRow(number, {"name": f"row-{number}"})
    issues = () if valid else (ValidationIssue(number, "name", "invalid", "Invalid name."),)
    return RowProcessingResult(data, data, issues)


def test_calculator_derives_all_counts_from_pipeline_result() -> None:
    retained_valid = row(2)
    retained_invalid = row(3, valid=False)
    filtered_valid = row(4)
    filtered_invalid = row(5, valid=False)
    duplicate = row(6, valid=False)
    result = DatasetProcessingResult(
        rows=(retained_valid, retained_invalid),
        filtered_rows=(filtered_valid, filtered_invalid),
        duplicate_rows=(DuplicateRow(duplicate, 2, ("row-2",)),),
        columns=("name",),
    )

    summary = ProcessingReportCalculator().calculate(
        Path("/input/customers.csv"),
        result,
        Path("output/cleaned.csv"),
    )

    assert summary.input_file == "customers.csv"
    assert summary.processed_records == 5
    assert summary.valid_records == 2
    assert summary.invalid_records == 2
    assert summary.duplicate_records == 1
    assert summary.exported_records == 1
    assert summary.output_file == "output/cleaned.csv"
