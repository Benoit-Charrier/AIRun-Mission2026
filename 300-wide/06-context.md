---
product: Meridian retail site and app
feature: AI availability assistant
kata: 3.W.7
date: 2026-06-25
---

# CONTEXT.md — Meridian AI Availability Assistant

## Feature in one sentence
An AI availability indicator on the product page estimates whether a click-&-collect item is likely on the shelf at a nearby Meridian store, showing a confidence-graded label, a data freshness timestamp, and a plain-language fallback when the system cannot confirm.

## Who uses it
Click-&-collect shoppers on the Meridian product page — mobile-first (>70% of traffic); also rendered on web. They are at the decision point of whether to reserve and drive; the feature is shown before the Reserve button activates.

## Technical environment
- **Frontend:** React (web) + React Native (app); design tokens via design-system package `@meridian/ds`
- **Data source:** SAP inventory sync (15–30 min cadence); store-level sales velocity + inbound transfer signals from the confidence model (US-08 / Module 200)
- **Availability verdict:** computed server-side via the Meridian Availability API; non-PII inputs only (SKU, store ID, stock count, velocity signal)
- **Confidence model:** returns a `confidence_score` (0–1) and a `verdict` enum: `LIKELY_AVAILABLE` | `UNCERTAIN` | `NOT_AVAILABLE` | `NO_DATA`
- **Latency target:** p95 < 1.5 s end-to-end; 4 s hard timeout; model inference < 200 ms
- **Auth:** no customer identity in the AI path; store proximity uses device location (permission-gated) or postcode input

## Hard constraints
- **MUST NOT** display exact unit counts (SAP count is not surfaced to the shopper)
- **MUST NOT** promise or imply a guaranteed hold on any stock
- **MUST NOT** show a green "In stock" state when `confidence_score` < 0.7 or data freshness > 12h
- **MUST NOT** block the reservation flow — the assistant degrades gracefully; the Reserve button remains available even in fallback state
- GDPR/CCPA: no personal data enters the AI path; device location is permission-gated and not persisted with the verdict

## Out of scope
- Reserve-and-hold inventory lock (SAP mutation — Phase 2)
- Real-time POS polling
- Push notification on post-reservation status change (US-05 — v2, pipeline not ready)
- POS flag for uncertain reservations (US-10 — Phase 2)
- Cross-store stock reallocation
- Personalised ranking by purchase history

## Related artefacts
- `04-ai-ac.md` — AI-specific acceptance criteria (6 clauses)
- `05-mockup.html` — lo-fi prototype (3-screen clickable flow)
- `06-spec.md` — component and state specification
- Module 200: `04-stories-acs.md` (US-01 through US-09), `06-prd.md` (scope boundary + Decision Memory)
