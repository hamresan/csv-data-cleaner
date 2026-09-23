"""Configuration-driven row filtering."""

from csv_data_cleaner.domain import FilterOperator, FilterRule, RowProcessingResult


class RowFilter:
    """Apply ordered inclusion and exclusion filters to processed rows."""

    def apply(
        self,
        rows: tuple[RowProcessingResult, ...],
        rules: tuple[FilterRule, ...],
    ) -> tuple[tuple[RowProcessingResult, ...], tuple[RowProcessingResult, ...]]:
        retained: list[RowProcessingResult] = []
        filtered: list[RowProcessingResult] = []

        for row in rows:
            if all(self._keeps(row, rule) for rule in rules):
                retained.append(row)
            else:
                filtered.append(row)

        return tuple(retained), tuple(filtered)

    def _keeps(self, row: RowProcessingResult, rule: FilterRule) -> bool:
        actual = row.normalized_row.values[rule.column]
        matches = actual == rule.value
        if rule.operator is FilterOperator.NOT_EQUALS:
            matches = not matches
        return matches if rule.include else not matches
