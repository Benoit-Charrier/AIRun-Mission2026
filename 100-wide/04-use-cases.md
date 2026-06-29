# 04-use-cases

Date: 2026-06-24
Case: Case A - Meridian Retail

## Input discipline

Hard inputs used from `03-research-audit.md`
- EU ecommerce participation is high and growing.
- Italy still has online conversion headroom.
- Delivery speed and poor website usability are common frictions.
- Inditex is investing in integrated store + online execution.
- Amazon is raising the bar on pickup convenience.
- DSA obligations create operational transparency / traceability requirements.

Soft hypotheses used only where noted
- Competitive pressure is converging around convenience infrastructure.
- Compliance-by-design is becoming a product requirement.
- Desk teardown findings are directional, not decision-grade.

## Candidate use cases (10)

| ID | Use case | Type | Pain mapped | Value (1-5) | Value rationale | Feasibility (1-5) | Feasibility rationale | Score |
|---|---|---|---|---:|---|---:|---|---:|
| UC-01 | AI product-content localization for Italy | Generative | Conversion friction / regional nuance | 2 | Helps merchandising and localization quality, but not tied to Meridian's most acute audited pain. | 5 | Straightforward with existing content workflows and low integration burden. | 10 |
| UC-02 | Click-and-collect failure risk scoring with promise adjustment | Classical ML | Inventory trust gap / delivery reliability | 5 | Directly attacks the audited 7% cancellation pain and customer trust loss. | 4 | Needs SAP + store/platform inventory signals, but fits current platform modernization. | 20 |
| UC-03 | Cross-channel identity and loyalty account resolution copilot | Agentic + ML | Fragmented journey economics | 5 | Supports one-customer identity, loyalty consolidation, and repeat-purchase economics. | 3 | Requires data matching, review workflow, and governance, but aligns to Phase 1 identity scope. | 15 |
| UC-04 | Support copilot for pickup, delivery, and checkout exceptions | Generative | Delivery / usability friction | 3 | Reduces service handling time and improves recovery when journeys fail. | 5 | Low-medium integration burden if grounded on order and policy data. | 15 |
| UC-05 | Checkout friction miner from sessions, tickets, and complaints | Generative analytics | Website usability friction | 4 | Surfaces root causes of conversion loss across web/mobile/store journeys. | 4 | Feasible with analytics, support text, and product telemetry already typical in ecommerce stacks. | 16 |
| UC-06 | Local payment and PSD2 recovery orchestration engine | Agentic + rules | Checkout friction / payment failure / regional compliance | 5 | Impacts checkout conversion in Italy/EU and reduces abandonment tied to payment friction. | 3 | Payment flows are sensitive and regulated, but orchestration can be layered without full platform replacement. | 15 |
| UC-07 | Store associate copilot for loyalty lookup and pickup exception handling | Generative | Cross-channel continuity / in-store recovery | 4 | Helps stores keep selling when identity or pickup journeys break. | 4 | Feasible if connected to customer, order, and policy data with constrained actions. | 16 |
| UC-08 | Inventory anomaly detection between SAP and channel stock feeds | Classical ML | Inventory trust gap | 5 | Directly targets phantom stock and reduces downstream pickup cancellations. | 3 | Integration complexity is real because SAP remains source of truth and regions vary. | 15 |
| UC-09 | DSA/GDPR release-evidence copilot for digital commerce changes | Agentic | Compliance and trust | 3 | Cuts governance drag and reduces release risk, but value is more defensive than growth-led. | 4 | Documentation and workflow automation are feasible with existing release artifacts. | 12 |
| UC-10 | AI campaign brief generator grounded on stock, loyalty, and region signals | Generative | Marketing efficiency / journey continuity | 2 | Useful, but downstream of more urgent operational and identity issues. | 4 | Technically easy if fed approved data, but impact depends on upstream fixes. | 8 |

## Dedup pass

- UC-02 and UC-08 overlap on inventory trust, but they are not duplicates.
- UC-02 is customer-facing promise control; UC-08 is back-office anomaly detection.
- UC-04 and UC-07 partially overlap on exception handling.
- UC-04 is customer-support-oriented; UC-07 is store-associate-oriented.
- UC-05 and UC-06 partially overlap on checkout friction.
- UC-05 diagnoses friction; UC-06 intervenes in one high-value failure domain (payments + PSD2 recovery).

## Top 3 by value x feasibility

1. **UC-02 — Click-and-collect failure risk scoring with promise adjustment**
- Why it made top 3: highest direct linkage to audited Meridian pain and strong operational feasibility.
- Value: 5
- Feasibility: 4
- Score: 20

2. **UC-03 — Cross-channel identity and loyalty account resolution copilot**
- Why it made top 3: supports the board-level target of one identity / one loyalty program and improves retention economics.
- Value: 5
- Feasibility: 3
- Score: 15

3. **UC-06 — Local payment and PSD2 recovery orchestration engine**
- Why it made top 3: checkout conversion is a board-visible growth lever, and local payment/regulatory nuance is explicit in the case.
- Value: 5
- Feasibility: 3
- Score: 15

## Commodity check on top 3

### UC-02
- Commodity verdict: **No**
- Reason: generic inventory tools exist, but AI-driven pickup-risk scoring tied to Meridian's SAP-grounded stock, regional rollout logic, and promise control is not an off-the-shelf commodity.

### UC-03
- Commodity verdict: **No**
- Reason: CIAM and loyalty platforms exist, but cross-region identity-resolution copilot with merge-confidence workflow across 22 country stacks is not a standard plug-and-play feature.

### UC-06
- Commodity verdict: **Borderline, but keep**
- Reason: payment routing is partly commoditized by PSPs, but Meridian's need is broader: local-method orchestration plus PSD2/SCA recovery and region-specific checkout optimization on top of a strangler migration.
- Swap decision: **Do not swap**. It remains differentiated enough in this case context.

## Short rationale on the 7 not selected

- UC-01: easy but too generic and too far from Meridian's hardest audited pain.
- UC-04: useful operating tool, but more reactive than top-3 choices.
- UC-05: strong diagnostic value, but not as directly monetizable as UC-02 or UC-06.
- UC-07: valuable for stores, but depends on upstream identity/order quality improvements.
- UC-08: strong alternative and likely wave-2 companion to UC-02; narrowly missed top 3 because integration burden is higher.
- UC-09: important, but defensive and less board-exciting than growth + trust uses.
- UC-10: clearly commodity and downstream of upstream data/journey issues.

## Recommended shortlist to carry forward

- UC-02
- UC-03
- UC-06
