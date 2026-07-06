# Lineage record — Nordstar retail pipeline

**Pipeline:** bronze → silver → gold → DQ → serving  
**Date:** 2026-07-02  
**Source of truth:** `bronze/transactions_raw.csv` (synthetic, seed=42)

---

## Source → silver

| Source | Path | Row count | Quality issues introduced deliberately |
|--------|------|-----------|----------------------------------------|
| Raw transactions CSV | `bronze/transactions_raw.csv` | 500 | 25 null amounts (~5%), 15 duplicate order_id rows (13 groups), 3 date formats |

**Silver cleaning steps** (row-count math):

```
500 bronze rows
 − 25 null amount rows (WHERE amount IS NOT NULL)
 − 13 duplicate rows (ROW_NUMBER() PARTITION BY order_id — counted from non-null rows only)
= 462 silver rows  ✓
```

Silver path: `silver/transactions_clean.parquet`

---

## Silver → gold

### gold/daily_sales_by_category.parquet

| Dimension | Value |
|-----------|-------|
| Grain | one row per (order_date, region, product_category) |
| Filter | `WHERE status = 'completed' HAVING SUM(amount) > 0` |
| Metrics | `total_revenue = ROUND(SUM(amount), 2)`, `order_count = COUNT(DISTINCT order_id)` |
| Row count | 349 (grain check: 349 unique combos = 349 rows ✓) |
| PRD reference | total_revenue definition: sum of completed order amounts per day/region/category |

### gold/returns_rate.parquet

| Dimension | Value |
|-----------|-------|
| Grain | one row per order_date |
| Denominator | `completed + returned` orders only — pending excluded by design |
| Metric | `returns_rate_pct = returned_orders / total_orders × 100` (COALESCE 0.0 for zero-return dates) |
| PRD reference | returns_rate formula: what fraction of *settled* orders were returned; pending orders not yet settled |
| Spot-check | 2024-03-19: 2 returned / 3 total (completed+returned) = 66.67% ✓ |

---

## Gold → consumers

| Gold table | Consumer | Consumed via | Metrics surfaced |
|------------|----------|--------------|-----------------|
| `daily_sales_by_category.parquet` | Streamlit dashboard (`kata-workspace/app.py`) | `pd.read_parquet` | Total Revenue metric card, grouped bar chart by region + category |
| `returns_rate.parquet` | Streamlit dashboard (`kata-workspace/app.py`) | `pd.read_parquet` | Avg Returns Rate metric card, line chart with average hline |
| `daily_sales_by_category.parquet` | Course completions comparison (`comparison.md`) | reference only | Pattern template for `daily_completions_by_category` |

---

## DQ gate

| Check | Table | Signal | Result |
|-------|-------|--------|--------|
| 1 No null date/region/category | gold_sales | COUNT(*) WHERE any key NULL = 0 | PASS |
| 2 total_revenue > 0 | gold_sales | COUNT(*) WHERE revenue ≤ 0 = 0 | PASS |
| 3 order_count > 0 | gold_sales | COUNT(*) WHERE count ≤ 0 = 0 | PASS |
| 4 No duplicate grain | gold_sales | COUNT(*) duplicate (date, region, category) = 0 | PASS |
| 5 No null date in returns | gold_returns | COUNT(*) WHERE date NULL = 0 | PASS |
| 6 rate in [0, 100] | gold_returns | MIN ≥ 0 AND MAX ≤ 100 | PASS (0.0..100.0) |
| 7 returned ≤ total | gold_returns | COUNT(*) WHERE returned > total = 0 | PASS |
| 8 date span ≥ 30 days | gold_returns | MAX − MIN ≥ 30 | PASS (362 days) |

Force-test: injected `total_revenue = −999.99` → checks 2 and 4 fired; removed row → 8/8 clean.
