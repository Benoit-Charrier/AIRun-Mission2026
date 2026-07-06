---
case: Meridian Retail Group — Click & Collect
consumes_from: 6.W.1 (00-test-plan.md)
date: 2026-07-01
author: Benoit Charrier
---

# Test Cases — Click & Collect Cross-Channel Flow

## In-scope reference (from 00-test-plan.md)

1. Web cart and reservation step
2. Identity stitch at first in-store pickup
3. SAP-sourced inventory check at pickup confirmation
4. Cross-region loyalty-points credit
5. POS pickup confirmation flow

---

## TC-01 — Happy-path reservation and pickup (Milano, Italian customer, Postepay)

**Category:** critical-path | **Priority:** 1 | **In-scope surface:** Web reservation + POS confirmation

**Preconditions:** Customer `C-IT-001` has a web account and an existing loyalty card `L-IT-001`. Item SKU `SKU-KETTLE-IT` is in stock at Milano store `S-IT-MI-01`. SAP inventory last synced <10s ago.

**Steps:**
1. Sign in to meridian.com as `C-IT-001`.
2. Add `SKU-KETTLE-IT` to cart; select Click & Collect at `S-IT-MI-01`; select 24-hour pickup window; pay via Postepay.
3. Receive QR code confirmation email and in-app notification.
4. At `S-IT-MI-01` POS: scan QR code.
5. POS reads SAP inventory (<30s staleness); confirms item available; prints receipt; credits loyalty points.

**Expected:** Pickup confirmed, receipt printed, loyalty points `+100` visible in app within 30 seconds, no errors.

---

## TC-02 — Happy-path reservation (German customer, German store, Klarna split-pay)

**Category:** critical-path | **Priority:** 1 | **In-scope surface:** Web reservation + payment

**Preconditions:** Customer `C-DE-001`, loyalty card `L-DE-001`. Item `SKU-COAT-DE` in stock at Berlin store `S-DE-BE-01`. Klarna split-pay enabled for Germany.

**Steps:**
1. Sign in as `C-DE-001`; add `SKU-COAT-DE`; select Click & Collect at `S-DE-BE-01`; pay via Klarna split-pay.
2. Klarna SCA challenge presented and completed.
3. QR code confirmation received.
4. At POS: scan QR; confirm pickup; credit loyalty.

**Expected:** SCA challenge completes, reservation confirmed, pickup confirmed, loyalty credited.

---

## TC-03 — Cross-region reservation (Italian customer, German pickup store)

**Category:** edge | **Priority:** 2 | **In-scope surface:** Web reservation + cross-region loyalty credit

**Preconditions:** Customer `C-IT-002` registered in Italy; selects Click & Collect at Berlin store `S-DE-BE-01`. Loyalty card `L-IT-002` registered to Italian region.

**Steps:**
1. Sign in as `C-IT-002`; add item to cart; select `S-DE-BE-01` for pickup.
2. Complete reservation via Visa card (cross-region, no Postepay).
3. Travel to Berlin; scan QR at `S-DE-BE-01`.
4. POS confirms pickup; loyalty points credited to Italian region account.

**Expected:** Reservation succeeds across regions. Pickup confirmed. Loyalty points credited to `L-IT-002` (Italy region account), visible in Italian loyalty app within 30 seconds.

---

## TC-04 — Identity stitch on first in-store pickup after web sign-up

**Category:** critical-path | **Priority:** 1 | **In-scope surface:** Identity stitch

**Preconditions:** Customer `C-UK-001` has web account (no prior in-store visits). In-store loyalty card `L-UK-001` exists in the legacy system under the same email address. This is the customer's first QR scan.

**Steps:**
1. Reserve item online as `C-UK-001`; receive QR code.
2. At London POS: scan QR code (first time this web account has triggered a stitch).
3. Platform detects matching loyalty card `L-UK-001` by email; merges accounts.

**Expected:** Single merged account created. Loyalty history from `L-UK-001` preserved. No duplicate account created. Customer receives merged-account confirmation notification.

---

## TC-05 — Loyalty-points credit for partial pickup (multi-item, one item out of stock at pickup)

**Category:** edge | **Priority:** 2 | **In-scope surface:** Loyalty-points credit + POS confirmation

**Preconditions:** Customer `C-JP-001` reserved 2 items at Tokyo store `S-JP-TO-01`. At pickup time, item 2 (`SKU-SCARF-JP`) is out of stock due to intervening sale. Item 1 (`SKU-BAG-JP`) is available.

**Steps:**
1. Customer arrives; POS scans QR code.
2. SAP inventory check: item 1 available, item 2 at zero stock.
3. POS surfaces partial pickup option; customer accepts item 1 only.
4. Partial receipt printed; loyalty points credited for item 1's value only.

