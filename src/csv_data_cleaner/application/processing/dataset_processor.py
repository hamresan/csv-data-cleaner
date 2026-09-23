"""Process canonical input rows through normalization, validation, and deduplication."""

from csv_data_cleaner.application.deduplication import RowDeduplicator
from csv_data_cleaner.application.processing.row_processor import RowProcessor
from csv_data_cleaner.domain import (
    DatasetProcessingResult,
    InputData,
    ProcessingConfig,
)


class DatasetProcessor:
    """Process input rows in source order and apply configured deduplication."""

    def __init__(
        self,
        row_processor: RowProcessor,
        row_deduplicator: RowDeduplicator,
    ) -> None:
        self.row_processor = row_processor
        self.row_deduplicator = row_deduplicator

    def process(
        self,
        input_data: InputData,
        config: ProcessingConfig,
    ) -> DatasetProcessingResult:
        processed_rows = tuple(
            self.row_processor.process(source_row=row, config=config) for row in input_data.rows
        )
        if config.deduplication is None:
            return DatasetProcessingResult(rows=processed_rows)

        deduplication_result = self.row_deduplicator.deduplicate(
            processed_rows,
            config.deduplication,
        )
        return DatasetProcessingResult(
            rows=deduplication_result.retained_rows,
            duplicate_rows=deduplication_result.duplicate_rows,
        )
