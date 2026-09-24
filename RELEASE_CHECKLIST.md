# Release checklist

Use this checklist from a clean clone before merging a release-hardening branch into `main`.

## Clean-clone verification

1. Clone the repository into a new directory.
2. Run `uv sync --locked --all-groups`.
3. Run `make check`.
4. Run `uv build`.
5. Run `uv run csv-data-cleaner --version`.
6. Run the documented example:
   `uv run csv-data-cleaner clean --input examples/customers.csv --config examples/rules.yaml --output-dir output`.
7. Compare `output/` with `examples/expected/`.
8. Remove `output/`, then run the documented dry-run command and confirm no output directory is created.

## Repository consistency

- README commands and terminal output match the CLI.
- README configuration options match the validated configuration schema.
- Package version and metadata are correct.
- The MIT license is present and included in distribution metadata.
- GitHub Actions passes on the release branch.
- Known limitations and spreadsheet/formula-input security notes are current.
- No generated output, local environment, cache, or build artifact is committed.

## Release decision

Merge only after every item above passes. Create a release/tag only from the verified `main` commit.
