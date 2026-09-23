"""Validate configured sorting rules against the input schema."""

from csv_data_cleaner.domain import InputData, SortRule
from csv_data_cleaner.domain.errors import InputDataError


class SortSchemaValidator:
    """Ensure all configured sort columns exist."""

    def validate(self, input_data: InputData, rules: tuple[SortRule, ...]) -> None:
        missing_columns = tuple(
            rule.column for rule in rules if rule.column not in input_data.columns
        )
        if missing_columns:
            columns = ", ".join(dict.fromkeys(missing_columns))
            raise InputDataError(f"Missing sorting columns: {columns}")
