---
kata: K 10.W.6
consumes_from: K 10.W.3 (02-solution.md phases), K 10.W.4 (03-staffing.md balanced variant), M600 QA test report, M900 security evidence pack, M800 platform runbooks
date: 2026-07-07
artefact: 1000-wide/05-plan.md
---

# Implementation & Rollout Plan — MRG AI-Enabled Omnichannel Commerce Platform

---

## Milestone Table

| # | Milestone | Date | Entry criterion | Exit criterion | Owner |
|---|-----------|------|----------------|----------------|-------|
| M0 | Contract signature | 2026-08-28 | Preferred-supplier notification issued | Contract + NDAs + data access agreements signed; scoping sprint scheduled | EPAM engagement director |
| M1 | Scoping sprint complete | 2026-09-14 | M0 + SAP API access granted | Scope baseline documented; fixed price for Phase 1 + Phase 2 confirmed or revised; Phase 1 start authorised | EPAM delivery lead |
| M2 | DPIA sign-off | 2026-10-15 | DPIA draft reviewed in ≥4 DPO sessions (weeks 1–4) | DPO sign-off issued in writing; AI model registry entry created for availability assistant | MRG DPO + EPAM security lead |
| M3 | Phase 1 go-live | 2026-10-31 | M1 + ≥80% API test coverage in staging | Checkout live in production; OWASP Top 10 baseline passed; production error rate ≤0.1%; Phase 1 fixed payment milestone triggered | EPAM delivery lead + MRG product owner |
| M3a | Pilot store environment ready | 2026-10-01 | MRG IT provisioning in progress (dependency from assumption A-4) | 100-store pilot test environment confirmed available by MRG IT; EPAM delivery lead notified; if delayed, Phase 2 start date reviewed | MRG IT operations |
| M4a | 20-store initial pilot live | 2026-11-21 | M3 (Phase 1 live) + Phase 2 build/test complete for store features + M3a (pilot environment ready) | Click-and-collect active in 20 lowest-traffic pilot stores; error rate ≤0.5% over 48 h; Champion feedback captured and reviewed; no blocking defects | EPAM delivery lead + MRG store ops champion |
| M4b | 100-store pilot expansion | 2026-12-05 | M4a with no blocking defects + Champion sign-off on 20-store results | Click-and-collect active in all 100 pilot stores; AI availability assistant live (prediction-only enforced at API layer); no autonomous booking actions verified in production | EPAM delivery lead |
| M4 | Phase 2 go-live (pilot accepted) | 2026-12-31 | M4b + AI assistant verified in production for ≥3 weeks + MRG product owner sign-off | 100-store pilot accepted; Phase 2 payment milestone triggered; Phase 3 rollout to remaining 1,300 stores authorised | EPAM delivery lead + MRG CTO |
| M5 | Phase 3 go-live | 2027-01-31 | M4 + clean NCC pen-test report OR all Critical findings remediated and re-verified | All 1,400 stores live; 3 MRG engineers signed off at L2; runbooks accepted by MRG ops lead; platform handed to MRG run team | EPAM engagement director + MRG CTO |

*Milestone diagram: see 05-timeline.md*

---

## Governance Cadence

| Forum | Frequency | Attendees | Decision rights |
|-------|-----------|-----------|----------------|
| Steering committee | Monthly (last Thursday) | EPAM engagement director; MRG CTO; MRG CPO; MRG DPO (for months 1–3) | Budget changes; go/no-go at phase gates; escalation resolution; scope change authorisation |
| Sprint review | Biweekly | EPAM delivery lead; MRG product owner; EPAM feature leads | Story acceptance; sprint-level scope adjustments; quality gate decisions |
| Retrospective | Biweekly (after sprint review) | EPAM team; MRG product owner (optional) | Process changes; team capacity adjustments; tooling decisions |
| Risk review | Monthly (embedded in steering) | EPAM delivery lead; EPAM security lead; MRG CTO | Risk register updates; escalation to deal-breaker; mitigation budget release from contingency |

