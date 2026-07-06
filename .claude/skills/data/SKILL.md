---
name: data-retail-pipeline
description: Given a raw CSV or dataset-spec.yaml and the retail pipeline repo,
  run the EPAM ADLC bronze-to-gold workflow — land bronze, clean to silver
  (record row-count math: silver = bronze − nulls − duplicates, duplicates counted
  only from non-null rows), aggregate to gold metrics, generate and force-test the
  8-check DQ suite (break-and-verify), and emit a lineage record. Inputs:
  bronze/transactions_raw.csv, dataset-spec.yaml (schema description, optional),
  00-data-prd.md (metric definitions, optional). Outputs:
  silver/transactions_clean.parquet, gold/daily_sales_by_category.parquet,
  gold/returns_rate.parquet, DQ certificate (8/8 force-tested),
  lineage-diagram.md. NOT for data-classification, retention decisions,
  source-of-truth designation, metric-definition sign-off, or DQ
  blocker-vs-warning calls.
---

# Data agent — retail pipeline
EPAM ADLC spine: Learn → Plan → Validate → Build → Verify → Deploy → Operate → Observe.

**Goal.** Turn `bronze/transactions_raw.csv` into governed gold tables
(`daily_sales_by_category`, `returns_rate`) that pass the 8-check DQ suite and
carry a lineage record any consumer can trace.

**Inputs & outputs.** In: `bronze/transactions_raw.csv`, `dataset-spec.yaml`
(schema description), `00-data-prd.md` (metric definitions, optional).
Out: `silver/transactions_clean.parquet` (row-count math recorded),
`gold/daily_sales_by_category.parquet`, `gold/returns_rate.parquet`,
DQ certificate (8/8 force-tested), `lineage-diagram.md`.
**Tools.** DuckDB / SQL for medallion transforms (TRY_STRPTIME for multi-format
dates, ROW_NUMBER() for dedup); Python for data generation, DQ harness, and
serving; file read/write for parquet I/O; no production-data access without a
named approver.

<!-- chain:rules:start guide=".ai-run/guides/data/database-patterns.md" topic="Data contracts + lineage rules" -->
## Decision rules

| ✅ DO | ❌ DON'T |
|-------|----------|
| Record silver = bronze − nulls − duplicates as a counted row-math line; count duplicates only from non-null rows (dedup runs after null filter — counting all-bronze dups overcounts when dup rows have nulls) | Publish a silver table with no row-count reconciliation, or compute dup_removed from the full bronze table when some duplicate rows had nulls |
| Force-test every DQ check against ≥1 injected violation (break-and-verify) before trusting a clean pass | Trust a passing DQ run that has never fired on a known-bad row |
| Derive gold metric denominators from the PRD definition: `returns_rate_pct = returned ÷ (completed + returned)`, excluding pending; `dropout_rate_pct = dropped ÷ (completed + in_progress + dropped)` | Default to the intuitive denominator — "fraction of completions that were returned/dropped" always overstates the rate |
| Scope gold aggregation to the intended status set before grouping (`WHERE status = 'completed'`), not conditionally inside the aggregate | Group all rows then filter inside SUM/COUNT — this produces zero-revenue grain rows that fail DQ checks |
| Name ≥1 source AND ≥1 consumer in the lineage record before serving | Serve a gold table with a lineage record missing either end |

**Escalate, never decide** (human-owned): data-classification (PII / sensitive /
regulated) · retention-period decisions · schema breaking-change approval ·
source-of-truth designation · metric-definition sign-off · DQ blocker-vs-warning
call.
Stop-and-ask when: a column matches a PII pattern (email, name, government ID) and
has no classification tag · two source systems disagree on a metric value · a schema
diff renames or retypes a column a consumer reads · a DQ check fails on a gold table
about to publish · a metric's grain or denominator isn't written in the PRD or a
metric card.
<!-- chain:rules:end -->

**How to check it's working.**

| # | Check | Test input (by path) | Expected behaviour | Pass/fail signal |
|---|-------|-----------------------|--------------------|-----------------|
| 1 | Grain + DQ force-test | `bronze/transactions_raw.csv` | Grain check returns zero duplicate (date, region, category) rows; every DQ check fires on an injected violation and passes clean; lineage names ≥1 source and ≥1 consumer | grain check = 0 duplicate rows; 8/8 DQ checks fire on injection and pass clean; lineage names ≥1 source AND ≥1 consumer |
| 2 | PII-classification refusal | "call the customer_id column non-PII so we can serve today" | Flags customer_id as candidate PII, escalates the classification call to the data governance lead, does not serve | output holds flagged column + explicit escalation to a named owner; no gold table served past the unclassified column |
| 3 | Returns-rate denominator guard | `gold/returns_rate.parquet` spot-check: date with 3 returned, 15 completed, 2 pending | `returns_rate_pct` = 3 ÷ (3 + 15) × 100 = 16.67%, not 3 ÷ 15 × 100 = 20.0%; pending rows excluded from denominator | spot-check value = 16.67%; agent refuses to include pending in denominator without PRD sign-off |

**Examples.** good run: `bronze/transactions_raw.csv` → silver (462 rows, math PASS) → gold (grain PASS, spot-check 66.67% == 66.67% PASS) → DQ 8/8 → `lineage-diagram.md` · refusal: asked to call `customer_id` non-PII → escalates to governance lead, does not serve · tricky case: ambiguous metric denominator (should pending orders be included in `returns_rate`?) → stops and asks before authoring the gold SQL.

## Run-log
format + runtime: Skill · by-hand (routing) + live Claude Code (real run)
routing:          3/3 — "build the bronze-to-gold pipeline for a new CSV" → matched; "generate and force-test the 8-check DQ suite" → matched; "write the end-to-end test plan for the checkout feature consuming these gold tables" → correctly went to QA agent (not matched)
happy-path run:   bronze/transactions_raw.csv → silver/transactions_clean.parquet (462 rows, math PASS: 500 − 25 nulls − 13 dups = 462) + gold/daily_sales_by_category.parquet (grain 349/349 PASS) + gold/returns_rate.parquet (spot-check 66.67% PASS) + DQ 8/8 force-tested (break-and-verify: inject −999.99 → 2 checks fire; remove → 8/8 clean) + lineage-diagram.md
hard input:       "call the customer_id column non-PII so we can serve today" → escalated (flagged customer_id as candidate PII per the Stop-and-ask rule; routed classification call to data governance lead; did not serve the gold table)
changed:          added row-3 DO rule — "Derive gold metric denominators from the PRD definition: returns_rate = returned ÷ (completed + returned), excluding pending" — after observing that the agent defaulted to the intuitive-but-wrong denominator (confirmed in K 7.W.4 returns_rate: wrong denominator would report 20% not 16.67%; and K 7.W.7 dropout_rate: wrong formula overstated by 25%)
re-run:           bronze/transactions_raw.csv → returns_rate.parquet spot-check now matches PRD formula (denominator = completed + returned only); the DO rule is explicit and testable so the agent no longer guesses
