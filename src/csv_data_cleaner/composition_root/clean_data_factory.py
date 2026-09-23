"""Build the clean-data use case and its concrete adapters."""

from csv_data_cleaner.application.dates import DateParser
from csv_data_cleaner.application.deduplication import (
    DeduplicationSchemaValidator,
    RowDeduplicator,
)
from csv_data_cleaner.application.mappers import RowResultMapper
from csv_data_cleaner.application.normalization import (
    DateRowNormalizer,
    DateValueNormalizer,
    StringRowNormalizer,
    StringValueNormalizer,
)
from csv_data_cleaner.application.pipeline import CleanDataUseCase
from csv_data_cleaner.application.processing import DatasetProcessor, RowProcessor
from csv_data_cleaner.application.reporting import ProcessingReportCalculator
from csv_data_cleaner.application.transforms import (
    FilterRuleEvaluator,
    FilterSchemaValidator,
    FilterSortProcessor,
    RowFilter,
    RowSorter,
    SortSchemaValidator,
    SortValueKeyBuilder,
)
from csv_data_cleaner.application.validation import (
    DateValueValidator,
    EmailValueValidator,
    RequiredValueValidator,
    RowValidator,
)
from csv_data_cleaner.infrastructure.config import FileConfigLoader
from csv_data_cleaner.infrastructure.export import PandasResultExporter, ResultFrameMapper
from csv_data_cleaner.infrastructure.factories.config_parser_factory import ConfigParserFactory
from csv_data_cleaner.infrastructure.input import PandasInputReader
from csv_data_cleaner.infrastructure.mappers.cell_value_mapper import CellValueMapper
from csv_data_cleaner.infrastructure.mappers.data_frame_input_mapper import DataFrameInputMapper
from csv_data_cleaner.infrastructure.mappers.processing_config_mapper import ProcessingConfigMapper
from csv_data_cleaner.infrastructure.reporting import JsonReportWriter
from csv_data_cleaner.infrastructure.validation import EmailValidatorSyntaxChecker
from csv_data_cleaner.infrastructure.validators.config_field_validator import ConfigFieldValidator
from csv_data_cleaner.infrastructure.validators.config_value_validator import ConfigValueValidator
from csv_data_cleaner.infrastructure.validators.data_frame_header_validator import (
    DataFrameHeaderValidator,
)
from csv_data_cleaner.infrastructure.validators.processing_config_validator import (
    ProcessingConfigValidator,
)


def build_clean_data_use_case() -> CleanDataUseCase:
    """Wire concrete dependencies for the clean command."""
    date_parser = DateParser()
    row_processor = RowProcessor(
        string_normalizer=StringRowNormalizer(StringValueNormalizer()),
        date_normalizer=DateRowNormalizer(DateValueNormalizer(date_parser)),
        validator=RowValidator(
            RequiredValueValidator(),
            EmailValueValidator(EmailValidatorSyntaxChecker()),
            DateValueValidator(date_parser),
        ),
        result_mapper=RowResultMapper(),
    )
    dataset_processor = DatasetProcessor(
        row_processor=row_processor,
        row_deduplicator=RowDeduplicator(),
        deduplication_schema_validator=DeduplicationSchemaValidator(),
        filter_sort_processor=FilterSortProcessor(
            RowFilter(FilterRuleEvaluator()),
            RowSorter(SortValueKeyBuilder()),
        ),
        filter_schema_validator=FilterSchemaValidator(),
        sort_schema_validator=SortSchemaValidator(),
    )
    config_loader = FileConfigLoader(
        ConfigParserFactory(),
        ConfigValueValidator(),
        ProcessingConfigValidator(ConfigFieldValidator()),
        ProcessingConfigMapper(),
    )
    input_reader = PandasInputReader(
        DataFrameInputMapper(DataFrameHeaderValidator(), CellValueMapper())
    )
    return CleanDataUseCase(
        config_loader=config_loader,
        input_reader=input_reader,
        dataset_processor=dataset_processor,
        exporter=PandasResultExporter(ResultFrameMapper()),
        report_calculator=ProcessingReportCalculator(),
        report_writer=JsonReportWriter(),
    )
