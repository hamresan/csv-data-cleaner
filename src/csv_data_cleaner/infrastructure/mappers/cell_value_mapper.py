"""Map physical table cell values to canonical domain values."""

from csv_data_cleaner.domain import CellValue


class CellValueMapper:
    """Convert physical table values to canonical cell values."""

    def map(self, value: object) -> CellValue:
        if value is None or (isinstance(value, float) and value != value):
            return None
        if isinstance(value, str | int | float | bool):
            return value
        return str(value)
