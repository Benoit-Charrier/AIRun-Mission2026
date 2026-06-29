---
product: Meridian retail site and app
feature: AI availability assistant
kata: 2.W.7
date: 2026-06-25
---

## Traceability matrix

**Outcome metric:** Phantom-stock cancellation rate at pickup — from ~7% to ≤ 2% (primary; measured weekly in OMS by region)

| Story | Moves metric? | Link |
|-------|:---:|------|
| US-01 — Confidence-labelled verdict | ✅ direct | Shoppers who see "Uncertain" or "Not available" avoid trips that would have cancelled — directly reduces phantom-stock cancellations |
| US-02 — Data freshness indicator | ✅ indirect | Shoppers who see stale data disclosed may choose not to reserve — reduces reservations on unreliable signals, protecting the metric |
| US-03 — Nearest alternative store | ✅ indirect | Redirects uncertain-verdict shoppers to a store with confirmed stock — converts potential cancellations into successful pickups |
| US-04 — No-data handling | ✅ direct | Prevents false "Likely available" verdicts on missing data — removes the most dangerous failure mode that inflates the cancellation rate |
| US-07 — 2s latency NFR | ✅ indirect | Slow verdict load causes shoppers to skip it and reserve blindly — without this NFR met, adoption drops and the metric is unaffected |
| US-08 — Confidence model | ✅ direct | The AI engine that makes US-01 accurate; without it, US-01 degrades to SAP-count-only (the current broken experience) |
| US-09 — SAP outage graceful degradation | ✅ direct | Prevents false "Likely available" during outages — protects the metric from regression during incidents |
| US-05 — Push notification *(deferred)* | ✅ indirect | Cancels post-reservation trips when status changes — would further reduce cancellation rate; deferred to v2 |
| US-06 — Store ops digest *(deferred)* | ✅ indirect | Proactive shelf checks reduce phantom-stock at source — longer-term metric improvement; deferred |
| US-10 — POS flag *(deferred)* | ✅ indirect | Store associates verify uncertain reservations before pickup window — deferred |

---

## Flags

**Dead metrics (metric with no linked story):** none — the single outcome metric (phantom-stock cancellation rate) is covered by multiple stories.

**Unlinked stories (story with no metric link):** none — all 10 stories trace to the primary metric, directly or indirectly.

**Dependency alert:** US-02, US-03, US-07 are all indirect — they move the metric only if US-01 ships and is adopted. If US-01 is descoped or delayed, these three lose their metric link. Flag in sprint planning: US-01 is the single critical dependency for the entire feature.
