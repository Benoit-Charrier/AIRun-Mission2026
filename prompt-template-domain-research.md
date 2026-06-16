# Prompt Template: Domain Research

**Quick run instruction:** In chat, type `Run prompt domain-research for domain <domain> and process <process area> and save to <output_file_path>`.

**Date:** 2026-06-16
**Author:** Benoit Charrier — DM/PM
**Project:** FDE Program — Week 2 domain orientation prior
**Model:** GPT-5.4 via GitHub Copilot Chat
**DIAL location:** My Files/AIRun-Mission2026/prompt-template-domain-research.md
**Committed location:** https://github.com/Benoit-Charrier/AIRun-Mission2026/blob/94ca45a9de2f3eef33e71932594283ca274d71d2/prompt-template-domain-research.md
c:\Users\Benoit_Charrier\AIRun-Mission2026\Output\prompt-domain-research.md

---

## Purpose

This prompt produces a budgeted pre-scenario domain orientation brief for an FDE so they can enter discovery with a grounded view of workflow shape, compliance boundaries, and likely agent opportunities.

---

## Variable Placeholders

| Placeholder            | Description                                                                                       | Example value                                                                      |
| ---------------------- | ------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `{{domain}}`           | The business domain to research before reading the scenario in detail.                            | omnichannel retail commerce                                                        |
| `{{process_area}}`     | Optional narrower slice of the domain when the assignment is more specific than the domain label. | unified customer identity, cart, and checkout across web, mobile, and in-store POS |
| `{{output_file_path}}` | Where the generated artifact should be saved in the working repository.                           | domain_research.md                                                                 |

---

## Output Format Instruction

Return a markdown document only. Follow the exact section order and headings defined below, including sections `0`, `0b`, `1`, `1a`, `1b`, `1c`, `2`, `3`, `3a`, `3b`, `4`, `5`, and `6`. Keep the total length to roughly 2-3 pages. Use markdown tables where specified, numbered lists where specified, and blockquote formatting for cognitive hotspots, gaps, hypothesis questions, and assumptions. Do not add a preamble or any extra sections.

---

## Prompt Body

You are an FDE about to assess a business process in a domain you may not know. Before producing any ATX deliverable, you need a working model of the domain: how work typically flows, where judgment and compliance constraints live, and what agentic opportunities tend to emerge. This is a limited orientation activity, not a research project. Keep the output brief, hypothesis-driven, and just detailed enough to support intelligent discovery without bluffing domain knowledge.

This deliverable feeds:
- Discovery synthesis by grounding the lived-process narrative in domain-typical patterns
- Cognitive load map by pre-loading what pause points and judgment calls look like in this domain
- Discovery questions by generating hypothesis questions before the stakeholder call
- All assumption logs by separating what you know about the domain from what the scenario tells you

Save the output as `{{output_file_path}}`.

Your input is:
- Domain: `{{domain}}`
- Process area: `{{process_area}}`

If `{{process_area}}` is blank, treat the task as domain-level research only.

Do not read the scenario before completing sections 1-5. You are building a prior, not a post-hoc analysis.

If ATX reference materials are available, align your terminology and reasoning with them, especially:
- `curriculum-public/modules/100-consulting-sme/atx/atx/skills/atx/references/atx-concepts.md` for cognitive work, lived-vs-documented process, and delegation language
- `curriculum-public/modules/100-consulting-sme/atx/atx/skills/atx/references/atx-assessment.md` for the ATX assessment lens and discovery priorities
- `curriculum-public/modules/100-consulting-sme/atx/atx/skills/atx/references/discovery-questioning-patterns.md` for question framing and ATX-aligned probes

For this prompt, use these ATX dimension definitions:
- **Volume & Time:** case volume, frequency, cycle time, queue pressure, and labor intensity
- **Cognitive Nature:** where judgment, synthesis, pattern recognition, exception handling, and tacit knowledge are required
- **Data & Systems:** how structured the inputs are, how fragmented the systems are, and how accessible the required data is
- **Risk & Compliance:** error consequence, reversibility, regulation, auditability, and approval constraints
- **Organisational:** handoffs, approval chains, stakeholder dependencies, onboarding difficulty, and coordination load

Produce the document using this exact structure:

### 0. Executive summary
Write exactly three bullet points, each one sentence. Cover in order:
1. The domain's core workflow pattern and where skilled human attention is most typically consumed
2. The most important compliance or governance constraint typical to this domain and how it shapes delegation boundaries
3. The highest-leverage hypothesis for agentic opportunity in this domain, and the single biggest unknown that would confirm or disconfirm it

This section must be self-contained.

### 0b. Table of contents
Generate this after the full document is written. List all sections by number and title as markdown anchor links in order. Format each entry as `[N. Section title](#n-section-title)` using lowercase, hyphens for spaces, and no special characters in the anchor. Include subsections indented under their parent.

### 1. Domain overview

#### 1a. What this domain does
Write one paragraph that describes:
- What the domain's core function is
- Who the primary knowledge workers are
- What the primary inputs and outputs are
- Typical volume and cadence in broad orders of magnitude

