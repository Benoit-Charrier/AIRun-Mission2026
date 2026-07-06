---
case: Meridian Retail Group — Click & Collect
consumes_from: 6.W.4 (03-defects.md)
most_painful_defect: DEF-001
date: 2026-07-01
author: Benoit Charrier
---

# Root Cause Analysis — DEF-001

## Section 1: Defect summary

**DEF-001 — POS accepts phantom-stock pickup: customer leaves store with cancelled order**

- **Test case:** TC-08
- **Priority / Severity:** P1 / S1
- **Steps to reproduce:** Reserve `SKU-KETTLE-IT` at `S-IT-MI-01`. Between reservation and pickup, SAP inventory is updated to zero stock for that SKU/store combination. Customer scans QR code at POS. POS reads SAP inventory (stub returns 0) but the pickup-confirmation screen still displays "Ready for collection — please hand over item." Store staff hands over the item.
- **Expected:** POS detects `stock == 0` and displays "Item no longer available — order cancelled." Refund initiated automatically.
- **Actual:** Pickup confirmation proceeds. The SAP inventory response reaches the service layer but the guard condition is not evaluated before the confirmation screen renders.

**Why this defect was selected as most painful:** It directly expresses the documented 7% phantom-stock cancellation baseline that David Park identified as the store team's worst case. It is S1 (customer leaves empty-handed, no automated refund), P1 (blocks Italy pilot), and it represents the highest-density failure class in the prior pain-point data.

---

## Section 2: Root cause

**The condition that made this bug possible was that the SAP inventory read at pickup confirmation was treated as advisory — its result was written to a log but the POS confirmation flow had no guard that blocked handover when `available_stock == 0` — and no held-stock token was written at reservation time to compensate for the gap between reservation and pickup.**

### Hypotheses and evidence

| # | Hypothesis | Evidence to confirm | Evidence to rule out |
|---|---|---|---|
| H1 | Guard condition missing in POS confirmation component | Code review: the `stock_check` response is read into a variable but no `if available_stock > 0` gate exists before the `renderConfirmationScreen()` call | If the guard exists and was bypassed by a race condition — check for a concurrent thread or async rendering that could skip the guard |
| H2 | SAP response arrives after the confirmation screen has already rendered (async timing race) | Step trace showing the confirmation screen renders before the SAP callback resolves | If the SAP call is synchronous and blocking — confirm with a network trace or service log |
| H3 | No held-stock token written at reservation time, so the platform cannot distinguish between "stock went to zero after my customer reserved it" and "stock was always zero" | Check whether a `held_stock` or `reservation_lock` record is written to the inventory service at reservation time | If a held-stock token exists but is not checked at pickup — the condition is the missing check, not the missing token |

**Selected hypothesis: H1 + H3 combined.** The guard condition in the POS confirmation component does not exist (H1), and the absence of a held-stock token at reservation time means even a corrected guard has no authoritative pre-reservation baseline to compare against (H3). The two conditions interact: fixing H1 alone may reduce the rate but not eliminate it, because without a held-stock token the guard is checking real-time SAP stock that could legitimately be zero for reasons unrelated to this customer's reservation.

---

## Section 3: Guard test

**Title:** SAP stock-zero signal blocks pickup confirmation across three input shapes

**Preconditions:** SAP stub configured to return `available_stock: 0` for the requested SKU+store combination at the moment of QR scan.

| # | Input variant | Steps | Expected |
|---|---|---|---|
| G-01 | Single-item order, domestic (IT customer, IT store, Postepay) — record `E-007` | Scan QR; SAP stub returns 0 | POS displays cancellation message; no item handed; refund initiated; no "Ready for collection" screen rendered |
| G-02 | Cross-region order (IT customer, DE store) — record `E-001` with `zero_stock_at_pickup` stub | Scan QR at German store; SAP stub returns 0 | Same cancellation outcome; cross-region routing does not bypass the guard |
| G-03 | Multi-item order, one item at zero stock — record `E-010` with `SKU-SCARF-JP` at 0 | Scan QR; SAP returns 0 for `SKU-SCARF-JP`, 3 for `SKU-BAG-JP` | Partial-pickup flow triggered (not outright cancellation); guard fires per-item, not per-order |

**Why this exercises the condition, not just the instance:** G-01 is the original failing input. G-02 tests whether cross-region routing re-enters a code path that skips the guard. G-03 tests whether the guard is applied per-item or per-order, catching a second class of failure (full cancellation of a multi-item order when only one item is at zero stock).

---

## Section 4: Fix recommendation

Write a held-stock token to the cart service at the moment of Click & Collect reservation (decrement the SAP-visible available count by 1, write a `reservation_hold` record with the `order_id`, `sku`, `store_id`, and a TTL matching the 48-hour pickup window); at pickup confirmation, enforce a synchronous SAP read with a 30-second maximum staleness ceiling, and add a guard in the POS confirmation component that blocks `renderConfirmationScreen()` until the SAP response is received and `available_stock > 0` is confirmed — if the condition is false, route to the cancellation and refund flow.
