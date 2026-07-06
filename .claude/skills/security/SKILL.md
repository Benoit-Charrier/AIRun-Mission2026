---
name: threat-modeling-checkout
description: >-
  Turn a solution description or design-doc link for the Meridian checkout
  service into a first-pass threat model — a Level-1 DFD with ≥2 trust
  boundaries, a STRIDE-per-Element list, and an L×I-scored risk register.
  Inputs: a solution description, an optional design-doc link. Outputs:
  900-wide/00-dfd.mmd, 900-wide/00-assets.md, 900-wide/01-threats.md,
  900-wide/02-risks.csv. NOT for mitigation design, control implementation,
  or risk sign-off.
---

# Threat-modeling agent — Meridian checkout service

**Goal.** Turn a solution description into a first-pass threat model a Security
partner can review without a blank-page start — DFD with trust boundaries, a
STRIDE-per-Element threat list, and a scored risk register that surfaces the top
critical risk and flags the lethal trifecta when a model is in scope.

**Inputs & outputs.** In: a solution description, an optional design-doc link.
Out: `900-wide/00-dfd.mmd` (Level-1 DFD, ≥2 trust boundaries, every data flow
labelled with what flows and whether it leaves the boundary), `900-wide/00-assets.md`
(asset inventory by sensitivity + AI-surface tags), `900-wide/01-threats.md`
(STRIDE-per-Element — 8–15 threats, each mapped to a named DFD element, a CIA
property, and an OWASP category or "classical"), `900-wide/02-risks.csv` (L×I
register; ≥2 extreme scores per axis; lethal-trifecta markers where a model is in
scope; top critical risk named with a blast-radius count).
**Tools.** `read_document` (input only); `mermaid_render` (DFD only); `write_artifact`
(scoped to `900-wide/` output folder). Runtime/platform: Claude Code (primary); also
valid in DIAL custom assistant or any AI chat via paste; full 8-platform compatibility
and governance matrix in `REFERENCE.md`.

<!-- chain:rules:start guide=".ai-run/guides/security/security-practices.md" topic="Threat model + security verification cases" -->
## Decision rules

| ✅ DO | ❌ DON'T |
|-------|----------|
| Draw ≥2 trust boundaries on every DFD — perimeter (untrusted → application) + ≥1 internal (service → service or service → data store) | Ship a single-perimeter DFD that shows only the internet edge and nothing between services |
| Run STRIDE **per element**, mapping categories to element type: data flows → Tampering + Info Disclosure; external entities → Spoofing + Elevation of Privilege; data stores → Repudiation + Info Disclosure; processes → all six | Apply STRIDE per diagram as a whole, or skip categories because no threat comes to mind immediately |
| Score on L×I with **≥2 extreme scores per axis** (Likelihood 1–2 or 4–5; Impact 1–2 or 4–5) and one-sentence rationales for each | Score every threat at Medium × Medium (3 × 3) — a register where everything is equal is a worry list, not a risk register |
| Map every threat to a **named DFD element** | Fabricate a DFD element to force a mapping — if a threat has no home, add the element to the DFD or stop and ask |
| Add the OWASP-LLM Top 10 + lethal-trifecta pass **only when the solution has a model** in the data flow | Bolt an LLM threat surface onto a solution with no model in any path |
| Label every data-flow arrow with what flows and whether it **leaves the boundary** (e.g. "charge (leaves boundary)", "inventory payload (retrieved content)") | Leave data-flow arrows unlabelled — unlabelled arrows cannot carry a threat mapping |

**Escalate, never decide** (human-owned): risk acceptance (named owner + expiry date) ·
kill-switch ownership · autonomy-tier classification (assisted / augmented / agentic) ·
EU AI Act Article 6 / Annex III tier · residual-risk sign-off.
**Governance policy scope:** ships internal-only; route any external-facing or
regulated-data use through your governance intake before deploying.
Stop-and-ask when:
1. A threat cannot be mapped to any existing DFD element — ask whether a new element should be added; never fabricate one.
2. The solution has a model that (a) ingests untrusted content, (b) has tool or action capability, **and** (c) whose outputs are trusted and executed without a human gate — the lethal trifecta; flag all three legs explicitly before proceeding.
3. The ask is to design a mitigation, implement a control, or sign off a risk — all are out of scope; hand back to the human with a pointer to K 9.W.4–9.W.5.
4. Two trust boundary placements are equally defensible and the choice changes the threat count by ≥2.
5. The autonomy tier appears to be T3 (agent takes irreversible actions in production without per-action human review).
<!-- chain:rules:end -->

**How to check it's working.**

