---
product: Meridian retail site and app
feature: AI availability assistant
kata: 2.W.4
date: 2026-06-25
---

## Competitor comparison

| Product | Approach | Strength | Weakness | Differentiator dimension |
|---------|----------|----------|----------|--------------------------|
| **IKEA** | Real-time store stock count pulled from WMS; binary in/out with exact unit count displayed on product page | High accuracy — IKEA's warehouse-style stores map 1:1 to their WMS; what the system says is usually on the shelf | No confidence signal, no data-freshness indicator; count drops to zero only after WMS update (lag still exists between sale and sync) | Count accuracy, not prediction confidence |
| **Argos** (UK) | Reservation-first model; store is a warehouse, not a browsing floor; stock shown as "available to reserve" only when confirmed | Near-zero phantom-stock rate — the store format eliminates the shelf/WMS mismatch entirely | Model is store-format-dependent; doesn't translate to a browsing-floor retailer like Meridian where shelf reality diverges from WMS | Format solves the problem rather than predicting it |
| **Walmart** (US) | Real-time inventory with ML-driven "low stock" label; demand velocity used to flag items likely to sell out before pickup window | Surfaces demand-side risk ("selling fast") alongside supply signal; reduces surprise cancellations | "Low stock" is a demand label, not a shelf-accuracy label — it doesn't distinguish phantom stock from genuine sell-out; no confidence level exposed to shopper | Demand-signal overlay, not shelf-accuracy confidence |
| **Meridian (us)** | SAP inventory sync cross-referenced with store-level signals (recent sales velocity, inbound transfer status); confidence-labelled verdict returned before reservation | Can expose data uncertainty to the shopper explicitly rather than masking it behind a binary badge | Dependent on SAP sync freshness; confidence label only as good as signal recency; requires store-level signal instrumentation not yet in place everywhere | **Confidence-labelled availability verdict — the shopper sees the reliability of the signal, not just the count** |

---

## Named differentiator

**Surface the reliability of the stock signal, not just its value** — every competitor shows a count or a binary badge; Meridian's assistant exposes whether that signal can be trusted at the moment of reservation, so the shopper decides with calibrated information rather than a phone call.

---

## Lifted AI feature

**Walmart's demand-velocity overlay** — using recent sales rate to flag items at risk of sell-out before pickup, not just items currently showing low count. Lifted into Meridian: cross-reference the SAP unit count against store-level sales velocity (units sold in last 4h) and inbound transfer status to produce the confidence label. A count of 3 units with sales velocity of 2/hour and no inbound transfer = "uncertain"; a count of 3 with zero recent movement and a confirmed transfer = "likely available." This is the AI capability that carries into K 2.W.5's AI Eval Card story and the Deep series eval.

> *(Competitor data synthesised from public product pages, app-store listings, and earnings-call references — unverified; validate specifics before using in client-facing material. Walmart ML-inventory claim sourced from 2023–2024 earnings calls — unverified at story level.)*
