"""Contract-shape tests for the configuration loader port."""

from pathlib import Path

from csv_data_cleaner.application.ports import ConfigLoader
from csv_data_cleaner.domain import NormalizationPolicy, OutputFormat, ProcessingConfig


class StubConfigLoader(ConfigLoader):
    """Minimal implementation proving the port can be implemented explicitly."""

    def load(self, path: Path) -> ProcessingConfig:
        del path
        return ProcessingConfig(
            required_columns=(),
            email_columns=(),
            date_rules=(),
            normalization=NormalizationPolicy(),
            deduplication=None,
            sorting=(),
            output_format=OutputFormat.CSV,
        )


def test_config_loader_contract_supports_explicit_implementation() -> None:
    loader: ConfigLoader = StubConfigLoader()

    assert loader.load(Path("config.json")).output_format is OutputFormat.CSV
