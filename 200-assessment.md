**Module 200 — PM / BA · Wide Assessment**
Date: 2026-06-25

---

**Knowledge-check questions:**

1. _(Wide Theory)_ Name the four SVPG risks every spec must address before delivery starts — and explain why *"the output should be accurate"* fails as an acceptance criterion. Rewrite it as a falsifiable AC for a non-deterministic feature.

    Four risks: value, usability, feasibility, viability.
    "The output should be accurate" fails because there is no metric or threshold — an LLM-as-judge (or any reviewer) cannot mechanically pass or fail it; "done" is never defined.
    Rewrite: refusal rate ≤ 5%, gate.

2. _(Wide Theory, Block 7)_ Name three conditions where you should pull in a real PM/BA instead of covering the role with AI.

    Irreversible high-impact decisions (one-way doors), regulated domains where the traceability chain is the audit evidence, and active stakeholder conflict where the call is political not analytical.

3. _(Wide Theory, Block 3)_ What does recording the rejected alternative in a Decision Memory entry protect against — that recording only the decision doesn't?

    Avoids relitigating the decision later (and avoids silently reversing it without realising it was already considered).

4. _(Wide Theory, Block 5)_ A story enters sprint planning with no falsifiable acceptance criterion. Per the Definition of Ready, what happens — and whose call is it?

    Goes back to refinement, not into the sprint. PROD/BA owns the call.
