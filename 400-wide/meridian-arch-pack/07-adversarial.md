---
kata: 4.W.8
artefact: adversarial-review
date: 2026-06-26
note: Fresh-session pre-mortem — reviewed as if the reviewer had not built the design
---

# Meridian Phase 1 — Adversarial Pre-Mortem

*Reviewed against the full arch pack (00–06) by a fresh session with no prior context. Instruction given: "You did not design this. Your job is to break it."*

---

## Stressor A — 10× Black Friday Peak Load

NFR-02 target: 8000 RPS sustained, 12000 RPS burst. 10× = 80000–120000 RPS.

### A1 — Apollo Gateway becomes a single-threaded choke point

**Container/relationship:** Apollo Gateway (Node.js / Apollo Server).
**First symptom a user would see:** Checkout and add-to-cart buttons stop responding; browser shows "connection timed out" after ~30s with no error message (HTTP timeout, not a 5xx).
**Why:** Apollo Server's default event loop is single-threaded; at 10× load without horizontal scaling, the Gateway's Node.js process saturates before any downstream service. The L2 diagram shows no explicit horizontal scale policy for the Gateway.

**Decision:** Patch.
- **Patch applied:** Add a horizontal pod autoscaler (HPA) specification to the Gateway deployment: scale from 3 → 20 replicas at 70% CPU. Add a Bulkhead-level timeout to the Gateway so that a slow Cart Service response does not hold Gateway worker threads — timeout: 1000ms per upstream call, fail-fast with HTTP 503.
- **Diagram impact:** `02-containers.mmd` note added: "Apollo GraphQL Gateway — HPA 3–20 replicas; 1000ms upstream timeout."
- **ADR impact:** None — HPA is an operational concern, not a new architectural decision.

### A2 — Kafka consumer lag outpaces the inventory cache warm-up

**Container/relationship:** Order Event Bus (Kafka) → Inventory Read Cache (Redis) consumer.
**First symptom a user would see:** "In stock" labels that are 2–4 hours stale during peak; click-and-collect phantom-stock rate spikes back toward 7% on peak days.
**Why:** At 10× load, SAP ECC publishes stock-change events at its normal batch rate — the Kafka topic message volume doesn't increase with web traffic. But the inventory cache consumer is a single consumer-group with default partition count (12). If 10× traffic increases cache-miss rate (more items, more stores), and the consumer falls behind, Redis serves increasingly stale projections.

**Decision:** Patch.
- **Patch applied:** Add a consumer-lag SLO to NFR-03: alert when Kafka consumer group lag > 10,000 messages (approximately 15 min of batch events at peak SAP write rate). Pre-warm the inventory cache for the top 500 SKUs per store 2 hours before expected peak (cron job, fires at 8am on Black Friday).
- **NFR impact:** `06-nfrs.yaml` NFR-03: add `consumer_lag_alert_threshold: 10000`.

### A3 — Redis ElastiCache becomes an unavailable dependency with no fallback

**Container/relationship:** Apollo Gateway → Inventory Cache (Redis).
**First symptom a user would see:** Every product page shows "Can't confirm right now — call the store" (the `cannot_confirm` fallback), degrading the availability assistant to fully useless during peak.
**Why:** The design relies on Redis as the *only* fast read path for inventory. Redis ElastiCache Multi-AZ failover takes 30–60 seconds during a primary node failure — during that window, all cache reads fail and every request falls through to the SAP inline fallback, which at 10× load would saturate SAP instantly.

**Decision:** Accepted risk (partial).
- The `cannot_confirm` fallback and degradation path are already designed (Module 300 AI-AC2). The user-visible impact is a degraded experience, not a checkout failure — shoppers can still reserve; they just see the fallback label.
- **Accepted by:** Tomás Reyes (architecture risk), Sarah Chen (CX impact of fallback label during peak).
- **Condition:** Redis ElastiCache Multi-AZ is confirmed enabled before Phase 1 launch. The 30–60s failover window is acceptable; a full Redis unavailability beyond 5 minutes during Black Friday would require a manual incident response to degrade gracefully.

---

## Stressor B — Hostile Inputs at EU Checkout

### B1 — Malformed PSD2 SCA callback replayed by an attacker

**Container/relationship:** Stripe webhook → Checkout Service.
**First symptom a user would see:** An attacker replays a valid `payment_intent.succeeded` webhook for a previous order; a second fulfilled order is dispatched for the same cart without payment.
**Why:** The Checkout Service must validate Stripe webhook signatures (`Stripe-Signature` header) and implement idempotency on order-creation. The integration contract in `03-integrations.md` covers the `cartMerge` call but does not explicitly cover webhook idempotency on the Checkout Service's inbound path.

