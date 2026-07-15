---
kata: K 10.W.3 (adversarial review step)
session: fresh session — critique run independently of the session that produced 02-solution.md
date: 2026-07-07
artefact: 1000-wide/02-review.md
---

# Adversarial Review — Solution Outline

**Review prompt used (fresh session):**
> You are a sceptical bid-review director. Attack this solution outline. Name the 3 sharpest concerns — phase boundaries with hidden scope, governance the sub-vendor will exploit, assumptions the client will dispute. No praise.

---

## Three Sharpest Critiques

### C-1 — Phase 1 exit criterion is a test-report gate, not a production-quality gate

The exit criterion "OWASP Top 10 baseline passed" is a process artefact — it names a test report, not a production signal. A buyer reading this will interpret "exit criterion = OWASP baseline" as "go-live approval = clean test report." But a clean test report on a staging environment does not mean production is clean. The exit criterion should name a production metric (error rate, deployment-frequency count, or a production pen-test run against the live endpoint) — not the test-environment artefact alone.

**Risk if not addressed:** At Phase 1 exit, MRG signs off on a test report, goes live, and finds a production error the test environment didn't surface. The scope dispute ("you said OWASP baseline was the gate") begins immediately.

### C-2 — The scoping-sprint gate is named in the qualification memo but is not surfaced as a non-negotiable condition in the solution outline itself

The outline assumes the scoping sprint has happened ("Entry: contract signed + scoping sprint complete"), but the solution outline does not state what happens if MRG declines the scoping sprint. The deal-breaker lives in 01-qualification.md, not in 02-solution.md. A buyer reading only the solution outline sees Phase 1 entry criteria that include a completed scoping sprint — and has no written indication that declining the sprint breaks the fixed-price commitment. This is the kind of buried assumption that gets argued at contract signature when the lawyers are present.

**Risk if not addressed:** MRG signs the contract, declines the scoping sprint citing time pressure, and holds EPAM to the Phase 1 fixed price against undocumented SAP scope.

### C-3 — NCC pen-test governance does not address the timeline consequence of a Critical finding

The outsourced capability section says "EPAM writes and owns the remediation plan" — but it does not specify what happens to the Phase 3 timeline or the fixed price if NCC delivers a Critical finding in week 19, 10 days before the contract's Phase 3 exit date. The escalation path names who gets notified (MRG CTO within 24 hours), but notification is not resolution. The buyer will ask: "If NCC finds a Critical finding three weeks before go-live, how many weeks does Phase 3 extend, and who pays for it?"

**Risk if not addressed:** A Critical pen-test finding forces a Phase 3 delay with no pre-agreed timeline buffer or cost treatment — the dispute moves from the delivery team to the legal team.

---

## Patch Applied — Weakest Part: C-3 (Phase 3 pen-test timeline gap)

C-3 is the sharpest risk because it is the most likely to materialise (pen-test findings at late stage are common) and the contractual exposure is the largest (fixed-price Phase 3 with no timeline buffer named).

**Changes made to 02-solution.md:**

1. Phase 3 entry criterion updated from "clean pen-test report from NCC Group" to:  
   *"clean pen-test report from NCC Group OR all Critical findings remediated and re-verified by NCC"*

2. Added explicit timeline-impact statement to the NCC governance section:  
   *"Critical finding detected in weeks 17–19 adds ≤2 weeks to Phase 3; cost absorbed by contingency reserve."*

This binds the timeline impact to a named number (≤2 weeks) and names the cost treatment (contingency, not a change-order request), removing the ambiguity before the contract is signed.

**C-1 and C-2 patch notes:**

- C-1: Phase 1 exit criterion supplemented with a production metric — error rate ≤0.1% in production — alongside the OWASP test report. Both conditions must be met for Phase 1 exit sign-off. This change is reflected in the Phase Table in 02-solution.md.  
- C-2: A note added to the scoping sprint row in the Phase Table: "Scoping sprint is a pre-contract condition; declining the sprint converts Phase 1 to a T&M gate." This makes the deal-breaker visible in the solution outline, not only in the qualification memo.
