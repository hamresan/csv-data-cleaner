"""Behavioral tests for processing summary."""

from csv_data_cleaner.domain import ProcessingSummary


def test_processing_summary_preserves_counters() -> None:
    summary = ProcessingSummary("input.csv", 1, 0, 1, 0, None)

    assert summary.processed_records == 1
    assert summary.invalid_records == 1
    assert summary.output_file is None
