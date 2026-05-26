# D-0050 — T04.11 Evidence: COMP-004-M4 axis-column site governance applied at 675-714

**Task:** T04.11 (Phase 4 — M4 Five Adversarial Axes Overlay)
**Roadmap items:** R-082 (COMP-004-M4 — rf-qa-qualitative.md axis-column site)
**Date:** 2026-05-17
**Status:** PASS
**Tier:** STANDARD
**Confidence:** [████████--] 85%

---

## 0. TL;DR

The COMP-004-M4 edit-site governance contract (R-082) is now binding
against `src/superclaude/agents/rf-qa-qualitative.md:675..714`. The
R-078 column-shape edit from T04.07 / D-0046 sits inside that range
(header at line 709, example row at line 711), and the per-row
uniqueness invariant declared in `D-0050/spec.md §3` holds against the
canonical fixture from T04.05 / D-0045.

T04.11 is a governance + verification task: no source-file bytes
change under D-0050. The 15-item checklist body (lines 546..582) and
the Critical Rules block (lines 834..846) remain byte-identical to
their T04.05 / T04.07 baselines.

| AC  | Statement                                                                                  | Status   | Section |
| --- | ------------------------------------------------------------------------------------------ | -------- | ------- |
| AC#1 | `grep -n "\| .* \| axis \| .* \|"` returns header line in [675, 714]                       | ✅ PASS | §1      |
| AC#2 | Every task-qualitative row has a non-empty axis value drawn from `{AX-1..AX-5, none}`    | ✅ PASS | §2      |
| AC#3 | Evidence at `D-0050/evidence.md`                                                           | ✅ PASS | this file |
| AC#4 | Edit confined to lines 675-714                                                             | ✅ PASS | §3      |

Invariant checks (T04.05 / T04.07 baselines preserved by R-082 governance):

| Invariant                                                              | Status   | Section |
| ---------------------------------------------------------------------- | -------- | ------- |
| 15-item checklist body byte-stable (sha256 `78edc7790dc00b49...`)      | ✅ PASS | §4      |
| Critical Rules block byte-stable (sha256 `fd7f2e457bf63ce0...`)        | ✅ PASS | §4      |
| `src/` ↔ `.claude/` parity (`diff -q` clean)                          | ✅ PASS | §5      |
| PR-07 test suite green (11/11 in `TestPR07AdversarialCategoryNaming`) | ✅ PASS | §6      |
| Roadmap label `COMP-004-M4` resolves to `roadmap.md:276`              | ✅ PASS | §7      |

---

## 1. AC#1 — `grep -n "| .* | axis | .* |"` returns header line in [675, 714]

**Command and output (verbatim, run 2026-05-17 against the as-landed source):**
```
$ grep -nE "\| .* \| axis \| .* \|" src/superclaude/agents/rf-qa-qualitative.md
709:| # | Check | axis | Result | Evidence |
```

**Range check:**
```
$ awk -F: 'NR==1 { if ($1 >= 675 && $1 <= 714) print "in-range: line " $1; else print "out-of-range: line " $1 }' \
    <(grep -nE "\| .* \| axis \| .* \|" src/superclaude/agents/rf-qa-qualitative.md)
in-range: line 709
```

Line 709 sits inside the [675, 714] window declared by the R-082
contract (`roadmap.md:276` and `phase-4-tasklist.md:495`). The
T04.11-specified regex `| .* | axis | .* |` is broader than the
T04.07 literal `| Check | axis | Result |` — both grep against the
same line, but the regex confirms COMP-004-M4 governance against any
future column-shape change that preserves the axis cell in the
between-Check-and-Result position without renaming neighbour columns.

AC#1 satisfied.

---

## 2. AC#2 — every task-qualitative row has a non-empty axis value from `{AX-1..AX-5, none}`

**Source template (`rf-qa-qualitative.md:708..711`):**
```
$ sed -n '708,711p' src/superclaude/agents/rf-qa-qualitative.md
## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | [check name] | [AX-1 / AX-2 / AX-3 / AX-4 / AX-5 / none] | PASS / FAIL | [what you verified and how] |
```

The example row at line 711 enumerates the full closed vocabulary
`{AX-1, AX-2, AX-3, AX-4, AX-5, none}` in the axis cell (column 3).
No `[optional]` qualifier, no `N/A` placeholder — the column is
structurally required for task-qualitative rows.

**Canonical 15-row fixture
(`.dev/releases/current/task-builder-merge/artifacts/D-0045/fixture-goal-baseline-absent.md`,
the source of truth for "axis column populated"):**

Row-by-row axis-cell census (awk scoped to the Items Reviewed table only):
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

