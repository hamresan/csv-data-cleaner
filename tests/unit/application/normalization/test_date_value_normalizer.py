"""Behavioral tests for date value normalization."""

import pytest

from csv_data_cleaner.application.dates import DateParser
from csv_data_cleaner.application.normalization import DateValueNormalizer
from csv_data_cleaner.domain import CellValue, DateValidationRule, NormalizationPolicy


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("2026-09-23", "23/09/2026"),
        ("23-09-2026", "23/09/2026"),
        ("09/23/2026", "23/09/2026"),
    ],
)
def test_normalizer_canonicalizes_configured_date_formats(
    value: str,
    expected: str,
) -> None:
    rule = DateValidationRule(
        column="created_at",
        formats=("%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y"),
    )
    policy = NormalizationPolicy(date_output_format="%d/%m/%Y")

    result = DateValueNormalizer(date_parser=DateParser()).normalize(value, rule, policy)

    assert result == expected


@pytest.mark.parametrize("value", ["not-a-date", "2026/09/23", None, 42])
def test_normalizer_preserves_values_it_cannot_parse(value: CellValue) -> None:
    rule = DateValidationRule(column="created_at", formats=("%Y-%m-%d",))

    result = DateValueNormalizer(date_parser=DateParser()).normalize(
        value,
        rule,
        NormalizationPolicy(),
    )

    assert result == value
