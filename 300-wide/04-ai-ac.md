---
product: Meridian retail site and app
feature: AI availability assistant
kata: 3.W.5
date: 2026-06-25
---

## User story

**AS** a click-&-collect shopper,
**I WANT** to see a confidence-graded availability estimate for my chosen store — with a freshness label and a fallback when the system can't confirm —
**SO THAT** I know before I drive whether the item is likely to be there, and I'm never misled by a confident "In stock" that doesn't reflect shelf reality.

---

## Base acceptance criteria (supplied)

| # | Given | When | Then |
|---|-------|------|------|
| AC1 | A product has store stock data | The shopper views the product page | An availability indicator is shown per nearby store |
| AC2 | No store within range has the item | The availability assistant runs | "Not collectable nearby" is shown + a delivery option is offered |
| AC3 | Stock data is missing for a store | The availability assistant runs | That store is omitted — the assistant does not guess |
| AC4 | The shopper taps a store | They expand its detail | Last-confirmed time + distance are shown |

---

## AI-specific acceptance criteria

**AI-AC1 — Confidence**
WHEN the availability model returns a stock-confidence score < 0.7 (SAP count ≥ 1 but data freshness > 6h, OR sales velocity ≥ 1 unit/hr in the last 4h, OR only partial signal available), THEN the label displayed is "Likely in stock" — not "In stock" — and the last-confirmed timestamp is shown inline alongside it.

**AI-AC2 — Refusal / fallback**
WHEN the SAP sync for a store is > 30 min stale OR the signal service is unreachable OR the model returns a confidence score below the refusal threshold (< 0.6), THEN display "Can't confirm right now — call the store" with the store phone number, and suppress any positive ("In stock" or "Likely in stock") availability state.

**AI-AC3 — Latency**
The availability indicator must resolve within 1.5 s (p95) of the shopper selecting a pickup store. Responses taking > 1.5 s show a loading skeleton. A 4 s timeout triggers AI-AC2 (fallback state); the page is never blocked.

**AI-AC4 — Disclosure**
Every availability estimate (positive or uncertain) carries an "Estimated from store data" label. Tapping the label opens a tooltip showing: (1) when the data was last synced, (2) what the estimate is based on, and (3) an explicit statement that it is not a guaranteed hold.

**AI-AC5 — Feedback**
A "Was this accurate?" prompt appears on the pickup-confirmation screen (post-collection). A "wrong at pickup" report is logged server-side with: store ID + SKU + verdict shown at time of reservation + timestamp. Reports are aggregated weekly per store for accuracy monitoring.

**AI-AC6 — Negative AC**
The assistant MUST NOT:
- State or display an exact unit count ("3 units in stock")
- Promise or imply a guaranteed hold ("reserved for you")
- Display the green "In stock" state when confidence < 0.7 OR data freshness > 12h OR the model has returned a refusal
