"""Behavioral tests for row filtering."""

from csv_data_cleaner.application.transforms import FilterRuleEvaluator, RowFilter
from csv_data_cleaner.domain import DataRow, FilterOperator, FilterRule, RowProcessingResult


def row(number: int, **values: object) -> RowProcessingResult:
    data = DataRow(number=number, values=values)
    return RowProcessingResult(source_row=data, normalized_row=data, issues=())


def test_filter_applies_inclusion_and_exclusion_rules() -> None:
    rows = (
        row(2, country="OM", active=True),
        row(3, country="US", active=True),
        row(4, country="OM", active=False),
    )
    rules = (
        FilterRule("country", FilterOperator.EQUALS, "OM"),
        FilterRule("active", FilterOperator.EQUALS, False, include=False),
    )

    retained, filtered = RowFilter(FilterRuleEvaluator()).apply(rows, rules)

    assert tuple(item.source_row.number for item in retained) == (2,)
    assert tuple(item.source_row.number for item in filtered) == (3, 4)


def test_filter_supports_empty_result() -> None:
    rows = (row(2, country="OM"),)
    rules = (FilterRule("country", FilterOperator.EQUALS, "US"),)

    retained, filtered = RowFilter(FilterRuleEvaluator()).apply(rows, rules)

    assert retained == ()
    assert filtered == rows
