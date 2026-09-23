"""Process canonical input rows through the Stage 4 transformation pipeline."""

from csv_data_cleaner.application.deduplication import (
    DeduplicationSchemaValidator,
    RowDeduplicator,
)
from csv_data_cleaner.application.processing.row_processor import RowProcessor
from csv_data_cleaner.application.transforms import (
    FilterSchemaValidator,
    FilterSortProcessor,
    SortSchemaValidator,
)
from csv_data_cleaner.domain import (
    DatasetProcessingResult,
    InputData,
    ProcessingConfig,
)


class DatasetProcessor:
    """Process input rows through normalize/validate, deduplicate, filter, and sort."""

    def __init__(
        self,
        row_processor: RowProcessor,
        row_deduplicator: RowDeduplicator,
        deduplication_schema_validator: DeduplicationSchemaValidator,
        filter_sort_processor: FilterSortProcessor,
        filter_schema_validator: FilterSchemaValidator,
        sort_schema_validator: SortSchemaValidator,
    ) -> None:
        self.row_processor = row_processor
        self.row_deduplicator = row_deduplicator
        self.deduplication_schema_validator = deduplication_schema_validator
        self.filter_sort_processor = filter_sort_processor
        self.filter_schema_validator = filter_schema_validator
        self.sort_schema_validator = sort_schema_validator

    def process(
        self,
        input_data: InputData,
        config: ProcessingConfig,
    ) -> DatasetProcessingResult:
        if config.deduplication is not None:
            self.deduplication_schema_validator.validate(input_data, config.deduplication)
        self.filter_schema_validator.validate(input_data, config.filters)
        self.sort_schema_validator.validate(input_data, config.sorting)

        processed_rows = tuple(
            self.row_processor.process(source_row=row, config=config) for row in input_data.rows
        )

        duplicate_rows = ()
        retained_rows = processed_rows
        if config.deduplication is not None:
            deduplication_result = self.row_deduplicator.deduplicate(
                processed_rows,
                config.deduplication,
            )
            retained_rows = deduplication_result.retained_rows
            duplicate_rows = deduplication_result.duplicate_rows

        transformed_rows, filtered_rows = self.filter_sort_processor.process(
            retained_rows,
            config.filters,
            config.sorting,
        )
        return DatasetProcessingResult(
            rows=transformed_rows,
            duplicate_rows=duplicate_rows,
            filtered_rows=filtered_rows,
        )
