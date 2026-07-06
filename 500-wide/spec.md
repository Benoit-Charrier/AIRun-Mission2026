# logsum — Feature Spec

## Goal
Read a synthetic events.csv log file and write summary.csv with one row per
(level, service) group, including count, first_seen, and last_seen timestamps.

## Inputs
`events.csv` — CSV with columns: `timestamp` (ISO 8601), `level` (string),
`service` (string), `message` (string).

## Outputs
`summary.csv` — CSV with columns: `level`, `service`, `count`, `first_seen`,
`last_seen`. One row per unique (level, service) pair. Rows sorted by (level, service)
ascending.

## Normalisation rules
- `level` is normalised to lowercase (e.g. `ERROR` → `error`).
- `service` is kept as-is (case-sensitive).
- Leading and trailing whitespace is stripped from all fields before grouping.

## Grouping rule
Group key is `(level, service)`. Each unique pair after normalisation produces
one output row.

## Aggregation
- `count`: number of rows in the group.
- `first_seen`: earliest `timestamp` in the group (preserved as the original string).
- `last_seen`: latest `timestamp` in the group (preserved as the original string).
- Timestamp ordering uses lexicographic comparison (ISO 8601 strings sort correctly
  without parsing).

## Edge cases
1. **Missing level** — rows with empty or whitespace-only `level` are assigned
   `level = "unknown"`.
2. **Malformed timestamp** — rows where `timestamp` fails the minimal ISO 8601 check
   (not starting with a digit, or shorter than 10 chars) are skipped; a warning is
   printed to stderr. A skip counter is tracked internally but not written to output.
3. **Empty input** — events.csv with only a header row (or truly empty) produces
   summary.csv with column headers and zero data rows.
4. **Missing required column** — if any of `timestamp`, `level`, or `service` is
   absent from the CSV header, exit with code 1 and a descriptive error to stderr.

## CLI
```
python -m src.logsum <input_csv> <output_csv> [--min-count N]
```
- `input_csv`: path to events.csv
- `output_csv`: path to write summary.csv
- `--min-count N`: optional integer; if set, only groups with `count >= N` are written
  to the output. Default: all groups are written.

Exit codes:
- `0` — success
- `1` — input file not found, missing required column, or other fatal error

## Out of scope
- Real-time or streaming log ingestion
- Database or network I/O
- Hardcoded log-level allowlist (accept whatever level values appear in input)
- Production log data — synthetic only
- Log-level allowlist enforcement (accept whatever values appear in input)

## Signed off
BC 2026-06-29

## Implementation notes
- Timestamp ordering is purely lexicographic; no `datetime` import needed for sorting.
- `src/__init__.py` left empty so `src` is a proper package for `python -m src.logsum`.
