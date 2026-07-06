# K 5.W.9 — By-hand vs by-agent comparison

**Replay branch:** `logsum-agent-replay` (single-pass plan-execute over K 5.W.2–6)

---

## What both produced

Both the supervised chain (K 5.W.1–8) and the agent replay produced:
- A `spec.md` with the same eight sections and signed-off edge cases
- A working `src/logsum.py` that passes all grouping, normalisation, and edge-case
  behaviours described in the spec
- A `tests/` suite reaching ≥9 tests with pytest green
- A `.github/workflows/ci.yml` under 40 lines running ruff + pytest on Python 3.11
- A refactored implementation with a recorded diff

---

## Where the agent saved time

1. **Boilerplate scaffolding (≈8 min saved).** `argparse` setup, CSV DictReader
   loop, `_write_summary` helper, and `if __name__ == "__main__"` block were
   generated in one shot. In the supervised run, each structural decision (where
   does the loop go? what are the output column names?) required a separate prompt
   and diff review. The agent produced the same shape in a single plan-execute pass.

2. **CI YAML syntax (≈3 min saved).** The workflow file required no iterations in
   the replay — `actions/checkout@v4`, `setup-python@v5`, and the correct
   `pip install` order were emitted correctly the first time. In the supervised run,
   the workflow file needed one review cycle to confirm the path and Python version.

3. **Refactor diff (≈4 min saved).** The agent identified `setdefault` as the
   right refactor target without prompting and produced the extracted helper in one
   pass, including a correctly updated call site.

---

## Where the agent went wrong or shorter

1. **Tests were not independent of the implementation (critical gap).** The replay
   wrote tests in the same session that produced `src/logsum.py`. Two tests
   referenced `_update_group` by name in their docstrings — an internal helper the
   spec never mentions. In the supervised run, K 5.W.4's fresh-session constraint
   meant tests were written from `spec.md` only, so they checked the contract, not
   the implementation shape. The agent replay's test suite would have missed a
   refactor that renamed `_update_group` while keeping behaviour identical.

2. **Missing-level normalisation was incomplete in the first draft.** The agent
   wrote `row["level"].lower()` without the `.strip() or "unknown"` guard. It
   produced an `AttributeError` on the empty-level edge case rather than mapping to
   `"unknown"`. In the supervised run, the spec was read carefully before
   implementation, so the guard was in the first draft.

3. **Provenance note was produced last, after review, not before.** The kata
   (K 5.W.7) requires the provenance note before you inspect the diff. The replay
   agent appended it as the final step. This means the "what was not verified" field
   was written after the reviewer had already seen the changed files — reducing its
   value as a pre-review signal.

---

## What the agent did better

1. **Consistent style throughout.** The replay produced consistent 4-space
   indentation, f-string usage, and docstring placement with no variation. In the
   supervised run, one early draft used a `%s`-style format string in the warning
   print that had to be corrected in K 5.W.6.

2. **Sorted output without prompting.** The agent added `sorted(groups.items())`
   to the output rows unprompted — the spec says "rows sorted by (level, service)
   ascending" and the agent respected it without a follow-up. In the supervised run,
   the sort was confirmed against the spec in the diff-review step (K 5.W.3).

---

## What I learned about supervised vs async

The supervised chain's main advantage is the **test independence** guarantee from
K 5.W.4. Writing tests in a fresh session that has not seen the implementation is
not a ritual — it is the only way to catch the category of bug where the
implementation and the tests share an incorrect assumption. The agent replay, by
writing tests and code in the same session, inherited the missing-level bug in both
and the tests passed even before the fix.

The agent's main advantage is **continuous context**: it held the spec, the
implementation, the refactor target, and the CI shape in one pass without needing
prompts between steps. For a task this small, that difference is roughly 15 minutes.
For a larger feature, the advantage compounds until the first boundary condition
that requires a human to decide — at which point the agent must stop and ask anyway.

Rule of thumb from this comparison: **delegate boilerplate and structure; supervise
anything that touches a boundary condition** (edge cases, test isolation, security
constraints, escalation gates).

---

## What I would do differently next time

1. **Force the agent to write tests before the implementation** (or at minimum in
   a separate tool call with a cleared context). The replay's test gap is the single
   largest quality difference between the two runs.
2. **Require the provenance note as the first output** of the plan-execute step, not
   the last, so "untested items" is visible before the diff review.
3. **Feed the agent K 5.W.4's isolation rule explicitly:** "Do not read
   src/logsum.py when writing tests; derive every assertion from spec.md only."
   The agent does not know this rule unless told.
