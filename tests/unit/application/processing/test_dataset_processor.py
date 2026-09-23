"""Behavioral tests for Stage 2 dataset processing orchestration."""

from tests.unit.application.validation.fakes import FakeEmailSyntaxChecker

from csv_data_cleaner.application.dates import DateParser
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
        )
    )


def build_config() -> ProcessingConfig:
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
        deduplication=None,
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
