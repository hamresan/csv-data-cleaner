"""Configuration-driven row filtering."""

from csv_data_cleaner.domain import FilterOperator, FilterRule, RowProcessingResult


class FilterRuleEvaluator:
    """Evaluate one filter rule against one processed row."""

    def matches(self, row: RowProcessingResult, rule: FilterRule) -> bool:
        actual = row.normalized_row.values[rule.column]
        matches = actual == rule.value
        if rule.operator is FilterOperator.NOT_EQUALS:
            matches = not matches
        return matches if rule.include else not matches


class RowFilter:
    """Apply ordered inclusion and exclusion filters to processed rows."""

    def __init__(self, evaluator: FilterRuleEvaluator) -> None:
        self.evaluator = evaluator

    def apply(
        self,
        rows: tuple[RowProcessingResult, ...],
        rules: tuple[FilterRule, ...],
    ) -> tuple[tuple[RowProcessingResult, ...], tuple[RowProcessingResult, ...]]:
        retained: list[RowProcessingResult] = []
        filtered: list[RowProcessingResult] = []

        for row in rows:
            if all(self.evaluator.matches(row, rule) for rule in rules):
                retained.append(row)
            else:
                filtered.append(row)

        return tuple(retained), tuple(filtered)
