---
kata: K 10.W.4
consumes_from: K 10.W.3 (02-solution.md), M400 architecture record, M500 engineering evidence chain, M700 data product, M800 platform artefact
source_draft: curriculum-public/modules/1000-management/artefacts/1000-wide/_fallbacks/10.W.4.draft.md
date: 2026-07-07
artefact: 1000-wide/03-staffing.md
note: Markdown stand-in for 03-staffing.xlsx. Tabs rendered as sections.
---

# Staffing Variants — MRG AI-Enabled Omnichannel Commerce Platform

---

## Diagnosis of the Provided Draft

The provided draft (10.W.4.draft.md) presents three variants — Lean (8 FTE), Balanced (12 FTE), Fast (16 FTE). All three share the same defects:

| Defect | Detail |
|--------|--------|
| Identical role mix | Each variant lists the same proportional role breakdown — e.g. 2 leads, 4 engineers, 1 BA, 1 QA — scaled by headcount. No variant changes *which* roles or *what level* is staffed. |
| 100% on-shore | All three variants assume 100% UK/Italy on-shore staffing. There is no blended delivery model. This removes the cost/speed lever entirely and inflates cost across all three variants. |
| Month-1 full productivity | The draft assumes every FTE is at 100% utilisation from day 1. Ramp-up (onboarding, environment access, context-building) is not modelled. |
| Bet differs only in headcount | The "lean" bet is described as "we use fewer people." The "fast" bet is "we use more people." Neither changes ramp curve, on/near/offshore mix, or role seniority profile — so there is no real cost/speed/risk trade. |

The three variants pass the form check (three tabs, role rows, FTE-month totals) but fail the content check: a decision-maker looking at them can only pick the cheapest version of the same plan.

---

## Repaired Variant A — Lean

**Bet:** Optimise for cost; accept a slower ramp, higher dependency-wait risk, and lower on-shore coverage. Blended 20% on-shore Italy / 80% near-shore Poland.

**Trade-off:** Lowest burn rate in months 1–3; higher coordination overhead; Phase 1 go-live risk increases if SAP API access is delayed (smaller team has less capacity to absorb a 2-week slip without pushing go-live).

**Ramp profile:** 30% month 1 → 60% month 2 → 90% month 3 → 100% month 4+

| Role | Level | Shore | M1 | M2 | M3 | M4 | M5 | M6+ | FTE-months |
|------|-------|-------|----|----|----|----|----|----|-----------|
| Delivery manager | Senior | On-shore IT | 0.3 | 0.6 | 1.0 | 1.0 | 1.0 | 1.0 | 5.9 |
| Solution architect | Senior | On-shore IT | 0.3 | 0.6 | 1.0 | 0.5 | 0.5 | 0.5 | 3.4 |
| Backend engineer | Mid | Near-shore PL | 0.3 | 0.6 | 1.0 | 1.0 | 1.0 | 1.0 | 4.9 (×2 = 9.8) |
| Frontend/mobile engineer | Mid | Near-shore PL | 0.3 | 0.6 | 1.0 | 1.0 | 1.0 | 1.0 | 4.9 |
| QA engineer | Mid | Near-shore PL | 0.3 | 0.6 | 1.0 | 1.0 | 1.0 | 0.5 | 4.4 |
| Data engineer | Mid | Near-shore PL | 0.0 | 0.3 | 0.6 | 1.0 | 1.0 | 0.5 | 3.4 |
| BA | Mid | Near-shore PL | 0.3 | 0.6 | 1.0 | 0.5 | 0.0 | 0.0 | 2.4 |
| **Peak FTE** | | | **1.8** | **3.9** | **7.6** | **7.0** | **6.5** | **5.5** | |
| **Total FTE-months** | | | | | | | | | **~34** |

**Timeline impact:** Slower ramp adds ~3 weeks to Phase 1 go-live vs balanced; estimated go-live 2026-11-21 unless SAP scope is clean and ramp accelerates from month 2.

---

## Repaired Variant B — Balanced *(Recommended)*

**Bet:** Optimise for predictable delivery at moderate cost. Blended 40% on-shore Italy / 60% near-shore Poland. Higher on-shore presence improves SAP integration speed and MRG stakeholder alignment.

**Trade-off:** Mid-range burn rate; lower SAP-scope risk than lean; delivers on the 2026-10-31 Phase 1 commitment with manageable contingency.

**Ramp profile:** 50% month 1 → 80% month 2 → 100% month 3+

