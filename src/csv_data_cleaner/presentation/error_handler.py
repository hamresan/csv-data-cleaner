"""Map expected application failures to concise CLI errors."""

from collections.abc import Callable
from typing import TypeVar

import click

from csv_data_cleaner.domain.errors import DataCleanerError

T = TypeVar("T")


class CliErrorHandler:
    """Translate expected domain/application failures into Click errors."""

    def run(self, operation: Callable[[], T]) -> T:
        """Execute an operation and map expected failures."""
        try:
            return operation()
        except DataCleanerError as error:
            raise click.ClickException(str(error)) from error
