# Silver Verification — transactions_clean.parquet

**Date:** 2026-07-02

## Row-count math

| Step | Count |
|------|-------|
| Bronze rows | 500 |
| Rows dropped (null amount) | 25 |
| Rows dropped (dedup, N-1 per group) | 15 |
| **Expected silver** | **460** |
| **Actual silver** | **460** |
| Result | PASS |

## Post-cleaning checks

| Check | Expected | Actual | Result |
|-------|----------|--------|--------|
| Null amount count | 0 | 0 | PASS |
| Duplicate order_ids | 0 | 0 | PASS |
| Null order_date | 0 | 0 | PASS |
| Negative amounts | kept | 10 | PASS (returns preserved) |

## Cleaning rules applied

1. Dropped rows where `amount IS NULL` (25 rows)
2. Standardised `order_date` to DATE: tried `YYYY-MM-DD`, then `DD/MM/YYYY`, then `Mon DD YYYY`
3. Deduplicated by `order_id`, keeping highest `customer_id` per group (ROW_NUMBER PARTITION BY order_id ORDER BY customer_id DESC)
4. Negative amounts preserved — legitimate return records
