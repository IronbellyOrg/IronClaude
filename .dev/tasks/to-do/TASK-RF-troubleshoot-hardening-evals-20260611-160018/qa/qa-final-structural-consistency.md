# QA Report — Final Structural Consistency (E1-E5 backtest harness)

**Topic:** Cross-artifact internal consistency of the E1-E5 differential backtest harness
**Date:** 2026-06-12
**Phase:** report-validation (static structural cross-check)
**Fix cycle:** N/A (report-only, fix_authorization: false — NO files modified)

---

## Overall Verdict: **FAIL**

One internal-consistency defect found: the harness inventory's headline total line count
contradicts both its own per-file table and the real files on disk.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | REPLAY_ESCAPES parent shas across git_replay.py + runners + replay-table | PASS | See criterion 1 below — all 5 agree across 3 surfaces |
| 2 | Schema enums == model constants (backtestStatus, verdict) | PASS | See criterion 2 below — verbatim match |
| 3 | `_ESCAPE_REFS` == each runner's `requires_impl_ref(...)` | PASS | See criterion 3 below — all 5 refs agree |
| 4 | Wave mapping (E1H1,E2H3,E3H3,E4H2,E5H4) across 3 surfaces | PASS | See criterion 4 below |
| 5 | Counts agree (total_escapes==5; 5 fixtures; no off-by-one) | **FAIL** | Inventory headline total = 2869 but actual = 2795 |

## Summary

- Checks passed: 4 / 5
- Checks failed: 1
- Critical issues: 0
- Important issues: 1 (inventory headline line-count desync)
- Issues fixed in-place: 0 (report-only)

---

## Criterion-by-Criterion Evidence

### 1. REPLAY_ESCAPES parent shas — PASS

Expected: E1=94d5baa0, E2=10723863, E3=e97aa4fd, E4=1b0264f1, E5=d878bc6d.

- `git_replay.py:49-55` — E1=`94d5baa0`, E2=`10723863`, E3=`e97aa4fd`, E4=`1b0264f1`, E5=`d878bc6d` ✓
- Runners read `escape_by_id(...).prefix_parent_sha` dynamically (e.g. `test_backtest_e1.py:24,27`),
  so they inherit the table; runner docstrings hardcode the same values:
  `test_backtest_e1.py:3` (94d5baa0), `test_backtest_e2.py:3` (10723863),
  `test_backtest_e3.py:3` (e97aa4fd), `test_backtest_e4.py:9` (1b0264f1),
  `test_backtest_e5.py:3` (d878bc6d) ✓
- `replay-table.md:10-14` — E1=94d5baa0, E2=10723863, E3=e97aa4fd, E4=1b0264f1, E5=d878bc6d ✓
- `final-harness-inventory.md:30-34` — same 5 shas ✓
- Chain note cross-check: E5 fix `10723863` == E2 parent (`git_replay.py:50,55`); E2 fix `e97aa4fd`
  == E3 parent (`git_replay.py:50,51`); echoed in `replay-table.md:26` ✓

### 2. Schema enums == model constants — PASS

- backtestStatus: schema `catch_rate.schema.json:73-77` = {not_run, partial, complete};
  model `catch_rate.py:41-43` STATUS_NOT_RUN/PARTIAL/COMPLETE = same three, same order ✓
- verdict: schema `catch_rate.schema.json:104-107` = {CATCH, MISS};
  model `catch_rate.py:37-38` VERDICT_CATCH/VERDICT_MISS = same ✓
- `escapeResult.required` (6) `catch_rate.schema.json:87-94` == `_ESCAPE_RESULT_FIELDS`
  `catch_rate.py:50-57` (6) ✓; top-level `required` (10) `catch_rate.schema.json:7-18` ==
  `_CATCH_RATE_FIELDS` `catch_rate.py:59-70` (10) ✓

### 3. `_ESCAPE_REFS` == runner `requires_impl_ref` — PASS

