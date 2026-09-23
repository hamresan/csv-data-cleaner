"""Behavioral tests for processing summary."""

from csv_data_cleaner.domain import ProcessingSummary


def test_processing_summary_preserves_counters() -> None:
    summary = ProcessingSummary(
        input_file="input.csv",
        processed_records=2,
        valid_records=1,
        invalid_records=1,
        duplicate_records=0,
        exported_records=1,
        output_file="output/cleaned.csv",
    )

    assert summary.processed_records == 2
    assert summary.invalid_records == 1
    assert summary.exported_records == 1
    assert summary.output_file == "output/cleaned.csv"
