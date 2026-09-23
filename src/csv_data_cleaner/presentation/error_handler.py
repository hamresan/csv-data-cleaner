"""Map expected application failures to concise CLI errors."""

import click

from csv_data_cleaner.domain.errors import DataCleanerError


class CliErrorHandler:
    """Translate expected domain/application failures into Click errors."""

    def run(self, operation: object) -> object:
        """Execute a zero-argument callable and map expected failures."""
        if not callable(operation):
            raise TypeError("operation must be callable")
        try:
            return operation()
        except DataCleanerError as error:
            raise click.ClickException(str(error)) from error
