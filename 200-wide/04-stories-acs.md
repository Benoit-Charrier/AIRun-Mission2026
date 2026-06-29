---
product: Meridian retail site and app
feature: AI availability assistant
kata: 2.W.5
date: 2026-06-25
---

## User stories

| # | Story |
|---|-------|
| US-01 | As a click-&-collect shopper, I want to see a confidence-labelled availability verdict on the product page before I reserve, so that I don't travel to a store for an item that isn't there. |
| US-02 | As a click-&-collect shopper, I want to know when the stock data was last updated, so that I can judge how much to trust the verdict. |
| US-03 | As a click-&-collect shopper who sees an "uncertain" verdict, I want to be shown the nearest alternative store with a "likely available" verdict, so that I can redirect my trip without extra searching. |
| US-04 | As a click-&-collect shopper, I want the assistant to tell me plainly when it has no reliable data, so that I'm never shown a false "available" when the system can't assess shelf reality. |
| US-05 | As a click-&-collect shopper with an active reservation, I want a push notification if my item's availability status drops to "not available" before my pickup window, so that I can cancel without making the trip. |
| US-06 | As a store operations lead, I want a daily digest of "uncertain" verdicts issued for my store, so that I can prioritise shelf checks before the pickup windows open. |
| US-07 | As a click-&-collect shopper on mobile, I want the availability verdict to appear within 2 seconds of selecting my pickup store, so that it doesn't add friction to the reservation flow. |
| US-08 | As a Meridian product manager, I want the confidence model to use SAP count, sales velocity, and inbound transfer status, so that the verdict reflects real shelf dynamics rather than a stale snapshot. *(AI Eval Card — see below)* |
| US-09 | As a click-&-collect shopper, I want the assistant to handle a SAP service outage gracefully, so that I'm given a clear fallback rather than a false confidence signal. |
| US-10 | As a store associate, I want reservations made on an "uncertain" verdict to be flagged in the POS queue, so that I can proactively verify stock before the customer arrives. |

---

## Gherkin acceptance criteria — top four stories

### US-01 — Confidence-labelled verdict

**Given** a shopper selects a product and chooses a pickup store  
**When** the availability assistant runs  
**Then** the product page displays one of three labels: "Likely available", "Uncertain — stock data may not reflect shelf reality", or "Not available at this store"  
**And** the label is visible before the "Reserve" button is active

*Adversarial patch — error path:*  
**Given** the SAP sync or store-signal service is unreachable  
**When** the assistant runs  
**Then** the label defaults to "Uncertain" (never to "Likely available") and a plain-language explanation is shown ("We can't confirm stock right now — call the store or choose delivery")

*Adversarial patch — NFR:*  
Verdict must render within **2 seconds (p95)** of store selection; if the call times out after 2s, default to "Uncertain" and surface the fallback message — do not block the page.

---

### US-03 — Nearest alternative store fallback

**Given** the assistant returns an "Uncertain" or "Not available" verdict for the selected store  
**When** the result is displayed  
**Then** the page shows up to two alternative stores within 25 km with a "Likely available" verdict, ordered by distance  
**And** each alternative store shows its distance and the same confidence label

*Adversarial patch — error path:*  
**Given** no alternative store within 25 km has a "Likely available" verdict  
**When** the fallback runs  
**Then** the page shows "No confirmed stock nearby — consider delivery" rather than a blank section or a false suggestion

*Adversarial patch — NFR:*  
Alternative store lookup must complete within the same 2s p95 budget as the primary verdict; results must not appear after the shopper has already scrolled past the verdict block.

---

### US-04 — No-data handling

**Given** the assistant cannot retrieve SAP data or store-level signals for the selected store  
**When** the verdict would otherwise be computed  
**Then** the displayed label is "Uncertain" — the assistant must never return "Likely available" in the absence of data  
**And** the shopper is shown a plain-language explanation and a direct link to call the store

