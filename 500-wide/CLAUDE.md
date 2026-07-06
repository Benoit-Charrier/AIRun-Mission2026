# logsum-sandbox

## Project context
Tiny CLI: reads synthetic events.csv logs (timestamp, level, service, message) and
writes a per-group counted summary. Services reference the Meridian omnichannel platform:
checkout-service, cart-api, identity-service, inventory-service.

## Conventions
- Code in src/
- Tests in tests/
- Data in data/
- Notes and docs at root

## Utilities to prefer
- Python 3.11 standard library (csv, argparse, sys, collections)
- ruff for linting
- pytest for testing

## Escalation gates
- Stop before adding dependencies outside Python 3.11 standard library
- Synthetic data only — never use production logs, emails, tokens, or customer records
- Never overwrite spec.md after sign-off without asking
