---
kata: K 10.W.8
consumes_from: K 10.W.1–K 10.W.7 (all prior artefacts); M100–M900 evidence chain
date: 2026-07-07
artefact: 1000-wide/07-proposal-pack.md
status: reconciled — all contradictions patched (see Reconciliation section)
---

# Proposal Pack — MRG AI-Enabled Omnichannel Commerce Platform

**Bid reference:** MRG-2026-OCP  
**Submitted by:** EPAM Systems EU Delivery  
**Date:** 2026-07-07  
**Commercial model:** Hybrid — fixed-price Phase 1 + Phase 2; T&M cap Phase 3  

---

## Executive Summary

**What EPAM proposes.** A production-ready AI-enabled omnichannel commerce platform for Meridian Retail Group — unified real-time inventory across 1,400 stores and 12 mobile apps, a modernised checkout flow with PSD2 SCA enforcement, a click-and-collect AI availability assistant (prediction-only, GDPR-compliant), and a full security evidence pack validated by independent CREST-certified pen-test. Delivery is turn-key; EPAM hands back a live system with runbooks, trained MRG engineers (L2), and a model registry entry. Phase 1 go-live: 2026-10-31. Full platform: 2027-01-31.

**Why EPAM wins.**

1. **Pre-built checkout security evidence chain (not a promise — a proof).** We carry a live threat model, OWASP-scored risk register, and control implementation with commit SHA from a checkout system at comparable scale (3.2M accounts, SAP integration, mobile-first). No other bidder can produce this at evaluation time.

2. **AI governance maturity with DPIA-ready delivery.** Model registry integration pattern, prediction-only architectural constraint enforced at the API layer, and OWASP-LLM Top 10 mitigations built into sprint workflow. We meet EC-4 criteria without pre-go-live remediation work.

3. **Blended EU delivery at MRG's scale.** Italian-market presence, near-shore Poland team, GDPR and PSD2 compliance handled in-house. Reference: EU omnichannel retailer (800 stores, 2024–2025).

**Commercial model.** Hybrid fixed-price (Phase 1 €350,000 + Phase 2 €410,000) with a T&M cap on Phase 3 (max €310,500). Total: €1,070,500 including 15% contingency reserve and 10% margin — held as separate lines. EPAM carries delivery risk on Phases 1–2; MRG carries Phase 3 extension risk (capped).

**Top risk and mitigation.** SAP integration scope is undocumented — the primary commercial and delivery risk. Mitigation: a 2-week paid scoping sprint (week 1) before the Phase 1 fixed price is locked. Declining the scoping sprint converts Phase 1 to a T&M gate. This is a contractual pre-condition, not a preference.

**Team lead.** EPAM VP of EU Delivery (engagement director); EPAM senior delivery lead (day-to-day). Reference: EU omnichannel retailer (800 stores, 2024–2025) — MRG may contact directly.

---

## RFP Response Matrix

| Criterion | Weight | How we meet it | Evidence artefact |
|-----------|--------|---------------|------------------|
| EC-1 Solution fit | 35 | 3-phase turn-key delivery with gated entry/exit criteria; SAP API replaced by resilient observable service (≤500 ms p95); checkout + mobile APIs modernised; AI assistant prediction-only constraint enforced at API layer | `02-solution.md` (phase table, entry/exit, outsourced capability plan); `02-review.md` (adversarial review + patch) |
| EC-2 Commercial | 25 | Hybrid fixed-price (P1+P2) + T&M cap (P3); contingency 15% separate from margin 10%; 4 bounded assumptions; payment milestones at phase gates | `04-estimate.md` (base effort, delivery impacts, contingency/margin split, assumption register) |
| EC-3 Team & references | 20 | Named delivery lead (EPAM VP EU Delivery); 44 FTE-months balanced blended team; EU retail reference (800-store omnichannel, 2024–2025); Italian-market GDPR/PSD2 experience | `03-staffing.md` (balanced variant); `01-qualification.md` (win themes) |
| EC-4 AI governance | 10 | AI availability assistant registered in model registry pre-go-live; prediction-only constraint in architecture; DPIA co-authorship with MRG DPO; OWASP-LLM Top 10 mitigations in sprint workflow; per-phase AI maturity targets with defined metrics | `06-ai-native.md` (per-phase table, human-owned decisions); `900-wide/03-mitigation.md` (OWASP-LLM controls); `900-wide/00-assets.md` (AI surface assessment) |
| EC-5 Delivery risk management | 10 | 4-risk register (all with active mitigations); 4 bounded assumptions; contingency sized from risk register (not flat percentage); Critical pen-test finding handled with named timeline buffer | `04-estimate.md` (risk register, assumption register); `02-solution.md` (NCC governance); `01-qualification.md` (risk table) |

