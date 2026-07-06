# Bronze Profile — transactions_raw.csv

**Generated:** 2026-07-02  |  **Seed:** 42  |  **Rows:** 500

## Column null counts

|   total_rows |   null_order_id |   null_customer_id |   null_region |   null_order_date |   null_amount |   null_quantity |   null_status |   min_amount |   max_amount |   distinct_statuses |
|-------------:|----------------:|-------------------:|--------------:|------------------:|--------------:|----------------:|--------------:|-------------:|-------------:|--------------------:|
|          500 |               0 |                  0 |             0 |                 0 |            25 |               0 |             0 |      -402.05 |       497.76 |                   3 |

## Duplicate order_ids (top 5)

| order_id   |   occurrences |
|:-----------|--------------:|
| ORD-00078  |             3 |
| ORD-00004  |             3 |
| ORD-00030  |             2 |
| ORD-00028  |             2 |
| ORD-00070  |             2 |

**Total order_ids with duplicates:** 13

## Status distribution

| status    |   cnt |
|:----------|------:|
| completed |   393 |
| returned  |    87 |
| pending   |    20 |

## Date formats observed

| Format | Example |
|--------|--------|
| YYYY-MM-DD | 2024-03-15 |
| DD/MM/YYYY | 15/03/2024 |
| Mon DD YYYY | Mar 15 2024 |

**Cleaning baseline (for K 7.W.3 math):**

- Bronze rows: 500
- Null amount rows to drop: 25
- Duplicate order_id groups: 13 (each group loses N-1 rows after keeping highest customer_id)
- Negative amounts (returns): kept — legitimate return records
