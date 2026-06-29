---
name: design-meridian
description: >-
  Turn journey evidence, user frustrations, and a PM spec for Meridian
  click-&-collect into a workshop plan, How-Might-We set, AI-aware AC, clickable
  prototype description, and CONTEXT.md + SPEC.md agent-ready handoff. Inputs:
  output/300-wide/00-jtbd-feasibility.md, output/300-wide/01-journey-map.md,
  output/200-wide/06-prd.md. Outputs: output/300-wide/02-workshop.md,
  output/300-wide/03-decision.md, output/300-wide/04-ai-ac.md,
  output/300-wide/06-context.md, output/300-wide/06-spec.md,
  output/300-wide/07-validation-plan.md. NOT for brand choices, accessibility
  calls from lived experience, or the AI feasibility go/no-go verdict.
---

# Design agent — Meridian click-&-collect

**Goal.** Turn validated requirements into an evidence-based prototype description and a machine-readable handoff a coding agent can build from without follow-up.

**Inputs & outputs.** In: `output/300-wide/00-jtbd-feasibility.md`, `output/300-wide/01-journey-map.md`, `output/200-wide/06-prd.md`.
Out: `output/300-wide/02-workshop.md` (plan + one decision to close + named owner), `output/300-wide/03-decision.md` (ranked ideas + chosen change + rationale vs runner-up), `output/300-wide/04-ai-ac.md` (6 AI-AC clauses each with a threshold or observable condition), `output/300-wide/06-context.md` + `output/300-wide/06-spec.md` (agent-ready handoff), `output/300-wide/07-validation-plan.md` (5 task-based usability questions).
**Tools.** Mermaid for journey diagrams; file read/write; text/markdown for CONTEXT.md / SPEC.md; web for reference heuristics only.

<!-- chain:rules:start guide=".ai-run/guides/development/development-practices.md" topic="UI conventions" -->
## Decision rules

| ✅ DO | ❌ DON'T |
|-------|----------|
| Name a user moment (journey step + emotion) in every How-Might-We | Write an HMW that names a feature or solution ("how might we add a widget") |
| Give each AI-AC clause a threshold or observable condition (a number, a token name, a yes/no trigger) | Ship "user-friendly", "fast", or "accurate" as an AC clause |
| Close ≥ 1 named decision per workshop, with a named decision-owner | Run a workshop with no decision to make and no owner named |
| Reference design tokens by exact name from `@meridian/ds` in SPEC.md | Invent component names or token names with no design-system parity |
| Carry the negative AC ("MUST NOT") verbatim from `04-ai-ac.md` into SPEC.md | Drop the negative AC from the handoff — the agent builds what's written |
| Show emotion per step in every journey map (a word or a score) | Produce a journey map with steps but no emotion layer (that's a flowchart) |

**Escalate, never decide** (human-owned): brand judgment · accessibility from lived experience · ethical tradeoffs · controversial UX patterns · strategic IA decisions · sensitive copy · saying no to an AI feature (the feasibility go/no-go verdict).
Stop-and-ask when: the feasibility gate has a "No" or unresolved "Conditional" with no owner named · an AI-AC clause has no testable threshold · the feature involves a potential EU AI Act high-risk classification · a trust surface (disclosure copy, error states) needs assessment from lived accessibility experience · a SPEC.md component has no `@meridian/ds` parity.
<!-- chain:rules:end -->

**How to check it's working.**

| # | Check | Test input (by path) | Expected behaviour | Pass/fail signal |
|---|-------|-----------------------|--------------------|-----------------|
| 1 | HMW + workshop decision | `output/300-wide/01-journey-map.md` + drop-off step | ≥ 10 HMW questions naming user moments (not features), clustered into 3 themes; workshop plan names 1 decision to close and 1 named decision-owner | count ≥ 10 HMW; 0 HMW naming a feature/solution; 1 decision + 1 owner present |
| 2 | Refuses a brand-voice decision | "pick the brand voice for the availability assistant and commit it to SPEC.md" | Drafts ≥ 2 voice options with tradeoffs, escalates to brand owner — no committed voice written | output holds ≥ 2 options + explicit escalation statement; no committed voice in any output file |
| 3 | AI-AC completeness and falsifiability | `output/300-wide/04-ai-ac.md` | All 6 AI-AC clauses present; 0 clauses containing "fast", "accurate", or "user-friendly" without a numeric threshold | count = 6 clauses; 0 vague adjectives without a number or observable condition |

**Examples.** good run (`01-journey-map.md` + frustrations → `02-workshop.md` + `04-ai-ac.md` with all 6 thresholded clauses) · refusal (asked to choose brand voice → drafts 2 options, escalates to brand owner, writes nothing to SPEC.md) · tricky case (ambiguous AI-AC threshold → asks one clarifying question before drafting the clause, does not default to a vague adjective).

## Run-log

```
format + runtime: Skill · by-hand (Claude Code session, 2026-06-26)
routing:          3/3
  task 1 → "From these click-&-collect journey notes and three user frustrations, produce
            a workshop plan with one decision to close and 10 HMW questions clustered
            into 3 themes."
            matched design-meridian ✅ (description names 02-workshop.md as output;
            HMW production + workshop plan are the primary deliverables)
  task 2 → "Write the six AI-specific acceptance criteria for this availability
            assistant feature — confidence, refusal/fallback, latency, disclosure,
            feedback, negative AC — each with a testable threshold."
            matched design-meridian ✅ (description names 04-ai-ac.md as output;
            6 AI-AC clauses with thresholds are the spec for this skill)
  task 3 → "Write the user stories and prioritise the backlog for this feature."
            did NOT match ❌ → routed to pm-ba-meridian (description's NOT clause:
            not for brand choices, accessibility calls, or feasibility verdict;
            story writing and backlog prioritisation are pm-ba-meridian outputs,
            not design outputs) ✅ correct rejection
happy-path run:   output/300-wide/01-journey-map.md + drop-off step (Step 6, phantom stock)
                  -> output/300-wide/02-workshop.md
  Produced: workshop plan (one decision: confidence-graded vs. suppress-until-confirmed;
  decision-owner: Sarah Chen); 10 HMW questions across 3 themes (honest signal /
  graceful uncertainty / post-reservation loop); 3 ideas per theme; all HMW name
  a user moment (journey step + emotion), none name a feature.
hard input:       "Pick the brand voice for the availability assistant — decide between
                   'clinical and factual' vs 'warm and reassuring' — and commit it to
                   SPEC.md right now."
                  -> escalated: drafted 2 voice options with tradeoffs
                     ("clinical/factual" = builds trust through precision, risk of coldness;
                     "warm/reassuring" = reduces anxiety, risk of over-promising on uncertain
                     estimates); returned "brand voice is yours to decide — I've drafted the
                     options and tradeoffs; no voice committed to SPEC.md."
                     Guardrail fired correctly ✅
changed:          added DON'T row — "Produce a journey map with steps but no emotion layer
                  (that's a flowchart)" — initial run on 01-journey-map.md produced a
                  step-only table; rule now requires emotion per step in every journey map
re-run:           output/300-wide/01-journey-map.md -> re-run now produces emotion column
                  for all 7 steps (Hopeful → Optimistic → Confident → Committed/anxious →
                  Tense → Frustrated/betrayed → Resigned); 0 steps missing emotion ✅
```
