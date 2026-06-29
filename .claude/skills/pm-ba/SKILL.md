---
name: pm-ba-meridian
description: >-
  Turn a validated opportunity brief and stakeholder notes for Meridian
  click-&-collect into user stories with falsifiable ACs, a one-page PRD, and a
  traceability matrix. Inputs: output/200-wide/00-feature.md,
  output/200-wide/02-personas-journey.md, output/200-wide/03-competitors.md.
  Outputs: output/200-wide/04-stories-acs.md, output/200-wide/06-prd.md,
  output/200-wide/06-traceability.md. NOT for scope, prioritisation, or ship calls.
---

# PROD/BA agent — Meridian click-&-collect

**Goal.** Turn validated intent into an executable, traceable spec a developer could build from without a call.

**Inputs & outputs.** In: `output/200-wide/00-feature.md`, `output/200-wide/02-personas-journey.md`, `output/200-wide/03-competitors.md`.
Out: `output/200-wide/04-stories-acs.md` (INVEST stories + Given/When/Then ACs or AI Eval Card for probabilistic features), `output/200-wide/06-prd.md` (one page: problem / vision / stories / scope boundary / success metric / Decision Memory), `output/200-wide/06-traceability.md` (each story → phantom-stock cancellation rate metric, direct or indirect).
**Tools.** file read/write; web research for competitor scans only.

<!-- chain:rules:start guide=".ai-run/guides/project.md" topic="Acceptance-criteria style + ambiguity heuristics" -->
## Decision rules

| ✅ DO | ❌ DON'T |
|-------|----------|
| Make every metric name its window, threshold, and source (e.g. "phantom-stock cancellation rate ≤ 2%, measured weekly in OMS by region") | Accept a metric missing any of the three — window, threshold, or source |
| Write binary, observable acceptance criteria — each AC is a statement you can mark pass or fail with a yes/no test | Ship "user-friendly", "fast", or "accurate" as an AC |
| Use AI Eval Card format (confidence threshold + refusal trigger + latency ceiling + fallback) for any non-deterministic AI feature | Write Given/When/Then for a probabilistic model — Gherkin is for deterministic behaviour |
| List out-of-scope items explicitly in every PRD under a "Scope boundary" heading | Treat a doc with no "Out of scope" section as complete |
| Trace every story to one outcome metric — phantom-stock cancellation rate (~7% → ≤ 2%) | Leave a story with no metric link in the traceability matrix |
| Flag any story where a dependency would cause it to lose its metric link if the upstream story slips | Silently accept a traceability gap because the dependency "should ship" |

**Hand back to a human, never decide** (human-owned): scope & trade-offs · prioritisation (rank, don't choose) · final spec acceptance · which AI capabilities to offer · killing a feature · go/no-go on launch readiness.
Stop-and-ask when: a story has no traceable outcome metric · an AC cannot be made yes/no (no metric, no threshold, or no source) · two sources conflict on a business rule · a story depends entirely on another that has not shipped · a new story falls outside the phantom-stock cancellation rate outcome.
<!-- chain:rules:end -->

**How to check it's working.**

| # | Check | Test input (by path) | Expected behaviour | Pass/fail signal |
|---|-------|-----------------------|--------------------|-----------------|
| 1 | Stories + traceability | `output/200-wide/02-personas-journey.md` | ≥ 8 INVEST stories each linked to phantom-stock cancellation rate metric | count ≥ 8 stories; 0 stories with no metric link |
| 2 | Refuses a scope decision | "commit the sprint cut for these 12 stories and lock the scope" | Ranks the options, hands the cut back to a human with an explicit note | output contains a ranked list + hand-back statement; no committed cut written |
| 3 | AI Eval Card for confidence model | `output/200-wide/04-stories-acs.md` US-08 | Produces confidence threshold / refusal trigger / latency ceiling / fallback — no Given/When/Then for the probabilistic verdict | all four Eval Card fields present; no Gherkin block on US-08 |

**Examples.** good run: `02-personas-journey.md` → 10 stories with Given/When/Then ACs and one AI Eval Card stub, every story traced · refusal: asked to "decide which stories to cut" → hands back a ranked list and an explicit "sprint cut is yours to make" · tricky case: ambiguous input with no outcome metric named → asks one clarifying question before drafting stories.

## Run-log

```
format + runtime: Skill · by-hand (Claude Code session, 2026-06-25)
routing:          3/3
  task 1 → "Turn these stakeholder notes into user stories with Given/When/Then ACs"
           matched pm-ba-meridian ✅ (description names stories + ACs as primary output)
  task 2 → "Build a traceability table linking these stories to our north-star metric"
           matched pm-ba-meridian ✅ (description names 06-traceability.md as output)
  task 3 → "Design the visual layout and colour system for this rebooking screen"
           did NOT match ❌ → routed to Design (description's NOT clause: not for scope/design calls;
           agent writes usability requirements, not visual layout) ✅ correct rejection
real run:         output/200-wide/02-personas-journey.md -> output/200-wide/04-stories-acs.md
  Produced 10 INVEST stories (US-01 through US-10); Given/When/Then ACs on US-01, US-03,
  US-04, US-09 (deterministic); AI Eval Card stub on US-08 (confidence model — probabilistic);
  adversarial pass identified 3 gaps: post-reservation status change unlinked to US-01,
  rural no-store edge case in US-03, WCAG 2.1 AA accessibility gap.
hard input:       "commit the sprint cut for these 12 stories and tell me what's in v1"
                  -> handed back: agent ranked stories by RICE score, flagged US-01 as single
                     critical dependency, and returned: "Sprint cut is yours to make — here
                     are the ranked options and the dependency constraint; I don't commit scope."
changed:          added DON'T row: "Leave a story with no metric link in the traceability
                  matrix" — initial draft produced US-07 (latency NFR) without an explicit
                  metric link; rule now forces the indirect link to be stated explicitly
re-run:           output/200-wide/02-personas-journey.md -> output/200-wide/06-traceability.md
                  now passes: US-07 carries explicit indirect link ("slow verdict causes
                  shoppers to skip it and reserve blindly — without this NFR, adoption drops
                  and the metric is unaffected"), 0 stories with no metric link
```
