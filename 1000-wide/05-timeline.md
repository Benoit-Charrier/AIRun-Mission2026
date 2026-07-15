---
kata: K 10.W.6 (milestone timeline artefact)
consumes_from: K 10.W.6 (05-plan.md milestone table)
date: 2026-07-07
artefact: 1000-wide/05-timeline.md
---

# Milestone Timeline — MRG AI-Enabled Omnichannel Commerce Platform

```mermaid
gantt
    title MRG Omnichannel Commerce Platform — Delivery Timeline
    dateFormat  YYYY-MM-DD
    axisFormat  %b %Y

    section Pre-delivery
    Preferred-supplier notification     :milestone, m_ps, 2026-08-14, 0d
    Contract signature                  :milestone, m0,   2026-08-28, 0d
    Kick-off                            :milestone, m_ko, 2026-09-01, 0d

    section Phase 1 — Checkout + SAP
    Scoping sprint (SAP scope baseline) :active,    p1_scope, 2026-09-01, 14d
    Scoping sprint complete             :milestone, m1,       2026-09-14, 0d
    Phase 1 build + test                :           p1_build, 2026-09-15, 46d
    Phase 1 go-live                     :milestone, m3,       2026-10-31, 0d

    section DPIA / AI Governance
    DPIA co-authorship (DPO 4h/week)    :           dpia_work, 2026-09-01, 44d
    DPIA sign-off                       :milestone, m2,        2026-10-15, 0d

    section Phase 2 — Click-and-Collect + AI Assistant
    Phase 2 build + integration test    :           p2_build,   2026-11-01, 21d
    Pilot env ready (MRG IT — A-4)      :milestone, m3a,        2026-10-01, 0d
    20-store initial pilot              :active,    p2_pilot20, 2026-11-22, 14d
    Initial pilot live                  :milestone, m4a,        2026-11-21, 0d
    Expand to 100 pilot stores          :           p2_pilot100,2026-12-06, 15d
    100-store pilot expansion live      :milestone, m4b,        2026-12-05, 0d
    AI assistant verification (3 weeks) :           p2_ai_ver,  2026-12-06, 21d
    Phase 2 go-live — pilot accepted    :milestone, m4,         2026-12-31, 0d

    section Phase 3 — Full Rollout + KT
    NCC pen-test (2-week window)        :           ncc,      2026-12-15, 14d
    Full 1400-store rollout             :           p3_roll,  2027-01-01, 30d
    Knowledge transfer (3 engineers)    :           p3_kt,    2027-01-01, 30d
    Phase 3 go-live                     :milestone, m5,       2027-01-31, 0d
```

---

## Dependency Notes

| Dependency | From → To | Risk if broken |
|-----------|----------|----------------|
| Scoping sprint → Phase 1 start | M0 (contract) → M1 (scoping complete) | Without scoping sprint, Phase 1 fixed price is ununderwritten; SAP integration scope unknown |
| DPIA sign-off → Phase 2 entry | M2 (DPIA) → M4 (Phase 2 pilot accepted) | AI assistant cannot go live without DPO sign-off; Phase 2 blocked if DPIA delayed |
| Phase 1 go-live → Phase 2 start | M3 → Phase 2 build start | Phase 2 builds on Phase 1 API layer; cannot begin before checkout modernisation is in production |
| Pilot environment ready → 20-store pilot | M3a (MRG IT) → M4a (20-store pilot) | EPAM cannot deploy click-and-collect to stores without MRG IT environment; delay pushes M4a and compresses AI assistant verification window |
| 20-store pilot sign-off → 100-store expansion | M4a → M4b | Blocking defects in the 20-store pilot must be resolved before expanding; skipping this gate risks a rollback across all 100 stores |
| 100-store pilot + AI verification → Phase 2 accepted | M4b + 3-week AI verification → M4 | AI assistant must be verified in production for ≥3 weeks before Phase 2 payment milestone triggers and Phase 3 is authorised |
| NCC pen-test → Phase 3 go-live | NCC 2-week window → M5 | Critical finding adds ≤2 weeks; if finding emerges in week 19, Phase 3 go-live moves to 2027-02-14 (absorbed by contingency) |
| KT (week 12–16) → Phase 3 exit | KT start → M5 | 3 MRG engineers must be released for KT from week 12; late release compresses KT below L2 sign-off threshold |
