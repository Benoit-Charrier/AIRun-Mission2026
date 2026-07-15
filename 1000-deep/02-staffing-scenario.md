---
kata: K 10.D.3
artefact: 1000-deep/02-staffing-scenario.md
consumes_from: 00-project-context.md, 01-stakeholders.md
engagement: ERP-modernization — EU industrial-machinery manufacturer
date: 2026-07-08
status: complete
---

# Staffing Scenarios — ERP Modernization Engagement

---

## Scenario Comparison

| Scenario     | Roles                                                                   | Level / Seniority                                | Ramp                                           | Capacity                               | Capability gap                                                                                                                                                 | AI-assisted work assumption                                                                                                                       | Cost / speed / risk bet                                                                                                                                             | People/capability search notes                                                                                           | Recommendation                                                                                                |
| ------------ | ----------------------------------------------------------------------- | ------------------------------------------------ | ---------------------------------------------- | -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| **Lean**     | Core build + PM only; on-shore                                          | Mid-heavy; 1 tech lead                           | ~1 week (small team, minimal onboarding)       | 8 FTE                                  | Azure Integration Services — no dedicated specialist; QA coverage thin; no BA to own AC quality                                                                | AI drafts PM artefacts and test summaries; tech lead reviews alone; no dedicated QA review loop                                                   | Low cost / slower velocity / **higher integration and quality risk** — single-point-of-failure on Azure knowledge; defect escape risk unmitigated                   | Adjacent Azure expert found in EPAM Radar — candidate only, availability unconfirmed                                     | **No** — capability gap is structural; AI cannot compensate for missing Azure depth                           |
| **Balanced** | Build (3 engineers), BA, QA, PM + part-time security/compliance advisor | Balanced seniority; 1 dedicated Azure specialist | ~2 weeks (onboarding + ramp to full velocity)  | **14 FTE blended** (on/near-shore mix) | Azure depth covered by specialist; QA coverage adequate for golden-set gate; BA owns AC quality                                                                | AI assists status reporting, AC drafting, test-case generation review, and decision log; BA reviews AI-drafted ACs; QA reviews AI-generated tests | Balanced cost / manageable speed / **controlled risk** — capability coverage adequate; ramp predictable; coordination overhead low                                  | Azure specialist candidate identified via Radar MCP (pending validation); BA and QA roles from near-shore pool confirmed | **Yes** — covers the key capability gap without adding unmanageable coordination overhead                     |
| **Fast**     | Two squads + sub-vendor (coordination role)                             | Mixed seniority; sub-vendor at mid-level         | ~3–4 weeks (sub-vendor alignment + governance) | 22 FTE blended                         | Sub-vendor coordination creates governance overhead; sub-vendor Azure knowledge unconfirmed; GDPR-safe AI tooling needs additional vetting for sub-vendor team | AI supports coordination, sprint reporting, and cross-squad decision logging; sub-vendor uses own tools — authorization check needed              | High cost / faster potential velocity / **higher governance overhead and fixed-price risk** — coordination overhead eats margin; sub-vendor GDPR alignment unproven | Sub-vendor availability unknown; second squad still being sourced                                                        | **No** — faster only if coordination succeeds; overhead risk outweighs speed gain on a fixed-price engagement |

---

## Recommendation: Balanced (14 FTE)

**Decision:** Balanced scenario. It is the only variant that covers the Azure integration capability gap without adding sub-vendor coordination overhead that could breach the fixed-price envelope.

**Risk accepted:** Azure specialist availability must be confirmed by week 2. If the specialist is not available, the Lean scenario becomes the fallback — but the integration quality risk must be logged in the risk register and reviewed weekly until a specialist is onboarded or the gap is mitigated by an alternative.

**AI-capacity assumption:** The 14-person balanced team assumes AI tools reduce PM reporting and AC-drafting effort by ~20% per sprint — validated if the AI-assisted PR rate reaches ≥70% in Build by month 3 (per `05-operating-model.md`). If the assumption does not hold, the BA workload estimate must be revised upward in the month 2 review.

---

## Balanced Scenario — Role × Month Capacity Matrix

*FTE per month for the recommended Balanced scenario (14-person blended team). Column months map to the milestone calendar in `00-project-context.md`. `—` = role not yet started or already off the engagement. Bottom row totals FTE per month; rightmost column totals FTE-months per role.*

