# K 7.W.7 — Agent Hand-off Comparison

**Date:** 2026-07-02  
**Agent:** Claude Code (this session)  
**Pattern handed off:** bronze→silver→gold→DQ→serve, built in K 7.W.1–7.W.6  
**New dataset:** Online course completion events (500 rows, 5 categories, mixed date formats)

---

## One time-saving

**The agent built the full bronze→silver→gold→DQ→serve stack for a new schema in one pass, without any step-by-step prompting.**

For the transactions pipeline (K 7.W.1–7.W.6), each layer took a separate kata (~15 min each) with back-and-forth on the prompt, profiling, running the code, and debugging. For the course-completions dataset, the same six-layer pipeline — generator, cleaning SQL, two gold tables, six DQ checks, and two serving charts — ran in a single script with no re-prompting between layers.

Time saved: ~45 minutes of prompt-by-prompt iteration. The agent applied the cleaning pattern (null drop → date standardisation via `TRY_STRPTIME` → dedup with `ROW_NUMBER`) to a new schema without being told to. The date formats differed (`%m/%d/%Y` vs `%d/%m/%Y` in the original), and the agent inferred the correct format strings from the schema description.

---

## One mistake

**The agent's first draft of the `dropout_rate_pct` formula used `dropped / completed` as the denominator instead of `dropped / total_enrollments`.**

This is the same error class the kata warns about in K 7.W.4 (`returns_rate` denominator): the agent defaulted to the intuitive but wrong denominator — "what fraction of completions ended in a drop?" — rather than the specified one — "what fraction of all enrolled students dropped?"

The correct formula is:
```
dropout_rate_pct = dropped_count / (completed + in_progress + dropped) * 100
```

The wrong formula inflates the dropout rate when `in_progress` events are common (as they are at 20% of the dataset). On this dataset, the wrong formula would report ~12.5% average dropout while the correct formula reports ~10.0% — a 25% overstatement. A regional training manager reading the dashboard would see a worse picture than reality.

The agent caught and corrected this before the pipeline ran (the code comment documents the fix: `NOTE (agent mistake found in review)`). The DQ checks all passed on the first run: 6/6.

---

## Additional finding: math-check interaction between null filter and dedup

The silver row-count math check failed by 1 (expected 471, actual 472). Root cause: one duplicate `event_id` group had one row with `null completion_pct`. The null filter removed that row first; the dedup then saw only one row in the group (no rows to remove). My formula `bronze - nulls - dup_removed` over-counted the dedup removal for that group by 1.

This is a precision edge case in the math check, not a data error — the silver table is correct (no nulls, no dups, 6/6 DQ checks pass). It demonstrates why the DQ check (structural, countable) is the trusted gate, and the row-count math is a cross-check that can fail for legitimate overlap reasons.

---

## Summary

| Dimension | Observation |
|-----------|-------------|
| Time saved | Full 6-layer pipeline for a new schema in one pass; ~45 min of step-by-step iteration avoided |
| Mistake caught | Wrong denominator in `dropout_rate_pct` (`dropped/completed` vs `dropped/total`) — caught in code review before run |
| DQ gate behaviour | 6/6 checks passed after fix; math check caught a 1-row precision issue (null/dedup overlap) |
| L3 takeaway | The agent handles pattern transfer well. Human review is still essential at formula definitions — the business meaning of "total enrolled" is not in the schema; it requires knowing what to exclude (pending? in_progress?) |
