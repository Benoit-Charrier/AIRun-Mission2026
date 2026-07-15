---
kata: K 10.D.1
artefact: 1000-deep/00-project-context.md
engagement: ERP-modernization — EU industrial-machinery manufacturer
date: 2026-07-08
status: complete
---

# Project Context Brief — ERP Modernization Engagement

## Client Objective

Replace the 14-year-old ERP-integration layer, launch a customer self-service portal, and add an AI assistant for sales operations before the legacy-support contract expires in 12 months. Delivery is fixed-price, single supplier (EPAM), blended team of 14.

---

## Business / Result Outcomes

| Outcome | Baseline / current signal | Target / win evidence | Source |
|---------|--------------------------|----------------------|--------|
| Go-live readiness | Legacy support expires in 12 months; no sign-off process in place | Release readiness signed by operations and compliance before month 11 | Proposal pack |
| Handoff clarity | Release decisions live in chat threads — no owner, no rationale logged | 100% of release decisions have owner, rationale, date, and rejected option logged | Delivery log |
| Delivery predictability | Risk register exists but is not linked to phase gates; status is narrative only | Top 5 risks reviewed weekly with go-to-green action; milestone movement tracked | PM report |
| Sales-ops efficiency | Quote/order cycle time not measured; sales-ops team uses manual lookups | AI assistant reduces quote preparation time; self-service portal handles ≥30% of routine order queries | Sales-ops lead estimate |

---

## Scope Boundaries

**In scope:** ERP integration platform (API layer replacing legacy middleware), customer self-service portal, AI assistant for sales operations, Azure deployment (client tenant), GDPR controls (data residency, PII handling, consent log).

**Out of scope:** Replacing the ERP core itself (SAP S/4HANA), multi-vendor delivery coordination, client HR or finance systems, and any functionality not specified in the SOW.

---

## Top Constraints

| ID | Constraint | Type | Impact if breached |
|----|-----------|------|-------------------|
| C-1 | 12-month hard deadline (legacy support expires) | Timeline | Cost overrun and production downtime risk |
| C-2 | Fixed-price commercial model | Commercial | EPAM absorbs overrun; scope creep is the primary delivery risk |
| C-3 | Azure tenant locked to EU data residency | Technical / Regulatory | GDPR Article 46 and client IT policy; no cross-border data transfer |
| C-4 | GDPR + EPAM AI governance | Regulatory | PII cannot enter unapproved AI tools; Safe Harbor gate required |
| C-5 | Single supplier | Commercial | No sub-vendor coordination overhead; all capability gaps sit with EPAM |

---

## Delivery Milestones (known)

| ID   | Milestone                                                              | Target date | Owner                                        |
|------|------------------------------------------------------------------------|-------------|----------------------------------------------|
| M0   | Contract signed + team onboarded                                       | Month 1     | EPAM delivery sponsor                        |
| M1   | Integration platform design approved                                   | Month 2     | Tech lead + client CTO                       |
| M2   | Integration layer deployed to staging; integration tests pass (0 critical defects) | Month 3 | Tech lead                           |
| M3   | Portal MVP deployed to staging                                         | Month 4     | Tech lead + client COO                       |
| M4   | Portal UAT complete; acceptance sign-off                               | Month 5     | Client COO + QA lead                         |
| M5a  | AI assistant — quote generation beta accepted by sales-ops team        | Month 6     | Delivery lead + sales-ops lead               |
| M5b  | AI assistant — lead triage beta accepted by sales-ops team             | Month 7     | Delivery lead + sales-ops lead               |
| M5c  | AI assistant — order-status answers beta accepted by sales-ops team    | Month 8     | Delivery lead + sales-ops lead               |
| M6   | GDPR compliance review complete                                        | Month 9     | Compliance lead + client DPO                 |
| M7   | End-to-end integration test + pen test passed                          | Month 10    | Tech lead + QA lead                          |
| M8   | Release readiness signed; go-live                                      | Month 11    | Delivery lead + client COO + compliance lead |

---

## Known Quality / Risk Gates

| Gate | Phase | Threshold | Human owner |
|------|-------|-----------|------------|
| Integration test gate | Build → Validate | 0 critical defects; ≤3 high defects open | Tech lead |
| AI assistant eval gate | Validate | Golden-set pass rate ≥90%; 0 critical safety failures | QA lead |
| GDPR Safe Harbor check | Validate + Handoff | All PII data classes logged; no unapproved tool used on confidential data | Compliance lead |
| Decision Memory gate | Handoff | 100% release decisions have owner, rationale, rejected option, date | Delivery lead |

---

## Bootcamp Win Evidence

Weekly delivery-health + AI-adoption memo showing outcome telemetry and Safe Harbor gate status. Specifically: at least one customer-benefit metric moved from baseline (e.g. decision-reopen count from 4 to ≤1, or defect escape from 7 to ≤3) within the 90-day adoption window — with source evidence cited in the status report, not asserted from memory.

---

## First AI-Adoption Hypothesis

If Intake improves from L0 to L1 — by introducing AI-assisted qualification summaries with source-linked triage — then unplanned scope changes should fall to ≤2 per month, reducing the rework and reprioritisation that currently propagates into Plan, Build, Validate, and Handoff. Intake is the right first target: it is the only L0 phase, and scope instability here undermines every downstream improvement. Fixing Handoff while Intake stays at L0 treats symptoms of a problem that originates earlier.
