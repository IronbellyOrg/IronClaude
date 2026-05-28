# D-0052 — T04.14 Evidence: TEST-011..014 Axis-overlay pytest fixtures

**Task:** T04.14 (Phase 4 — M4 Five Adversarial Axes Overlay)
**Roadmap items:** R-084, R-085, R-086, R-087
**Date:** 2026-05-17
**Status:** PASS
**Tier:** STANDARD
**Confidence:** [█████████-] 90%

---

## 0. TL;DR

Four pytest fixtures land under `tests/audit/` covering the M4 axis-overlay
acceptance surface. All four files run green in a single pytest invocation
(37 / 37 PASS, 0.06 s wall-clock):

| Fixture | File | Tests | Roadmap |
|---|---|---|---|
| TEST-011 | `tests/audit/test_five_axes_overlay.py` | 10 | R-084 |
| TEST-012 | `tests/audit/test_axis_column_populated.py` | 10 | R-085 |
| TEST-013 | `tests/audit/test_drift_axis_inactive_when_no_goal_baseline.py` | 9 | R-086 |
| TEST-014 | `tests/audit/test_severity_floor_unweakened.py` | 8 | R-087 |

| AC | Statement | Status | Section |
|----|-----------|--------|---------|
| AC#1 | `uv run pytest tests/audit/test_five_axes_overlay.py tests/audit/test_axis_column_populated.py tests/audit/test_drift_axis_inactive_when_no_goal_baseline.py tests/audit/test_severity_floor_unweakened.py -v` exits 0 | PASS | §1 |
| AC#2 | TEST-013 asserts `drift-axis-inactive` literal annotation in Summary block | PASS | §3 |
| AC#3 | TEST-014 asserts byte-diff of Critical Rules block is zero | PASS | §4 |
| AC#4 | Evidence at `TASKLIST_ROOT/artifacts/D-0052/evidence.md` | PASS | this file |

---

## 1. AC#1 — Combined pytest invocation exits 0

**Command:**
```
uv run pytest \
  tests/audit/test_five_axes_overlay.py \
  tests/audit/test_axis_column_populated.py \
  tests/audit/test_drift_axis_inactive_when_no_goal_baseline.py \
  tests/audit/test_severity_floor_unweakened.py -v
```

**Output (tail):**
```
tests/audit/test_severity_floor_unweakened.py::TestRule6Verbatim::test_rule_6_present_in_source PASSED [ 94%]
tests/audit/test_severity_floor_unweakened.py::TestRule6Verbatim::test_rule_6_present_in_mirror PASSED [ 97%]
tests/audit/test_severity_floor_unweakened.py::TestRule6Verbatim::test_no_softening_tokens_in_critical_rules_block PASSED [100%]

============================== 37 passed in 0.06s ==============================
```

37 / 37 PASS, 0 failures, 0 errors. Exit code 0. AC#1 satisfied.

## 2. TEST-011 — Axes header precedes 15-item Checklist (R-084)

**File:** `tests/audit/test_five_axes_overlay.py` (10 tests).

**Assertions:**
- `#### Five Adversarial Axes` substring is present in BOTH
  `src/superclaude/agents/rf-qa-qualitative.md` and the `.claude/` mirror.
- `#### Checklist (15 items)` header is present in both.
- Ordering: the axes header line number is strictly less than the
  Checklist header line number (post-M4: 528 < 546 in both surfaces).
- All five canonical tokens `AX-1..AX-5` appear inside the slice
  between the axes header and the Checklist header.
- Source ↔ mirror byte-identity check.

**Roadmap traceability:** R-084 — "axes header before checklist."

## 3. TEST-012 — Axis column populated on every task-qualitative row (R-085)

**File:** `tests/audit/test_axis_column_populated.py` (10 tests).

**Assertions:**
- Items Reviewed table header `| # | Check | axis | Result | Evidence |`
  is present in both source and mirror (regex tolerates whitespace).
- Column order: `axis` sits BETWEEN `Check` and `Result` (positional
  index check on the header substring).
- Canonical vocabulary pattern `AX-1, AX-2, AX-3, AX-4, AX-5, none`
  appears in both surfaces (matches the binding at
  `rf-qa-qualitative.md:540`).
