# 05-canvas-uc3

Date: 2026-06-24
Case: Case A - Meridian Retail
Selected use case: UC-03 - Cross-channel identity and loyalty account resolution copilot

## Problem

Meridian cannot deliver one-customer-identity and one-loyalty-program outcomes because customers currently exist as duplicate profiles across regions and channels, creating fragmented loyalty balances, weaker campaign targeting, and avoidable service friction during platform consolidation.

## Users

Primary user segments
- Existing Meridian customers with multiple IDs and loyalty accounts across regions/channels.
- New customers entering the unified platform during migration waves.

Operational user segments
- Identity operations analysts reviewing uncertain match and merge candidates.
- Loyalty operations specialists reconciling points, tiers, and expiry conflicts.
- Regional product/data stewards approving policy exceptions by market.
- Customer support teams handling post-merge disputes and corrections.

## Value

Within 2 migration waves in Italy and one additional EU market, reduce duplicate-customer rate in active loyalty members by at least 40%, increase correctly unified profiles to 95% precision, and cut identity-related support tickets by at least 25% while preserving customer trust and compliance.

## Assumptions

1. At least 70% of duplicate profiles can be resolved with high confidence using existing signals (email, phone, device, address, order history, loyalty behavior) without manual intervention.
2. Manual review capacity can process the remaining low-confidence 30% within a 72-hour SLA during migration windows without creating rollout bottlenecks.
3. Unified profile migration can achieve at least 99.5% accuracy for loyalty-balance and tier transfer on in-scope accounts, with all exceptions traceable and reversible.

## Solution

Deploy an identity-resolution copilot that scores potential profile matches and proposes merge actions with evidence and confidence levels. High-confidence cases are auto-merged under policy thresholds; medium-confidence cases are routed to operations review with guided decision steps; low-confidence or policy-conflict cases are held for manual adjudication. Every merge decision writes an auditable trail (why merged, by whom, what changed), supports rollback for contested cases, and applies loyalty-reconciliation rules for points, tier precedence, and expiry handling per region.

## Critique and rewrites

Weak cell 1 identified: Value was initially broad and not auditable.
- Rewrite made: added numeric targets for duplicate reduction, precision, and support-ticket impact across defined rollout waves.

Weak cell 2 identified: Assumptions initially described capability, not testability.
- Rewrite made: added explicit thresholds for auto-resolution rate, manual SLA capacity, and loyalty transfer accuracy.

Weak cell 3 identified: Solution risked becoming a platform migration spec.
- Rewrite made: kept behavior-level flow (score, route, decide, audit, rollback) and left implementation detail out.
