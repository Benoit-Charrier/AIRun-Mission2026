# Agent task provenance — K 5.W.7

**Task:** Add `--min-count N` to `src/logsum.py`. When set, output only groups
whose count is >= N. Default behaviour unchanged. Update `spec.md` and
`tests/test_logsum.py`.

**Model:** claude-sonnet-4-6
**Context loaded:** CLAUDE.md, spec.md, src/logsum.py, tests/test_logsum.py

**Plan approved before execution:**
1. Add `--min-count N` (int, default None) to `parse_args()`.
2. Add `min_count=None` parameter to `summarise()`.
3. Filter rows in the list comprehension before `_write_summary`: keep row only
   if `min_count is None or data["count"] >= min_count`.
4. Pass `args.min_count` in the `__main__` block.
5. Update `spec.md` CLI section — add the flag and its semantics.
6. Remove the "planned; added in K 5.W.7" note from spec.md Out-of-scope list.
7. Add `test_min_count_filters_groups` to `tests/test_logsum.py`.

**Files changed:**
- `src/logsum.py` — parse_args, summarise signature, rows filter, __main__
- `spec.md` — CLI section updated, Out-of-scope list updated
- `tests/test_logsum.py` — one test added

**Plan deviations:** none

**Untested items:**
- `--min-count 0` edge case (0 means keep all groups — same as omitting the flag;
  semantically correct but not explicitly tested)
- CLI invocation via subprocess to test argument parsing end-to-end
