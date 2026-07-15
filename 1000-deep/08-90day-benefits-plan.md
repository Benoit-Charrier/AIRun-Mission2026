---
kata: K 10.D.9
artefact: 1000-deep/08-90day-benefits-plan.md
consumes_from: 00-project-context.md, 01-stakeholders.md, 02-staffing-scenario.md, 03-command-center.md, 04-maturity-baseline.md, 05-operating-model.md, 06-gates.md, 07-telemetry-status.md
engagement: ERP-modernization — EU industrial-machinery manufacturer
date: 2026-07-08
status: complete
---

# 90-Day Customer-Benefit AI Adoption Plan — ERP Modernization Engagement

*Targets are tied to project outcomes, not generic maturity levels. Every target has a customer benefit, a falsifiable evidence statement, a named owner, a gate or telemetry proof, and champion/enablement support.*

---

## Target Table

| SDLC Phase   | Current maturity | Day-90 target                                                              | Customer benefit                                                                                                     | Falsifiable evidence                                                                                                                | Owner         | Gate / telemetry proof                                                                                                                 | Champion / enablement support                                                                                              | Status-report audience                             |
| ------------ | ---------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| **Intake**   | L0               | L1 (AI-assisted qualification with source links)                           | More stable scope: fewer mid-flight scope surprises; SOW baseline holds                                              | 3/3 qualification summaries carry source links **AND** unplanned scope changes ≤2 per month from sprint 2 onward                    | Delivery lead | Source-check gate (05-operating-model.md): 3/3 pass; scope-change count from Jira                                                      | Delivery champion — 10% protected time from month 1; joins weekly triage to review AI summaries before they leave the team | EPAM delivery sponsor                              |
| **Validate** | L1               | L2 (AI-generated tests reviewed by QA lead; golden-set gate active)        | Lower defect escape rate: client receives safer releases; compliance lead sees tested evidence before sign-off       | Golden-set pass rate ≥90% at sprint 6 **AND** escaped defects ≤3 in the release following gate activation                           | QA lead       | Eval gate (06-gates.md): CI blocks on golden-set failure; defect-escape-rate trend from defect tracker (07-telemetry-status.md)        | QA champion — 10% protected time from sprint 3; maintains the golden set and reviews AI-generated test scaffolds           | Compliance lead; client COO (via release sign-off) |
| **Handoff**  | L1               | L2 (Decision Memory completeness gate active; 100% decisions logged)       | Fewer reopened decisions: COO and compliance lead can sign off on go-live without rediscovering decisions from chat  | 100% of release decisions logged (owner + rationale + rejected option + date) **AND** decision-reopen count ≤1 per month by month 6 | Delivery lead | Decision Memory gate (06-gates.md): 100% completion check; decision-reopen count from Confluence decision log (07-telemetry-status.md) | Delivery champion — 10% protected time; creates decision log entries in real time during release readiness reviews         | Client COO                                         |
| **Build**    | L2               | L3 (rule-file lint in CI; automated improvement loop; PR rework below 12%) | Lower PR rework: engineers spend time on new features; tech lead sees quality trend rather than firefighting reviews | Lint = 0 errors for 4 consecutive weeks **AND** PR rework rate below 12% by day 90 (from 18% baseline)                              | Tech lead     | Rule-file lint CI gate (06-gates.md): blocks merge on failure; PR rework rate from Jira + PR labels (07-telemetry-status.md)           | Engineering champion — 15% protected time from sprint 2; owns `rules/` repo maintenance and lint-rule review               | Client CTO                                         |

---

## 30 / 60 / 90 Cadence

| Milestone | Date target | Focus | Evidence due | Review audience |
|-----------|------------|-------|-------------|----------------|
| **Day 30 — Gate setup** | Month 1 close | All gates defined in 06-gates.md are active in CI or have a manual enforcement process in place; champions designated and protected time confirmed | Source-check gate: first 3 summaries reviewed. Decision log: template published and first 2 entries logged. Lint: CI step active. Golden-set: first draft committed by QA lead | Delivery lead + EPAM delivery sponsor (internal) |
| **Day 60 — Telemetry trend check** | Month 2 close | Adoption metrics have ≥4 data points; at least one outcome metric shows movement from baseline; Azure specialist availability confirmed and risk closed or escalated | AI-assisted PR rate: 4-week trend visible. BA-reviewed AC rate: ≥2 sprints of data. Decision-reopen count: first monthly reading. Defect escape: previous release report available | Delivery lead + client CTO + client COO (status report section) |
| **Day 90 — Sponsor readout** | Month 3 close | At least one customer-benefit metric has moved from baseline with evidence; Build at L3 (lint in CI for 4 weeks); Handoff and Validate at L2; Intake at L1; bootcamp win evidence ready | Weekly memo showing one metric delta from baseline (cited source). Lint = 0 for 4 weeks. Decision-reopen ≤1. Golden-set ≥90%. Source-link pass 3/3 | EPAM delivery sponsor + client COO + compliance lead |

---

## Bootcamp Win Evidence

**Artefact:** Weekly delivery-health + AI-adoption memo from `03-command-center.md` approved-source prompt, showing:
- At least one customer-benefit metric moved from baseline with source cited (e.g. decision-reopen count: 4 → ≤1; or defect escape: 7 → ≤3).
- Safe Harbor gate status included (at least one gate active and result reported).
- No metric invented or estimated without a named source.

**What the bootcamp grades:** Whether the memo ties AI adoption to a client outcome — not whether adoption percentages are high.

---

## Sponsor Ask

1. **Confirm Azure specialist availability by week 2.** If unavailable, the Lean scenario risk (R-AZ-01) is unmitigated; delivery lead escalates to EPAM delivery sponsor for alternative sourcing.
2. **Approve protected time for three champions:**
   - Delivery champion: 10% from month 1 (covers Intake + Handoff improvements)
   - QA champion: 10% from sprint 3 (covers Validate golden-set gate)
   - Engineering champion: 15% from sprint 2 (covers Build L3 rule-file lint CI)
3. **Authorize AI tool use on confidential project data** (source code, confidential risk log entries) by SOW confirmation and Data Classification Matrix review — needed before the Build gate can be activated in CI.
4. **Confirm DPIA timeline with compliance lead** — if the AI assistant for sales-ops processes any client-identifiable data (quote/order records), a DPIA is required before M3 beta. Compliance lead must be engaged by month 2.

---

## Reconciliation Notes

| Artefact | Cross-check result |
|---------|-------------------|
| `00-project-context.md` — outcomes | All four targets (Intake, Validate, Handoff, Build) trace to a named project outcome: scope stability, defect escape, go-live readiness, cycle time. ✓ |
| `01-stakeholders.md` — escalation triggers | COO escalation trigger (critical path moves 2 weeks) is covered by Handoff L2 target (decision-reopen ≤1). CTO trigger (integration gate fails twice) is covered by Build L3 lint gate. ✓ |
| `04-maturity-baseline.md` — two weakest phases | Intake (L0) and Handoff (L1) are the two weakest — both are the primary targets in this plan. ✓ |
| `06-gates.md` — gate thresholds | All numeric thresholds in this plan (lint = 0; golden-set ≥90%; 100% decisions logged; ≤2 scope changes/month) match the gate table in 06-gates.md. ✓ |
| `07-telemetry-status.md` — metrics and baselines | Every falsifiable evidence statement in this plan has a corresponding metric row with a denominator and baseline in 07-telemetry-status.md. ✓ |
| `02-staffing-scenario.md` — AI-assisted work assumption | Protected-time allocations for three champions (10% + 10% + 15%) are within the balanced scenario capacity. ✓ |
