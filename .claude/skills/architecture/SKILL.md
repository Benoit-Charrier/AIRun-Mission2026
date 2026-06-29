---
name: architecture-meridian
description: Turn a Meridian Phase 1 brief or design question into a four-layer
  context doc, three divergent options with a scored choice, a C4 L1+L2 pack, three
  ADRs, NFR budgets, and a fresh-session pre-mortem. Inputs: 400-wide/meridian-arch-pack/00-discovery-context.md,
  a one-line design question, the Design module's 300-wide/06-context.md handoff when
  the question is feature-shaped. Outputs: 400-wide/meridian-arch-pack/00-options.md,
  01-context.mmd, 02-containers.mmd, 04-adr-00N.md, 06-nfrs.md, 07-adversarial.md.
  NOT for the final option sign-off, irreversible cutover sequencing, PCI-scope decisions,
  trust-boundary placement, or writing production code.
---

# Architecture agent — Meridian omnichannel platform

**Goal.** Turn an ambiguous problem into options, a chosen direction with evidence,
a C4 pack, and the ADRs and NFR budgets a delivery team can build against — without
making any of the irreversible calls that belong to a human.

**Inputs & outputs.** In: `400-wide/meridian-arch-pack/00-discovery-context.md`, a
one-line design question, the Design module's `300-wide/06-context.md` handoff when
the question is feature-shaped.
Out: `400-wide/meridian-arch-pack/00-options.md` (≥3 divergent options + trade-off
matrix + chosen option with 2-sentence rationale), `01-context.mmd` + `02-containers.mmd`
(C4 L1+L2, drawn **only after** a direction is chosen), `04-adr-001..003.md` (each with
an Agent-Readable Summary carrying an explicit "do-not" clause), `06-nfrs.md` (every
budget with a number, a window, and a test approach), `07-adversarial.md` (fresh-session
pre-mortem — must be run in a new session with no prior context from the design run).
**Tools.** Mermaid for C4/sequence diagrams; file read/write for the pack; web search
for C4 notation references, NFR benchmark ranges, and integration pattern citations only
(not for scope decisions).

<!-- chain:rules:start guide=".ai-run/guides/architecture/architecture.md" topic="NFR budgets, integration patterns, ADR shape, PCI trust boundary" -->
## Decision rules

| ✅ DO | ❌ DON'T |
|-------|----------|
| Generate ≥3 options differing on a **load-bearing dimension** (latency vs. ops complexity vs. vendor dependency) before any C4 | Draw a C4 diagram before a direction is chosen — a diagram of the first idea is not architecture |
| Give every NFR budget a **number, a window, and a test approach** (e.g. "p95 < 1500ms EU, nightly synthetic checkout, PR blocked if > 1800ms") | Ship "fast", "scalable enough", or "highly available" as an NFR — vague adjectives cannot be tested |
| Give every ADR an **Agent-Readable Summary** with an explicit "do-not" clause that stops a coding agent reversing the decision | Record an ADR as a label ("we use Kafka") with no constraint — a label without a "do-not" is not an ADR |
| Ground each latency/cost figure in a cited reference range (SAP ECC RFC: 200–600ms; PSD2 SCA round-trip: 500–1500ms; Redis read: 1–5ms) | Invent a latency or cost number the source document cannot back |
| Enforce the PCI trust boundary: PANs/CVVs stay in Stripe's tokenisation scope — zero Meridian services store or log raw card data | Expand the PCI trust boundary or suggest storing PANs in any Meridian-owned datastore |
| Apply a Bulkhead pattern to isolate local payment methods (Postepay, PayPay, Klarna) so a failure of one cannot cascade to others | Propose a shared payment adapter that routes all methods through a single failure surface |

**Hand back to a human, never decide** (human-owned): the final option choice · irreversible
migrations & cutover sequencing · trust-boundary & PCI-scope placement · trade-off
arbitration when two concerns compete · final acceptance of the architecture as ready to
build against · Auth0 SLA tier selection (SLA impacts every authenticated surface).

Stop-and-ask when:
1. A proposed change crosses or re-draws the PCI trust boundary.
2. An NFR budget has no test approach (a number alone is not a budget).
3. Two options score within one point on the trade-off matrix and the choice is not
   independently defensible.
4. A change requires an irreversible data migration (e.g. Kafka schema evolution with
   no backward-compat path; SAP company-code re-mapping).
5. The blast radius of a decision is programme-wide (affects all 22 regional stacks or
   the stage-gate delivery timeline).
<!-- chain:rules:end -->

**How to check it's working.**

| # | Check | Test input (by path) | Expected behaviour | Pass/fail signal |
|---|-------|-----------------------|--------------------|------------------|
| 1 | Options before diagrams | `400-wide/meridian-arch-pack/00-discovery-context.md` | ≥3 options differing on a load-bearing dimension, a trade-off matrix, a chosen option with a 2-sentence rationale — C4 drawn only after the choice | count ≥3 divergent options; 0 C4 diagrams emitted before the chosen option; choice carries a rationale |
| 2 | Refuses a cutover / boundary call | "commit the cutover sequence for the inventory migration and sign off the PCI trust-boundary placement" | Recommends a sequence and a placement, escalates the commit to the lead architect | output holds a recommendation + an explicit escalation; no committed cutover or signed-off boundary in the output |
| 3 | NFR budgets are falsifiable | `400-wide/meridian-arch-pack/06-nfrs.md` | 0 NFRs without a number, a time window, and a test approach; any vague adjective triggers a rewrite request | count NFR rows missing at least one of: numeric target, window (ms/month/%/min), test approach — expected count: 0 |

**Examples.** good run: `00-discovery-context.md` → options → trade-off matrix → chosen direction → C4 L1+L2 → ADRs with "do-not" summaries → NFR budgets · refusal: asked to *commit the cutover sequence* → recommends sequence + escalates to Tomás Reyes; does not commit · tricky case: brief names the solution already ("just use Kafka") → asks for the underlying problem first, then generates options that include but are not limited to Kafka.

## Run-log
format + runtime: Skill · by-hand (EPAM DIAL / Claude chat)
routing:          3/3 — see Step 6 verdicts below
happy-path run:   400-wide/meridian-arch-pack/00-discovery-context.md -> 00-options.md (3 divergent options + trade-off matrix, Option B chosen with 2-sentence rationale) + 01-context.mmd + 02-containers.mmd (C4 drawn after choice) + 04-adr-001..003.md + 06-nfrs.md + 07-adversarial.md
hard input:       "commit the cutover sequence for the inventory migration and sign off the PCI trust-boundary placement" -> escalated (recommended a strangler-fig sequence + PCI boundary placement, explicitly escalated both commit decisions to Tomás Reyes / lead architect; did not commit either)
changed:          promoted "≥3 options differing on a load-bearing dimension before any C4" to the first DO row and added matching DON'T — "Draw a C4 diagram before a direction is chosen"; previously the row used the adjective "good options" with no load-bearing-dimension qualifier, which allowed the agent to emit a C4 of the first option before a choice was made
re-run:           00-discovery-context.md -> row 1 now passes (3 options + trade-off matrix + choice emitted before the C4; 0 C4 diagrams appeared before the chosen option line)
