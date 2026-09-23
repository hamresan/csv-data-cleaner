"""Parse date strings using explicit configured formats."""

from datetime import datetime


class DateParser:
    """Parse deterministic date formats without inference."""

    def parse(self, value: str, formats: tuple[str, ...]) -> datetime | None:
        for date_format in formats:
            try:
                return datetime.strptime(value, date_format)
            except ValueError:
                continue
        return None
