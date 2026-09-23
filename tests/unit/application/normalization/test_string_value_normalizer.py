"""Behavioral tests for string value normalization."""

import pytest

from csv_data_cleaner.application.normalization import StringValueNormalizer
from csv_data_cleaner.domain import NormalizationPolicy


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("  Ada Lovelace  ", "Ada Lovelace"),
        ("  علی  ", "علی"),
        ("   ", None),
        ("", None),
        (42, 42),
        (True, True),
        (None, None),
    ],
)
def test_normalizer_applies_default_string_policy(value: object, expected: object) -> None:
    result = StringValueNormalizer().normalize(value, NormalizationPolicy())  # type: ignore[arg-type]

    assert result == expected


def test_normalizer_respects_disabled_string_rules() -> None:
    policy = NormalizationPolicy(
        trim_whitespace=False,
        empty_strings_as_null=False,
    )

    assert StringValueNormalizer().normalize("  ", policy) == "  "
