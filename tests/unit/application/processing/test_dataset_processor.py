"""Behavioral tests for dataset processing orchestration."""

from tests.unit.application.validation.fakes import FakeEmailSyntaxChecker

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
from csv_data_cleaner.application.validation import (
    DateValueValidator,
    EmailValueValidator,
    RequiredValueValidator,
    RowValidator,
)
from csv_data_cleaner.domain import (
    DataRow,
    DateValidationRule,
    DeduplicationPolicy,
    InputData,
    NormalizationPolicy,
    OutputFormat,
    ProcessingConfig,
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
                email_validator=EmailValueValidator(
                    syntax_checker=FakeEmailSyntaxChecker({"ada@example.com"})
                ),
                date_validator=DateValueValidator(date_parser=date_parser),
            ),
            result_mapper=RowResultMapper(),
        ),
        row_deduplicator=RowDeduplicator(),
        deduplication_schema_validator=DeduplicationSchemaValidator(),
    )


def build_config(
    deduplication: DeduplicationPolicy | None = None,
) -> ProcessingConfig:
    return ProcessingConfig(
        required_columns=("name", "email"),
        email_columns=("email",),
        date_rules=(
            DateValidationRule(
                column="created_at",
                formats=("%d/%m/%Y",),
            ),
        ),
        normalization=NormalizationPolicy(date_output_format="%Y.%m.%d"),
        deduplication=deduplication,
        sorting=(),
        output_format=OutputFormat.CSV,
    )


def test_processor_separates_rows_and_preserves_source_values() -> None:
    input_data = InputData(
        columns=("name", "email", "created_at"),
        rows=(
            DataRow(
                number=2,
                values={
                    "name": " Ada ",
                    "email": " ada@example.com ",
                    "created_at": "23/09/2026",
                },
            ),
            DataRow(
                number=3,
                values={
                    "name": " ",
                    "email": "bad-email",
                    "created_at": "31/02/2026",
                },
            ),
        ),
    )

    result = build_processor().process(input_data, build_config())

    assert len(result.valid_rows) == 1
    assert result.valid_rows[0].normalized_row.values["created_at"] == "2026.09.23"
    assert len(result.invalid_rows) == 1
    assert [(issue.column, issue.code) for issue in result.invalid_rows[0].issues] == [
        ("name", "required"),
        ("email", "invalid_email"),
        ("created_at", "invalid_date"),
    ]
    assert result.invalid_rows[0].source_row.values["created_at"] == "31/02/2026"
    assert result.duplicate_rows == ()


def test_processor_deduplicates_after_normalization_and_validation() -> None:
    input_data = InputData(
        columns=("name", "email", "created_at"),
        rows=(
            DataRow(
                number=2,
                values={
                    "name": "Ada",
                    "email": " ada@example.com ",
                    "created_at": "23/09/2026",
                },
            ),
            DataRow(
                number=3,
                values={
                    "name": "Ada duplicate",
                    "email": "ada@example.com",
                    "created_at": "23/09/2026",
                },
            ),
        ),
    )

    result = build_processor().process(
        input_data,
        build_config(deduplication=DeduplicationPolicy(columns=("email",))),
    )

    assert tuple(row.source_row.number for row in result.rows) == (2,)
    assert len(result.duplicate_rows) == 1
    duplicate = result.duplicate_rows[0]
    assert duplicate.row.source_row.number == 3
    assert duplicate.retained_row_number == 2
    assert duplicate.key == ("ada@example.com",)


def test_processor_counts_invalid_duplicate_only_as_duplicate_after_deduplication() -> None:
    input_data = InputData(
        columns=("name", "email", "created_at"),
        rows=(
            DataRow(
                number=2,
                values={
                    "name": "First invalid",
                    "email": "bad-email",
                    "created_at": "23/09/2026",
                },
            ),
            DataRow(
                number=3,
                values={
                    "name": "Duplicate invalid",
                    "email": "bad-email",
                    "created_at": "23/09/2026",
                },
            ),
        ),
    )

    result = build_processor().process(
        input_data,
        build_config(deduplication=DeduplicationPolicy(columns=("email",))),
    )

    assert len(result.rows) == 1
    assert len(result.invalid_rows) == 1
    assert result.invalid_rows[0].source_row.number == 2
    assert len(result.duplicate_rows) == 1
    duplicate = result.duplicate_rows[0]
    assert duplicate.row.source_row.number == 3
    assert not duplicate.row.is_valid
    assert duplicate.retained_row_number == 2
    assert len(result.invalid_rows) + len(result.duplicate_rows) == 2

