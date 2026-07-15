---
kata: K 10.W.5
consumes_from: K 10.W.4 (03-staffing.md balanced variant), K 10.W.3 (02-solution.md phase structure), M900 security risk register, M600 QA test report, M800 platform cost model
source_draft: curriculum-public/modules/1000-management/artefacts/1000-wide/_fallbacks/10.W.5.draft.md
date: 2026-07-07
artefact: 1000-wide/04-estimate.md
note: Markdown stand-in for 04-estimate.xlsx.
---

# Estimate — MRG AI-Enabled Omnichannel Commerce Platform

---

## Diagnosis of the Provided Draft (10.W.5.draft.md)

| # | Defect | Location in draft | Fix |
|---|--------|------------------|-----|
| D-1 | Contingency and margin combined into a single "25% overhead" line | Bottom of the cost summary | Split into two separate lines: Contingency (risk reserve, sized from risk register) and Margin (profit). Each has its own percentage. |
| D-2 | Legacy-support risk scored L4×I5 = Critical/20 with no active mitigation | Risk register, Row "Legacy SAP integration complexity" | Add active mitigation: 2-week scoping sprint pre-contract + scope cap to documented APIs only. |
| D-3 | Assumption "the team will be productive" is unbounded and unfalsifiable | Assumption register, Row 2 | Rewrite with a falsifiable, numerically bounded condition. |
| D-4 | Commercial model recommendation is T&M despite the RFP's C-1 fixed-price constraint | Commercial recommendation section | Change to Hybrid (fixed Phase 1 + Phase 2, T&M cap Phase 3) with rationale naming who carries the delivery risk. |

---

## Base Effort — Balanced Variant (from 03-staffing.md)

| Phase | Roles | FTE-months | Base effort |
|-------|-------|-----------|-------------|
| Phase 1 — Checkout + SAP | DM, Architect, 3× BE, FE/mobile, QA, Security, BA (ramp 50–100%) | 18 | ~18 FTE-months × blended rate |
| Phase 2 — C&C + AI assistant | DM, BE×2, FE/mobile, QA, Data engineer (ramp 100%) | 16 | ~16 FTE-months × blended rate |
| Phase 3 — Full rollout + KT | DM, BE, QA, Data engineer, Security (ramp 80–50%) | 10 | ~10 FTE-months × blended rate |
| **Total base** | | **44 FTE-months** | |

**Blended day rate:** €950/day (40% on-shore Italy ~€1,300/day; 60% near-shore Poland ~€700/day)  
**Base cost:** 44 FTE-months × 20 working days × €950 = **€836,000**

---

## Delivery Impacts (separate lines)

| Impact | FTE-weeks | Cost |
|--------|-----------|------|
| Ramp reduction — 50% utilisation month 1 vs full | −4 FTE-weeks productivity | Already modelled in base FTE-months |
| SAP dependency wait — 2-week scoping sprint gate | +2 FTE-weeks coordination overhead | €19,000 (DM + Architect at full rate) |
| NCC pen-test coordination — Phase 3 | +1 FTE-week security lead time | €6,500 |
| **Delivery impact sub-total** | | **€25,500** |

---

## Contingency (risk reserve) — SEPARATE FROM MARGIN

Contingency is derived from the Expected Monetary Value (EMV) of the risk register, then rounded up to the nearest 5% to cover unknown unknowns. EMV = P(risk fires) × financial impact, summed across all risks.

**Probability mapping used (L score → probability):** L1 ≈ 10% · L2 ≈ 20% · L3 ≈ 50% · L4 ≈ 70% · L5 ≈ 90%

**Phase 1 base cost (EMV anchor):** 18 FTE-months × €19,000 = €342,000

| Risk | L | Prob | Financial impact | EMV |
|------|---|------|-----------------|-----|
| R-1: SAP scope overrun — 30% Phase 1 rework if integration is undocumented | 4 | 70% | 30% × €342,000 = €102,000 | **€71,400** |
| R-2: DPIA/DPO delay — 2–4 week slip, DM + architect holding time | 3 | 50% | ~€20,000 | €10,000 |
| R-3: Critical pen-test finding — 2-week Phase 3 slip, security + BE team | 2 | 20% | ~€13,000 | €2,600 |
| R-4: AI model accuracy below threshold — Phase 2 extension 2 weeks | 2 | 20% | ~€10,000 | €2,000 |
| **Total EMV** | | | | **€86,000** |

**EMV as % of base:** €86,000 / €836,000 = **~10.3%**

**Contingency set at 15%** = EMV floor (10.3%) + 4.7% management buffer for unknown unknowns (undocumented SAP behaviours not in the register, integration edge cases that surface only in production, NCC coordination overhead). The buffer is explicit and named — it is not padding folded into margin.

| Line | % | Derivation | Amount |
|------|---|-----------|--------|
| Contingency (risk reserve) | 15% | EMV ~10% + unknown-unknowns buffer ~5% | **€125,400** |
| Margin (profit) | 10% | Standard engagement margin, separate from risk reserve | **€83,600** |

