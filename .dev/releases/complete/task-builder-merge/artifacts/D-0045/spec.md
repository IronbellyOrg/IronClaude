# D-0045 — T04.05 Spec: `none` sentinel + `drift-axis-inactive` annotation

**Task:** T04.05 (Phase 4 — M4 Five Adversarial Axes Overlay)
**Roadmap items:** R-076 (`none` sentinel), R-077 (`drift-axis-inactive` annotation)
**Date:** 2026-05-17
**Tier:** STANDARD
**Confidence:** [████████--] 85%

---

## 1. Scope

Land the canonical annotation rules for the PR-07 Five Adversarial
Axes overlay in `src/superclaude/agents/rf-qa-qualitative.md`:

- **`none` sentinel** — the only legal Axis-column value for a passing
  task-qualitative check that surfaced no axis-attributable finding.
  Not an `N/A` escape; not a permission to skip the five-axis lens.
- **`drift-axis-inactive` annotation** — a single-line annotation
  emitted on its own line inside the **Summary** block of the QA
  report when no BUILD_REQUEST.GOAL verbatim baseline is available
  for the review, signalling that AX-1 Drift was lens-disabled for
  this run. Not encoded as an Axis-column cell value; not placed in
  the Recommendations section.
- **Canonical annotation rules subsection** — a binding, grep-able
  rule block under the Five Adversarial Axes header that ties the
  closed vocabulary `{AX-1..AX-5, none}` to the column and the
  `drift-axis-inactive` annotation to the Summary block.

## 2. Vocabulary (closed set)

| Token        | Phase scope          | Cell legality                                    |
|--------------|----------------------|--------------------------------------------------|
| `AX-1`       | task-qualitative     | required cell value when Result = FAIL and drift |
| `AX-2`       | task-qualitative     | required cell value when Result = FAIL           |
| `AX-3`       | task-qualitative     | required cell value when Result = FAIL           |
| `AX-4`       | task-qualitative     | required cell value when Result = FAIL           |
| `AX-5`       | task-qualitative     | required cell value when Result = FAIL           |
| `none`       | task-qualitative     | required cell value when Result = PASS           |
| `N/A` / `n/a`| task-qualitative     | FORBIDDEN — emit nothing if drift inactive       |
| `drift-axis-inactive` | task-qualitative | Summary block line — NOT a cell value         |

Non-task-qualitative phases omit the Axis column entirely.

## 3. Acceptance Criteria (from phase-4-tasklist.md)

| AC | Statement | Evidence section |
|----|-----------|------------------|
| AC#1 | `grep -n "drift-axis-inactive" src/superclaude/agents/rf-qa-qualitative.md` returns annotation rule | evidence.md §1 |
| AC#2 | GOAL-baseline-absent fixture's Summary block contains the literal `drift-axis-inactive` annotation | evidence.md §2 |
| AC#3 | Passing check uses `none` sentinel, NOT `N/A` | evidence.md §3 |
| AC#4 | Evidence at `D-0045/evidence.md` | evidence.md (this artifact) |

## 4. Invariants preserved (carry-over from T04.01..T04.04)

- 15-item checklist body byte-stable.
- Critical Rules block (Rule #6 Contradictions floor) byte-stable.
- src ↔ .claude/ parity intact via `make verify-sync`.
- PR-07 test suite green (11/11 in TestPR07AdversarialCategoryNaming).

## 5. Rollback

Revertable by removing the "Canonical annotation rules" subsection
(528..547) and the rewritten Items Reviewed comment + Summary-block
"Axis lens status" bullet. The 15-item checklist body and the
Critical Rules block remain untouched and require no revert.