| Role | Level | Shore | M1 | M2 | M3 | M4 | M5 | M6+ | FTE-months |
|------|-------|-------|----|----|----|----|----|----|-----------|
| Delivery manager | Senior | On-shore IT | 0.5 | 0.8 | 1.0 | 1.0 | 1.0 | 1.0 | 5.3 |
| Solution architect | Senior | On-shore IT | 0.5 | 1.0 | 1.0 | 0.5 | 0.5 | 0.5 | 4.0 |
| Backend engineer | Senior | On-shore IT | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 5.5 |
| Backend engineer | Mid | Near-shore PL | 0.5 | 0.8 | 1.0 | 1.0 | 1.0 | 1.0 | 5.3 (×2 = 10.6) |
| Frontend/mobile engineer | Mid | Near-shore PL | 0.5 | 0.8 | 1.0 | 1.0 | 1.0 | 1.0 | 5.3 |
| QA engineer | Mid | Near-shore PL | 0.5 | 0.8 | 1.0 | 1.0 | 1.0 | 0.5 | 4.8 |
| Data engineer | Senior | On-shore IT | 0.0 | 0.5 | 1.0 | 1.0 | 1.0 | 0.5 | 4.0 |
| Security engineer | Senior | On-shore IT | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.0 | 2.5 |
| BA | Mid | Near-shore PL | 0.5 | 0.8 | 1.0 | 0.5 | 0.0 | 0.0 | 2.8 |
| **Peak FTE** | | | **5.0** | **7.0** | **9.5** | **8.5** | **8.0** | **6.5** | |
| **Total FTE-months** | | | | | | | | | **~44** |

**Timeline impact:** On-track for Phase 1 go-live 2026-10-31 and Phase 3 go-live 2027-01-31 under standard assumptions.

---

## Repaired Variant C — Fast

**Bet:** Optimise for time-to-market; accept higher burn and earlier senior commitment. 70% on-shore Italy/UK, 30% near-shore Poland. Senior-heavy front-loading reduces SAP-scope risk and accelerates Phase 1 by ~2 weeks.

**Trade-off:** Highest day-rate burn in months 1–3; Phase 1 go-live possible by 2026-10-17 (2 weeks early); higher risk if scope changes materially in the first sprint (senior capacity is committed and not easily redeployed).

**Ramp profile:** 80% month 1 → 100% month 2+

| Role | Level | Shore | M1 | M2 | M3 | M4 | M5 | M6+ | FTE-months |
|------|-------|-------|----|----|----|----|----|----|-----------|
| Delivery manager | Senior | On-shore IT | 0.8 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 5.8 |
| Solution architect | Lead | On-shore IT | 0.8 | 1.0 | 1.0 | 0.5 | 0.5 | 0.5 | 4.3 |
| Backend engineer | Senior | On-shore IT | 0.8 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 5.8 (×2 = 11.6) |
| Backend engineer | Mid | Near-shore PL | 0.8 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 5.8 |
| Frontend/mobile engineer | Senior | On-shore UK | 0.8 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 5.8 |
| QA engineer | Senior | On-shore IT | 0.8 | 1.0 | 1.0 | 1.0 | 1.0 | 0.5 | 5.3 |
| Data engineer | Senior | On-shore IT | 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0.5 | 5.0 |
| Security engineer | Lead | On-shore IT | 0.8 | 1.0 | 1.0 | 1.0 | 0.5 | 0.0 | 4.3 |
| BA | Senior | On-shore IT | 0.8 | 1.0 | 1.0 | 0.5 | 0.0 | 0.0 | 3.3 |
| DevOps / SRE | Senior | On-shore IT | 0.0 | 0.5 | 1.0 | 1.0 | 1.0 | 0.5 | 4.0 |
| **Peak FTE** | | | **7.9** | **10.5** | **10.5** | **9.0** | **8.0** | **6.0** | |
| **Total FTE-months** | | | | | | | | | **~55** |

**Timeline impact:** Phase 1 go-live potentially 2 weeks early (2026-10-17); however, fast-ramp senior cost is ~30% higher in blended day-rate vs balanced. If scope is well-defined, this is a defensible premium. If SAP scope expands, the senior team has capacity to absorb it without a delivery slip — but budget exposure increases.

---

## Summary Comparison

| Dimension | Lean | Balanced | Fast |
|-----------|------|----------|------|
| Peak FTE | ~8 | ~10 | ~12 |
| Total FTE-months | ~34 | ~44 | ~55 |
| On-shore mix | 20% | 40% | 70% |
| Ramp curve | 30/60/90/100% | 50/80/100% | 80/100% |
| Phase 1 go-live | 2026-11-21 (risk) | 2026-10-31 (target) | 2026-10-17 (early) |
| SAP-scope risk tolerance | Low | Medium | High |
| Best commercial fit | T&M or hybrid cap | Fixed Phase 1+2 | Fixed Phase 1, hybrid Phase 2+ |

---

## Recommendation

**Balanced variant (Variant B).**

The balanced variant is the only one that reliably delivers Phase 1 on the contracted date (2026-10-31) while keeping the blended cost within a fixed-price margin. The lean variant saves cost but introduces unacceptable Phase 1 timeline risk given the undocumented SAP integration scope. The fast variant accelerates delivery but at a day-rate premium that the fixed-price commitment cannot absorb without compressing margin below acceptable thresholds.

The balanced variant's 40% on-shore presence provides the SAP integration speed and MRG stakeholder alignment that the engagement needs in months 1–3, while the 60% near-shore mix keeps the blended rate competitive for the Phase 2–3 work, which is more execution-heavy and less investigative.
