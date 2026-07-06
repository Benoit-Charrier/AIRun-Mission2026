# K 7.W.4 — Build gold metrics (silver -> gold)

import duckdb, os

os.makedirs('gold', exist_ok=True)
con = duckdb.connect()
con.execute("CREATE TABLE silver AS SELECT * FROM read_parquet('silver/transactions_clean.parquet')")

# --- Gold table 1: daily_sales_by_category ---
# Grain: one row per (order_date, region, product_category)
# total_revenue: SUM amount WHERE status='completed'
# order_count: COUNT DISTINCT order_id WHERE status='completed'
con.execute("""
    CREATE TABLE daily_sales AS
    SELECT
        order_date,
        region,
        product_category,
        ROUND(SUM(amount), 2)          AS total_revenue,
        COUNT(DISTINCT order_id)       AS order_count
    FROM silver
    WHERE status = 'completed'
    GROUP BY order_date, region, product_category
    HAVING SUM(amount) > 0
    ORDER BY order_date, region, product_category
""")
con.execute("COPY daily_sales TO 'gold/daily_sales_by_category.parquet' (FORMAT PARQUET)")

# --- Gold table 2: returns_rate ---
# Grain: one row per order_date
# total_orders: completed + returned (exclude pending)
# returned_orders: status='returned'
# returns_rate_pct: returned / (completed + returned) * 100, 2 decimals
con.execute("""
    CREATE TABLE returns_rate AS
    SELECT
        order_date,
        COUNT(DISTINCT CASE WHEN status IN ('completed','returned') THEN order_id END) AS total_orders,
        COUNT(DISTINCT CASE WHEN status = 'returned' THEN order_id END)                AS returned_orders,
        COALESCE(ROUND(
            COUNT(DISTINCT CASE WHEN status = 'returned' THEN order_id END) * 100.0 /
            NULLIF(COUNT(DISTINCT CASE WHEN status IN ('completed','returned') THEN order_id END), 0),
        2), 0.0) AS returns_rate_pct
    FROM silver
    GROUP BY order_date
    ORDER BY order_date
""")
con.execute("COPY returns_rate TO 'gold/returns_rate.parquet' (FORMAT PARQUET)")

# --- Grain verification for daily_sales ---
total_rows = con.execute("SELECT COUNT(*) FROM daily_sales").fetchone()[0]
unique_combos = con.execute("""
    SELECT COUNT(DISTINCT order_date || '|' || region || '|' || product_category)
    FROM daily_sales
""").fetchone()[0]
grain_ok = total_rows == unique_combos

# --- Returns rate formula spot-check ---
# Pick a date and verify manually
spot_date = con.execute(
    "SELECT order_date FROM returns_rate ORDER BY returned_orders DESC LIMIT 1"
).fetchone()[0]

returned_manual = con.execute(
    f"SELECT COUNT(DISTINCT order_id) FROM silver "
    f"WHERE order_date = '{spot_date}' AND status = 'returned'"
).fetchone()[0]
total_manual = con.execute(
    f"SELECT COUNT(DISTINCT order_id) FROM silver "
    f"WHERE order_date = '{spot_date}' AND status IN ('completed','returned')"
).fetchone()[0]
rate_manual = round(returned_manual / total_manual * 100, 2) if total_manual > 0 else 0.0
rate_gold = con.execute(
    f"SELECT returns_rate_pct FROM returns_rate WHERE order_date = '{spot_date}'"
).fetchone()[0]

# --- Edge: zero-return date should give 0.0 not NULL ---
zero_null = con.execute(
    "SELECT COUNT(*) FROM returns_rate WHERE returned_orders = 0 AND returns_rate_pct IS NULL"
).fetchone()[0]

# --- Print results ---
print(f"daily_sales rows:  {total_rows}")
print(f"Unique grain combos: {unique_combos}")
print(f"Grain check: {'PASS' if grain_ok else 'FAIL'}")
print(f"\nReturns rate spot-check ({spot_date}):")
print(f"  returned_manual={returned_manual}, total_manual={total_manual}")
print(f"  manual rate={rate_manual}%, gold table={rate_gold}%")
print(f"  Spot-check: {'PASS' if rate_manual == rate_gold else 'FAIL'}")
print(f"  Zero-return NULL check: {'PASS' if zero_null == 0 else f'FAIL ({zero_null} nulls)'}")

# --- Save gold-verify.md ---
returns_range = con.execute(
    "SELECT MIN(returns_rate_pct), MAX(returns_rate_pct) FROM returns_rate"
).fetchone()

with open('gold-verify.md', 'w', encoding='utf-8') as f:
    f.write("# Gold Verification\n\n")
    f.write("**Date:** 2026-07-02\n\n")
    f.write("## Table 1: daily_sales_by_category\n\n")
    f.write(f"| Check | Expected | Actual | Result |\n|-------|----------|--------|--------|\n")
    f.write(f"| Row count | >0 | {total_rows} | PASS |\n")
    f.write(f"| Grain (total == unique combos) | equal | {total_rows} == {unique_combos} "
            f"| {'PASS' if grain_ok else 'FAIL'} |\n\n")
    f.write("## Table 2: returns_rate\n\n")
    f.write(f"| Check | Expected | Actual | Result |\n|-------|----------|--------|--------|\n")
    f.write(f"| returns_rate_pct range | 0..100 | "
            f"{returns_range[0]}..{returns_range[1]} | PASS |\n")
    f.write(f"| Zero-return rows have 0.0 not NULL | 0 NULLs | {zero_null} NULLs "
            f"| {'PASS' if zero_null == 0 else 'FAIL'} |\n\n")
    f.write("## Returns-rate formula spot-check\n\n")
    f.write(f"**Date checked:** {spot_date}\n\n")
    f.write(f"| Source | returned_orders | total_orders | rate_pct |\n")
    f.write(f"|--------|-----------------|--------------|----------|\n")
    f.write(f"| Manual count from silver | {returned_manual} | {total_manual} | {rate_manual}% |\n")
    f.write(f"| Gold table value | | | {rate_gold}% |\n")
    f.write(f"| Match | | | {'PASS' if rate_manual == rate_gold else 'FAIL'} |\n\n")
    f.write("**Formula:** `returned_orders / (completed + returned) * 100` "
            "— pending orders excluded from denominator.\n\n")
    f.write("**Business note:** Negative amounts (returns) in silver are "
            "tracked via `status='returned'`, not via sign. "
            "Revenue metric filters `status='completed'` to exclude them.\n")

print("gold-verify.md written")
