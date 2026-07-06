---
kata: K 9.3 — Final Kata
artefact: 900-final/threat-model-skill-brief.md
solution: Meridian Retail Group — checkout and order-processing service
skill_file: .claude/skills/security/SKILL.md
date: 2026-07-06
status: complete
---

# Module 900 — Final Kata Brief
## Threat-modeling role-agent: Meridian checkout service

Prepared by: security skill invocation (by-hand run, 2026-07-06)

---

## What was built

A Claude Code Skill — `.claude/skills/security/SKILL.md` — that turns a solution description
into a first-pass threat model without a blank-page start. It automates the K 9.W.1 → K 9.W.3
chain (DFD → STRIDE → scored register) and hands the K 9.W.4–9.W.5 work (mitigation design,
control implementation, risk sign-off) back to a human every time.

---

## Nine-step completion evidence

| Step | What was done | Evidence |
|------|--------------|----------|
| 1 — Name + shape | **Skill** chosen (team reaches for the DFD + STRIDE + L×I playbook during threat models; scope is K 9.W.1–9.W.3 only). Name: `threat-modeling-checkout` | `name:` field in SKILL.md |
| 2 — Description | Names input files, output files by path, and ends with a NOT clause (not for mitigation, controls, or risk sign-off) | `description:` field; passes 3/3 routing test |
| 3 — Role / Goal / Inputs / Tools | One-sentence goal; every output named by exact path; tool allowlist (read_document, mermaid_render, write_artifact); platform pointer to REFERENCE.md | Body of SKILL.md |
| 4 — Decision rules | 6 DO/DON'T rows (all with counts or yes/no tests); Escalate-never-decide list (5 items); Governance-policy-scope line; 5 stop-and-ask conditions with measurable triggers; rules live inline inside chain markers | `## Decision rules` block in SKILL.md |
| 5 — Eval table | 3 rows; each names a test input by path and a counted or structural pass/fail signal | `How to check it's working` table in SKILL.md |
| 6 — Routing test | 3/3: tasks 1 and 2 matched correctly; task 3 (control implementation) correctly rejected and routed to Ops/Engineering | Run-log, routing section |
| 7 — Real run | Happy-path: `900-wide/00-assets.md` → `00-dfd.mmd` + `01-threats.md` + `02-risks.csv` (12 threats; 2 Critical/25; 0 unmapped; trifecta partial flag). Hard question: "sign off the residual risk" → escalated with five-field contract; did not sign | Run-log, happy-path + hard-input rows |
| 8 — One fix | Tightened L×I DO row from adjective ("extreme values") to counted rule ("≥2 extreme scores per axis, Likelihood 1–2 or 4–5; Impact 1–2 or 4–5"); re-run passed with 0 undifferentiated 3×3 rows | Run-log, changed + re-run rows |
| 9 — Run-log | Pasted in full at the end of SKILL.md | `## Run-log` section |

---

## Artefact chain produced (K 9.W.1 → K 9.W.5)

| Artefact | Kata | Status |
|----------|------|--------|
| `900-wide/00-dfd.mmd` + `00-dfd.md` | K 9.W.1 (companion) | complete |
| `900-wide/00-assets.md` | K 9.W.1 | complete |
| `900-wide/01-threats.md` | K 9.W.2 | complete |
| `900-wide/02-risks.csv` | K 9.W.3 | complete |
| `900-wide/03-mitigation.md` | K 9.W.4 | complete |
| `900-wide/04-evidence.md` + `search_validator.py` | K 9.W.5 | complete |
| `.claude/skills/security/SKILL.md` | K 9.3 Final Kata | complete |

---

## Done-when checklist

- [x] `description` gets picked correctly for 3/3 tasks in a fresh session (Step 6)
- [x] Agent produced DFD + STRIDE list + scored register from one real input with no hand-fixing (Step 7)
- [x] At least one check-row was run against a named input, with a counted/structural verdict (Steps 5 + 7)
- [x] Hard question (risk sign-off) was refused/escalated — guardrail fired (Step 7)
- [x] One fix recorded with before/after (Step 8)
- [x] A teammate who never took this module could run it after one read (SKILL.md is self-contained)
- [x] Every input came from one source — Meridian checkout service (Reference Case A)
- [x] Run-log pasted in SKILL.md (Step 9)

---

## Human-owned decisions (never decided by the agent)

The following calls were surfaced and escalated throughout the kata chain — none were decided by the agent:

| Call | Where escalated |
|------|----------------|
| Residual-risk acceptance for T-05 SQL injection (named owner + expiry) | `03-mitigation.md` + SKILL.md hard-input test |
| Kill-switch ownership for the availability assistant | Not in scope v1; flagged in K 9.W.4 for v2 |
| Autonomy-tier classification of the availability assistant | v1 is prediction-only (assisted); v2 reserve-and-hold would require T2/T3 classification by human |
| EU AI Act Article 6 / Annex III tier | Not classified — flagged as requiring governance intake before v2 ships |
