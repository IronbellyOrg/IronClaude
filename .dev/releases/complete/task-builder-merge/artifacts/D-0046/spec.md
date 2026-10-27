# D-0046 — T04.07 Spec: Add `axis` column to Items Reviewed table

**Task:** T04.07 (Phase 4 — M4 Five Adversarial Axes Overlay)
**Roadmap items:** R-078 (Axis column on Items Reviewed table)
**Date:** 2026-05-17
**Tier:** STANDARD
**Confidence:** [█████████-] 90%

---

## 1. Scope

Position the `axis` column in the Items Reviewed table inside the
"Output Format (All Phases)" block of
`src/superclaude/agents/rf-qa-qualitative.md` so that:

- The header line reads `| # | Check | axis | Result | Evidence |` —
  i.e. the `axis` column sits **between** `Check` and `Result`,
  satisfying the R-078 / T04.11 grep contract
  `grep -n "| .* | axis | .* |"`.
- Every task-qualitative row carries one value drawn from the closed
  vocabulary `{AX-1, AX-2, AX-3, AX-4, AX-5, none}` (kebab aliases
  `{drift, contradictions, omissions, weakened-criteria,
  invented-content, none}`) — `none` for PASS, `AX-1..AX-5` for FAIL,
  per the canonical annotation rules landed in T04.05 / D-0045.
- Non-task-qualitative phases (PRD / TDD / tech-ref / ops-guide /
  readme / report / doc / fix-cycle) omit the column entirely — this
  is enforced by the HTML comment beneath the table, not by a separate
  template variant.

A precursor PR-07 intent-port (commit `0abf897`) already added an
`Axis (PR-07)` column **after** `Result`. This task moves the column
to its R-078-mandated position and renames the header to the canonical
lowercase `axis` token. The change is overlay-only: no new conditional
code path; no impact on the 15-item checklist body (lines 546..582)
or the Critical Rules block (lines 834..846).

## 2. Column position contract

**Before T04.07 (precursor PR-07 placement, 2026-05-15):**
```
| # | Check | Result | Axis (PR-07) | Evidence |
|---|-------|--------|--------------|----------|
| 1 | [check name] | PASS / FAIL | [AX-1 / AX-2 / AX-3 / AX-4 / AX-5 / none] | [what you verified and how] |
```

**After T04.07 (R-078 placement, this task):**
```
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | [check name] | [AX-1 / AX-2 / AX-3 / AX-4 / AX-5 / none] | PASS / FAIL | [what you verified and how] |
```

The column moves from position 4 (between `Result` and `Evidence`)
to position 3 (between `Check` and `Result`). The header literal
changes from `Axis (PR-07)` to `axis` to match the R-078 contract.
The PR-07 attribution lives in the section header `#### Five
Adversarial Axes (PR-07 — applied as a sharpening overlay across all
15 checks below)` at line 528 and in the canonical-rules subheader
`##### Canonical annotation rules (PR-07 — \`none\` sentinel + \`drift-axis-inactive\`)`
at line 538 — it is not duplicated in the column header.

## 3. Phase-omission contract

The HTML comment immediately below the table (lines 713..732) is the
binding spec for which phases carry the column:

- `task-qualitative` — Axis column REQUIRED on every row.
- All other phases (`prd-qualitative`, `tdd-qualitative`,
  `tech-ref-qualitative`, `ops-guide-qualitative`,
  `readme-qualitative`, `report-qualitative`, `doc-qualitative`,
  `fix-cycle`) — column OMITTED entirely.

The comment block is unchanged by T04.07 (already landed by T04.05 /
D-0045). Only the header line and the example row are repositioned.

## 4. Acceptance Criteria (from phase-4-tasklist.md T04.07)

| AC | Statement | Evidence section |
|----|-----------|------------------|
| AC#1 | `grep -n "| Check | axis | Result |" rf-qa-qualitative.md` (or equivalent header line) returns the new table header | evidence.md §1 |
| AC#2 | Every task-qualitative row in the Items Reviewed table has a non-empty Axis value | evidence.md §2 |
| AC#3 | Non-task-qualitative phase tables do not include the Axis column | evidence.md §3 |
| AC#4 | Evidence at `D-0046/evidence.md` | evidence.md (this artifact) |

## 5. Invariants preserved

- 15-item checklist body (lines 546..582) byte-stable — T04.07 edits
  the template at lines 708..711, well outside the checklist range.
- Critical Rules block (lines 834..846) byte-stable — Rule #6
  Contradictions floor unchanged.
- `src/` ↔ `.claude/` parity via `make verify-sync`.
- PR-07 test suite (`TestPR07AdversarialCategoryNaming`, 11 tests)
  remains green; the legacy `test_axis_annotation_required_in_items_reviewed`
  assertion is updated to pin the new R-078 header literal.
- Canonical annotation rules subsection (lines 538..545) untouched —
  the `none` sentinel + `drift-axis-inactive` semantics land via
  T04.05 / D-0045, not this task.

## 6. Rollback

Revertable by restoring the previous header to `| # | Check | Result |
Axis (PR-07) | Evidence |` and swapping the example-row cells back to
their pre-T04.07 order. The 15-item checklist body and the Critical
Rules block need no revert. The canonical annotation rules subsection
needs no revert (T04.05 / D-0045 is independent).

## 7. Out of scope (deferred to other phase-4 tasks)

- Edit COMP-004-M4 axis-column site at 675-714 — T04.11 (D-0050)
  re-applies the same edit under the COMP-004-M4 edit-site
  governance; T04.07 lands the column position itself.
- Insert `### Five Adversarial Axes` header subsection — T04.08
  (D-0047). Already present at line 528 from the PR-07 intent-port;
  T04.08 verifies ordering vs. the Checklist header.
- TEST-012 axis-column-populated pytest fixture — T04.14 (D-0052).
- MIG-004 single-commit landing — T04.15 (D-0053).
