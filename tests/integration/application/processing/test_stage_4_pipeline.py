"""Integration tests for the Stage 4 transform pipeline with real CSV input."""

import csv
from pathlib import Path

from csv_data_cleaner.application.dates import DateParser
from csv_data_cleaner.application.deduplication import (
    DeduplicationSchemaValidator,
    RowDeduplicator,
)
from csv_data_cleaner.application.mappers import RowResultMapper
from csv_data_cleaner.application.normalization import (
    DateRowNormalizer,
    DateValueNormalizer,
    StringRowNormalizer,
    StringValueNormalizer,
)
from csv_data_cleaner.application.processing import DatasetProcessor, RowProcessor
from csv_data_cleaner.application.transforms import (
    FilterRuleEvaluator,
    FilterSchemaValidator,
    FilterSortProcessor,
    RowFilter,
    RowSorter,
    SortSchemaValidator,
    SortValueKeyBuilder,
)
from csv_data_cleaner.application.validation import (
    DateValueValidator,
    EmailValueValidator,
    RequiredValueValidator,
    RowValidator,
)
from csv_data_cleaner.domain import (
    DeduplicationPolicy,
    FilterOperator,
    FilterRule,
    NormalizationPolicy,
    OutputFormat,
    ProcessingConfig,
    SortRule,
)
from csv_data_cleaner.infrastructure.input import PandasInputReader
from csv_data_cleaner.infrastructure.mappers.cell_value_mapper import CellValueMapper
from csv_data_cleaner.infrastructure.mappers.data_frame_input_mapper import DataFrameInputMapper
from csv_data_cleaner.infrastructure.validation import EmailValidatorSyntaxChecker
from csv_data_cleaner.infrastructure.validators.data_frame_header_validator import (
    DataFrameHeaderValidator,
)


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
            string_normalizer=StringRowNormalizer(StringValueNormalizer()),
            date_normalizer=DateRowNormalizer(DateValueNormalizer(date_parser)),
            validator=RowValidator(
                RequiredValueValidator(),
                EmailValueValidator(EmailValidatorSyntaxChecker()),
                DateValueValidator(date_parser),
            ),
            result_mapper=RowResultMapper(),
        ),
        row_deduplicator=RowDeduplicator(),
        deduplication_schema_validator=DeduplicationSchemaValidator(),
        filter_sort_processor=FilterSortProcessor(
            RowFilter(FilterRuleEvaluator()),
            RowSorter(SortValueKeyBuilder()),
        ),
        filter_schema_validator=FilterSchemaValidator(),
        sort_schema_validator=SortSchemaValidator(),
    )


def test_real_csv_pipeline_produces_valid_invalid_duplicate_and_filtered_sets(
    tmp_path: Path,
) -> None:
    path = tmp_path / "customers.csv"
    with path.open("w", encoding="utf-8", newline="") as file:
        csv.writer(file).writerows(
            [
                ["name", "email", "country"],
                ["Bob", "bob@example.com", "OM"],
                ["Ada", "ada@example.com", "OM"],
                ["Ada duplicate", " ADA@example.com ", "OM"],
                ["Invalid", "bad-email", "OM"],
                ["Grace", "grace@example.com", "US"],
            ]
        )

    config = ProcessingConfig(
        required_columns=("name", "email"),
        email_columns=("email",),
        date_rules=(),
        normalization=NormalizationPolicy(casefold_columns=("email",)),
        deduplication=DeduplicationPolicy(columns=("email",)),
        filters=(FilterRule("country", FilterOperator.EQUALS, "OM"),),
        sorting=(SortRule("name"),),
        output_format=OutputFormat.CSV,
    )

    result = build_processor().process(build_reader().read(path), config)

    assert tuple(row.source_row.number for row in result.valid_rows) == (3, 2)
    assert tuple(row.source_row.number for row in result.invalid_rows) == (5,)
    assert tuple(item.row.source_row.number for item in result.duplicate_rows) == (4,)
    assert tuple(row.source_row.number for row in result.filtered_rows) == (6,)


def test_real_csv_pipeline_supports_empty_filtered_result(tmp_path: Path) -> None:
    path = tmp_path / "customers.csv"
    path.write_text("name,country\nAda,OM\nGrace,US\n", encoding="utf-8")
    config = ProcessingConfig(
        required_columns=("name",),
        email_columns=(),
        date_rules=(),
        normalization=NormalizationPolicy(),
        deduplication=None,
        filters=(FilterRule("country", FilterOperator.EQUALS, "AE"),),
        sorting=(SortRule("name"),),
        output_format=OutputFormat.CSV,
    )

    result = build_processor().process(build_reader().read(path), config)

    assert result.rows == ()
    assert tuple(row.source_row.number for row in result.filtered_rows) == (2, 3)
