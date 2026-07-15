---
kata: K 10.3 — Final Kata
artefact: 1000-final/delivery-pm-skill-brief.md
solution: Meridian Retail Group — omnichannel commerce platform
skill_file: .claude/skills/delivery-pm-status/SKILL.md
date: 2026-07-07
status: complete
---

# Module 1000 — Final Kata Brief
## Delivery PM Status Agent: Meridian omnichannel commerce

---

## What was built

A Claude Code Skill — `.claude/skills/delivery-pm-status/SKILL.md` — that turns the week's sprint signal (Jira export + AI-gateway log + retro output) plus the engagement's proposal pack into a weekly delivery-health + AI-adoption status memo ready for the MRG steering committee. It automates the RAG scoring, scorecard, adoption progress card, and go-to-green action list — and hands every commitment, escalation call, performance conversation, and contract change back to a named human every time.

---

## Nine-step completion evidence

| Step | What was done | Evidence |
|------|--------------|----------|
| 1 — Name + shape | **Skill** chosen (team reaches for the weekly-memo + RAG + go-to-green playbook; scope is weekly status → memo + scorecard + adoption card + go-to-green list). Name: `delivery-pm-mrg` | `name:` field in SKILL.md |
| 2 — Description | Names input files by exact path (proposal pack, carry-forwards, sprint signal), output files by exact path, ends with NOT clause (not for commitment, escalation, performance conversations, contract changes, Champion designations) | `description:` field; passes 3/3 routing test |
| 3 — Role / Goal / Inputs / Tools | One-sentence goal; every output named by exact path; tool allowlist (read_document, write_artifact scoped to `1000-final/`); no web, no client-data export | Body of SKILL.md |
| 4 — Decision rules | 6 DO/DON'T rows (all with counts or yes/no tests); escalate-never-decide list (9 items); 5 stop-and-ask conditions with measurable triggers; rules live inline inside chain markers | `## Decision rules` block in SKILL.md |
| 5 — Eval table | 3 rows; each names a test input by path and a counted or structural pass/fail signal | `How to check it's working` table in SKILL.md |
| 6 — Routing test | 3/3: tasks 1 and 2 matched correctly; task 3 (write AC for click-and-collect feature) correctly rejected and routed to PM/BA agent | Run-log, routing section |
| 7 — Real run | Happy-path: proposal pack + simulated sprint 1 signal → weekly-memo-2026-07-07.md (Phase 1 Amber with CFR 6% > 5% threshold cited; gateway log absent for Validate flagged; 3 decisions named). Hard question: "commit a new Phase 1 date of 2026-10-17" → escalated with steering committee data; no date committed | Run-log, happy-path + hard-input rows |
| 8 — One fix | Tightened the RAG DO row from "score RAG against the sprint signal" (adjective-only) to "score against the exit criterion from 05-plan.md — cite the specific criterion"; re-run produced a citation of "production error rate ≤0.1% not yet verified" rather than a bare "Amber" | Run-log, changed + re-run rows |
| 9 — Run-log | Pasted in full at the end of SKILL.md | `## Run-log` section |

---

## Done-when checklist

- [x] `description` gets picked correctly for 3/3 tasks in a fresh session (Step 6)
- [x] Agent produced the memo from one real input with no hand-fixing (Step 7)
- [x] At least one check-row was run against a named input, with a counted/structural verdict (Steps 5 + 7)
- [x] Hard question (commit a new go-live date) was refused/escalated — guardrail fired (Step 7)
- [x] One fix recorded with before/after (Step 8)
- [x] A teammate who never took this module could run it after one read (SKILL.md is self-contained)
- [x] Every input came from one source — Meridian Retail Group Case A
- [x] Run-log pasted in SKILL.md (Step 9)

---

## Human-owned decisions (never decided by the agent)

| Call | Where escalated |
|------|----------------|
| Commitment of any new date, scope, or commercial term | Hard-input test: "commit 2026-10-17" → refused, data surfaced for steering committee |
| Escalation calls on cost / quality / governance / client-risk threshold breaches | Escalate-never-decide list in SKILL.md |
| Performance conversations and staffing decisions | Escalate-never-decide list |
| Contract changes | Escalate-never-decide list + description NOT clause |
| Champion designations and removals | Escalate-never-decide list |
| Risk acceptance at portfolio level | Escalate-never-decide list |
| DPIA approval and DPO sign-off | Escalate-never-decide list (MRG DPO) |
| AI model classification — prediction-only vs agentic | Escalate-never-decide list (MRG CTO + EPAM architect) |
| Phase gate go/no-go | Stop-and-ask condition 4 + escalate-never-decide list |
