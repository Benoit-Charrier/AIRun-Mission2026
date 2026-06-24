---
kata_id: 1.W.4
consumes_from: 1.W.3, 1.W.2
case: A (Meridian Retail Group)
industry: fashion & lifestyle retail
region: Italy
date: 2026-06-23
---

# Ten AI Use Cases — Generated & Scored

**Context from K1.W.1–K1.W.3**
Italy click & collect segment, €280–350M revenue, 180 stores. Primary pain: 7% click & collect cancellations = €8.4–10.5M revenue leak due to SAP-to-platform inventory sync gap. Secondary pain: regulatory compliance (GDPR/PSD2/VAT) is a blocking constraint, not a customer-facing pain driver.

---

## 10 Candidate AI Use Cases (Across Pain Points)

### Pain Point 1: Inventory Sync & Real-Time Visibility (Primary)

**UC1.A (Classical ML):** Real-time SAP-to-platform inventory sync with anomaly detection
- Continuously sync SAP ERP inventory to checkout platform every 5–10 minutes (vs. current 4-hour batch).
- Use classical ML (Isolation Forest) to flag anomalies: sudden stock drops that don't match sales transactions → alert operations to investigate phantom stock.
- Outcome: Reduce failed pickups due to inventory lag from 7% → <2%.

**UC1.B (Generative AI):** Demand forecasting + inventory pre-positioning for click & collect hotspots
- Train generative model (e.g., Claude API fine-tuned on MRG sales + seasonality) to predict click & collect demand per store location (Milan, Rome, Naples) 48–72 hours ahead.
- Pre-position stock from regional warehouse to high-demand stores before peak times (weekends, paydays, seasonal events).
- Outcome: Reduce out-of-stock pickups by anticipating demand spikes; increase pickup conversion.

**UC1.C (Agentic):** Autonomous inventory orchestration agent
- Build an agentic system that monitors real-time inventory, customer orders, and store capacity constraints.
- Agent automatically decides: fulfill this order from which store? (minimize distance, maximize pickup SLA compliance, balance store stock).
- Agent re-routes orders if a store runs out of stock post-reservation (proactive notification + alternative location).
- Outcome: Eliminate phantom stock by actively managing inventory allocation as orders flow in.

---

### Pain Point 2: Regulatory Compliance (Secondary)

**UC2.A (Classical ML):** Real-time VAT calculation engine with compliance auditing
- Build VAT calculation logic that triggers on order-pickup location mismatch (e.g., order from DE, pickup in IT).
- Implement classical rules engine + audit log; tag every transaction with VAT jurisdiction + applied rate + reason.
- Classical ML flags inconsistencies that violate EU VAT rules in real time.
- Outcome: Eliminate VAT non-compliance fines (20% of tax per transaction); achieve Garante + EU compliance audit readiness.

**UC2.B (Generative AI):** GDPR compliance co-pilot for location-data handling
- Generative AI tool (Claude API) that reviews location-based inventory queries (e.g., "show stock near you") and suggests GDPR-compliant alternatives (pseudonymization, consent wording, data minimization).
- Auto-generates privacy-impact documentation for Italian Garante submission.
- Outcome: Reduce compliance risk; accelerate Garante approval for location-based features.

---

### Supporting Use Cases (Enhance Primary Pain Solution)

**UC3.A (Classical ML + Generative):** Personalized pickup-experience ranking
- Classical ML scores each order's likely pickup experience risk (based on store capacity, time-to-pickup, customer sentiment history).
- High-risk orders are flagged; generative model suggests proactive interventions: offer alternate location, extend time window, offer shipping alternative with discount.
- Outcome: Reduce repeat failed-pickup customers; improve NPS on click & collect.

**UC3.B (Agentic):** Multi-channel inventory visibility agent
- Agent monitors real-time inventory across all 180 MRG Italy stores + regional warehouse.
- Customer-facing: agent powers "find it in nearby stores" feature on checkout (tested < 2 seconds latency).
- Outcome: Increase click & collect adoption by removing search friction; customer confidence in inventory accuracy.

---

### Adjacent Use Cases (Supportive to Main Pain)

