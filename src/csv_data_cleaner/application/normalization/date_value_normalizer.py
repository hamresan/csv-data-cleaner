"""Normalize configured date values."""

from csv_data_cleaner.application.dates import DateParser
from csv_data_cleaner.domain import CellValue, DateValidationRule, NormalizationPolicy


class DateValueNormalizer:
    """Canonicalize parseable configured date strings without validating failures."""

    def __init__(self, date_parser: DateParser) -> None:
        self.date_parser = date_parser

    def normalize(
        self,
        value: CellValue,
        rule: DateValidationRule,
        policy: NormalizationPolicy,
    ) -> CellValue:
        if not isinstance(value, str) or value == "":
            return value

        parsed = self.date_parser.parse(value, rule.formats)
        if parsed is None:
            return value
        return parsed.strftime(policy.date_output_format)
