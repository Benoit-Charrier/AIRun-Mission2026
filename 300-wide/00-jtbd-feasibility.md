---
product: Meridian retail site and app
feature: AI availability assistant
kata: 3.W.1
date: 2026-06-25
---

## JTBD statement

**User:** click-&-collect shopper (not the store associate)

> **When** I need an item today and a Meridian store is nearby,
> **I want** to know whether it's actually collectable there right now,
> **so I can** pick it up on my way without risking a wasted trip.

*Outcome clause check:* the goal is not "see a stock widget" — it is avoiding a wasted trip. The feature is a means; the outcome is the avoided cost of driving to an empty shelf.

---

## Two-branch feasibility gate

### Branch 1 — AI in the process (us using AI to design and deliver)

| Gate question | Answer | Verdict |
|---|---|---|
| Client permits AI tools for delivery? | Yes — EPAM CodeMie pre-approved by Meridian | ✅ Yes |
| Sensitive data kept out of AI inputs? | Yes — non-PII stock counts + store metadata only; customer identity and order history stay out of the AI path | ✅ Yes |
| Approved toolset named? | CodeMie Claude (primary); Claude / v0 / Lovable permitted with anonymised inputs | ✅ Yes |

**Branch 1 verdict: Conditional** — CodeMie Claude is the primary runtime; third-party AI tools (Claude, v0, Lovable) are permitted for delivery work with anonymised inputs only.

---

### Branch 2 — AI in the product (the availability assistant itself)

| Gate question | Answer | Verdict |
|---|---|---|
| Stock data ready and fresh enough for the promise we'd make? | SAP inventory sync is 15–30 min stale at best; data is sufficient for an *estimate* but not a guarantee or exact unit count | ⚠️ Conditional |
| Regulatory framework clear? | GDPR/CCPA apply if the surface personalises by customer identity; EU AI Act high-risk classification not expected but not yet confirmed | ⚠️ Conditional |
| Worst-case understood? | Confident false promise ("In stock") → shopper drives over → item not there → wasted trip → churn; currently ~7% of click-&-collect orders | ✅ Yes |

**Branch 2 verdict: Conditional** — the assistant may proceed provided:
1. It **never** promises exact unit counts or a guaranteed hold.
2. It **never** shows a positive availability state when data is stale (> 30 min) or missing.
3. It shows a confidence cue ("Likely in stock") and a freshness label on every estimate.
4. It shows a plain-language fallback ("Can't confirm right now — call the store") when data is unavailable.
5. GDPR/CCPA compliance is confirmed before any personalised surface is added.

---

## Approved-tools list for the rest of the series

| Use | Tool |
|-----|------|
| Design, journeys, specs | CodeMie Claude, DIAL |
| Prototype generation | v0 / Lovable / Claude Artifacts (anonymised inputs) |
| Heuristic review | DIAL with a vision model, Claude |
| Data: inputs to AI | Non-PII only — SAP stock counts, store metadata, distances |
