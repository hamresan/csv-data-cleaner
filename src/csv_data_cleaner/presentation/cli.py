"""Command-line interface for CSV Data Cleaner."""

import click

from csv_data_cleaner.presentation.clean_command import clean


@click.group()
@click.version_option()
def cli() -> None:
    """Clean, validate, deduplicate, and report on CSV and Excel data."""


cli.add_command(clean)


def main() -> None:
    """Run the CSV Data Cleaner command-line interface."""
    cli()
