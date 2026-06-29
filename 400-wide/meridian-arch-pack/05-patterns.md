---
kata: 4.W.6
artefact: placed-pattern-catalog
date: 2026-06-26
---

# Meridian Phase 1 — Placed Pattern Catalog

| Pattern | Where on L2 (`02-containers.mmd`) | Meridian constraint it addresses | Trade-off |
|---------|-----------------------------------|----------------------------------|-----------|
| **Strangler Fig** | Apollo GraphQL Gateway — routes `/v1/*` to the Italy regional legacy stack (first region to migrate), `/v2/*` to the new commercetools platform | CTO Asha Sundaram mandate: no Big Bang; 22 stacks must coexist through Phase 3 | The Gateway becomes a deployment dependency for every region migration; it cannot be deleted until the last region (estimated Phase 3, ~month 36). Gateway routing rules accumulate per region. |
| **Outbox** | Cart Service + Checkout Service → `outbox` table in PostgreSQL → Debezium CDC → Kafka Order Event Bus | Cross-service event consistency without distributed transactions (ADR-002); prevents dual-write split-brain that would cause phantom-stock cache entries | Adds Debezium CDC connector to the operational surface; PostgreSQL replication slot must be monitored — if Debezium falls behind, WAL retention grows and risks disk fill on the RDS instance. |
| **Bulkhead** | Checkout Service — separate thread pools + connection pools per payment method (Stripe/Postepay, Stripe/PayPay, Stripe/Klarna); each payment method runs in an isolated pod group | Local payment methods (Postepay Italy, PayPay Japan, Klarna UK/DE) must not share fate; a PayPay issuer outage in Japan must not affect Postepay checkout in Italy | More pods to provision and maintain; resource utilisation is lower than a unified checkout pool; health-check and circuit-breaker config must be duplicated per payment-method bulkhead. |
| **Circuit Breaker** | Apollo Gateway → SAP ECC (inline cache-miss fallback); Checkout Service → Stripe | SAP ECC and Stripe are outside Meridian's control; their degradation must not cascade to store POS or web checkout — Black Friday 2024 EU outage was partly a cascading failure from an external dependency | Circuit breaker timeout thresholds must be tuned to SAP's actual p99 (not p95) response time; misconfigured thresholds trip prematurely on Black Friday burst or fail to trip on genuine SAP degradation. |
| **Backend for Frontend (BFF)** | Three BFF layers fronting Apollo Gateway: Web BFF (Next.js server), Mobile BFF (React Native), POS BFF (cart-bridge + loyalty QR validation) | Three surfaces have diverging query shapes and auth flows — especially POS, which needs cart-merge and loyalty QR validation that web/mobile do not | Three codebases to keep aligned as the GraphQL schema evolves; schema changes that affect POS must be validated against all three BFF surfaces before deploy. |
| **CQRS (implicit)** | Inventory Read Cache (Redis) as the read side; SAP ECC + PostgreSQL as the write side for inventory state | Read traffic (product pages, POS cart-bridge) far exceeds write traffic (actual stock changes); separating the read model allows Redis to serve reads at < 5ms without contending with SAP's batch write cycles | This is not a full CQRS implementation — there is no explicit command model. It is read/write segregation via the Kafka-hydrated cache. Full CQRS with event sourcing would add operational cost the junior MRG team cannot absorb in Phase 1. |

---

## Patterns reviewed and rejected for Phase 1

| Pattern | Reason rejected |
|---------|----------------|
| **Event Sourcing** | High operational cost (event log compaction, replay latency, schema versioning) disproportionate to Phase 1 scope; the junior MRG team does not have the event-sourcing debugging skills. The Kafka + Outbox pattern delivers the consistency benefits without the full event-sourcing surface. Revisit in Phase 3 for the loyalty programme. |
| **Service Mesh (Istio/Linkerd)** | Deployment-level concern, not a design pattern. Adds JVM sidecar overhead and operational complexity (mTLS cert rotation, traffic policies) that the junior team cannot maintain in Phase 1. Circuit Breaker at the application level (above) covers the resilience requirement with lower overhead. |
| **Saga (choreography)** | See ADR-002: Saga requires each service to implement compensating logic for distributed transactions; Outbox + Kafka achieves event reliability without per-service compensation logic. Saga would be appropriate if Phase 2 introduces long-running multi-service workflows (e.g. returns processing), but that is out of scope for Phase 1. |

---

## Open question flagged

**Pipe & Filter** was evaluated for the SAP CDC → Kafka → Redis projection pipeline. The current design is effectively a two-step filter (CDC produces raw SAP stock events → Kafka consumer transforms and writes to Redis). This is an implicit Pipe & Filter. It is not named or placed explicitly because the pipeline has no branching enrichment logic in Phase 1. If Phase 2 adds inventory segmentation (e.g. reserve stock for loyalty customers), the pipeline should be formalised as a named Pipe & Filter chain with an explicit contract between stages. **Open question for Phase 2 architecture review.**
