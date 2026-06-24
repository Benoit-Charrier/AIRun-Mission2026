# Maturity Gap Analysis

**Date:** 2026-06-17
**Author:** Benoit Charrier — DM/PM
**Project:** Meridian Retail Group — Omnichannel Commerce Platform (Reference Case A)
**Committed location:** [Repo path — update on commit]

---

## Scorecard

| Dimension | Level (L1 / L2 / L3) | Score (1.0 / 2.0 / 3.0) | Evidence (2–3 sentences) |
|---|---|---|---|
| AI Capabilities | L1 | 1.0 | The case description contains no mention of AI tooling, AI-assisted workflows, or agent usage across the ~80-person delivery team. Current pain points — phantom stock, fragmented loyalty accounts, mobile app crashes — are described as operational problems with no AI-assisted resolution noted. |
| Reusability | L1 | 1.0 | The case description contains no mention of shared AI tooling, reused context, or AI artifacts across the delivery team or SI partners. |
| AI Champions | L1 | 1.0 | The case describes the internal MRG product team as "junior and learning the platform alongside delivery," and lists no AI mandate across three SI partners. |
| Performance Tracking | L1 | 1.0 | The case includes operational metrics (7% click & collect cancellation rate, 40-minute Black Friday outage) but none related to AI productivity or cost. |
| DAU | L1 | 1.0 | The team section describes ~80 people across six product squads, a BA cell, QA chapter, and architecture team — no AI tools mentioned in the workflow. |
| **Average** | | **1.0** | |
| **Overall Level** | L1 | | 1.0–1.9 = L1 |

---

## Gap Analysis

### Gap 1

**Dimension:** AI Capabilities
**Current level:** L1
**Why this gap is most damaging:** Without AI-assisted delivery, knowledge transfer between three SI partners and a junior MRG internal team relies entirely on manual documentation, creating a handover risk the 18-month timeline cannot absorb.
**Root cause:** There is no AI tooling mandate or delivery standard at the program level, so teams default to non-AI workflows.

---

### Gap 2

**Dimension:** AI Champions
**Current level:** L1
**Why this gap is most damaging:** Without a Champion mandate, no one is accountable for AI tooling decisions across three SI partners, so inconsistent practices compound across 22 countries and six product squads.
**Root cause:** Management has not mandated the need for AI Champions across the program or its SI partners.

---

## 30-Day Improvement Plan

### Step 1 — addresses Gap 1

| Field | Value |
|---|---|
| **Action** | Run a 30-day AI-assisted delivery pilot in 2 squads on 2 recurring tasks (story-to-acceptance-criteria drafting and test-case generation), and publish the shared prompt templates in the team repository. |
| **Owner** | Lena Park |
| **Timeline** | 2026-07-17 |
| **Success metric** | At least 2 prompt templates committed, at least 3 teammates use them, and at least 10 pilot outputs are produced in repo history. |

---

### Step 2 — addresses Gap 2

| Field | Value |
|---|---|
| **Action** | Nominate and announce 1 AI Champion per SI plus 1 MRG Champion, define responsibilities, and start a weekly 30-minute Champion sync for adoption blockers and standards. |
| **Owner** | Lena Park |
| **Timeline** | 2026-07-01 |
| **Success metric** | 4 named Champions documented, 4 weekly syncs held, and at least 1 adoption update posted per week to the shared team channel or repo notes. |

---

## Peer Review

**Reviewer:** Dmytro Polkovnykov — Solution Architect
**Date reviewed:** 2026-06-19
**Model used by reviewer:** Claude Sonnet 4.6 (via Claude Code)

| Review question | Reviewer answer |
|---|---|
| Is the evidence for each dimension specific and observable — not aspirational? | Partially — Performance Tracking and AI Champions cite concrete observable facts from the case; AI Capabilities, Reusability, and DAU rely on "case description contains no mention of X," which is absence of evidence rather than an observed team behaviour, and does not satisfy the kata's standard of "specific, observable facts from your project." |
| Which score do you challenge, and why? | **AI Capabilities — challenge the evidence, not the level.** L1 is almost certainly correct, but "no mention in a case document" can only confirm L1 in a reference case scenario, not a real project. In a live engagement, a team that simply never documented its AI usage could be scored L1 by this method when it is actually L2. The artefact should note this limitation explicitly so anyone consuming it downstream knows the evidence is case-description-derived, not field-observed. |
| Is each root cause a structural/behavioural cause — not a symptom? | No for Gap 1 — "The program was scoped for platform consolidation, not AI-assisted delivery" is a historical scoping decision, not a structural or behavioural cause; it explains the context but not why the gap would persist if scoping were revisited. A root cause here would be: "There is no AI delivery standard or tooling mandate at the program level, so teams default to non-AI workflows by default." Gap 2's root cause ("Management has not mandated AI Champions") is structural and passes. |
| Are the success metrics measurable without asking the author? | Yes — both metrics contain specific numbers (≥2 templates, ≥3 teammates, ≥10 outputs; 4 Champions, 4 syncs, ≥1 update/week) that a teammate can verify independently from repo history and meeting records. |
| Would you sign off on this plan as a teammate? | Yes, with one revision required: Gap 1's root cause must be rewritten as a structural/behavioural cause before version 1.1 is committed, per the kata's explicit failure-mode rule. |

**Issues found during review:**

1. **Evidence methodology (affects AI Capabilities, Reusability, DAU).** Three of five evidence cells are grounded in "case description contains no mention of…" rather than observed team behaviour. This is valid for a reference-case run but must be flagged as a limitation — downstream modules consuming this baseline should know it is case-document-derived, not discovery-validated.

2. **Gap 1 root cause is a historical constraint, not a structural cause.** "The program was scoped for platform consolidation" describes why AI was never introduced; it does not explain the structural mechanism that would prevent introduction now. Rewrite to name the missing structure (e.g., no AI tooling mandate, no delivery standard referencing AI practices).

3. **Lena Park is not a named character in Reference Case A.** Both improvement plan steps list Lena Park as owner, but this name does not appear anywhere in the Meridian Retail case description. Either the author should name a role that exists in the case (e.g., "Program Delivery Lead") or explicitly note that Lena Park is a fictional stand-in for the purpose of the exercise. As written, a teammate reading the artefact cannot identify who owns these actions.

---

## Revision History

| Version | Date | Change | Author |
|---|---|---|---|
| 1.0 | 2026-06-17 | Initial commit — scorecard complete | Benoit Charrier |
| 1.1 | 2026-06-19 | Peer review completed by Dmytro Polkovnykov | Dmytro Polkovnykov |
| 1.2 | 2026-06-23 | Gap 1 root cause rewritten as structural cause | Benoit Charrier |
