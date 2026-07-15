---
kata: K 10.D.4
artefact: 1000-deep/03-command-center.md
consumes_from: 00-project-context.md, 01-stakeholders.md, 02-staffing-scenario.md
engagement: ERP-modernization — EU industrial-machinery manufacturer
title: Command center — project second brain
owner: delivery lead
freshness_rule: refresh the source map weekly; re-confirm owners after any steering change
safe_harbor: no confidential client data in public tools; PII removed before cloud reasoning unless the data owner authorizes
date: 2026-07-08
status: complete
---

# Command Center — Project Second Brain

*This is an LLM-wiki page: a governed Markdown knowledge map the delivery assistant reads via an approved filesystem or Git MCP server to produce the weekly status report.*

---

## Source Map

| Source | Location | Owner | Freshness rule | Privacy / Safe Harbor boundary | Used in status? |
|--------|----------|-------|----------------|-------------------------------|----------------|
| Project context brief | `1000-deep/00-project-context.md` | Delivery lead | Update after any steering change or scope revision | Internal only — no confidential client data pasted to public tools | Yes |
| Stakeholder map | `1000-deep/01-stakeholders.md` | Delivery lead | Weekly — review escalation triggers after each steering meeting | Internal use only; stakeholder names are internal | Yes |
| Staffing scenario | `1000-deep/02-staffing-scenario.md` | Delivery lead | Update after any staffing change or capability gap closes | Candidate people data validated before sharing; no personal data in AI tools | Yes |
| Risk log | Jira / risk register (linked in project Confluence) | PM | Weekly; top 5 risks refreshed before status report | Redact client-sensitive details before AI use; delivery-level risk only | Yes |
| Decision log | Confluence — "Release Decisions" page (repo: `1000-deep/` for snapshots) | BA lead | Updated per decision; reviewed at each release gate | Check authorization before summarizing client decisions with AI | Yes |
| Maturity baseline | `1000-deep/04-maturity-baseline.md` | Delivery lead | Update at each 30/60/90 review | Internal — no PII; adoption evidence only | Yes |
| Operating model | `1000-deep/05-operating-model.md` | Delivery lead | Update when a phase transitions rollout stage | Internal | Yes — AI adoption signal |
| Telemetry / metrics | `1000-deep/07-telemetry-status.md` + gateway logs (approved Azure tool tier) | Tech lead / QA lead | Weekly; sourced from Git + gateway at sprint close | Gateway logs: Internal/Confidential — approved tool tier only; no PII in log lines | Yes |

---

## MCP / Radar / Knowledge-Search Notes

| Query | Source path | Result | Validation status | Follow-up |
|-------|------------|--------|------------------|-----------|
| Azure Integration Services delivery examples and capability signals | EPAM Radar MCP (if available) or approved internal search; fallback: `1000-deep/02-staffing-scenario.md` | 2 related project references identified; 1 Azure specialist candidate found | Candidate — delivery lead to confirm availability by week 2 | Confirm Azure specialist availability; log as risk R-AZ-01 if unresolved |
| GDPR-safe AI assistant usage guidance | EPAM GenAI policy + AI Governance Advisory pack; fallback: `06-gates.md` Safe Harbor block | Safe Harbor gate required for PII and confidential data; approved tool tier is DIAL + CodeMie (EU-hosted) | Validated by compliance lead | Compliance lead reviews tool list before M3 AI assistant beta |
| Sales-ops AI assistant prior reference | EPAM knowledge base or Radar MCP | No direct match — adjacent reference in manufacturing sector | Candidate — delivery lead validates relevance | Surface to sales-ops lead at M3 sign-off prep |

*No-MCP fallback:* If Radar MCP is unavailable, run queries manually through the EPAM approved knowledge base and record search terms, date, and validation status in the table above.

---

## Weekly Status-Report Skeleton

> **Prompt:** Draft the weekly status report for the ERP modernization engagement using only the approved sources in the source map above. Flag any missing or stale evidence — do not invent figures. Do not include confidential client data.

**Delivery health:** [Overall RAG — Green / Amber / Red; one-line rationale citing the named exit criterion or milestone status]

**Milestone movement since last report:**
- [M_ name] — [on track / at risk / moved; by how much; owner]

**Risks / issues:**
- [Risk ID + description + current status + go-to-green action + owner]
- [Max 3 top risks — force prioritisation]

**Decisions needed:**
- [Decision + options + human owner + deadline]
- [Max 3 — anything not decided by this deadline goes to escalation]

**Staffing / capability notes:**
- [Any capability gaps, availability updates, or AI-assisted work rate changes]

**AI-adoption signal:**
- [Phase / metric / current value vs target — cite dimension and threshold from `05-operating-model.md`]

**Customer-benefit evidence:**
- [One metric that moved from baseline — cite source and delta; if no movement, say so explicitly]

**Next action:**
- [Single most important action before next report + owner + date]

---

## Approved-Source Prompt

```
Draft the weekly status report for the ERP modernization engagement using only:
- 1000-deep/00-project-context.md (context and outcomes)
- 1000-deep/01-stakeholders.md (escalation triggers and evidence needs)
- 1000-deep/04-maturity-baseline.md + 1000-deep/05-operating-model.md (AI adoption signal)
- 1000-deep/07-telemetry-status.md (metrics and movement)
- Current Jira risk log and decision log (provided at runtime)

Flag any missing or stale evidence — do not estimate or invent. Output the skeleton above with each
section populated from the named sources. Cite the source for every factual claim.
```
