# D-0050 — T04.11 Spec: COMP-004-M4 axis-column site (675-714)

**Task:** T04.11 (Phase 4 — M4 Five Adversarial Axes Overlay)
**Roadmap items:** R-082 (COMP-004-M4 — rf-qa-qualitative.md axis-column site)
**Date:** 2026-05-17
**Tier:** STANDARD
**Confidence:** [████████--] 85%

---

## 1. Scope

T04.11 is the **COMP-004-M4 edit-site governance** step that locks the
R-082 contract against the Items Reviewed table edit applied by T04.07
(R-078) at `src/superclaude/agents/rf-qa-qualitative.md:675..714`.

R-082 and R-078 are intentionally co-targeted on the same edit site:

- **R-078 (T04.07 / D-0046)** carries the *column-design* contract —
  header literal `| # | Check | axis | Result | Evidence |`, axis cell
  sits between `Check` and `Result`, vocabulary draws from the closed
  set `{AX-1, AX-2, AX-3, AX-4, AX-5, none}`, phase-omission rule
  binding via the HTML comment immediately below the table.
- **R-082 (T04.11 / D-0050, this artifact)** carries the *edit-site
  governance* contract — the canonical lookup label `COMP-004-M4`
  from `roadmap.md:276` is fixed to the byte range
  `rf-qa-qualitative.md:675..714`, every future M-series edit that
  touches the Items Reviewed table must reference COMP-004-M4 (not
  free-form coordinates), and the parser-level invariant
  "one axis value per row" is anchored as a binding acceptance check.

The split is deliberate. R-078 protects the *shape* of the column;
R-082 protects the *location and the per-row uniqueness invariant*.
The two roadmap items together prevent (a) future PRs from moving the
column back to position 4 (R-078) and (b) future PRs from splitting
the axis cell across multi-axis tuples or comma-lists (R-082). The
COMP-004-M4 label is the durable identifier that any later M5 / M7
change must cite when re-editing this site.

T04.11 itself does not modify the source file — the column already
sits in its R-078 position from T04.07. T04.11 (i) declares the
COMP-004-M4 label binding against the current site, (ii) re-runs the
grep + parse contracts against the as-landed state to confirm zero
drift since T04.07, (iii) records the per-row uniqueness invariant
formally in this spec, and (iv) emits D-0050 evidence the T04.12
mid-phase checkpoint will consume.

## 2. COMP-004-M4 edit-site contract

**Canonical label:** `COMP-004-M4`
**Source-of-truth coordinates:** `src/superclaude/agents/rf-qa-qualitative.md:675..714`
**Roadmap row:** `roadmap.md:276` (M4 component table row 13)
**Roadmap acceptance string:** `axis-column-header:present-in-table; parse:one-axis-value-per-row`

The COMP-004-M4 site spans the Items Reviewed section heading at line
708 (`## Items Reviewed`), the table header at 709, the column
divider at 710, the example template row at 711, and the HTML
canonical-rules comment block at 713..732 (which extends past the
nominal 714 ceiling but is anchored by line-708 + line-709). Edits
within COMP-004-M4 are confined to those lines; the surrounding
"Overall Verdict" line (706) and "Summary" subheading (735) are NOT
part of the site.

The label is referenced by name in:

- `roadmap.md:276` (component-table definition).
- `phase-4-tasklist.md:490..536` (T04.11 task body — title, Why, deliverables, AC).
- `D-0050/spec.md` (this artifact — binding governance).
- `D-0050/evidence.md` (sibling artifact — observed-state proof).

Any later milestone that needs to edit this region MUST cite
`COMP-004-M4` in its task body, MUST re-run the R-082 grep + parse
contracts as part of its evidence, and MUST update D-0050 (this
artifact) to extend the governance record rather than create a
parallel label.

## 3. Per-row uniqueness invariant (R-082 binding)

**Statement:** every task-qualitative row in the Items Reviewed table
carries exactly one axis value drawn from the closed vocabulary
`{AX-1, AX-2, AX-3, AX-4, AX-5, none}` (or the kebab aliases
`{drift, contradictions, omissions, weakened-criteria,
invented-content, none}`).

**Implications:**

