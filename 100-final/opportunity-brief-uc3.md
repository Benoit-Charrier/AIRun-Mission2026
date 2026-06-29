# Opportunity Brief - UC3

Date: 2026-06-24
Case: Meridian Retail (Case A)
Prepared by: consulting-sme skill invocation (by-hand run)

## 1) Opportunity definition

MRG should prioritize UC-03 (cross-channel identity and loyalty account resolution copilot) as a Phase 1 enabling capability to support one-customer-identity outcomes during platform consolidation.

## 2) Business problem

MRG currently operates fragmented customer identities and loyalty accounts across regions/channels. This creates split balances, weak campaign targeting, avoidable support friction, and slower migration execution because teams cannot trust a unified customer view.

## 3) Why now

- Ecommerce penetration is high and customer expectations for reliable, coherent journeys are rising.
- Italy still shows conversion headroom, increasing value of better identity and loyalty continuity.
- Competitors are improving integrated digital/store convenience, increasing pressure on fragmented operators.
- Regulatory pressure favors stronger traceability and governance in digital commerce operations.

## 4) Evidence base used

Primary inputs:
- artefacts/100-wide/00-playground.md
- artefacts/100-wide/01-context-brief.md
- artefacts/100-wide/03-research-audit.md
- artefacts/100-wide/04-use-cases.md
- artefacts/100-wide/05-canvas-uc3.md
- artefacts/100-wide/06-roi-uc3.md
- artefacts/100-wide/08-pre-mortem-uc3.md

Evidence quality note:
- Carry-forward respected from audit: sourced claims treated as hard inputs; unverified items retained only as hypotheses.

## 5) Use-case shortlist context

From scored shortlist:
- UC-02 score 20
- UC-03 score 15
- UC-06 score 15

Why UC-03 is selected for this brief:
- Directly aligned with Phase 1 identity consolidation needs.
- Foundational for loyalty continuity and downstream retention economics.
- Strong strategic leverage despite medium implementation complexity.

## 6) Solution shape (UC-03)

Deploy a confidence-based identity-resolution copilot:
- Auto-merge high-confidence duplicate profiles under policy thresholds.
- Route medium-confidence profiles to operations review.
- Hold low-confidence or policy-conflict profiles for manual adjudication.
- Maintain full audit trail and rollback support for contested merges.
- Apply explicit loyalty reconciliation rules (points, tier precedence, expiry) by region.

## 7) Value hypothesis

Target outcomes in first two migration waves (Italy + one EU market):
- >=40% duplicate-profile reduction in active loyalty members.
- >=95% merge precision on correctly unified profiles.
- >=25% reduction in identity-related support tickets.

## 8) ROI hypothesis (three scenarios)

All monetary assumptions are currently tagged unverified and require benchmark replacement before executive commitment.

| Metric | Pessimistic | Base | Optimistic |
|---|---:|---:|---:|
| One-time costs (EUR M) | 4.10 | 3.00 | 2.00 |
| Annual run costs (EUR M) | 2.30 | 1.70 | 1.10 |
| Annual value (EUR M) | 4.10 | 6.75 | 10.10 |
| Annual net benefit (EUR M) | 1.80 | 5.05 | 9.00 |
| Payback (months) | 27.3 | 7.1 | 2.7 |

Sensitivity highlights (base case):
- Largest upside driver: loyalty revenue-contribution uplift.
- Largest execution-risk driver: manual review operations cost.

## 9) Six-gate risk read

| Gate | Current read | Rationale | Required mitigation |
|---|---|---|---|
| Value | Amber-Green | Strong strategic fit and base-case economics, but benchmark quality is not yet decision-grade. | Replace unverified assumptions with internal finance/ops baselines. |
| Usability | Amber | Customer-facing outcomes are strong but merge errors can damage trust quickly. | Strict confidence thresholds and rollback-ready support playbooks. |
| Feasibility | Amber | Data matching and workflow build are feasible but integration complexity is non-trivial. | Phase rollout with queue/SLA controls and escalation paths. |
| Viability | Amber-Green | Base payback is favorable; pessimistic case is long. | Gate expansion by measurable pilot KPIs before scaling. |
| Responsible AI | Amber | Identity resolution has fairness and error-harm implications. | Bias/error monitoring, human review for ambiguous matches, auditable decisions. |
| Model and Ops Risk | Amber | Review bottlenecks and throughput variability can break timeline/value assumptions. | Capacity model, queue depth guardrails, and weekly threshold tuning. |

Most likely kill gate if unmanaged:
- Model and Ops Risk (exception queue overload and SLA failure).

## 10) Recommendation and escalations

Recommendation:
- Proceed with controlled pilot for UC-03 in Italy + one EU market with hard gates.

Escalate to human owners before commitment:
- Final problem-priority confirmation versus UC-02/UC-06 trade-offs.
- Ethical boundary confirmation for identity merge policy.
- Pilot go/no-go and expansion go/no-go decisions.
- Stakeholder commitments (budget, timeline, external promises).
- Final value framing for executive communication.

## 11) Pilot go/no-go gates

Pilot must meet all three to scale:
- Duplicate reduction >=35% in pilot scope.
- Review SLA attainment >=95% with queue depth under 1 week.
- Cost per merged identity within agreed baseline band (+/-10%).

## 12) Invocation record

Concrete invocation
- Input focus: artefacts/100-wide/05-canvas-uc3.md + artefacts/100-wide/06-roi-uc3.md + artefacts/100-wide/08-pre-mortem-uc3.md
- Output produced: artefacts/100-final/opportunity-brief-uc3.md
- Constraint behavior: no autonomous go/no-go or stakeholder commitment decisions made.
