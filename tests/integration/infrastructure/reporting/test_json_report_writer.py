"""Integration tests for deterministic JSON report persistence."""

import json
from pathlib import Path

from csv_data_cleaner.domain import ProcessingSummary
from csv_data_cleaner.infrastructure.reporting import JsonReportWriter


def test_writer_persists_deterministic_report_json(tmp_path: Path) -> None:
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    summary = ProcessingSummary(
        input_file="customers.csv",
        processed_records=5,
        valid_records=3,
        invalid_records=1,
        duplicate_records=1,
        exported_records=2,
        output_file=str(output_dir / "cleaned.csv"),
    )

    report_path = JsonReportWriter().write(summary, output_dir)

    assert report_path == output_dir / "report.json"
    assert json.loads(report_path.read_text(encoding="utf-8")) == {
        "input_file": "customers.csv",
        "processed_records": 5,
        "valid_records": 3,
        "invalid_records": 1,
        "duplicate_records": 1,
        "exported_records": 2,
        "output_file": str(output_dir / "cleaned.csv"),
    }
    assert report_path.read_text(encoding="utf-8").endswith("\n")