- The axis cell is a single token, not a comma-list or a tuple. If a
  finding spans two axes, the row author picks the most-specific axis
  per the canonical-rules priority order (rf-qa-qualitative.md:725..732)
  and surfaces the secondary axis in the Evidence column as prose.
- `none` is permitted only on rows with `Result = PASS`. The
  canonical-rules comment at lines 720..724 makes this binding.
- Blank, `N/A`, `n/a`, and `—` are forbidden for the task-qualitative
  phase. The canonical-rules comment at lines 723..724 makes this
  binding.
- `drift-axis-inactive` is a Summary-block annotation, NOT a cell
  value. The canonical-rules comment at lines 725..730 makes this
  binding. A row whose finding would have been AX-1 Drift but for the
  missing BUILD_REQUEST.GOAL baseline records `none` in the axis cell
  (because AX-1 cannot fire without a baseline) and the
  `drift-axis-inactive` annotation in the Summary block at lines
  735..740 declares the lens-level disablement.

**Verification contract:** the awk pivot in §2 of evidence.md emits
one line per task-qualitative row's axis cell; the line-count MUST
equal the row-count and every emitted cell MUST be a member of the
closed vocabulary. An empty-cell sweep MUST return zero. Both checks
are codified in the T04.14 / TEST-012 fixture
(`tests/audit/test_axis_column_populated.py`).

## 4. Acceptance Criteria (from phase-4-tasklist.md T04.11)

| AC  | Statement                                                                                                | Evidence section |
| --- | -------------------------------------------------------------------------------------------------------- | ---------------- |
| AC#1 | `grep -n "\| .* \| axis \| .* \|" src/superclaude/agents/rf-qa-qualitative.md` returns header line in [675, 714] | evidence.md §1 |
| AC#2 | Every task-qualitative row has a non-empty axis value drawn from `{AX-1..AX-5, none}`                  | evidence.md §2 |
| AC#3 | Evidence at `TASKLIST_ROOT/artifacts/D-0050/evidence.md`                                                 | evidence.md (this artifact) |
| AC#4 | Edit confined to lines 675-714                                                                           | evidence.md §3 |

## 5. Invariants preserved

- COMP-004-M4 edit-site governance does NOT alter the as-landed state
  of `rf-qa-qualitative.md`. T04.11 is a governance + verification
  task; no source-file bytes change under D-0050.
- 15-item checklist body (lines 546..582) byte-stable —
  sha256 `78edc7790dc00b49...` (matches T04.05 / T04.07 baseline).
- Critical Rules block (lines 834..846) byte-stable —
  sha256 `fd7f2e457bf63ce0...` (matches T04.05 / T04.07 baseline).
- `src/` ↔ `.claude/` parity preserved (`diff -q` clean).
- T04.07 / D-0046 evidence remains the authoritative record for the
  R-078 column-shape contract; D-0050 (this artifact) is the
  authoritative record for the R-082 edit-site contract. The two
  artifacts are non-overlapping and citation-linked.

## 6. Rollback

Per `phase-4-tasklist.md:535` ("As stated in roadmap"): rollback of
the axis-column overlay removes the column from line 709 and
re-collapses the example row at 711 to the pre-T04.07 four-column
shape (`| # | Check | Result | Evidence |`). The COMP-004-M4 label
itself is retired from the roadmap component table as part of the
same revert. The 15-item checklist body and the Critical Rules block
remain untouched in any rollback scenario (they were never part of
COMP-004-M4).

## 7. Forward references

- **T04.12 / CP-P04-T07-T11** consumes D-0050/evidence.md as part of
  the mid-phase gate confirming axis column landed.
- **T04.14 / D-0052** authors the TEST-012 pytest fixture
  (`tests/audit/test_axis_column_populated.py`) that codifies the
  per-row uniqueness invariant declared in §3 above.
- **T04.15 / MIG-004 / D-0053** lands the overlay (including
  COMP-004-M4) as a single revertable commit; the commit body cites
  D-0050 alongside D-0046 in the COMP-004-M4 governance trail.
- **M7 / K-004 axis-distribution audit** consumes the COMP-004-M4
  label when sampling task-qualitative outputs to verify axis
  distribution is non-degenerate.