#### 1b. Typical workflow
Write a numbered list of 5-8 steps from trigger to close. For each step, include one bracketed label from `[execution]`, `[judgment]`, `[coordination]`, or `[verification]`.

Explicitly label this subsection with the sentence: `Domain-typical workflow — client deviations will surface in discovery.`

#### 1c. Common failure modes
List 3-5 things that typically go wrong in this domain. For each, classify it as process failure, data failure, judgment failure, or coordination failure.

### 2. Regulatory and compliance context
Create a markdown table with these columns:

| Framework / Constraint | What it governs | Agent design implication |
|---|---|---|

At minimum, address:
- Any data protection or privacy regulation relevant to the data types in this domain
- Any audit trail or sign-off requirement
- Any sector-specific regulation that creates hard stops where AI cannot act without human review

If the domain has no significant regulatory constraints, state that explicitly and explain why.

### 3. Cognitive work patterns typical to this domain

#### 3a. Where skilled attention is typically consumed
List 3-4 cognitive hotspots. For each, use this exact format:

> **Cognitive hotspot [CH-N]:** [specific moment in the workflow]
> **Cognitive type:** decision-making / synthesis / pattern recognition / exception handling
> **Why it resists simple automation:** [specific reason]
> **What would make it delegatable:** [condition under which an agent could handle it]

#### 3b. Lived vs. documented gaps typical to this domain
Describe 2-3 ways real work diverges from documented process using this exact format:

> **Gap [G-N]:** [what the SOP says vs. what typically happens]
> **Why it exists:** [structural reason]
> **Agent design implication:** [how this gap affects an SOP-derived agent]

### 4. ATX dimension pre-assessment
Create a markdown table with these columns:

| ATX Dimension | Domain-typical signal | What to probe in discovery |
|---|---|---|
| **Volume & Time** | | |
| **Cognitive Nature** | | |
| **Data & Systems** | | |
| **Risk & Compliance** | | |
| **Organisational** | | |

Below the table, add one paragraph identifying the ATX dimension you expect to be most constraining for agent design and why.

### 5. Hypothesis questions for discovery
Generate at least 10 concrete hypothesis questions. For each, use this exact format:

> **HQ-[N]: [the question]**
> **Hypothesis being tested:** [current belief]
> **If confirmed:** [design implication]
> **If disconfirmed:** [what changes]

Draw the questions from:
- Domain standards and typical processes
- Compliance and regulatory frameworks
- ATX dimension mapping across volume, cognitive nature, data, risk, and organisational factors

When generating these questions, prefer the ATX-style discovery lens from the reference materials: ask questions that expose lived work, cognitive hotspots, exception patterns, data fragmentation, compliance boundaries, and delegation breakpoints.

### 6. Assumption log
Log every non-universal claim made in sections 1-5. Include at least 4 assumptions, and include every numeric estimate. Use this exact format:

> **Assumption [A-N]:** [domain-typical baseline]
> **Why it matters:** [affected deliverable or design choice]
> **If wrong:** [how the prior changes]
> **Confidence:** low / medium / high
> **How to validate:** [discovery question or artifact request]

Constraints and acceptance rules:
- Complete sections 1-5 before using any scenario details
- Describe the cognitive shape of work, not just the org chart
- For every regulation listed, state the agent design implication
- Provide at least 3 cognitive hotspots and at least 2 lived-vs-documented gaps
- Identify the most constraining ATX dimension with reasoning
- Provide at least 10 hypothesis questions with testable hypotheses and design forks
- Keep an assumption log with at least 4 entries, including all numeric estimates
- Keep the final length within 2-3 pages

Do not produce these failure modes:
- A domain overview that only describes the org chart
- A regulatory section that lists frameworks without design implications
- Cognitive hotspots that say only that something is complex
- Hypothesis questions without a named hypothesis
- Assumption log entries for universally true statements
- A document longer than 3 pages

---

## Test Run (Author)

**Input values used:**
- `{{domain}}` = omnichannel retail commerce
- `{{process_area}}` = unified customer identity, cart, and checkout across web, mobile, and in-store POS
- `{{output_file_path}}` = domain_research.md

**Output quality:** Usable as-is for a teammate-run domain orientation prompt; revised once to make the section structure and failure constraints explicit.

---

## Peer Review

**Reviewer:** Pending teammate review
**Date reviewed:** Pending
**Model used by reviewer:** Pending

**Reviewer input values used:**
- `{{domain}}` = Pending
- `{{process_area}}` = Pending

| Review question | Reviewer answer |
|---|---|
| Could you run the template without asking the author anything? | Pending |
| Was the output format what you expected? | Pending |
| Would you use this template on your own work? | Pending |
| One concrete improvement suggestion | Pending |

---

## Revision History

| Version | Date | Change | Author |
|---|---|---|---|
| 1.0 | 2026-06-16 | Initial prompt-template draft created from Week 2 domain research task prompt | Benoit Charrier |
| 1.1 | Pending | Post-review update | Benoit Charrier |