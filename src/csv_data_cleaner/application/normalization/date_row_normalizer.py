"""Normalize configured date values in canonical input rows."""

from csv_data_cleaner.application.normalization.date_value_normalizer import DateValueNormalizer
from csv_data_cleaner.domain import (
    DataRow,
    DateValidationRule,
    NormalizationPolicy,
)


class DateRowNormalizer:
    """Canonicalize configured date columns after validation."""

    def __init__(self, value_normalizer: DateValueNormalizer) -> None:
        self.value_normalizer = value_normalizer

    def normalize(
        self,
        row: DataRow,
        rules: tuple[DateValidationRule, ...],
        policy: NormalizationPolicy,
    ) -> DataRow:
        values = dict(row.values)
        for rule in rules:
            if rule.column not in values:
                continue
            values[rule.column] = self.value_normalizer.normalize(
                values[rule.column],
                rule,
                policy,
            )
        return DataRow(number=row.number, values=values)
