# 1000 Assessment

**Date:** 2026-07-07

---

## Sprint throughput up 15%, change-failure rate up 8%

**What the combination indicates**

The two metrics are moving in opposite directions on the quality axis. Throughput up 15% means more work is completing each sprint; change-failure rate up 8% means a larger fraction of what ships is causing failures or incidents in production. Together they describe a team that is going faster by skipping something — test coverage, review rigour, acceptance-criteria completeness, or some combination. The velocity gain is partly fictitious: the 8% increase in failures generates incident response, hotfixes, and rework that will consume future sprint capacity but does not appear as a throughput deduction in the current window.

**Why it is a risk signal, not a success signal**

In the DORA model, elite performers have high deployment frequency *and* low change-failure rate. The two should move together or the high throughput decouples from delivery quality. When CFR rises alongside throughput, the team is not accelerating toward elite performance — it is trading tomorrow's stability for today's velocity numbers. Each percentage point increase in CFR has a compounding cost: incidents consume senior engineers, erode customer trust, and push teams toward change-freeze habits that collapse throughput in the next quarter. The 15% throughput gain is real only if it survives the rework load that the 8% CFR increase will create.

**What to investigate before concluding the team has reached L2 on AI Capabilities**

1. **AI-output correlation with failures.** Are the stories that failed in production disproportionately the ones written or scaffolded with AI assistance? If yes, the throughput increase is coming from AI-generated code that is not being validated to the same standard as hand-written code — the speed gain is a quality transfer, not a genuine capability uplift.
2. **Test coverage delta.** Has test coverage held flat, risen, or fallen over the same quarter? A throughput increase that is accompanied by a coverage decline is a reliability debt instrument, not an L2 signal.
3. **Review cycle time.** Are pull-request review times shortening in line with the throughput increase? If reviews are getting shorter while failure rates rise, the acceleration is coming from reduced scrutiny of AI suggestions, not from genuine efficiency.
4. **CFR distribution.** Is the 8% increase clustered on a small number of high-impact incidents or spread across many low-impact ones? A cluster points to a systemic gap in one workflow stage; a spread points to a degraded quality baseline across the board.
5. **L2 repeatability evidence.** L2 on AI Capabilities means the practices are repeatable across multiple sprints and feature types — not a good quarter followed by a bad one. Before signing off L2, you need at least two consecutive quarters where throughput improvements are accompanied by stable or improving CFR, not a single quarter showing one metric up and the other also up.

---

## Three staffing variants that cost different totals but staff the same roles at the same ramp

**Why it is a failed variant set**

If three variants staff the same roles at the same ramp pace, they deliver the same outcome at the same speed and the same risk profile. The only variable is the price. That is a quotation exercise — three bids for an identical scope — not a variant set. A decision-maker looking at these three options cannot make a strategic bet: they can only pick the cheapest version of the same thing. The variants offer no real choice about what to trade.

The structural failure is that the variants share all three load-bearing dimensions simultaneously — cost, speed, and risk are all fixed at the same level. A genuine variant set requires at least one of those dimensions to differ materially, and the difference must cascade into the others. Changing the rate card while keeping roles and ramp identical moves only one number on the cost line without changing what the client is actually buying.

**What makes a variant a genuine cost / speed / risk bet**

A genuine variant is defined by a *different ramp profile, role mix, or scope phasing* — not by a different total. Each of the following produces a real variant:

- **Ramp profile:** Variant A staffs a full team from week 1 (highest burn rate early, fastest path to delivery, least resilience to scope change). Variant B ramps to full team over eight weeks (lower early cost, more time to validate requirements before full commitment, higher risk if the delayed ramp creates a scheduling crunch). The trade is explicit: speed versus adaptability.
- **Role mix:** Variant A uses a senior-heavy team (higher day rate, faster execution, lower management overhead). Variant B uses a pyramid with juniors supported by leads (lower blended rate, longer delivery, higher dependency on knowledge transfer quality). Variant C uses an AI-augmented smaller team (lower headcount, faster for well-defined work, higher dependency on toolchain maturity and prompt-engineering discipline). Each mix has a different failure mode, not just a different invoice.
- **Scope phasing:** Variant A delivers full scope in six months. Variant B delivers an MVP in three months with a priced option to extend. Variant C delivers via two gates with a go/no-go checkpoint after gate one. The trade is certainty versus optionality: the client pays more per feature in Variant C to preserve the right to stop.

The test for any variant: can the client look at it and immediately name what they are giving up in exchange for what they are gaining? If the answer is only "I am paying less," the variant is not a variant.

---

## All-L2 baseline across all six SDLC phases

**Why uniform L2 should increase scepticism**

Real teams do not mature uniformly across phases. The skills, incentives, tooling, and feedback loops are different for planning, coding, testing, integration, deployment, and monitoring. A team that has invested heavily in AI-assisted code generation will typically show stronger maturity in the coding phase than in deployment or monitoring, where the investment has not yet landed. An all-L2 baseline is statistically unlikely for any team that has been assessed independently on each phase — it is the signature of anchoring, averaging, or social pressure rather than independent evaluation.

Three specific failure modes produce an all-L2 result:

1. **Anchoring to the safe middle.** L2 is the "not embarrassing, not implausible" score. An assessor working under time pressure, or a team under pressure to look competent, will converge on L2 for ambiguous phases rather than defend an L1 or L3 verdict. The uniformity is the tell.
2. **Shared evidence applied across phases.** If the assessor used a single piece of evidence — "the team uses Copilot on 60% of stories" — as proof of maturity for planning, coding, testing, and review simultaneously, the grades are not independent assessments; they are the same grade applied to four phases with different labels.
3. **Masking by averaging.** A team that is genuinely L3 on coding and L1 on production monitoring averages to L2. The average is technically accurate and completely misleading. The L1 monitoring phase is the active risk; the L3 coding phase is not the story. An all-L2 baseline hides this asymmetry and produces a remediation plan that treats every phase as equally mature, which means the L1 phase gets under-resourced.

**Evidence required before signing off any single phase at L2**

L2 means the practice is *repeatable* — it happened consistently across multiple delivery cycles, not just once or on a specific project.

| Evidence type | What it must show |
|---------------|------------------|
| **Phase-specific artefacts** | Evidence tied to that phase only, not reused across phases. For coding: PR history showing AI-assisted commits with review outcomes over ≥2 sprints. For testing: AI-generated test coverage reports showing coverage held or improved. For deployment: pipeline logs showing AI-assisted change scoring applied consistently. |
| **Metric corroboration** | The team's own DORA or equivalent metrics for that phase must be consistent with L2. A team claiming L2 deployment maturity with a 20% change-failure rate cannot be signed off — the number contradicts the level. |
| **Repeatability window** | Minimum two consecutive sprints or delivery cycles where the practice was applied without being prompted or reviewed. One observed instance is L1 with a good day, not L2. |
| **Counter-evidence check** | Active search for disconfirming signals: scope churn rate for planning, defect escape rate for testing, incident frequency for deployment. If any counter-signal contradicts the claimed level, the phase is not signed off until it is explained. |
| **Assessment independence** | Who scored it and how. Self-assessment with no external benchmark is the weakest form. Before signing off any phase at L2, require either a peer review by someone outside the team or a comparison against a named external benchmark. An all-L2 self-assessment with no independent verification is not signable. |
