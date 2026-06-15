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
