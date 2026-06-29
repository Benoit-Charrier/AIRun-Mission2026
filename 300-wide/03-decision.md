---
product: Meridian retail site and app
feature: AI availability assistant
kata: 3.W.4
date: 2026-06-25
---

## Idea scoring — impact × effort (1–5)

| # | Idea | Impact | Effort | Score | Notes |
|---|------|:------:|:------:|------:|-------|
| 1 | Confidence-graded label + timestamp | 5 | 3 | **8** | Core UX change; reuses Module 200 AI verdict (US-01/US-02); effort is integration, not net-new |
| 2 | Alternative stores (up to 2, within 25 km) | 4 | 3 | **7** | Redirects uncertain-verdict shoppers; US-03 already scoped; same effort bracket as #1 |
| 3 | "Can't confirm — call the store" fallback | 4 | 1 | **5** | Trivially cheap; prevents false positive; must ship with #1 — standalone is meaningless |
| 4 | Pickup-screen feedback ("was this accurate?") | 2 | 1 | **3** | Low reach but builds accuracy loop; low effort; add as a bundled addition |
| 5 | "Reserve & confirm in 10 min" hold | 5 | 5 | **10** | Maximum impact but requires SAP inventory mutation + POS integration across 1,400 stores; explicitly out of scope for v1 per Module 200 PRD Decision Memory |
| 6 | Push notification on status change | 3 | 4 | **7** | Status-change detection pipeline not ready; deferred to v2 (US-05) |
| 7 | POS flag for uncertain reservations | 2 | 4 | **6** | POS integration deferred to Phase 2 (US-10) |

*Scoring: impact = contribution to reducing phantom-stock cancellations; effort = estimated build cost. Scores are sum, not product, to avoid effort-masking low-impact high-impact ties.*

---

## Decided change

**Ship:** a confidence-graded availability display — bundling ideas #1 + #2 + #3 + #4:

1. **Confidence label + freshness timestamp** on the product page before the Reserve button activates ("Likely in stock", "Uncertain", "Not available" — with last-confirmed time inline).
2. **Up to 2 alternative stores** within 25 km shown when verdict is "Uncertain" or "Not available", ranked by confidence then distance.
3. **"Can't confirm" fallback** when data is stale (> 30 min) or missing — store phone number shown, positive availability state suppressed.
4. **Pickup-screen feedback prompt** — "Was this accurate?" logged with store + SKU + timestamp.

**Rationale vs runner-up:** the runner-up (reserve-and-hold, idea #5) would eliminate phantom-stock by design — but it requires real-time SAP inventory mutation and POS integration across 1,400 stores, which is out of scope for this phase and carries high mutation risk (this is documented in the Module 200 PRD Decision Memory). The confidence-graded display ships in weeks, not quarters, reduces the cancellation rate without mutating inventory state, and creates the feedback loop needed to improve the model over time.

**Owner:** Sarah Chen (Head of CX) — committed to the confidence-graded display model in workshop convergence.

---

## Adversarial challenge (fresh AI session result)

*Question put to AI:* "What would make the confidence-graded label fail — what's the scenario where it makes things worse?"

*AI challenge:* "If shoppers anchor on 'Likely in stock' as a guarantee rather than an estimate, a confident-but-wrong verdict is worse than no verdict — it creates a stronger betrayal effect. The label needs to be coupled with explicit disclosure that it is an estimate, not a hold."

*Response:* accepted — AI-AC4 (disclosure) and AI-AC6 (negative AC) address this directly. The prototype must show the "Estimated from store data" label and the "not a guaranteed hold" note on every positive verdict.
