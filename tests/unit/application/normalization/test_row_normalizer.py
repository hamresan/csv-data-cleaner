"""Behavioral tests for staged row normalization."""

from csv_data_cleaner.application.dates import DateParser
from csv_data_cleaner.application.normalization import (
    DateRowNormalizer,
    DateValueNormalizer,
    StringRowNormalizer,
    StringValueNormalizer,
)
from csv_data_cleaner.domain import (
    DataRow,
    DateValidationRule,
    NormalizationPolicy,
)


def test_string_row_normalizer_preserves_source_and_non_ascii_text() -> None:
    source = DataRow(
        number=7,
        values={"name": "  مهران  ", "note": "   "},
    )

    result = StringRowNormalizer(value_normalizer=StringValueNormalizer()).normalize(
        source, NormalizationPolicy()
    )

    assert result.values == {"name": "مهران", "note": None}
    assert source.values == {"name": "  مهران  ", "note": "   "}


def test_date_row_normalizer_canonicalizes_configured_dates() -> None:
    source = DataRow(
        number=7,
        values={"created_at": "23/09/2026", "name": "Ada"},
    )
    rules = (DateValidationRule("created_at", ("%d/%m/%Y",)),)

    result = DateRowNormalizer(
        value_normalizer=DateValueNormalizer(date_parser=DateParser())
    ).normalize(
        source,
        rules,
        NormalizationPolicy(date_output_format="%Y-%m-%d"),
    )

    assert result.values == {"created_at": "2026-09-23", "name": "Ada"}
    assert source.values["created_at"] == "23/09/2026"
