# D-0045 — T04.05 Evidence: `none` sentinel + `drift-axis-inactive` Landed

**Task:** T04.05 (Phase 4 — M4 Five Adversarial Axes Overlay)
**Roadmap items:** R-076 (`none` sentinel), R-077 (`drift-axis-inactive` annotation)
**Date:** 2026-05-17
**Status:** PASS
**Tier:** STANDARD
**Confidence:** [████████--] 85%

---

## 0. TL;DR

Landed the binding "Canonical annotation rules" subsection under the
Five Adversarial Axes overlay in
`src/superclaude/agents/rf-qa-qualitative.md` (lines 538..545) and
rewrote the Items Reviewed comment + Summary-block "Axis lens status"
bullet in the output template (lines 711..743) to operationalise the
two new sentinels:

- **`none`** is now the only legal Axis-column value for a task-qualitative
  row whose check PASSED — a positive "lens applied, nothing fired"
  statement, NOT an `N/A` escape (R-076).
- **`drift-axis-inactive`** is the literal Summary-block line that signals
  AX-1 was lens-disabled because no BUILD_REQUEST.GOAL verbatim baseline
  was available — NOT an Axis-column cell, NOT a Recommendations line
  (R-077).

A synthetic `fixture-goal-baseline-absent.md` (sibling to this evidence)
demonstrates the rule end-to-end: every row uses `none` or `AX-2..AX-5`,
no row uses `N/A` or `drift-axis-inactive` as a cell, and the Summary
block carries the literal `drift-axis-inactive` line.

