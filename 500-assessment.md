# 500 — Wide Theory Assessment

## Three context layers and their primary staleness risks

**Hot layer** — the always-loaded rule file (`CLAUDE.md`). Every session reads it before touching code.
*Primary staleness risk:* drift from actual conventions. As the codebase evolves, the hot layer is rarely updated, so the AI follows rules that no longer match the repo — wrong folder layout, a removed utility, an outdated linting command. The secondary risk is growth: a hot layer that becomes a stack guide is too large to stay hot and starts crowding out the real session context.

**Warm layer** — on-demand reference material: spec, ADRs, stack docs, NFR budgets.
*Primary staleness risk:* stale contract. A spec or ADR gets updated after sign-off (a scope change, a revised edge case, a superseded decision), but the agent is loaded with the old version. It implements faithfully against a contract the team has already moved past, and the divergence is invisible until review.

**Cold layer** — the gaps note: what the context doesn't cover and the agent cannot see.
*Primary staleness risk:* promoted-but-invisible gaps. A gap stays cold because nobody explicitly promoted it to warm, so the agent fills it from training-data inference rather than project reality. The risk is not that the gap is documented — it is that the cold note is written once and never re-examined, so it describes what was missing at authoring time, not what is missing now.

---

## Five-phase arc of the Deep kata series

| Phase | Artefact produced |
|-------|-------------------|
| **Infrastructure** | `CLAUDE.md` (hot layer rule file) — project context, conventions, utilities, and escalation gates that every subsequent session loads before touching code |
| **Specification** | `spec.md` (signed off) — named acceptance criteria, edge cases, CLI contract, and out-of-scope list that define what "correct" means for the implementation and the tests |
| **Implementation** | `src/logsum.py` — the working code, written against the signed-off spec, with plan approved before execution and deviations logged |
| **Verification** | `tests/test_logsum.py` (isolation tier recorded) + `sessions/<task>/session-log.md` — independent tests generated from spec only, with tier (A/B/C/limited) recorded as an auditable fact; session log documents the context bundle loaded, deviations, and untested items |
| **Delivery** | `reviews/<pr>/review.md` (seven-lens + adversarial) + PR provenance block linking all four artefacts — evidence chain that lets any downstream role reconstruct key decisions without asking the author |

### Two decisions the engineer must make personally

**1. Spec sign-off.**
The engineer must accept the spec as complete and correct before any implementation begins — this decision cannot be delegated to the agent. The spec defines what "correct" means: if the agent interprets the spec and proceeds without human sign-off, its interpretation becomes the ground truth with no external check. Any defect in the spec is invisible to the agent; the agent will implement faithfully against a flawed contract and generate tests that confirm the flawed behaviour. Sign-off is the human checkpoint that breaks the circular evidence chain before it starts.

**2. The merge button.**
The engineer must decide whether the PR is ready to merge — the agent can open a PR, write a review, and flag findings, but it must not press merge. Merge deploys changes to a shared branch or production environment: the consequences (broken builds, data migrations, user-visible regressions) cannot be undone by the agent and fall on the team. An agent that can merge is an agent that can ship defects autonomously. The escalation gate exists because the blast radius of a wrong merge is programme-wide; the blast radius of a wrong spec comment is one conversation.

---

## Two cross-role review lenses

### Behaviour preservation

**What failure class it catches:** *silent regression via clean-looking removal.*

An AI refactor optimises for readability. It removes a guard clause, a default value, or a nested exception path because the surrounding code looks cleaner without it. The removed line carried a spec-required behaviour — an edge case, a fallback, a boundary check — but neither the diff description nor the test suite surfaces the gap. Tests stay green because the removed path was either untested or the AI quietly weakened the assertion to match the new code. The bug ships.

The lens forces the reviewer to read every *removed* line before evaluating what looks better. K 5.W.6 grounded this: the refactor extracted `_update_group` and removed the explicit `if key not in groups` init block — a correct change, but one that had to be checked against the spec's first-seen/last-seen invariant before approving.

### Hidden assumptions

**What failure class it catches:** *blind-spot propagation — a circular evidence chain.*

When tests are written in the same session that produced the implementation, both the code and the tests inherit the same misreading of the spec. The spec says "rows with empty level → `unknown`"; the implementation applies the rule incorrectly; the tests — written from the same mental model — assert the incorrect behaviour. The suite passes with no signal. The evidence chain looks complete: tests written, CI green, PR opened. It is internally circular.

The lens breaks the loop by requiring the test author to hold nothing but the spec — no implementation, no prior session context. K 5.W.4 enforced this with the fresh-session constraint. The isolation tier (A, B, C, limited) written into the session log makes the quality of that separation an auditable fact rather than an assumption, so a reviewer can judge how much weight the test evidence carries.

