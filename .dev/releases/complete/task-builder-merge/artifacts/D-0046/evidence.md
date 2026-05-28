# D-0046 — T04.07 Evidence: `axis` column repositioned between Check and Result

**Task:** T04.07 (Phase 4 — M4 Five Adversarial Axes Overlay)
**Roadmap items:** R-078 (Axis column on Items Reviewed table)
**Date:** 2026-05-17
**Status:** PASS
**Tier:** STANDARD
**Confidence:** [█████████-] 90%

---

## 0. TL;DR

The Items Reviewed table in `src/superclaude/agents/rf-qa-qualitative.md`
now carries the `axis` column **between** `Check` and `Result`, matching
the R-078 contract and the T04.11 grep regex `| .* | axis | .* |`. The
header literal moved from the precursor PR-07 form

```
| # | Check | Result | Axis (PR-07) | Evidence |
```

to the R-078 canonical form

```
| # | Check | axis | Result | Evidence |
```

The example row at `rf-qa-qualitative.md:711` was repositioned to match
(axis vocabulary cell now sits in position 3, Result PASS/FAIL placeholder
in position 4). The HTML comment immediately below the table (lines
713..732) — which encodes the "task-qualitative only; column omitted for
other phases" rule landed in T04.05 — was not touched. The body
reference at line 540 was updated from `\`Axis (PR-07)\`` to `\`axis\`` so
the canonical-rules subsection refers to the column by its new header
literal.

| AC | Statement | Status | Section |
|----|-----------|--------|---------|
| AC#1 | `grep -n "| Check | axis | Result |"` returns the new header | ✅ PASS | §1 |
| AC#2 | Every task-qualitative row has a non-empty Axis value drawn from `{AX-1..AX-5, none}` | ✅ PASS | §2 |
| AC#3 | Non-task-qualitative phases do not include the Axis column | ✅ PASS | §3 |
| AC#4 | Evidence at `D-0046/evidence.md` | ✅ PASS | this file |

Invariant checks (T04.01..T04.06 baselines preserved):

| Invariant | Status | Section |
|---|---|---|
| 15-item checklist body byte-stable (sha256 `78edc7790dc00b49...`) | ✅ PASS | §4 |
| Critical Rules block byte-stable (sha256 `fd7f2e457bf63ce0...`) | ✅ PASS | §4 |
| Five Adversarial Axes header (line 528) precedes Checklist header (line 546) | ✅ PASS | §4 |
| `src/` ↔ `.claude/` parity (`make verify-sync` PASS) | ✅ PASS | §5 |
| PR-07 test suite green (11/11 in `TestPR07AdversarialCategoryNaming`) | ✅ PASS | §6 |

---

## 1. AC#1 — `grep -n "| Check | axis | Result |"` returns the new header

**Command and output:**
```
$ grep -n "| Check | axis | Result |" src/superclaude/agents/rf-qa-qualitative.md
709:| # | Check | axis | Result | Evidence |
```

**T04.11 regex contract (same column-position constraint):**
```
$ grep -nE "\| .* \| axis \| .* \|" src/superclaude/agents/rf-qa-qualitative.md
709:| # | Check | axis | Result | Evidence |
```

The header line at `rf-qa-qualitative.md:709` matches both the literal
T04.07 grep (`| Check | axis | Result |`) and the broader T04.11 regex
(`| .* | axis | .* |`). The header sits inside the "## Output Format
(All Phases)" code-fence at the canonical Items Reviewed location
(line 708 immediately above), per the original COMP-004-M4 edit site.

AC#1 satisfied.

---

## 2. AC#2 — every task-qualitative row has a non-empty Axis value

**Source template (example row at `rf-qa-qualitative.md:711`):**
```
$ sed -n '708,711p' src/superclaude/agents/rf-qa-qualitative.md
## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | [check name] | [AX-1 / AX-2 / AX-3 / AX-4 / AX-5 / none] | PASS / FAIL | [what you verified and how] |
```

The example-row vocabulary placeholder (column 3, "axis") enumerates
the entire closed set `{AX-1, AX-2, AX-3, AX-4, AX-5, none}`. The
column is structurally required (no `[optional]` qualifier, no `N/A`
placeholder).

**Synthetic 15-row task-qualitative fixture
(`.dev/releases/current/task-builder-merge/artifacts/D-0045/fixture-goal-baseline-absent.md`,
updated post-T04.07 to mirror the new column position):**
```
$ grep -nE "^\| [#0-9]+ \| .* \|" .dev/releases/current/task-builder-merge/artifacts/D-0045/fixture-goal-baseline-absent.md | head -3
24:| # | Check | axis | Result | Evidence |
26:| 1 | Gate/command dry-run | none | PASS | Walked every `make` target in the task; all preconditions satisfied; no axis-attributable finding. |
27:| 2 | Project convention compliance | none | PASS | Every edit targets `src/superclaude/...` per CLAUDE.md sync rule; no axis-attributable finding. |
```

