---
product: Meridian retail site and app
feature: AI availability assistant
kata: 2.W.6
date: 2026-06-25
scoring: RICE (Reach × Impact × Confidence ÷ Effort)
confidence_values: constrained to {10%, 50%, 80%, 100%}
---

## RICE backlog — scored and sorted

| # | Story | Reach | Impact | Confidence | Effort (wks) | RICE | Rationale (top 5) |
|---|-------|------:|-------:|-----------:|-------------:|-----:|-------------------|
| US-02 | Data freshness indicator | 100 | 0.5 | 100% | 1 | **50.0** | All users, 1-week effort, full confidence — ship bundled with US-01; standalone it is meaningless but trivially cheap to add. |
| US-01 | Confidence-labelled verdict | 100 | 3 | 80% | 5 | **48.0** | Core user-facing feature and the series root; 80% confidence reflects SAP sync integration unknowns — a spike is needed in sprint 1 before sizing. |
| US-04 | No-data handling | 15 | 3 | 100% | 1 | **45.0** | Low reach but prevents the worst failure mode (false "likely available" on no data); 1-week effort, full confidence — must ship as a safety gate alongside US-01. |
| US-07 | 2s latency NFR | 100 | 1 | 80% | 3 | **26.7** | NFR already embedded in US-01's AC; scored separately to surface the 3-week build cost of the p95 target, which must be sized explicitly in sprint planning. |
| US-03 | Nearest alternative store fallback | 40 | 2 | 80% | 3 | **21.3** | Reduces abandonment for the ~40% of users expected to receive an "uncertain" verdict; depends on US-01 but fits the same sprint window. |
| US-08 | Confidence model (SAP + velocity + transfer) | 100 | 3 | 50% | 8 | 18.75 | — |
| US-09 | SAP outage graceful degradation | 10 | 3 | 100% | 2 | 15.0 | — |
| US-05 | Push notification on status change | 30 | 2 | 50% | 4 | 7.5 | — |
| US-06 | Store ops daily digest | 5 | 2 | 50% | 3 | 1.67 | — |
| US-10 | POS flag for uncertain reservations | 5 | 2 | 50% | 5 | 1.0 | — |

---

## AI critique

**Highest-score row — US-02 (data freshness indicator, RICE 50.0):**
RICE ranks US-02 above US-01 because effort is 1 week and confidence is 100%. But US-02 has a hidden dependency — a freshness indicator without a verdict to attach it to is meaningless. The score is technically correct but misleading. *Decision: ship US-01 and US-02 together in sprint 1; do not treat US-02 as independently deliverable.*

**Lowest-confidence row — US-08 (confidence model, 50%):**
US-08 is the AI engine that makes US-01's confidence labels accurate. Its 50% confidence reflects one unresolved question: store-level signal quality (sales velocity, inbound transfer data) is untested at scale. If US-08 slips or the signal pipeline underdelivers, US-01 degrades to SAP-count-only — which is the current experience with a new label. This is the critical-path risk for the whole feature. *Decision: schedule a data-quality spike on store signals in sprint 1, parallel to US-01 integration work.*

---

## Scoring notes

- **Reach** = estimated quarterly users or stakeholders who encounter the story (relative, not absolute counts — validate against Meridian OMS data)
- **Impact** = contribution to phantom-stock cancellation reduction: 0.5 low, 1 medium, 2 high, 3 massive
- **Confidence** = {10%, 50%, 80%, 100%} only; reflects certainty in reach and impact estimates
- **Effort** = estimated person-weeks; all estimates are pre-spike and should be confirmed in sprint 1 refinement
