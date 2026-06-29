---
product: Meridian retail site and app
feature: AI availability assistant
kata: 3.W.8
date: 2026-06-25
---

## Journey Redesign Pack — 1-page narrative

### What we changed and why

The current click-&-collect product page shows a binary "In stock" label derived from a 15–30 minute stale SAP snapshot. Shoppers trust it, reserve, drive to the store, and ~7% find the item isn't there. The label violates two Nielsen heuristics (H1 — system status not visible; H5 — error not prevented) and creates a trust deficit that causes shoppers to abandon click-&-collect entirely.

**The redesign surfaces what the system actually knows.** Instead of a binary label, shoppers now see:
- A confidence-graded verdict ("In stock" / "Likely in stock" / "Uncertain" / "Can't confirm") with a freshness timestamp
- Up to 2 alternative stores within 25 km when the primary store is uncertain or unavailable
- A plain-language fallback with the store phone number when the system can't assess availability
- A disclosure link explaining that the estimate is not a guaranteed hold

The key design principle: **surface the reliability of the signal, not just its value.** A "Likely in stock" label that the shopper understands is honest and useful; a green "In stock" badge that may be wrong is a liability.

---

### Benefit

Shoppers who see "Uncertain" or "Not available" avoid wasted trips — directly reducing phantom-stock cancellations. Shoppers who see "Likely in stock" with a disclosure make an informed decision rather than a blind one. Alternative store suggestions redirect uncertain-verdict shoppers to a confirmed location, converting potential cancellations into successful pickups.

**Expected outcome metric:** phantom-stock cancellation rate at pickup — from ~7% to ≤ 3% at EU-West pilot stores within 3 months of launch. Measured weekly in the OMS; attributed via holdout (assistant-active stores vs. matched control stores).

---

### Cost estimate

| Cost area | Estimate | Notes |
|-----------|----------|-------|
| Engineering | ~8 weeks (2 sprints) | Frontend component build + Availability API integration + confidence model (US-08, Module 200) — see Module 200 RICE backlog for story-level effort |
| Design | ~2 weeks | Component design + accessibility audit + prototype iteration |
| Content | ~0.5 weeks | Label wording, disclosure copy, fallback message, feedback prompt |
| QA | ~1 week | 6 AI-AC clauses + accessibility audit (WCAG 2.1 AA) + circuit-breaker test |

**Total estimated calendar time:** ~4–5 weeks with a 2-person eng squad, subject to sprint-1 spike on signal pipeline (US-08 at 50% confidence — Module 200 R2 risk).

---

### Risks and dependencies

1. **Signal pipeline (R2):** if the store-level confidence model (US-08) underdelivers by code freeze, all verdicts default to "Uncertain" (SAP-count-only). The design degrades gracefully but the metric impact is reduced.
2. **Accessibility (R3):** confidence labels are colour-coded — WCAG 2.1 AA requires colour + icon + text. Audit is a DoD gate for US-01.
3. **Label anchoring risk (adversarial finding):** shoppers may anchor on "Likely in stock" as a near-guarantee. The disclosure link and warning-box on the confirmation screen mitigate this — but wording must be tested in the usability sessions (Task 2).
