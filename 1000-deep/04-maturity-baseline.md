---
kata: K 10.D.5
artefact: 1000-deep/04-maturity-baseline.md
consumes_from: 00-project-context.md, 03-command-center.md
engagement: ERP-modernization — EU industrial-machinery manufacturer
date: 2026-07-08
status: complete
---

# AI-SDLC Maturity Baseline — ERP Modernization Engagement

*Scored against the AI-SDLC Maturity Framework (L0–L3 rubric). A score is a profile across all five dimensions — AI Capabilities, Reusability, AI Champions, Performance Tracking, DAU — not a single number. Weak phases are linked directly to the project outcomes at risk.*

---

## Five-Dimension Breakdown

*Each cell is scored independently against the AI-SDLC Maturity Framework rubric. Read down a column to see the full profile for a phase; read across a row to see where a dimension is consistently weak across all phases.*

| Dimension | Intake | Plan | Build | Validate | Handoff | Learn |
|-----------|:------:|:----:|:-----:|:--------:|:-------:|:-----:|
| **AI Capabilities** | L0 | L1 | L2 | L1 | L1 | L1 |
| **Reusability** | L0 | L1 | L2 | L1 | L0 | L1 |
| **AI Champions** | L0 | L1 | L1 | L1 | L0 | L1 |
| **Performance Tracking** | L0 | L0 | L1 | L0 | L0 | L0 |
| **DAU** | L0 | L1 | L2 | L1 | L0 | L1 |

**Dimension scoring rationale:**

| Dimension | Score reasoning |
|-----------|----------------|
| AI Capabilities | Intake: zero AI use. Plan/Validate/Learn/Handoff: L1 — assisted only; output not reviewed or verified; results vary. Build: L2 — `rules/` repo + tech-lead verified PR review; >50% of core deliverables made AND verified. |
| Reusability | Intake: zero prompts or shared tooling. Plan/Validate/Learn: L1 — prompts in shared drive/folder but siloed; individuals use their own copies; onboarding not updated. Build: L2 — `rules/` repo reused team-wide across every PR; standard enforced by CI. Handoff: L0 — no shared process, no decision log, nothing reused. |
| AI Champions | Intake/Handoff: L0 — no AI use means no enthusiast even at sporadic level. Plan/Validate/Learn: L1 — one or more engineers act as sporadic enthusiasts (BA drafts stories, QA shares prompts, delivery lead uses AI at retros) but no mandate, no protected time, no designation. Build: L1 — tech lead is a de facto champion (owns `rules/` repo) but the role is informal; no designation or protected time. |
| Performance Tracking | Build: L1 — lint CI provides a partial signal (artefact-based, not productivity-metric); anecdotal evidence only; no metric defined and measured consistently. All other phases: L0 — nothing tracked; no standard metric exists. |
| DAU | Intake/Handoff: L0 — no AI use. Plan/Validate/Learn: L1 — occasional use; well below 70% of sessions. Build: L2 — majority of sprints use AI on every PR (lint + review); DAU >70% for the Build workstream. |

**Cross-cutting pattern:** Performance Tracking is L0 or L1 everywhere — the engagement has no shared AI productivity metric at all. AI Champions never reach L2 — no phase has a formally designated champion with protected time. These two dimensions are the weakest across the board and are the primary targets for the 90-day plan.

---

## Baseline Table

*Score profile notation: Cap · Reu · Champ · Perf · DAU (in dimension order above). Where all five are the same level, a single value is shown.*

