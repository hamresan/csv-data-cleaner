"""Command-line interface for CSV Data Cleaner."""

import click


@click.group()
@click.version_option()
def cli() -> None:
    """Clean, validate, deduplicate, and report on CSV and Excel data."""


def main() -> None:
    """Run the CSV Data Cleaner command-line interface."""
    cli()
