"""Integration tests for real CSV/XLSX output artifacts."""

from pathlib import Path

import pandas as pd
import pytest

from csv_data_cleaner.domain import (
    DataRow,
    DatasetProcessingResult,
    NormalizationPolicy,
    OutputFormat,
    ProcessingConfig,
    RowProcessingResult,
    ValidationIssue,
)
from csv_data_cleaner.domain.deduplication import DuplicateRow
from csv_data_cleaner.domain.errors import OutputDataError
from csv_data_cleaner.infrastructure.export import PandasResultExporter, ResultFrameMapper


def config(output_format: OutputFormat) -> ProcessingConfig:
    return ProcessingConfig(
        required_columns=(),
        email_columns=(),
        date_rules=(),
        normalization=NormalizationPolicy(),
        deduplication=None,
        filters=(),
        sorting=(),
        output_format=output_format,
    )


def row(
    number: int,
    source_name: str,
    normalized_name: str,
    *,
    valid: bool = True,
) -> RowProcessingResult:
    source = DataRow(number, {"name": source_name})
    normalized = DataRow(number, {"name": normalized_name})
    issues = () if valid else (ValidationIssue(number, "name", "invalid", "Invalid name."),)
    return RowProcessingResult(source, normalized, issues)


@pytest.mark.parametrize("output_format", [OutputFormat.CSV, OutputFormat.XLSX])
def test_exporter_writes_readable_cleaned_and_review_files(
    tmp_path: Path,
    output_format: OutputFormat,
) -> None:
    valid = row(2, " Ada ", "Ada")
    invalid = row(3, " Invalid ", "Invalid", valid=False)
    duplicate = row(4, " Duplicate ", "Duplicate")
    result = DatasetProcessingResult(
        rows=(valid, invalid),
        duplicate_rows=(DuplicateRow(duplicate, 2, ("Ada",)),),
        columns=("name",),
    )
    output_dir = tmp_path / "output"

    output_file = PandasResultExporter(ResultFrameMapper()).export(
        result,
        config(output_format),
        output_dir,
    )

    if output_format is OutputFormat.CSV:
        cleaned = pd.read_csv(output_file)
    else:
        cleaned = pd.read_excel(output_file, engine="openpyxl")
    invalid_rows = pd.read_csv(output_dir / "invalid_rows.csv")
    duplicate_rows = pd.read_csv(output_dir / "duplicate_rows.csv")

    assert cleaned.to_dict(orient="records") == [{"name": "Ada"}]
    assert invalid_rows.to_dict(orient="records") == [{"name": " Invalid "}]
    assert duplicate_rows.to_dict(orient="records") == [{"name": " Duplicate "}]


def test_exporter_writes_headers_for_empty_result_sets(tmp_path: Path) -> None:
    result = DatasetProcessingResult(rows=(), columns=("name", "email"))
    output_dir = tmp_path / "output"

    PandasResultExporter(ResultFrameMapper()).export(
        result,
        config(OutputFormat.CSV),
        output_dir,
    )

    assert (output_dir / "cleaned.csv").read_text(encoding="utf-8") == "name,email\n"
    assert (output_dir / "invalid_rows.csv").read_text(encoding="utf-8") == "name,email\n"
    assert (output_dir / "duplicate_rows.csv").read_text(encoding="utf-8") == "name,email\n"


def test_exporter_rejects_existing_output_directory(tmp_path: Path) -> None:
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    with pytest.raises(OutputDataError, match="Output directory already exists"):
        PandasResultExporter(ResultFrameMapper()).export(
            DatasetProcessingResult(rows=(), columns=("name",)),
            config(OutputFormat.CSV),
            output_dir,
        )
