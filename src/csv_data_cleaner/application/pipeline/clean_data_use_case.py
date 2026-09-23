"""Top-level cleaning pipeline orchestration."""

from csv_data_cleaner.application.pipeline.clean_data_request import CleanDataRequest
from csv_data_cleaner.application.pipeline.clean_data_result import CleanDataResult
from csv_data_cleaner.application.ports import (
    ConfigLoader,
    Exporter,
    InputReader,
    ReportCalculator,
    ReportWriter,
)
from csv_data_cleaner.application.processing import DatasetProcessor


class CleanDataUseCase:
    """Compose the complete pipeline while delegating every responsibility."""

    def __init__(
        self,
        config_loader: ConfigLoader,
        input_reader: InputReader,
        dataset_processor: DatasetProcessor,
        exporter: Exporter,
        report_calculator: ReportCalculator,
        report_writer: ReportWriter,
    ) -> None:
        self.config_loader = config_loader
        self.input_reader = input_reader
        self.dataset_processor = dataset_processor
        self.exporter = exporter
        self.report_calculator = report_calculator
        self.report_writer = report_writer

    def execute(self, request: CleanDataRequest) -> CleanDataResult:
        config = self.config_loader.load(request.config_path)
        input_data = self.input_reader.read(request.input_path, sheet=request.sheet)
        processing_result = self.dataset_processor.process(input_data, config)

        if request.dry_run:
            summary = self.report_calculator.calculate(
                request.input_path,
                processing_result,
                None,
            )
            return CleanDataResult(processing_result=processing_result, summary=summary)

        output_file = self.exporter.export(processing_result, config, request.output_dir)
        summary = self.report_calculator.calculate(
            request.input_path,
            processing_result,
            output_file,
        )
        self.report_writer.write(summary, request.output_dir)
        return CleanDataResult(processing_result=processing_result, summary=summary)