| SDLC Phase | Score profile (Cap · Reu · Champ · Perf · DAU) | Evidence statement | Weak / Strong signal | Project outcome affected | First adoption hypothesis |
|-----------|------------------------------------------------|--------------------|---------------------|--------------------------|--------------------------|
| **Intake** | **L0** (all five) | Opportunity triage lives in email threads; no AI-assisted qualification memo has been produced; source links absent from every summary | Weak — no AI use observed on any dimension; process is manual and undocumented | Scope stability: mid-flight scope surprises because qualification gaps are not surfaced before SOW signature | Use AI-assisted qualification memo with source-linked triage; if 3/3 summaries carry source links and unplanned scope changes ≤2 per month, scope stability improves |
| **Plan** | **L1 · L1 · L1 · L0 · L1** | Story-drafting notes exist in a shared drive folder; ACs are drafted manually; no AI-reviewed AC has been merged; no standard template | Weak — AI is used occasionally but output is not reviewed or verified; Performance Tracking at L0: no metric exists | Delivery predictability: incomplete or ambiguous ACs cause rework mid-sprint and inflate cycle time | Add BA-reviewed AI-drafted ACs as a required step; if ≥80% of stories carry reviewed ACs by sprint 3, rework rate falls |
| **Build** | **L2 · L2 · L1 · L1 · L2** | `rules/` repo exists in version control; PR comments reference AI review; tech lead verifies flagged changes; CI runs lint | Strong on Capabilities / Reusability / DAU — AI use is consistent and verified. Weak on Champions (no designation) and Performance Tracking (lint is anecdotal, not a productivity metric) | Cycle time and quality: Build is the strongest phase; risk is score drift if the tech lead changes or the `rules/` repo is not maintained | Standardise rule-file lint as a CI gate and designate the tech lead as a formal champion; if lint = 0 for 4 consecutive weeks and the role is protected, the Build standard is self-enforcing |
| **Validate** | **L1 · L1 · L1 · L0 · L1** | Test prompts exist in a shared folder; no golden set defined; AI-generated tests not reviewed by QA lead before merge; coverage metric is inflated | Weak — AI is used for test generation but output is unverified; shared folder has no owner; Performance Tracking at L0 | Defect escape: unreviewed AI tests inflate coverage numbers without testing critical paths; escaped defects carry client reputation risk | Add an eval/golden-set gate and designate a QA champion to maintain it; if golden-set pass rate ≥90% at sprint 6, defect escape rate falls toward target ≤3 |
| **Handoff** | **L1 · L0 · L0 · L0 · L0** | Release decisions live in chat messages; no decision log exists; owner, rationale, and rejected options are absent; decisions are frequently reopened | Weak — only AI Capabilities reaches L1 (occasional AI-assisted release-note writing); all other dimensions at L0; this is the most fragile profile in the engagement | Go-live readiness: reopened decisions cause rework in the final two months and push the compliance sign-off date; directly threatens M8 | Add Decision Memory completeness gate and a delivery champion to own it; if 100% of release decisions are logged and reopens ≤1 per month, go-live confusion falls |
| **Learn** | **L1 · L1 · L1 · L0 · L1** | Retro decks exist in a shared drive; insights are not actioned in a trackable way; no retro output is committed to a repo; improvement items decay between sprints | Weak — retrospectives happen but produce no artefact; Performance Tracking at L0: improvement items are never measured to closure | Continuous improvement: without a tracked improvement backlog, delivery quality does not improve sprint-over-sprint; accumulated technical and process debt is invisible | Turn the retro into a repo artefact and an improvement backlog item; if ≥1 actionable item per retro is tracked to closure, the team builds a continuous improvement signal |

---

## Two Weakest Phases

**1. Intake (L0)** — the only phase with no AI use at all. Every later phase inherits whatever scope confusion goes unresolved here. Improving Intake from L0 to L1 is the lowest-cost, highest-leverage move available.

**2. Handoff (L1 · L0 · L0 · L0 · L0)** — the most fragile profile in the engagement: only AI Capabilities reaches L1; Reusability, Champions, Performance Tracking, and DAU are all L0. All release decisions live in chat. This is the most direct threat to M8 (go-live) and to the compliance sign-off chain. Improving Handoff from L1 to L2 (Decision Memory completeness gate) is the highest-urgency move given the 12-month deadline.

---

## Notes on Build (L2)

Build at L2 is genuine — evidence is strong. The risk is not the current score but score drift if the tech lead changes or the `rules/` repo is not maintained. The 90-day plan targets L3 (rule-file lint in CI, automated improvement loop) — that target is achievable because the L2 foundation is solid.
