---
product: Meridian retail site and app
feature: AI availability assistant
kata: 3.W.8
date: 2026-06-25
---

## Usability validation plan — confidence-graded availability indicator

**Feature under test:** confidence-graded availability label, alternative store suggestions, and "can't confirm" fallback state on the Meridian product page (click-&-collect flow).

**Method:** task-based usability test with 5 participants (click-&-collect shoppers who have used or attempted click-&-collect in the last 3 months). Sessions: 30 min each, think-aloud protocol, moderated remote via screenshare. Prototype: `05-mockup.html` (3-screen clickable flow).

---

## 5 usability task questions

**Task 1 — Primary happy path**
"Show me how you'd check whether this item is available to collect at a Meridian store near you today, and how you'd decide whether to reserve it."

*What we're testing:* does the shopper notice and understand the confidence label before reaching the Reserve button? Do they read the freshness timestamp?

---

**Task 2 — Low-confidence state**
"The app is showing 'Likely in stock' for the store nearest to you. Show me what you'd do next."

*What we're testing:* does the shopper understand the difference between "In stock" and "Likely in stock"? Do they tap the disclosure link? Do they feel more or less confident about reserving?

---

**Task 3 — Fallback state (can't confirm)**
"You've selected a store and the app is showing 'Can't confirm right now'. Show me what you'd do."

*What we're testing:* does the shopper find the store phone number and understand why the estimate isn't available? Do they consider the alternative stores? Do they feel blocked or informed?

---

**Task 4 — Alternative store redirect**
"The item you want shows 'Uncertain' at your nearest store. Show me how you'd use this page to find somewhere you could collect it today."

*What we're testing:* does the shopper notice and use the alternative store suggestions? Do they understand the confidence ranking? Are 2 alternatives sufficient or does the shopper expect more?

---

**Task 5 — Post-collection feedback**
"You've collected your item. The app is asking you a question — show me what you'd do with it."

*What we're testing:* does the shopper understand the feedback prompt? Are they willing to answer? Does the framing feel like a chore or a useful contribution?

---

## Success criteria

| Task | Pass signal | Target |
|------|-------------|--------|
| T1 | Shopper reaches Reserve button and can explain what the label means | ≥ 4/5 participants pass without prompting |
| T2 | Shopper identifies "Likely" as distinct from "In stock" and taps disclosure or verbalises the difference | ≥ 4/5 participants |
| T3 | Shopper finds the store phone number within 10 seconds | ≥ 4/5 participants |
| T4 | Shopper identifies and taps at least one alternative store suggestion | ≥ 4/5 participants |
| T5 | Shopper submits feedback (either response) without prompting | ≥ 3/5 participants |

**Outcome metric anchor:** phantom-stock cancellation rate — current ~7%; target ≤ 3% at the EU-West pilot stores within 3 months of launch. If T1 and T2 fail for ≥ 2/5 participants, label language must be revised before launch.
