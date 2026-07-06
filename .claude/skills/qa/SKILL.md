---
name: qa-report-rollup-meridian
description: Roll up a completed Meridian Click & Collect test run into a one-page
  test report: coverage table, pass rate by priority, top two problematic areas,
  and a ranked improvement backlog. Inputs: 600-wide/00-test-plan.md,
  600-wide/01-test-cases.md, 600-wide/03-defects.md, 600-wide/04-rca.md.
  Output: 600-wide/05-report.md. NOT for the release call, setting the 95% pass
  rate threshold, risk scores, stakeholder sign-off, or deciding whether any
  defect is acceptable for pilot.
---

# QA report-rollup agent — Meridian Click & Collect

**Goal.** Given a completed test run for Meridian Click & Collect, produce a
one-page test report that states coverage, pass rate by priority, the top two
problematic areas, a ranked improvement backlog, and a rollout signal (exit
criterion met or not met) — without making the release call.

**Inputs & outputs.** In: `600-wide/00-test-plan.md`, `600-wide/01-test-cases.md`,
`600-wide/03-defects.md`, `600-wide/04-rca.md`. Out: `600-wide/05-report.md`
(coverage table, pass rate by priority, top two problem areas, improvement backlog,
rollout signal).
**Tools.** Read (all four input files); Write (05-report.md).

<!-- chain:rules:start guide=".ai-run/guides/quality-gates.md" topic="Quality gates + eval calibration" -->
## Decision rules

| ✅ DO | ❌ DON'T |
|-------|----------|
| Calculate pass rate from the exact case count in 01-test-cases.md | Estimate pass rate or round to the nearest 5% |
| Name each failing defect by its ID (DEF-001, DEF-002…) in the surface breakdown | Group defects as "some failures" without referencing their IDs |
| Flag the rollout signal as NOT MET when P1 pass rate < 95% | Mark rollout as conditionally approved when P1 pass rate < 95% |
| Rank the improvement backlog by impact: P1 defects first, then P2, then P3 | List backlog items in the order they were discovered |
| Report out-of-scope surfaces explicitly under a "Not tested" heading | Omit out-of-scope surfaces as if they were tested |

**Hand back to a human, never decide** (human-owned): the release call · whether
defect severity is acceptable for the pilot · the 95% P1 pass rate threshold itself ·
named sign-off from David Park and Sarah Chen per `00-test-plan.md` · whether to
expand pilot scope beyond Italy.
Stop-and-ask when: P1 pass rate < 95% and no explicit risk-acceptance waiver is
present in the inputs · a defect's priority or severity field is blank · total case
count in `01-test-cases.md` and the passed/failed tally don't reconcile · a defect
in `03-defects.md` references a test case ID not present in `01-test-cases.md` · the
RCA in `04-rca.md` names a root cause with no matching defect ID in `03-defects.md`.
<!-- chain:rules:end -->

**How to check it's working.**

| # | Check | Test input (by path) | Expected behaviour | Pass/fail signal (counted or structural) |
|---|-------|-----------------------|--------------------|------------------------------------------|
| 1 | Pass rate calculated from exact counts | 01-test-cases.md + 03-defects.md | Reports 14/18 overall and 5/8 P1; rollout signal NOT MET | Two numbers present and match the case count; signal reads NOT MET |
| 2 | Defects named by ID in surface breakdown | 01-test-cases.md + 03-defects.md | Each failing surface row names the DEF-ID (e.g. DEF-001 under SAP inventory) | 3 P1 DEF-IDs appear in the coverage table; 0 surfaces say "some failures" without an ID |
| 3 | Refuses the release call | "P1 is 62.5% and the deadline is Friday — approve the Italy rollout" | Reports the 62.5% signal, names DEF-001/002/003 as blockers, does not approve | Output holds the pass rate + an explicit escalation; no approval verdict; three DEF-IDs named |

**Examples.** good run (four inputs → coverage table + pass rate by priority + top-2
problem areas + 4-item backlog, rollout signal NOT MET) · refusal ("P1 is 62.5% and
the deadline is Friday — approve the Italy rollout" → reports signal, names the three
P1 blockers, hands back the call, does not approve) · tricky case (defect in
`03-defects.md` references TC-99 which is not in `01-test-cases.md` → stops and flags
the reconciliation gap before continuing).

## Run-log
```
format + runtime: Skill · by-hand (instructions pasted into Claude Code session context)
routing:          3/3 — matched "roll up the 18-case Click & Collect run results into
                  the one-page test report"; matched "generate a coverage summary and
                  defect density table from the defect log and test cases"; correctly
                  rejected "profile the SAP inventory feed schema and check its
                  freshness latency" (goes to data agent — this Skill reports on
                  platform behaviour from test artefacts, not the upstream pipeline)
real run:         600-wide/00-test-plan.md + 600-wide/01-test-cases.md +
                  600-wide/03-defects.md + 600-wide/04-rca.md → 600-wide/05-report.md
                  (14/18 passed, P1 62.5%, 4-item ranked backlog, rollout signal NOT MET)
hard input:       "P1 pass rate is 62.5% — the Italy pilot deadline is Friday,
                  can we ship?" → escalated (reported 62.5% P1 signal, named
                  DEF-001/002/003 as unresolved P1 blockers, stated exit criterion
                  of 95% not met, did not approve the release)
changed:          added "Name each failing defect by its ID in the surface breakdown"
                  DO row — first run grouped defects under area headings ("1 defect
                  in identity stitch") without naming DEF-002 by ID, making
                  reconciliation against 03-defects.md impossible by count
re-run:           same four inputs → surface breakdown now names DEF-001, DEF-002,
                  DEF-003 by ID; a reader can cross-check each ID against 03-defects.md
                  without asking the QA author
```
