---
module: 300 — Design & Experience
track: Wide
date: 2026-06-26
case: Reference Case A — Meridian (AI availability assistant)
---

## Knowledge Check

### Q1 — Framing & gate (Wide Theory)

**What makes a JTBD different from a feature request?**
A feature request names a solution ("show stock faster"). A JTBD names a real-world outcome the user is trying to achieve — the situation that triggers it, the motivation, and the result they need. The feature is invisible in a well-written JTBD.

**Rewrite:** "I want the app to show stock faster"
→ *When I'm near a Meridian store and need an item today, I want to know whether it's actually on the shelf right now, so I can decide whether to drive over without risking a wasted trip.*

The original names a UI speed improvement; the JTBD names the outcome (avoided wasted trip) and the situation (near a store, time-sensitive). The feature that serves it could be speed, or confidence labelling, or a phone number — the JTBD doesn't prescribe which.

**Two branches of the feasibility gate:**
- **Branch 1 — AI in the process** (us using AI to design and deliver): gate question — is the client's approved toolset named and is sensitive data kept out of AI inputs? (For Meridian: CodeMie pre-approved; non-PII stock data only — passes Conditional.)
- **Branch 2 — AI in the product** (the availability assistant itself): gate question — is the stock data ready and fresh enough for the promise the feature would make, and is the worst case understood? (For Meridian: SAP sync is 15–30 min stale — estimate only, never a guarantee; worst case = confident false promise → wasted trip → churn — passes Conditional with design constraints.)

---

### Q2 — Trust & HITL (Deep Theory)

**What makes something a gap vs "users will be confused"?**
A gap is a specific sentence the user would say that reveals a false assumption about how the system works — something you can write down and test. "Users will be confused" is a vague worry; a gap is observable: *"It said 'In stock' so I assumed the item was held for me."* That sentence reveals a concrete false belief (hold = guaranteed) that the design must address.

**Concrete gap for the availability assistant:**
*"It said 'Likely in stock' so I assumed that meant it was almost certainly there."* — The gap is that "Likely" reads as high-confidence to shoppers even when confidence is 0.62. The design fix: add a numeric or verbal anchor ("estimated, not confirmed") and a disclosure link — patched via AI-AC4 (disclosure) and the warning box on the confirmation screen in `05-mockup.html`.

**Three actions classified:**
| Action | Classification | Why |
|--------|---------------|-----|
| Estimate and display the availability verdict | **Agent-led** | Fast, reversible, compensated by logging; no inventory mutated; the shopper still decides whether to reserve |
| Place a stock hold that commits store inventory for 30 min | **Confirm-then-act** | Irreversible and costly — commits store stock, blocks other shoppers; user must explicitly trigger it |
| Override a "Not available" verdict that is wrong (e.g. associate physically finds the item) | **Human-only** | Requires lived context the AI doesn't have; a wrong override has direct downstream consequences |

**Why all-confirm defeats the point:**
Confirm-then-act is right for irreversible, costly actions. Applying it to every action — including reading a verdict and displaying it — kills the speed benefit that makes the AI feature worth building. The shopper already has to confirm the reservation; adding confirmation to the verdict display adds friction with no safety gain. Reserve confirmation for actions that commit something (inventory, money, a trip) and compensate agent-led actions with logging, not friction.

---

### Q3 — AI-aware AC & handoff (Kata / Final Kata)

**Three of the 6 AI-AC layers with one testable clause each:**

- **Confidence:** WHEN `stock_confidence` < 0.7, THEN display "Likely in stock" (not "In stock") and show the last-confirmed timestamp inline. *(Threshold: 0.7; observable: label text changes.)*
- **Refusal / fallback:** WHEN SAP sync for a store is > 30 min stale OR the signal service is unreachable, THEN display "Can't confirm right now — call the store" with the store phone number and suppress any positive availability state. *(Threshold: 30 min; observable: positive state suppressed.)*
- **Negative AC:** The assistant MUST NOT display the green "In stock" state when `confidence_score` < 0.7 OR `data_freshness_minutes` > 720. *(Threshold: 0.7 confidence / 720 min freshness; testable: render the in-stock state at confidence 0.69 and verify it does not appear.)*

**Why the negative AC is the most expensive to skip:**
Every other clause tells the agent what to do; the negative AC tells it what it must never do regardless of any other condition. An AI coding agent builds what is written. Without an explicit "MUST NOT", the agent has no instruction preventing it from rendering a confident "In stock" badge on stale data — which is exactly the current failure mode causing ~7% phantom-stock cancellations. Fixing it post-launch means a hotfix, comms to affected shoppers, and trust repair. Skipping it in the spec costs the most because the failure mode it prevents is the entire reason the feature exists.

**Two of the six Definition of Handoff Done checks (K 3.W.7):**
1. ≥ 3 AI-AC refined to component / variant / color token / typography / placement / visual gate.
2. Negative AC ("must NOT") carried verbatim into SPEC.md.

---

## Self-Reflection

### SR1 — Missing decision-owner

In the Meridian kata, the workshop (K 3.W.3) forced naming Sarah Chen (Head of CX) as the decision-owner for the confidence-graded vs suppress-until-confirmed question. On live projects the equivalent moment is a "design review" with stakeholders from CX, Ops, and Product where the conversation covers the design direction but no one is named as the person who closes it. The typical stall: a second round of the same review happens three weeks later because no one was empowered to say "we're going with option A." The fix is the same as the kata — name the decision and the owner before the room meets, not after.

### SR2 — Weakest trust surface

The weakest trust surface in products I encounter regularly is the **fallback state** — what the system shows when it can't assess something. Most AI-assisted features either show a spinner that never resolves, silently default to the happy-path label, or show a generic error. None of these tell the user what happened or what to do next. For the Meridian assistant, this was patched via AI-AC2 and the `FallbackBanner` component ("Can't confirm right now — call the store"). The concrete next step for any product with a similar gap: audit every AI-driven state for the absence of a `cannot-confirm` branch, then write AI-AC2 (refusal/fallback) with an explicit threshold and a human recovery path.

### SR3 — Saying no to an AI feature

The exact words for the next time a "let's add AI" suggestion fails the feasibility gate:

*"Before we design this, let's run the two-branch gate. Branch 1: do we have an approved tool and are we keeping sensitive data out of the model? Branch 2: is the data fresh enough for the promise we'd be making, and do we understand the worst case if the estimate is wrong? If Branch 2 comes back Conditional or No, we redesign the feature to match what the data can actually support — or we descope the AI surface until the data is ready. The goal is not to block AI; it's to make sure we're not shipping a confident wrong answer."*
