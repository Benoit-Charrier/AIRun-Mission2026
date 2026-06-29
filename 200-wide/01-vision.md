---
product: Meridian retail site and app
feature: AI availability assistant
kata: 2.W.2
date: 2026-06-25
---

## First draft

**Vision.**
By end of 2026, Meridian's click-&-collect experience will be one customers trust to save a trip, not one they hedge by phoning the store first. The availability assistant predicts whether an item is genuinely on the shelf at a nearby store — drawing on SAP inventory sync and store-level signals — so shoppers can reserve with confidence and stores can stop cancelling pickups that never had stock.

**Problem statement.**
~7% of Meridian click-&-collect orders are cancelled at pickup because the online stock indicator does not reflect real shelf availability, eroding customer trust and generating avoidable last-mile failures.

**Target user.**
Click-&-collect shoppers who reserve online to avoid a wasted trip and currently cannot trust the stock indicator.

**Outcome metric.**
Phantom-stock cancellation rate at pickup: from ~7% (baseline, 2024 EU average) to ≤ 2% within 6 months of rollout.

---

## Adversarial pass (fresh session)

**Critique 1 — mechanism is missing.**
The vision says "trust" and "confidence" but never names what the predictor does differently from the current stock indicator. "SAP inventory sync + store-level signals" is a technology gesture, not a user-facing behaviour. What does the shopper actually see that the current experience doesn't show?

**Critique 2 — metric has no measurement method.**
"≤ 2% within 6 months" reads like a target, not a metric. How is the cancellation rate measured — at what point in the journey, by which system, attributed to phantom-stock vs. shopper mind-change? Without this the metric is unfalsifiable in practice.

**Critique 3 — the data problem is buried.**
"SAP is the inventory ground truth" and phantom stock exists *because* SAP lags reality. Adding store-level signals on top of a lagging source may reduce but not eliminate the gap. The vision implies the predictor solves phantom stock; it should state it *predicts the probability* of availability given known data quality limits — accuracy is bounded by signal freshness.

---

## Revised vision (post-critique)

**Vision.**
By end of 2026, Meridian's click-&-collect product page will show shoppers a confidence-labelled availability verdict — "likely available", "uncertain", or "not available" — derived from SAP inventory sync cross-referenced with store-level signals (recent sales velocity, inbound transfer status). Shoppers stop phoning ahead; stores stop issuing cancellations for reservations that had no stock. The predictor does not guarantee availability; it surfaces the probability so the shopper decides with real information, not a stale badge.

**Problem statement.**
~7% of Meridian click-&-collect orders are cancelled at pickup because the online stock indicator is a point-in-time SAP snapshot that does not reflect shelf reality, eroding trust and creating avoidable last-mile failures.

**Target user.**
Click-&-collect shoppers who reserve online to avoid a wasted trip and currently distrust or work around the stock indicator (e.g. phone the store).

**Outcome metric.**
Phantom-stock cancellation rate at pickup: from ~7% (baseline = EU 2024 click-&-collect cancellations flagged "item not found at pickup" in OMS) to ≤ 2% within 6 months of rollout, measured weekly in the OMS by region; attribution via holdout (stores with assistant vs. without in matched pairs).