- Forbidden values `N/A`, `n/a`, `—`, `blank` are explicitly named
  in the canonical-rules block (HTML comment under Items Reviewed).
- Example row at `rf-qa-qualitative.md:711` enumerates the full
  closed vocabulary `[AX-1 / AX-2 / AX-3 / AX-4 / AX-5 / none]` and
  does NOT use `N/A` as a placeholder.
- Header line number matches between source and mirror (sync parity).
- Source ↔ mirror byte-identity check.

**Roadmap traceability:** R-085 — "axis column non-empty on every row."

## 4. TEST-013 — `drift-axis-inactive` Summary-block annotation (R-086)

**File:** `tests/audit/test_drift_axis_inactive_when_no_goal_baseline.py`
(9 tests).

**Assertions covering AC#2 (literal Summary-block annotation):**
- Literal token `drift-axis-inactive` appears in both source and mirror.
- The canonical-rules paragraph that mentions `drift-axis-inactive`
  also names the `Summary` block AND the `Axis-column` cell value
  (binding the annotation to the Summary block and forbidding cell-level
  placement).
- The literal string `NOT as an Axis-column cell value` (or its
  case-folded variant) appears verbatim in the rule body.
- The canonical GOAL-baseline-absent fixture at
  `artifacts/D-0045/fixture-goal-baseline-absent.md` exists.
- That fixture contains the literal `drift-axis-inactive` annotation.
- The annotation appears INSIDE the `## Summary` block
  (between `## Summary` and the next `## ` heading).
- The annotation does NOT appear as a cell value in any
  `| ... drift-axis-inactive ... |` table row.
- Source ↔ mirror byte-identity check.

**AC#2 directly satisfied** by
`TestDriftFixtureEmitsAnnotation::test_annotation_appears_inside_summary_block`:
it slices the fixture between `## Summary` and the next `## ` heading and
asserts the literal `drift-axis-inactive` is in that slice.

**Roadmap traceability:** R-086 — "drift-axis-inactive when no GOAL-baseline."

## 5. TEST-014 — Severity-floor / Critical Rules block byte-diff zero (R-087)

**File:** `tests/audit/test_severity_floor_unweakened.py` (8 tests).

**Assertions covering AC#3 (byte-diff zero on Critical Rules block):**

| # | Test | Invariant |
|---|---|---|
| 1 | `test_slice_hash_matches_baseline_source` | 10-line severity-floor slice in source SHA-256 == `770f439517cab45a605f0e098561946f04485d406393567fa8bbeaba9de91fc7` (pre-M4 baseline at commit `3a57a0d`). |
| 2 | `test_slice_hash_matches_baseline_mirror` | Same invariant for `.claude/` mirror. |
| 3 | `test_block_hash_matches_baseline_source` | Entire Critical Rules block in source SHA-256 == `fd7f2e457bf63ce0045ec5d7014e9af67c1b46892f49b090334be17bbd2fff0f` (pre-M4 baseline). |
| 4 | `test_block_hash_matches_baseline_mirror` | Same invariant for `.claude/` mirror. |
| 5 | `test_byte_diff_block_source_vs_mirror_is_zero` | Critical Rules block byte-equal between source and mirror. |
| 6 | `test_rule_6_present_in_source` | Severity-floor literal Rule #6 verbatim in source. |
| 7 | `test_rule_6_present_in_mirror` | Severity-floor literal Rule #6 verbatim in mirror. |
| 8 | `test_no_softening_tokens_in_critical_rules_block` | No softening tokens (`may be MINOR`, `could be MINOR`, `typically`, `should be IMPORTANT`, `consider IMPORTANT`) appear in the block. |

**Anchoring detail:** the 10-line slice is anchored by the
`## Critical Rules` header line (`start = header_line - 3`,
`end = header_line + 6`). This survives future strictly-additive
insertions above the section — the test fails only if the slice content
changes, not when upstream insertions shift its line numbers.

**Block delimitation:** the Critical Rules block runs from the
`## Critical Rules` header line through the first line that begins
Rule #11 (`11. **You complement rf-qa, not replace it**`), inclusive.
Both block-bound lookups locate the same line range in source and mirror.

