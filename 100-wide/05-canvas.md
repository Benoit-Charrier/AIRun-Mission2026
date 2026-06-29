# 05-canvas

Date: 2026-06-24
Case: Case A - Meridian Retail
Selected use case: UC-02 — Click-and-collect failure risk scoring with promise adjustment

## Problem

Meridian is losing customer trust and avoidable revenue because about 7% of click-and-collect orders are canceled at pickup due to inventory mismatch, while EU customer expectations for reliable ecommerce fulfillment keep rising and competitors are improving pickup convenience.

## Users

Primary user segment
- Omnichannel customers in Italy placing click-and-collect orders across home goods, electronics, and fashion categories.

Operational user segments
- Store associates handling pickup exceptions at collection time.
- Regional ecommerce/product operations teams setting pickup promise rules.
- Inventory and fulfillment analysts monitoring SAP-to-channel stock quality.

## Value

Reduce click-and-collect cancellation rate from about 7% to 4% or lower in the Italy pilot market within 2 quarters by predicting high-risk orders before promise confirmation and adjusting the pickup promise, store recommendation, or exception handling path.

## Assumptions

1. At least 60% of click-and-collect cancellations are predictable before order confirmation using already-available signals from SAP inventory, store stock feeds, order history, and pickup location data.
2. Showing a safer pickup promise or alternate store option for high-risk orders will reduce click-and-collect cancellations by at least 30% relative to the current baseline without reducing checkout conversion by more than 3%.
3. At least 80% of Italy click-and-collect orders have sufficient data quality and latency to score risk in near real time before the customer completes checkout.

## Solution

Add a risk-scoring service into the click-and-collect checkout flow that evaluates each order against inventory-confidence signals before the pickup promise is shown. When risk exceeds threshold, the experience shifts from a default pickup promise to one of three guarded paths: adjusted pickup time, alternate nearby store recommendation, or explicit availability warning with fallback delivery/pickup options. The service is paired with an operations view for monitoring false positives, false negatives, and store-level anomaly clusters so Meridian can tune rules while preserving SAP as inventory ground truth.

## Critique and rewrites

Weak cell 1 identified: Value was too vague in early draft.
- Rewrite made: added baseline, target, pilot geography, and time horizon.

Weak cell 2 identified: Assumptions were initially directional rather than falsifiable.
- Rewrite made: all 3 assumptions now include numeric thresholds.

Weak cell 3 identified: Solution risked becoming a technical spec.
- Rewrite made: kept behavior-level description focused on customer promise control and operating feedback loop.
