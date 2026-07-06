# K 7.W.3 — Clean bronze -> silver
# Cleaning baseline (from bronze-profile.md):
#   Bronze rows:       500
#   Null amount rows:  25  (drop)
#   Dup order_id groups: 13  (keep highest customer_id, lose N-1 per group)
#   Negative amounts: kept (legitimate returns)

import duckdb, os

os.makedirs('silver', exist_ok=True)
con = duckdb.connect()

con.execute("CREATE TABLE bronze AS SELECT * FROM read_csv_auto('bronze/transactions_raw.csv')")

bronze_count = con.execute("SELECT COUNT(*) FROM bronze").fetchone()[0]
print(f"Bronze rows loaded: {bronze_count}")

# Cleaning SQL:
# 1. Drop rows where amount IS NULL
# 2. Standardise order_date to DATE (three formats)
# 3. Deduplicate by order_id, keeping the row with the highest customer_id
con.execute("""
    CREATE TABLE silver AS
    WITH dated AS (
        SELECT *,
            COALESCE(
                TRY_STRPTIME(order_date, '%Y-%m-%d'),
                TRY_STRPTIME(order_date, '%d/%m/%Y'),
                TRY_STRPTIME(order_date, '%b %d %Y')
            )::DATE AS order_date_clean
        FROM bronze
        WHERE amount IS NOT NULL
    ),
    deduped AS (
        SELECT *,
               ROW_NUMBER() OVER (
                   PARTITION BY order_id
                   ORDER BY customer_id DESC
               ) AS rn
        FROM dated
    )
    SELECT
        order_id,
        customer_id,
        region,
        order_date_clean AS order_date,
        product_category,
        CAST(amount AS DOUBLE) AS amount,
        quantity,
        status
    FROM deduped
    WHERE rn = 1
""")

# Write to parquet
con.execute("COPY silver TO 'silver/transactions_clean.parquet' (FORMAT PARQUET)")

# Verification
silver_count   = con.execute("SELECT COUNT(*) FROM silver").fetchone()[0]
null_amount_s  = con.execute("SELECT COUNT(*) FROM silver WHERE amount IS NULL").fetchone()[0]
dup_check      = con.execute("""
    SELECT COUNT(*) FROM (
        SELECT order_id FROM silver GROUP BY order_id HAVING COUNT(*) > 1
    )
""").fetchone()[0]
null_dates     = con.execute("SELECT COUNT(*) FROM silver WHERE order_date IS NULL").fetchone()[0]
neg_amounts    = con.execute("SELECT COUNT(*) FROM silver WHERE amount < 0").fetchone()[0]

print(f"Silver rows:         {silver_count}")
print(f"Null amount:         {null_amount_s}   (expected 0)")
print(f"Duplicate order_ids: {dup_check}   (expected 0)")
print(f"Null dates:          {null_dates}   (expected 0)")
print(f"Negative amounts:    {neg_amounts}  (kept — returns)")

# Math verification
# Rows removed by null filter: 25
# Rows removed by dedup: sum of (group_size - 1) for each dup group
dup_removed = con.execute("""
    SELECT SUM(cnt - 1) FROM (
        SELECT COUNT(*) AS cnt FROM bronze GROUP BY order_id HAVING COUNT(*) > 1
    )
""").fetchone()[0] or 0
expected = bronze_count - 25 - dup_removed
print(f"\nMath check:")
print(f"  Bronze {bronze_count} - null {25} - dup_rows {int(dup_removed)} = {int(expected)}")
print(f"  Actual silver: {silver_count}  => {'PASS' if silver_count == int(expected) else 'FAIL'}")

# Save verification
with open('silver-verify.md', 'w', encoding='utf-8') as f:
    f.write("# Silver Verification — transactions_clean.parquet\n\n")
    f.write(f"**Date:** 2026-07-02\n\n")
    f.write("## Row-count math\n\n")
    f.write(f"| Step | Count |\n|------|-------|\n")
    f.write(f"| Bronze rows | {bronze_count} |\n")
    f.write(f"| Rows dropped (null amount) | 25 |\n")
    f.write(f"| Rows dropped (dedup, N-1 per group) | {int(dup_removed)} |\n")
    f.write(f"| **Expected silver** | **{int(expected)}** |\n")
    f.write(f"| **Actual silver** | **{silver_count}** |\n")
    f.write(f"| Result | {'PASS' if silver_count == int(expected) else 'FAIL'} |\n\n")
    f.write("## Post-cleaning checks\n\n")
    f.write(f"| Check | Expected | Actual | Result |\n|-------|----------|--------|--------|\n")
    f.write(f"| Null amount count | 0 | {null_amount_s} | {'PASS' if null_amount_s == 0 else 'FAIL'} |\n")
    f.write(f"| Duplicate order_ids | 0 | {dup_check} | {'PASS' if dup_check == 0 else 'FAIL'} |\n")
    f.write(f"| Null order_date | 0 | {null_dates} | {'PASS' if null_dates == 0 else 'FAIL'} |\n")
    f.write(f"| Negative amounts | kept | {neg_amounts} | PASS (returns preserved) |\n\n")
    f.write("## Cleaning rules applied\n\n")
    f.write("1. Dropped rows where `amount IS NULL` (25 rows)\n")
    f.write("2. Standardised `order_date` to DATE: tried `YYYY-MM-DD`, then `DD/MM/YYYY`, then `Mon DD YYYY`\n")
    f.write("3. Deduplicated by `order_id`, keeping highest `customer_id` per group "
            "(ROW_NUMBER PARTITION BY order_id ORDER BY customer_id DESC)\n")
    f.write("4. Negative amounts preserved — legitimate return records\n")

print("silver-verify.md written")