15 rows total (11 + 1 + 1 + 1 + 1 = 15). Every cell is a member of
the closed vocabulary `{AX-1, AX-2, AX-3, AX-4, AX-5, none}`. AX-1
does not appear in the fixture because the fixture is the
GOAL-baseline-absent scenario (T04.05 / D-0045) — AX-1 Drift cannot
fire without a BUILD_REQUEST.GOAL verbatim baseline, so rows that
would have been AX-1 record `none` plus the `drift-axis-inactive`
Summary annotation per the canonical-rules block at
`rf-qa-qualitative.md:725..730`.

**Empty / escape-value sweep (must return zero):**
```
$ awk -F'|' '/^\| [0-9]+ \|/ {
    gsub(/^ +| +$/, "", $4);
    if ($4 == "" || $4 == "N/A" || $4 == "n/a" || $4 == "—") print NR": empty/escape cell"
  }' .dev/releases/current/task-builder-merge/artifacts/D-0045/fixture-goal-baseline-absent.md \
  | wc -l
0
```

Zero rows with blank / `N/A` / `n/a` / `—` axis cells. The COMP-004-M4
per-row uniqueness invariant (D-0050/spec.md §3) holds against the
fixture as authored. AC#2 satisfied.

---

## 3. AC#4 — edit confined to lines 675-714

T04.11 is a governance + verification task; no source-file edit
lands under D-0050. The R-078 column-shape edit landed by T04.07 /
D-0046 is the only mutation against this site since the COMP-004-M4
label was declared.

**Line-level locus of every COMP-004-M4-relevant edit since T04.05:**

| Date       | Task   | Lines touched | Description                                                    |
| ---------- | ------ | ------------- | -------------------------------------------------------------- |
| 2026-05-17 | T04.05 | 713..732      | HTML canonical-rules comment block (D-0045)                    |
| 2026-05-17 | T04.07 | 708..711      | Items Reviewed header + example row repositioned (D-0046)      |
| 2026-05-17 | T04.07 | 540           | Body reference updated from `Axis (PR-07)` to `axis` (D-0046)  |
| 2026-05-17 | T04.11 | (none)        | Governance-only: no source-file mutation (D-0050, this artifact) |

Line 540 sits outside [675, 714] but is NOT a COMP-004-M4 edit — it
is a downstream prose reference inside the Canonical annotation
rules subsection (which itself lives at lines 538..545 in the Five
Adversarial Axes header block, not in the Items Reviewed table). The
roadmap acceptance string for R-082 (`axis-column-header:present-in-table;
parse:one-axis-value-per-row`) scopes COMP-004-M4 strictly to the
table site at 708..711 inside the [675, 714] window; the line-540
reference is governed by R-076 (canonical annotation rules block),
not R-082.

**As-landed extent of the COMP-004-M4 site (verbatim, current file):**
```
$ sed -n '708,711p' src/superclaude/agents/rf-qa-qualitative.md
## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | [check name] | [AX-1 / AX-2 / AX-3 / AX-4 / AX-5 / none] | PASS / FAIL | [what you verified and how] |
```

All four lines (708, 709, 710, 711) sit inside the [675, 714] R-082
window. AC#4 satisfied.

---

## 4. Invariant — 15-item checklist body + Critical Rules block byte-stable

**15-item checklist body (lines 546..582):**
```
$ sed -n '546,582p' src/superclaude/agents/rf-qa-qualitative.md | sha256sum
78edc7790dc00b49f050f5a7c27484428195a3af189f665c64f21314236c4bf1  -
$ sed -n '546,582p' src/superclaude/agents/rf-qa-qualitative.md | grep -cE "^[0-9]+\.\s+\*\*"
15
```

Hash matches the T04.05 / D-0045 + T04.07 / D-0046 baseline
(`78edc7790dc00b49...`). Exactly 15 numbered checklist items
present. The COMP-004-M4 governance step did not touch the checklist
body (out of scope for R-082).

**Critical Rules block (lines 834..846):**
```
$ sed -n '834,846p' src/superclaude/agents/rf-qa-qualitative.md | sha256sum
fd7f2e457bf63ce0045ec5d7014e9af67c1b46892f49b090334be17bbd2fff0f  -
$ grep -n "Contradictions are always IMPORTANT or CRITICAL" src/superclaude/agents/rf-qa-qualitative.md
841:6. **Contradictions are always IMPORTANT or CRITICAL** — If two sections say different things about the same topic, that's never minor. Always surface contradictions.
```

Hash matches the T04.05 + T04.07 baseline (`fd7f2e457bf63ce0...`).
Rule #6 (the Contradictions severity floor anchoring AX-2) is
byte-verbatim. T04.10 / D-0049 confirms the same hash from the
opposite direction (Critical Rules block pre/post M4 byte-diff = 0);
D-0050 (this artifact) re-confirms it from the COMP-004-M4
governance angle to document that the R-082 governance does NOT
weaken the severity floor.

---