**Decision:** Patch.
- **Patch applied:** Add to `03-integrations.md`: "Checkout Service MUST validate `Stripe-Signature` header on every inbound webhook (Stripe HMAC-SHA256 signature with a 5-minute timestamp tolerance). Checkout Service MUST store `payment_intent_id` with `UNIQUE` constraint in PostgreSQL `orders` table; duplicate webhook delivery results in a no-op, not a second order creation."
- **ADR impact:** No new ADR; this is an implementation constraint on ADR-001's Checkout Service.

### B2 — Injection at the loyalty QR lookup (POS cart-bridge)

**Container/relationship:** POS Client → Apollo Gateway → Identity Service (loyaltyQR input).
**First symptom a user would see:** A crafted loyalty QR code containing a GraphQL injection payload loads another customer's cart at the POS, or causes the Identity Service to return a null customer with an active session.
**Why:** The `cartMerge` mutation takes a `loyaltyQR: String!` input that the Identity Service passes to Auth0 for token validation. If the Identity Service does not sanitise the QR payload before passing it to Auth0's OIDC endpoint, a crafted payload could manipulate the decoded token claims.

**Decision:** Patch.
- **Patch applied:** Add to `04-adr-003.md` Agent-Readable Summary: "The Identity Service MUST validate that the `loyaltyQR` input is a valid signed JWT before passing it to Auth0 — reject any input that does not pass `jwt.verify()` with the Auth0 public key. Do not pass raw QR string content to any downstream service."
- **NFR impact:** NFR-07 (`06-nfrs.yaml`): add `input_validation: "loyaltyQR must pass jwt.verify() before Identity Service forwards to Auth0"`.

### B3 — PCI boundary violated by a logging misconfiguration

**Container/relationship:** Checkout Service + PII scrub stage.
**First symptom a user would see:** No user-visible symptom — this is a silent compliance failure that surfaces in a QSA audit or a data breach.
**Why:** Apollo Server's default error logging includes the full GraphQL variables object on resolver errors. If a checkout mutation includes card-related metadata (even tokenised references), a resolver error during the Stripe SCA callback could log the full PaymentIntent object. This is already called out in NFR-07's anti-pattern, but the architecture pack has no explicit "PII scrub stage" container in the L2.

**Decision:** Patch.
- **Patch applied:** `02-containers.mmd` updated to add a `PII Scrub Filter` as a component of the Checkout Service (not a separate container — a middleware layer): "Checkout Service middleware strips PANs, CVVs, and raw PaymentIntent objects from all log output before forwarding to the logging pipeline." NFR-07 test approach updated: "CI PAN-pattern grep covers log output from Checkout Service resolver error fixtures."

---

## Stressor C — Partner Outage

### C1 — SAP ECC down for 2 hours during trading hours

**Container/relationship:** SAP ECC → Kafka CDC → Inventory Read Cache; also Apollo Gateway → SAP ECC (inline cache-miss fallback).
**First symptom a user would see:** After approximately 30 minutes, inventory cache entries begin to expire (Redis TTL) for slow-selling SKUs. New cache-miss fallback calls to SAP time out at 1000ms and return `cannot_confirm`. POS cart-bridge lines with cache-miss SKUs show "Check with staff." After 2 hours, high-velocity SKU cache entries also expire; most product pages show `cannot_confirm`.
**Why:** Redis TTL is set to 1800s (30 min) by convention (ADR-001). A 2-hour SAP outage exceeds the TTL for all SKUs, progressively degrading availability indicators across the platform.

**Decision:** Patch (TTL extension) + Accepted risk (degraded state).
- **Patch applied:** During a detected SAP outage (circuit breaker open on the Gateway → SAP path), the Inventory Cache consumer switches to a "stale-but-keep" mode: extends TTL of existing cache entries by 4 hours rather than letting them expire. The `cannot_confirm` state is shown only for SKUs that were never cached (new arrivals or first-request cache misses during the outage).
- **Accepted risk:** After 4 hours of SAP outage, inventory data will be too stale to serve even extended-TTL entries. The fallback state ("Can't confirm — call the store") affects the entire catalogue. Accepted by David Park (Store Ops) — stores continue to sell but associates must verify stock manually.
- **ADR impact:** ADR-001 Agent-Readable Summary updated: "On a detected SAP outage (circuit breaker open), the Inventory Cache consumer MUST extend cache entry TTL to 4 hours rather than expiring entries on their default 30-minute TTL."