**Row-by-row axis-cell census on the fixture (15 rows total — awk scoped to the Items Reviewed table only):**
```
$ awk -F'|' '
    /^## Items Reviewed/ { in_tbl=1; next }
    /^## / && !/^## Items Reviewed/ { in_tbl=0 }
    in_tbl && /^\| [0-9]+ \|/ { gsub(/^ +| +$/, "", $4); print $4 }
  ' .dev/releases/current/task-builder-merge/artifacts/D-0045/fixture-goal-baseline-absent.md \
  | sort | uniq -c | sort -nr
     11 none
      1 AX-5
      1 AX-4
      1 AX-3
      1 AX-2
```
(Scoping the awk to the Items Reviewed section excludes the
unrelated Issues Found table further down the fixture, whose own
column 4 is the Description field, not an axis cell.)

15 rows, 15 non-empty axis values; vocabulary draws only from
`{AX-2, AX-3, AX-4, AX-5, none}` for this fixture (AX-1 INACTIVE
because the fixture has no BUILD_REQUEST.GOAL verbatim baseline, per
the T04.05 `drift-axis-inactive` rule — the literal annotation
appears in the Summary block, not as a cell value).

**Empty-cell sweep (must return zero):**
```
$ awk -F'|' '/^\| [0-9]+ \|/ { gsub(/^ +| +$/, "", $4); if ($4 == "" || $4 == "N/A" || $4 == "n/a" || $4 == "—") print NR": empty/escape cell" }' \
    .dev/releases/current/task-builder-merge/artifacts/D-0045/fixture-goal-baseline-absent.md \
  | wc -l
0
```

Zero rows with empty / `N/A` / `n/a` / `—` axis cells. AC#2 satisfied.

---

## 3. AC#3 — non-task-qualitative phases do not include the Axis column

The phase-omission rule is encoded in the HTML comment at
`rf-qa-qualitative.md:713..732`, immediately below the Items Reviewed
header. The comment is binding spec (no parallel templates exist for
the other phases — the same template is reused with the column
omitted).

**Comment block (verbatim, lines 713..732):**
```
$ sed -n '713,732p' src/superclaude/agents/rf-qa-qualitative.md
<!-- PR-07 canonical annotation rules (see "Canonical annotation rules"
subsection under "Five Adversarial Axes" for the binding spec):
- task-qualitative phase: the Axis column is REQUIRED on every row and
  the only legal cell values are the closed set
  `{AX-1, AX-2, AX-3, AX-4, AX-5, none}` (or their kebab aliases).
- Passing checks (Result = PASS) MUST use the `none` sentinel — meaning
  "the five-axis lens was applied and surfaced nothing." `none` is NOT
  an N/A escape and NOT a permission to skip the lens.
- Failing checks (Result = FAIL) MUST carry one of `AX-1..AX-5` (the
  most-specific axis that fired). `none` on a FAIL row is invalid.
- `N/A`, `n/a`, `—`, and blank are FORBIDDEN values in the Axis column
  for task-qualitative phase.
- If the AX-1 Drift axis is INACTIVE for this review (no BUILD_REQUEST.GOAL
  verbatim baseline available), the lens-level disablement is recorded as
  the literal `drift-axis-inactive` annotation inside the Summary block
  below — NOT as an Axis-column cell value, NOT in the Recommendations
  section. Individual rows continue to use `none` / `AX-2..AX-5` per the
  rules above.
- Non-task-qualitative phases (PRD / TDD / tech-ref / ops-guide / readme /
  report / doc / fix-cycle) omit the Axis column entirely. -->
```

The final bullet (line 731..732) is the AC#3 binding rule: PRD,
TDD, tech-ref, ops-guide, readme, report, doc, and fix-cycle phases
omit the `axis` column entirely. This comment was landed by T04.05
(D-0045) and was not touched by T04.07 — only the table header above
it was repositioned.

**Phase-enumeration sanity:**
```
$ grep -n "prd-qualitative / tdd-qualitative" src/superclaude/agents/rf-qa-qualitative.md
701:**Phase:** [prd-qualitative / tdd-qualitative / tech-ref-qualitative / ops-guide-qualitative / readme-qualitative / report-qualitative / task-qualitative / doc-qualitative / fix-cycle]
```

All nine phase tokens enumerated at line 701; the comment at 731..732
explicitly excludes eight of them from the Axis column, leaving only
`task-qualitative` as the column-bearing phase. AC#3 satisfied.

---

## 4. Invariants — 15-item checklist body + Critical Rules block byte-stable; axes header precedes checklist

**15-item checklist body (lines 546..582):**
```
$ sed -n '546,582p' src/superclaude/agents/rf-qa-qualitative.md | sha256sum
78edc7790dc00b49f050f5a7c27484428195a3af189f665c64f21314236c4bf1  -
$ sed -n '546,582p' src/superclaude/agents/rf-qa-qualitative.md | grep -cE "^[0-9]+\.\s+\*\*"
15
```