## 5. Invariant — `src/` ↔ `.claude/` parity

```
$ diff -q src/superclaude/agents/rf-qa-qualitative.md .claude/agents/rf-qa-qualitative.md
$ grep -nE "\| .* \| axis \| .* \|" .claude/agents/rf-qa-qualitative.md
709:| # | Check | axis | Result | Evidence |
```

`diff -q` is silent (files identical). The R-082 contract holds
byte-for-byte against the `.claude/` mirror at the same line number.
T04.15 / MIG-004 will re-run `make verify-sync` as the formal
landing gate; T04.11 confirms parity in the as-landed state.

---

## 6. Invariant — PR-07 test suite green (11/11 in `TestPR07AdversarialCategoryNaming`)

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
pins the R-078 canonical header literal (
`"| # | Check | axis | Result | Evidence |"`) and continues to pass
under the R-082 governance lock. T04.14 / D-0052 will add the
TEST-012 fixture `tests/audit/test_axis_column_populated.py` that
codifies the per-row uniqueness invariant declared in
`D-0050/spec.md §3` — this evidence file pre-stages the awk pivot
the new fixture will run as a Python parser.

---

## 7. Invariant — roadmap label `COMP-004-M4` resolves cleanly

```
$ grep -n "COMP-004-M4" .dev/releases/current/task-builder-merge/roadmap.md
276:|13|COMP-004-M4|rf-qa-qualitative.md axis-column site (675-714)|Modify Items Reviewed table at rf-qa-qualitative.md:675-714 to add `axis` column between `Check` and `Result`|rf-qa-qualitative.md|FR-CONV.4|axis-column-header:present-in-table; parse:one-axis-value-per-row|S|P0|
```

The `COMP-004-M4` label appears exactly once in `roadmap.md`, at line
276, row 13 of the M4 component table. The label resolves to the
byte range `rf-qa-qualitative.md:675-714` (matching the
phase-4-tasklist.md T04.11 task body at line 495 and §2 of
D-0050/spec.md). No naming collisions with other M-series components
(`COMP-001-M4`, etc.).

```
$ grep -nE "COMP-00[0-9]+-M4" .dev/releases/current/task-builder-merge/roadmap.md
276:|13|COMP-004-M4|rf-qa-qualitative.md axis-column site (675-714)|Modify Items Reviewed table at rf-qa-qualitative.md:675-714 to add `axis` column between `Check` and `Result`|rf-qa-qualitative.md|FR-CONV.4|axis-column-header:present-in-table; parse:one-axis-value-per-row|S|P0|
277:|14|COMP-001-M4|SKILL.md task-qualitative prompt axis directive (961)|Add axis-annotation directive at SKILL.md:961 in Task-Qualitative prompt|SKILL.md|FR-CONV.4|grep-Axis-in-SKILL.md:~961-returns-≥1-match; directive:instructs-annotation-per-row|S|P0|
```

`COMP-004-M4` (this artifact) and `COMP-001-M4` (T04.13 / D-0051,
SKILL.md axis directive) sit on adjacent rows and address distinct
edit sites; no overlap.

---

## 8. Files changed / created

```
created:    .dev/releases/current/task-builder-merge/artifacts/D-0050/spec.md
            (COMP-004-M4 edit-site governance contract — binding for R-082)
created:    .dev/releases/current/task-builder-merge/artifacts/D-0050/evidence.md
            (this file — observed-state proof against the four ACs)

unchanged:  src/superclaude/agents/rf-qa-qualitative.md
            (no source bytes mutate under T04.11; the as-landed state
             from T04.07 / D-0046 already satisfies R-082)
unchanged:  .claude/agents/rf-qa-qualitative.md
            (still byte-identical to src/ per §5)
```

---

## 9. Roadmap traceability

| Roadmap row                                | Title                                                       | Wired by T04.11                                                                                                    |
| ------------------------------------------ | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| R-082 (roadmap.md row 13 — COMP-004-M4)    | rf-qa-qualitative.md axis-column site (675-714)            | COMP-004-M4 label declared binding against `src/superclaude/agents/rf-qa-qualitative.md:675..714`; per-row uniqueness invariant codified in `D-0050/spec.md §3`; grep + parse contracts evidenced in §1, §2 above. |

T04.07 / R-078 / D-0046 lands the column position (R-078 column-shape
contract). T04.11 / R-082 / D-0050 (this artifact) locks the edit-site
governance (COMP-004-M4 label + per-row uniqueness invariant).
T04.12 (CP-P04-T07-T11) consumes both D-0046 and D-0050 as the
mid-phase gate. T04.14 (D-0052) commits the TEST-012 pytest fixture
asserting the per-row invariant. T04.15 (MIG-004 / D-0053) lands the
overlay as a single revertable commit and cites both D-0046 and
D-0050 in the COMP-004-M4 governance trail.
