"""JSON processing-report writer."""

import json
from dataclasses import asdict
from pathlib import Path

from csv_data_cleaner.application.ports import ReportWriter
from csv_data_cleaner.domain import ProcessingSummary
from csv_data_cleaner.domain.errors import OutputDataError


class JsonReportWriter(ReportWriter):
    """Persist a deterministic machine-readable processing report."""

    def write(self, summary: ProcessingSummary, output_dir: Path) -> Path:
        report_path = output_dir / "report.json"
        try:
            report_path.write_text(
                json.dumps(asdict(summary), indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        except (OSError, TypeError) as error:
            raise OutputDataError(f"Could not write processing report: {report_path}") from error
        return report_path