`test_catch_rate_aggregation.py:39-45` vs runner decorators:

- E1 → runtime-entrypoint-verification.md == `test_backtest_e1.py:78` ✓
- E2 → unmask-and-sweep.md == `test_backtest_e2.py:90` ✓
- E3 → unmask-and-sweep.md == `test_backtest_e3.py:103` ✓
- E4 → contract-enumeration.md == `test_backtest_e4.py:94` ✓
- E5 → effective-input-proof.md == `test_backtest_e5.py:67` ✓

### 4. Wave mapping — PASS

Expected E1→H1, E2→H3, E3→H3, E4→H2, E5→H4.

- `git_replay.py:49-55` — H1/H3/H3/H2/H4 ✓
- Runner `EscapeResult(wave=...)`: `test_backtest_e1.py:70` H1, `test_backtest_e2.py:81` H3,
  `test_backtest_e3.py:94` H3, `test_backtest_e4.py:85` H2, `test_backtest_e5.py:58` H4 ✓
- `replay-table.md:10-14` — H1/H3/H3/H2/H4 ✓
- `final-harness-inventory.md:30-34` — H1/H3/H3/H2/H4 ✓
- Note (non-blocking): doc-range strings differ — `git_replay.py:35` says "(H0..H5)" while
  `catch_rate.py:79` says "(H1..H4)". These are descriptive ranges, not per-escape pins; the
  five actual per-escape mappings all agree, so this is NOT a consistency failure (cosmetic only).

### 5. Counts — FAIL

Sub-checks:
- 5 fixtures: `final-harness-inventory.md:40` lists 5; `ls fixtures/catch_rate/` returns exactly
  5 (all_catch_missing_witness, invalid_bad_status, invalid_bad_verdict, valid_full, valid_minimal) ✓
- total_escapes==5: schema `catch_rate.schema.json:41`, aggregation asserts
  `test_catch_rate_aggregation.py:136,194,272`, `_ESCAPE_REFS` 5 keys, `REPLAY_ESCAPES` 5 tuples ✓
- **Headline line-count off — FAIL.** `final-harness-inventory.md:3` claims **"Total: 2869 lines."**
  The inventory's OWN per-file table sums to **2795** (modules 1+240+248+284+169+57+50+125+33 = 1207;
  tests 87+140+125+337+70+19+90+100+113+104+77+50+276 = 1588; 1207+1588 = 2795). Actual concatenated
  `wc -l` over the same 23 listed files = **2795**. The headline overstates by **74 lines**. The
  per-file numbers and disk agree; only the headline total is wrong.
  ("max = test_catch_rate_schema.py at 337" IS correct — 337 is the true max.)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT | `final-harness-inventory.md:3` | Headline "Total: 2869 lines" contradicts the document's own per-file table (sums to 2795) and the actual files on disk (2795). 74-line overstatement. | Change "2869" → "2795" so the headline matches the per-file table and disk reality. The I21 trigger reasoning ("no single file exceeds 500") is unaffected; max=337 is correct. |

## Actions Taken

None — report-only (fix_authorization: false). No file was modified.

## Recommendations

- Correct `final-harness-inventory.md:3` from `2869` to `2795` before this inventory is consumed by
  any downstream gate or sign-off that trusts the headline figure.
- (Optional, cosmetic) Reconcile the H-wave doc-range strings (`git_replay.py:35` "H0..H5" vs
  `catch_rate.py:79` "H1..H4"). Not a correctness defect; the per-escape pins are all consistent.

## Confidence

- **Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
  (The "38 passed/11 skipped" runtime claim at `final-harness-inventory.md:44` was OUT OF STATIC
  SCOPE — not part of the 5 consistency criteria — and was deliberately not executed; it does not
  affect the structural verdict.)
- **Tool engagement:** Read: 8 | Grep: 0 | Glob: 0 | Bash: 4

## QA Complete
