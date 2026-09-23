"""Behavioral tests for deduplication domain results."""

from csv_data_cleaner.domain.deduplication import DeduplicationResult, DuplicateRow
from csv_data_cleaner.domain.input_data import DataRow
from csv_data_cleaner.domain.row_processing import RowProcessingResult


def build_row(number: int, email: str | None) -> RowProcessingResult:
    source_row = DataRow(number=number, values={"email": email})
    normalized_row = DataRow(number=number, values={"email": email})
    return RowProcessingResult(
        source_row=source_row,
        normalized_row=normalized_row,
        issues=(),
    )


def test_duplicate_row_preserves_dropped_row_retained_link_and_key() -> None:
    retained = build_row(2, "ada@example.com")
    dropped = build_row(5, "ada@example.com")

    duplicate = DuplicateRow(
        row=dropped,
        retained_row_number=retained.source_row.number,
        key=("ada@example.com",),
    )

    assert duplicate.row.source_row.number == 5
    assert duplicate.retained_row_number == 2
    assert duplicate.key == ("ada@example.com",)


def test_deduplication_result_keeps_retained_and_duplicate_rows_separate() -> None:
    retained = build_row(2, "ada@example.com")
    dropped = build_row(5, "ada@example.com")

    result = DeduplicationResult(
        retained_rows=(retained,),
        duplicate_rows=(
            DuplicateRow(
                row=dropped,
                retained_row_number=retained.source_row.number,
                key=("ada@example.com",),
            ),
        ),
    )

    assert result.retained_rows == (retained,)
    assert tuple(item.row for item in result.duplicate_rows) == (dropped,)