*Adversarial patch — error path:*  
**Given** partial data is available (e.g. SAP count present but sales velocity unavailable)  
**When** the assistant computes the verdict  
**Then** the verdict uses available signals and labels itself "Uncertain" unless both SAP count and at least one store-level signal are present and fresh (< 6h)

*Adversarial patch — NFR:*  
The "data unavailable" state must be logged for monitoring; if > 15% of verdict requests in a region return no-data within a 1h window, an ops alert fires.

---

### US-09 — SAP outage graceful degradation

**Given** the SAP inventory service returns a 5xx or times out  
**When** a shopper requests an availability verdict  
**Then** the assistant returns "Uncertain" with the message "Stock information is temporarily unavailable — we recommend calling the store before travelling"  
**And** the reservation flow remains available (the assistant does not block checkout)

*Adversarial patch — error path:*  
**Given** SAP is degraded (latency > 4s) but not fully down  
**When** the assistant call times out at the 2s client-side threshold  
**Then** the same "Uncertain" label and message are shown — a slow response is treated identically to a failed one from the shopper's perspective

*Adversarial patch — NFR:*  
Circuit-breaker: after 5 consecutive SAP timeouts in a 60s window, the assistant switches to "Uncertain-only" mode and stops querying SAP until a health check passes; recovery must not require a page reload.

---

## AI Eval Card stub — US-08 (confidence verdict model)

**Story:** As a Meridian product manager, I want the confidence model to use SAP count, sales velocity, and inbound transfer status to produce a three-class verdict, so that shoppers receive a calibrated signal rather than a stale binary badge.

| Field | Value |
|-------|-------|
| **Confidence threshold — "Likely available"** | SAP count ≥ 2 units **and** sales velocity < 1 unit/hour in the last 4h **and** data freshness < 6h |
| **Confidence threshold — "Uncertain"** | SAP count ≥ 1 but sales velocity ≥ 1 unit/hour, **or** data freshness ≥ 6h, **or** partial signal only |
| **"Not available"** | SAP count = 0 and no inbound transfer confirmed within 24h |
| **Refusal trigger** | Return "Uncertain" (never "Likely available") when: SAP unreachable, data freshness > 12h, or confidence score < 0.6 from the model |
| **Latency ceiling** | p95 < 2s end-to-end; model inference < 200ms; SAP + signal fetch < 1.5s |
| **Fallback** | On any model or data failure: default to "Uncertain" + plain-language message; never block the reservation flow |
| **Eval metric** | Phantom-stock cancellation rate at pickup ≤ 2% in stores where assistant is active vs. control stores (holdout); false-"Likely available" rate (item not found at pickup despite "Likely available" verdict) ≤ 1% |

---

## Adversarial pass — gaps found (fresh session)

1. **US-01 / US-08:** What happens when a shopper reserves on a "Likely available" verdict and the item sells in-store before their pickup window? The current ACs don't cover post-reservation status change — only US-05 (notification) addresses this, and it's not linked back to US-01. *Patched: added cross-reference to US-05 in the DoR checklist; US-05's AC needs to fire within 30 min of the status change, not just "before the pickup window."*

2. **US-03:** "Up to two alternative stores within 25 km" — what if the shopper is in a rural area with no stores within 25 km? The fallback handled no stock but not no stores. *Patched: added "No confirmed stock nearby" case to US-03 AC above.*

3. **NFR gap across all stories:** Accessibility not named anywhere. The confidence label is colour-coded in the UX design — colour alone fails WCAG 2.1 AA. *Patch: add to US-01 AC — label text must be accompanied by an icon + text string, not colour alone; must pass WCAG 2.1 AA contrast ratio (4.5:1).*

**Accessibility patch — appended to US-01:**  
The verdict label must not rely on colour alone to communicate state; each label must include a text string and an icon; colour contrast ratio must meet WCAG 2.1 AA (4.5:1 minimum).
