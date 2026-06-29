# 08-pre-mortem-uc3

Date: 2026-06-24
Case: Case A - Meridian Retail
Artifact reviewed: `07-deck-uc3.md`
Review mode: Fresh-session skeptical board pre-mortem

## Top-3 weaknesses (ranked)

1. **Unverified ROI foundation** (High)
- Why this kills the case: Investment ask and payback rely on unverified assumptions, so finance can block approval.
- Weak slide(s): 5-6
- Patch line: "Before pilot gate, lock internal benchmarks and add +/-30% sensitivity guardrails; if precision <90% or review SLA breaches, rephase spend."

2. **Review bottleneck mitigation is underspecified** (High)
- Why this kills the case: Exception queues can overwhelm review operations at scale, undermining precision and timeline claims.
- Weak slide(s): 4, 7, 8
- Patch line: "Define review capacity model (named roles, throughput, escalation), plus pilot gate checks: queue depth <1 week and SLA attainment >=95%."

3. **Pilot-to-scale gap** (Medium)
- Why this kills the case: Deck asks for pilot funding but lacks explicit gate criteria for scaling across 22 stacks.
- Weak slide(s): 8, 9, 10
- Patch line: "Add phased expansion gates (tier-1, tier-2, regional) with measurable thresholds for duplicate reduction, SLA, and cost-per-ID merged."

## Patched actions applied to deck

- Added ROI benchmark and sensitivity guardrail note to Slide 6 speaker note.
- Added explicit review-capacity and queue/SLA gate note to Slide 7 speaker note.
- Added phased scale-gate criteria to Slide 10 speaker note.

## Result

Deck now addresses the top three likely steering objections and ties pilot approval to measurable go/no-go gates for scale.
