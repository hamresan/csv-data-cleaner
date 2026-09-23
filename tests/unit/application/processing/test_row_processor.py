"""Behavioral tests for Stage 2 row processing orchestration."""

from tests.unit.application.validation.fakes import FakeEmailSyntaxChecker

from csv_data_cleaner.application.dates import DateParser
from csv_data_cleaner.application.mappers import RowResultMapper
from csv_data_cleaner.application.normalization import (
    DateRowNormalizer,
    DateValueNormalizer,
    StringRowNormalizer,
    StringValueNormalizer,
)
from csv_data_cleaner.application.processing import RowProcessor
from csv_data_cleaner.application.validation import (
    DateValueValidator,
    EmailValueValidator,
    RequiredValueValidator,
    RowValidator,
)
from csv_data_cleaner.domain import (
    DataRow,
    DateValidationRule,
    NormalizationPolicy,
    OutputFormat,
    ProcessingConfig,
)


def build_processor() -> RowProcessor:
    return RowProcessor(
        string_normalizer=StringRowNormalizer(
            value_normalizer=StringValueNormalizer(),
        ),
        date_normalizer=DateRowNormalizer(
            value_normalizer=DateValueNormalizer(date_parser=DateParser()),
        ),
        validator=RowValidator(
            required_validator=RequiredValueValidator(),
            email_validator=EmailValueValidator(
                syntax_checker=FakeEmailSyntaxChecker({"user@example.com"})
            ),
            date_validator=DateValueValidator(date_parser=DateParser()),
        ),
        result_mapper=RowResultMapper(),
    )


def build_config() -> ProcessingConfig:
    return ProcessingConfig(
        required_columns=("name", "email"),
        email_columns=("email",),
        date_rules=(
            DateValidationRule(
                column="created_at",
                formats=("%Y-%m-%d", "%d/%m/%Y"),
            ),
        ),
        normalization=NormalizationPolicy(),
        deduplication=None,
        filters=(),
        sorting=(),
        output_format=OutputFormat.CSV,
    )


def test_processor_validates_source_then_returns_normalized_row() -> None:
    source = DataRow(
        number=2,
        values={
            "name": "  مهران  ",
            "email": " user@example.com ",
            "created_at": "23/09/2026",
        },
    )

    result = build_processor().process(source, build_config())

    assert result.is_valid is True
    assert result.normalized_row.values == {
        "name": "مهران",
        "email": "user@example.com",
        "created_at": "2026-09-23",
    }
    assert result.source_row is source
    assert source.values["name"] == "  مهران  "


def test_processor_applies_configured_case_normalization_and_preserves_source() -> None:
    config = build_config()
    config = ProcessingConfig(
        required_columns=config.required_columns,
        email_columns=config.email_columns,
        date_rules=config.date_rules,
        normalization=NormalizationPolicy(casefold_columns=("email",)),
        deduplication=config.deduplication,
        filters=config.filters,
        sorting=config.sorting,
        output_format=config.output_format,
    )
    source = DataRow(
        number=3,
        values={
            "name": "  Ada Lovelace  ",
            "email": "  USER@EXAMPLE.COM  ",
            "created_at": "2026-09-23",
        },
    )

    result = build_processor().process(source, config)

    assert result.is_valid is True
    assert result.normalized_row.values["name"] == "Ada Lovelace"
    assert result.normalized_row.values["email"] == "user@example.com"
    assert result.source_row is source
    assert source.values["email"] == "  USER@EXAMPLE.COM  "


def test_processor_returns_all_issues_with_original_invalid_row() -> None:
    source = DataRow(
        number=11,
        values={
            "name": "   ",
            "email": " bad-email ",
            "created_at": "31/02/2026",
        },
    )

    result = build_processor().process(source, build_config())

    assert result.is_valid is False
    assert [(issue.column, issue.code) for issue in result.issues] == [
        ("name", "required"),
        ("email", "invalid_email"),
        ("created_at", "invalid_date"),
    ]
    assert result.source_row.values == {
        "name": "   ",
        "email": " bad-email ",
        "created_at": "31/02/2026",
    }
    assert result.normalized_row.values == {
        "name": None,
        "email": "bad-email",
        "created_at": "31/02/2026",
    }


def test_processor_does_not_validate_canonical_date_against_source_formats() -> None:
    config = ProcessingConfig(
        required_columns=(),
        email_columns=(),
        date_rules=(DateValidationRule("created_at", ("%d/%m/%Y",)),),
        normalization=NormalizationPolicy(date_output_format="%Y.%m.%d"),
        deduplication=None,
        filters=(),
        sorting=(),
        output_format=OutputFormat.CSV,
    )
    source = DataRow(number=2, values={"created_at": "23/09/2026"})

    result = build_processor().process(source, config)

    assert result.is_valid is True
    assert result.normalized_row.values["created_at"] == "2026.09.23"
