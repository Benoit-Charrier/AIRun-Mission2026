---
kata: 4.W.1
artefact: discovery-context
date: 2026-06-26
case: Reference Case A — Meridian Retail Group
---

# Meridian Phase 1 — Architecture Context

## Business layer

- **Revenue at stake:** 31% of Meridian's total revenue is digital; 22 regional stacks fragmenting that base → customer churn in Italy (phantom-stock cancellations), lost cross-regional upsell.
- **Programme:** $42M / 18 months to merge 22 regional stacks into one headless platform. Phase 1 = unified identity + cart + checkout. Quarterly stage gates; budget does not float.
- **Success measure:** Black Friday 2025 runs on the new platform with zero EU region outage (prior year: 40-minute EU outage). Phantom-stock cancellation rate drops from ~7% to below 2%.
- **Stakeholders with architectural pull:**
  - Asha Sundaram (CTO) — mandated strangler-fig cutover; "no Big Bang, no new monolith."
  - Tomás Reyes (Lead Architect) — owns C4 pack, ADRs, pattern choices.
  - Eva Müller (Programme Director) — owns stage gates and the 18-month delivery window.
  - David Park (Head of Store Ops) — owns the POS cart-bridge requirement; stores cannot be blocked by platform downtime.
  - Sarah Chen (Head of CX) — owns the click-and-collect promise; trust surfaces.

## Product layer

- **Customer-facing surfaces:** Web storefront (Next.js), mobile app (React Native iOS + Android), in-store POS client (used by store associates).
- **Channels and user moments in Phase 1:**
  - Online browse → add to cart → checkout (web and mobile)
  - Store Associate scans customer loyalty QR code → retrieves online cart → rings up in-store (POS cart-bridge)
  - Click-and-collect reservation → pickup confirmation with stock feedback
- **Out of scope for Phase 1:** loyalty programme rebuild, personalised recommendations, Phase 2 CRM consolidation, Phase 3 legacy-stack retirement.

## Engineering layer

- **Target stack:** commercetools (headless commerce), Apollo GraphQL Gateway, AWS EKS (microservices), Kafka eventing, Auth0 (identity), Next.js (web), React Native (mobile), PostgreSQL on RDS (order/cart persistence), Redis (inventory read cache), Stripe (payments), SendGrid (email).
- **Legacy systems that must coexist:** SAP ECC (inventory ground truth; batch stock feed, not real-time query API); 6 regional CRMs (customer data per region; async sync, not replaced in Phase 1).
- **Cutover pattern:** Strangler-fig mandated by Asha Sundaram. Apollo Gateway routes `/v1/*` to the legacy regional stack and `/v2/*` to the new platform; regional migrations are incremental.
- **Team constraint:** Junior internal MRG product team. Operational complexity (service meshes, event-sourcing, multi-region active-active) is a risk, not a feature.

## Regulatory layer

- **GDPR / CCPA:** Customer PII may not leave the EU/CA data region; the platform must support right-to-erasure and consent management before any EU or California launch.
- **PCI-DSS Level 1:** Stripe tokenisation keeps PANs out of Meridian's trust boundary; all payment flows must pass annual QSA audit. Cardholder data MUST NOT be stored or logged by any Meridian service.
- **PSD2 SCA:** Every EU card payment requires strong customer authentication. SCA round-trip adds 500–1500ms to EU checkout; checkout latency budget must account for this — a < 100ms checkout target is physically impossible on EU paths.
- **Local payment methods:** Italy (Postepay), Japan (PayPay), UK (Klarna). Each has its own auth flow; a failure of one MUST NOT cascade to others (Bulkhead pattern required).

---

## Five implicit assumptions the brief never states

1. **SAP ECC serves real-time inventory queries**
   *Brief hint:* "SAP ECC is the inventory source of truth for all 22 regions."
   *Assumption:* The platform can query SAP synchronously per request.
   *What breaks if wrong:* SAP ECC inventory updates are batch-processed (typically 15–30 min lag); direct synchronous RFC calls for per-page stock checks at e-commerce scale will saturate SAP's RFC gateway and cause cascading slowdowns across every region sharing the ERP.

2. **Regional stacks can be migrated in a defined, stable order**
   *Brief hint:* "Strangler-fig cutover, 22 regional stacks."
   *Assumption:* Each regional stack's integration surface is known and can be strangled without surprising the others.
   *What breaks if wrong:* Some regional stacks share data models or ERP segments with others; migrating Italy's checkout without auditing the shared SAP company codes could corrupt inventory attribution for France.

3. **Auth0 is purely an external dependency with stable SLA**
   *Brief hint:* "Auth0 identity" in the tech stack list.
   *Assumption:* Auth0 uptime and latency are acceptable for in-store POS flows where a 2-second auth delay blocks the queue.
   *What breaks if wrong:* Auth0 Starter tier has no SLA; Auth0 Enterprise SLA is 99.99% but requires negotiation; an Auth0 incident takes down every Meridian surface simultaneously unless the Identity Service caches tokens locally.

4. **Kafka is already provisioned and operated by the team**
   *Brief hint:* "Kafka eventing" in the stack.
   *Assumption:* A Kafka cluster exists, is maintained, and the junior MRG team can operate it.
   *What breaks if wrong:* Kafka requires tuned consumer-group lag monitoring, partition rebalancing, and schema registry management; a junior team with no prior Kafka experience is likely to under-provision it for Black Friday burst, causing consumer lag and stale inventory projections at peak.

5. **Stripe's PSD2 SCA implementation covers all EU markets**
   *Brief hint:* "Stripe (payments)" + "PSD2 SCA for EU payments."
   *Assumption:* Stripe's SCA flow works for all EU card schemes and local payment methods Meridian supports.
   *What breaks if wrong:* Postepay (Italy) and Carte Bancaire (France) have issuer-specific SCA quirks; Stripe's generic 3DS2 flow has non-trivial decline rates on these schemes; Meridian may need a Stripe Radar rule or payment method–specific fallback to avoid SCA-caused basket abandonment.
