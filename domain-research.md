# D0A — Domain Research: Omnichannel Retail Commerce

**Domain:** Omnichannel retail commerce
**Process area:** Unified customer identity, cart, and checkout across web, mobile, and in-store POS
**Generated:** 2026-06-16

---

## 0. Executive summary

- Omnichannel retail commerce centres on synchronising product, inventory, pricing, and customer state across channels in real time, with skilled human attention concentrated at exception resolution — cases where channel state diverges and a live customer transaction must be preserved or redirected.
- The most important constraint is PCI-DSS Level 1 for payment data, which mandates scoped, audited handling of card information at every channel touchpoint and creates a hard stop: no autonomous agent may store, log, or relay raw card data without explicit human-governed vault design.
- The highest-leverage agentic opportunity is cross-channel cart and identity reconciliation (merging anonymous and authenticated sessions), where the key unknown is whether session-merge rules are codified policy or embedded per-channel in implementation code.

---

## 0b. Table of contents

- [0. Executive summary](#0-executive-summary)
- [0b. Table of contents](#0b-table-of-contents)
- [1. Domain overview](#1-domain-overview)
  - [1a. What this domain does](#1a-what-this-domain-does)
  - [1b. Typical workflow](#1b-typical-workflow)
  - [1c. Common failure modes](#1c-common-failure-modes)
- [2. Regulatory and compliance context](#2-regulatory-and-compliance-context)
- [3. Cognitive work patterns typical to this domain](#3-cognitive-work-patterns-typical-to-this-domain)
  - [3a. Where skilled attention is typically consumed](#3a-where-skilled-attention-is-typically-consumed)
  - [3b. Lived vs. documented gaps typical to this domain](#3b-lived-vs-documented-gaps-typical-to-this-domain)
- [4. ATX dimension pre-assessment](#4-atx-dimension-pre-assessment)
- [5. Hypothesis questions for discovery](#5-hypothesis-questions-for-discovery)
- [6. Assumption log](#6-assumption-log)

---

## 1. Domain overview

### 1a. What this domain does

Omnichannel retail commerce exists to present a unified buying experience to customers regardless of the channel they use — web, mobile app, or in-store point-of-sale — while keeping inventory, pricing, promotions, and customer account state consistent across all touchpoints. The primary knowledge workers are platform engineers maintaining integration layers, identity and session architects defining merge and conflict rules, and operations analysts resolving channel-state discrepancies. Primary inputs are customer actions (account creation, session initiation, cart modification, payment initiation) and back-end events (inventory updates, price changes, promotion activations). Primary outputs are confirmed orders, session tokens, loyalty credit events, and inventory reservation confirmations. Volume is high — a mid-scale retailer processes hundreds of thousands of sessions daily, with cart and identity events in the millions per week during peak periods.

### 1b. Typical workflow

Domain-typical workflow — client deviations will surface in discovery.

1. Customer initiates session on any channel — anonymous or authenticated [execution]
2. Identity layer resolves whether an existing account exists (email, device fingerprint, loyalty ID) [judgment]
3. If anonymous cart exists, merge decision is made — keep, discard, or merge line items [judgment]
4. Cart is hydrated with real-time pricing, promotions, and inventory availability [execution]
5. Customer proceeds to checkout — address, shipping method, payment method selected [execution]
6. Payment gateway validates and authorises — PCI-DSS scoped call [verification]
7. Order confirmation triggers inventory reservation and loyalty credit calculation [execution]
8. Post-purchase state syncs back to identity profile (order history, loyalty balance) [coordination]

### 1c. Common failure modes

- **Phantom stock at checkout** — inventory shown as available when already reserved or depleted; customer completes checkout but fulfilment fails. **Data failure.**
- **Session merge conflict** — a returning customer logs in mid-session; no codified rule exists for which cart wins, leading to silent line-item loss. **Judgment failure.**
- **Cross-channel identity fragmentation** — the same customer holds accounts on web, mobile, and in-store; loyalty points are split and promotions duplicated. **Coordination failure.**
- **Payment tokenisation mismatch** — a token valid in one channel is not accepted by a different gateway instance, causing checkout abandonment. **Process failure.**
- **Promotion double-application** — regional promotion engines run independently; a customer eligible in two regions receives both discounts, creating a margin error that surfaces only in reconciliation. **Data failure.**

---

## 2. Regulatory and compliance context

| Framework / Constraint | What it governs | Agent design implication |
|---|---|---|
| PCI-DSS Level 1 | Cardholder data storage, processing, and transmission at every channel touchpoint | Agents must never log, cache, or relay raw card numbers or CVVs; all payment steps must route through a certified tokenisation vault; agent scope must be explicitly defined relative to PCI scope boundary |
| GDPR / CCPA | Personal data collection, consent, cross-border transfer, and right to erasure for EU and California customers | Identity merge actions must carry consent lineage; agents performing identity resolution must flag customers with active erasure or restriction requests before acting |
| PSD2 SCA (EU) | Strong Customer Authentication for online payments above €30 in the EU | Checkout flows for EU customers must trigger SCA challenge; agents automating checkout steps cannot bypass SCA; exemptions must be explicitly coded and audited |
| Local payment method requirements | Country-specific instruments (PayPay in Japan, Klarna in Nordics, Postepay in Italy) | Agents routing payment cannot apply a single global flow; country context must be resolved before the checkout step |
| Consumer protection / distance selling regulations | Right of withdrawal, return policy disclosure, and order confirmation requirements | Agents generating order confirmations must include jurisdiction-correct withdrawal rights text |

---

## 3. Cognitive work patterns typical to this domain

### 3a. Where skilled attention is typically consumed

> **Cognitive hotspot [CH-1]:** Session merge decision when an anonymous cart collides with an authenticated account at login
> **Cognitive type:** judgment
> **Why it resists simple automation:** Merge rules conflict with customer expectation — keeping the new cart may delete items a returning customer added weeks ago on another device; the right decision depends on recency, item type, and channel context, none of which is universally codified
> **What would make it delegatable:** A codified merge policy (explicit precedence rules by cart age, item category, and channel) with a confidence threshold below which a human review queue is triggered

> **Cognitive hotspot [CH-2]:** Inventory reservation decision during peak load when oversell risk is elevated
> **Cognitive type:** exception handling
> **Why it resists simple automation:** Inventory ground truth lags real-time by seconds to minutes in distributed systems; accepting an order on stale stock requires weighing oversell cost against abandonment cost — a tradeoff that shifts by season and SKU category
> **What would make it delegatable:** Real-time inventory sync with sub-second latency, combined with explicit oversell tolerance thresholds per product category set by merchandising

> **Cognitive hotspot [CH-3]:** Cross-channel identity resolution for customers with fragmented accounts across legacy CRM instances
> **Cognitive type:** pattern recognition
> **Why it resists simple automation:** Matching signals (email, phone, loyalty ID, device fingerprint) are often partial, stale, or contradictory; a wrong merge permanently corrupts a customer's history and is costly to unwind
> **What would make it delegatable:** A probabilistic match model with a high-confidence threshold (e.g., >0.95) for auto-merge, a mid-band queue for human review, and a low-confidence do-not-merge default

> **Cognitive hotspot [CH-4]:** Promotion eligibility resolution when regional rules conflict on the same basket
> **Cognitive type:** synthesis
> **Why it resists simple automation:** Promotion rules are created by regional marketing teams in separate systems with different data models; eligibility may depend on loyalty tier, region of purchase, channel, and basket composition simultaneously
> **What would make it delegatable:** A single promotion rules engine with a deterministic evaluation order and explicit conflict-resolution policy

### 3b. Lived vs. documented gaps typical to this domain

> **Gap [G-1]:** The SOP says cart merge follows a documented policy; in practice, developers have hard-coded channel-specific merge logic in checkout microservices and the policy document is out of date
> **Why it exists:** Cart merge logic evolved incrementally as channels were added; no centralised policy owner exists; the technical implementation drifted from the document
> **Agent design implication:** An agent trained on the documented policy will apply the wrong merge logic for a majority of real sessions; it must be trained on the actual code path, not the policy doc

> **Gap [G-2]:** The SOP says inventory availability is checked at add-to-cart and again at checkout; in practice the second check is skipped under high load to reduce latency, and oversell events are handled post-order by operations
> **Why it exists:** The second check adds 80–120ms of latency; it was removed during a peak-season performance optimisation and never restored
> **Agent design implication:** An agent enforcing the documented two-check flow will add latency that contradicts live performance requirements; the agent design must accommodate the single-check reality or negotiate an explicit performance budget

> **Gap [G-3]:** The SOP says all payment failures are routed to a standard error message; in practice, payment teams maintain a hand-maintained lookup table of gateway error codes and channel-specific recovery scripts
> **Why it exists:** Gateway error codes are not standardised across providers; the lookup table grew organically from customer service escalations
> **Agent design implication:** An agent handling payment failure recovery built only on the SOP will miss the majority of recoverable failure types; it must ingest the lookup table as a live knowledge source and flag when a code is absent

---

## 4. ATX dimension pre-assessment

| ATX Dimension | Domain-typical signal | What to probe in discovery |
|---|---|---|
| **Volume & Time** | High volume; millions of sessions per week at peak; identity resolution and cart hydration must complete in <200ms | What is the peak transaction rate? What is the current p95 latency for identity resolution and cart hydration? Where does the system degrade under load? |
| **Cognitive Nature** | Mixed — execution steps are rule-bound and high-volume; judgment steps (merge, resolution, exception) are low-volume but high-consequence | Where do exceptions land today — automated handling, queue, or direct escalation? How are merge and resolution policies currently expressed (code, doc, tribal knowledge)? |
| **Data & Systems** | Fragmented — identity data across multiple CRMs, inventory across ERP and warehouse systems, promotions across regional engines; real-time sync is partial | What is the authoritative source for inventory, identity, and promotions? What are the known sync lags? Which systems are read-only vs. writable by the platform? |
| **Risk & Compliance** | High — PCI-DSS scope touches every payment step; GDPR applies to identity and session data; SCA applies to EU checkout; oversell and identity merge errors have direct customer and financial impact | Which compliance frameworks are currently certified? What is the PCI-DSS scope boundary? Are there active compliance findings? |
| **Organisational** | Complex — multiple SI partners, regional teams with autonomy, internal product team still building capability; promotion and inventory ownership is split across functions | Who owns the promotion rules engine? Who owns the identity merge policy? What approval is required to change a checkout flow in production? |

The most constraining ATX dimension for agent design in this domain is **Data & Systems**. The fragmentation of identity, inventory, and promotion data across systems with partial, lagged synchronisation means that any agent acting on these data sources will routinely encounter stale or conflicting state. Before defining agent scope, discovery must establish which system is authoritative for each data type, what the lag profile looks like under load, and whether the agent can write to the authoritative source or only read from a downstream copy.

---

## 5. Hypothesis questions for discovery

> **HQ-1: When a customer logs in mid-session on a different device from where they built their cart, what happens to the anonymous cart — is it merged, replaced, or discarded?**
> **Hypothesis being tested:** Cart merge rules are not uniformly codified; different channel implementations handle this differently
> **If confirmed:** Agent design must use the actual per-channel implementation logic, not a central policy; a merge arbitration service is a prerequisite
> **If disconfirmed:** A single merge policy exists and is enforced; agent can consume the policy as a ruleset

> **HQ-2: What is the current p95 latency for resolving a customer identity at session start, and what happens when the identity service is slow or unavailable?**
> **Hypothesis being tested:** Identity resolution is a latency-sensitive hot path with a degraded-mode fallback that may create ghost sessions
> **If confirmed:** Agent acting on identity data must handle degraded-mode state explicitly; a resolved identity cannot be assumed
> **If disconfirmed:** Identity resolution is fast and reliable; latency is not a binding constraint for agent design

> **HQ-3: Is there a single inventory source of truth, or do different channels read inventory from different systems with different latency profiles?**
> **Hypothesis being tested:** Inventory fragmentation is a root cause of phantom-stock events; channels have different read latency from the same ERP
> **If confirmed:** Agent must resolve which inventory source is canonical per channel before making availability decisions; arbitration logic is required
> **If disconfirmed:** All channels read from one source with consistent latency; agent can trust the read

> **HQ-4: Who owns the promotion rules engine — central marketing, regional teams, or a mix — and how are conflicting promotions resolved today?**
> **Hypothesis being tested:** Promotion eligibility logic is distributed and conflict resolution is manual or implicit
> **If confirmed:** Agent cannot evaluate eligibility without accessing a fragmented ruleset; a promotion arbitration layer is a prerequisite
> **If disconfirmed:** A single rules engine exists with deterministic evaluation order; agent can call the engine directly

> **HQ-5: What is the current process when a customer reports a duplicate loyalty account — who resolves it, how long does it take, and what data is used to decide which account is canonical?**
> **Hypothesis being tested:** Identity merge for existing fragmented accounts is a manual, low-throughput process handled by customer service
> **If confirmed:** A high-confidence automated merge path would unlock significant capacity; discovery must surface what signals customer service actually uses
> **If disconfirmed:** An automated merge process already exists; agent opportunity is elsewhere

> **HQ-6: Does the current checkout flow for EU customers implement PSD2 SCA, and is the SCA challenge handled by the gateway or embedded in platform logic?**
> **Hypothesis being tested:** SCA implementation is partially embedded in checkout logic the agent would touch; mishandling it would create a compliance breach
> **If confirmed:** Agent scope must explicitly exclude or include the SCA step with certified handling; compliance review required before deployment
> **If disconfirmed:** SCA is fully handled by the gateway; agent checkout steps are outside SCA scope

> **HQ-7: When inventory is found to be oversold after an order is confirmed, what is the recovery workflow and who owns it?**
> **Hypothesis being tested:** Oversell recovery is a manual, reactive process with high customer service cost — a candidate for agent-assisted triage
> **If confirmed:** Agent-assisted oversell triage is a viable scope; recovery scripts may already exist in informal form
> **If disconfirmed:** Oversell events are rare and handled by automation; the opportunity is smaller than hypothesised

> **HQ-8: Are there any checkout flows where a human must review or approve a transaction before confirmation — high-value orders, B2B accounts, flagged fraud scores?**
> **Hypothesis being tested:** Human-in-the-loop checkpoints exist in checkout for certain transaction types; agent must not bypass them
> **If confirmed:** Agent checkout scope must be bounded below the review threshold; the review trigger rules must be codified
> **If disconfirmed:** All transactions are processed without human review; agent can act on the full checkout flow

> **HQ-9: How are country-specific payment methods configured — central registry or distributed across regional deployments?**
> **Hypothesis being tested:** Local payment method support is implemented inconsistently, with regional teams maintaining their own configurations
> **If confirmed:** Agent routing payments must resolve country context before selecting a method; a central registry is a prerequisite or the agent must read from distributed configs
> **If disconfirmed:** A central payment method registry exists and is maintained; agent can resolve routing from one source

> **HQ-10: What is the current time-to-detect for a channel-state divergence — e.g., web showing a price that differs from in-store — and who is responsible for resolving it?**
> **Hypothesis being tested:** Channel-state divergence detection is reactive (reported by customers or store staff) rather than proactive; resolution ownership is unclear
> **If confirmed:** A proactive monitoring agent would fill a real gap; discovery must determine acceptable detection latency and notification ownership
> **If disconfirmed:** Automated monitoring exists and divergences are detected within minutes; agent opportunity is in resolution, not detection

> **HQ-11: When a GDPR erasure request is processed, which systems are in scope and is the process manual or automated?**
> **Hypothesis being tested:** GDPR erasure spans identity, order history, session data, and loyalty records across multiple systems; the process is partially manual and error-prone
> **If confirmed:** An agent coordinating erasure across systems would reduce compliance risk; discovery must surface whether a canonical erasure checklist exists
> **If disconfirmed:** Erasure is automated and covers all systems; agent opportunity is elsewhere

---

## 6. Assumption log

> **Assumption [A-1]:** A mid-scale omnichannel retailer processes hundreds of thousands of sessions per day and millions of cart/identity events per week during peak periods
> **Why it matters:** Volume drives the latency and throughput requirements for any identity or cart agent; if volume is an order of magnitude lower, batch processing becomes viable
> **If wrong:** Agent design shifts from real-time stream processing to near-real-time or batch; architecture choices change significantly
> **Confidence:** medium
> **How to validate:** Request peak and average daily session counts and cart event volumes from platform telemetry

> **Assumption [A-2]:** Cart merge logic is not uniformly codified — it exists in per-channel implementation code rather than a central policy document
> **Why it matters:** If merge logic is in code, the agent must be built from code inspection, not documentation; discovery and build effort is higher
> **If wrong:** A central policy exists and is enforced consistently; agent can consume it as a ruleset with lower discovery cost
> **Confidence:** high (common in multi-channel retail built incrementally)
> **How to validate:** Ask engineering: "Where is the cart merge decision made — is there a single service or is it in each channel's checkout code?"

> **Assumption [A-3]:** Inventory sync from ERP to the commerce platform has a lag of seconds to minutes under normal load, increasing under peak conditions
> **Why it matters:** If lag is material, the agent must treat inventory reads as approximate and design for oversell tolerance; if negligible, the agent can trust the read
> **If wrong:** Real-time sync with sub-second lag exists; inventory reads are reliable; agent design is simpler
> **Confidence:** high (ERP sync latency is a known challenge in headless commerce)
> **How to validate:** Request current p95 inventory sync latency and known max lag during peak load

> **Assumption [A-4]:** Identity resolution completes in under 200ms under normal load and degrades above that threshold during peak
> **Why it matters:** Identity resolution is on the critical path for every session start; if the agent touches this path it must add negligible latency or be excluded from the hot path
> **If wrong:** Identity resolution is already slow (>500ms), or is fast enough that latency is not a binding constraint
> **Confidence:** medium
> **How to validate:** Request p50, p95, and p99 identity resolution latency from platform monitoring

> **Assumption [A-5]:** Promotion rule management is distributed across regional marketing teams with no single rules engine enforcing conflict resolution
> **Why it matters:** If true, any agent evaluating promotion eligibility must integrate with all regional engines — a prerequisite dependency, not an agent feature
> **If wrong:** A centralised promotion engine exists; agent can call one API; discovery and build effort is lower
> **Confidence:** medium (common in retailers grown through acquisition)
> **How to validate:** Ask: "If a customer in Italy uses a promo code created by the Nordic team, which system evaluates eligibility and what happens when they conflict?"
