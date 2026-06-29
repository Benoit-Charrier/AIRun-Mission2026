---
product: Meridian retail site and app
feature: AI availability assistant
kata: 2.W.7
date: 2026-06-25
status: draft
---

## Problem

~7% of Meridian click-&-collect orders are cancelled at pickup because the online stock indicator is a point-in-time SAP snapshot that does not reflect shelf reality. Shoppers drive to stores for items that are not there; stores issue last-minute cancellations; customer trust erodes.

## Vision

The availability assistant shows click-&-collect shoppers a confidence-labelled verdict — "Likely available", "Uncertain", or "Not available" — before they reserve, derived from SAP inventory count cross-referenced with store-level sales velocity and inbound transfer status. The assistant does not guarantee availability; it surfaces the probability so the shopper decides with real information, not a stale badge.

## Target user

Click-&-collect shoppers who reserve online to avoid a wasted trip and currently distrust or work around the stock indicator (phones the store, skips click-&-collect entirely).

## Top stories and acceptance criteria

| Story | AC summary |
|-------|-----------|
| **US-01** — Confidence-labelled verdict | Three-label verdict displayed before "Reserve" is active; defaults to "Uncertain" on any service failure; p95 < 2s; WCAG 2.1 AA (no colour-only labelling) |
| **US-02** — Data freshness indicator | Timestamp of last data sync shown alongside the verdict; no additional latency budget |
| **US-04** — No-data handling | Never returns "Likely available" when data is absent or stale (> 12h); plain-language fallback + store contact link shown |
| **US-03** — Nearest alternative store | Up to 2 alternatives within 25 km shown on "Uncertain" / "Not available"; "No confirmed stock nearby" message when none exist |
| **US-09** — SAP outage graceful degradation | Defaults to "Uncertain" on 5xx or timeout; circuit-breaker after 5 consecutive SAP timeouts in 60s; reservation flow never blocked |

## Scope boundary

**In:** confidence verdict display, data freshness indicator, no-data handling, alternative store fallback, SAP outage degradation.  
**Deferred to v2:** push notification on status change (US-05), store ops digest (US-06), POS flag for uncertain reservations (US-10).  
**Out of scope:** reserve-and-hold inventory lock, real-time POS polling, cross-store stock reallocation.

## Success metric

Phantom-stock cancellation rate at pickup: **from ~7% to ≤ 2%** within 6 months of rollout, measured weekly in the OMS by region; attributed via holdout (assistant-active stores vs. matched control stores).

---

## Decision Memory

**Decision:** Build a prediction-only availability assistant rather than a reserve-and-hold system.  
**Rationale:** A reservation lock that holds inventory for 30 minutes would eliminate phantom-stock cancellations by design — but requires real-time inventory mutation and POS integration across 1,400 stores, which is out of scope for this program phase (SAP is the inventory ground truth; mutation risk is high). The prediction assistant ships in weeks, not quarters, and reduces the cancellation rate without mutating inventory state.  
**Rejected alternative:** Reserve-and-hold with a 30-minute inventory lock per reservation. Rejected due to POS integration complexity, SAP mutation risk, and timeline — revisit in Phase 2 once unified inventory API is live.  
**Owner:** Product lead. **Review trigger:** if phantom-stock cancellation rate does not reach ≤ 4% after 3 months, revisit reservation-lock feasibility.
