"""Behavioral tests for configurable row deduplication."""

from csv_data_cleaner.application.deduplication import RowDeduplicator
from csv_data_cleaner.domain import (
    DataRow,
    DeduplicationKeep,
    DeduplicationPolicy,
    ValidationIssue,
)
from csv_data_cleaner.domain.row_processing import RowProcessingResult


def build_row(
    number: int,
    *,
    email: str | None,
    country: str | None = None,
    issues: tuple[ValidationIssue, ...] = (),
) -> RowProcessingResult:
    row = DataRow(number=number, values={"email": email, "country": country})
    return RowProcessingResult(source_row=row, normalized_row=row, issues=issues)


def test_deduplicates_single_key_and_keeps_first_row() -> None:
    rows = (
        build_row(2, email="ada@example.com"),
        build_row(3, email="grace@example.com"),
        build_row(4, email="ada@example.com"),
    )

    result = RowDeduplicator().deduplicate(
        rows,
        DeduplicationPolicy(columns=("email",), keep=DeduplicationKeep.FIRST),
    )

    assert tuple(row.source_row.number for row in result.retained_rows) == (2, 3)
    assert len(result.duplicate_rows) == 1
    assert result.duplicate_rows[0].row.source_row.number == 4
    assert result.duplicate_rows[0].retained_row_number == 2
    assert result.duplicate_rows[0].key == ("ada@example.com",)


def test_deduplicates_single_key_and_keeps_last_row() -> None:
    rows = (
        build_row(2, email="ada@example.com"),
        build_row(3, email="grace@example.com"),
        build_row(4, email="ada@example.com"),
    )

    result = RowDeduplicator().deduplicate(
        rows,
        DeduplicationPolicy(columns=("email",), keep=DeduplicationKeep.LAST),
    )

    assert tuple(row.source_row.number for row in result.retained_rows) == (3, 4)
    assert result.duplicate_rows[0].row.source_row.number == 2
    assert result.duplicate_rows[0].retained_row_number == 4


def test_deduplicates_composite_keys() -> None:
    rows = (
        build_row(2, email="ada@example.com", country="UK"),
        build_row(3, email="ada@example.com", country="US"),
        build_row(4, email="ada@example.com", country="UK"),
    )

    result = RowDeduplicator().deduplicate(
        rows,
        DeduplicationPolicy(columns=("email", "country")),
    )

    assert tuple(row.source_row.number for row in result.retained_rows) == (2, 3)
    assert result.duplicate_rows[0].key == ("ada@example.com", "UK")


def test_uses_normalized_values_for_duplicate_keys() -> None:
    source_first = DataRow(number=2, values={"email": " Ada@Example.com "})
    normalized_first = DataRow(number=2, values={"email": "ada@example.com"})
    source_second = DataRow(number=3, values={"email": "ada@example.com"})
    normalized_second = DataRow(number=3, values={"email": "ada@example.com"})
    rows = (
        RowProcessingResult(source_first, normalized_first, ()),
        RowProcessingResult(source_second, normalized_second, ()),
    )

    result = RowDeduplicator().deduplicate(
        rows,
        DeduplicationPolicy(columns=("email",)),
    )

    assert tuple(row.source_row.number for row in result.retained_rows) == (2,)
    assert result.duplicate_rows[0].retained_row_number == 2
    assert result.duplicate_rows[0].row.source_row.values["email"] == "ada@example.com"


def test_treats_equal_missing_keys_as_duplicates() -> None:
    rows = (
        build_row(2, email=None),
        build_row(3, email=None),
    )

    result = RowDeduplicator().deduplicate(
        rows,
        DeduplicationPolicy(columns=("email",)),
    )

    assert tuple(row.source_row.number for row in result.retained_rows) == (2,)
    assert result.duplicate_rows[0].row.source_row.number == 3
    assert result.duplicate_rows[0].key == (None,)


def test_duplicate_invalid_rows_preserve_validation_state() -> None:
    issue = ValidationIssue(
        row_number=2,
        column="email",
        code="invalid_email",
        message="Invalid email.",
    )
    rows = (
        build_row(2, email="bad-email", issues=(issue,)),
        build_row(3, email="bad-email", issues=(issue,)),
    )

    result = RowDeduplicator().deduplicate(
        rows,
        DeduplicationPolicy(columns=("email",)),
    )

    assert result.retained_rows[0].is_valid is False
    assert result.duplicate_rows[0].row.is_valid is False
    assert result.duplicate_rows[0].retained_row_number == 2