**Expected:** Partial pickup confirmed. Points proportional to item 1's value credited within 30s. Refund initiated for item 2. POS receipt shows partial fulfilment.

---

## TC-06 — SAP inventory freshness at 47h59m into the 48h pickup window

**Category:** edge | **Priority:** 2 | **In-scope surface:** SAP inventory check

**Preconditions:** Reservation made 47h59m ago (within the 48h window by 1 minute). SAP last synced 25 seconds ago (within the 30s freshness budget).

**Steps:**
1. Customer scans QR at POS with 1 minute remaining in the pickup window.
2. Platform reads SAP inventory (25s-old data).
3. Item is confirmed in stock; handover proceeds.

**Expected:** Pickup proceeds normally. Window-boundary edge does not trigger an expiry error. SAP freshness check passes (25s < 30s ceiling).

---

## TC-07 — PSD2 SCA failure holds reservation for 10-minute retry window

**Category:** negative | **Priority:** 1 | **In-scope surface:** Web reservation (EU SCA)

**Preconditions:** Customer `C-DE-002` in Germany; Klarna SCA challenge configured to fail on first attempt (test stub).

**Steps:**
1. Customer selects Click & Collect, attempts to pay via Klarna.
2. SCA challenge fails (stub returns error).
3. Platform should hold the reservation for a 10-minute retry window instead of immediately cancelling.

**Expected:** Reservation is held (status: `pending_sca_retry`), not cancelled. Customer is notified to retry within 10 minutes. After 10 minutes with no retry, reservation is released and item returned to inventory.

---

## TC-08 — SAP inventory returns zero stock between reservation and pickup (phantom-stock cancel)

**Category:** negative | **Priority:** 1 | **In-scope surface:** SAP inventory check at pickup

**Preconditions:** Item reserved at `S-IT-MI-01`. Between reservation and pickup, another customer purchases the last unit in-store. SAP inventory sync updates to zero stock.

**Steps:**
1. Customer arrives and scans QR code.
2. POS reads SAP inventory: zero stock returned.
3. Platform must reject the pickup confirmation.

**Expected:** POS displays "Item no longer available — order cancelled" message. Refund is automatically initiated. No item is handed over. Defect class: phantom-stock cancellation — this is the documented 7% baseline scenario.

---

## TC-09 — Identity-merge collision — loyalty number resolves to two customer IDs

**Category:** negative | **Priority:** 1 | **In-scope surface:** Identity stitch

**Preconditions:** Loyalty card `L-DUPE-001` is associated with two customer records in the legacy system (a known data-quality issue from the pre-migration dataset). Customer `C-IT-003` scans QR code at pickup; platform attempts identity stitch.

**Steps:**
1. Customer scans QR at POS.
2. Platform looks up loyalty card `L-DUPE-001` during stitch; finds two matching customer IDs.
3. Platform must not merge records without deterministic resolution.

**Expected:** Platform escalates to a deterministic resolution rule (e.g., oldest account wins) or surfaces a conflict to the store operator rather than silently merging. No cross-customer loyalty data leak. Escalation logged for DPO review.

---

## TC-10 — SAP timeout at pickup confirmation

**Category:** negative | **Priority:** 1 | **In-scope surface:** SAP inventory check

**Preconditions:** SAP sandbox configured to time out (>5s response) on the inventory read request at pickup time.

**Steps:**
1. Customer scans QR at POS.
2. Platform sends inventory read to SAP; SAP does not respond within 5s.

**Expected:** Platform falls back to the reservation snapshot (the inventory state at reservation time) rather than blocking the pickup indefinitely. POS displays a degraded-mode warning. Fallback path is logged. No silent success with stale data.

---

## TC-11 — POS QR code scan with wrong customer ID (theft attempt)

**Category:** negative | **Priority:** 2 | **In-scope surface:** POS confirmation

**Preconditions:** Customer `C-IT-004` attempts to use QR code belonging to customer `C-IT-001`'s order.

**Steps:**
1. `C-IT-004` scans QR code at POS.
2. Platform checks: presenting customer ≠ reservation customer.

**Expected:** Pickup rejected. POS displays "QR code not valid for this customer." No item handed over. Incident logged.

---

## TC-12 — Reservation at 47h00m, SAP sync data is 31 seconds old (exceeds freshness ceiling)

**Category:** edge | **Priority:** 2 | **In-scope surface:** SAP inventory check

**Preconditions:** SAP last synced 31 seconds ago — just over the 30s freshness ceiling.

**Steps:**
1. Customer scans QR code at POS.
2. Platform reads SAP inventory; cached data is 31s old.

