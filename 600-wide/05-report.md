---
case: Meridian Retail Group — Click & Collect
consumes_from: 6.W.1–6.W.5 (00-test-plan.md, 01-test-cases.md, 02-test-data.json, 03-defects.md, 04-rca.md)
date: 2026-07-01
author: Benoit Charrier
report_for: Eva Müller (VP Digital), David Park (Head of Retail Ops), Sarah Chen (Head of CX), Marco Rossi (Regional GM Italy)
---

# Test Report — Click & Collect Phase 1

**Feature:** Click & Collect cross-channel flow — Meridian omnichannel platform Phase 1
**Test window:** 2026-07-01
**Execution method:** Path C (manual observation with stub harness); no Playwright MCP browser agent available

---

## 1. Coverage

**Tested:** Web cart and reservation step; identity stitch at first in-store pickup; SAP-sourced inventory check at pickup confirmation; cross-region loyalty-points credit; POS pickup confirmation flow — across 18 test cases against 15 test records spanning Italy, Germany, Japan, UK, US, and UAE markets. Test cases covered critical-path flows (5), edge inputs (7), explicit negatives (5), and one regression (expiry window).

**Not tested:** SAP ECC inventory ground-truth correctness (owned by Finance, covered by their own controls); legacy Shopify storefronts (out of scope per plan); cross-region multi-currency settlement (Stripe-owned, out of Meridian's application boundary); Phase 2 cross-channel inventory reservation patterns (not in Phase 1 scope); cross-region multi-currency settlement; regions not yet onboarded to Phase 1 (e.g., South-East Asia except Japan).

---

## 2. Pass rate and defect density

**Overall: 14 passed / 18 cases | 4 defects logged**

| Surface | Cases run | Passed | Defects | Defect density |
|---|---|---|---|---|
| Web reservation + payment | 4 | 3 | 1 (DEF-003) | 1 / 4 |
| Identity stitch | 2 | 1 | 1 (DEF-002) | 1 / 2 |
| SAP inventory check at pickup | 4 | 2 | 1 (DEF-001) | 1 / 4 |
| Cross-region loyalty credit | 2 | 1 | 1 (DEF-004) | 1 / 2 |
| POS confirmation (incl. QR, window expiry, wrong ID) | 6 | 6 | 0 | 0 / 6 |

**Pass rate by priority:**
- Priority 1 (Italy pilot blockers): 5 passed / 8 cases = **62.5%** — below the 95% exit criterion
- Priority 2: 5 passed / 6 cases = 83%
- Priority 3 / 4: 4 passed / 4 cases = 100%

**The Priority-1 pass rate does not meet the 95% exit criterion.** Three P1 defects (DEF-001, DEF-002, DEF-003) must be resolved before the exit criterion can be assessed again.

---

## 3. Top 2 problematic areas

**Area 1 — SAP inventory check at pickup confirmation**
DEF-001 (P1/S1): The POS confirmation component has no guard blocking handover when `available_stock == 0`. The SAP response is received but not evaluated before the confirmation screen renders. This directly expresses the documented 7% phantom-stock cancellation rate. Root cause and guard test documented in `04-rca.md`. Fix: held-stock token at reservation + synchronous 30s-ceiling SAP read + guard in the confirmation component.

**Area 2 — Identity stitch and EU SCA retry**
DEF-002 (P1/S2): Case-sensitive email comparison in the identity stitch silently creates a duplicate account when the web-account email and the legacy loyalty-card email differ in casing. No error surfaced; loyalty history is fragmented. DEF-003 (P1/S2): SCA failure immediately cancels the Click & Collect reservation instead of holding it for a 10-minute retry window, causing EU customers to lose their store slot on any transient authentication failure.

---

## 4. Improvement backlog (5 items, ranked by impact)

1. **Add a held-stock token at reservation and enforce a synchronous 30s SAP freshness ceiling at pickup confirmation** — closes the phantom-stock cancellation race (DEF-001, the documented 7% baseline); the guard condition blocking `renderConfirmationScreen()` when `available_stock == 0` is the immediate fix — **Engineering (Tomás Reyes' team) — P1.**

2. **Replace case-sensitive email comparison in the identity-stitch service with a case-insensitive match** — closes DEF-002; prevents silent duplicate-account creation on first in-store pickup for any customer whose legacy loyalty card email uses mixed case (common in legacy POS data entry) — **Engineering (Tomás Reyes' team) + DPO (Asha Sundaram review) — P1.**

3. **Add a 10-minute SCA retry hold on Click & Collect reservation cancellation** — closes DEF-003; reservation status transitions to `pending_sca_retry` on SCA failure, not `cancelled`; reservation is released to inventory only after the 10-minute window expires without a successful retry — reduces EU pilot drop-off and addresses Marco Rossi's SCA friction risk — **Engineering (Tomás Reyes' team) + CX (Sarah Chen) — P1.**

4. **Fix cross-region loyalty-point routing to use the customer's home region, not the pickup store's region** — closes DEF-004; loyalty points from a cross-region pickup must be credited to the customer's home-region loyalty ledger — required before Phase 1b cross-region rollout; does not block Italy domestic pilot — **Engineering + Loyalty Platform team — P2.**

5. **Wire a daily dashboard report of phantom-stock cancellation rate and identity-stitch success/failure counts to the Phase 1 rollout dashboard** — gives David Park (Head of Retail Ops) and Sarah Chen (Head of CX) the operational signal they need before approving Phase 1 expansion from Italy to the next two markets; without this signal, each rollout decision is based on incident reports rather than trends — **Data + Retail Ops — P3.**

---

## Rollout recommendation

**Do not ship Click & Collect to the Italy pilot until DEF-001, DEF-002, and DEF-003 are resolved.**

DEF-001 would reproduce the exact phantom-stock customer journey that the Phase 1 build was designed to eliminate, at a measurable rate, from day one of the pilot. DEF-002 and DEF-003 would affect every EU pilot customer who experiences an SCA failure or whose loyalty email has mixed casing — both are near-silent failures that accumulate data quality and customer trust debt without triggering a visible alert.

Once all three P1 defects are resolved, re-run the 8 Priority-1 test cases. If pass rate reaches ≥ 95%, the exit criterion is met. Named sign-off from David Park and Sarah Chen is required before rollout, per the entry/exit criteria in `00-test-plan.md`.
