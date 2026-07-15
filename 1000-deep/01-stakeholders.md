---
kata: K 10.D.2
artefact: 1000-deep/01-stakeholders.md
consumes_from: 00-project-context.md
engagement: ERP-modernization — EU industrial-machinery manufacturer
date: 2026-07-08
status: complete
---

# Stakeholder Map — ERP Modernization Engagement

---

| Stakeholder / Role | Goal | Influence | Concern | Decision owned | Evidence they trust | Reporting cadence | Escalation trigger |
|-------------------|------|-----------|---------|----------------|--------------------|--------------------|-------------------|
| **Client COO** | Go live before legacy support expires; no production downtime at cutover | High | Schedule slip; scope creep delaying go-live | Launch priority and phase-gate go/no-go | Milestone movement; risk burndown chart; go-live readiness sign-off | Weekly | Critical path moves by ≥2 weeks or M8 confidence drops |
| **Client CTO** | Stable, performant Azure integration that does not degrade ERP uptime | High | Integration quality; unverified AI tool use on production data | Technical readiness approval at each gate | Gate results (pass/fail with threshold); defect escape trend; integration test report (M2, M7) | Weekly | Integration gate fails twice in a row or critical defect escapes to staging |
| **Compliance Lead** | GDPR-safe AI assistant; no PII entering unapproved tools; DPO alignment | High | PII handled by AI tools without authorization; unclear data classification | Privacy approval and Safe Harbor gate sign-off per release | Safe Harbor log; data-class audit trail; DPIA status | Per release (+ weekly flag if new PII surface discovered) | Any unclear data class entering an AI tool; DPIA gap identified after M6 |
| **Sales-Ops Lead** | AI assistant improves quote/order workflow; measurable cycle-time reduction | Medium | Low adoption; assistant answers unreliably; team resistance | Workflow acceptance and AI assistant sign-off per feature (M5a quote generation → M5b lead triage → M5c order-status) | User feedback score per feature; quote cycle-time signal; assistant accuracy trend | Biweekly | Adoption below target after 4-week pilot; 2+ reliability complaints from the team |
| **EPAM Delivery Sponsor** | Predictable delivery within fixed-price envelope; margin protected | High | Fixed-price risk; scope creep; capability gaps materializing late | Escalation/funding decisions; staffing changes above threshold | Status report (health + risks + financial outlook); staffing scenario; risk-exposure trend | Weekly | Risk exposure grows above contingency floor; Azure specialist availability not confirmed by week 2 |

---

## Notes

- **COO and CTO are co-blockers** on the go/no-go decision at M8 — both must sign release readiness; a veto from either delays go-live.
- **Compliance Lead** is the only stakeholder who can block a release after M6 if a GDPR gap is found; her escalation trigger operates independently of the COO/CTO chain.
- **Sales-Ops Lead** has medium influence but owns three sequential sign-offs (M5a → M5b → M5c); a failed M5a blocks the later features and puts the AI assistant workstream at risk within the fixed-price envelope.
- **EPAM Delivery Sponsor** is the internal escalation owner; client-facing escalations pass through the COO/CTO escalation chain, not directly to the sponsor.
