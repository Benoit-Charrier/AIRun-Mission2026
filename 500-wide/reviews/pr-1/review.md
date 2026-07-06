# Review — PR-1: add --min-count N flag

**Change:** `--min-count N` CLI flag for `src/logsum.py`
**Files changed:** `src/logsum.py`, `spec.md`, `tests/test_logsum.py`
**Spec:** `500-wide/spec.md §CLI` (signed off 2026-06-29)
**Session log:** `500-wide/sessions/logsum-min-count/session-log.md`
**Tests:** `500-wide/tests/test_logsum.py::test_min_count_filters_groups`
**Test isolation tier:** `limited` — written in the same session as the implementation

---

## Seven-lens review

| # | Lens | Finding |
|---|------|---------|
| 1 | **Correctness** | Spec says: groups with `count >= N` written to output; default writes all groups. Implementation: `min_count is None or data["count"] >= min_count` in the list comprehension. Matches spec. Test `test_min_count_filters_groups` covers the filter case. **None found.** |
| 2 | **Security** | No auth, no PII, no external calls, no file-path injection (argparse handles the argument boundary). `type=int` in argparse rejects non-integers before the function is called. **None found.** |
| 3 | **Error handling** | `--min-count -5` silently includes all groups (`count >= -5` is always true for positive counts). `--min-count 0` same. No exception, no warning, no spec position on negative or zero values. **Minor finding:** document the N ≤ 0 behaviour in `spec.md §CLI` ("N ≤ 0 is treated as no filter"). |
| 4 | **Performance** | Filter is a single list comprehension over `groups.items()`, O(n) where n = unique (level, service) pairs. No concern at synthetic-log scale. **None found.** |
| 5 | **Observability** | When `--min-count N` filters all groups to zero rows, the user receives an empty `summary.csv` (headers only) with no stderr signal explaining why. **Minor finding:** emit a stderr note — `"Info: 0 groups met --min-count={N} threshold"` — when `min_count is not None` and the filtered `rows` list is empty. |
| 6 | **Maintainability** | `min_count=None` is a clean optional parameter on an already-refactored `summarise()` signature. The K 5.W.6 `_update_group` extraction was unaffected. Session log and provenance note written. **None found.** |
| 7 | **Dependency** | No new imports; `argparse` and `csv` are standard library. CLAUDE.md escalation gate ("stop before adding dependencies outside Python 3.11 standard library") respected. **None found.** |

---

## Adversarial pass

**Goal:** actively try to produce incorrect, silent, or misleading output.

| Probe | Result |
|-------|--------|
| `--min-count abc` | argparse exits code 2 with `"invalid int value: 'abc'"` before `summarise()` is called. ✅ |
| `--min-count 0` on 3-group input | All 3 groups output (count >= 0 is always true). Correct but undocumented — matches Error-handling finding above. |
| `--min-count 9999` on 3-group input | Empty summary.csv, headers written (spec §Edge cases 3). ✅ |
| `--min-count 2` on 3-group input where one group has count=1 | Only the 2 groups with count >= 2 written. Test `test_min_count_filters_groups` covers this exact case. ✅ |
| No `--min-count` flag at all | `args.min_count` is `None`; `min_count is None` short-circuits filter; full output written. Default unchanged. ✅ |

**Adversarial verdict:** no security or correctness issues found. Two minor
observability/documentation gaps identified (lenses 3 and 5). Neither is
security-class; neither requires stopping before merge.

---

## AC coverage

| Spec section | Test(s) | Covered |
|---|---|---|
| §Goal | `test_groups_by_level_and_service`, `test_duplicate_rows_collapsed_into_one_group` | ✅ |
| §Normalisation | `test_level_normalised_to_lowercase` | ✅ |
| §Aggregation | `test_count_aggregation`*, `test_first_seen_and_last_seen` | ✅ |
| §Edge cases 1 | `test_missing_level_becomes_unknown` | ✅ |
| §Edge cases 2 | `test_malformed_timestamp_row_skipped` | ✅ |
| §Edge cases 3 | `test_empty_input_produces_header_only` | ✅ |
| §Edge cases 4 | `test_missing_required_column_exits_1` | ✅ |
| §CLI exit code 1 | `test_missing_input_file_exits_1` | ✅ |
| §CLI --min-count | `test_min_count_filters_groups` | ✅ |

*`test_count_aggregation` is an alias for the duplicate-group test — both cover the
count AC.

**Result: 0 ACs uncovered.**

---

## Recommendations before merge (non-blocking)

1. Add one line to `spec.md §CLI`: "N ≤ 0 is treated as no filter (all groups written)."
2. Emit stderr note when `--min-count` filters to zero rows.
3. Re-generate `test_min_count_filters_groups` in a fresh session from `spec.md §CLI
   --min-count N` to upgrade its isolation tier from `limited` to `B`.

---

## PR provenance block

```
spec:        500-wide/spec.md (signed off BC 2026-06-29)
session-log: 500-wide/sessions/logsum-min-count/session-log.md
tests:       500-wide/tests/test_logsum.py (10 tests; K 5.W.4 tier B + K 5.W.7 limited)
review:      500-wide/reviews/pr-1/review.md (7 lenses + adversarial; 2 minor findings)
```
