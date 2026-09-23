"""Behavioral parity tests for deduplication across real CSV/XLSX inputs."""

import csv
from pathlib import Path

from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from csv_data_cleaner.application.dates import DateParser
from csv_data_cleaner.application.deduplication import RowDeduplicator
from csv_data_cleaner.application.mappers import RowResultMapper
from csv_data_cleaner.application.normalization import (
    DateRowNormalizer,
    DateValueNormalizer,
    StringRowNormalizer,
    StringValueNormalizer,
)
from csv_data_cleaner.application.processing import DatasetProcessor, RowProcessor
from csv_data_cleaner.application.validation import (
    DateValueValidator,
    RequiredValueValidator,
    RowValidator,
)
from csv_data_cleaner.domain import (
    DeduplicationKeep,
    DeduplicationPolicy,
    NormalizationPolicy,
    OutputFormat,
    ProcessingConfig,
)
from csv_data_cleaner.infrastructure.input import PandasInputReader
from csv_data_cleaner.infrastructure.mappers.cell_value_mapper import CellValueMapper
from csv_data_cleaner.infrastructure.mappers.data_frame_input_mapper import DataFrameInputMapper
from csv_data_cleaner.infrastructure.validators.data_frame_header_validator import (
    DataFrameHeaderValidator,
)


def active_sheet(workbook: Workbook) -> Worksheet:
    worksheet = workbook.active
    assert worksheet is not None
    return worksheet


def write_inputs(tmp_path: Path) -> tuple[Path, Path]:
    rows = [
        ["name", "email", "country"],
        ["Ada", " ada@example.com ", "UK"],
        ["Grace", "grace@example.com", "US"],
        ["Ada duplicate", "ada@example.com", "UK"],
        ["Missing one", "", "OM"],
        ["Missing two", "", "OM"],
    ]

    csv_path = tmp_path / "customers.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as file:
        csv.writer(file).writerows(rows)

    xlsx_path = tmp_path / "customers.xlsx"
    workbook = Workbook()
    worksheet = active_sheet(workbook)
    for row in rows:
        worksheet.append([None if value == "" else value for value in row])
    workbook.save(xlsx_path)
    return csv_path, xlsx_path


def build_reader() -> PandasInputReader:
    return PandasInputReader(
        mapper=DataFrameInputMapper(
            header_validator=DataFrameHeaderValidator(),
            cell_value_mapper=CellValueMapper(),
        )
    )


def build_processor() -> DatasetProcessor:
    date_parser = DateParser()
    return DatasetProcessor(
        row_processor=RowProcessor(
            string_normalizer=StringRowNormalizer(
                value_normalizer=StringValueNormalizer(),
            ),
            date_normalizer=DateRowNormalizer(
                value_normalizer=DateValueNormalizer(date_parser=date_parser),
            ),
            validator=RowValidator(
                required_validator=RequiredValueValidator(),
                email_validator=None,
                date_validator=DateValueValidator(date_parser=date_parser),
            ),
            result_mapper=RowResultMapper(),
        ),
        row_deduplicator=RowDeduplicator(),
    )


def build_config(keep: DeduplicationKeep) -> ProcessingConfig:
    return ProcessingConfig(
        required_columns=("name",),
        email_columns=(),
        date_rules=(),
        normalization=NormalizationPolicy(),
        deduplication=DeduplicationPolicy(
            columns=("email", "country"),
            keep=keep,
        ),
        sorting=(),
        output_format=OutputFormat.CSV,
    )


def result_signature(path: Path, keep: DeduplicationKeep) -> tuple[object, ...]:
    result = build_processor().process(build_reader().read(path), build_config(keep))
    return (
        tuple(row.source_row.number for row in result.rows),
        tuple(
            (
                item.row.source_row.number,
                item.retained_row_number,
                item.key,
            )
            for item in result.duplicate_rows
        ),
    )


def test_csv_and_xlsx_have_same_first_retention_behavior(tmp_path: Path) -> None:
    csv_path, xlsx_path = write_inputs(tmp_path)

    csv_result = result_signature(csv_path, DeduplicationKeep.FIRST)
    xlsx_result = result_signature(xlsx_path, DeduplicationKeep.FIRST)

    assert csv_result == xlsx_result
    assert csv_result == (
        (2, 3, 5),
        (
            (4, 2, ("ada@example.com", "UK")),
            (6, 5, (None, "OM")),
        ),
    )


def test_csv_and_xlsx_have_same_last_retention_behavior(tmp_path: Path) -> None:
    csv_path, xlsx_path = write_inputs(tmp_path)

    csv_result = result_signature(csv_path, DeduplicationKeep.LAST)
    xlsx_result = result_signature(xlsx_path, DeduplicationKeep.LAST)

    assert csv_result == xlsx_result
    assert csv_result == (
        (3, 4, 6),
        (
            (2, 4, ("ada@example.com", "UK")),
            (5, 6, (None, "OM")),
        ),
    )
