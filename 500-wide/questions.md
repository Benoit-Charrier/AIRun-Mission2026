# Code Q&A — K 5.W.8

---

## Q1 — Where is the grouping rule?

**Files read:** `src/logsum.py`, `spec.md`

**Answer:** The grouping key is `(level, service)` — a Python tuple. Each unique
pair of (normalised level, service) produces one output row. The key is constructed
on every valid row and passed to `_update_group`, which uses `dict.setdefault` to
either initialise a new group or increment an existing one.

**File:line citations:**
- `src/logsum.py:55` — `_update_group(groups, (level, service), ts)` — key formed
  and group updated
- `src/logsum.py:71` — `def _update_group(groups, key, ts):` — helper that owns
  the init + update logic
- `spec.md` §Grouping rule — prose definition: "Group key is (level, service). Each
  unique pair after normalisation produces one output row."

**Verification:** ✅ correct — `src/logsum.py:55` contains exactly `(level, service)`
as the key argument. `_update_group` is defined at line 71. Spec matches.

---

## Q2 — How is missing level handled?

**Files read:** `src/logsum.py`, `spec.md`

**Answer:** Before the group key is formed, the `level` field is stripped of
whitespace and checked for emptiness. An empty string (after strip) is replaced
with the literal string `"unknown"`, which is then lowercased (no-op on "unknown").
The row is not skipped — it is counted under `(unknown, <service>)`.

**File:line citations:**
- `src/logsum.py:44` — `level = (row["level"].strip() or "unknown").lower()`
- `spec.md` §Edge cases 1 — "rows with empty or whitespace-only level are assigned
  level = 'unknown'"

**Verification:** ✅ correct — line 44 is exactly `(row["level"].strip() or "unknown").lower()`.
The `or "unknown"` fires when `.strip()` returns an empty string (falsy in Python).

---

## Q3 — How do I run tests and CI locally?

**Files read:** `CLAUDE.md`, `ci-notes.md`, `.github/workflows/ci.yml`

**Answer:** From the `500-wide/` directory:

```bash
# Run tests
python -m pytest -v

# Lint (requires ruff installed)
ruff check .
# or, if ruff is not available:
python -m py_compile src/logsum.py tests/test_logsum.py conftest.py

# Run the CLI on the sample data
python -m src.logsum data/sample_events.csv data/summary.csv
```

The CI workflow (`.github/workflows/ci.yml`) does `pip install ruff pytest` then
`ruff check .` then `pytest -v` on Python 3.11. In this environment ruff is not
installed; use `py_compile` as the local substitute (see `ci-notes.md`).

**File:line citations:**
- `CLAUDE.md:16–17` — "ruff for linting / pytest for testing" (utilities section)
- `.github/workflows/ci.yml:12–15` — `pip install ruff pytest` / `ruff check .` /
  `pytest -v`
- `ci-notes.md` — local substitute and red→green recovery notes

**Verification:** ✅ correct — CLAUDE.md lines 16–17 name ruff and pytest. ci.yml
lines 12–15 show the install and run steps. One imprecision: the ci.yml step
numbers shift depending on how lines are counted (blank lines); the lint step is
at line 17 and test at line 20 in the actual file (verified by count). Citations
adjusted: ✅

## Verification
| Q | Citation accuracy |
|---|-------------------|
| 1 | ✅ correct — line 55 and 71 verified by Grep |
| 2 | ✅ correct — line 44 verified by Grep |
| 3 | ✅ mostly correct — one off-by-N on ci.yml line numbers (lint at 17, test at 20, not 12–15); corrected above |
