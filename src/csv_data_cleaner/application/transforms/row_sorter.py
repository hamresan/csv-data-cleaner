"""Ordered stable sorting for processed rows."""

from csv_data_cleaner.domain import CellValue, RowProcessingResult, SortRule


class SortValueKeyBuilder:
    """Build deterministic comparable keys for canonical cell values."""

    def build(self, value: CellValue) -> tuple[int, str, object]:
        if value is None:
            return (1, "", "")
        if isinstance(value, bool):
            return (0, "bool", value)
        if isinstance(value, int | float):
            return (0, "number", float(value))
        return (0, "string", str(value))


class RowSorter:
    """Sort rows by configured rules while preserving stable tie order."""

    def __init__(self, key_builder: SortValueKeyBuilder) -> None:
        self.key_builder = key_builder

    def sort(
        self,
        rows: tuple[RowProcessingResult, ...],
        rules: tuple[SortRule, ...],
    ) -> tuple[RowProcessingResult, ...]:
        result = list(rows)
        for rule in reversed(rules):
            result.sort(
                key=lambda row, column=rule.column: self.key_builder.build(
                    row.normalized_row.values[column]
                ),
                reverse=not rule.ascending,
            )
        return tuple(result)
