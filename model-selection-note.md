# Model Selection Note

**Date:** 2026-06-15
**Author:** Benoit Charrier — DM/PM
**Project:** Meridian Retail Group reference case — weekly executive RAG drafting
**Task:** Draft a weekly RAG status update for Eva Muller from a fixed prompt and input file, then select the better model for this recurring executive-status task.
**Committed location:** c:\Users\Benoit_Charrier\AIRun-Mission2026\curriculum-public\output\model-selection-note.md

---

## Evaluation Criteria

| # | Criterion | Why it matters for this task |
|---|-----------|------------------------------|
| 1 | Executive readability | Eva Muller reads a one-pager and must understand it on first pass without technical translation. |
| 2 | Format compliance | The weekly RAG has a fixed structure, so drift from the template weakens reuse and comparison. |
| 3 | Accuracy | Executive status must stay grounded in the provided facts and must not invent owners, dates, or mitigations. |
| 4 | Conciseness | The document must fit a one-page executive read with no extra framing or repetition. |

---

## Prompt Used

Exact prompt file used on both models, with the same unchanged companion input file `weekly-rag-eva-muller.input.md` in the same folder:

```markdown
---
mode: ask
description: Draft the weekly RAG status update for Eva Müller (VP Digital, MRG sponsor)
---

# Weekly RAG Status — Eva Müller

You are drafting the weekly RAG (Red / Amber / Green) project status update for **Eva Müller, VP Digital and programme sponsor at Meridian Retail Group (MRG)**.

## Eva's communication profile

- Reads a **one-pager**. She will not scroll past the fold.
- Asks **two questions** and decides. Surface only the decisions that genuinely need her.
- **Allergic to jargon.** No acronyms without expansion on first use. No tech stack names unless unavoidable.
- Primary concerns: **board update visibility** and **regional GM resistance**.
- Wants no surprises — flag risks early, even when uncertain.

## Programme context

18-month, $42M omnichannel commerce programme at MRG:
- **Phase 1** — Unified identity + cart + checkout (target GA month 8)
- **Phase 2** — Loyalty + cross-channel inventory (starts month 8)
- **Phase 3** — ML personalisation, marketing automation (starts month 14)
- Three SI partners involved; MRG internal product team is junior and learning alongside delivery.
- Key risks to surface: store POS continuity, regional compliance (GDPR/PCI-DSS), regional GM buy-in.

---

## Input

Read all input data from **`weekly-rag-eva-muller.input.md`** (same folder as this prompt). Do not ask for input — it is already provided in that file.

The input file contains:
1. **Overall programme RAG** — 🟢 Green / 🟡 Amber / 🔴 Red with one-sentence rationale.
2. **Workstream statuses** — per workstream RAG + one-line summary.
3. **Key events this week** — decisions, milestones, incidents, stakeholder meetings.
4. **Top risks or blockers** — what could escalate in the next two weeks.
5. **Decisions needed from Eva** — genuine escalations only.
6. **Next week's focus** — two or three bullets.

*If a field is missing or marked TBD in the input file, carry it through as TBD — do not invent values.*

---

## Output format

Produce a single markdown document formatted as a **one-page weekly status**. Sections:

``` 
# Weekly Programme Status — [DATE]
**Programme:** MRG Omnichannel Commerce  
**Reported by:** [NAME]  
**Overall status:** 🟢 / 🟡 / 🔴 [one sentence]

---

## Workstream status

| Workstream | Status | This week | Next step |
|---|---|---|---|
| ... | 🟢/🟡/🔴 | ... | ... |

---

## Risks & blockers

| Risk | Impact | Owner | Mitigation |
|---|---|---|---|
| ... | High/Med/Low | ... | ... |

---

## Decisions needed from Eva Müller

1. [Decision — context — recommended action — deadline]

*No decisions needed this week.* ← use this if none

---

## Next week

- ...
- ...
- ...
```

**Quality criteria — in priority order:**

1. **Executive readability:** Eva reads a one-pager and asks two questions. Every sentence must be intelligible to a non-technical VP on first read. No acronyms without expansion. No tech stack names unless unavoidable. Short, declarative sentences — no hedging ("it appears", "there may be").
2. **Format compliance:** Use the exact template structure below. Every section present, every table column populated, RAG emoji on every workstream row. No extra sections, no prose where a table is specified.
3. **Accuracy:** Every claim traces to input provided. Do not invent numbers, dates, or statuses. If information is missing, write TBD — never guess.
4. **Conciseness:** Every word must earn its place. Workstream summaries: max 8 words. Risk descriptions: one clause. Decisions: one sentence of context + one of recommendation. If the whole document exceeds one printed page, cut until it fits.
```

---

## Output Comparison

### Model A: Claude Sonnet 4.6
> Overall status: Amber — Identity integration at risk; all other workstreams on track.
> 
> Unified Identity — Legal sign-off on consent flow pending
> 
> Italian payment compliance (PSD2/SCA) has no workstream owner. Recommend assigning to SI partner given regulatory complexity.

### Model B: GPT-5.4
> **Overall status:** 🟡 Phase 1 remains on schedule, but identity sign-off risk could delay release.
> 
> | Unified Identity | 🟡 | Privacy approval blocking identity setup | Secure legal sign-off |
> 
> 1. Assign ownership of the Italy payment compliance gap before next sprint planning in 3 days.

---

## Scorecard

| Criterion | Model A score (1–3) | Model A evidence | Model B score (1–3) | Model B evidence |
|-----------|---------------------|------------------|---------------------|------------------|
| Executive readability | 2 | The rendered page is easy to scan, but terms like "general availability," "parallel-path," and "PSD2/SCA" reduce clarity for a non-technical VP. | 3 | The status, tables, and decision are written in short, plain language that an executive can understand on first read. |
| Format compliance | 2 | It includes all required sections and table columns, but it does not follow the requested template exactly because it replaces the explicit overall-status line with a custom banner and adds extra presentation elements. | 3 | It preserves the requested structure exactly with the required title, status line, section order, tables, and next-step list. |
| Accuracy | 2 | Most content matches the input, but it adds unsupported specifics such as recommending the SI partner as owner and introducing mitigation details not present in the source. | 3 | The content stays close to the provided input, preserves the stated risks and decision, and does not introduce unsupported numbers or ownership decisions. |
| Conciseness | 2 | The rendered content is fairly compact, but extra labels, footer metadata, and richer wording make it less tight than necessary for a one-page executive update. | 3 | Each section is stripped to the minimum needed to communicate status, risk, decision, and next steps without repetition. |
| **Total** | **8** |  | **12** |  |

---

## Decision

**Selected model:** GPT-5.4

**Rationale:** GPT-5.4 wins because it performed better on the highest-priority criterion, executive readability, while also scoring higher on format compliance, accuracy, and conciseness. It stayed closer to the exact brief and source evidence. Claude Sonnet 4.6's main shortcoming on this task was constraint drift: it optimized for a more polished artifact and added unsupported detail instead of staying inside the narrow executive template.

---

## Active Constraint

**What could change this decision within 30 days:** If the task shifts from strict executive one-pagers to richer stakeholder-ready HTML presentation, Claude Sonnet 4.6 may become more competitive despite losing on this constrained status format.

---

## Revision history

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-06-15 | Initial commit |