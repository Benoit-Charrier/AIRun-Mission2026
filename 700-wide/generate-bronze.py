wh# K 7.W.2 — Generate bronze dataset
# 500 rows of messy retail transactions for Nordstar Customer 360

import random
import numpy as np
import pandas as pd
import os, duckdb

random.seed(42)
np.random.seed(42)

os.makedirs('bronze', exist_ok=True)

N = 500
order_ids = [f"ORD-{i:05d}" for i in range(1, N + 1)]

# Inject ~3% duplicate order_ids (≈15 rows)
dup_count = 15
for i in random.sample(range(N), dup_count):
    order_ids[i] = random.choice(order_ids[:100])

customer_ids = np.random.randint(1000, 10000, N)
regions = np.random.choice(['North', 'South', 'East', 'West'], N,
                            p=[0.27, 0.25, 0.25, 0.23])
categories = np.random.choice(
    ['Electronics', 'Clothing', 'Food', 'Home', 'Sports'], N)

# Mixed date formats
def rand_date():
    day = random.randint(1, 365)
    d = pd.Timestamp('2024-01-01') + pd.Timedelta(days=day - 1)
    fmt = random.choice([
        d.strftime('%Y-%m-%d'),          # ISO
        d.strftime('%d/%m/%Y'),          # European
        d.strftime('%b %d %Y'),          # Month DD YYYY
    ])
    return fmt

dates = [rand_date() for _ in range(N)]

# Amount: 5% null, ~2% negative (returns)
amounts = np.random.uniform(5.0, 500.0, N).round(2)
null_indices = random.sample(range(N), 25)
for i in null_indices:
    amounts[i] = float('nan')
neg_indices = random.sample([i for i in range(N) if i not in null_indices], 10)
for i in neg_indices:
    amounts[i] = -amounts[i]

quantities = np.random.randint(1, 11, N)
statuses = np.random.choice(
    ['completed', 'returned', 'pending'], N, p=[0.80, 0.15, 0.05])

df = pd.DataFrame({
    'order_id':        order_ids,
    'customer_id':     customer_ids,
    'region':          regions,
    'order_date':      dates,
    'product_category': categories,
    'amount':          amounts,
    'quantity':        quantities,
    'status':          statuses,
})

df.to_csv('bronze/transactions_raw.csv', index=False)

# Profile via DuckDB
con = duckdb.connect()
con.execute("CREATE TABLE bronze AS SELECT * FROM read_csv_auto('bronze/transactions_raw.csv')")

total_rows = con.execute("SELECT COUNT(*) FROM bronze").fetchone()[0]
null_amount = con.execute(
    "SELECT COUNT(*) FROM bronze WHERE amount IS NULL").fetchone()[0]
dup_order_ids = con.execute("""
    SELECT COUNT(*) FROM (
        SELECT order_id FROM bronze
        GROUP BY order_id HAVING COUNT(*) > 1
    )
""").fetchone()[0]
date_formats = con.execute("""
    SELECT COUNT(DISTINCT
        CASE
            WHEN regexp_matches(order_date, '^\\d{4}-\\d{2}-\\d{2}$') THEN 'YYYY-MM-DD'
            WHEN regexp_matches(order_date, '^\\d{2}/\\d{2}/\\d{4}$') THEN 'DD/MM/YYYY'
            ELSE 'Mon DD YYYY'
        END
    ) FROM bronze
""").fetchone()[0]

print(f"Total rows:           {total_rows}")
print(f"Null amount count:    {null_amount}")
print(f"Duplicate order_ids:  {dup_order_ids}")
print(f"Distinct date formats:{date_formats}")
print("bronze/transactions_raw.csv written")

# Save profile as markdown
con.execute("CREATE VIEW bronze_v AS SELECT * FROM bronze")
profile = con.execute("""
    SELECT
        COUNT(*)                                              AS total_rows,
        SUM(CASE WHEN order_id IS NULL THEN 1 ELSE 0 END)   AS null_order_id,
        SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) AS null_customer_id,
        SUM(CASE WHEN region IS NULL THEN 1 ELSE 0 END)      AS null_region,
        SUM(CASE WHEN order_date IS NULL THEN 1 ELSE 0 END)  AS null_order_date,
        SUM(CASE WHEN amount IS NULL THEN 1 ELSE 0 END)      AS null_amount,
        SUM(CASE WHEN quantity IS NULL THEN 1 ELSE 0 END)    AS null_quantity,
        SUM(CASE WHEN status IS NULL THEN 1 ELSE 0 END)      AS null_status,
        MIN(TRY_CAST(amount AS DOUBLE))                      AS min_amount,
        MAX(TRY_CAST(amount AS DOUBLE))                      AS max_amount,
        COUNT(DISTINCT status)                               AS distinct_statuses
    FROM bronze
""").fetchdf()

dup_detail = con.execute("""
    SELECT order_id, COUNT(*) AS occurrences
    FROM bronze
    GROUP BY order_id
    HAVING COUNT(*) > 1
    ORDER BY occurrences DESC
    LIMIT 5
""").fetchdf()

statuses_dist = con.execute("""
    SELECT status, COUNT(*) AS cnt
    FROM bronze
    GROUP BY status
    ORDER BY cnt DESC
""").fetchdf()

with open('bronze-profile.md', 'w', encoding='utf-8') as f:
    f.write("# Bronze Profile — transactions_raw.csv\n\n")
    f.write("**Generated:** 2026-07-02  |  **Seed:** 42  |  **Rows:** 500\n\n")
    f.write("## Column null counts\n\n")
    f.write(profile.to_markdown(index=False))
    f.write("\n\n## Duplicate order_ids (top 5)\n\n")
    f.write(dup_detail.to_markdown(index=False))
    f.write(f"\n\n**Total order_ids with duplicates:** {dup_order_ids}\n")
    f.write("\n## Status distribution\n\n")
    f.write(statuses_dist.to_markdown(index=False))
    f.write("\n\n## Date formats observed\n\n")
    f.write("| Format | Example |\n|--------|--------|\n")
    f.write("| YYYY-MM-DD | 2024-03-15 |\n")
    f.write("| DD/MM/YYYY | 15/03/2024 |\n")
    f.write("| Mon DD YYYY | Mar 15 2024 |\n")
    f.write("\n**Cleaning baseline (for K 7.W.3 math):**\n\n")
    f.write(f"- Bronze rows: {total_rows}\n")
    f.write(f"- Null amount rows to drop: {null_amount}\n")
    f.write(f"- Duplicate order_id groups: {dup_order_ids} "
            f"(each group loses N-1 rows after keeping highest customer_id)\n")
    f.write(f"- Negative amounts (returns): kept — legitimate return records\n")

print("bronze-profile.md written")
