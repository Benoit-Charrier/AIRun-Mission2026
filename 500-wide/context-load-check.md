# Context load check — K 5.W.1

**Session:** fresh (CLAUDE.md loaded before any code request)
**Cited filename:** `CLAUDE.md`

## Rule file summary by section

**Project context**
This is `logsum-sandbox`, a tiny CLI that reads synthetic `events.csv` logs
(columns: timestamp, level, service, message) and writes a counted summary.
Services in the data reference the Meridian omnichannel platform:
checkout-service, cart-api, identity-service, inventory-service.

**Conventions**
Source code lives in `src/`, tests in `tests/`, data files in `data/`, and
notes/docs at the repo root.

**Utilities to prefer**
Python 3.11 standard library (csv, argparse, sys, collections); `ruff` for
linting; `pytest` for testing. No external packages.

**Escalation gates**
Three hard stops:
1. Do not add any dependency outside the Python 3.11 standard library.
2. Use synthetic data only — no production logs, emails, tokens, or customer records.
3. Never overwrite `spec.md` after sign-off without asking first.
