---
kata: K 10.W.2
consumes_from: K 10.W.1 (00-rfp.md) + Module 100 Opportunity Brief
date: 2026-07-07
artefact: 1000-wide/01-qualification.md
---

# Qualification Memo — MRG AI-Enabled Omnichannel Commerce Platform

**Bid:** MRG-2026-OCP  
**Buyer:** Meridian Retail Group S.p.A.  
**Prepared by:** Delivery practice lead  
**Date:** 2026-07-07  
**Status:** Bid with conditions (see Recommendation)

---

## 1. Fit Scores

| Dimension | Score (1–5) | Rationale |
|-----------|------------|-----------|
| Capability | 5 | Full-stack commerce delivery, SAP integration track record, AI-SDLC maturity demonstrated through M500–M900 evidence chain (security hardening, threat model, test automation); OWASP-LLM mitigation embedded in delivery process |
| Delivery | 4 | Blended EU delivery model with Italian-market GDPR/PSD2 experience; 12-month fixed-price for a complex SAP integration is at the edge of our comfortable risk envelope — manageable with a scoping sprint pre-contract |
| Commercial | 3 | Fixed-price is our non-preferred model for integrations with undocumented legacy scope; hybrid mitigates this and aligns with C-1; requires negotiation at preferred-supplier stage |
| Strategic | 5 | AI-first omnichannel delivery is a reference case for EPAM's EU retail vertical; the AI availability assistant and DPIA-readiness work directly strengthen the AI governance practice area |

**Composite:** 17/20. Strong technical and strategic fit; commercial risk is the watch item.

---

## 2. Win Themes

| # | Theme | Specific differentiator |
|---|-------|------------------------|
| WT-1 | Pre-built checkout security evidence chain | We carry a live threat model, scored risk register, and control implementation proof (commit SHA) from a checkout system at comparable scale. No competitor can demo this at bid time — they can only promise it. |
| WT-2 | AI governance maturity with DPIA-ready delivery | We have a model registry integration pattern, a prediction-only architectural constraint enforced at the API layer, and OWASP-LLM Top 10 mitigations built into the sprint workflow — meeting EC-4 criteria without additional pre-go-live work. |
| WT-3 | Blended EU delivery at MRG's scale | Near-shore Poland + Italy on-shore presence; Italian retail reference (800-store omnichannel rollout, 2024–2025); GDPR and PSD2 compliance handled in-house without a specialist sub-contractor surcharge. |

---

## 3. Deal-Breaker

**DB-1 — SAP integration scope is undocumented.**  
The current SAP batch-sync behaviour is not documented in the RFP data appendix. A fixed-price commitment on an undocumented integration layer is a liability underwritten by ignorance, not expertise. **Gate condition:** a 2-week paid scoping sprint before contract lock — MRG provides full SAP API access and documentation; EPAM produces a scope baseline and confirms or revises the fixed price. If MRG declines the scoping sprint, we do not bid fixed-price.

---

## 4. Risk Table

| # | Risk | Likelihood (1–5) | Impact (1–5) | Score | Mitigation |
|---|------|-----------------|-------------|-------|------------|
| R-1 | SAP integration scope is larger than RFP implies — undocumented edge cases surface in Phase 1 | 4 | 5 | 20 | Scoping sprint pre-contract; scope capped to documented APIs; change-control clause for undocumented scope |
| R-2 | 12-month deadline aggressive for 1,400-store inventory unification — Phase 3 slips | 3 | 4 | 12 | Phase 1/2/3 go-live gates with independent MRG sign-off; Phase 3 scope reduced to 100-store pilot if deadline is at risk |
| R-3 | MRG DPO DPIA sign-off delayed — AI assistant go-live blocked | 3 | 3 | 9 | DPIA kick-off week 1; DPO minimum 4 h/week committed in contract; 2-week DPO delay = 2-week Phase 2 shift (absorbed within schedule buffer) |

---

## 5. Recommendation

**Bid with conditions.**

Capability and strategic fit are strong (17/20 composite). The two conditions that must be met before the proposal pack is submitted:

1. **Scoping sprint accepted** — MRG must agree in writing to a 2-week paid scoping sprint (from week 1 of engagement) during which SAP API access and documentation are provided and the scope baseline is confirmed. Without this, we convert to a hybrid commercial model with a Phase 1 T&M gate.

2. **DPO availability confirmed** — MRG DPO must commit minimum 4 hours per week to DPIA review in weeks 1–4. If DPO availability is not confirmed before contract signature, Phase 2 go-live is moved to 2027-01-31 and Phase 3 to 2027-02-28.

If both conditions are met: bid fixed-price Phase 1 + Phase 2, T&M cap Phase 3.

---

## 6. Competitive Context

| Likely competitor | Win theme they will hit | Our counter |
|------------------|------------------------|-------------|
| Large SI (incumbent SAP integrator) | "We know your SAP environment" — they will claim integration speed advantage | We counter with delivery quality: evidence pack (M900), AI governance, OWASP compliance. The incumbent knows SAP; we know what breaks SAP in production at scale. |
| AI-native boutique | "AI-first delivery at lower cost" — they will undersell on headcount | We counter with EU compliance credentials and scale evidence. A boutique that hasn't delivered in 1,400 stores carries implementation risk MRG can't absorb on a fixed price. |
