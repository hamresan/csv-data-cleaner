"""Processing result summary model."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProcessingSummary:
    """Machine-readable processing counters and output location."""

    input_file: str
    processed_records: int
    valid_records: int
    invalid_records: int
    duplicate_records: int
    output_file: str | None
