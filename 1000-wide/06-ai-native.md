---
kata: K 10.W.7
consumes_from: K 10.W.2 (01-qualification.md win themes), K 10.W.3 (02-solution.md phases), M500 engineering evidence chain, M600 QA eval pack, M800 platform telemetry
theory_source: curriculum-public/modules/1000-management/1000-wide-theory.md §1.1
date: 2026-07-07
artefact: 1000-wide/06-ai-native.md
---

# AI-Native Delivery Section — MRG AI-Enabled Omnichannel Commerce Platform

---

## Maturity Framework Reference (§1.1)

Targets are grounded in the five-dimension rubric from `1000-wide-theory.md §1.1`. Each row names the primary dimension being measured and uses its threshold — not an invented percentage.

| Dimension | L1 (At Risk) | L2 (Baseline) | L3 (Frontier) |
|-----------|-------------|--------------|--------------|
| AI Capabilities | Assisted — deliverables made with AI help, results vary | Augmented — >50% of core-role deliverables made **and verified** with AI | Agentic — agents handle sub-tasks; new ways of working |
| Reusability | Siloed — local prompts used by individuals | Shared — prompts, rules, context, custom agents reused; onboarding updated | Codified — rules and agents maintained as code; automated improvement loops |
| AI Champions | Sporadic — enthusiasts acting without a mandate | Designated — at least one champion per team | Embedded — all core roles represented; a champions network |
| Performance Tracking | Partial — anecdotal evidence, no standard metrics | Tracked — productivity metrics defined and measured consistently | Governed — AI cost tracked; reviews drive optimisations to output per total cost |
| DAU | Low — occasional use | Majority — >70% DAU | Prevalent — >80% DAU |

*Scale: L0 (not using AI) → L1 → L2 → L3. A score is a profile across all five dimensions, not a single number. Most engagements target L2.*

---

## Per-Phase Maturity Table

| SDLC Phase | Target by | Primary dimension | Adoption metric (with denominator) | Tooling baseline | Key risk |
|-----------|----------|------------------|------------------------------------|-----------------|---------|
| **Intake** | L2 by month 2 | AI Capabilities — >50% of core-role deliverables made AND verified | >50% of user stories have an AI-assisted draft **reviewed and verified** before merge (stories with AI-draft marker reviewed in PR / total stories merged per sprint, from sprint 2) | DIAL (EPAM allow-listed, EU-hosted); Claude for internal-only data (EPAM Data Classification Matrix cleared) | Low-quality story drafts accepted without review → velocity spike masks quality debt; AC completeness drops; CFR rises. *(Note: an 80% target would be L3 DAU territory — the L2 AI Capabilities threshold is >50% made AND verified.)* |
| **Plan** | L2 by month 2 | DAU — >70% of sessions with active AI use | >70% of sprint planning sessions use AI-generated dependency analysis reviewed before sprint kick-off (sessions with AI output in meeting notes / total sprint planning sessions from sprint 3) | DIAL; GitHub Copilot Chat (EPAM allow-listed) | AI dependency graph treated as authoritative without human validation → hidden critical paths not surfaced; phase-gate entry criteria fail |
| **Build** | L2 by month 3 | AI Capabilities + DAU — >50% deliverables made AND verified; >70% DAU | >70% of merged PRs carry an AI-assisted scaffolding commit **with a human review sign-off** (PRs with AI-commit marker AND reviewer approval / total PRs merged per sprint, from sprint 4) | GitHub Copilot (EPAM allow-listed); DIAL for code review prompts | AI-generated code accepted without security review → change-failure rate rises; repeat of throughput↑ + CFR↑ pattern (see 1000-assessment.md Q1). The "AND verified" requirement in AI Capabilities L2 is the guard against this. |
| **Validate** | L2 by month 4 | AI Capabilities — >50% of core-role deliverables made AND verified | >50% of API test cases have AI-generated scaffold **reviewed by QA lead before merge** (AI-generated test files with QA sign-off / total test files at sprint 6 retrospective) | DIAL; GitHub Copilot test-generation; pytest (EPAM allow-listed) | AI-generated tests inflate coverage metric without testing the critical path. *(Note: an 80% target would be L3 DAU territory — L2 AI Capabilities requires >50% made AND verified, not a high volume count.)* |
| **Handoff** | L2 (Champions) by month 5 | AI Champions — designated (≥1 champion per team, with mandate) | 3 of 3 designated MRG Champions operate the AI-assisted runbook workflow without EPAM support (engineers passing KT sign-off / 3 targeted, by week 16). EPAM team Champions dimension already at L2 from month 2 (3 designated, protected time); this row tracks the client-side handoff of that L2 to MRG. | DIAL (MRG internal instance provisioned pre-KT); GitHub Copilot (MRG license obtained ≥4 weeks before KT start) | MRG does not provision AI tooling before KT begins → engineers learn on EPAM tools, not MRG tools; Champion handoff blocked. *(AI Capabilities for MRG engineers will be at L1 at handoff — assisted, results vary — that is expected and honest; the Champions designation is the L2 claim.)* |
| **Learn** | L2 by month 6 | Performance Tracking — metrics defined and measured consistently | ≥1 retro insight per sprint actioned using AI-assisted analysis, with the source metric named (actioned insights from AI-assisted retro / total sprints from month 4; source metric logged in Jira) | DIAL; retrospective AI summariser (EPAM allow-listed internal tool) | AI retro summaries cluster dissenting voices into majority themes → team dysfunction, safety issues, or quality risks masked by aggregation. Performance Tracking L2 requires the metric to be *consistent* — one-off retro use is L1. |

