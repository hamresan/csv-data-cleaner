"""Validate configured filters against the input schema."""

from csv_data_cleaner.domain import FilterRule, InputData
from csv_data_cleaner.domain.errors import InputDataError


class FilterSchemaValidator:
    """Ensure all configured filter columns exist."""

    def validate(self, input_data: InputData, rules: tuple[FilterRule, ...]) -> None:
        missing_columns = tuple(
            rule.column for rule in rules if rule.column not in input_data.columns
        )
        if missing_columns:
            columns = ", ".join(dict.fromkeys(missing_columns))
            raise InputDataError(f"Missing filter columns: {columns}")
