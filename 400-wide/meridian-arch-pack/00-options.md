---
kata: 4.W.2
artefact: options
decision: How does the Meridian platform read inventory and bridge the online/in-store cart while SAP ECC stays the source of truth?
date: 2026-06-26
---

# Inventory / Cart-Bridge Options — Meridian Phase 1

**Decision question:** How does the Meridian platform read inventory and bridge the online/in-store cart while SAP ECC stays the source of truth?

---

## Option A — Synchronous reads direct from SAP ECC (boring / safe option)

**Core idea:**
- Every availability check on the product page and in the POS cart-bridge is a live RFC call to SAP ECC.
- No caching layer; no event bus. The platform calls SAP and returns whatever SAP returns.
- Cart merge at POS = Identity lookup (Auth0) + cart fetch (PostgreSQL) + per-item SAP RFC call.

**Optimises for:** Data freshness — stock count always reflects the live ERP ledger.

**Sacrifices:** Latency (SAP ECC RFC round-trips are 200–600ms each; a 4-item cart = up to 2.4s just for stock checks) and SAP stability (retail peak load queries will exceed SAP ECC RFC gateway capacity — the Black Friday EU outage was partly caused by this pattern in a legacy stack).

**Meridian constraint that pressures this hardest:** *Black Friday peak load.* At ~8000 RPS peak across the platform, synchronous SAP reads will saturate the ERP RFC gateway and cause cascading failures — the exact failure mode Meridian has already experienced.

---

## Option B — Event-driven inventory read model hydrated via Kafka (chosen direction)

**Core idea:**
- SAP ECC publishes stock-change events to Kafka via a CDC (Change Data Capture) connector.
- A Kafka consumer projects those events into a Redis read cache (Inventory Read Cache).
- The platform reads stock from Redis (1–5ms). SAP ECC is only queried inline on a Redis cache miss, with a degraded-availability fallback when SAP is unreachable.
- Cart merge at POS = Identity lookup + cart fetch + per-item Redis read; SAP only touched on cache miss.

**Optimises for:** Read latency and SAP isolation — the ERP is decoupled from the hot read path, so SAP maintenance windows do not cascade to store POS or web.

**Sacrifices:** Data freshness (Redis projection is 15–30 min stale at worst; phantom-stock risk on slow SAP batch segments) and operational complexity (Kafka, CDC connector, consumer-group lag monitoring, schema registry — high burden for the junior MRG team).

**Meridian constraint that pressures this hardest:** *SAP batch-update reality.* SAP ECC stock updates are not real-time; even with CDC, a batch-committed stock update arrives 15–30 min after a sale. The confidence labels and disclosure copy from Module 300 (AI availability assistant) exist to manage this gap.

---

## Option C — Buy a cross-channel inventory service (e.g. OneStock / Fluent Commerce)

**Core idea:**
- Adopt a SaaS distributed order management / inventory visibility platform as the read layer.
- SAP ECC syncs to the external service; Meridian queries the service's API for stock and cart-merge.
- The vendor handles CDC, Kafka, caching, and freshness guarantees under their SLA.

**Optimises for:** Build velocity — removes Kafka / CDC / cache operational burden from the junior team; the vendor's SLA owns freshness.

**Sacrifices:** Vendor lock-in (a third major external dependency alongside Stripe and Auth0), vendor SLA risk at Black Friday scale, and additional cost (~$400K–$800K/yr licensing on top of the $42M programme budget). Also delays Phase 1 delivery: procurement and integration of a new SaaS vendor takes 2–4 months the 18-month window cannot absorb.

**Meridian constraint that pressures this hardest:** *18-month/$42M budget and junior internal team.* Paradoxically the solution that removes team complexity adds procurement complexity and budget risk at a stage-gate programme where the first gate is 6 months out.

---

## Decision deferred to K 4.W.5

All three options remain on the table. No choice is made in this artefact — the trade-off scoring happens in K 4.W.5 against the full constraint matrix.

| Option | Optimises | Sacrifices | Hardest constraint |
|--------|-----------|------------|-------------------|
| A — Sync SAP reads | Freshness | Latency, ERP stability | Black Friday peak load |
| B — Event-driven cache (Kafka + Redis) | Latency, SAP isolation | Freshness lag, Kafka ops complexity | SAP batch-update reality |
| C — Buy inventory SaaS | Build velocity | Vendor lock-in, cost, procurement time | 18-month budget / stage gates |
