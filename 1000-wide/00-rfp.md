---
kata: K 10.W.1
buyer: Meridian Retail Group S.p.A. (Italy/EU)
project: AI-Enabled Omnichannel Commerce Platform — Modernisation and Click-and-Collect Intelligence
date: 2026-07-07
artefact: 1000-wide/00-rfp.md
---

# Request for Proposal
## AI-Enabled Omnichannel Commerce Platform — Modernisation and Click-and-Collect Intelligence

**Issued by:** Meridian Retail Group S.p.A., Digital & Technology Division  
**Issue date:** 2026-07-07  
**Response deadline:** 2026-07-28  
**Contact:** rfp-digital@meridianretail.eu | PGP-encrypted submissions only  

---

## 1. Buyer & Decision

Meridian Retail Group (MRG) operates 1,400 stores across Italy and the EU, serving approximately 3.2 million registered customers through a web storefront and 12 mobile applications. MRG's current commerce platform is a monolithic stack built in 2017. The system does not support unified inventory visibility across channels, real-time click-and-collect slotting, or AI-assisted customer guidance at point of search and discovery.

**Decision being made.** MRG is selecting a delivery partner to design, build, and hand over a modernised omnichannel commerce platform, including an AI availability assistant integrated into the checkout and click-and-collect flows. The partner will own delivery end to end (turn-key engagement) and hand back a production-ready system with runbooks, a security evidence pack, and trained internal owners.

---

## 2. Objective

Deliver a production-ready omnichannel commerce platform that:

- Unifies web, mobile (12 apps), and in-store inventory in real time across all 1,400 locations
- Introduces click-and-collect with AI-assisted slot-availability guidance (prediction-only, GDPR-compliant)
- Replaces the current SAP integration batch-sync with a resilient, observable API service (latency target: ≤500 ms p95)
- Achieves a change-failure rate ≤5% and deployment frequency ≥2 per week within 6 months of go-live
- Passes GDPR Article 35 DPIA review and PSD2 SCA compliance sign-off before final go-live

---

## 3. Scope

**In scope**

- Modernisation of the web storefront checkout flow (cart → payment → confirmation)
- Modernisation of all 12 mobile-application checkout and order-management APIs
- Real-time inventory API replacing the existing SAP batch-sync
- AI availability assistant: prediction model for click-and-collect slot availability; outputs surface to customer-facing UI only; prediction-only (no autonomous booking actions in v1)
- Notification service (email + SMS) for order confirmation, collection reminder, and delay alert
- Security hardening: parameterised query enforcement, WAF, input validation, credential rotation
- Data platform: unified order and inventory data product in the MRG data warehouse
- Test automation: ≥80% API test coverage; performance regression suite
- Runbooks, security evidence pack (OWASP Top 10 baseline), deployment playbook
- Knowledge transfer: 3 internal MRG engineers trained to L2 on the new stack

**Out of scope (v1)**

- In-store POS terminal software
- Loyalty and rewards module
- B2B/wholesale portal
- Returns and refunds workflow beyond order-status lookup
- Agentic AI (the availability assistant does not take booking or payment actions in v1)

---

## 4. Constraints

| # | Constraint | Detail |
|---|-----------|--------|
| C-1 | Commercial model | Fixed-price preferred. MRG will consider a hybrid (fixed Phase 1 + Phase 2, T&M cap on Phase 3) with written justification. T&M-only bids will be scored down on EC-2. |
| C-2 | Timeline | Full platform go-live by 2027-01-31. Phase 1 (checkout modernisation) go-live by 2026-10-31. |
| C-3 | Data residency | All customer PII and payment data must remain within the EU. No PII in non-EU AI inference calls without a signed DPA. |
| C-4 | AI governance | The AI availability assistant must be registered in MRG's internal AI model registry before go-live. Prediction outputs are advisory only; no autonomous actions. |
| C-5 | Security | OWASP Top 10 compliance verified by an independent CREST-certified pen-test report before go-live. |
| C-6 | GDPR / PSD2 | DPIA completed and DPO sign-off obtained. PSD2 SCA enforced on all payment flows. |
| C-7 | Tooling | AI development tools used on MRG data must be cleared against MRG's Data Classification Matrix before use; supplier confirms in writing at contract signature. |

---

## 5. Evaluation Criteria

Responses will be scored out of 100. The evaluation committee will apply the weights below. Scores are final once the committee has met; re-scoring requests are not accepted.

| # | Criterion | Weight |
|---|-----------|--------|
| EC-1 | Solution fit — quality of technical approach, phase design, integration architecture | 35 |
| EC-2 | Commercial — total cost of ownership, fixed-price commitment, payment milestones | 25 |
| EC-3 | Team & references — named delivery leads, EU delivery track record, reference customer in retail/omnichannel | 20 |
| EC-4 | AI governance — AI-SDLC maturity, DPIA readiness, model-registry approach, prediction-only enforcement | 10 |
| EC-5 | Delivery risk management — risk register quality, contingency structure, assumption register | 10 |
| **Total** | | **100** |

**Minimum thresholds.** Bidders must score ≥15/35 on EC-1 and ≥6/10 on EC-4 to remain eligible. Bids below either threshold are eliminated before commercial scoring.

**Bidder pre-scoring aid**

| Criterion | Weight | Self-score (1–5) | Weighted |
|-----------|--------|------------------|---------|
| EC-1 Solution fit | 35 | — | — |
| EC-2 Commercial | 25 | — | — |
| EC-3 Team & references | 20 | — | — |
| EC-4 AI governance | 10 | — | — |
| EC-5 Delivery risk mgmt | 10 | — | — |
| **Total** | **100** | | |

---

## 6. Timeline

| Event | Date |
|-------|------|
| RFP issued | 2026-07-07 |
| Clarification window closes | 2026-07-21 |
| Responses due | 2026-07-28 |
| Shortlist interviews | 2026-08-04 to 2026-08-08 |
| Preferred-supplier notification | 2026-08-14 |
| Contract signature target | 2026-08-28 |
| Delivery kick-off | 2026-09-01 |
| Phase 1 go-live (checkout modernisation) | 2026-10-31 |
| Phase 2 go-live (click-and-collect + AI assistant) | 2026-12-31 |
| Phase 3 go-live (full platform + runbooks + KT) | 2027-01-31 |

---

## 7. Submission Rules

| Rule | Requirement |
|------|------------|
| Format | PDF + Markdown source. No Word documents. |
| Page limit | 25 pages excluding appendices; appendices capped at 15 pages. |
| Language | English. Italian translations accepted for appendices only. |
| Channel | rfp-digital@meridianretail.eu; subject: `[BID] MRG-2026-OCP — [Firm name]` |
| Disqualifiers | Late submission; missing EC-1 or EC-4 sections; PII in unencrypted submission; T&M-only bid without written justification |
| NDA | Bidders must sign MRG's standard NDA before receiving the technical data appendix. Submission without signed NDA is ineligible. |
| Reference customer | Bidders must name at least one reference customer in EU retail or omnichannel commerce. MRG reserves the right to contact the reference directly before shortlist. |
| Clarifications | Submit clarification questions in writing by 2026-07-21. Answers are published to all bidders simultaneously. No private clarifications. |
