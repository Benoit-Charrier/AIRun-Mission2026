# K 7.W.7 — Agent-built pipeline: online course completions
# Same bronze->silver->gold->DQ->serve pattern, new dataset

import random, numpy as np, pandas as pd, duckdb, os

random.seed(99)
np.random.seed(99)

for d in ['bronze2', 'silver2', 'gold2']:
    os.makedirs(d, exist_ok=True)

# ============================================================
# LAYER 1: BRONZE — generate 500 rows of course completion data
# ============================================================
N = 500
event_ids = [f"EVT-{i:05d}" for i in range(1, N + 1)]
dup_count = 10  # ~2% duplicates
for i in random.sample(range(N), dup_count):
    event_ids[i] = random.choice(event_ids[:80])

student_ids = np.random.randint(1000, 10000, N)
categories = np.random.choice(
    ['Data', 'Engineering', 'Design', 'Business', 'Security'], N)

def rand_date2():
    day = random.randint(1, 365)
    d = pd.Timestamp('2024-01-01') + pd.Timedelta(days=day - 1)
    fmt = random.choice([
        d.strftime('%Y-%m-%d'),
        d.strftime('%m/%d/%Y'),
        d.strftime('%B %d %Y'),
    ])
    return fmt

dates2 = [rand_date2() for _ in range(N)]

completion_pcts = np.random.uniform(0, 100, N).round(1)
null_indices2 = random.sample(range(N), 20)  # ~4% nulls
for i in null_indices2:
    completion_pcts[i] = float('nan')

time_spent = np.random.randint(10, 481, N)
statuses2 = np.random.choice(
    ['completed', 'in_progress', 'dropped'], N, p=[0.70, 0.20, 0.10])

df2 = pd.DataFrame({
    'event_id':         event_ids,
    'student_id':       student_ids,
    'event_date':       dates2,
    'course_category':  categories,
    'completion_pct':   completion_pcts,
    'time_spent_minutes': time_spent,
    'status':           statuses2,
})
df2.to_csv('bronze2/course_events_raw.csv', index=False)

con = duckdb.connect()
con.execute("CREATE TABLE bronze2 AS SELECT * FROM read_csv_auto('bronze2/course_events_raw.csv')")
b2_total  = con.execute("SELECT COUNT(*) FROM bronze2").fetchone()[0]
b2_nulls  = con.execute("SELECT COUNT(*) FROM bronze2 WHERE completion_pct IS NULL").fetchone()[0]
b2_dups   = con.execute("""
    SELECT COUNT(*) FROM (
        SELECT event_id FROM bronze2 GROUP BY event_id HAVING COUNT(*) > 1
    )""").fetchone()[0]
print(f"BRONZE  rows={b2_total}, null_completion={b2_nulls}, dup_event_ids={b2_dups}")

# ============================================================
# LAYER 2: SILVER — clean
# ============================================================
con.execute("""
    CREATE TABLE silver2 AS
    WITH dated AS (
        SELECT *,
            COALESCE(
                TRY_STRPTIME(event_date, '%Y-%m-%d'),
                TRY_STRPTIME(event_date, '%m/%d/%Y'),
                TRY_STRPTIME(event_date, '%B %d %Y')
            )::DATE AS event_date_clean
        FROM bronze2
        WHERE completion_pct IS NOT NULL
    ),
    deduped AS (
        SELECT *,
               ROW_NUMBER() OVER (
                   PARTITION BY event_id
                   ORDER BY student_id DESC
               ) AS rn
        FROM dated
    )
    SELECT event_id, student_id, event_date_clean AS event_date,
           course_category, completion_pct, time_spent_minutes, status
    FROM deduped
    WHERE rn = 1
""")
con.execute("COPY silver2 TO 'silver2/course_events_clean.parquet' (FORMAT PARQUET)")

s2_count = con.execute("SELECT COUNT(*) FROM silver2").fetchone()[0]
s2_nulls = con.execute("SELECT COUNT(*) FROM silver2 WHERE completion_pct IS NULL").fetchone()[0]
s2_dups  = con.execute("""
    SELECT COUNT(*) FROM (
        SELECT event_id FROM silver2 GROUP BY event_id HAVING COUNT(*) > 1
    )""").fetchone()[0]
dup_removed = con.execute("""
    SELECT SUM(cnt - 1) FROM (
        SELECT COUNT(*) AS cnt FROM bronze2
        WHERE completion_pct IS NOT NULL
        GROUP BY event_id HAVING COUNT(*) > 1
    )""").fetchone()[0] or 0
expected_s2 = b2_total - b2_nulls - int(dup_removed)
print(f"SILVER  rows={s2_count} (expected {expected_s2}), "
      f"null_completion={s2_nulls}, dup_events={s2_dups}")
print(f"  Math: {b2_total} - {b2_nulls} - {int(dup_removed)} = {expected_s2} "
      f"=> {'PASS' if s2_count == expected_s2 else 'FAIL'}")

# ============================================================
# LAYER 3: GOLD
# Table 1: daily_completions_by_category
#   Grain: event_date x course_category
#   avg_completion_pct, completion_count (completed only)
# Table 2: dropout_rate
#   Grain: event_date
#   total_enrollments (completed + in_progress + dropped)
#   dropped_count, dropout_rate_pct = dropped / total * 100
# ============================================================
con.execute("""
    CREATE TABLE gold2_completions AS
    SELECT
        event_date,
        course_category,
        ROUND(AVG(completion_pct), 2) AS avg_completion_pct,
        COUNT(DISTINCT event_id)      AS completion_count
    FROM silver2
    WHERE status = 'completed'
    GROUP BY event_date, course_category
    ORDER BY event_date, course_category
""")
con.execute("COPY gold2_completions TO 'gold2/daily_completions_by_category.parquet' (FORMAT PARQUET)")