---

## Measurement Plan

| Phase | Source of truth for metric |
|-------|--------------------------|
| Intake | GitHub PR history: story-draft marker in PR description body; tracked by delivery lead at biweekly sprint review |
| Plan | Sprint planning meeting notes in Confluence: AI dependency analysis artefact attached or linked; delivery lead marks session as AI-assisted before sprint kick-off |
| Build | GitHub commit history: `[ai-assisted]` commit tag in message; EPAM delivery lead verifies ≥1 tagged commit per PR |
| Validate | Test file directory in version control: AI-generated test files tagged with `# ai-scaffold` header comment; QA lead counts at sprint 6 retro |
| Handoff | KT session log (Google Doc, shared with MRG ops lead): engineer sign-off column completed without EPAM present; delivery lead witnesses the final KT session |
| Learn | Jira retro board: action-item creation timestamp vs retro close timestamp; EPAM delivery lead exports the report monthly |

---

## What Is NOT Automated — Human-Owned Decisions

The following decisions are never delegated to AI tooling in this engagement. They are owned by named humans and require written sign-off:

| Decision | Human owner | Why it stays human |
|----------|------------|-------------------|
| Acceptance-criteria approval | MRG product owner | AC approval is a contractual commitment to scope; AI-generated AC is a draft input, not the acceptance |
| Client commitments and contract changes | EPAM engagement director + MRG CTO | Commercial commitments carry legal and financial liability |
| Performance conversations and staffing decisions | EPAM delivery lead | People decisions require judgment, context, and accountability that AI tooling cannot provide |
| Residual-risk sign-off | Named risk owner (EPAM engagement director for delivery risks; MRG CTO for platform risks) | Risk acceptance requires a named owner and an expiry date — not an AI recommendation |
| DPIA approval and DPO sign-off | MRG DPO | Regulatory accountability under GDPR Article 35; cannot be delegated |
| AI model classification — prediction-only vs agentic | MRG CTO + EPAM solution architect | Autonomy-tier classification (T1 assisted / T2 augmented / T3 agentic) determines regulatory scope under EU AI Act and EPAM governance policy |
| Phase gate go/no-go | MRG CTO + EPAM engagement director at steering committee | Phase gates trigger payment milestones and scope changes; require human authority |