| Role | Seniority | Location | M1 | M2 | M3 | M4 | M5 | M6 | M7 | M8 | M9 | M10 | M11 | Total FTE-months |
|------|-----------|----------|---:|---:|---:|---:|---:|---:|---:|---:|---:|----:|----:|-----------------:|
| Delivery Lead / PM | Senior | On-shore | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | **11.0** |
| BA Lead | Senior | On-shore | 0.5 | 1 | 1 | 1 | 1 | 1 | 0.5 | 0.5 | 0.5 | 0.5 | — | **7.5** |
| Azure Integration Specialist | Senior | On-shore | 0.5 | 1 | 1 | 1 | 0.5 | 0.5 | — | — | — | — | — | **4.5** |
| Tech Lead | Senior | Near-shore | 0.5 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0.5 | **10.0** |
| Senior Engineer (Portal / Integration) | Senior | Near-shore | 0.5 | 1 | 1 | 1 | 1 | 0.5 | — | — | — | — | — | **5.0** |
| Full-Stack Engineer 1 | Mid | Near-shore | 0.5 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0.5 | 0.5 | — | **8.5** |
| Full-Stack Engineer 2 | Mid | Near-shore | 0.5 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0.5 | 0.5 | — | **8.5** |
| AI / ML Engineer | Senior | Near-shore | — | 0.5 | 1 | 1 | 1 | 1 | 1 | 1 | 0.5 | — | — | **7.0** |
| QA Lead | Mid-Senior | Near-shore | 0.5 | 0.5 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0.5 | **9.5** |
| QA Engineer | Mid | Near-shore | — | 0.5 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0.5 | **9.0** |
| DevOps / Azure Cloud Engineer | Mid | Near-shore | 0.5 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0.5 | **10.0** |
| UX / UI Designer | Mid | Near-shore | — | 0.5 | 1 | 1 | 1 | 0.5 | — | — | — | — | — | **4.0** |
| Security / Compliance Advisor | Senior | On-shore | 0.25 | 0.25 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.25 | **4.75** |
| Business Analyst | Mid | Near-shore | — | 0.5 | 1 | 1 | 1 | 1 | 1 | 0.5 | — | — | — | **6.0** |
| **Total FTE / month** | | | **5.25** | **10.75** | **13.5** | **13.5** | **13.0** | **12.0** | **10.0** | **9.5** | **7.5** | **7.0** | **3.25** | **105.25** |

*Milestones for reference: M1 design approved (month 2) · M2 integration deployed (month 3) · M3 portal MVP (month 4) · M4 portal UAT (month 5) · M5a–M5c AI assistant features (months 6–8) · M6 GDPR review (month 9) · M7 pen test (month 10) · M8 go-live (month 11).*

**Ramp / wind-down notes:**
- Month 1 (5.25 FTE): onboarding, environment setup, SOW baseline; only Delivery Lead at full capacity.
- Months 3–4 (13.5 FTE peak): integration build and portal build running in parallel; all roles active.
- Month 6 (12.0): portal roles (Sr Engineer, UX) wind down after M4 UAT sign-off; AI/ML engineer at full pace.
- Month 7 (10.0): BA Lead, Azure Specialist, UX off; AI assistant lead-triage sprint active.
- Months 9–10 (7.5 → 7.0): AI/ML, BA, portal engineers off; QA lead + QA engineer own the M6 GDPR review and M7 pen test.
- Month 11 (3.25): skeleton crew — Delivery Lead, Tech Lead (0.5), QA Lead (0.5), QA Engineer (0.5), DevOps (0.5), Security Advisor (0.25) — for go-live and hypercare handover.

---

## AI-Assisted Work Allocation

| Role | AI-assisted task | Review owner | Authorization check |
|------|-----------------|--------------|---------------------|
| PM / Delivery lead | Weekly status memo draft from approved sources | Delivery lead signs before sending | Sources approved; no confidential client data pasted to public tools |
| BA | Acceptance-criteria draft (stories) | BA lead reviews + product owner approves | Internal project data only; no PII |
| QA | Test-case scaffolding for sales-ops assistant | QA lead reviews against golden set | Confidential test data stays in approved tool tier |
| Tech lead | AI PR review (rule-file lint) | Tech lead signs every AI-authored change | Source code — SOW confirmation required; no credentials/secrets |
