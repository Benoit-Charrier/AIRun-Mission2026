---
case: Meridian Retail Group — Click & Collect
feature: Click & Collect cross-channel flow (Phase 1 omnichannel platform)
date: 2026-07-01
author: Benoit Charrier
---

# Test Plan — Click & Collect Cross-Channel Flow

## In scope

- **Web cart and reservation step** — customer adds item on meridian.com, selects Click & Collect, chooses a store and pickup window, and receives a QR code reservation confirmation.
- **Identity stitch at first in-store pickup** — the customer's existing in-store loyalty account merges with their web account at the moment the POS scans the QR code for the first time.
- **SAP-sourced inventory check at pickup confirmation** — when the POS scans the QR code, the platform reads current SAP inventory to confirm the item is still available; the result gates the handover.
- **Cross-region loyalty-points credit** — points are credited to the customer's loyalty account within 30 seconds of pickup confirmation, visible in the app and at the in-store POS.
- **POS pickup confirmation flow** — the POS terminal accepts the QR code scan, validates the order against SAP, triggers the handover, and prints the receipt.

## Out of scope

- **SAP ECC inventory ground-truth correctness** — owned by Finance, covered by their own audit controls; this plan tests only that the platform reads SAP correctly and applies a defined freshness budget, not that SAP's ledger is accurate.
- **Legacy Shopify storefronts** — being strangled away in Phase 1; their behaviour is not part of the new platform's acceptance criteria.
- **Phase 2 cross-channel inventory reservation patterns** — not yet in scope for Phase 1 delivery.
- **Cross-region multi-currency settlement** — handled by the payment provider (Stripe) outside the Meridian application boundary.

## Top 3 risks

**Risk 1 — Phantom-stock cancellation at pickup (SAP inventory race)**
*Failure:* SAP inventory sync lag exceeds the freshness budget between reservation time and pickup confirmation, so the POS confirms a pickup for an item already reserved or sold elsewhere.
*User impact:* Customer arrives at the store, QR scan fails, leaves without the item. No refund is automatically initiated.
*Business impact:* Directly increases the documented 7% phantom-stock cancellation baseline; David Park (Head of Retail Ops) has flagged this as the store team's worst-case scenario. Each cancellation costs a customer journey and opens a refund ticket.

**Risk 2 — Identity-merge collision creating cross-customer loyalty contamination**
*Failure:* Two customers share a loyalty number, or the identity stitch resolves to the wrong account when a web customer picks up in-store for the first time.
*User impact:* Customer's loyalty balance is credited to the wrong account, or their purchase history is merged with a stranger's.
*Business impact:* GDPR Article 5(1)(f) exposure (integrity and confidentiality principle); Asha Sundaram's (DPO) escalation path. One confirmed cross-account leak in an EU market would require notification to the supervisory authority within 72 hours.

**Risk 3 — PSD2 SCA failure cancelling reservation instead of retrying**
*Failure:* EU payment authentication challenge fails or times out during the reservation step, and the platform cancels the reservation immediately rather than holding it for a retry window.
*User impact:* EU customer's Click & Collect order is cancelled without a clear retry path; they must restart the entire reservation flow.
*Business impact:* Elevated drop-off in EU pilot markets (Italy, Germany, Nordics); Marco Rossi (Regional GM, Italy) has flagged SCA friction as a risk to the Italy pilot timeline.

## Entry criteria

1. Phase 1 build (identity service, cart API, checkout service, inventory service) deployed and healthy in the QA region.
2. SAP ECC sandbox seeded with realistic inventory deltas for the test stores (Milano, Berlin, London, Tokyo).
3. Identity-provider stub configured to support both clean-account and merged-account scenarios from `02-test-data.json`.

## Exit criteria

1. Pass rate ≥ 95% on all Priority-1 (critical-path) test cases.
2. Zero phantom-stock cancellations observed on the Priority-1 SAP-inventory-check test cases.
3. Named sign-off from David Park (Head of Retail Ops) and Sarah Chen (Head of CX) confirming the defect log and the improvement backlog are acceptable for Phase 1 rollout to the Italy pilot.
