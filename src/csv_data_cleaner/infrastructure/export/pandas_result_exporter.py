"""Pandas-backed processing-result exporter."""

from pathlib import Path

from csv_data_cleaner.application.ports import Exporter
from csv_data_cleaner.domain import DatasetProcessingResult, OutputFormat, ProcessingConfig
from csv_data_cleaner.domain.errors import OutputDataError
from csv_data_cleaner.infrastructure.export.result_frame_mapper import ResultFrameMapper


class PandasResultExporter(Exporter):
    """Write cleaned and review artifacts with safe output-directory behavior."""

    def __init__(self, frame_mapper: ResultFrameMapper) -> None:
        self.frame_mapper = frame_mapper

    def export(
        self,
        result: DatasetProcessingResult,
        config: ProcessingConfig,
        output_dir: Path,
    ) -> Path:
        if output_dir.exists():
            raise OutputDataError(f"Output directory already exists: {output_dir}")

        try:
            output_dir.mkdir(parents=True)
            output_file = output_dir / f"cleaned.{config.output_format.value}"
            cleaned = self.frame_mapper.cleaned(result)
            if config.output_format is OutputFormat.CSV:
                cleaned.to_csv(output_file, index=False)
            else:
                cleaned.to_excel(  # pyright: ignore[reportUnknownMemberType]
                    output_file,
                    index=False,
                    engine="openpyxl",
                )

            self.frame_mapper.invalid(result).to_csv(
                output_dir / "invalid_rows.csv",
                index=False,
            )
            self.frame_mapper.duplicates(result).to_csv(
                output_dir / "duplicate_rows.csv",
                index=False,
            )
        except (OSError, ValueError) as error:
            raise OutputDataError(f"Could not write output artifacts: {output_dir}") from error

        return output_file
