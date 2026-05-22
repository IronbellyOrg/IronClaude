# Research: FR-CONV.4 (PR-07) Five Adversarial Axes Overlay Insertion Points

**Status:** In Progress
**Date:** 2026-05-14
**Agent type:** Code Tracer
**CASE:** D (sc:tasklist has tasklist-wide 5-category adversarial prompt; task-builder has per-item Task-Qualitative 15-item checklist — related but non-conflicting)
**Conflict-register row:** PR-07
**Protected invariant:** zero-trust QA (axes overlay MUST NOT weaken anti-inflation severity floor at rf-qa-qualitative.md:789)
**Lands:** 4th of 6 FRs

---

## 1. Verified-Current Insertion Points

All four cited locations were verified verbatim against the live source files on
2026-05-14.

### Site A — `src/superclaude/agents/rf-qa-qualitative.md` lines 525-585 (15-item Task-Qualitative checklist body — PRD cites 527-583)

```
Read the **entire task file** end to end. Then for each checklist item that modifies code, read the actual target source file. Apply the checklist below.

#### Checklist (15 items)

**Operational Simulation**

1. **Gate/command dry-run** — For every shell command, make target, or gate referenced in checklist items (`make verify-sync`, `make sync-dev`, `pytest`, grep checks, etc.), reason through whether it would succeed given the current repo state. ...

2. **Project convention compliance** — If the project has source-of-truth conventions (e.g., `src/` → `.claude/` sync, monorepo package boundaries, generated file patterns), verify every edit targets the correct side of the boundary. ...

3. **Intra-phase execution order simulation** — Mentally execute each phase's items in order. At each item, ask: "do I have everything I need from previous items?" ...

**Code Compatibility**

4. **Function signature verification** — For each item that modifies a function, read the actual function in the target source file. ...
5. **Module context analysis** — For each item that adds or modifies a function, read the full module (not just the function). ...
6. **Downstream consumer analysis** — For each item that changes an output format, schema, or return value, trace all consumers of that output. ...

**Test and Verification Quality**

7. **Test validity** — Verification steps must test the actual artifact with representative input, not stubs. ...
8. **Test coverage of primary use case** — The task's tests should cover the primary use case end-to-end, not just individual functions in isolation. ...

**Failure Mode Analysis**

9. **Error path coverage** — For each new user-facing flag, input type, or configuration option, verify the task includes validation and meaningful error messages for misuse. ...
10. **Runtime failure path trace** — Trace the execution path from entry point through pipeline to completion. ...
11. **Completion scope honesty** — Does the task honestly represent what it will accomplish? ...
12. **Ambient dependency completeness** — For each new function or modified module, verify the task addresses ALL necessary touchpoints. ...
13. **Kwarg sequencing red flags** — Look for "add kwarg" items before "add parameter" items. ...
14. **Function existence claims require verification** — "does not exist" and "exists at path X" claims must ALL be grep-verified against actual source code. ...
15. **Cross-reference accuracy for templates** — Verify ALL template section references (§N, "Section X") per phase against actual template content. ...
```

Excerpt confirms a single, named, numbered 15-item checklist organised under 4
sub-headings: **Operational Simulation** (1-3), **Code Compatibility** (4-6),
**Test and Verification Quality** (7-8), **Failure Mode Analysis** (9-15). The
heading line "#### Checklist (15 items)" is the **anchor before which the new
"Five Adversarial Axes" subsection MUST be inserted**.

### Site B — `src/superclaude/agents/rf-qa-qualitative.md` lines 673-716 (Items Reviewed table — PRD cites 675-714)

The block contains the **shared output-format template** used for all eight QA
phases (prd / tdd / tech-ref / ops-guide / readme / report / task / doc / fix-cycle),
including the Task-Qualitative phase. Verbatim:

```
## Output Format (All Phases)

​```markdown
# QA Report — [Phase Name]

