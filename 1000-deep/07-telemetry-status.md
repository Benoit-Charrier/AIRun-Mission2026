---
kata: K 10.D.8
artefact: 1000-deep/07-telemetry-status.md
consumes_from: 00-project-context.md, 01-stakeholders.md, 03-command-center.md, 05-operating-model.md, 06-gates.md
engagement: ERP-modernization — EU industrial-machinery manufacturer
date: 2026-07-08
status: complete
---

# Telemetry and Status Report — ERP Modernization Engagement

---

## Adoption Metrics

*Adoption metrics show whether the team is using AI tools in delivery. Each needs a denominator so the percentage is falsifiable.*

| Metric | Denominator | Current value (baseline) | Target | Source | Reviewer | Cadence | Stakeholder |
|--------|------------|-------------------------|--------|--------|----------|---------|------------|
| AI-assisted PR rate | All PRs merged per sprint | Not yet measured (Build L2 — `rules/` repo active; tagging inconsistent) | ≥70% of PRs carry AI-assist tag AND reviewer sign-off by month 3 | Git commit history + PR labels | Tech lead | Weekly | Client CTO |
| BA-reviewed AC rate | All stories merged per sprint | Not yet measured (Plan L1 — ACs exist but review not tracked) | ≥80% of merged stories carry BA-reviewed AI-drafted AC by sprint 3 | Jira story cards (AC template field + BA sign-off tag) | BA lead | Biweekly | EPAM delivery sponsor |
| Decision Memory completion rate | All release decisions (per decision log, defined as any decision affecting scope, quality, go-live, or GDPR) | 0% (Handoff L1 — decisions in chat; no log exists) | 100% of release decisions logged before each handoff gate | Decision log (Confluence "Release Decisions" page) | Delivery lead | Weekly | Client COO |
| AI-generated test review rate | All test cases added per sprint | Not yet measured (Validate L1 — test prompts in shared folder; no review) | ≥50% of test cases carry QA-reviewed AI-generated scaffold by sprint 6 | QA repo (test file headers + QA sign-off tag) | QA lead | Per sprint | Compliance lead |

---

## Outcome Metrics

*Outcome metrics show whether AI adoption is changing what the client receives. Each needs a baseline so movement is visible.*

| Metric | Baseline | Target / movement | Source | Reviewer | Cadence | Stakeholder | Customer benefit |
|--------|----------|------------------|--------|----------|---------|-------------|----------------|
| PR rework rate | 18% of PRs required rework last month (defined as: PR re-opened or re-reviewed after initial merge) | Below 12% by day 90 | Jira sprint boards + PR labels; tech lead exports monthly | Tech lead | Per sprint | EPAM delivery sponsor | Lower delivery churn; engineers spend time on new features, not rework |
| Defect escape rate | 7 defects escaped to client-facing staging in last release | ≤3 escaped defects per release by month 9 | Defect tracker (Jira — "Escaped" label applied at post-release review) | QA lead | Per release | Client COO + compliance lead | Safer release; fewer client-reported issues at go-live |
| Decision-reopen count | 4 release decisions reopened last month (source: retro notes; decision was documented in chat) | ≤1 reopen per month by month 6 | Decision log (Confluence) — count decisions marked "Reopened" tag | Delivery lead | Weekly | Client COO | Clearer handoff; go-live confidence increases for COO and compliance sign-off |
| Quote cycle time (AI assistant — quote generation) | Not measured (baseline to be established in M5a beta; sales-ops lead estimate: ~45 min per quote) | Measurable reduction by M5a sign-off; target set by sales-ops lead after 2-week beta | Sales-ops lead usage log + self-reported time tracker | Sales-ops lead | Biweekly from M5a | Sales-ops lead | Faster quote turnaround; sales-ops team adopts the assistant instead of reverting to manual lookups |
| Lead triage time (AI assistant — lead triage) | Not measured (baseline to be established in M5b beta; sales-ops lead estimate: ~20 min per lead) | Measurable reduction by M5b sign-off; target set by sales-ops lead after 2-week beta | Sales-ops lead usage log + self-reported time tracker | Sales-ops lead | Biweekly from M5b | Sales-ops lead | Faster lead routing; fewer leads lost in manual qualification step |
| Order-status query resolution time (AI assistant — order-status) | Not measured (baseline to be established in M5c beta; current: manual lookup in ERP UI ~10 min) | ≤2 min resolution for routine order-status queries by M5c sign-off | Sales-ops lead usage log + ERP query log | Sales-ops lead | Biweekly from M5c | Sales-ops lead + client COO | Portal self-service handles routine queries; sales-ops team focuses on exceptions |

---

## Weekly Status Skeleton

*(Populated from approved sources in `03-command-center.md`. Each line cites its source. Missing evidence is flagged, not invented.)*

---

**Week of:** [DATE]
**Prepared by:** Delivery lead
**Approved by:** [Delivery lead signature before sending]

---

**Delivery health:** [Green / Amber / Red — one-line rationale citing milestone or gate status]

**Milestone movement since last report:**
- [M_ name]: [on track / at risk / moved by N days]; [owner]; [source: Jira / milestone log]

**Top risks (max 3):**
- [Risk ID] [Description] — [current L×I score] — [go-to-green action] — [owner] — [deadline]

**Decisions needed (max 3):**
- [Decision description] — [options available] — [human owner] — [deadline or escalation trigger]

**Staffing / capability notes:**
- [Azure specialist availability: confirmed / pending by week 2 / escalated]
- [Any other open capability items]

**AI-adoption signal (this sprint):**
- Build: AI-assisted PR rate [X%] vs target ≥70% (source: Git; reviewer: tech lead) — [on track / at risk]
- Plan: BA-reviewed AC rate [X%] vs target ≥80% (source: Jira; reviewer: BA lead) — [on track / at risk]
- Handoff: Decision Memory completion [X%] vs target 100% (source: decision log; reviewer: delivery lead) — [on track / at risk]

**Customer-benefit evidence (this report):**
- [One metric that moved from baseline — cite source and delta] OR [No movement this week — baseline established for [metric]; next checkpoint [date]]

**Next action:**
- [Single most important action + owner + date]

---

## Metric-to-Stakeholder Map

| Metric | Primary stakeholder | Why they need it |
|--------|--------------------|--------------------|
| AI-assisted PR rate | Client CTO | Technical readiness signal; tells CTO whether AI use in Build is controlled and verified |
| Decision Memory completion rate | Client COO | Go-live readiness; directly linked to M8 sign-off confidence |
| Defect escape rate | Client COO + compliance lead | Release safety; compliance lead needs it for GDPR-sensitive releases |
| Decision-reopen count | Client COO | Handoff clarity; COO's escalation trigger is 4+ reopens |
| PR rework rate | EPAM delivery sponsor | Fixed-price margin indicator; high rework burns contingency |
| Quote cycle time | Sales-ops lead | Adoption signal for quote generation feature; M5a sign-off evidence |
| Lead triage time | Sales-ops lead | Adoption signal for lead triage feature; M5b sign-off evidence |
| Order-status resolution time | Sales-ops lead | Adoption signal for order-status feature; M5c sign-off evidence |
