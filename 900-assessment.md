# 900 Assessment

**Date:** 2026-07-06

---

## STRIDE category and failed trust boundary

**Which STRIDE category applies to the data flow carrying the search string?**

**Tampering (T).** The attacker controls characters in the search string and can embed syntax that restructures the query the backend service builds — changing its logic, scope, or target. That is textbook tampering: an external actor modifying data in transit in a way that alters its intended meaning or effect. Information Disclosure (I) and Elevation of Privilege (E) are the likely downstream consequences once the tampered query executes, but the threat *on the data flow itself* is Tampering.

**Which trust boundary failed?**

The **external-to-internal service boundary** — specifically the API ingress point where user-supplied input crosses from the untrusted public network into the trusted backend. The invariant at that boundary is: validate and sanitize all untrusted input before it enters the trusted zone. Here that invariant was absent: the raw string crossed the boundary unchecked and was handed directly to the query builder inside the trusted zone. The database query builder had no reason to distrust its caller — it was inside the trust boundary — so it used the string faithfully, exactly as an attacker intended. The failure is not in the query builder; it is in the boundary that should have stopped the malicious payload from reaching it.

---

## The lethal trifecta and prompt injection

**The three legs**

| Leg | What it means |
|-----|---------------|
| 1. Attacker-controlled content reaches the model's context | Malicious text is embedded in the prompt — via a web page the agent fetches, a document it processes, a tool result it reads, or the user's own message |
| 2. The model has agentic capability | The model can invoke tools: send email, read/write files, call APIs, execute code, exfiltrate data |
| 3. The model's outputs are trusted and executed | Downstream components — orchestrators, tool executors, human consumers — treat the model's instructions as authoritative and act on them without an independent safety check |

**Why removing any one leg contains the blast radius**

- **Remove leg 1:** The attacker never gets a vector. No malicious instruction enters the context, so there is nothing to execute. All other defences are moot.
- **Remove leg 2:** Even a perfectly injected instruction can only produce text. The model cannot send the email, delete the file, or call the exfiltration endpoint — it has no actuators. The injected payload dies in the output buffer.
- **Remove leg 3:** Even if the model is injected and has tools, if the output is reviewed before execution — or if the tool executor applies its own policy checks — the attacker's instruction is intercepted before it causes real harm. The blast radius is contained at the execution gate rather than at the injection point.

Removing *any single leg* forces the attacker to solve an additional problem: provide the vector, provide the capability, or bypass the trust check. That is why defence-in-depth targets at least two legs simultaneously rather than betting everything on one.

**Which kind of system has all three legs live almost by definition?**

An **agentic AI assistant with tool use and access to untrusted content** — particularly a web-browsing or document-processing agent that can take real-world actions. The value proposition of such a system *is* that it reads arbitrary external content (leg 1 always live), acts via tools (leg 2 always live), and is trusted to complete tasks autonomously without per-action human review (leg 3 always live). The three legs are not incidental risks; they are the design. That is why agentic systems require the strongest prompt-injection mitigations: they cannot remove any leg without losing their core utility.

---

## K 9.W.5 — what "tested manually" is missing

**What is missing**

"Tested manually" is a point-in-time attestation by a human, not evidence of continuous operation. It tells the auditor that someone checked the filter on an unknown date under unknown conditions. It does not show:

1. **That the filter ran continuously in production throughout the quarter** — a manual test in a lab or staging environment proves nothing about the live system.
2. **That the evidence is machine-verifiable and timestamped across the full period** — there is no audit trail, no density of records, and no way to rule out that the filter was disabled or degraded between the one manual check and the next.

An auditor asking for evidence of *operation during the last quarter* needs records that span the quarter, are generated automatically (not by a human who could have skipped a week), and come from the production system, not a test bench.

**Two artifacts that make the finding go away**

| Artifact | What it provides |
|----------|-----------------|
| **CI/CD automated test logs** spanning the quarter | Timestamped, per-deployment pass/fail records of the PII filter regression tests — proves the filter was continuously tested on every build, not just checked once by hand |
| **Production filter telemetry / audit logs** | Operational records from the live system showing invocations, detection events, and redaction counts day-by-day across the quarter — proves the filter was actually running in production, not just passing in a test environment |

Together these two artifacts answer both gaps: the CI logs prove continuous automated testing; the production telemetry proves live operation. Either alone is insufficient — CI logs without production logs leave open "did it actually run in prod?", and production logs without CI logs leave open "how do you know the logic was correct?".
