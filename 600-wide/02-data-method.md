---
case: Meridian Retail Group — Click & Collect
consumes_from: 6.W.2 (01-test-cases.md)
date: 2026-07-01
author: Benoit Charrier
---

# Test Data Generation Method — 02-test-data.json

**Tool used:** Claude Sonnet 4.6 (claude-sonnet-4-6) in the current session, guided by explicit field specifications and variety constraints drawn from `01-test-cases.md` and the Click & Collect feature card.

**Record count:** 15 (5 realistic + 10 edge-case)

## Fields generated

`customer_id`, `customer_name`, `email`, `order_id`, `store_id`, `store_name`, `sku`, `payment_method`, `payment_token`, `loyalty_number`, `loyalty_tier`, `loyalty_points_balance`, `reservation_ts`, `pickup_window_expires`, `region`, `language`, `identity_merge_state`

## Fields obfuscated

- **`customer_name`:** Fully fictional names chosen to be plausible for the target locale (Italian, German, Japanese, British, US, Arabic, UAE). No real individual's name used.
- **`email`:** All addresses use the `@meridian-qa.invalid` domain — a non-resolvable TLD that cannot be delivered or leaked. Format follows realistic locale patterns (first.last.test@).
- **`payment_token`:** All tokens use `-XXXX-TEST` or `-STUB-FAIL-TEST` suffixes and contain no real card or account numbers. Japanese PayPay tokens follow the `PPAY-JP-TOK-` prefix convention without encoding real credentials.
- **`loyalty_number`:** Fictional identifiers (`L-IT-001`, `L-DUPE-001`, etc.) with no relationship to production loyalty account ranges.

No records were derived from or cross-referenced against production data. This complies with CLAUDE.md's synthetic-data-only gate and GDPR Article 30 documentation requirements (Asha Sundaram's office).

## Variety dimensions exercised

| Dimension | Values covered |
|---|---|
| Country / region | IT, DE, JP, GB, US, AE (6 of 22 markets) |
| Payment method | Postepay, Klarna split-pay, PayPay, Visa, Amex |
| Language / script | it-IT, de-DE, ja-JP (kana), en-GB, en-US, ar-AE (Arabic RTL) |
| Identity-merge state | merged, clean_web_account, first_instore_stitch_pending, no_loyalty_account, collision_two_ids |
| SAP stub behaviour | normal, zero_stock_at_pickup, timeout_6000ms |
| SCA stub behaviour | normal, fail_first_attempt |
| Pickup window state | active (normal), boundary (1 min before expiry), expired (1 hour after) |
| Order size | single-item (14 records), multi-item (1 record — E-010) |
| Customer name length | standard, max-length with hyphen and umlaut (E-009), kana (R-003, E-010), Arabic (E-008) |

## What is intentionally missing

- Records from regions not yet onboarded to Phase 1 (e.g., South-East Asia except Japan) — out of scope per `00-test-plan.md`.
- Real PSD2 SCA round-trip data — not reproducible in a test harness without a live bank SCA stub; SCA failure is simulated via the `sca_stub_behaviour` field.
- Records exercising the legacy Shopify storefront — explicitly out of scope per `00-test-plan.md`.
- Records covering multi-currency cross-region settlement — out of scope per `00-test-plan.md`.