**Expected:** Platform requests a fresh SAP read before confirming pickup (cache miss forces refresh). Does not use stale data. Adds observable latency; POS UI shows a loading state.

---

## TC-13 — Klarna split-pay cancelled mid-reservation (payment provider webhook)

**Category:** negative | **Priority:** 2 | **In-scope surface:** Web reservation

**Preconditions:** Customer `C-NO-001` completes Klarna split-pay; while the reservation is being written, Klarna fires a cancellation webhook (simulates a payment reversal before fulfilment).

**Steps:**
1. Klarna split-pay selected; SCA completed.
2. Klarna fires cancellation webhook while reservation is in `creating` state.
3. Platform must roll back the reservation atomically.

**Expected:** Reservation does not persist in the system. Item is returned to available inventory. Customer notified of cancellation with reason "payment cancelled by provider." No orphaned reservation record.

---

## TC-14 — Customer attempts pickup with a different government ID than the reservation name

**Category:** negative | **Priority:** 3 | **In-scope surface:** POS confirmation (identity check)

**Preconditions:** Reservation is under name "Marco Rossi." Customer presents government ID showing "Marco Giuseppe Rossi."

**Steps:**
1. Store staff compares reservation name with government ID.
2. Names differ by a middle name.

**Expected:** Defined policy is applied (documented in store ops runbook) — either a fuzzy-match threshold accepts the pickup, or escalation to a manager. The system surfaces the policy clearly; it does not silently accept or reject. (Note: policy must be documented — absence of a policy is itself a finding.)

---

## TC-15 — Empty loyalty number field — no loyalty credit, no crash

**Category:** edge | **Priority:** 3 | **In-scope surface:** Loyalty-points credit

**Preconditions:** Customer `C-US-001` has a web account with no loyalty number (never enrolled).

**Steps:**
1. Customer completes Click & Collect reservation and pickup.
2. Platform attempts loyalty credit; loyalty number field is null.

**Expected:** Pickup completes successfully. No loyalty credit issued (customer was never enrolled). No error thrown; no POS crash. Null loyalty number handled gracefully.

---

## TC-16 — Multi-item order, pickup at 47h59m, one item added to cart after reservation (modification attempt)

**Category:** edge | **Priority:** 3 | **In-scope surface:** Web reservation + POS confirmation

**Preconditions:** Customer reserved 2 items. After reservation, they attempt to add a third item to the same Click & Collect order from the web.

**Steps:**
1. Customer opens their active Click & Collect reservation on meridian.com and adds item 3.
2. Platform must either allow or explicitly reject modification of a confirmed reservation.

**Expected:** Platform rejects the in-flight modification (reservation is locked once confirmed) or routes the new item to a new reservation. No silent addition to the QR code's payload that would cause a mismatch at pickup.

---

## TC-17 — Japanese customer, PayPay payment, Tokyo store, kana characters in customer name

**Category:** edge | **Priority:** 2 | **In-scope surface:** Web reservation + POS confirmation

**Preconditions:** Customer `C-JP-002` with name `田中 花子` (Tanaka Hanako in kana); PayPay payment method; Tokyo store `S-JP-TO-01`.

**Steps:**
1. Reserve item via PayPay; QR code generated for customer name containing kana characters.
2. POS scans QR; customer name renders correctly on POS receipt.

**Expected:** Reservation succeeds. POS receipt renders the kana name without garbling or replacement characters. Loyalty points credited to the Japanese loyalty account.

---

## TC-18 — Pickup window expires before customer arrives (48h elapsed)

**Category:** negative | **Priority:** 1 | **In-scope surface:** POS confirmation + inventory release

**Preconditions:** Customer `C-IT-005` reserved an item 49 hours ago. The 48h pickup window has elapsed.

**Steps:**
1. Customer attempts to scan QR code at POS.
2. Platform checks pickup window: expired.

**Expected:** POS rejects the QR code with "Pickup window expired" message. Item has been returned to available inventory (the platform released it automatically at the 48h mark). Refund is automatically initiated. No item handed over.

---

## Summary counts

| Category | Count |
|---|---|
| Critical-path | 5 (TC-01, 02, 04, 07, 08) |
| Edge | 7 (TC-03, 05, 06, 12, 15, 16, 17) |
| Negative | 5 (TC-07, 08, 09, 10, 11) |
| Regression | 1 (TC-18) |
| **Total** | **18** |

Negatives: TC-07 (SCA failure), TC-08 (phantom-stock), TC-09 (identity collision), TC-10 (SAP timeout), TC-11 (wrong customer ID) = **5 explicit negatives** ✅

Priority 1: TC-01, TC-02, TC-04, TC-07, TC-08, TC-09, TC-10, TC-18 = 8 cases blocking Italy pilot
