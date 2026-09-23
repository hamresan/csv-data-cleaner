"""Fakes for pipeline orchestration tests."""

from pathlib import Path

from csv_data_cleaner.application.ports import ConfigLoader, Exporter, InputReader, ReportCalculator
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
    def __init__(self) -> None:
        self.calls: list[tuple[DatasetProcessingResult, ProcessingConfig, Path]] = []

    def export(
        self,
        result: DatasetProcessingResult,
        config: ProcessingConfig,
        output_dir: Path,
    ) -> None:
        self.calls.append((result, config, output_dir))


class FakeReportCalculator(ReportCalculator):
    def __init__(self, summary: ProcessingSummary) -> None:
        self.summary = summary
        self.calls: list[tuple[Path, DatasetProcessingResult]] = []

    def calculate(
        self,
        input_path: Path,
        result: DatasetProcessingResult,
    ) -> ProcessingSummary:
        self.calls.append((input_path, result))
        return self.summary
