---
kata: K 10.D.7
artefact: 1000-deep/06-gates.md
consumes_from: 04-maturity-baseline.md, 05-operating-model.md
engagement: ERP-modernization — EU industrial-machinery manufacturer
date: 2026-07-08
status: complete
---

# Safe Harbor Quality and Risk Gates — ERP Modernization Engagement

*Gates for the three highest-risk phases (Build, Validate, Handoff), each with a numeric threshold, enforcement mechanism, escalation path, AI-use authorization row, and customer-risk prevented.*

---

## Gate Table

| Phase gate | Required check | Numeric threshold | Enforcement mechanism | Escalation path | AI-use authorization row | Customer risk prevented |
|-----------|---------------|------------------|-----------------------|----------------|--------------------------|------------------------|
| **Build — AI PR review** | AI-assisted PR review passes rule-file lint; tech lead signs every AI-authored change | Lint = 0 errors; reviewer sign-off present on every PR with an AI-assist tag | CI pipeline (lint step blocks merge on failure) + tech lead mandatory review | Tech lead decides block/override; delivery lead records every exception in the decision log; EPAM delivery sponsor reviews exceptions weekly | Approved tools: CodeMie, Claude (DIAL tier), or EPAM-approved equivalent only; source code allowed only with SOW confirmation; **credentials/secrets never enter AI tools**; `rules/` repo changes require tech-lead sign-off | Quality regression — AI-authored code merges without human verification → change-failure rate rises; throughput↑ + CFR↑ combination is a risk signal, not a win |
| **Validate — AI golden-set eval** | AI-generated test cases reviewed by QA lead; golden-set run passes before any release candidate is promoted | Golden-set pass rate ≥90%; 0 critical safety failures; QA lead sign-off on every release candidate | QA sign-off (mandatory) + CI golden-set run (blocks promotion on failure) | QA lead blocks release candidate; delivery lead escalates timeline impact to COO if ≤2 weeks remain; compliance lead reviews if any test case touches PII or GDPR-classified data | Confidential test data only in approved tool tier (DIAL/CodeMie, EU-hosted); **PII removed from test inputs before cloud reasoning** unless written authorization from data owner (compliance lead); no raw production data in AI tools | Defect escape and policy breach — AI-generated tests inflate coverage without testing critical paths; escaped defect or GDPR policy breach reaches client |
| **Handoff — Decision Memory completeness** | All release decisions logged in the decision log before handoff pack is issued | 100% of release decisions have: owner, rationale, rejected option, date; decision-reopen count ≤1 per month after gate passes | Human review by delivery lead (mandatory); compliance lead countersigns all GDPR-relevant decisions | Delivery lead owns sign-off; if a decision is missing: gate blocked, delivery lead escalates to COO with the gap named and a date to resolve; no "partial handoff" accepted | AI may summarize decision logs **only after** client-data authorization is confirmed by compliance lead; draft summary produced in DIAL (Internal tier); **strictly confidential decisions not summarized by AI** unless authorized | Go-live confusion — undocumented decisions reopen in the post-go-live support window; compliance gap creates GDPR audit exposure |

---

## Safe Harbor Block

The following data-class handling rules apply to all AI tool use on this engagement. Every gate's AI-use authorization row must reference these rules.

| Data class | Example on this project | Permitted AI tool use | Authorization required | Legal trigger |
|-----------|------------------------|----------------------|----------------------|--------------|
| **Public / Internal** | Project timeline, team names, milestone list, delivery metrics | Any EPAM-approved AI tool with output review; no raw client name in public tools | None beyond standard EPAM acceptable-use policy | None |
| **Confidential** | Risk log details, client strategic plans, commercial terms, staffing costs | Approved internal tool tier only (DIAL, CodeMie — EU-hosted, EPAM-controlled); **no public cloud AI tools** | Delivery lead confirms tool tier before first use; compliance lead reviews if client data is involved | MSA data-processing clause; EPAM GenAI policy |
| **Strictly confidential** | Client financial data, M&A-related content, board-level decisions | **Blocked** from AI tool use unless client data owner provides written authorization to compliance lead | Written authorization from client data owner + compliance lead countersign | Data Processing Agreement; EPAM Security Policy |
| **PII** | Sales-ops user names, email addresses, contact data in the portal | **Remove PII before cloud reasoning**; anonymize or tokenize; use only in approved on-premise or EPAM-controlled AI tier | Data owner authorization (compliance lead); DPIA review if new processing activity | GDPR Article 5(1)(b) purpose limitation; Article 25 data protection by design |
| **Credentials / Secrets** | API keys, Azure service principal credentials, database passwords | **Never enter AI tools** — not in prompts, not in test data, not in PRs | Not applicable — unconditional block | EPAM Security Policy; SOW confidentiality clause |
| **Source code** | ERP integration layer, portal codebase, sales-ops assistant logic | Permitted in approved tool tier (CodeMie, GitHub Copilot Enterprise — if EPAM allow-listed for this engagement); **SOW confirmation required** before first use | SOW/tool-tier confirmation from EPAM delivery sponsor; tech lead validates before first use | EPAM IP protection policy; client source-code ownership clause in SOW |

---

## Gate Override Protocol

An override of any gate threshold requires:
1. The decision-level owner (tech lead for Build; QA lead for Validate; delivery lead for Handoff) documents the override in the decision log with: rationale, risk accepted, mitigating action, and expiry date.
2. Delivery lead reviews within 24 hours and records the override in the weekly status report.
3. No override that increases GDPR risk is accepted without compliance lead countersignature.