### C2 — Stripe degraded (elevated error rates, not full outage)

**Container/relationship:** Checkout Service → Stripe.
**First symptom a user would see:** 5–15% of EU checkout attempts fail at the payment step with a generic "Payment failed, please try again" message. Customers retry; second attempt may also fail. Cart abandonment rate spikes.
**Why:** Stripe degradation (elevated error rates on the SCA challenge or PaymentIntent creation) does not trip the circuit breaker at low degradation levels (<20% error rate). The Checkout Service retries synchronously up to 3 times (default), holding the checkout session open for up to 3 × 1500ms = 4.5s before surfacing an error. At 10× load this compounds with Stressor A.

**Decision:** Patch + Accepted risk.
- **Patch applied:** Add Stripe-specific circuit breaker threshold to Checkout Service: trip when Stripe error rate > 10% over a 60-second window (lower than the generic 20% threshold). When tripped, surface an explicit "Payments temporarily unavailable — your cart is saved; try again in a few minutes" message (not a generic error). This preserves the cart and reduces retry churn.
- **Accepted risk:** A full Stripe outage means EU checkout is unavailable. No alternative payment path exists in Phase 1 (adding a secondary payment processor is a Phase 2 consideration). Accepted by Eva Müller (Programme Director) — Stripe SLA is 99.99%; full outage is within acceptable risk tolerance for Phase 1.

### C3 — Auth0 incident during peak trading

**Container/relationship:** Identity Service → Auth0; all authenticated surfaces.
**First symptom a user would see:** New login attempts fail immediately; existing sessions whose JWT is cached in the Identity Service's Redis session cache continue to work for up to 15 minutes. After 15 minutes, cached tokens expire and the platform becomes fully inaccessible to logged-in users.
**Why:** Auth0 outages are rare (Enterprise SLA 99.99%) but not impossible. The Identity Service Redis cache provides a 15-minute grace window (ADR-003 consequence + NFR-06), after which every authenticated request fails.

**Decision:** Accepted risk.
- The 15-minute Redis session cache is the designed mitigation. Extending it further (e.g. to 60 minutes) increases the risk of serving revoked tokens (security trade-off).
- **Accepted by:** Tomás Reyes (architecture risk) — the Auth0 Enterprise SLA makes an outage exceeding 15 minutes a statistically rare event. A second identity provider as hot standby is out of scope for Phase 1.
- **Condition for re-evaluation:** If Auth0 has ≥ 2 incidents > 15 minutes in 12 months, escalate to Tomás and Asha Sundaram for Phase 2 identity resilience review.

---

## Summary of patches applied

| Finding | Patch | File changed |
|---------|-------|-------------|
| A1 — Gateway saturation | HPA 3–20 replicas + 1000ms upstream timeout | `02-containers.mmd` (note) |
| A2 — Kafka consumer lag at peak | Consumer-lag SLO alert; Black Friday cache pre-warm cron | `06-nfrs.yaml` NFR-03 |
| B1 — Stripe webhook replay | Stripe-Signature validation + idempotency constraint | `03-integrations.md` |
| B2 — QR injection | loyaltyQR jwt.verify() before forwarding | `04-adr-003.md` Agent-Readable Summary; `06-nfrs.yaml` NFR-07 |
| B3 — PCI log misconfiguration | PII scrub middleware in Checkout Service; log grep in CI | `02-containers.mmd`; `06-nfrs.yaml` NFR-07 |
| C1 — SAP 2-hour outage | Stale-but-keep TTL extension (4h) on circuit-breaker-open | `04-adr-001.md` Agent-Readable Summary |
| C2 — Stripe degradation | Stripe-specific circuit breaker (10% error rate threshold) | `05-patterns.md` Circuit Breaker row |

## Summary of accepted risks

| Finding | Owner | Condition |
|---------|-------|-----------|
| A3 — Redis failover 30–60s window | Tomás Reyes + Sarah Chen | Redis Multi-AZ confirmed before launch |
| C1 (partial) — SAP > 4h outage = full catalogue `cannot_confirm` | David Park | Manual associate verification accepted |
| C2 — Full Stripe outage | Eva Müller | Stripe Enterprise SLA 99.99%; Phase 2 for secondary processor |
| C3 — Auth0 > 15 min incident | Tomás Reyes | Escalate to Asha Sundaram if recurs ≥ 2× in 12 months |