---

## Solution (from 02-solution.md)

Three-phase turn-key delivery. See `1000-wide/02-solution.md` for full phase table, outsourced capability plan (NCC Group pen-test), compliance shape (Turn-key), key assumptions, and out-of-scope statement.

**Phase summary:**

| Phase | Scope | Go-live |
|-------|-------|---------|
| Phase 1 | Checkout modernisation + SAP API | 2026-10-31 |
| Phase 2 | Click-and-collect + AI availability assistant (100 pilot stores) | 2026-12-31 |
| Phase 3 | Full 1,400-store rollout + runbooks + KT | 2027-01-31 |

**Compliance shape:** Turn-key. EPAM pre-approved tools plus anything cleared by MRG's Data Classification Matrix. DPA required for AI inference on customer session data and order history.

---

## Staffing (from 03-staffing.md — Balanced Variant)

**Recommended variant: Balanced** — 40% on-shore Italy / 60% near-shore Poland; 44 FTE-months total; peak ~10 FTE from month 3. See `1000-wide/03-staffing.md` for full role × month matrix and variant comparison.

Ramp profile: 50% month 1 → 80% month 2 → 100% month 3+

---

## Estimate (from 04-estimate.md)

| Line | Amount |
|------|--------|
| Base effort (44 FTE-months × blended €950/day × 20 days) | €836,000 |
| Delivery impacts (ramp, SAP dependency wait, NCC coordination) | €25,500 |
| **Contingency (15% — risk reserve, separate from margin)** | **€125,400** |
| **Margin (10% — profit, separate from contingency)** | **€83,600** |
| **Total** | **€1,070,500** |

Payment milestones: contract signature (20%), Phase 1 go-live (30%), Phase 2 go-live (30%), Phase 3 go-live (20%).

See `1000-wide/04-estimate.md` for risk register, assumption register, and commercial-model decision matrix.

---

## Plan (from 05-plan.md + 05-timeline.md)

Six milestones from contract signature (2026-08-28) to Phase 3 go-live (2027-01-31). Governance: monthly steering committee (MRG CTO + EPAM engagement director; go/no-go authority at phase gates) + biweekly sprint review + biweekly retro.

Change management: named resistance scenarios (sceptical engineers, store managers, DPO time constraints) with structured response patterns; 3-person Champion network with contractually protected time (10–20% from weeks 8–12); adoption tracked against three measurable behaviours.

