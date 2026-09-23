"""Fakes for pipeline orchestration tests."""

from pathlib import Path

from csv_data_cleaner.application.ports import (
    ConfigLoader,
    Exporter,
    InputReader,
    ReportCalculator,
    ReportWriter,
)
from csv_data_cleaner.domain import (
    DatasetProcessingResult,
    InputData,
    ProcessingConfig,
    ProcessingSummary,
)


class FakeConfigLoader(ConfigLoader):
    def __init__(self, config: ProcessingConfig) -> None:
        self.config = config
        self.calls: list[Path] = []

    def load(self, path: Path) -> ProcessingConfig:
        self.calls.append(path)
        return self.config


class FakeInputReader(InputReader):
    def __init__(self, data: InputData) -> None:
        self.data = data
        self.calls: list[tuple[Path, str | None]] = []

    def read(self, path: Path, *, sheet: str | None = None) -> InputData:
        self.calls.append((path, sheet))
        return self.data


class FakeExporter(Exporter):
    def __init__(self, output_file: Path) -> None:
        self.output_file = output_file
        self.calls: list[tuple[DatasetProcessingResult, ProcessingConfig, Path]] = []

    def export(
        self,
        result: DatasetProcessingResult,
        config: ProcessingConfig,
        output_dir: Path,
    ) -> Path:
        self.calls.append((result, config, output_dir))
        return self.output_file


class FakeReportCalculator(ReportCalculator):
    def __init__(self, summary: ProcessingSummary) -> None:
        self.summary = summary
        self.calls: list[tuple[Path, DatasetProcessingResult, Path]] = []

    def calculate(
        self,
        input_path: Path,
        result: DatasetProcessingResult,
        output_file: Path,
    ) -> ProcessingSummary:
        self.calls.append((input_path, result, output_file))
        return self.summary


class FakeReportWriter(ReportWriter):
    def __init__(self) -> None:
        self.calls: list[tuple[ProcessingSummary, Path]] = []

    def write(self, summary: ProcessingSummary, output_dir: Path) -> Path:
        self.calls.append((summary, output_dir))
        return output_dir / "report.json"
