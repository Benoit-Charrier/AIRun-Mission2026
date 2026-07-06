# 700 Assessment

**Date:** 2026-07-02

---

## Wide Theory — Medallion layers

### The three layers in order

**Bronze — raw landing.**
The source data is written exactly as received, with nothing changed or removed. Purpose: preserve a full, replayable audit trail. If the source system changes schema, disappears, or a metric formula is later corrected, bronze is the point you rewind to. It cannot be re-derived from downstream layers.

**Silver — clean, typed, deduplicated.**
Nulls are dropped, dates are standardised to a single format, and duplicates are resolved by a deterministic rule (e.g. keep the row with the highest customer_id). Purpose: produce a dataset that can be aggregated without silently wrong results. Silver is never served directly — it feeds gold.

**Gold — aggregated business metrics.**
Silver rows are grouped, filtered to the right status set, and reduced to the numbers consumers actually use (daily revenue by region and category, daily returns rate). The formula, grain, and denominator are written down here. Purpose: enforce a single reviewed definition so every consumer uses the same numbers.

### Why three layers instead of cleaning directly to metrics

A single-step raw → metric table collapses three distinct failure modes into one opaque transform. When something goes wrong — and it will — you cannot tell which step caused it.

**Each layer is designed to catch one class of failure:**

- **Bronze catches: source loss / replayability failure.** Without a raw landing, a schema change or source decommission permanently destroys the history. There is no way to reprocess with corrected logic. Bronze makes the pipeline replayable from a known-good snapshot.

- **Silver catches: dirty-data propagation.** Null amounts, duplicate order IDs, and three-format dates (`YYYY-MM-DD`, `DD/MM/YYYY`, `Nov 15 2024`) all silently corrupt aggregates when grouped without cleaning. Silver stops this class of error before it reaches the metric layer. The row-count math (`bronze − nulls − duplicates = silver`) makes the cleaning auditable and checkable.

- **Gold catches: metric inconsistency and wrong grain.** Without a single aggregation layer, each consuming team computes the same metric differently — one includes pending orders in the returns-rate denominator, another does not. Gold enforces the reviewed formula in one place. The grain check (zero duplicate rows at the intended key) catches the case where the aggregation is silently running at the wrong level of detail.

---

## Katas / Final Kata — Bronze → silver → gold arc

### The artefact each stage produces

| Stage | Artefact type |
|-------|--------------|
| Bronze | A raw file (CSV or equivalent) — the source data landed exactly as received, quality issues intact. It is a snapshot, not a product: no rows removed, no types changed, no formats normalised. |
| Silver | A typed, cleaned Parquet file — nulls dropped, dates standardised to one format, duplicates resolved by a deterministic rule. The row-count math (`bronze − nulls − duplicates = silver`) is recorded alongside it as a reconciliation line. |
| Gold | One or more aggregated Parquet files — business metric tables at a defined grain (e.g. one row per date × region × category), with reviewed formulas and a grain check proving no duplicate rows exist at that key. |
| DQ certificate | A signed-off record that every check in the quality suite has been force-tested against a known-bad row (break-and-verify), so a clean pass is evidence, not assumption. |
| Serving layer | A dashboard or API that reads only from gold — never from silver or bronze — so consumers always see the reviewed, grain-checked numbers. |
| Role-agent (Final Kata) | A Skill file (plain text) that captures the pipeline playbook — goal, inputs, outputs, decision rules, and escalation conditions — so a teammate can run the same bronze-to-gold pattern on a new dataset without step-by-step prompting. |

### Two decisions a data engineer must make personally

**1. Business rule interpretation.**

The agent can see column names and values, but it cannot see business intent. What does "active customer" mean — anyone who placed an order in the last 90 days, or anyone whose account is not suspended? Should `pending` orders be included in the returns-rate denominator? Does `completion_pct = 0` mean the course was never started, or that the student enrolled and immediately dropped? These are not data questions — they are questions about what the organisation decided the data should measure. The correct answer lives in a metric definition document, a stakeholder's head, or a legal clause, not in the schema.

Why it cannot be delegated: the agent drafts SQL from column names. When the business rule is ambiguous — and it always is at the edges — the agent picks an interpretation. That interpretation will be consistent and internally coherent, and it will still be wrong if it does not match what the business actually decided. A wrong formula that reaches a dashboard is not a pipeline bug; it is a silent misdefinition that compounds across every report that uses it. Only the person who owns the metric can verify that the formula matches the intent, and only they can sign off that it is correct.

**2. Data classification, access, and retention.**

Before a gold table is served, someone must decide: does this table contain PII or sensitive data? Who is allowed to read it? How long is it retained before deletion? These three decisions are structurally linked — the classification determines the access rules, and the access rules constrain the retention period. They are also the decisions with the most serious external consequences: a misclassified PII column that reaches an unauthorised consumer can trigger a regulatory breach, and a retention period set without a legal basis can violate data protection law.

Why it cannot be delegated: the agent cannot know whether a column named `customer_id` maps to a natural person, whether a given team has a legitimate purpose for accessing order history, or what the applicable retention law is in the jurisdiction where the data was collected. These answers require authority — someone who has read the privacy policy, spoken to legal counsel, or holds the data steward role for this product. An agent that classifies a column as non-PII to unblock a pipeline has made a compliance decision it has no standing to make. The classification must come from a named human who will be accountable if it is wrong.
