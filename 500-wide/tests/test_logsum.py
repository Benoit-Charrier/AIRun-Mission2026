"""
Tests derived from spec.md only.
Session isolation: these tests were written without reading src/logsum.py.
Every assertion maps to a named spec rule or edge case.
"""

import csv
import sys

import pytest

from src.logsum import summarise


# ── helpers ──────────────────────────────────────────────────────────────────

def write_events(path, rows, fieldnames=None):
    if fieldnames is None:
        fieldnames = ["timestamp", "level", "service", "message"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def read_summary(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ── spec: Grouping rule ───────────────────────────────────────────────────────

def test_groups_by_level_and_service(tmp_path):
    """Spec §Grouping rule: group key is (level, service)."""
    inp, out = tmp_path / "e.csv", tmp_path / "s.csv"
    write_events(inp, [
        {"timestamp": "2026-06-29T09:00:00", "level": "info", "service": "checkout-service", "message": "a"},
        {"timestamp": "2026-06-29T09:00:01", "level": "info", "service": "cart-api",          "message": "b"},
        {"timestamp": "2026-06-29T09:00:02", "level": "error","service": "checkout-service", "message": "c"},
    ])
    summarise(str(inp), str(out))
    keys = {(r["level"], r["service"]) for r in read_summary(out)}
    assert keys == {
        ("info", "checkout-service"),
        ("info", "cart-api"),
        ("error", "checkout-service"),
    }


def test_duplicate_rows_collapsed_into_one_group(tmp_path):
    """Two rows with the same (level, service) → one output row."""
    inp, out = tmp_path / "e.csv", tmp_path / "s.csv"
    write_events(inp, [
        {"timestamp": "2026-06-29T09:00:00", "level": "info", "service": "checkout-service", "message": "x"},
        {"timestamp": "2026-06-29T09:00:01", "level": "info", "service": "checkout-service", "message": "y"},
    ])
    summarise(str(inp), str(out))
    rows = read_summary(out)
    assert len(rows) == 1
    assert rows[0]["count"] == "2"


# ── spec: Normalisation ───────────────────────────────────────────────────────

def test_level_normalised_to_lowercase(tmp_path):
    """Spec §Normalisation: level is normalised to lowercase."""
    inp, out = tmp_path / "e.csv", tmp_path / "s.csv"
    write_events(inp, [
        {"timestamp": "2026-06-29T09:00:00", "level": "ERROR", "service": "cart-api", "message": "x"},
        {"timestamp": "2026-06-29T09:00:01", "level": "error", "service": "cart-api", "message": "y"},
    ])
    summarise(str(inp), str(out))
    rows = read_summary(out)
    assert len(rows) == 1, "ERROR and error must collapse into the same group"
    assert rows[0]["level"] == "error"


# ── spec: Aggregation ─────────────────────────────────────────────────────────

def test_first_seen_and_last_seen(tmp_path):
    """Spec §Aggregation: first_seen is earliest timestamp, last_seen is latest."""
    inp, out = tmp_path / "e.csv", tmp_path / "s.csv"
    write_events(inp, [
        {"timestamp": "2026-06-29T09:00:02", "level": "error", "service": "checkout-service", "message": "late"},
        {"timestamp": "2026-06-29T09:00:00", "level": "error", "service": "checkout-service", "message": "early"},
        {"timestamp": "2026-06-29T09:00:01", "level": "error", "service": "checkout-service", "message": "mid"},
    ])
    summarise(str(inp), str(out))
    rows = read_summary(out)
    assert rows[0]["first_seen"] == "2026-06-29T09:00:00"
    assert rows[0]["last_seen"]  == "2026-06-29T09:00:02"


# ── spec: Edge case 1 — missing level ────────────────────────────────────────

def test_missing_level_becomes_unknown(tmp_path):
    """Spec §Edge cases 1: empty level → 'unknown'."""
    inp, out = tmp_path / "e.csv", tmp_path / "s.csv"
    write_events(inp, [
        {"timestamp": "2026-06-29T09:00:00", "level": "", "service": "identity-service", "message": "x"},
    ])
    summarise(str(inp), str(out))
    rows = read_summary(out)
    assert len(rows) == 1
    assert rows[0]["level"] == "unknown"


# ── spec: Edge case 2 — malformed timestamp ──────────────────────────────────

def test_malformed_timestamp_row_skipped(tmp_path):
    """Spec §Edge cases 2: malformed timestamp → row skipped, valid rows counted."""
    inp, out = tmp_path / "e.csv", tmp_path / "s.csv"
    write_events(inp, [
        {"timestamp": "2026-06-29T09:00:00", "level": "info", "service": "cart-api", "message": "good"},
        {"timestamp": "not-a-date",           "level": "info", "service": "cart-api", "message": "bad"},
    ])
    summarise(str(inp), str(out))
    rows = read_summary(out)
    assert len(rows) == 1
    assert rows[0]["count"] == "1"


# ── spec: Edge case 3 — empty input ──────────────────────────────────────────

def test_empty_input_produces_header_only(tmp_path):
    """Spec §Edge cases 3: headers-only CSV → summary.csv with headers, no data rows."""
    inp, out = tmp_path / "e.csv", tmp_path / "s.csv"
    write_events(inp, [])          # writes header row, zero data rows
    summarise(str(inp), str(out))
    rows = read_summary(out)
    assert rows == []
    with open(out) as f:
        header = f.readline()
    assert "level" in header and "service" in header and "count" in header


# ── spec: Edge case 4 — missing required column ──────────────────────────────

def test_missing_required_column_exits_1(tmp_path):
    """Spec §Edge cases 4: missing 'service' column → exit code 1."""
    inp, out = tmp_path / "e.csv", tmp_path / "s.csv"
    write_events(
        inp,
        [{"timestamp": "2026-06-29T09:00:00", "level": "info", "message": "x"}],
        fieldnames=["timestamp", "level", "message"],
    )
    with pytest.raises(SystemExit) as exc:
        summarise(str(inp), str(out))
    assert exc.value.code == 1


# ── spec: CLI — exit code 1 on missing file ──────────────────────────────────

def test_missing_input_file_exits_1(tmp_path):
    """Spec §CLI: input file not found → exit code 1."""
    out = tmp_path / "s.csv"
    with pytest.raises(SystemExit) as exc:
        summarise(str(tmp_path / "nonexistent.csv"), str(out))
    assert exc.value.code == 1


# ── spec: CLI — --min-count N (added K 5.W.7) ────────────────────────────────

def test_min_count_filters_groups(tmp_path):
    """Spec §CLI --min-count: only groups with count >= N appear in output."""
    inp, out = tmp_path / "e.csv", tmp_path / "s.csv"
    write_events(inp, [
        {"timestamp": "2026-06-29T09:00:00", "level": "info",  "service": "checkout-service", "message": "a"},
        {"timestamp": "2026-06-29T09:00:01", "level": "info",  "service": "checkout-service", "message": "b"},
        {"timestamp": "2026-06-29T09:00:02", "level": "error", "service": "cart-api",          "message": "c"},
    ])
    summarise(str(inp), str(out), min_count=2)
    rows = read_summary(out)
    assert len(rows) == 1
    assert rows[0]["level"] == "info"
    assert rows[0]["service"] == "checkout-service"
    assert rows[0]["count"] == "2"
