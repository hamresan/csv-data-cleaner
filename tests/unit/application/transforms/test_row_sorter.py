"""Behavioral tests for ordered row sorting."""

from csv_data_cleaner.application.transforms import RowSorter
from csv_data_cleaner.domain import DataRow, RowProcessingResult, SortRule


def row(number: int, **values: object) -> RowProcessingResult:
    data = DataRow(number=number, values=values)
    return RowProcessingResult(source_row=data, normalized_row=data, issues=())


def test_sorter_applies_multiple_rules_in_declared_order() -> None:
    rows = (
        row(2, country="OM", name="B"),
        row(3, country="US", name="A"),
        row(4, country="OM", name="A"),
    )

    result = RowSorter().sort(
        rows,
        (
            SortRule("country", ascending=True),
            SortRule("name", ascending=False),
        ),
    )

    assert tuple(item.source_row.number for item in result) == (2, 4, 3)


def test_sorter_preserves_tie_order_and_handles_null() -> None:
    rows = (
        row(2, score=None),
        row(3, score=10),
        row(4, score=10),
    )

    result = RowSorter().sort(rows, (SortRule("score"),))

    assert tuple(item.source_row.number for item in result) == (3, 4, 2)
