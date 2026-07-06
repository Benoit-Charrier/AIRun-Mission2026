# 600 — QA Assessment

## Wide Theory — Root cause vs symptom; guard tests

### Why "the payment service is sometimes slow" is a symptom, not a root cause

A symptom names what you *observe*. It says the surface-level effect — slow, failing, unreliable — without naming the structural condition that makes the bug *possible*. Two things make "sometimes slow" particularly weak as a root cause:

First, it names a frequency ("sometimes"), not a condition. A condition can be reproduced: *"the payment service times out when the SCA challenge takes longer than the 2-second timeout that was configured for synchronous calls."* A frequency cannot: there is no test input labelled "sometimes." You cannot write a guard against "sometimes."

Second, it names an observation about a service rather than a code path. The same observable — the service appearing slow — can be caused by a missing timeout, a missing retry-hold state, a lock contention, or an unbounded synchronous call. Each of those has a different fix and a different guard test. Stopping at the observation leaves the fix path ambiguous.

**What a complete RCA must name instead.** The specific structural condition in the code (or design) that allows the failure to occur. It must identify: (1) the code path or state transition where the gap exists, (2) what is missing — a guard, a hold, a timeout, a state — and (3) why fixing one layer is not sufficient if two conditions interact. The Meridian DEF-001 RCA named this exactly: "the SAP inventory read at pickup confirmation was treated as advisory — its result was written to a log but the POS confirmation flow had no guard that blocked handover when `available_stock == 0` — and no held-stock token was written at reservation time." That sentence identifies the missing guard, the missing token, and the interaction between them. A stranger can write the fix and a test from it; they cannot write either from "the system sometimes fails."

### What a guard test adds that re-running the original failing input does not

Re-running the original failing input proves the specific instance no longer fails. It does not prove the *class* of failure is closed.

A guard test is built around the condition — not the instance — and runs that condition across multiple input shapes. The DEF-001 guard test ran three variants: G-01 (single-item, domestic), G-02 (cross-region), G-03 (multi-item, one item at zero stock). Each variant exercises the same `available_stock == 0` guard from a structurally different entry point. If the fix applies the guard per-order rather than per-item, G-01 and G-02 pass but G-03 fails — and that failure would not appear in a re-run of TC-08 alone.

Re-running the original input is a regression check. The guard test is a structural proof. The distinction matters in code review and in sign-off: a failing guard test tells you the fix is incomplete; a passing re-run without a guard test tells you only that the exact case that was reported is gone.

---

## Katas / Final Kata — The Wide chain; Deep human-owned decisions

### The Wide kata chain: test plan to test report

Each artefact is produced by a single kata and creates the input the next one depends on:

| Kata | Artefact produced | How it feeds the next |
|------|-------------------|-----------------------|
| **K 6.W.1 — Test plan** | `00-test-plan.md` | Names in-scope surfaces and top three risks. Those surfaces and risks are the coverage contract that test-case authoring must satisfy — without the plan, there is no shared definition of what cases are required vs optional. |
| **K 6.W.2 — Test cases** | `01-test-cases.md` | 18 cases (critical-path, edge, negative, regression) derived from the plan's surfaces and risks. Each case specifies the preconditions and expected behaviour that test data must make reproducible — the data kata inherits every case's precondition list. |
| **K 6.W.3 — Test data** | `02-test-data.json` + `02-data-method.md` | The records (customer IDs, store IDs, SAP stub behaviours, loyalty cards) needed to execute each case. Without the data file, the cases are specifications with no runnable inputs; the defect log kata inherits the records by reference in every reproduction path. |
| **K 6.W.4 — Defect log** | `03-defects.md` | What actually happened when cases were run — expected vs actual, minimal reproduction steps, priority and severity. The RCA kata takes the most painful defect from this log as its starting point; the log also provides the defect density and priority distribution that the test report reads directly. |
| **K 6.W.5 — RCA** | `04-rca.md` | Root cause of the most painful defect: structural condition, hypotheses, guard test, fix recommendation. The test report inherits this as the evidence behind the "top two problematic areas" and the first item in the improvement backlog — the report's rollout signal and backlog require the RCA to go beyond "we found a bug." |
| **K 6.W.6 — Test report** | `05-report.md` | Rolls up all five prior artefacts into a one-page coverage table, pass rate by priority, top two problem areas, ranked improvement backlog, and a binary rollout signal (exit criterion met or not met). The report consumes the plan (exit criteria), the cases (total count), the defects (IDs and priorities), and the RCA (structural insight behind the top area). |

### Two Deep decisions that stay human-owned no matter how good the AI's draft is

**1. What "good enough" means — the acceptance threshold itself.**

The AI can report that per-rule agreement on the factuality dimension is 82%. It cannot decide whether 82% is acceptable for this feature, at this risk level, in this deployment context. That decision requires weighing the cost of a false pass — a customer receives incorrect factual information, the regulatory exposure, the incident pattern — against the cost of holding the release. Those trade-offs are not legible from the eval pack alone; they require knowing the business risk appetite, the downstream accountability chain, and the stakeholder context. If the AI sets the threshold, the threshold has no human accountability behind it: when the threshold turns out to be wrong, there is no one to review and adjust it. The human who sets the threshold can be held accountable for the consequences; the AI cannot. That is why it cannot be delegated.

**2. The release call.**

Even when all the measured signals look acceptable — per-rule agreement above threshold, buckets preserved, no sub-85% rules, borderlines reviewed — the release call requires integrating signals that extend beyond the eval pack: operational readiness, support capacity, regulatory timing, whether the customer-facing population is the same one the golden set was built on. More fundamentally, the release call is an act of accountability. A named human is accepting responsibility for the consequences of deploying to production. Those consequences — a wave of customer contacts, a data incident, a regulatory query — fall on the team and the business, not on the AI. An agent that makes the release call autonomously is an agent that takes on zero consequences for being wrong. The escalation gate exists precisely because the person who signs off must be the person who can be called to account.