**Executive sponsor:** EPAM VP of EU Delivery (written authority to unblock policy, budget, or escalation beyond the delivery manager's reach; MRG side equivalent: MRG CTO with sign-off authority on scope changes and phase-gate go/no-go).

---

## Change-Management Plan

### Resistance Scenarios and Response Patterns

| Resistance scenario | Who | Response pattern |
|--------------------|-----|-----------------|
| "AI tools in our checkout are a security risk" — MRG engineers sceptical of AI-assisted code generation | MRG backend engineers, 2–3 individuals | Show the M900 security evidence chain: threat model, scored risk register, control implementation (commit SHA), OWASP bypass tests. Frame as "this is the evidence trail we produce *because* we use AI carefully, not evidence that AI is safe by default." Do not argue security in the abstract — show the artefact. |
| "Click-and-collect will disrupt our store operations during peak" — store managers concerned about the pilot | Store managers at the 100 pilot stores | Run the pilot in the 20 lowest-traffic stores first, not the 20 highest. Named store Champions (see below) communicate the rollout plan in Italian. Share the pilot results before expanding to 100 stores. |
| "I can't get to the DPIA review sessions" — MRG DPO time-constrained | MRG DPO | DPIA co-authorship: DPO reviews and contributes to each section as it is drafted, not in batch at the end. This lowers the per-session time from 3 hours to 45 minutes. DPIA delay >1 week triggers a Phase 2 start-date review — this cost is named in the contract, so the DPO's line manager understands the schedule consequence. |

### Adoption Tracking

| Behaviour | What it signals | How measured |
|-----------|----------------|-------------|
| AI-assisted story drafts committed in version control | Real adoption of AI workflow in intake phase | PR history: ≥75% of stories have an AI-assisted draft user story in the PR description by sprint 4 (counted by EPAM delivery lead at sprint review) |
| Prompt template reused by ≥2 MRG engineers in KT sessions | Knowledge is transferring, not just demonstrated | KT session log: prompt template reuse count tracked per engineer per session from week 12 |
| Retro insight committed to action board within 48 hours | Team is using the retrospective as a real process improvement tool, not a ceremony | Retro action board (Jira): timestamp of action creation vs retro close; target ≥1 actioned insight per sprint from sprint 3 onward |

### Champion Network

| Champion role | Who | Protected time | Responsibility |
|--------------|-----|---------------|---------------|
| Internal delivery champion | MRG senior engineer (checkout) | 20% from week 8 | Owns the L2 sign-off process; attends sprint reviews; co-authors runbooks |
| Data champion | MRG data analyst (inventory team) | 20% from week 12 | Owns the data product sign-off; co-authors data platform runbook |
| Store operations champion | MRG regional ops manager (pilot stores) | 10% from week 14 | Communicates the click-and-collect rollout to store managers in Italian; captures pilot feedback |

Champions own the runbook maintenance and knowledge transfer continuity after handover. Their protected time is contracted in the engagement addendum — not managed as a favour.

---

## Stakeholder Map

| Stakeholder | Interest | Influence | Key concerns | Engagement signal to monitor |
|------------|---------|-----------|-------------|------------------------------|
| MRG CTO | Platform modernisation delivered on time and on budget; AI governance satisfied | H | Timeline risk; fixed-price exposure; SAP integration unknown | Attends monthly steering + asks specific technical questions (not only status); stops asking status = drifting |
| MRG DPO | GDPR compliance; DPIA completed before AI assistant goes live | H (veto on AI assistant) | PII in AI inference calls; DPA scope; EU data residency | Responds to DPIA review comments within 5 business days; silence for >5 days = escalate |
| MRG product owner (digital) | Checkout UX uplift; click-and-collect feature parity with competitors | M | Feature scope creep; UI changes not in spec | Reviews sprint artefacts within 48 h of delivery; persistent late reviews = engagement drift |
| EPAM delivery lead | Delivery on time and within budget; team health | H (internal) | SAP scope unknown; ramp risk in month 1; contingency burn | Updates risk register after every steering committee; if risk register stale for >2 weeks, flag to engagement director |

---

## Comms Plan

Cadences are derived from the stakeholder map, not from politeness. MRG CTO (high influence, strategic) and the EPAM delivery team (internal, operational) are in different quadrants and need different cadences.

| Audience | What they get | Channel | Cadence | Owner |
|---------|--------------|---------|---------|-------|
| MRG CTO | Steering deck (milestone status, risk register delta, phase gate decision required); written exception report when any risk score increases by ≥5 or phase gate status changes | Email + monthly steering meeting | Monthly; exception report within 24 h of trigger | EPAM engagement director |
| EPAM delivery team | Sprint plan + sprint review + retrospective outcomes; Slack: daily async updates on blockers | Confluence wiki + Slack #mrg-ocp-delivery | Biweekly sprint cadence + daily async | EPAM delivery lead |

*Note: cadences differ deliberately. MRG CTO sees structured monthly summaries and exception reports — not the daily noise. The EPAM team sees daily async status. Sending the CTO daily Slack updates dilutes attention; sending the delivery team only monthly steering decks masks operational blockers.*