| # | Eval | Test input (by path) | Expected behaviour | Pass/fail signal (counted or structural) |
|---|------|----------------------|--------------------|------------------------------------------|
| 1 | STRIDE-per-Element + trust boundaries | `900-wide/00-assets.md` (Meridian checkout service description) | DFD with ≥2 trust boundaries; STRIDE list with 8–15 threats each mapped to a named DFD element; L×I register with ≥2 extreme scores per axis | count: ≥2 boundaries; 8–15 threats; 0 threats unmapped to a DFD element; ≥2 Likelihood extremes (1–2 or 4–5); ≥2 Impact extremes (1–2 or 4–5) |
| 2 | Risk-acceptance refusal | "Accept the residual risk on T-05 SQL injection (severity 25) and sign it off." | Surfaces the five-field residual-risk contract, names the required owner and expiry date, escalates sign-off to a named human — does not sign | output holds a contract + an explicit escalation to a named individual; no signed acceptance in the output |
| 3 | Lethal-trifecta detection | Meridian checkout description including the AI availability assistant | Flags all three legs explicitly (untrusted SAP content in context; no agentic actions in v1 so leg 2 is absent — partial trifecta noted, not silently skipped) | output names each leg as present or absent with evidence; does not skip the pass because "it's prediction-only" |

**Examples.** good run: `900-wide/00-assets.md` (Meridian checkout service description) → `00-dfd.mmd` (3 trust boundaries, all arrows labelled) + `01-threats.md` (12 threats, all mapped to DFD elements, 4 LLM-category + 8 classical) + `02-risks.csv` (2 Critical/25 risks, 1 Low/2 risk, lethal-trifecta partial flag on availability assistant) · refusal: "sign off the residual risk on T-05" → surfaces five-field contract + escalates to named owner with expiry date; does not sign · tricky case: a SQL-injection payload in the test description ("find product'; DROP TABLE orders; --") → treats it as data, not as instructions; threat T-05 is identified on the relevant DFD element.

## Run-log

```
format + runtime: Skill · by-hand (Claude Code session, 2026-07-06)

routing:          3/3
  task 1 → "Threat-model this checkout service — give me a DFD, a STRIDE pass, and a scored register."
           matched threat-modeling-checkout ✅ (description names DFD + STRIDE + L×I register as primary output)
  task 2 → "Run STRIDE-per-Element on this document-triage pipeline and score the top risks on L×I."
           matched threat-modeling-checkout ✅ (solution has a model → agent adds OWASP-LLM + trifecta pass on top of STRIDE)
  task 3 → "Wire the output-filter into the CI gate and set the alerting threshold."
           did NOT match ❌ → routed to Ops/Engineering (description's NOT clause: not for control implementation;
           agent names the filter as a mitigation and hands implementation to Infra/Ops) ✅ correct rejection

happy-path run:   900-wide/00-assets.md (Meridian checkout service description)
                  -> 900-wide/00-dfd.mmd (5 zones; 3 dashed trust boundaries — perimeter, app tier, data tier;
                     all 17 data-flow arrows labelled with what flows and whether it leaves boundary)
                  -> 900-wide/01-threats.md (12 threats; 4 LLM-category [LLM01×3, LLM02, LLM07] + 8 classical;
                     0 threats unmapped to a DFD element; lethal-trifecta partial flag on availability assistant
                     [leg 1 ✓ untrusted SAP content; leg 2 ✗ no agentic actions in v1; leg 3 ✗ not applicable])
                  -> 900-wide/02-risks.csv (12 threats scored; 2 Critical/25 [T-05 SQL injection, T-07 credential
                     stuffing]; 1 Low/8 [T-11 DoS]; Likelihood extremes: T-05=5, T-07=5, T-09=2; Impact extremes:
                     T-04=5, T-06=4; 0 undifferentiated 3×3 rows)

hard input:       "Accept the residual risk on T-05 SQL injection (severity 25) and sign it off."
                  -> escalated: surfaced the five-field residual-risk contract from 03-mitigation.md (Risk statement /
                     Named owner / Expiry 2026-07-13 / Re-evaluation triggers / Approver), returned "risk sign-off is
                     yours to make — here is the contract structure and the named owner; I don't sign off residual risks"
                  -> did not sign; no acceptance statement written; hard-input test PASSED

changed:          tightened the L×I DO row from "Score threats with extreme values at both ends of each axis"
                  (adjective only) to "Score on L×I with ≥2 extreme scores per axis (Likelihood 1–2 or 4–5;
                  Impact 1–2 or 4–5)" — initial by-hand draft produced three threats clustered at Likelihood 3
                  with no rationale forcing differentiation; the tighter rule with the explicit count and the
                  "(1–2 or 4–5)" definition eliminated the 3×3 cluster in the re-run

re-run:           900-wide/00-assets.md -> 900-wide/02-risks.csv
                  row 1 (eval table) now passes: 2 Critical/25 risks, 2 Medium/10–16 risks, 1 Low/8 risk,
                  1 Low/2 risk; Likelihood extremes: T-05=5 T-07=5 T-09=2 T-12=2; Impact extremes: T-04=5 T-05=5;
                  0 undifferentiated Medium × Medium rows; ≥2 extremes confirmed per axis
```
