"""Process canonical input rows through Stage 2 row processing."""

from csv_data_cleaner.application.processing.row_processor import RowProcessor
from csv_data_cleaner.domain import (
    DatasetProcessingResult,
    InputData,
    ProcessingConfig,
)


class DatasetProcessor:
    """Process input rows in source order and retain every row result."""

    def __init__(self, row_processor: RowProcessor) -> None:
        self.row_processor = row_processor

    def process(
        self,
        input_data: InputData,
        config: ProcessingConfig,
    ) -> DatasetProcessingResult:
        return DatasetProcessingResult(
            rows=tuple(
                self.row_processor.process(source_row=row, config=config) for row in input_data.rows
            )
        )
