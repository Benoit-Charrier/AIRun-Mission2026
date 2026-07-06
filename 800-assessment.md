# 800 Assessment

**Date:** 2026-07-03

---

## L3 ops processes and their safety bounds

At L3 the agent executes the process autonomously; the human sets the bound in advance and reviews after, not during. Three canonical examples:

**1. Autoscaling**
The agent watches CPU / queue-depth metrics and adjusts replica counts.
Bound: max-replica cap (prevents runaway cost) + cooldown period ≥ pod-startup time (prevents thrashing — without it, a new scale-up event fires before the previous pods are ready, triggering another, and so on until the cap is hit).

**2. Canary deployment rollout**
The agent shifts traffic to a new version in steps, checking error rate and latency at each step before proceeding.
Bound: maximum traffic percentage per step (e.g. 5 % → 10 % → 25 % → 50 %, each requiring a passing observation window) + automatic rollback if the error rate rises above baseline by a fixed threshold within the window. The bound ensures no bad deploy can reach full traffic before a human can intervene; the auto-rollback is the hard floor if the observation window is breached.

**3. Alert triage and runbook execution**
The agent receives a firing alert, runs diagnostic commands, and executes a remediation step from a pre-approved runbook.
Bound: write actions restricted to an explicit allowlist from the runbook (read-only diagnostics are unrestricted); any action whose blast radius exceeds N services, or whose severity is classified S1, requires a human confirmation step before execution. This prevents the agent from taking broad remediation based on a misread or correlated alert — the blast-radius check is the hard gate that separates "I can fix this" from "I need a human."

---

## Observability signals

### The three classical signals

**Metrics** — numeric time-series measurements sampled on an interval: CPU, memory, request rate, error rate, latency percentiles. They are cheap to store and fast to query. They answer "how much" and "how often."

**Logs** — discrete, timestamped event records emitted when something notable happens. Structured logs carry key-value fields; unstructured logs are free text. They answer "what exactly happened, and when."

**Traces** — correlated spans that follow a single request through every service it touches, recording duration and status at each hop. They answer "where did this request spend its time, and where did it fail."

### Two failure modes a green uptime dashboard still misses

**1. Silent wrong answers (semantic failures).**
Every request returns HTTP 200, latency is nominal, error rate is zero — but the responses are incorrect. A metric formula is using the wrong denominator, a recommendation engine is serving stale embeddings, a price calculation has a silent overflow. The uptime dashboard has nothing to report. This class of failure is only detectable by checking the *content* of responses against a ground truth, not the delivery of responses.

**2. Latency degradation that stays below the error threshold.**
Requests complete without errors, but p99 latency has climbed from 200 ms to 2,800 ms. Users time out on the client side or abandon, but the service never returns a 5xx. If the alerting threshold is "error rate > 1 %" and the SLO is defined only on availability, this degradation is invisible to the dashboard. Uptime is 100 %; the service is effectively broken for interactive use.

### The signal DIAL adds for AI model calls

**Token consumption per request** — prompt tokens in, completion tokens out, and total tokens per model call. Traditional APM has no concept of this signal; it is the AI-specific unit of work. DIAL surfaces it as a first-class metric so teams can see cost per feature, identify prompt-size outliers, and set per-call token caps the same way they set CPU limits on a container.

---

## Agent spec: seven required fields and the inline field

### The seven fields

| # | Field | What it contains |
|---|-------|-----------------|
| 1 | `name` | Short, lowercase, hyphenated slug (≤ 64 chars); unique within the agent roster |
| 2 | `description` | The "use me when" line: what the agent does + which inputs and outputs it names by path + a NOT-for clause listing the calls it must hand back to a human |
| 3 | Goal | One sentence: what raw input it turns into what governed output |
| 4 | Inputs & outputs | Every input and output named by its exact path, so the next operator can run it with no questions |
| 5 | Tools | An allowlist — which tools the agent may use, and the condition under which each is permitted; "everything except X" is not a safe spec |
| 6 | Decision rules | A DO / DON'T table where every row carries a number or a yes/no test, plus the escalate-never-decide line (human-owned calls) and 3–5 stop-and-ask conditions (each with a measurable trigger) |
| 7 | Check table | ≥ 3 rows, each naming a test input by path and a pass/fail signal that is counted or structural — never "the output looks correct" |

### The one field that must live inline

**Decision rules (the DO / DON'T table + escalation conditions).**

The `<!-- chain:rules:start --> … <!-- chain:rules:end -->` markers let Module 1111 copy the block out to a shared guide, but the block itself must remain in the agent body. The reason is a hard constraint: guardrails the agent cannot see are guardrails it cannot follow. If the rules live in a separate file that is not loaded into the agent's context — or that drifts from the inline version — the agent operates without its safety bounds. Every other field can be referenced externally; this one cannot. The rules must be in the same file the agent reads.
