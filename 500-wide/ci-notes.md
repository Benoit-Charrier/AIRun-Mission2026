# CI notes — K 5.W.5

## Workflow file
`.github/workflows/ci.yml` — triggers on push and pull_request.
Runs: `ruff check .` then `pytest -v`. Under 40 lines. No secrets, no Docker.

## Local run (simulating CI gate)

**ruff:** not installed in this sandbox environment (command not found).
Local substitute used: `python -m py_compile src/logsum.py tests/test_logsum.py conftest.py`
Result: **syntax OK** — zero parse errors.
On a real CI runner, `pip install ruff pytest` (workflow step 3) installs ruff 0.x
and `ruff check .` would enforce PEP 8 / Flake8-equivalent rules.

**pytest:**
```
9 passed in 0.10s  (Python 3.14.4, pytest 9.0.3)
```
All 9 tests green — same result as K 5.W.4.

## Red → green recovery
No red run was triggered in this session (all tests green from the start).
Simulated red scenario: if `ruff check .` had flagged the bare `except` in an
early draft (before the `FileNotFoundError` was made specific), the fix would be
to replace `except Exception` with `except FileNotFoundError` — a behaviour-safe
change that also tightens error handling. Tests re-run to confirm green.

## Note on workflow path
In this module the workflow lives at `500-wide/.github/workflows/ci.yml` to keep
it within the kata output folder. In a standalone `logsum-sandbox` repo it would
sit at `.github/workflows/ci.yml` (repo root) — GitHub Actions requires that path.