**AC#3 directly satisfied** by
`TestCriticalRulesBlockHash::test_block_hash_matches_baseline_source` and
`TestCriticalRulesBlockHash::test_block_hash_matches_baseline_mirror`:
both assert the block SHA-256 equals the pre-M4 baseline
`fd7f2e457bf63ce0045ec5d7014e9af67c1b46892f49b090334be17bbd2fff0f`.

**Roadmap traceability:** R-087 — "severity-floor block unchanged."

## 6. Per-file test breakdown

```
tests/audit/test_five_axes_overlay.py                                 10 passed
tests/audit/test_axis_column_populated.py                             10 passed
tests/audit/test_drift_axis_inactive_when_no_goal_baseline.py          9 passed
tests/audit/test_severity_floor_unweakened.py                          8 passed
                                                              ─────────────────
                                                                       37 passed
```

## 7. Dependencies satisfied

- **T04.08** (Five Adversarial Axes header inserted) — CONFIRMED. Header at
  `rf-qa-qualitative.md:528` precedes Checklist header at `:546` (see
  CP-P04-T07-T11 §3 V2). TEST-011 verifies this invariant from the test
  surface.
- **T04.09** (15-item checklist body byte-stable) — CONFIRMED. Body
  SHA-256 `78edc7790dc00b49…` at `:546-582` matches pre-M4 baseline.
  TEST-014 indirectly relies on this — strictly-additive insertions
  above the Critical Rules section are accounted for by the
  header-anchored slice locator.
- **T04.10** (severity-floor block byte-stable at `:786-795` pre-M4 /
  `:831-840` post-M4) — CONFIRMED. TEST-014's primary assertion.
- **T04.11** (axis column at Items Reviewed table `:675-714`) —
  CONFIRMED. Header at `:709` enumerates `| # | Check | axis | Result |
  Evidence |`. TEST-012 verifies header presence and column ordering.
- **T04.13** (SKILL.md axis-annotation directive at `:1158-1170`) —
  CONFIRMED via D-0051 PASS. TEST-012's canonical-vocabulary assertion
  also exercises the SKILL.md side indirectly (the closed set is
  identical to the directive's binding).

## 8. Roadmap-item traceability

| R-id | Roadmap intent | Evidence |
|---|---|---|
| R-084 | "TEST-011 axes header before checklist" | `tests/audit/test_five_axes_overlay.py::TestFiveAxesHeaderOrdering::test_ordering_in_source` (and `_mirror`) — line-number-strict ordering check, 528 < 546. |
| R-085 | "TEST-012 axis column non-empty on every row" | `tests/audit/test_axis_column_populated.py::TestAxisColumnHeaderPresent::test_header_column_order_check_axis_result` and `TestAxisColumnRowFormat::test_example_row_enumerates_full_vocabulary` — column present, in canonical position, with the full closed vocabulary enumerated and `N/A` placeholder explicitly forbidden. |
| R-086 | "TEST-013 drift-axis-inactive when no GOAL-baseline" | `tests/audit/test_drift_axis_inactive_when_no_goal_baseline.py::TestDriftFixtureEmitsAnnotation::test_annotation_appears_inside_summary_block` — literal annotation in the Summary block of the canonical GOAL-baseline-absent fixture. |
| R-087 | "TEST-014 severity-floor block unchanged" | `tests/audit/test_severity_floor_unweakened.py::TestCriticalRulesBlockHash::test_block_hash_matches_baseline_source` — block SHA-256 byte-equal to pre-M4 baseline `fd7f2e457bf63ce0…`. |

## 9. Validation (manual reviewer note)

A reviewer can re-run the AC#1 invocation in one shell command:

```
uv run pytest \
  tests/audit/test_five_axes_overlay.py \
  tests/audit/test_axis_column_populated.py \
  tests/audit/test_drift_axis_inactive_when_no_goal_baseline.py \
  tests/audit/test_severity_floor_unweakened.py -v
```

Expected: `37 passed` (0 failures, 0 errors, exit 0). The four files are
isolated by intent (one per checked invariant) so a future regression
will identify the broken invariant by file name without requiring a
full-suite re-bisect.

---

**Status: PASS** — all 4 acceptance criteria satisfied; 37 / 37 tests
green. Ready for T04.15 (MIG-004 single-commit landing).