**Topic:** [topic]
**Date:** [today]
**Phase:** [prd-qualitative / tdd-qualitative / tech-ref-qualitative / ops-guide-qualitative / readme-qualitative / report-qualitative / task-qualitative / doc-qualitative / fix-cycle]
**Fix cycle:** [1 / 2 / 3 / N/A]

---

## Overall Verdict: [PASS / FAIL]

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | [check name] | PASS / FAIL | [what you verified and how] |

## Summary
- Checks passed: [count] / [total]
- Checks failed: [count]
- Critical issues: [count]
- Issues fixed in-place: [count] (if fix-authorized)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL / IMPORTANT / MINOR | [file:section] | [what's wrong] | [specific fix] |
...
​```
```

The current `Items Reviewed` table schema is **4 columns**: `# | Check | Result | Evidence`. FR-CONV.4 inserts a fifth column **`axis`** between `Check` and
`Result`, yielding `# | Check | axis | Result | Evidence`. This is the only
allowed modification to the table; row count, column order of the four existing
columns, and the rest of the output-format block remain unchanged.

### Site C — `src/superclaude/skills/task-builder/SKILL.md` lines 940-985 (5-axis overlay insertion site — PRD cites 961)

```
    TRACK GOAL: [goal for this track]

    TARGET FILES (verify ALL — no spot-checking):
    [list every unique source file path from checklist items]

    PROJECT CONVENTIONS:
    [Include any project-specific patterns discovered during research that affect
    whether items will succeed. Examples:
    - Sync models: "src/superclaude/ is source of truth. make sync-dev copies
      src/ → .claude/. make verify-sync fails if .claude/ has dirs with no src/
      counterpart."
    - Build gates: "make lint runs ESLint with --max-warnings 0"
    - Test location: "Tests go in tests/ using pytest. The project does not use
      inline python -c scripts for testing."
    - CI requirements: "Pre-commit hooks run ESLint + Prettier on staged files"
    Pull these from CLAUDE.md and research files. If no project-specific
    conventions were discovered, state "None identified."]

    **ADVERSARIAL STANCE:** Assume the work contains errors. Your job is to find what was missed, not confirm everything is fine. Verify every claim exhaustively. A verdict of 0 issues requires evidence you thoroughly checked.

    INSTRUCTIONS:
    Apply the 15-item Task File Qualitative Review checklist from your agent
    definition. For each checklist item that requires reading source code, read
    the ACTUAL target files — do not rely on research file summaries alone.

    For every shell command or make target referenced in checklist items, verify
    its preconditions are satisfied by earlier items or the current repo state.
    ...
```

Line 961 sits inside the rendered prompt template that task-builder feeds to
rf-qa-qualitative for the Task-Qualitative QA phase. The **`ADVERSARIAL STANCE`
paragraph** is the anchor: FR-CONV.4 inserts the Five Adversarial Axes overlay
**immediately after** that paragraph and **before** the `INSTRUCTIONS:` block,
so the axes are surfaced as a per-item annotation requirement that
rf-qa-qualitative must apply while it walks the existing 15-item checklist.

### Site D — `src/superclaude/agents/rf-qa-qualitative.md` lines 787-792 (severity floor — PRD cites 789)

```
4. **Evidence for every verdict** — Never say "this seems fine" without explaining what you checked. Never say "this is wrong" without explaining what it should be.
5. **Fix then verify** — If authorized to fix, always verify the fix worked. A fix that doesn't verify = still failed.
6. **Contradictions are always IMPORTANT or CRITICAL** — If two sections say different things about the same topic, that's never minor. Always surface contradictions.
7. **Be specific about fixes** — "This section needs work" is useless. ...
8. **Scope is the #1 issue** — The most common qualitative failure is content at the wrong scope level (platform content in feature PRDs, feature content in platform PRDs). Check this first and thoroughly.
9. **Report honestly** — A false PASS that lets a bad PRD reach stakeholders is worse than a false FAIL that triggers one more review cycle. When in doubt, fail it and explain why.
```

Line 789 lands on Critical-Rules item 6 — **"Contradictions are always IMPORTANT
or CRITICAL"** — the anchor of the anti-inflation severity floor. The
floor is reinforced by surrounding lines: item 9 (line 792, "Report honestly —
when in doubt, fail it") and item 10 (line 793, "Maximum 3 fix cycles… ALL
findings regardless of severity must be resolved"). FR-CONV.4 is an **overlay
that MUST NOT weaken this floor** — axes annotate findings; they do not
re-categorise existing severity outcomes.

---

## 2. Five Adversarial Axes Naming (overlay-only annotation)

The canonical 6 axis values that FR-CONV.4 introduces (5 active axes plus a
"no-issue" sentinel):

| Axis | Definition |
|---|---|
| **drift** | Review item drifts from `BUILD_REQUEST.GOAL` — the item builds something tangential to or off-target from the stated goal. |
| **contradictions** | Review item internally contradicts itself, or contradicts another item in the same task file. |
| **omissions** | Review item is missing required content (missing test, missing error path, missing downstream consumer, missing template touchpoint). |
| **weakened-criteria** | Review item softens an acceptance criterion below the level specified in BUILD_REQUEST or template (e.g. "verify functionality" instead of "verify with realistic input"). |
| **invented-content** | Review item references non-existent files, functions, line numbers, or commands — i.e. hallucinated source-code claims. |
| **none** | Applicable when the item is correct and on-spec. Used so every row in the Items Reviewed table has a populated `axis` cell. |

All six values are **annotations** — they label *why* a finding fires (or why no
finding fires), not *whether* a finding fires. Severity (CRITICAL / IMPORTANT /
MINOR) is determined independently by the existing 15-item checklist plus the
Critical-Rules severity floor; the axis tells the reader *which adversarial lens*
caught the issue. This is the CB-3 ("overlay-only") guarantee.

---

## 3. Header Insertion Site

The new `### Five Adversarial Axes` subsection header inserts at Site A
(`rf-qa-qualitative.md` line 528, immediately after the `Read the **entire
task file** end to end.` paragraph and **immediately before** the
`#### Checklist (15 items)` heading).

**Structural rule:** The 15-item checklist body (lines 530-573, items 1-15
plus their four sub-headings) **MUST NOT be modified, removed, reordered,
renamed, or replaced**. The axes subsection precedes the checklist; the
checklist itself is untouched. Insertion form:

```
Read the **entire task file** end to end. Then for each checklist item that modifies code, read the actual target source file. Apply the checklist below.

### Five Adversarial Axes

Each finding produced by the 15-item checklist below MUST be annotated with one
of six axis values: drift, contradictions, omissions, weakened-criteria,
invented-content, or none. The axis labels which adversarial lens surfaced the
finding; it does not alter severity classification. ...

#### Checklist (15 items)

**Operational Simulation**

1. **Gate/command dry-run** — ...
```

**Negative constraint:** Any diff that touches the body of items 1-15 fails
acceptance even if the axes subsection is correctly added.

---

## 4. Items Reviewed Table Axis Column

The existing Items Reviewed table at Site B (`rf-qa-qualitative.md` lines
686-688) currently has 4 columns:

```
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | [check name] | PASS / FAIL | [what you verified and how] |
```

FR-CONV.4 inserts a new **`axis`** column between `Check` and `Result`, giving
5 columns:

```
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | [check name] | drift / contradictions / omissions / weakened-criteria / invented-content / none | PASS / FAIL | [what you verified and how] |
```

**Population rule:** Every row gets exactly one of the six canonical axis values
(`drift`, `contradictions`, `omissions`, `weakened-criteria`, `invented-content`,
`none`). Empty cells, multi-value cells, and non-canonical values all fail
acceptance.

**Mapping rule (one axis per finding):** When a finding could plausibly fire
under more than one axis (e.g. an item that omits a downstream consumer
*because* it drifts from the goal), the rf-qa-qualitative agent picks the
**primary** axis — the one closest to the root cause — and notes the secondary
axis in the `Evidence` column. The `axis` cell remains single-valued.

**Compatibility with Issues Found table:** The existing `Issues Found` table
(line 700-702, columns `# | Severity | Location | Issue | Required Fix`) is
**not modified**. Severity is a separate dimension from axis; both surface on
the same finding via cross-reference (`Items Reviewed row N` ↔ `Issues Found
row N`).

---

## 5. drift-axis-inactive Annotation Rule

**Trigger:** When the generated MDTM task file contains **no checklist item
that captures BUILD_REQUEST.GOAL verbatim** (or via a clearly equivalent
restatement), the drift axis has no baseline against which to compute drift —
the GOAL is not present in the task to drift *from*.

**Required output:** In that case the rf-qa-qualitative report MUST emit a
single-line annotation:

```
drift-axis-inactive: no item in the task file restates BUILD_REQUEST.GOAL — drift axis disabled for this review
```

The annotation is emitted **once per report**, in the `Summary` block of the
output template (Site B, immediately after the existing `Issues fixed in-place`
line). All remaining axes (`contradictions`, `omissions`, `weakened-criteria`,
`invented-content`, `none`) remain active and populate the `axis` column
normally. The drift axis itself is treated as N/A for every row.

**PR-07 failure-mode #3 mapping:** This rule prevents the failure mode where
rf-qa-qualitative silently marks every row `drift: none` because it has no
GOAL baseline — producing a false-confidence PASS. The explicit annotation
forces the absence of a GOAL into the report surface, where it can be caught
by a reviewer or downstream gate.

---

## 6. Acceptance Criteria (PRD §14.1 FR-CONV.4)

### Observable
- rf-qa-qualitative output renders a **`### Five Adversarial Axes`** subsection
  BEFORE the 15-item checklist heading.
- The `Items Reviewed` table has an **`axis`** column populated on every row
  with one of the six canonical axis values.
- A synthetic no-GOAL-baseline fixture produces the single-line
  `drift-axis-inactive` annotation in the Summary block.

### Verification commands
- `grep -n "### Five Adversarial Axes" src/superclaude/agents/rf-qa-qualitative.md`
  returns at least one match.
- `grep -nE '^\| # \| Check \| axis \| Result \| Evidence \|'
  src/superclaude/agents/rf-qa-qualitative.md` returns the table header line.
- Parser test: every row of an emitted `Items Reviewed` table has a non-empty
  `axis` cell whose value ∈ {drift, contradictions, omissions,
  weakened-criteria, invented-content, none}.
- Fixture test: feed task-builder a BUILD_REQUEST where no generated checklist
  item restates `GOAL`; rf-qa-qualitative report contains the exact substring
  `drift-axis-inactive`.

### Negative (must-not)
- 15-item checklist (Site A lines 530-573) MUST NOT be removed, reordered,
  renamed, or replaced — axes **annotate**; they do not substitute.
- Severity floor at Site D line 789 ("Contradictions are always IMPORTANT or
  CRITICAL") MUST NOT be weakened or rewritten.
- The five active axes MUST NOT introduce any new conditional code path in
  rf-qa-qualitative or task-builder — overlay-only per CB-3.
- The `axis` column MUST NOT replace or merge into the `Severity` column of
  the Issues Found table.
- No axis value outside the canonical 6 may appear in an emitted report.

---

## 7. Dependencies on other FRs

- **FR-CONV.3 (inherited PASS composition, INV-013)** — The 5 active axes apply
  to items NOT already covered by an inherited PASS from a prior QA tier. Items
  with an inherited PASS receive `axis: none` automatically (no adversarial
  re-evaluation), preserving INV-013's composition rule. Composition is clean:
  axes operate on items that were re-reviewed in this tier; inherited items
  short-circuit to `none`. (See research file `10-fr3-inherited-pass.md` for
  the inheritance mechanism.)
- **FR-CONV.1 (BUILD_REQUEST.GOAL plumbing)** — The drift axis depends on
  BUILD_REQUEST.GOAL being available at rf-qa-qualitative invocation time. If
  FR-CONV.1 has not yet landed, the `drift-axis-inactive` annotation fires
  unconditionally (no baseline). FR-CONV.4 must land **after** FR-CONV.1 to
  function correctly; PRD's "4th of 6" landing order satisfies this.
- **FR-CONV.2 (per-item-axis adversarial overlay in task-builder SKILL.md)** —
  Site C (line 961) is the task-builder side of the contract; rf-qa-qualitative
  (Sites A, B, D) is the agent side. Both sides must land in the same release
  to maintain the overlay contract.

---

## 8. Gaps and Questions

- **G1.** PRD line citation 789 lands on Critical-Rules item 6 ("Contradictions
  are always IMPORTANT or CRITICAL"). The PRD's phrasing
  "anti-inflation severity floor" maps cleanly to this rule plus items 9-10
  (lines 792-793). No ambiguity, but TDD should explicitly state the floor is
  **multi-line** (786-795), not a single line.
- **G2.** The PRD does not specify whether the `axis` column should appear in
  the Issues Found table as well as the Items Reviewed table. This research
  treats the Issues Found table as **unmodified** (severity-only) because
  duplicating axis information across both tables would create a sync surface
  with no acceptance-criterion teeth. Recommend TDD lock this scope.
- **G3.** The drift axis assumes BUILD_REQUEST.GOAL is plain text. If a future
  BUILD_REQUEST schema makes GOAL a structured object (e.g. list of sub-goals),
  the "verbatim match" criterion needs refinement. Out of scope for this
  release, but worth flagging.
- **G4.** "Verbatim" GOAL match is conservative — many valid task files
  paraphrase GOAL across multiple items. Recommend TDD permit a "clearly
  equivalent restatement" as a stretch criterion, evaluated by the
  rf-qa-qualitative agent's judgement (overlay-only, no code path).

---

## 9. Stale Documentation Found

- **None** at the four cited sites. All PRD line numbers match live source as
  of 2026-05-14, within ±2 lines (PRD cites 527-583 / 675-714 / 961 / 789;
  actual content lands at 525-585 / 673-716 / 940-985 / 787-795). The ±2 drift
  is normal post-PRD editing and does not invalidate insertion-point intent.
- **One observation, not stale:** Critical-Rules item 10 on line 793
  ("Maximum 3 fix cycles … ALL findings regardless of severity must be
  resolved") is a second pillar of the anti-inflation floor and should be
  cross-referenced in the TDD alongside line 789. Not a doc bug — a
  completeness note for the TDD author.

---

## 10. Summary

FR-CONV.4 lands a **per-item Five Adversarial Axes overlay** on top of the
existing 15-item Task-Qualitative checklist by inserting (a) a new
`### Five Adversarial Axes` subsection header BEFORE the untouched 15-item
checklist body in `rf-qa-qualitative.md`, (b) a new `axis` column in the
shared `Items Reviewed` output table, (c) an axis-annotation directive in the
task-builder Task-Qualitative prompt at SKILL.md line 961, and (d) a
single-line `drift-axis-inactive` annotation rule for the no-GOAL-baseline
edge case. All four insertion sites were verified verbatim against live source
on 2026-05-14 with ±2-line drift from PRD citations. The overlay is
**annotation-only** (CB-3): no axis introduces a code path, no axis substitutes
for the existing 15 checklist items, no axis modifies the
"contradictions are always IMPORTANT or CRITICAL" severity floor at line 789,
and the canonical six axis values (drift, contradictions, omissions,
weakened-criteria, invented-content, none) form a closed enumeration with
single-value-per-row population. Dependencies: FR-CONV.1 (GOAL plumbing) and
FR-CONV.3 (inherited-PASS composition, INV-013) must land first or alongside;
PRD's "4th of 6" ordering satisfies both.

**Status:** Complete
