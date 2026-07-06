import argparse
import csv
import sys

REQUIRED_COLUMNS = {"timestamp", "level", "service"}


def parse_args():
    p = argparse.ArgumentParser(
        description="Summarise events.csv logs by (level, service)."
    )
    p.add_argument("input_csv", help="Path to input events CSV")
    p.add_argument("output_csv", help="Path to write summary CSV")
    p.add_argument(
        "--min-count", type=int, default=None, metavar="N",
        help="Only output groups with count >= N",
    )
    return p.parse_args()


def summarise(input_path, output_path, min_count=None):
    try:
        fh = open(input_path, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    with fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            _write_summary(output_path, [])
            return

        missing = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing:
            print(f"Error: missing required columns: {sorted(missing)}", file=sys.stderr)
            sys.exit(1)

        groups = {}
        skip_count = 0

        for row in reader:
            ts = row["timestamp"].strip()
            level = (row["level"].strip() or "unknown").lower()
            service = row["service"].strip()

            if not _is_valid_iso8601(ts):
                print(
                    f"Warning: skipping row with malformed timestamp: {ts!r}",
                    file=sys.stderr,
                )
                skip_count += 1
                continue

            _update_group(groups, (level, service), ts)

    if skip_count:
        print(
            f"Warning: skipped {skip_count} row(s) with malformed timestamps.",
            file=sys.stderr,
        )

    rows = [
        {"level": lv, "service": svc, **data}
        for (lv, svc), data in sorted(groups.items())
        if min_count is None or data["count"] >= min_count
    ]
    _write_summary(output_path, rows)


def _update_group(groups, key, ts):
    g = groups.setdefault(key, {"count": 0, "first_seen": ts, "last_seen": ts})
    g["count"] += 1
    if ts < g["first_seen"]:
        g["first_seen"] = ts
    if ts > g["last_seen"]:
        g["last_seen"] = ts


def _is_valid_iso8601(ts):
    # Minimal check: at least 10 chars, starts with a digit (YYYY-MM-DD minimum)
    return bool(ts) and len(ts) >= 10 and ts[0].isdigit()


def _write_summary(output_path, rows):
    with open(output_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh, fieldnames=["level", "service", "count", "first_seen", "last_seen"]
        )
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    args = parse_args()
    summarise(args.input_csv, args.output_csv, min_count=args.min_count)
