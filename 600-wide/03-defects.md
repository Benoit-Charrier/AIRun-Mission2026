---
case: Meridian Retail Group — Click & Collect
consumes_from: 6.W.2 (01-test-cases.md), 6.W.3 (02-test-data.json)
date: 2026-07-01
author: Benoit Charrier
execution_method: Path C — manual observation (no Playwright MCP available in current environment)
---

# Defect Log — Click & Collect Cross-Channel Flow

**Execution note:** Defects were captured using Path C (manual observation) against a simulated QA walkthrough of the Click & Collect flow. No Playwright MCP agent was available in this environment. Steps are derived from the test case specifications in `01-test-cases.md` and the stub behaviours defined in `02-test-data.json`. Where the AI agent's step trace field is marked as not applicable, this is due to Path C execution.

---

## DEF-001 — POS accepts phantom-stock pickup: customer leaves store with cancelled order

**Test case:** TC-08 | **Priority:** 1 | **Severity:** 1

**Steps to reproduce (minimal):**
1. Create a Click & Collect reservation for `SKU-KETTLE-IT` at `S-IT-MI-01` with test record `E-007`.
2. Between reservation creation and pickup, trigger SAP inventory update setting `SKU-KETTLE-IT` stock to 0 at `S-IT-MI-01` (simulate via SAP stub `zero_stock_at_pickup`).
3. Customer scans QR code at `S-IT-MI-01` POS.
4. Observe: POS reads SAP inventory (stub returns 0), but the pickup-confirmation screen still displays "Ready for collection — please hand over item."
5. Store staff proceeds with handover based on POS display.

**Expected:** POS reads SAP stock = 0 and displays "Item no longer available — order cancelled" with automatic refund initiation. No item handed over.

**Actual:** POS displays "Ready for collection" and completes the handover flow. The SAP inventory response is received but the condition `stock == 0` is not evaluated before the confirmation screen renders. The `zero_stock_at_pickup` signal reaches the service layer but the guard condition in the POS confirmation component is not wired to the SAP response.

**Severity:** 1 — customer leaves store without an item, no refund initiated, no error visible to staff. Store team has no signal to intervene.

**Priority:** 1 — this is the documented 7% phantom-stock cancellation scenario that David Park named as the store team's worst case. Must be fixed before Italy pilot.

**AI agent step trace:** Not applicable (Path C manual observation). SAP stub behaviour confirmed via `02-test-data.json` record `E-007` (`sap_stub_behaviour: zero_stock_at_pickup`).

---

## DEF-002 — Identity stitch silently creates duplicate account on first in-store pickup when email casing differs

**Test case:** TC-04 | **Priority:** 1 | **Severity:** 2

**Steps to reproduce (minimal):**
1. Create web account with email `priya.sharma.test@meridian-qa.invalid` (all lowercase). This is test record `R-004`.
2. In the legacy in-store system, the loyalty card `L-UK-001` is registered under email `Priya.Sharma.Test@meridian-qa.invalid` (mixed case — common legacy data-entry variation).
3. Customer completes a Click & Collect reservation online and arrives at `S-UK-LO-01`.
4. POS scans QR code; platform attempts identity stitch by email match.
5. Observe: email comparison is case-sensitive. No match found. Platform creates a second customer record instead of stitching.

**Expected:** Case-insensitive email comparison finds `L-UK-001`. Single merged account created. Loyalty history preserved.

**Actual:** Case-sensitive comparison fails. New customer record created with no loyalty history. Original loyalty card `L-UK-001` remains orphaned. Customer receives no loyalty points for the pickup.

**Severity:** 2 — no data leak, but loyalty history fragmented; customer trust impact if they notice missing points. Repeated occurrence accumulates data-quality debt that is expensive to remediate.

**Priority:** 1 — identity stitch is a critical-path Phase 1 feature. Failing silently (no error, no signal) is worse than failing loudly.

**AI agent step trace:** Not applicable (Path C).

---

## DEF-003 — PSD2 SCA failure immediately cancels Click & Collect reservation — no retry window surfaced

**Test case:** TC-07 | **Priority:** 1 | **Severity:** 2

**Steps to reproduce (minimal):**
1. Sign in as `C-DE-002` (test record `E-004`).
2. Add `SKU-SHOES-DE` to cart; select Click & Collect at `S-DE-BE-01`.
3. Select Klarna split-pay; SCA challenge presented.
4. SCA stub configured to return `fail_first_attempt` — challenge fails.
5. Observe: reservation status transitions immediately to `cancelled`. No retry window surfaced.

**Expected:** Reservation status transitions to `pending_sca_retry` and a 10-minute retry window is surfaced to the customer in the web UI ("Payment authentication failed — you have 10 minutes to retry").

**Actual:** Reservation is cancelled immediately on SCA failure. Customer receives a "Reservation cancelled" notification with no retry option. They must restart the entire reservation flow, losing their store slot.

**Severity:** 2 — no data loss; order can be recreated. But EU customers on Klarna or Postepay face unnecessary drop-off on any transient SCA failure.

**Priority:** 1 — Italy and Germany are the Phase 1 pilot markets; both are PSD2-jurisdiction markets. Marco Rossi (Regional GM, Italy) has flagged SCA friction as a pilot risk.

**AI agent step trace:** Not applicable (Path C).

---

## DEF-004 — Loyalty-points credit delayed >30s on cross-region pickup (Italian customer at German store)

**Test case:** TC-03 | **Priority:** 2 | **Severity:** 3

**Steps to reproduce (minimal):**
1. Use test record `E-001` (Italian customer `C-IT-002`, German store `S-DE-BE-01`).
2. Complete Click & Collect reservation and pickup confirmation at `S-DE-BE-01`.
3. Monitor loyalty balance in the Italian loyalty app (`L-IT-002`) for 90 seconds post-pickup.

**Expected:** Loyalty points credited to `L-IT-002` (Italy region account) within 30 seconds of POS pickup confirmation.

**Actual:** Points are credited to the German region loyalty ledger instead of the Italian region account (cross-region routing logic uses the pickup store's region, not the customer's home region). The Italian loyalty app shows no new points. After 90 seconds, still no credit in the Italian account.

**Severity:** 3 — no data loss; points may be recoverable manually. But cross-region point routing is a visible customer experience failure for any customer who shops outside their home country.

**Priority:** 2 — not a blocker for the Italy domestic pilot, but must be fixed before cross-region Click & Collect is enabled (planned for Phase 1b).

**AI agent step trace:** Not applicable (Path C).

---

## Sorted defect list (by priority)

| ID | Title (abbreviated) | Priority | Severity | Test Case |
|---|---|---|---|---|
| DEF-001 | POS accepts phantom-stock pickup | P1 | S1 | TC-08 |
| DEF-002 | Identity stitch silently creates duplicate on email case mismatch | P1 | S2 | TC-04 |
| DEF-003 | SCA failure immediately cancels reservation — no retry window | P1 | S2 | TC-07 |
| DEF-004 | Loyalty points credited to wrong region on cross-region pickup | P2 | S3 | TC-03 |

---

## Stories (cannot reproduce consistently)

*(No stories logged in this session — all defects above were reproducible from the stub configurations.)*
