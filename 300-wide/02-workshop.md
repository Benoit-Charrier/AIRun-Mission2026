---
product: Meridian retail site and app
feature: AI availability assistant
kata: 3.W.3
date: 2026-06-25
---

## Workshop plan

**The one decision to close:** Do we show a confidence-graded availability estimate with a freshness label and a fallback state, or suppress availability entirely until a store physically confirms the item is ready to collect?

**Decision-owner:** Sarah Chen (Head of CX)

| Field | Detail |
|-------|--------|
| Goal | Close one decision: which availability disclosure model ships in v1 |
| Must decide | Confidence-graded estimate (show with caveats) vs. suppress-until-confirmed |
| Explore only | Specific label wording, colour system, alternative store UI — downstream of the decision |
| Out of scope | Pricing, loyalty, POS integration, reservation holds |
| Decision-owner | Sarah Chen (Head of CX) — has authority to commit the design direction |
| Participants | Sarah Chen (CX), David Park (Retail Ops), Marco Rossi (Regional GM), Engineering lead |
| Timeboxes | 5 min frame · 15 min diverge (HMW + ideas) · 10 min converge (synthesis → K 3.W.4) |

---

## How Might We — 10 questions clustered into 3 themes

### Theme 1 — Honest signal before reservation

1. HMW help shoppers gauge how reliable the "in stock" signal is before they reserve?
2. HMW show shoppers whether the item was recently confirmed on the shelf?
3. HMW help a shopper make a faster, lower-risk reservation decision?

**3 ideas:**
- (a) Confidence-graded label with last-confirmed timestamp: "Likely in stock — confirmed 12 min ago"
- (b) Freshness indicator only: show "Last synced: 18 min ago" below the label
- (c) Tiered disclosure: green = confirmed within 10 min / amber = 10–30 min stale / grey = > 30 min stale

---

### Theme 2 — Graceful uncertainty and recovery

4. HMW prevent the system from making a promise it can't keep?
5. HMW help shoppers when the system can't confirm availability?
6. HMW redirect a shopper to an alternative store when their store is uncertain?
7. HMW reduce the cost of a wasted trip if the item turns out not to be there?

**3 ideas:**
- (a) "Can't confirm right now — call the store" fallback with store phone number, suppressing any positive availability state
- (b) Show 2 nearby alternative stores ranked by confidence + distance when primary is uncertain or unavailable
- (c) "Reserve and we'll confirm in 10 min" hold — notify when confirmed ready (requires SAP mutation — high effort)

---

### Theme 3 — Post-reservation loop

8. HMW let a shopper cancel before they leave home if availability status changes?
9. HMW help store associates know which reservations might have stock issues before the pickup window opens?
10. HMW create a feedback signal that improves availability accuracy over time?

**3 ideas:**
- (a) Push notification if status drops to "not available" after reservation
- (b) POS flag for reservations made on an "uncertain" verdict — associate proactively verifies
- (c) Pickup-screen feedback prompt: "Was this accurate?" logged with store + SKU + timestamp

---

*Note: Theme 3 ideas are carry-forward candidates to v2 (status-change detection pipeline not yet ready — see Module 200 scope outputs). Surfaced here for completeness; not in scope for workshop decision.*