> These are two separate lines. In negotiation, if the buyer requests a price reduction, margin is reduced first. Contingency is never negotiated down — it is the risk reserve the delivery team draws against during the engagement. Reducing it below the EMV floor (€86,000 / ~10%) exposes EPAM to unmitigated delivery risk.

---

## Total Price

| Line | Amount |
|------|--------|
| Base effort | €836,000 |
| Delivery impacts | €25,500 |
| Contingency (15%) | €125,400 |
| Margin (10%) | €83,600 |
| **Total (fixed Phase 1 + Phase 2; T&M cap Phase 3)** | **€1,070,500** |

**Phase 1 fixed price:** €350,000  
**Phase 2 fixed price:** €410,000  
**Phase 3 T&M cap (max):** €310,500 (billed actuals; cap applies; unused cap is not invoiced)

*AI inference costs (availability assistant, Phase 2–3): placeholder €12,000 — unit cost to be sourced from M800 gateway logs before price is locked. Open item OI-1.*

---

## Risk Register (repaired — all rows have active mitigations)

| # | Risk | Likelihood (1–5) | Impact (1–5) | Score | Active mitigation |
|---|------|----------------|-------------|-------|--------------------|
| R-1 | SAP integration scope larger than documented — undocumented edge cases surface in Phase 1 | 4 | 5 | 20 | **2-week scoping sprint pre-contract**; scope capped to documented APIs; undocumented scope triggers a change-order (not fixed-price) |
| R-2 | DPIA/DPO sign-off delayed — AI assistant go-live blocked | 3 | 3 | 9 | DPIA kick-off week 1; DPO ≥4 h/week committed in contract (A-3); delay >1 week = Phase 2 start-date review |
| R-3 | Critical pen-test finding in weeks 17–19 — Phase 3 delayed | 2 | 4 | 8 | ≥2-week buffer between NCC delivery and Phase 3 exit; costs absorbed by contingency reserve (≤2-week slip modelled) |
| R-4 | AI assistant prediction accuracy below 85% at Phase 2 entry gate | 2 | 3 | 6 | Model evaluation gate at Phase 2 entry; prediction-only constraint limits blast radius to advisory outputs only |

*R-1 is sourced from M900 02-risks.csv (T-05 SQL injection + T-07 credential stuffing are the highest-scored checkout risks; SAP scope risk is delivery-layer, not security-layer, but adjacent). R-3 maps to M900 K 9.W.5 evidence gap (CI logs + production telemetry not yet in place at Phase 1 entry — resolved by Phase 2).*

---

## Assumption Register (repaired — all bounds are falsifiable)

| # | Assumption | Bounded by |
|---|-----------|-----------|
| A-1 | MRG provides SAP API access and full documentation | Within 14 calendar days of contract signature; if not met, Phase 1 go-live shifts by equivalent delay and fixed price converts to T&M for Phase 1 only |
| A-2 | ≥70% team utilisation from sprint 3 (week 5) onward | If utilisation falls below 60% in any sprint, delivery manager triggers a capacity review within 48 hours; three consecutive below-60% sprints trigger an engagement escalation |
| A-3 | MRG DPO allocates ≥4 h/week to DPIA review | Weeks 1–4; delay of >1 week triggers Phase 2 start-date review; total DPO unavailability >3 weeks = Phase 2 go-live shifts to 2027-01-31 |
| A-4 | 100-store pilot test environment available | From 2026-10-01; delay shifts Phase 2 exit by equivalent delay; MRG IT operations confirm availability at Phase 1 entry gate |

---

## Commercial Model Recommendation (repaired)

**Hybrid: fixed-price Phase 1 + Phase 2; T&M cap Phase 3.**

The RFP's C-1 constraint (fixed-price preferred) is met for Phases 1 and 2, where the scope is defined by the scoping sprint and the architecture record. Phase 3 (full 1,400-store rollout + knowledge transfer) carries scope variability that depends on MRG's pilot-store readiness and internal IT timelines — variability MRG controls, not EPAM. A T&M cap on Phase 3 means EPAM carries delivery risk on Phases 1–2; MRG carries Phase 3 extension risk (but is protected by the cap at €310,500).

T&M-only is not recommended: it conflicts with the buyer's C-1 constraint and would score down on EC-2 in the evaluation.

Fixed-price-only is not recommended: the undocumented SAP integration scope makes a fixed-price commitment on Phase 3 a liability EPAM cannot underwrite without the scoping sprint evidence.

---

## Commercial-Model Decision Matrix

| Model | Risk fit | Cash-flow fit | Buyer fit |
|-------|---------|--------------|-----------|
| T&M (full) | Poor — EPAM carries no delivery risk; buyer carries all | Buyer pays as billed; no predictability | Conflicts with C-1; scored down |
| Fixed-price (full) | Poor on Phase 3 — SAP scope unknown; contingency cannot cover open scope | Predictable for buyer; liability risk for EPAM | Preferred by buyer but not defensible without scoping sprint |
| **Hybrid (fixed P1+P2, T&M cap P3)** ← recommended | **Good — EPAM carries defined scope; buyer carries Phase 3 variability with a cap** | **Predictable on P1+P2; capped exposure on P3** | **Meets C-1 spirit; justified in writing** |