**UC4.A (Generative AI):** Predictive low-stock alerting for category managers
- Generative model trained on historical stock-outs + seasonal patterns predicts which SKUs will go OOS in next 7 days.
- Category managers receive AI-generated brief: "These 42 SKUs will likely stock out this week; recommend reorder these quantities from supplier X by date Y."
- Outcome: Reduce stock-outs by improving demand planning; lower carrying costs via better inventory targeting.

**UC4.B (Classical ML):** Store fulfillment capacity optimization
- Classical ML model predicts store pickup capacity constraints (e.g., Milan store can handle max 80 pickups/day before staff gets overwhelmed).
- Real-time: fulfillment orchestration respects store capacity; doesn't oversell pickup slots.
- Outcome: Eliminate pickup delays due to store overwhelm; maintain <2% failed-pickup rate even during peak.

---

## Idea Deduplication Pass

**Deduplication analysis:**

- **UC1.A vs UC1.C (inventory sync):** UC1.A is data-pipeline-centric (sync + anomaly detection); UC1.C is agentic orchestration (allocation decisions). Not duplicates; complementary. Keep both.
- **UC1.B vs UC4.A (demand forecasting):** UC1.B is *click & collect location-specific* demand; UC4.A is *category SKU-specific* demand. Different scopes. Not duplicates; both useful. Keep both.
- **UC2.A vs UC2.B (compliance):** UC2.A is VAT/rules engine; UC2.B is GDPR/location data. Different regulatory domains. Keep both.
- **UC3.A vs UC3.B (experience):** UC3.A is reactive (flag at-risk orders); UC3.B is proactive (find-it-nearby). Different use cases. Keep both.
- **UC1.C vs UC3.B (agents):** UC1.C is inventory allocation; UC3.B is customer visibility. Different scopes. Not duplicates. Keep both.

**Deduplication verdict:** No true duplicates found. All 10 use cases are distinct in scope or mechanism. Proceed to scoring.

---

## Scoring Table: Value (1–5) × Feasibility (1–5)

