"""Process one source row through Stage 2 normalization and validation."""

from csv_data_cleaner.application.mappers import RowResultMapper
from csv_data_cleaner.application.normalization import (
    DateRowNormalizer,
    StringRowNormalizer,
)
from csv_data_cleaner.application.validation import RowValidator
from csv_data_cleaner.domain import DataRow, ProcessingConfig, RowProcessingResult


class RowProcessor:
    """Orchestrate staged normalization, validation, and result mapping."""

    def __init__(
        self,
        string_normalizer: StringRowNormalizer,
        date_normalizer: DateRowNormalizer,
        validator: RowValidator,
        result_mapper: RowResultMapper,
    ) -> None:
        self.string_normalizer = string_normalizer
        self.date_normalizer = date_normalizer
        self.validator = validator
        self.result_mapper = result_mapper

    def process(self, source_row: DataRow, config: ProcessingConfig) -> RowProcessingResult:
        validation_row = self.string_normalizer.normalize(
            source_row,
            config.normalization,
        )
        issues = self.validator.validate(validation_row, config)
        normalized_row = self.date_normalizer.normalize(
            validation_row,
            config.date_rules,
            config.normalization,
        )
        return self.result_mapper.map(source_row, normalized_row, issues)
