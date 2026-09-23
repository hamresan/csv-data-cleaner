"""Pipeline input request."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class CleanDataRequest:
    """Physical inputs required to run the cleaning pipeline."""

    input_path: Path
    config_path: Path
    output_dir: Path
    sheet: str | None = None
    dry_run: bool = False