Hash matches the T04.05 / D-0045 baseline (`78edc7790dc00b49...`).
Exactly 15 numbered items present. T04.07 did not touch the
checklist body — its edits are confined to the Items Reviewed table
(lines 708..711) and the canonical-rules paragraph reference at
line 540.

**Critical Rules block (lines 834..846):**
```
$ sed -n '834,846p' src/superclaude/agents/rf-qa-qualitative.md | sha256sum
fd7f2e457bf63ce0045ec5d7014e9af67c1b46892f49b090334be17bbd2fff0f  -
$ grep -n "Contradictions are always IMPORTANT or CRITICAL" src/superclaude/agents/rf-qa-qualitative.md
841:6. **Contradictions are always IMPORTANT or CRITICAL** — If two sections say different things about the same topic, that's never minor. Always surface contradictions.
```

Hash matches the T04.05 / D-0045 baseline (`fd7f2e457bf63ce0...`).
Rule #6 (the Contradictions severity floor anchoring AX-2) is
byte-verbatim. T04.10 will re-hash this block post-MIG-004 against
this same baseline.

**Ordering (axes header BEFORE checklist):**
```
$ grep -n "Five Adversarial Axes\|Checklist (15 items)" src/superclaude/agents/rf-qa-qualitative.md | sort -t: -k1n
528:#### Five Adversarial Axes (PR-07 — applied as a sharpening overlay across all 15 checks below)
538:##### Canonical annotation rules (PR-07 — `none` sentinel + `drift-axis-inactive`)
546:#### Checklist (15 items)
```

Axes header at 528 precedes Checklist header at 546. The canonical-
rules subheader at 538 sits between them, still inside the Five
Adversarial Axes block.

---

## 5. Invariant — `make verify-sync` PASS

```
$ make sync-dev
🔄 Syncing src/superclaude/ → .claude/ for local development...
✅ Sync complete.
   Skills:   20 directories
   Agents:   35 files
   Commands: 40 files
   Hooks:    11 files

$ make verify-sync
…
✅ All components in sync.
```

`.claude/agents/rf-qa-qualitative.md` matches
`src/superclaude/agents/rf-qa-qualitative.md` byte-for-byte after
the T04.07 column-position edit.

---

## 6. Invariant — PR-07 test suite green (11/11)

```
$ uv run pytest tests/skills/test_task_builder_merge.py -k "PR07" -v
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
====================== 11 passed, 57 deselected in 0.05s =======================
```

All 11 fixtures pass. `test_axis_annotation_required_in_items_reviewed`
(tests/skills/test_task_builder_merge.py:321..326) was updated under
T04.07 to pin the new R-078 header literal — it now asserts the exact
string `"| # | Check | axis | Result | Evidence |"` rather than the
precursor `"Axis (PR-07)"` token. The semantic check is stricter and
more useful post-T04.07: it verifies column position, header naming,
AND structural shape in a single assertion.

---

## 7. Files changed

```
modified:   src/superclaude/agents/rf-qa-qualitative.md
            (header at line 709 repositioned from
             "| # | Check | Result | Axis (PR-07) | Evidence |"
             to "| # | Check | axis | Result | Evidence |";
             example row at line 711 reordered to match;
             body reference at line 540 updated from
             "`Axis (PR-07)` column" to "`axis` column")
modified:   .claude/agents/rf-qa-qualitative.md
            (synced from src/ via `make sync-dev`)
modified:   tests/skills/test_task_builder_merge.py
            (test_axis_annotation_required_in_items_reviewed now
             pins the R-078 canonical header literal)
modified:   .dev/releases/current/task-builder-merge/artifacts/D-0045/fixture-goal-baseline-absent.md
            (15-row fixture re-columned to the R-078 order to stay
             consistent with the source-of-truth template)
created:    .dev/releases/current/task-builder-merge/artifacts/D-0046/spec.md
created:    .dev/releases/current/task-builder-merge/artifacts/D-0046/evidence.md
```

## 8. Roadmap traceability

| Roadmap row | Title | Wired by T04.07 |
|---|---|---|
| R-078 | Axis column on Items Reviewed table (rf-qa-qualitative.md:675-714) | Header repositioned to `| # | Check | axis | Result | Evidence |` at `rf-qa-qualitative.md:709`; example row reordered at line 711; canonical-rules body reference updated at line 540. |

T04.07 lands the column position; T04.11 (D-0050) re-applies the
COMP-004-M4 edit-site governance against the same site; T04.14
(D-0052) commits the TEST-012 pytest fixture asserting "every row
has one canonical axis value"; T04.15 (MIG-004 / D-0053) lands the
overlay as a single revertable commit.
