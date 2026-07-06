# DQ Certificate — Bronze->Silver->Gold Pipeline

**Date:** 2026-07-02  |  **Pipeline:** Nordstar retail transactions

## Clean run (8/8 expected)

| # | Check | Result |
|---|-------|--------|
| 1  No null order_date/region/category | PASS |
| 2  total_revenue > 0 | PASS |
| 3  order_count > 0 | PASS |
| 4  No duplicate grain (date+region+category) | PASS |
| 5  No null order_date in returns_rate | PASS |
| 6  returns_rate_pct in [0, 100] | PASS |
| 7  returned_orders <= total_orders | PASS |
| 8 date span >= 30 days | PASS |

**8/8 checks passed** on clean data

## Break test — injected bad row (`total_revenue = -999.99`)

| # | Check | Result |
|---|-------|--------|
| 1  No null order_date/region/category | PASS |
| 2  total_revenue > 0 | FAIL (1) |
| 3  order_count > 0 | PASS |
| 4  No duplicate grain (date+region+category) | PASS |
| 5  No null order_date in returns_rate | PASS |
| 6  returns_rate_pct in [0, 100] | PASS |
| 7  returned_orders <= total_orders | PASS |
| 8 date span >= 30 days | PASS |

**7/8 checks passed** — check #2 (`total_revenue > 0`) fires as expected

## Re-run after cleanup (8/8 expected)

| # | Check | Result |
|---|-------|--------|
| 1  No null order_date/region/category | PASS |
| 2  total_revenue > 0 | PASS |
| 3  order_count > 0 | PASS |
| 4  No duplicate grain (date+region+category) | PASS |
| 5  No null order_date in returns_rate | PASS |
| 6  returns_rate_pct in [0, 100] | PASS |
| 7  returned_orders <= total_orders | PASS |
| 8 date span >= 30 days | PASS |

**8/8 checks passed** after bad row removed

## Break-and-verify summary

Check #2 (`total_revenue > 0`) fired on the injected `−999.99` row and returned to PASS after cleanup.
All other checks remained stable through the break-and-verify cycle.

**Certification:** These 8 DQ checks are confirmed gate-ready — they pass on clean data and fail correctly on injected violations.