# NOTE (agent mistake found in review):
# First draft used dropped / completed as denominator — WRONG.
# Correct: dropout_rate_pct = dropped / (completed + in_progress + dropped) * 100
con.execute("""
    CREATE TABLE gold2_dropout AS
    SELECT
        event_date,
        COUNT(DISTINCT event_id) AS total_enrollments,
        COUNT(DISTINCT CASE WHEN status = 'dropped' THEN event_id END) AS dropped_count,
        COALESCE(ROUND(
            COUNT(DISTINCT CASE WHEN status = 'dropped' THEN event_id END) * 100.0 /
            NULLIF(COUNT(DISTINCT event_id), 0),
        2), 0.0) AS dropout_rate_pct
    FROM silver2
    GROUP BY event_date
    ORDER BY event_date
""")
con.execute("COPY gold2_dropout TO 'gold2/dropout_rate.parquet' (FORMAT PARQUET)")

g2_comp_rows = con.execute("SELECT COUNT(*) FROM gold2_completions").fetchone()[0]
g2_comp_grain = con.execute("""
    SELECT COUNT(DISTINCT event_date || '|' || course_category) FROM gold2_completions
""").fetchone()[0]
dr_range = con.execute(
    "SELECT MIN(dropout_rate_pct), MAX(dropout_rate_pct) FROM gold2_dropout"
).fetchone()
print(f"GOLD    completions rows={g2_comp_rows} grain={'PASS' if g2_comp_rows == g2_comp_grain else 'FAIL'}, "
      f"dropout range={dr_range[0]}..{dr_range[1]}%")

# ============================================================
# LAYER 4: DQ CHECKS (6 checks)
# ============================================================
dq_results = []

def dq(name, sql, expect_zero=True):
    v = con.execute(sql).fetchone()[0]
    ok = (v == 0) if expect_zero else (v > 0)
    dq_results.append((name, ok, v))
    print(f"  {'OK' if ok else 'XX'}  {name}: {'PASS' if ok else f'FAIL ({v})'}")

print("\nDQ CHECKS:")
dq("1  No null event_date",
   "SELECT COUNT(*) FROM gold2_completions WHERE event_date IS NULL")
dq("2  avg_completion_pct in [0, 100]",
   "SELECT COUNT(*) FROM gold2_completions WHERE avg_completion_pct < 0 OR avg_completion_pct > 100")
dq("3  completion_count > 0",
   "SELECT COUNT(*) FROM gold2_completions WHERE completion_count <= 0")
dq("4  No duplicate grain (date+category)",
   """SELECT COUNT(*) FROM (
       SELECT event_date, course_category FROM gold2_completions
       GROUP BY event_date, course_category HAVING COUNT(*) > 1
   )""")
dq("5  dropout_rate_pct in [0, 100]",
   "SELECT COUNT(*) FROM gold2_dropout WHERE dropout_rate_pct < 0 OR dropout_rate_pct > 100")
days_span = con.execute(
    "SELECT MAX(event_date) - MIN(event_date) FROM gold2_dropout"
).fetchone()[0]
ok6 = days_span >= 30
dq_results.append(("6 date span >= 30 days", ok6, days_span))
print(f"  {'OK' if ok6 else 'XX'}  6  date span >= 30 days: "
      f"{'PASS' if ok6 else 'FAIL'} ({days_span} days)")

passed = sum(1 for _, p, _ in dq_results if p)
print(f"\n  {passed}/{len(dq_results)} checks passed")

# Save DQ results
with open('gold2/dq-results.md', 'w', encoding='utf-8') as f:
    f.write("# Course pipeline DQ results\n\n")
    for name, ok, val in dq_results:
        f.write(f"- {name}: {'PASS' if ok else f'FAIL ({val})'}\n")
    f.write(f"\n**{passed}/6 checks passed**\n")

# ============================================================
# LAYER 5: SERVING — inline chart verification
# ============================================================
comp = pd.read_parquet('gold2/daily_completions_by_category.parquet')
drop = pd.read_parquet('gold2/dropout_rate.parquet')
comp['event_date'] = pd.to_datetime(comp['event_date'])
drop['event_date'] = pd.to_datetime(drop['event_date'])

cats = set(comp['course_category'].unique())
assert len(cats) == 5, f"Expected 5 categories, got {cats}"
assert drop['dropout_rate_pct'].std() > 0, "Dropout line is flat"
print(f"\nSERVING {len(cats)} categories, dropout rate range: "
      f"{drop['dropout_rate_pct'].min():.1f}%..{drop['dropout_rate_pct'].max():.1f}%")

import plotly.express as px
fig_c = px.bar(
    comp.groupby(['event_date', 'course_category'], as_index=False)['completion_count'].sum(),
    x='event_date', y='completion_count', color='course_category',
    title='Daily Completions by Course Category')
fig_d = px.line(drop, x='event_date', y='dropout_rate_pct',
                title='Dropout Rate Over Time (%)')
fig_c.write_html('kata-workspace/chart-course-completions.html')
fig_d.write_html('kata-workspace/chart-dropout-rate.html')
print("Course charts written to kata-workspace/")
print("\nK 7.W.7 pipeline run complete")
