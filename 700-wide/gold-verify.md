# Gold Verification

**Date:** 2026-07-02

## Table 1: daily_sales_by_category

| Check | Expected | Actual | Result |
|-------|----------|--------|--------|
| Row count | >0 | 345 | PASS |
| Grain (total == unique combos) | equal | 345 == 345 | PASS |

## Table 2: returns_rate

| Check | Expected | Actual | Result |
|-------|----------|--------|--------|
| returns_rate_pct range | 0..100 | 0.0..100.0 | PASS |
| Zero-return rows have 0.0 not NULL | 0 NULLs | 0 NULLs | PASS |

## Returns-rate formula spot-check

**Date checked:** 2024-01-15

| Source | returned_orders | total_orders | rate_pct |
|--------|-----------------|--------------|----------|
| Manual count from silver | 2 | 3 | 66.67% |
| Gold table value | | | 66.67% |
| Match | | | PASS |

**Formula:** `returned_orders / (completed + returned) * 100` — pending orders excluded from denominator.

**Business note:** Negative amounts (returns) in silver are tracked via `status='returned'`, not via sign. Revenue metric filters `status='completed'` to exclude them.