| UC ID | Use Case | Value | Rationale (Value) | Feasibility | Rationale (Feasibility) | Score |
|---|---|---|---|---|---|---|
| **UC1.A** | Real-time inventory sync + anomaly detection | 5 | Directly addresses primary pain (7% cancellations → <2%); revenue impact €8.4–10.5M/year if solved | 4 | SAP API access exists; classical ML is proven; 6-month implementation | **20** |
| **UC1.B** | Demand forecasting + pre-positioning | 4 | Reduces OOS by anticipating demand; 15–20% incremental pickup conversion if successful | 3 | Requires 18+ months of sales data per store; generative model needs tuning; complex supply-chain coordination | **12** |
| **UC1.C** | Autonomous inventory orchestration agent | 5 | Solves allocation at order time; prevents phantom stock entirely; enables dynamic routing | 2 | Requires real-time event streaming (Kafka), agent framework (Claude API + tools), complex state management; 9–12 month dev | **10** |
| **UC2.A** | Real-time VAT calculation + compliance auditing | 3 | Eliminates compliance risk; not a revenue driver, but fines avoided = €11–14M potential upside | 4 | Rules engine well-established; classical ML audit is straightforward; 4–5 month implementation | **12** |
| **UC2.B** | GDPR compliance co-pilot (location-data) | 2 | Reduces risk but is a one-time enabler (not recurring revenue impact); documentation tool rather than revenue-generation tool | 4 | Generative AI (Claude API) is plug-and-play; template generation is straightforward; 2–3 months | **8** |
| **UC3.A** | Personalized pickup-experience ranking | 3 | Improves NPS + retention on click & collect; secondary to core inventory fix but valuable for moat | 3 | Requires ML pipeline for risk scoring; generative suggestions require training data; 6–8 months | **9** |
| **UC3.B** | Multi-channel inventory visibility agent (find-it-nearby) | 4 | Increases click & collect adoption; competitive parity with Zalando; UX-heavy but high leverage | 3 | Requires real-time inventory API + agent integration; latency <2s is challenging; 8–10 months | **12** |
| **UC4.A** | Predictive low-stock alerting | 2 | Improves demand planning; nice-to-have but not binding constraint (won't solve 7% cancellation directly) | 4 | Generative model on historical data is straightforward; integration is light; 3–4 months | **8** |
| **UC4.B** | Store fulfillment capacity optimization | 2 | Prevents overwhelm-driven delays but is secondary pain (primary is inventory accuracy, not store capacity) | 4 | Classical ML model on store operations data; straightforward; 3–4 months | **8** |
| — | — | — | — | — | — | — |
| **Top 3 by score:** | | | | | | **UC1.A (20), UC1.B (12), UC2.A (12), UC3.B (12)** |

---

## Top 3 Selection & Commodity Check

Ranked by value × feasibility score, top 3:

### **#1: UC1.A — Real-time Inventory Sync + Anomaly Detection (Score: 20)**

**Commodity check:** 
- Is this already a vendor product? Yes, partially. SAP real-time sync solutions exist (SAP Commerce Cloud + extensions, Kinaxis Rapid Response, Blue Yonder).
- Switching cost if vendor solution: High (requires SAP implementation partner, 6–9 month implementation, €2–4M cost).
- MRG's competitive advantage if built in-house: Meridian gets a proprietary anomaly-detection layer tailored to their SKU mix + store network. Vendors sell generic sync; Meridian can detect phantom stock patterns that are specific to Italian click & collect behavior.
- **Verdict: NOT commodity.** While the sync pipeline is standard, the anomaly detection + proactive alerting tailored to click & collect is novel. **Keep UC1.A as #1.**

---

### **#2: UC1.B — Demand Forecasting + Pre-positioning (Score: 12)**

**Commodity check:**
- Is this already a vendor product? Yes. Demand-sensing platforms exist (SAP Integrated Business Planning, Kinaxis, Blue Yonder, Shopify Flow).
- Switching cost if vendor solution: Medium (€500K–1.5M for demand-planning platform + training; 6–8 month implementation).
- MRG's competitive advantage if built in-house: Click & collect specific demand forecasting (not just inventory); real-time pre-positioning logic is highly tailored to MRG's store network topology. Most vendors focus on aggregate demand; Meridian's 180-store network + customer-location data is proprietary intel.
- **Verdict: BORDERLINE commodity.** High risk that a vendor platform (e.g., Blue Yonder's Demand Sensing) offers 80% of this. But MRG's location-specific pre-positioning is defensible.
- **Recommendation: Rank #2, but explore vendor alternatives first. If Blue Yonder or Kinaxis can do 70%+ of the job, use vendor + customize. Only build in-house if vendor gap is >30%.**

---

### **3rd Runner-Up: UC3.B — Multi-Channel Inventory Visibility Agent (Score: 12)**

Tied with UC1.B on score, but higher novelty + strategic value than commodity alternatives.

**Commodity check:**
- Is this already a vendor product? Partially. Commerce search engines (Algolia, Elasticsearch, Solr) do real-time inventory search. Agent-based orchestration is less commodity.
- Switching cost if vendor solution: Medium (€400K–1.2M for search platform + agent framework integration; 5–7 months).
- MRG's competitive advantage if built in-house: Agent-based "find it for me" UX is novel (most competitors offer search, not orchestration). Real-time agent that re-routes orders if OOS is rare in market.
- **Verdict: NOVEL + DEFENSIBLE.** Search is commodity; agent orchestration is not. This is where AI-native differentiation lives.
- **Recommendation: Promote UC3.B to #2; keep UC1.B as #3.**

---

## Final Top 3 Use Cases (Re-Ranked Post-Commodity Check)

| Rank | Use Case | Score | Commodity? | Rationale |
|---|---|---|---|---|
| **1** | **UC1.A: Real-time inventory sync + anomaly detection** | 20 | No (proprietary anomaly layer) | Directly solves primary pain (7% → <2% cancellations); highest revenue impact; novel anomaly detection tailored to click & collect |
| **2** | **UC3.B: Multi-channel inventory visibility agent** | 12 | No (agentic orchestration is novel) | Increases click & collect adoption; competitive parity with Zalando; agent-based "find it" is defensible vs. commodity search |
| **3** | **UC1.B: Demand forecasting + pre-positioning** | 12 | BORDERLINE (explore vendor alternatives first) | Location-specific demand + pre-positioning is valuable; but demand-sensing vendors offer 70%+ capability. **Action: RFP Kinaxis/Blue Yonder; build in-house only if vendor gap >30%.** |

---

**Next step:** Proceed to Kata K1.W.5 (build one-page opportunity canvas) using UC1.A as the primary use case, with UC3.B and UC1.B as secondary optionality.
