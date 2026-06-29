---
product: Meridian retail site and app
feature: AI availability assistant
kata: 3.W.2
date: 2026-06-25
---

## Nielsen heuristic review — click-&-collect product page and reservation flow

**Method:** screens reviewed — product page (availability label), reservation confirmation, pickup-counter email. Fresh AI session used for initial violation scan; findings cross-checked against lived friction and retained only where heuristic violated + screen element can both be named.

---

| Priority | Heuristic | Violation | Screen / element | Redesign implication |
|----------|-----------|-----------|-----------------|---------------------|
| 🔴 Critical | **H1 — Visibility of system status** | "In stock" label is binary and timeless — no sync timestamp, no confidence signal, no indicator that the data may be 15–30 min stale | Product page: availability label (e.g. green "In stock" badge) | Replace binary label with confidence-graded label + freshness timestamp |
| 🔴 Critical | **H5 — Error prevention** | Reservation flow allows a shopper to commit a trip on an uncertain stock signal with no warning or friction; no checkpoint between "reserve" and "drive" | Product page → reservation CTA flow | Surface the confidence cue and fallback *before* the Reserve button activates, not after |
| 🟠 High | **H9 — Help users recognise, diagnose, and recover from errors** | After phantom-stock discovery at the counter, no in-product recovery path exists: no alternative store offered, no delivery option surfaced, no next-step guidance | Pickup counter (no screen — gap in the product) | Add "No confirmed stock nearby" fallback + alternative store suggestions in the product page flow |
| 🟡 Medium | **H2 — Match between system and real world** | "In stock" implies certainty and ownership; the reality is a probabilistic estimate from a 15–30 min stale count. The label creates a false mental model. | Product page: availability label language | Use language that matches the actual system capability: "Likely in stock", "Uncertain", "Not available" |
| 🟡 Medium | **H10 — Help and documentation** | After a cancellation there is no guidance on what the shopper can do differently: call the store, choose delivery, check an alternative location | Post-cancellation state (none exists in the current product) | Add contextual guidance at the moment of uncertainty (pre-reservation), not only post-failure |

**Discarded findings (from AI scan):** suggestions about checkout flow speed and cart abandonment — these do not violate a named heuristic for the availability-specific surface and are out of scope for this feature.