Executive sponsor: EPAM VP of EU Delivery (written authority to unblock policy, budget, and escalation beyond the delivery manager's reach).

See `1000-wide/05-plan.md` for full stakeholder map, comms plan, and change-management detail. Timeline: `1000-wide/05-timeline.md`.

---

## AI-Native Delivery (from 06-ai-native.md)

Per-phase maturity targets with metrics and denominators:

| Phase | Target | Metric |
|-------|--------|--------|
| Intake | L2 by month 2 | ≥80% stories with AI-assisted draft marker (stories with marker / total stories per sprint) |
| Plan | L2 by month 2 | ≥75% sprint planning sessions with AI dependency analysis reviewed |
| Build | L2 by month 3 | ≥70% PRs with AI-scaffolding commit (tagged PRs / total PRs merged) |
| Validate | L2 by month 4 | ≥80% API test cases with AI-generated scaffold (AI test files / total test files at sprint 6) |
| Handoff | L1 by month 5 | 2 of 3 MRG engineers operate AI runbook workflow without EPAM support |
| Learn | L2 by month 6 | ≥1 actioned retro insight per sprint from AI-assisted analysis |

Human-owned decisions (never automated): AC approval, client commitments, performance conversations, residual-risk sign-off, DPIA approval, AI model classification, phase gate go/no-go.

See `1000-wide/06-ai-native.md` for tooling baseline (allow-list status), key risks, and measurement plan.

---

## Reconciliation — Contradictions Found and Patched

The following contradictions were identified on end-to-end review. All have been patched before this executive summary was written.

| # | Contradiction | Artefacts involved | Resolution |
|---|--------------|-------------------|-----------|
| RC-1 | Phase 3 entry criterion language differed: 02-solution.md originally said "clean pen-test report from NCC" (absolute); 05-plan.md M5 milestone used "OR Critical findings remediated" formulation after the K 10.W.3 review patch | `02-solution.md` + `05-plan.md` | 02-solution.md was updated in the K 10.W.3 review patch to match: "clean pen-test report OR all Critical findings remediated and re-verified." Both artefacts now use the same language. ✓ |
| RC-2 | 06-ai-native.md references DIAL and Claude (allow-listed for internal data) as tooling baseline — 04-estimate.md has a €12,000 placeholder for AI inference cost but notes "unit cost to be sourced from M800 gateway logs before price locked." The tooling baseline commits to tools that are not yet priced. | `06-ai-native.md` + `04-estimate.md` | Flagged as OI-1 (open item). Not a contradiction in the technical sense but a pricing gap: AI inference cost must be sourced from M800 gateway logs and locked before bid submission. The €12,000 placeholder is marked as provisional. |
| RC-3 | 03-staffing.md Lean variant estimated total ~34 FTE-months with a slower ramp; this differs from the 44 FTE-months base in 04-estimate.md. | `03-staffing.md` (lean) + `04-estimate.md` | No contradiction — the estimate bases on the recommended Balanced variant (44 FTE-months). The Lean variant is an alternative option only; it is not the basis of the price. The estimate header now explicitly states "Balanced variant" as the lineage. ✓ |
| RC-4 | 01-qualification.md states "Commercial fit: 3/5 — fixed-price is our non-preferred model." 04-estimate.md recommends hybrid fixed-price. Without alignment, a reviewer might see these as contradictory. | `01-qualification.md` + `04-estimate.md` | The qualification memo correctly identified the commercial risk; the estimate correctly resolves it with a hybrid model (fixed P1+P2, T&M cap P3). The qualification's score of 3/5 reflects the residual risk of fixed-price on SAP scope, which the hybrid model mitigates but does not eliminate. No change required — the narrative is coherent. ✓ |

---

## Open-Items Log

Items unresolved going into bid submission — named and owned, not buried.

| # | Open item | Owner | Resolution needed by |
|---|-----------|-------|---------------------|
| OI-1 | AI inference unit cost for availability assistant (Phase 2–3) — placeholder €12,000; must be sourced from M800 gateway logs | EPAM solution architect | Before bid submission (2026-07-28) |
| OI-2 | NCC Group pen-test scope, timeline, and pricing — placeholder in Phase 3 estimate; NCC has not confirmed the EU engagement rate | EPAM security lead | Before contract signature (2026-08-28) |
| OI-3 | MRG DPO availability confirmation — 4 h/week for weeks 1–4 committed in qualification memo but not yet confirmed by DPO's line manager | EPAM engagement director → MRG CTO | Before preferred-supplier notification (2026-08-14) |
| OI-4 | SAP API documentation quality — unknown until scoping sprint; if documentation is incomplete, Phase 1 fixed price is provisional | Resolved at scoping sprint (2026-09-14) | If still open at M1, Phase 1 converts to T&M gate |

---

## Supporting Artefacts Index

| Artefact | Kata | Purpose in proposal |
|---------|------|-------------------|
| `1000-wide/00-rfp.md` | K 10.W.1 | Evaluation criteria + weights; submission rules |
| `1000-wide/01-qualification.md` | K 10.W.2 | Fit scores; win themes; deal-breaker; risk table; competitive context |
| `1000-wide/02-solution.md` | K 10.W.3 | Phase design; outsourced capability (NCC); compliance shape; key assumptions |
| `1000-wide/02-review.md` | K 10.W.3 | Fresh-session adversarial review + 3 critiques + patch record |
| `1000-wide/03-staffing.md` | K 10.W.4 | Staffing variants (lean/balanced/fast); ramp curves; recommendation |
| `1000-wide/04-estimate.md` | K 10.W.5 | Base effort; delivery impacts; contingency/margin (separate); risk register; assumption register; commercial model |
| `1000-wide/05-plan.md` | K 10.W.6 | Milestones; governance cadence; change management; stakeholder map; comms plan |
| `1000-wide/05-timeline.md` | K 10.W.6 | Mermaid Gantt timeline with dependency notes |
| `1000-wide/06-ai-native.md` | K 10.W.7 | Per-phase AI maturity targets; metrics; tooling; human-owned decisions |
| `900-wide/03-mitigation.md` | M900 K 9.W.4 | Security control design (T-05 SQL injection + T-07 credential stuffing) |
| `900-wide/04-evidence.md` | M900 K 9.W.5 | Security evidence pack (control identity, test output, monitoring, audit trail) |
| `900-wide/02-risks.csv` | M900 K 9.W.3 | Scored risk register (12 threats; 2 Critical/25; blast radius 3.2M accounts) |
