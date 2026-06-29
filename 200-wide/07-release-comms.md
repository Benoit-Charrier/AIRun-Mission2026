---
product: Meridian retail site and app
feature: AI availability assistant
kata: 2.W.8
date: 2026-06-25
status: draft
---

## Part 1 — Release-scope confirmation

**In this release:**

| Story | Description |
|-------|-------------|
| US-01 | Confidence-labelled availability verdict ("Likely available" / "Uncertain" / "Not available") displayed on the product page before the Reserve button is active |
| US-02 | Data freshness indicator — timestamp of last stock sync shown alongside the verdict |
| US-03 | Nearest alternative store suggestions (up to 2, within 25 km) when verdict is "Uncertain" or "Not available" |
| US-04 | No-data handling — system defaults to "Uncertain" when data is absent or stale; plain-language fallback message shown |
| US-09 | SAP outage graceful degradation — circuit-breaker on 5 consecutive timeouts; reservation flow never blocked |

**Deferred to v2:**
- US-05 — Push notification on post-reservation status change (status-change detection pipeline not ready)
- US-06 — Store operations daily digest (ops adoption tooling out of scope for v1)
- US-10 — POS flag for uncertain reservations (POS integration deferred to Phase 2)

**Out of scope (this program phase):**
- Reserve-and-hold inventory lock
- Real-time POS polling
- Cross-store stock reallocation

---

## Part 2 — Open risks

| # | Risk | Owner | Mitigation |
|---|------|-------|------------|
| R1 | **SAP signal freshness below threshold in some regions** — store-level signals (sales velocity, inbound transfers) may not meet the < 6h freshness requirement outside the EU-West pilot; affects confidence label accuracy at launch | Data Engineering Lead | Define minimum viable signal coverage (≥ 80% of stores in pilot region) as a hard go/no-go gate; launch EU-West first where SAP sync cadence is most reliable; other regions follow once signal coverage is confirmed |
| R2 | **Store-level signal pipeline untested at scale** — US-08 confidence model is at 50% confidence; if the pipeline underdelivers by code freeze, US-01 degrades to SAP-count-only (all verdicts show "Uncertain" until signals are live) | Architecture Lead | Sprint 1 data-quality spike on sales-velocity and inbound-transfer feeds; gate model training on spike outcome; communicate degraded-mode risk to stakeholders before launch commitment |
| R3 | **Accessibility compliance** — WCAG 2.1 AA requires colour + icon + text on confidence labels; browser testing across supported devices not yet complete | Design Lead | Accessibility audit included in DoD for US-01; release blocked if AA contrast ratio (4.5:1 minimum) fails on any supported browser/platform |

---

## Part 3 — Stakeholder notifications

### Delivery leads (scope + risks + timeline)

> **AI availability assistant — v1 release update**
>
> **What's shipping:** Five stories confirmed in scope — confidence-labelled availability verdict, data freshness indicator, nearest alternative store suggestions, no-data handling, and SAP outage degradation. Three stories deferred to v2: push notifications, store ops digest, POS flag.
>
> **Open risks to track:** (R1) SAP signal freshness — EU-West launch gated on ≥ 80% store coverage; (R2) confidence model pipeline — sprint 1 spike determines whether v1 ships with full ML labels or SAP-count-only fallback; (R3) accessibility audit must pass before release sign-off.
>
> **Timeline:** Sprint 1 spike (signal pipeline + SAP integration) → code freeze → accessibility audit → EU-West pilot launch → regional rollout. Confirm dates in next sprint planning.

### Business and external stakeholders (value + timeline, plain language)

> **What's changing for shoppers**
>
> Starting [launch date], Meridian's product page will show a clear signal — "Likely available", "Uncertain", or "Not available" — before a customer confirms a click-&-collect reservation, alongside when the stock data was last updated. If the item looks uncertain at one store, the page will suggest the nearest store where it is confirmed available.
>
> **Why it matters:** Today ~7% of click-&-collect orders are cancelled at pickup because the stock indicator doesn't reflect shelf reality. This feature gives shoppers the information they need to make the right call before they travel.
>
> **When:** EU-West pilot launches [date TBC]; regional rollout follows. Customers will see the new verdict automatically — no app update required.

---

## Part 4 — "What's New" release note

*(Each bullet verified against `06-traceability.md` — only shipped stories included)*

- **Stock confidence verdict** — the product page now shows whether an item is "Likely available", "Uncertain", or "Not available" at your chosen store before you reserve, so you know before you travel. *(US-01 ✓)*
- **Data freshness indicator** — a timestamp shows when the stock information was last updated, so you can judge how current the signal is. *(US-02 ✓)*
- **Alternative store suggestions** — if stock at your chosen store is uncertain or unavailable, the page suggests up to two nearby stores where availability is confirmed. *(US-03 ✓)*
- **Honest "no data" state** — when the system cannot assess availability, it tells you clearly rather than showing a potentially false "in stock" badge. *(US-04 + US-09 ✓)*

*Not in this release: real-time notifications when reservation status changes — coming in v2.*

---

## Part 5 — Spec update on ship

Once v1 ships, update `06-prd.md` **Scope boundary** section: move US-05 (push notification on status change) from "Deferred to v2" to "In scope — next sprint" once the status-change detection pipeline is validated in the EU-West pilot.