All four ACs for T04.05 satisfied. The 15-item checklist body
(post-edit lines 546..582, 15 numbered items) and the Critical Rules
block (Rule #6 Contradictions floor, lines 834..846) are byte-stable.
`make verify-sync` PASS. PR-07 fixture suite (TestPR07AdversarialCategoryNaming,
11 tests) PASS 11/11.

| AC | Statement | Status | Section |
|----|-----------|--------|---------|
| AC#1 | `grep -n "drift-axis-inactive" rf-qa-qualitative.md` returns annotation rule | ✅ PASS | §1 |
| AC#2 | GOAL-baseline-absent fixture Summary block contains the literal `drift-axis-inactive` | ✅ PASS | §2 |
| AC#3 | Passing check uses `none` sentinel, NOT `N/A` | ✅ PASS | §3 |
| AC#4 | Evidence at `D-0045/evidence.md` | ✅ PASS | this file |

Bonus invariant checks (T04.01..T04.04 baselines preserved):

| Invariant | Status | Section |
|---|---|---|
| 15-item checklist body byte-stable (15 items present) | ✅ PASS | §4 |
| Critical Rules block byte-stable (Rule #6 verbatim) | ✅ PASS | §4 |
| src ↔ .claude/ parity (`make verify-sync` PASS) | ✅ PASS | §5 |
| PR-07 test suite green (11/11) | ✅ PASS | §6 |
| Ordering: axis header (528) before checklist (546) | ✅ PASS | §4 |

---

## 1. AC#1 — `grep -n "drift-axis-inactive"` returns annotation rule

**Command:**
```
grep -n "drift-axis-inactive" src/superclaude/agents/rf-qa-qualitative.md
```

**Output (5 hits — full chain rule landed):**
```
532:- **AX-1 Drift** (kebab alias: `drift`) — … annotate `drift-axis-inactive` in the report and proceed with the other four axes. …
538:##### Canonical annotation rules (PR-07 — `none` sentinel + `drift-axis-inactive`)
544:- **`drift-axis-inactive` Summary-block annotation — drift baseline absent.** … you MUST emit the literal annotation `drift-axis-inactive` on its own line inside the **Summary** block of the QA report (not in Recommendations, not as an Axis-column cell value) …
727:  the literal `drift-axis-inactive` annotation inside the Summary block
741:  `drift-axis-inactive` here on its own when no BUILD_REQUEST.GOAL
```

**Interpretation:** The grep returns the binding annotation rule at
line 544 inside the new "Canonical annotation rules" subsection at
line 538 (under the Five Adversarial Axes overlay at line 528). The
rule is reinforced in the output-template HTML comment at line 727
and in the Summary-block placeholder at line 741. AC#1 satisfied.

The rule explicitly mandates:
- emission inside the **Summary** block (not Recommendations);
- as a literal single-line annotation;
- NOT as an Axis-column cell value;
- NOT encoded as `Axis = N/A`.

This is the canonical rule that TEST-013 (T04.14) will assert against
in pytest. T04.05 lands the rule; T04.14 commits the pytest fixture.

---

## 2. AC#2 — GOAL-baseline-absent fixture Summary block contains literal annotation

**Fixture path:** `.dev/releases/current/task-builder-merge/artifacts/D-0045/fixture-goal-baseline-absent.md`

**Summary-block excerpt (verbatim):**
```
## Summary
- Checks passed: 11 / 15
- Checks failed: 4
- Critical issues: 1
- Issues fixed in-place: 0
- Axis lens status: drift-axis-inactive
```

**Grep verification:**
```
$ awk '/^## Summary$/,/^## Issues Found/' .dev/releases/current/task-builder-merge/artifacts/D-0045/fixture-goal-baseline-absent.md \
    | grep -c "drift-axis-inactive"
1
```

The fixture emits the literal `drift-axis-inactive` token exactly
once inside the Summary block, on its own bullet line, per the rule
at rf-qa-qualitative.md:544 / :741. The fixture also demonstrates
the negative invariants:

- The Axis column for the 15 reviewed rows uses only `{none, AX-2, AX-3, AX-4, AX-5}`.
- AX-1 never appears as a cell value (AX-1 is INACTIVE for this
  review, so the AX-1 lens fired no findings).
- `N/A` / `n/a` / blank never appear in the Axis column.
- `drift-axis-inactive` never appears as an Axis-column cell value.
- `drift-axis-inactive` never appears in the Recommendations section.

AC#2 satisfied.

---

## 3. AC#3 — Passing check uses `none` sentinel, NOT `N/A`

**Source evidence — canonical rule (rf-qa-qualitative.md:542):**
```
- **`none` sentinel — passing check that surfaced nothing.** Use
  `none` when the check at this row PASSED and the five-axis lens
  surfaced no finding. `none` is a positive statement that all five
  axes were applied and none fired; it is NOT an `N/A` escape, and
  it is NOT a permission to skip the axis lens for that row. A row
  with Result = `PASS` and Axis = `none` means: "I ran every axis
  against this check and recorded no axis-attributable finding." A
  row with Result = `FAIL` MUST carry one of `AX-1..AX-5` (the
  most-specific axis that fired) — `none` on a FAIL row is invalid.
```

**Source evidence — `N/A` forbidden (rf-qa-qualitative.md:543):**
```
- **`N/A` is forbidden in the Axis column for task-qualitative phase.**
  Do not write `N/A`, `n/a`, `—`, blank, or any other escape value
  in the Axis column when running task-qualitative. The Axis column
  is only present for task-qualitative reviews (see comment under
  Items Reviewed); other phases omit the column entirely rather than
  filling it with `N/A`.
```

**Source evidence — Items Reviewed example row updated (rf-qa-qualitative.md:711):**
```
| 1 | [check name] | PASS / FAIL | [AX-1 / AX-2 / AX-3 / AX-4 / AX-5 / none] | [what you verified and how] |
```
The placeholder vocabulary now reads `{AX-1..AX-5, none}` — the
prior placeholder `n/a` token has been removed from the example row.

**Source evidence — Items Reviewed comment rewritten (rf-qa-qualitative.md:713..733):**
```
<!-- PR-07 canonical annotation rules …
- Passing checks (Result = PASS) MUST use the `none` sentinel — meaning
  "the five-axis lens was applied and surfaced nothing." `none` is NOT
  an N/A escape and NOT a permission to skip the lens.
- `N/A`, `n/a`, `—`, and blank are FORBIDDEN values in the Axis column
  for task-qualitative phase. -->
```

**Fixture demonstration:**
The synthetic fixture has 11 PASS rows, each annotated `none`. Zero
rows use `N/A`, `n/a`, `—`, or blank in the Axis column.

```
$ grep -cE "^\| [0-9]+ \| .* \| PASS \| none \|" .dev/releases/current/task-builder-merge/artifacts/D-0045/fixture-goal-baseline-absent.md
11
$ grep -cE "^\| [0-9]+ \| .* \| PASS \| (N/A|n/a|—|) \|" .dev/releases/current/task-builder-merge/artifacts/D-0045/fixture-goal-baseline-absent.md
0
```

AC#3 satisfied.

---

## 4. Invariant — 15-item checklist body byte-stable, Critical Rules unchanged

**Post-edit anchors:**
```
$ grep -n "^#### Checklist (15 items)\|^### Adaptation Guidance\|^## Critical Rules" src/superclaude/agents/rf-qa-qualitative.md
546:#### Checklist (15 items)
583:### Adaptation Guidance (NO check may be marked N/A — adapt instead)
834:## Critical Rules
```

**15-item body content (lines 546..582):**
```
$ sed -n '546,582p' src/superclaude/agents/rf-qa-qualitative.md | grep -cE "^[0-9]+\.\s+\*\*"
15
$ sed -n '546,582p' src/superclaude/agents/rf-qa-qualitative.md | sha256sum
78edc7790dc00b49f050f5a7c27484428195a3af189f665c64f21314236c4bf1  -
```
Exactly 15 numbered items present. T04.08 will capture this hash as
its baseline (per the phase-4 plan T04.08 step 1) and T04.09 will
re-diff post-MIG-004 — both should match this digest.

**Critical Rules block (lines 834..846):**
```
$ sed -n '834,846p' src/superclaude/agents/rf-qa-qualitative.md | sha256sum
fd7f2e457bf63ce0045ec5d7014e9af67c1b46892f49b090334be17bbd2fff0f  -
$ grep -n "Contradictions are always IMPORTANT or CRITICAL" src/superclaude/agents/rf-qa-qualitative.md
841:6. **Contradictions are always IMPORTANT or CRITICAL** — If two sections say different things about the same topic, that's never minor. Always surface contradictions.
```
Rule #6 (the Contradictions severity floor that AX-2 anchors to)
is byte-verbatim and was not touched by T04.05. T04.10 will re-hash
this block post-MIG-004 and assert zero drift.

**Ordering (axes header BEFORE checklist):**
```
$ grep -n "Five Adversarial Axes\|Checklist (15 items)" src/superclaude/agents/rf-qa-qualitative.md | sort -t: -k1n
528:#### Five Adversarial Axes (PR-07 — applied as a sharpening overlay across all 15 checks below)
546:#### Checklist (15 items)
```
Axes header at line 528 precedes Checklist header at line 546. The
new "Canonical annotation rules" subheader sits at line 538, still
inside the Five Adversarial Axes block and still before the Checklist
block.

---

## 5. Invariant — `make verify-sync` PASS

```
$ make sync-dev   # propagated src/ → .claude/
🔄 Syncing src/superclaude/ → .claude/ for local development...
✅ Sync complete.

$ make verify-sync
…
✅ All components in sync.
```

`.claude/agents/rf-qa-qualitative.md` matches
`src/superclaude/agents/rf-qa-qualitative.md` byte-for-byte after
the T04.05 edits.

---

## 6. Invariant — PR-07 test suite green (11/11)

```
$ uv run pytest tests/skills/test_task_builder_merge.py \
    -k "PR07 or pr_07 or pr07 or drift or AdversarialAxes or axis" -v
…
tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_rf_qa_qualitative_contains_axis[Drift] PASSED
tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_rf_qa_qualitative_contains_axis[Contradictions] PASSED
tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_rf_qa_qualitative_contains_axis[Omissions] PASSED
tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_rf_qa_qualitative_contains_axis[Weakened criteria] PASSED
tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_rf_qa_qualitative_contains_axis[Invented content] PASSED
tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_axes_are_overlay_not_replacement PASSED
tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_drift_baseline_requirement PASSED
tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_axis_annotation_required_in_items_reviewed PASSED
tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_skill_references_5_axis_lens PASSED
tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_invented_content_axis_is_evidence_bound PASSED
tests/skills/test_task_builder_merge.py::TestPR07AdversarialCategoryNaming::test_weakened_axis_anti_inflation PASSED
====================== 11 passed, 57 deselected in 0.02s =======================
```

All 11 PR-07 fixtures green. The existing
`test_drift_baseline_requirement` (line 312..319) still asserts the
`drift-axis-inactive` literal and still passes — the literal appears
at 5 distinct locations in the file post-edit (counted in §1).

---

## 7. Files changed

```
modified:   src/superclaude/agents/rf-qa-qualitative.md
            (insert "Canonical annotation rules" subsection after AX-5
             entry; rewrite Items Reviewed example row and HTML
             comment; add "Axis lens status" bullet to Summary block)
modified:   .claude/agents/rf-qa-qualitative.md
            (synced from src/ via `make sync-dev`)
created:    .dev/releases/current/task-builder-merge/artifacts/D-0045/spec.md
created:    .dev/releases/current/task-builder-merge/artifacts/D-0045/evidence.md
created:    .dev/releases/current/task-builder-merge/artifacts/D-0045/fixture-goal-baseline-absent.md
```

## 8. Roadmap traceability

| Roadmap row | Title | Wired by T04.05 |
|---|---|---|
| R-076 | `none` sentinel | Canonical annotation rules §`none` (line 542) + Items Reviewed comment (line 718..720) |
| R-077 | `drift-axis-inactive` annotation | Canonical annotation rules §drift (line 544) + Summary-block bullet (line 740..743) |

T04.05 lands the spec; T04.14 commits the pytest fixture TEST-013
that asserts these rules in CI; T04.15 (MIG-004) lands the whole
overlay as a single revertable commit.
