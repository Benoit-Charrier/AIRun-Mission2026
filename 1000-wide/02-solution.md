---
kata: K 10.W.3
consumes_from: K 10.W.1 (00-rfp.md), K 10.W.2 (01-qualification.md), M200 spec package, M300 design pack, M400 architecture record, M500 engineering evidence chain
date: 2026-07-07
artefact: 1000-wide/02-solution.md
compliance_shape: Turn-key
patched: 2026-07-07 (per 02-review.md critique C-1 and C-2)
---

# Solution Outline — MRG AI-Enabled Omnichannel Commerce Platform

---

## High-Level Approach

EPAM will deliver the MRG platform modernisation as a turn-key engagement — we design, build, test, and hand over a production-ready system. The delivery is structured as three gated phases, each with contractually defined entry and exit criteria, so that scope, risk, and payment milestones are anchored to delivery events rather than calendar dates. Phase 1 targets the highest-risk and highest-value element first (checkout modernisation and SAP integration), so the commercial constraint (fixed-price) is underwritten by a scoped and confirmed baseline before Phase 2 begins. The AI availability assistant is introduced in Phase 2 as a prediction-only service, constrained by architecture to prevent autonomous actions. Full 1,400-store rollout and knowledge transfer close Phase 3.

---

## Phase Table

| Phase | Entry criteria | Exit criteria | Duration | Owner |
|-------|---------------|--------------|----------|-------|
| **Phase 1 — Checkout modernisation + SAP API** | Contract signed + scoping sprint complete (SAP API access granted + scope baseline documented + fixed price confirmed) | Web + mobile checkout live in production; OWASP Top 10 baseline passed; production error rate ≤0.1%; ≥80% API test coverage | 8 weeks (2026-09-01 → 2026-10-31) | EPAM delivery lead |
| **Phase 2 — Click-and-collect + AI availability assistant** | Phase 1 exit met + DPIA sign-off issued + AI model registered in MRG model registry | Click-and-collect live in 100 pilot stores; AI assistant active with prediction-only constraint enforced at API layer; no autonomous booking actions verified | 8 weeks (2026-11-01 → 2026-12-31) | EPAM delivery lead |
| **Phase 3 — Full rollout + runbooks + knowledge transfer** | Phase 2 exit met + clean pen-test report from NCC Group OR all Critical findings remediated and re-verified (timeline impact: Critical finding detected in weeks 17–19 adds ≤2 weeks to Phase 3; cost absorbed by contingency reserve) | All 1,400 stores live; 3 MRG engineers signed off at L2 on new stack; runbooks accepted by MRG operations lead; platform handed to MRG run team | 4 weeks (2027-01-01 → 2027-01-31) | EPAM engagement director + MRG ops lead |

---

## Outsourced Capability — Security Pen-Test (NCC Group)

EPAM has no in-house CREST-certified penetration testing capability at the depth required by MRG's C-5 constraint. The pen-test is outsourced to **NCC Group** (CREST-certified, EU-regulated sector experience).

**Integration:**  
NCC tests the production checkout API and click-and-collect endpoints against the scope defined in the EPAM security evidence pack (derived from M900 K 9.W.5 format — control identity, test method, monitoring, audit trail). EPAM provides NCC with the threat model, risk register, and test scope document at Phase 2 exit. NCC's output is a signed clean-bill-of-health report (or a findings report with CVSS scores).

**Governance:**  
- EPAM writes and owns the remediation plan for any finding; NCC does not dictate remediation approach.  
- Gate: NCC findings report delivered ≥2 weeks before Phase 3 exit target, giving EPAM a remediation buffer.  
- Escalation path: EPAM security lead → EPAM engagement director → NCC account lead; MRG CTO notified of any Critical (CVSS ≥9.0) finding within 24 hours of receipt.  
- Phase 3 entry criterion updated (post-review patch): "clean pen-test report OR all Critical findings remediated and verified by NCC" — a Critical finding detected in weeks 17–19 adds ≤2 weeks; cost absorbed by contingency.

---

## Key Assumptions

| # | Assumption | Bound / falsifiable condition |
|---|-----------|-------------------------------|
| A-1 | MRG provides SAP API access and full documentation | Within 14 calendar days of contract signature; if not met, Phase 1 go-live shifts by the equivalent delay |
| A-2 | MRG DPO allocates ≥4 h/week to DPIA review | Weeks 1–4; delay of >1 week triggers a Phase 2 start-date review; if DPO unavailable for >3 weeks, Phase 2 go-live moves to 2027-01-31 |
| A-3 | Pilot-store test environment (100 stores) available | From 2026-10-01; delay shifts Phase 2 exit by equivalent delay |
| A-4 | ≥70% team utilisation from sprint 3 (week 5) onward | If utilisation falls below 60% in any sprint, delivery manager triggers a capacity review within 48 hours |

---

## Client-Side Dependencies

- SAP API access + full documentation (A-1)
- DPO availability for DPIA co-authorship (A-2)
- 100-store pilot test environment provisioned by MRG IT (A-3)
- 3 MRG engineers identified and released for knowledge transfer from week 12
- MRG product owner available for sprint review within 48 h of delivery

---

## Out-of-Scope Statement

The following are explicitly out of scope for this engagement: POS terminal software, loyalty and rewards module, B2B/wholesale portal, returns and refunds workflow beyond order-status lookup, agentic AI (the availability assistant takes no booking or payment actions in v1), infrastructure provisioning outside the EPAM-defined cloud environment.

---

## Compliance Shape

**Turn-key.** EPAM delivers the complete solution using EPAM pre-approved tools (DIAL, GitHub Copilot, Claude for internal-only data) plus anything additionally cleared by MRG's Data Classification Matrix. Any use of AI tools on MRG PII/PHI/regulated data triggers a compliance assessment and DPO sign-off before use — confirmed in writing at contract signature against MRG's C-7 constraint. Legal review: this engagement requires a signed DPA covering AI inference on customer session data and order history.
