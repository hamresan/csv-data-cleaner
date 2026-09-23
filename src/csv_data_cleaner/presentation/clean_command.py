"""User-facing clean command."""

from pathlib import Path

import click

from csv_data_cleaner.application.pipeline import CleanDataRequest
from csv_data_cleaner.composition_root import build_clean_data_use_case


@click.command("clean")
@click.option(
    "--input",
    "input_path",
    required=True,
    type=click.Path(path_type=Path, dir_okay=False),
    help="CSV or XLSX input file.",
)
@click.option(
    "--config",
    "config_path",
    required=True,
    type=click.Path(path_type=Path, dir_okay=False),
    help="YAML or JSON processing configuration.",
)
@click.option(
    "--output-dir",
    required=True,
    type=click.Path(path_type=Path, file_okay=False),
    help="Directory for generated output artifacts.",
)
@click.option("--sheet", default=None, help="XLSX sheet name.")
@click.option(
    "--dry-run",
    is_flag=True,
    help="Run the complete pipeline without writing output files.",
)
def clean(
    input_path: Path,
    config_path: Path,
    output_dir: Path,
    sheet: str | None,
    dry_run: bool,
) -> None:
    """Clean an input dataset using a processing configuration."""
    use_case = build_clean_data_use_case()
    result = use_case.execute(
        CleanDataRequest(
            input_path=input_path,
            config_path=config_path,
            output_dir=output_dir,
            sheet=sheet,
            dry_run=dry_run,
        )
    )
    summary = result.summary
    click.echo(f"Processed records: {summary.processed_records}")
    click.echo(f"Valid records: {summary.valid_records}")
    click.echo(f"Invalid records: {summary.invalid_records}")
    click.echo(f"Duplicate records: {summary.duplicate_records}")
    click.echo(f"Exported records: {summary.exported_records}")
    if dry_run:
        click.echo("Dry run: no output files were written.")
    else:
        click.echo(f"Output file: {summary.output_file}")
        click.echo(f"Report file: {output_dir / 'report.json'}")
