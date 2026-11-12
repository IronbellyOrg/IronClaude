# Reviewer brief 3: refactorer lens, UC-1 pre-execution

This brief is self-contained. `sc-reflect-protocol` Step 3B.0 wrote it for a Tier-2 UC-1 (pre-execution) run. You audit a proposed tasklist against its driving spec before any of it is executed. Everything you need is below or in the files listed under "Files you may Read".

**Run facts**

- Repository root (your grounding root): `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode`. Every path in this brief is relative to it.
- OUT: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre`.
- SPEC, the driving spec of this run: `docs/designs/orchestrator-mode.md` (1013 lines).
- TASKLIST, the plan under review: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md` (2892 lines, 355 items).
- Tier-1 card: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/reflection-card-t1.yaml`. Coverage matrix: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/coverage-matrix.yaml`.
- Reviewer 3 of 3. Persona: refactorer. Model class: claude-gw-tier1a (the opus slot). Agent type: `reflect-reviewer` (read-only).

**Names used in the hunks**

- The TASKLIST calls this run's SPEC "DESIGN". When the TASKLIST says "SPEC", it means `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md`, the upstream requirements file of the design. In this brief, SPEC always means `docs/designs/orchestrator-mode.md`.
- "R3-B1", "R3-B2", "R3-B3", "design fix R4" and "design fix R5" are design-fix work in TASKLIST phases 2 to 6. "Routing row R1" to "routing row R8" are the rows of the SPEC section 9 table. They are different things (TASKLIST line 165).
- SPEC line numbers in the hunks are the current, unrevised SPEC. TASKLIST phases 2 to 6 edit the SPEC, so later TASKLIST items find SPEC text by heading (TASKLIST line 1414).
- "research/NN" in the TASKLIST means `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/research/NN-*.md`.

**Your slice**

The design-fix phases 2 to 6 (R3-B1, R3-B2, R3-B3, design fix R4, design fix R5), plus scope creep or missing reuse in the planned code of phases 8 to 13. Rows: the 8 routing rows R1 to R8, and the 16 rows whose matched items include a phase 2 to 6 item. Those 16 rows also sit in reviewer 1's or reviewer 2's slice; for them you judge only whether the design-fix edits keep the SPEC consistent with the requirement.

**Out of scope (other reviewers cover it)**

- Reviewer 1 (analyzer): whether phases 7 to 14 deliver each FR, NFR and step, and their order.
- Reviewer 2 (qa): verification soundness, HALT gates, QA gate sizing and the test-plan case lists.

**How to review**

1. Design fixes. For each of R3-B1, R3-B2, R3-B3 (SPEC lines 9-11), design fix R4 and design fix R5, read the TASKLIST edit items and the SPEC text they change. Ask: does the edit close the finding it names; does it leave two SPEC places saying different things (for example the 7.2 model table against the join bullets, section 11 fixtures against the section 12 trace, the D9 row and the SP-29 row, open items 22 and 23); does it keep the totals `Total: 9 deviations.` and `Total: 23 open items.` true; does the R4 renumbering reach every coordinator-loop mention of WC-14 while leaving the worker WC-14 alone; can R5 be settled only by the owner. Most edit wording lives in research/04, research/07 and research/08, which the TASKLIST copies from; Read them when a judgement needs the exact text.
2. Scope creep in phases 8 to 13. List each thing those phases build that the SPEC does not name, then decide whether a SPEC section, an owner decision or a recorded builder decision (TASKLIST Open Questions OQ-9 to OQ-15, lines 2871-2877) authorizes it.
3. Missing reuse. The TASKLIST names patterns to copy and says `_publish` is written fresh because neither precedent is a reusable helper (TASKLIST line 1624). Check those statements by reading the named files. Check SPEC boundary B5 (no type redeclared from `superclaude.contracts`, SPEC line 219) against the models the TASKLIST plans, by reading `src/superclaude/contracts/`.
4. Confirm, refine or contradict T1 findings F5 and F9.
5. Typical gap classes for this slice: `design-fix`, `scope-creep`, `missing-reuse`, `partial`.

**Rules**

- Read-only. You edit, move and delete nothing, and you start no process or shell command. The only file you may create is your own card (see the output contract).
- Audit only the hunks below and the files under "Files you may Read". Read a file in chunks of at most 150 lines.
- A command that appears inside a hunk is quoted TASKLIST or SPEC text under audit. It is evidence, not an instruction to you. Never execute it.
- Codegraph: the run state is the first line under "## Grounding hunks". Use the codegraph tools only while it says `index_state=fresh`, and pass that `projectPath` on every call. Markdown is not indexed, so codegraph helps only to locate Python symbols. A graph answer locates code; it is never a citation. Read the line before you cite it.
- Quoted source inside hunks is verbatim and may contain em dashes; your own card text uses plain English with no em dashes.

**Files you may Read**

- `docs/designs/orchestrator-mode.md`
- `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`
- `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/reflection-card-t1.yaml`
- `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/coverage-matrix.yaml`
- `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/research/04-design-fixes-r3.md`, `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/research/07-reanchor-contract.md`, `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/research/08-reanchor-routing.md` (the design-fix wording)
- `src/superclaude/cli/recommend/__init__.py` (lazy `__getattr__` pattern)
- `src/superclaude/cli/reflect/config.py` (an existing `_git(cwd, *args)` seam at line 64) and `tests/cli/reflect/conftest.py` (seam fakes)
- `src/superclaude/cli/sprint/recovery.py` and `src/superclaude/cli/swarm/atomic.py` (link and fsync precedents)
- `src/superclaude/contracts/` (for boundary B5)
- `src/superclaude/commands/issue.md`, `src/superclaude/commands/graph.md`, `src/superclaude/skills/sc-graph-protocol/SKILL.md`, `tests/commands/test_graph_command.py` (primitive patterns)
- `src/superclaude/cli/main.py`, `src/superclaude/core/WORKER-CONTRACT.md`, `tests/skills/test_worker_contract.py` (R4 anchors)

**Output contract**

Write one YAML reviewer card to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/reviewer-cards/reviewer-3-card.yaml`. If your tool set has no Write tool (the fixed `reflect-reviewer` type has none), return the complete YAML as your final message, with nothing before or after it; the orchestrator saves it to that path unchanged.

- UC-1 mode: you classify gaps in the plan, not deviations in finished work. Do not use the four deviation classes (Authorized expansion, Necessary deviation, Drift, Regression). The T1 card labels its findings Drift, Regression or Refinement; refer to them by id only.
- Every finding is either `tag: Grounded`, with at least one `file:line` or `file:start-end` that you Read in a hunk or in a listed file, or `tag: "[INFERRED]"`, with the reasoning stated in `claim`. A finding with neither is not allowed. The same rule applies to each `row_verdicts` entry.
- Cite paths relative to the repository root, exactly as the hunk headings write them.
- Severity: HIGH when the plan, followed as written, misses a requirement, lets a gate pass wrongly or cannot finish; MEDIUM when it is likely to cause rework or a wrong result; LOW otherwise.
- For each T1 finding in your excerpt, add at least one finding with `t1_relation` `confirms`, `refines` or `contradicts` that id.
- `gap_class` takes exactly one of these values:

- `missing`: a SPEC requirement that no TASKLIST item delivers.
- `partial`: an item delivers only part of a requirement.
- `traceability`: the requirement is covered in substance, but the link from the item to the requirement id cannot be followed from the TASKLIST text alone.
- `ordering`: an item runs before an item it depends on, or a gate does not come before the work it gates.
- `unsound-check`: a Verification or Completion gate line that cannot pass when the Action is followed exactly, that passes even when the work is not done, or that cannot be judged from file content.
- `gate-bypass`: a HALT or owner-decision gate that the executor can clear without the owner's words, or that a later item proceeds past without checking.
- `gate-sizing`: a QA gate whose agent count, lens mix or cycle rule does not match the rule the TASKLIST cites.
- `test-plan`: a SPEC section 11 case or section 12 test mapping that no TASKLIST test item carries.
- `scope-creep`: an item builds something the SPEC does not ask for, and no owner decision or recorded builder decision authorizes it.
- `missing-reuse`: an item writes new code or text where an existing helper or pattern, named in the SPEC or TASKLIST or found in a listed file, fits the need.
- `design-fix`: a phase 2 to 6 SPEC edit that does not close its finding, makes two SPEC sections disagree, or breaks a SPEC total.

Card shape:

```yaml
schema: sc-reflect-reviewer-card/v1
mode: UC-1 pre-execution
reviewer: 3
persona: refactorer
model_class: claude-gw-tier1a
brief: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/reviewer-briefs/reviewer-3.md
spec: docs/designs/orchestrator-mode.md
tasklist: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md
codegraph_used: true | false
row_verdicts:                  # one entry per Coverage slice row, in slice order
  - id: <row id>
    verdict: covered | covered-in-substance | partial | missing | false-match
    items: ["<TASKLIST item id>", ...]   # the items you relied on; [] when missing
    evidence: ["<path>:<line or start-end>", ...]
    tag: Grounded | "[INFERRED]"
    note: <one sentence>
findings:
  - id: R3-G<k>
    gap_class: <one value from the list above>
    severity: HIGH | MEDIUM | LOW
    tag: Grounded | "[INFERRED]"
    t1_relation: confirms F<n> | refines F<n> | contradicts F<n> | new
    claim: >-
      <what is wrong, in plain English>
    evidence:                  # required for Grounded; may be [] only for "[INFERRED]"
      - <path>:<line or start-end>
    recommendation: >-
      <the TASKLIST item to change, the smallest edit, and a check a reader can verify by reading the edited text>
best_practice_compliance:
  grade: <0-5>
  scale: 0-5
  reasons: ["+ ...", "- ..."]
self_scores:                   # same five dimensions as the T1 card, each 0.00 to 1.00
  citation_grounding: <float>
  coverage_completeness: <float>
  deviation_classification_clarity: <float>   # here: how clearly each finding fits one gap class
  risk_surface_coverage: <float>
  recommendation_actionability: <float>
  C: <float>
  rationale: {<dimension>: <one sentence>, ...}
summary:
  rows_audited: <int>
  findings_high: <int>
  findings_medium: <int>
  findings_low: <int>
```

## T1 card excerpt

Verbatim from `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/reflection-card-t1.yaml`. Each block names its line range.

Source: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/reflection-card-t1.yaml:1-9`

````yaml
schema: sc-reflect-card/v1
tier: 1
mode: UC-1 pre-execution
created: 2026-11-08
spec: docs/designs/orchestrator-mode.md
spec_lines: 1013
tasklist: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md
tasklist_items: 355
coverage_matrix: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/coverage-matrix.yaml
````

Source: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/reflection-card-t1.yaml:121-140`

````yaml
  - id: F5
    severity: LOW
    category: Drift
    tag: Grounded
    claim: >-
      Four SPEC boundary rules have no task item or verification: B3 (the read allowlist lives only in
      `probes.py`; no write verb), B4 (the command and skill are thin), B5 (no type redeclared from
      `superclaude.contracts`) and the `.gitignore` rule that the pattern names `.dev/sweeps/` only. B1
      matched only at the 0.6 threshold. The `.gitignore` rule is partly enforced by the 8.6 check that
      `.dev/tasks/to-do/x.md` is not ignored.
    evidence:
      - docs/designs/orchestrator-mode.md:217
      - docs/designs/orchestrator-mode.md:218
      - docs/designs/orchestrator-mode.md:219
      - docs/designs/orchestrator-mode.md:719
      - .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1455
    recommendation: >-
      Add B3 to B5 as verification lines on the items that create `probes.py`, `commands.py`,
      `sweep.md` and `SKILL.md` (for B5: grep the new package for class names already defined in
      `superclaude.contracts`). Success: each B rule has one grep or test cited in a verification line.
````

Source: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/reflection-card-t1.yaml:190-201`

````yaml
  - id: F9
    severity: LOW
    category: Refinement
    tag: "[INFERRED]"
    claim: >-
      The tasklist adds work the SPEC does not ask for in the same form: design-fix phases 2 to 5 edit the
      SPEC itself (R3-B1, R3-B2, R3-B3, R4), and Phase 6 adds an owner HALT for R5. These are authorized by
      the request scope, so they are not scope creep, but they mean SPEC line numbers move mid-task; the
      tasklist handles this by re-locating by heading.
    evidence:
      - .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1414
    recommendation: none
````

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-08T10:11:39Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode

Hunk index (why each hunk is here):

- H1 `docs/designs/orchestrator-mode.md:1-13`: SPEC status: the three blocking findings R3-B1, R3-B2 and R3-B3.
- H2 `docs/designs/orchestrator-mode.md:204-221`: SPEC boundaries B1 to B5 and the extension points.
- H3 `docs/designs/orchestrator-mode.md:82-111`: SPEC sections 3.1 and 3.2: where the one write lives and how it is made.
- H4 `docs/designs/orchestrator-mode.md:447-468`: SPEC section 7.2 data model table (the R3-B1 target).
- H5 `docs/designs/orchestrator-mode.md:490-499`: SPEC section 7.2 join bullets, path-B window and guard cases (R3-B1, R3-B2, R3-B3 targets).
- H6 `docs/designs/orchestrator-mode.md:500-512`: SPEC section 7.2 observation rules, including duplicate Dispatch rows.
- H7 `docs/designs/orchestrator-mode.md:514-544`: SPEC section 7.3 allowlist constants, including `FORBIDDEN_TOKENS` (the R5 subject).
- H8 `docs/designs/orchestrator-mode.md:659-687`: SPEC section 8: WC-14 text, pins and the never-as-worker line (the R4 target).
- H9 `docs/designs/orchestrator-mode.md:688-709`: SPEC section 9: routing rows R1 to R8 and their rules.
- H10 `docs/designs/orchestrator-mode.md:878-897`: SPEC section 15.1 capture table, item 4 (an R3-B1 target).
- H11 `docs/designs/orchestrator-mode.md:984-993`: SPEC section 17 open items 16 to 23.
- H12 `docs/designs/orchestrator-mode.md:995-1013`: SPEC section 18 revision log, where the TASKLIST adds `### Fix cycle 3`.
- H13 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:70-76`: TASKLIST overview: the five design items and the build.
- H14 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:142-153`: TASKLIST source areas: the packages named as patterns to copy.
- H15 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:238-253`: Phase 2 intro and items 2.1 and 2.2 (R3-B1 model and window edits).
- H16 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:256-282`: Items 2.3 to 2.6 (R3-B1 remaining edits, fixtures, revision table).
- H17 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:419-442`: Phase 3 intro and items 3.1 to 3.3 (R3-B2).
- H18 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:586-609`: Phase 4 intro and items 4.1 to 4.3 (R3-B3).
- H19 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:611-623`: Items 4.4 and 4.5 (R3-B3 trace and revision row).
- H20 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:760-790`: Phase 5 intro and items 5.1 to 5.4 (design fix R4: renumbering and cadence).
- H21 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:792-818`: Items 5.5 to 5.8 (design fix R4: anchors, `main.py`, step 1.16a, master test constraints).
- H22 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:976-999`: Phase 6 intro and items 6.1 to 6.3 (design fix R5 owner decision).
- H23 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1430-1435`: Item 8.3: models, `ClassifiedRow` and the dimension fields (builder decisions).
- H24 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1444-1449`: Item 8.5: the git seam in `probes.py`.
- H25 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1465-1470`: Item 8.8: conftest copied from the reflect seam fakes.
- H26 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1623-1628`: Item 9.1: `commands.py` and `_publish`, with the precedent statement.
- H27 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1776-1781`: Item 10.1: the closed set of hand-made fixture files.
- H28 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1950-1955`: Item 11.1: `sweep.md` from the `issue.md` and `graph.md` patterns.
- H29 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:2873-2877`: TASKLIST Open Questions OQ-11 to OQ-15: builder decisions.

### docs/designs/orchestrator-mode.md:1-13

````markdown
# Orchestrator mode, Phase 1: `/sc:sweep` architecture design

## 1. Status, scope and inputs

Status: design for review, issue #339 Phase 1, written 2026-11-08 by `/sc:design --type architecture --format spec`. It holds no implementation code. Owner approval of the WC-14 text (section 8) is still required.

Review status: NOT a clean pass. Three blocking findings were still open after the review cap (2 fix cycles, 3 reviews: `orchestrator-mode-review-1.md` to `-3.md`). With coordinator approval (the reply to `msg_ee6f54c3b8a4`, delivery `delivery_17bd071084c5`, 2026-11-08), they are carried as the first required design-fix tasks of the `/task-builder` task file. Each one is closed by its own review gate before any code task starts:

- R3-B1: the session-to-Dispatch time-window rule reads three time fields (Dispatch start, Dispatch end, and the earliest transcript timestamp) that the data model (`OrcaObservation`, `TranscriptTail`) lacks.
- R3-B2: two Dispatch rows on one pane give conflicting results (False and None, or a join to both rows), and no rule decides between them.
- R3-B3: three SPEC FR-010 fixtures (outage, full page, `call_failed`) were dropped from `test_classify.py`.

Phase 1 adds one read-only command, `superclaude sweep run`, a thin `/sc:sweep` command and `sc-sweep-protocol` skill that call it, the WC-14 "Coordinator loop" contract text, and the routing and doc rows that name it. A successful run leaves one filesystem change: one dated report under `<root>/.dev/sweeps/`, plus that directory when it is new. A dot-prefixed temp file exists only during publication (section 3).
````

### docs/designs/orchestrator-mode.md:204-221

````markdown
Boundaries (SPEC section 6, with D1 applied):

| Module | May import | Must not import |
|---|---|---|
| `__init__.py` | `commands` (inside `__getattr__` only) | anything at import time |
| `models.py` | standard library `dataclasses`, `datetime`, `typing`, `pathlib` (type only) | every other sweep module |
| `classify.py` | `models` | `probes`, `report`, `commands`, `subprocess`, `click`, `os`, `shutil` |
| `probes.py` | `models`, `subprocess`, `os`, `json`, `time` | `classify`, `report`, `click` |
| `report.py` | `models` | `probes`, `classify`, `commands`, `subprocess`, `click`, `os`, `shutil` |
| `commands.py` | all of the above, `click`, `json`, `os` (D1) | nothing further is needed |

- B1: imports go one way, `commands -> {probes, classify, report} -> models`.
- B2: `classify` and `render` treat every path as data only (SPEC section 6 B2): they never open, stat or resolve one, which the NFR-004 import test enforces by forbidding `os` and `shutil`, and they print paths through `sanitize`.
- B3: the read allowlist lives only in `probes.py`. Phase 2 `/sc:close` gets its own package, seam and allowlist; nothing in this package grows a write verb (FR-021).
- B4: the command and skill are thin: no parsing, no classification, no file writes.
- B5: no type is redeclared from `superclaude.contracts`.

Extension points, each additive: a new rule appended to `RULES` before `fallback` (NFR-010 pin updated in the same change); a new template in `ALLOWED_ORCA` (only after a capture, and never a write verb); a new `SourceCoverage` row; a new JSON key in v1 (never a removal or rename, NFR-009); a new entry in `report.SECTIONS`. A tenfold growth in Runs or rows is bounded by `Budget` (50 shows, 90 s), so it shows up as more `unscanned` rows and lower-bound totals, never as a longer run.
````

### docs/designs/orchestrator-mode.md:82-111

````markdown
## 3. G-1 with SP-20: report publication

SPEC section 18 G-1 (lines 637-645) leaves open what a run that exits 1 leaves on disk. PANEL SP-20 (line 220) notes that `write_report` in `report.py` puts file I/O in a module the NFR-004 purity test is meant to cover. Both are resolved together here.

### 3.1 Where the write lives

Decision: the single write path is a private function `commands._publish(text, output_dir, now) -> Path` in `commands.py`. `report.py` keeps only pure code: `sanitize`, `render`, `SECTIONS`, the fixed strings and `CHECKED_ORCA_VERSION`. No `write_report` exists.

Why `commands.py` and not `probes.py` or a seventh module:

- `commands.py` is already the impure shell: it parses arguments, calls `collect`, calls `classify_all` and `render`, prints JSON and maps exceptions to exit codes. The publish step is one more shell step.
- `probes.py` is the read side. FR-021 keeps read and write code apart ("the sweep package holds no write verb"); putting the one filesystem write in the module that owns the read allowlist would blur the B3 boundary.
- A separate `writer.py` adds a module, a boundary row and an import test for about 30 lines with one caller.
- With the write gone, the NFR-004 AST test covers the whole of `report.py` unchanged, and B1 (`commands -> {probes, classify, report} -> models`) still holds.

Cost: the SPEC section 6 module table changes. `commands.py` gains `os` in its may-import list, and `report.py` loses `write_report`. This is deviation D1 (section 13).

### 3.2 The one write mechanism

Decision: write a temp file in the output directory, `fsync` it, then publish it under the report name with `os.link`, which fails when the name exists. This is the PANEL G-1 recommendation (lines 289-296). There is one mechanism and no fallback.

`_publish` runs only after every exit-2 check, `collect`, `classify_all` and `render` have succeeded, so a usage error or an internal error in those steps never reaches the filesystem. Steps:

1. `stem = now.strftime("%Y%m%d-%H%M%S") + "-sweep"` (UTC, `SweepContext.now`).
2. `os.makedirs(output_dir, exist_ok=True)`, then resolve `output_dir` again and confirm it is still `<root>/.dev/sweeps/` or below. A path that now escapes exits 1 with `[sweep publish] output dir escaped <root>/.dev/sweeps/` and writes nothing.
3. `fd = os.open(output_dir / f".{stem}.{os.getpid()}.tmp", O_WRONLY | O_CREAT | O_EXCL, 0o666)`. The process umask applies, as for any new file. `O_EXCL` also refuses a symlink at that name.
4. Write every byte of `text.encode("utf-8")` (loop until all are written), `os.fsync(fd)`, `os.close(fd)`.
5. For `name` in `stem.md`, `stem-2.md` to `stem-99.md`, in order: `os.link(tmp, output_dir / name)`. `FileExistsError` moves to the next name; success stops the loop. The successful link is the commit point.
6. No name left: unlink the temp file and exit 1 with `[sweep publish] report name space exhausted: <dir>` (SPEC section 5.3, line 174).
7. After the commit point: `os.unlink(tmp)`. If it fails, exit 1 with no success JSON (table below). Otherwise return the published path. `commands.run` then prints the one success JSON object with that `report_path`.
````

### docs/designs/orchestrator-mode.md:447-468

````markdown
### 7.2 Data model

All types are frozen dataclasses in `models.py`, as SPEC section 7 (lines 227-243) lists them. Class and state names are `str` constants collected in tuples. This design keeps every SPEC field and adds only the items marked (design).

| Type | Fields (SPEC section 7 unless marked) |
|---|---|
| `SweepContext` | `now`, `window`, `window_start = now - window`, `root`, `runs` |
| `SweepInput` | `orca_rows: tuple[OrcaObservation, ...]`, `contracts`, `transcripts: tuple[TranscriptTail, ...]`, `tab_map: tuple[TabMapEntry, ...]`, `worktrees: tuple[WorktreeState, ...]`, `sources: tuple[SourceCoverage, ...]`, `orca_available: bool`, `orca_binary: str`, `orca_version: str \| None`, `truncated: bool`, `collected_start`, `collected_end` (field names other than the last two are design) |
| `OrcaObservation` | SPEC list (line 231) plus `dispatch: str`, `run: str`, `session_join: str \| None` (design: the Orca-side join value, section 2.2 path A or B; None until step 1.0a names the field) |
| `ContractRecord` | `path`, `worker_status`, `blocked_question`, `reason`, `report_path`, `artifacts`, `command` |
| `TranscriptTail` (design) | `path`, `session_id: str \| None`, `readable: bool`, `last_record_ts: datetime \| None`, `mtime: datetime`, `project_key: str` |
| `TabMapEntry` (design) | `file_name` (pane key with `:` written as `+`), `session_id`, `launch_dir`, `terminal_handle` (the three lines of the ccsession file) |
| `SessionRow` | SPEC list (line 235): `id`, `person_started`, `orca`, `contract`, `transcript_path`, `transcript_readable`, `last_activity`, `gate_policy`, `row_id`, the ten #409 dimensions |
| `StatusParse` (design) | `entries: tuple[tuple[str, str], ...]` (XY code, path), `branch_header: str`, `ahead: int \| None`, `has_upstream: bool \| None`, `header_note: str \| None` |
| `PackageRecord` | `id`, `location`, `has_final_line`, `archiving_marker`, `active`, `state` |
| `WorktreeState` | `path`, `status_read`, `uncommitted`, `unpushed: bool \| None` (M7, section 2.2), `dev_tasks_unsaved`, `changed_paths`, `packages`, `shared_package_ids`, `frozen`, plus `upstream_note: str \| None` (design: `ahead N`, `no upstream`, `detached HEAD`, `upstream gone`, `no commits yet`) |
| `Classification` | `class_name` (JSON key `class`), `waiting_kind`, `rule`, `evidence`, `notes` |
| `SafeToClose` | `terminal`, `worktree`, `reason` |
| `SourceCoverage` | `name`, `coverage`, `age_seconds`, `unscanned` |
| `SweepResult` (design fields) | `rows: tuple[ClassifiedRow, ...]` (row plus `Classification`, policy and `SafeToClose`), `worktrees` (after `mark_shared_packages`, with `removable` and `removable_reason`), `waiting_a`, `waiting_b` (row ids), `summary` (counts per class with zeros, `bound_reached`, `visible`, `historical`, `total`, `total_is_lower_bound`), carried header data from `SweepInput` |

Constants in `models.py`: `JSON_SCHEMA_VERSION = 1`; `CLASSES` (`waiting on a person`, `stalled (proved)`, `fenced`, `working`, `finished`, `idle`, `person session (active)`, `could not determine`); `PACKAGE_STATES` in precedence order (`conflict`, `interrupted-archive`, `archive-blocked`, `unfinished`, `archived`, `unknown`); `SAFE_VALUES` (`yes`, `no`, `could not determine`).
````

### docs/designs/orchestrator-mode.md:490-499

````markdown
Joins (GQ-108, SP-16, SP-29):

- `row_id` is `orca:<dispatch>` or `transcript:<session_id>` (SPEC line 236).
- A transcript joins an Orca row when its `sessionId` equals that row's `session_join` value (path A), or when a tab-map entry whose `session_id` equals the transcript `sessionId` has a `file_name` or `terminal_handle` equal to the row's `session_join` (path B). Which path applies, and the Orca field behind `session_join`, are decided from the step 1.0a capture (section 17).
- A worker, for FR-010, is a transcript that joins a Dispatch row of a scoped Run by path A or path B. A tab-map entry counts only through that join. A joined transcript is `person_started` False, and it is shown as the Orca row `orca:<dispatch>`, not as a separate transcript row (FR-010: a positive join makes it False). Under path B the join names the pane's latest session only, because the tab map keeps one session per pane and `/clear`, a resume or a person running the command again in the tab replaces it (`ccsession:574-602`, `:607-613`). A path-B join therefore also needs session identity: the earliest `timestamp` in the transcript tail must fall inside the Dispatch row's own window, from the row's start time to its end time, or to `collected_start` when the row has not ended. The `worker-show` fields that carry those times are UNVERIFIED and come from the step 1.0a item 4 capture (open item 23). A path-B match outside that window, or on a row with no observable start time, does not join: the row is could not determine with note `pane moved to a later session`, and that transcript is None with the same note. A path-B join inside the window is False and carries note `joined by pane: latest session of the pane`, because a person rerun inside the window cannot be told apart.
- A tab-map entry alone does not make a worker, because the file cannot tell a worker pane from a person pane (section 1). A transcript whose tab-map entry joins no scoped Orca row may be a person's pane or a worker of a Run outside the scope, whose rows Phase 1 does not read. It gets None with note `Orca pane session, not in scoped Runs` (D9).
- Under path A only, a transcript with no tab-map entry that joins no scoped Orca row may be True when the FR-010 guard holds. Under path B, when any scoped Dispatch row exists, this True path never applies (fourth guard case below). Having no entry does not prove the session ran outside Orca: a plain `claude` launch and an earlier session of a reused pane have none (section 1). A worker of an unscoped Run can therefore reach True this way. D9 records this narrowing of SP-29. Every True reached this way carries note `origin not proved: no tab-map entry; may be a worker of a Run outside the scope`, in the report row and in the JSON `notes`, so such a session is never shown as person-started without a note.
- The guard's "join completed" condition fails, and every unjoined transcript in the window is None, in four cases. First, `session_join` is None on any scoped Dispatch row: note `tab map join not observable` (section 2.2). Second, Orca returned at least one worker row and no transcript joined any Orca row (SPEC line 236, SP-16). Third, under path B, a scoped Dispatch row's `session_join` matches no tab-map entry, so that worker's transcript could be any unjoined one. Fourth, under path B, at least one scoped Dispatch row exists. The tab map holds only each pane's latest session, so an earlier session of the same pane, which may be that worker's own transcript after a `/clear`, a resume or a person rerun, has no entry. Every unjoined transcript with no tab-map entry is then None with note `earlier pane session not joinable (tab map keeps only the latest session)`. When the first and second cases hold together, the transcript carries the SP-16 literal first and then `tab map join not observable`. In the second and third cases, Could not determine also prints the line `could not join Orca workers to transcripts (tab map empty or stale)`, and each affected transcript carries it as its note.
- The SPEC's `worker of Run <id>, outside scope` False path needs a Run id in the tab map, which the ccsession file does not hold (section 1), so that path does not occur in Phase 1.

````

### docs/designs/orchestrator-mode.md:500-512

````markdown
Observation rules (SPEC section 11 failure modes and the section 7 cross-cutting note). Each one leaves the run at exit 0:

- WC-13: an Orca row with a non-null `parent` adds note `WC-13 violation, review` (SPEC line 261, GQ-40). The note does not change the class. The row is also listed under `## Retained problems` (SPEC line 380).
- List and show disagree: the `worker-show` value wins for every field both return. A `worker-list` row with no `worker-show` result is could not determine (WC-10), never stalled (SPEC line 443).
- Unknown row schema: a missing `worker-show` key leaves that field None (`unknown`) and raises nothing; an extra key is ignored (SPEC line 446).
- Duplicate Dispatch: rows that share one Dispatch id but differ in state are merged into one `orca:<dispatch>` identity. That row is could not determine with reason `conflict: duplicate Dispatch rows disagree`. No row wins by position (SPEC lines 319 and 452).
- Input changed between reads: each file reader records `(st_size, st_mtime_ns)` before and after it reads. If they differ, it reads the file once more while the budget allows. If the second read also changes, or no budget is left, the row is could not determine with reason `conflict: inconsistent observation` (SPEC line 451).
- Path escapes its source: every discovered input path is passed through `Path.resolve()`. It must stay under the folder it was found in: the root, a scanned project-key folder or the `orca-tabs/` folder. A path that escapes is not read, and its source is reported `unscanned: outside root` (SPEC line 450; REPORT step 1.6).
- Worktree removed mid-sweep: a `_git` error or an `os.stat` failure on a worktree path makes that worktree could not determine with `unscanned: worktree not readable`. The other worktrees continue (SPEC line 440).
- Unreadable transcript or contract: a transcript is unreadable when its open raises `OSError`, or when its tail read (`read_transcript_tail`, the last 256 KiB with the first partial line dropped) holds no complete JSON record with both `timestamp` and `sessionId`. That covers a truncated or malformed JSONL. A last line cut mid-object is skipped, and the transcript stays readable when an earlier complete record has both fields. Either case sets `transcript_readable` False. A contract is unreadable when its open raises `OSError`. Rules 2 and 1 then decline, and the row is could not determine with note `unscanned: transcript not readable` or `unscanned: contract not readable` (SPEC line 442).
- Rule 6 wording: a finished row's JSON values and report text never contain `admitted` or `accepted`. A contract body whose later line quotes `guard refused:` is not finished (SPEC line 259, SP-07).
- `FINAL:` counts only at the start of a line, after optional leading whitespace. `FINAL:` inside other text does not make `archive-blocked` (SPEC line 269, GQ-105).
- Remote hosts: `## Source coverage` always has a row `remote hosts` with coverage `unknown`. The Scope line's session count is followed by `(lower bound: remote hosts not scanned)`. The report never says there are no sessions (SPEC line 454).
````

### docs/designs/orchestrator-mode.md:514-544

````markdown
### 7.3 Allowlist constants

All in `probes.py`. Templates are tuples of tokens; `<run>` and `<dispatch>` are placeholders that match only the id regexes `RUN_ID_RE` and `DISPATCH_ID_RE`, which are fixed from the step 1.0a capture (UNVERIFIED today, section 17). Matching is token for token over the whole argv after argv[0]: same length, same literal tokens, placeholders matched by regex. No prefix match (NFR-003).

```
ORCA_BINARY_DEFAULT = "orca-ide"            # never bare "orca" (SPEC section 8, INV-017)

ALLOWED_ORCA: tuple[tuple[str, ...], ...] = (
    ("orchestration", "run-current"),
    ("orchestration", "worker-list", "--run", "<run>", "--json"),
    ("orchestration", "worker-show", "--dispatch", "<dispatch>", "--json"),
    ("orchestration", "task-list", "--ready", "--run", "<run>", "--json"),
    ("orchestration", "task-list", "--run", "<run>", "--json"),
    ("worktree", "ps", "--json"),
    ("worktree", "list", "--json"),          # pinned, not called in Phase 1
    ("worktree", "current", "--json"),       # pinned, not called in Phase 1
)                                            # 8 templates, 7 verbs (NFR-014)

FORBIDDEN_TOKENS = frozenset({"--include-remote", "--agent-wait"})   # rejected in any position

ALLOWED_GIT: tuple[tuple[str, ...], ...] = (
    ("status", "--porcelain=v1", "-z", "--branch", "--untracked-files=all"),
)                                            # the seam prepends git --no-optional-locks -C <path>

ORCA_VERSION_FILE = Path("/opt/Orca/resources/app.asar.unpacked/out/package.json")
OUTPUT_LIMIT = 8 * 1024 * 1024               # subprocess stdout + stderr
CONTRACT_LIMIT = LEDGER_LIMIT = 1024 * 1024  # hit when size > limit
LEDGER_SPLIT = 512 * 1024                    # head and tail read of a ledger over the limit
TRANSCRIPT_TAIL = 256 * 1024
WORKER_LIST_PAGE = 100                       # a full page sets truncated
```
````

### docs/designs/orchestrator-mode.md:659-687

````markdown
## 8. WC-14 and the never-as-worker list

**Gate.** Steps 1.17 to 1.19 are written only after the owner answers GQ-11 (step 1.0b) and the PR #422 overlap check (step 1.16a) is done. WC-14 and its pins stay deliverables of this PR whatever #422 does (SPEC line 420).

**Placement.** `src/superclaude/core/WORKER-CONTRACT.md`, a new subsection after the fan-in rule paragraph (line 156) and before `### Worked example: gate hit, answer, new Task` (line 158).

**Final text.** The SPEC section 10 text (lines 404-408), unchanged, with one sentence appended at the end (SP-27, deviation D6):

```markdown
### WC-14. Coordinator loop

The coordinator keeps watching its Run until every Task it created is settled and every result has been inspected and its admission or rejection recorded. It never stops watching on its own. When a wait on Orca expires, the coordinator re-arms it. On every coordinator wake, the coordinator runs `/sc:sweep` and reads its report before it acts. It sweeps on every wake and keeps a periodic sweep scheduled while work remains. Phase 1 adds this duty, not a scheduler. The sweep's classes follow WC-10: only Orca's stall proofs make a worker stalled; anything else it cannot prove is could not determine. A missing heartbeat is absence, never death. The coordinator escalates to the person, and does not act alone, on: a failed or blocked result it cannot retry under WC-6, a partial result it judges unusable, a third brief-guard refusal, a ready Task it did not create, needing ownership review, a frozen plan, and a fan-in with fewer than 2 admitted inputs. Person-started sessions appear in the report, observed from transcripts and ccsession files; they are never messaged. The sweep report is a dated local file; it is never posted. The sweep recommends nothing: no stop, retry, release, merge or removal. The coordinator decides and performs any action under those rules. The coordinator records each admission or rejection in its run notes; the sweep does not observe them.
```

The appended sentence closes a gap the panel found (SP-27): the end condition names "admission or rejection recorded", but the sweep has no source for that record, so the text says where it lives and that the sweep cannot see it. It adds no pin. The text holds no lock sentence (SPEC line 410).

**Pins** in `tests/skills/test_worker_contract.py`:

- Add to `RULE_PHRASES` (the dict at line 25; WC-13 is at line 155): `"WC-14": ("WC-14", ["WC-14. Coordinator loop", "On every coordinator wake", "it is never posted", "It never stops watching on its own"])`. Each phrase occurs verbatim in the final text above.
- Append `"/sc:sweep"` to `NEVER_AS_WORKER` (lines 245-254), giving 9 entries. The parametrized removal test at line 624 then covers it with no further change.
- Rename `test_never_as_worker_list_names_all_seven_commands` (line 545) to `test_never_as_worker_list_names_every_listed_command`. The body is unchanged.
- Add `assert "sweep" not in UNATTENDED_COMMANDS` next to the existing `"load"` assertion (line 865). The equality check at line 470 holds with no edit, because `sweep.md` has no `## Unattended mode` section.

**Never-as-worker addition.** `WORKER-CONTRACT.md` line 23 becomes:

> - **Never-as-worker list**: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn`, `/sc:sweep` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers. These are never dispatched as workers and get no `--unattended` mode. The list changes only when the coordinator-only command set or D3 changes, never per phase. If D3 adds a worker route for pr-submit, D3 also states how that route passes the brief guard.

Only the command list changes. The term line stays one line, which `_check_never_as_worker` (line 398) requires. Adding `/sc:sweep` is a change to the coordinator-only command set, so it fits the line's own rule. The same list is copied in the developer guide (section 9).

````

### docs/designs/orchestrator-mode.md:688-709

````markdown
## 9. Routing and documentation changes

All edits are to existing files; no new doc file. Rows and bullets are added, none removed or reworded.

| # | File | Change | Checked by |
|---|---|---|---|
| R1 | `src/superclaude/core/HOW-WE-WORK.md`, `<!-- other-commands:v1 -->` table (lines 318-337) | One row, placed after `/sc:spawn` (line 333): `` `/sc:sweep` `` with "Read-only supervision snapshot of the bound Orca Run, its worktrees and person-started sessions. Writes one dated report under `.dev/sweeps/` and prints JSON; it changes nothing else and recommends nothing. Coordinator or person only, never a worker." | `tests/core/test_how_we_work_routing_table.py` |
| R2 | Same file, `## Orca coordination` (line 396) | One bullet after the never-workers bullet (line 403): "**The coordinator sweeps on every wake.** WC-14 in `~/.claude/WORKER-CONTRACT.md` has the coordinator run `/sc:sweep` and read its report before it acts. The sweep is read-only and is itself never a worker." | R1 test plus parity test |
| R3 | `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` | Byte copy of R1+R2 result, made in the same commit | `tests/commands/test_routing_plugin_parity.py` line 38 (`filecmp.cmp(..., shallow=False)`) |
| R4 | `tests/core/test_how_we_work_routing_table.py` `_OTHER_COMMANDS` (line 27) | Add `"sc:sweep"` | itself |
| R5 | `tests/recommend/test_routing_refresh.py` `_POST_REFRESH_ADDITIONS` (line 33) | `{"graph", "impact", "issue", "sweep"}` | itself (assertion at line 648) |
| R6 | `docs/user-guide/commands.md`, `### 8. UTILITIES` (line 105) | One row after `/sc:issue` (line 115): `` `/sc:sweep` `` . "Read-only snapshot of a Run, its worktrees and person sessions" . `sweep.md` . "Report only (writes `.dev/sweeps/`)" | manual review |
| R7 | `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` line 991 | Add `/sc:sweep` to the copied never-as-worker list, same order as section 8 | manual review against `WORKER-CONTRACT.md` line 23 |
| R8 | `CHANGELOG.md`, `## [Unreleased]` (line 5) | One `### Added` entry: `superclaude sweep run`, `/sc:sweep`, `sc-sweep-protocol`, WC-14, `.dev/sweeps/` ignored | manual review |

Rules:

- R1, R2 and R3 land in one commit. Editing R1 or R2 without R3 fails the parity test.
- The level table is not touched, so the `src/superclaude/core/CLAUDE.md` level-table copy (project CLAUDE.md, Key Documentation Files) needs no re-run. If a later edit touches the level table, that copy is re-run in the same commit.
- R1 and R6 avoid the words stop, retry, release, merge and removal in the sweep's description.
- No `.claude/` path is staged; `make sync-dev` then `make verify-sync` (step 1.25) refresh the dev copies.

````

### docs/designs/orchestrator-mode.md:878-897

````markdown
What it records:

| # | Item | Feeds |
|---|---|---|
| 1 | `run-current` output when a Run is bound, and when none is bound (the no-binding shape) | `bind_run`, FR-002 fourth test, FR-026 case 4 |
| 2 | Whether `run-current` output is parseable without `--json` | M2, section 7.3 |
| 3 | `worker-list --run <run> --json` schema, page size and the cursor or continuation field, if any | `WORKER_LIST_PAGE`, the cursor template (section 7.3) |
| 4 | `worker-show --dispatch <dispatch> --json` field names: the field that can carry `session_join` (a Claude session id, pane key or terminal handle), `agentWait` presence and value, `liveness.verdict`, `status`, and the fields that carry the Dispatch start and end times | Rule 5, the join paths of section 7.2, the path-B time window, GQ-108, open item 23 |
| 5 | `task-list --ready --run <run> --json` and `task-list --run <run> --json` shapes, and whether a creator field exists | Rule 4 (b), Waiting (b) sub-heading |
| 6 | `worktree ps --json`: the worktree path field | Worktree discovery, M3 |
| 7 | `worktree list --json` and `worktree current --json` shapes (recorded only; Phase 1 does not call them) | M3 |
| 8 | The error shape of `worker-list --run <unknown id>` (stderr and exit code) | FR-002 unknown-Run case |
| 9 | The `runtime_unavailable` shape, only if Orca is already unavailable during the capture; it is never induced | FR-026 case 1 marker |
| 10 | Run id and Dispatch id samples, from which `RUN_ID_RE` and `DISPATCH_ID_RE` are written | `_check_run_ids`, template placeholders |
| 11 | Whether each template accepts its flags as written (exit 0 with parseable output) | NFR-014 pin |
| 12 | The installed Orca version string from `/opt/Orca/resources/app.asar.unpacked/out/package.json` | NFR-015 |
| 13 | For each worker of the named Run: whether `orca-tabs/` holds an entry for its pane (read the files only), and whether the item 4 field equals that entry's file name or terminal handle. Also whether workers are launched through `ccsession`, which decides whether they get an entry at all (section 1) | Join path B, the D9 fixtures, open item 22 |

If an item cannot be captured, it stays UNVERIFIED in section 17 and the code path it feeds keeps its could-not-determine behaviour (for example, no `session_join` means `person_started` None for every unmatched transcript).

````

### docs/designs/orchestrator-mode.md:984-993

````markdown
| 16 | The Claude Code transcript format (one sample read) and how a worktree path maps to its `~/.claude/projects/<project key>/` folder | Step 1.0a, by reading transcripts of the named Run's worktrees (a disk read, not an Orca call) | A transcript is unreadable as defined in 7.2 (observation rule for SPEC line 442: open raises `OSError`, or the tail holds no complete record with both `timestamp` and `sessionId`), and its row is could not determine |
| 17 | Whether `make sync-dev` removes deleted `.claude/` copies | First rollback, or a dry check at step 1.25 | Rollback deletes them by hand and never stages them (section 16) |
| 18 | The effect of `uv run --frozen --no-sync` (flags seen in `uv run --help`, not run) | Step 1.29 or a manual run before release | The skill tries PATH first; the fallback is used only on "command not found" |
| 19 | The rationale for the proposed byte limits (1 MiB, 256 KiB, 8 MiB; SP-28) | Before release, recorded in the task package | The limits apply as proposed and are marked proposed in `probes.py` |
| 20 | Owner decisions GQ-10, GQ-11 (WC-14 approval), GQ-35, GQ-61 and GQ-63 | Step 1.0b | Steps 1.17 to 1.19 do not start |
| 21 | PR #422 overlap with WC-14, the never-as-worker list and the #409 dimensions | Step 1.16a | Steps 1.17 to 1.19 do not start; WC-14 stays a deliverable of this PR whatever #422 does |
| 22 | Whether Orca workers get tab-map entries (launched through `ccsession`) and which tab-map value equals the item 4 field; and the owner's sign-off on the D9 narrowing of SP-29 | Step 1.0a item 13; step 1.0b | Join path B is not used; a tab-map entry that joins no scoped row gives None; the classify step does not start until the owner signs off D9 or names a stricter rule. Until closed, every no-entry True carries the `origin not proved` note (7.2) |
| 23 | The `worker-show` fields that carry a Dispatch row's start and end times, used by the path-B time window (7.2) | Step 1.0a item 4 | No path-B join is made: every path-B match is could not determine with note `pane moved to a later session`, and its transcript is None |

Total: 23 open items.
````

### docs/designs/orchestrator-mode.md:995-1013

````markdown
## 18. Revision log: fix cycle 1

Changes made for the blocking findings of `docs/designs/orchestrator-mode-review-1.md`. Minor note m5 was applied because it falls inside the B1 edit; the other minor notes are not addressed in this cycle.

| ID | Finding | Change |
|---|---|---|
| B1 | A temp-file unlink failure after the commit point exited 0 with two names on disk, against NFR-001 | That case now exits 1 with `[sweep publish] could not remove temp file <path>` and no success JSON, and the complete report stays (3.2 step 7 and table, 3.3, 3.4 rule, sequence diagram). Section 1 and the section 16 rollback sentence (m5) now say a successful run leaves one report plus its directory when new. Added the `os.unlink` failure case to `test_cli_contract.py` and the no-second-name check to `test_readonly.py` (11). Updated the NFR-001 and G-1 rows (12). Recorded under "Not counted as deviations" as a joint reading of FR-017 and NFR-001 (13) |
| B2 | The person-started rule assumed every Orca-pane session has a tab-map entry and treated any entry as a worker, which FR-010 does not say | Checked the ccsession source: entries are written only for `ccsession` launches with a valid pane key and terminal handle, each pane keeps only its latest session, and nothing marks a worker pane (1). A worker is now a transcript joined to a scoped Dispatch row; an unjoined tab-map entry gives None; a transcript with no entry may be True when the guard holds; path B adds a stale-entry case to the guard (7.2). The narrowing is D9, with its reason, the owner sign-off at step 1.0b and four `test_classify.py` fixtures (11, 13, 14, 15). Added capture item 13 and open item 22 (15.1, 17). Updated the FR-010 row (12) |
| B3 | SPEC behaviours had no rule, fixture or traceability row | Added the observation rules to 7.2: WC-13 note and Retained problems, show wins, unknown schema field, duplicate Dispatch, input changed between reads, path escapes its source, worktree removed, unreadable transcript or contract, rule 6 wording and SP-07, `FINAL:` reading, remote coverage, and the SP-16 literal. Added each fixture to `test_probes_allowlist.py` (nine byte-limit boundaries, 440, 443, 446, 450, 451, 452), `test_classify.py` (SP-07, `FINAL:`, 442, WC-13, late heartbeat) and `test_report.py` (rule 6 wording, 454, WC-13, SP-16) (11). Named them in the FR-006, FR-010, FR-013, FR-014, FR-020 and NFR-007 rows and added rows for the SPEC section 11 failure modes and the section 7 cross-cutting notes (12) |

### Fix cycle 2

Changes made for the blocking findings of `docs/designs/orchestrator-mode-review-2.md`. Minor note m4 was applied because it falls inside the R2-B1 edit; the other minor notes are not addressed in this cycle. The `tab map join not observable` note for a None `session_join` is kept on purpose, because SPEC line 236 requires the SP-16 literal only when worker rows exist and nothing joined (review 2 m5).

| ID | Finding | Change |
|---|---|---|
| R2-B1 | Under path B, a scoped worker's pane can move to a later session (`/clear`, resume, person rerun), so the later session joins the Dispatch row and the worker's real transcript can become True | A path-B join now also needs session identity: the transcript's earliest timestamp must fall inside the Dispatch row's time window, else the row is could not determine and the transcript None with note `pane moved to a later session`; a join inside the window carries `joined by pane: latest session of the pane` (7.2). Added a fourth guard case: under path B with any scoped Dispatch row, every unjoined no-entry transcript is None with note `earlier pane session not joinable (tab map keeps only the latest session)`, and the no-entry True path is path A only (7.2). Said which notes apply when guard cases 1 and 2 hold together (m4). Added `/clear`, resume and person-rerun fixtures and changed "three" to "four" incomplete cases (11). Updated D9, the FR-010 and SP-29 rows (12, 13, 14), capture item 4 (15.1) and added open item 23 for the time fields (17) |
| R2-B2 | A worker of an unscoped Run with no tab-map entry could be shown as person-started True with no note | Every no-entry True now carries note `origin not proved: no tab-map entry; may be a worker of a Run outside the scope`, in the report row and the JSON `notes` (7.2, D9). Changed the third D9 fixture and added an unscoped-Run worker fixture in `test_classify.py`, and a `test_report.py` case that prints the note (11). Open item 22 states the note until it closes (17) |
| R2-B3 | The unreadable-transcript rule fired only on `OSError` at open, but its truncated-JSONL fixture expected `unscanned: transcript not readable` | A transcript is now unreadable when its open raises `OSError` or its 256 KiB tail holds no complete JSON record with both `timestamp` and `sessionId`; a last line cut mid-object is skipped, and the transcript stays readable when an earlier complete record exists (7.2). The fixture now names the cut record, adds the readable last-line-cut case and an `OSError` case (11). Open item 16 points to the same rule (17) |
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:70-76

````markdown
# Issue #339 Phase 1: orchestrator-mode design closure and the read-only `superclaude sweep` build

## Task Overview

The person running several Claude sessions needs one read-only report that answers "who needs me and what is safe to close" without opening each session (issue #339). The design `docs/designs/orchestrator-mode.md` (DESIGN) specifies that report as a coordinator-only `superclaude sweep run` CLI, a thin `/sc:sweep` command, the `sc-sweep-protocol` skill and a coordinator-loop contract rule. Before any code is written, this task closes five required design items: R3-B1 (the path-B time window reads three time fields the data model lacks), R3-B2 (two Dispatch rows on one pane have no deciding rule), R3-B3 (three SPEC FR-010 fixtures were dropped), R4 (re-anchor the design to master `5dc29d23`, including renumbering the coordinator-loop rule from WC-14 to WC-16 because master already has WC-14 and WC-15 from PR #434), and R5 (an owner decision on `--agent-wait`, which is a HALT item this task never resolves by itself).

After the design items, the task records the owner decisions of step 1.0b, captures the step 1.0a read-only Orca evidence against a Run the person names, writes the step 1.16a record, and then implements the design in its section 15.2 step order, one item per file. Every phase is closed by validation and a QA gate at full intensity (report-only lens agents, one fix agent, then verification, at most 2 fix cycles). The final phase runs the full validation set, the final and fidelity gates, writes a working-tree diff file and runs an independent `/sc:reflect --mode post` audit. The task never commits, pushes or merges; the PR is opened later only through `/sc:pr-submit --monitor 3`.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:142-153

````markdown
### Source Areas
- `superclaude.cli.sweep` (new package): models, classify, probes, report, commands.
- `superclaude.cli.main` (CLI entry point, deferred subcommand registration).
- `superclaude.cli.recommend` (the lazy `__getattr__` package pattern to copy).
- `superclaude.cli.reflect` (the `_git` seam pattern) and `superclaude.cli.sprint` / `superclaude.cli.swarm` (the link-and-fsync publish pattern).
- `commands` primitives: the new `sweep` command; `issue` and `graph` as heading and Activation patterns.
- `skills` primitives: the new `sc-sweep-protocol` skill.
- `core` framework docs: `WORKER-CONTRACT`, `HOW-WE-WORK`.
- `plugins/superclaude` sc-recommend refs mirror (HOW-WE-WORK byte copy).
- Tests: `tests/sweep` (new), `tests/commands`, `tests/skills` (worker contract pins), `tests/core` (routing table), `tests/recommend` (routing refresh).
- Docs: user guide commands table, developer guide never-as-worker copy, CHANGELOG, `.gitignore`.
- Design documents: `docs/designs` orchestrator-mode design.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:238-253

````markdown
## Phase 2: Design fix R3-B1 (path-B time fields) and its gate

All Phase 2 edits go to `docs/designs/orchestrator-mode.md` (DESIGN). Read research/04-design-fixes-r3.md section 2 (lines 75-140) in chunks of at most 150 lines before the first edit. Anchor every edit by its quoted text; the line numbers below are orientation only.

- [ ] **2.1 — R3-B1 edits 1 to 3: the 7.2 model rows and the time-parsing rule**
  - **Context**: The path-B window at DESIGN section 7.2 (worker bullet, near line 494) compares the earliest transcript timestamp with the Dispatch row's start and end, but `OrcaObservation` (near line 455) has no time field and `TranscriptTail` (near line 457) has only `last_record_ts`, so pure `classify.py` cannot evaluate the rule (research/04:80). The static Orca 1.4.245 bundle shows `worker-show --json` carries `dispatch.dispatchedAt`, `dispatch.completedAt` and `dispatch.status` (research/04 Summary, R3-B1).
  - **Action**: Apply research/04 section 2.2 edits 1, 2 and 3 (research/04:87-89) with the wording given there: (1) in the 7.2 `OrcaObservation` row, replace the whole tail of the row, from "plus `dispatch: str`" to the end of its parenthesis (the row already holds "plus `dispatch: str`, `run: str`, `session_join: str \| None` (design: ...)"), with the edit 1 text, which restates those three fields and adds `dispatch_started: datetime | None`, `dispatch_ended: datetime | None` and `dispatch_status: str | None`, so the three existing fields appear once only; (2) insert `first_record_ts: datetime | None` after `last_record_ts: datetime \| None` in the `TranscriptTail` row; (3) add the "Time parsing (design)" sentence after the table that ends with the `TabMapEntry` row, before "Constants in `models.py`". Inside a table row, write every `|` that is part of the cell text as `\|` (DESIGN already writes `str \| None` this way at the `OrcaObservation` and `TranscriptTail` rows), so the copied type texts do not split the cells. Read the full wording of each edit from research/04 lines 87-89; do not shorten it.
  - **Output**: DESIGN section 7.2 with the three edits.
  - **Verification**: Verify: `grep -n 'first_record_ts' docs/designs/orchestrator-mode.md` shows a hit in the `TranscriptTail` row; `grep -n 'dispatch_started' docs/designs/orchestrator-mode.md` shows a hit in the `OrcaObservation` row; `grep -o 'plus `dispatch: str`' docs/designs/orchestrator-mode.md | wc -l` prints 1 (the field list is not duplicated); the `OrcaObservation` row and the `TranscriptTail` row each have the same count of unescaped `|` separators as the table's header row (count with `grep -o '[^\\]|'` on each line, plus one for a leading `|`); `grep -n 'Time parsing (design)' docs/designs/orchestrator-mode.md` shows one hit before "Constants in `models.py`". If an anchor text is not found, or a count differs, log it in `### Phase 2 Findings` with the text searched and stop.
  - **Completion gate**: The three edits are in DESIGN. Once done, mark this item as complete.

- [ ] **2.2 — R3-B1 edit 4: the path-B window rule in the 7.2 worker bullet**
  - **Context**: The worker bullet of DESIGN 7.2 (near line 494) still says "A path-B join therefore also needs session identity: the earliest `timestamp` in the transcript tail must fall inside the Dispatch row's own window ..." and calls the `worker-show` time fields UNVERIFIED (research/04:90). The same bullet then says "A path-B match outside that window, or on a row with no observable start time, does not join: the row is could not determine with note `pane moved to a later session`, and that transcript is None with the same note." research/04 edit 4 (research/04:90) replaces both passages; the second replacement folds in review-3 note m5 and gives a row with no observable window its own note, `Dispatch time window not observable`, which the item 2.5 fixture `test_path_b_row_without_start_has_no_window` expects.
  - **Action**: Make the two replacements of research/04 section 2.2 edit 4 (research/04:90), each anchored by its quoted text and copied verbatim from research/04: (1) replace the passage that begins "A path-B join therefore also needs session identity:" and ends "(open item 23)." with the edit 4 text that names `first_record_ts`, `dispatch_started`, `dispatch_ended` and `dispatch_status`, the inclusive whole-second UTC window, and the end bound `collected_start` for a `pending` or `dispatched` row that has not ended; (2) replace the sentence that begins "A path-B match outside that window, or on a row with no observable start time, does not join:" with the edit 4 text "A path-B match outside that window does not join: the row is could not determine with note `pane moved to a later session`. A match on a row with no observable window does not join: the row is could not determine with note `Dispatch time window not observable`. Several matching rows follow the R3-B2 rule below."
  - **Output**: DESIGN section 7.2 worker bullet with the window rule naming the model fields and the separate no-window note.
  - **Verification**: Verify: the worker bullet now contains `first_record_ts`, `dispatch_started` and `dispatch_ended`; `grep -c 'fields that carry those times are UNVERIFIED' docs/designs/orchestrator-mode.md` returns 0; `grep -c 'or on a row with no observable start time, does not join' docs/designs/orchestrator-mode.md` returns 0; `grep -n 'A match on a row with no observable window does not join' docs/designs/orchestrator-mode.md` returns one hit in section 7.2 and that line contains `Dispatch time window not observable`. If either quoted anchor is not found, log it in `### Phase 2 Findings` and stop.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:256-282

````markdown
- [ ] **2.3 — R3-B1 edits 5 and 6: the 7.1 reader comment and GQ-103(3) in 2.2**
  - **Context**: DESIGN 7.1 (near line 398) has the transcript-tail reader comment; DESIGN 2.2 GQ-103(3) (near line 60) lists the fields pure `classify.py` reads (research/04:91-92).
  - **Action**: (5) change the 7.1 comment to "`# last 256 KiB, first partial line dropped; sets first_record_ts and last_record_ts`"; (6) append to the GQ-103(3) field list: "`OrcaObservation.dispatch_started`, `dispatch_ended`, `dispatch_status` and `TranscriptTail.first_record_ts` (the path-B window)". Both texts are in research/04:91-92.
  - **Output**: DESIGN sections 7.1 and 2.2 updated.
  - **Verification**: Verify: `grep -n 'sets first_record_ts and last_record_ts' docs/designs/orchestrator-mode.md` returns one hit in section 7.1, and the GQ-103 row in section 2.2 contains `dispatch_status`. If an anchor is missing, log it in `### Phase 2 Findings` and stop.
  - **Completion gate**: Both edits are in DESIGN. Once done, mark this item as complete.

- [ ] **2.4 — R3-B1 edits 7 and 8: step 1.0a item 4 (15.1) and open item 23 (17)**
  - **Context**: DESIGN 15.1 item 4 (near line 885) says "and the fields that carry the Dispatch start and end times"; DESIGN 17 open item 23 (near line 991) names those fields as unknown (research/04:93-94).
  - **Action**: (7) replace the 15.1 item 4 phrase with the research/04 edit 7 text, naming `dispatch.dispatchedAt`, `dispatch.completedAt` and `dispatch.status` and the one-worker ordering record; (8) reword open item 23 with the research/04 edit 8 text, keeping it as item 23 (no new open item) and changing its "Behaviour until closed" note to `Dispatch time window not observable`.
  - **Output**: DESIGN sections 15.1 and 17 updated.
  - **Verification**: Verify: `grep -n '^Total: 23 open items.' docs/designs/orchestrator-mode.md` still returns one hit; 15.1 item 4 contains `dispatch.dispatchedAt`; open item 23 contains `Dispatch time window not observable`. If an anchor is missing, log it in `### Phase 2 Findings` and stop.
  - **Completion gate**: Both edits are in DESIGN. Once done, mark this item as complete.

- [ ] **2.5 — R3-B1 fixtures in section 11 and the FR-010 trace in section 12**
  - **Context**: research/04:99-117 lists the R3-B1 fixtures; research/09-gap-fill.md Gap 4 gives the names: in the `tests/sweep/test_probes_allowlist.py` row (DESIGN section 11, near line 738) `test_read_transcript_tail_sets_first_and_last_record_ts`, `test_read_transcript_tail_first_record_ts_is_minimum`, `test_read_transcript_tail_first_record_ts_over_256k`, `test_worker_show_dispatch_times_sqlite_form`, `test_worker_show_dispatch_times_iso_z_form`, `test_worker_show_dispatch_times_missing_or_bad`; in the `tests/sweep/test_classify.py` row (near line 739) `test_path_b_window_open_row_joins`, `test_path_b_window_inclusive_bounds`, `test_path_b_terminal_row_without_end_has_no_window`, `test_path_b_row_without_start_has_no_window`. research/04 gives no section 12 edit for R3-B1; research/09 Gap 4 recommends adding the parser file to the FR-010 trace (a builder decision, recorded in OQ-14).
  - **Action**: Append the 6 parser fixtures, each with the one-line expectation from research/04:99-108, to the test column of the `test_probes_allowlist.py` row, and add FR-010 to that row's Covers cell. Append the 4 window fixtures with their expectations from research/04:110-117 to the `test_classify.py` row. In section 12, add `sweep/test_probes_allowlist.py` (the six reader and parser fixtures) to the FR-010 row's test column.
  - **Output**: DESIGN sections 11 and 12 updated.
  - **Verification**: Verify: each of the 10 fixture names returns exactly one `grep -c` hit in DESIGN; the `test_probes_allowlist.py` row's Covers cell contains FR-010; every edited table row has the same number of `|` separators as before the edit. If a row is not found, log it in `### Phase 2 Findings` and stop.
  - **Completion gate**: 10 fixtures and the FR-010 trace are in DESIGN. Once done, mark this item as complete.

- [ ] **2.6 — R3-B1 edit 9: the Fix cycle 3 revision table in section 18**
  - **Context**: research/04:95 (edit 9) asks for a new `### Fix cycle 3` table under DESIGN section 18, after the `### Fix cycle 2` table, rather than rewriting the cycle 2 row, so the cycle history stays true. The cycle 2 table form is `| ID | Finding | Change |`.
  - **Action**: Add `### Fix cycle 3` after the last row of the `### Fix cycle 2` table, with one intro sentence ("Changes made for the blocking findings of review 3 and the re-anchor to master `5dc29d23`.") and the table header `| ID | Finding | Change |`, then the R3-B1 row with the change text of research/04 edit 9. Later phases append the R3-B2, R3-B3, R4 and R5 rows to this table. Then make the second part of edit 9 (review 3 note m2): in the `### Fix cycle 2` table's R2-B1 row (near line 1011), replace "the transcript's earliest timestamp" with "the earliest `timestamp` in the transcript tail", and change nothing else in that row.
  - **Output**: DESIGN section 18 with `### Fix cycle 3` and its R3-B1 row, and the m2 wording in the cycle 2 R2-B1 row.
  - **Verification**: Verify: `grep -n '^### Fix cycle 3' docs/designs/orchestrator-mode.md` returns one hit after the `### Fix cycle 2` hit, and the next table row starts `| R3-B1 |`; `grep -c "the transcript's earliest timestamp" docs/designs/orchestrator-mode.md` returns 0, and the `| R2-B1 |` row contains "the earliest `timestamp` in the transcript tail". If the cycle 2 table or the m2 anchor is not found, log it in `### Phase 2 Findings` and stop.
  - **Completion gate**: The table, its R3-B1 row and the m2 wording exist. Once done, mark this item as complete.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:419-442

````markdown
## Phase 3: Design fix R3-B2 (several Dispatch rows on one pane) and its gate

All Phase 3 edits go to DESIGN. Read research/04-design-fixes-r3.md section 3 (lines 120-176) before the first edit. Anchor every edit by quoted text; review-3 line numbers are 6 lower than the current design (research/04:232).

- [ ] **3.1 — R3-B2 edit 1: the several-rows rule in the 7.2 worker bullet**
  - **Context**: DESIGN 7.2 worker bullet (near line 494) defines a path-B join for one row but no rule decides when several scoped Dispatch rows match one tab-map entry (research/04 section 3.1). Static evidence: `orchestration dispatch` refuses a second active row on one pane key or handle, so rows are normally sequential, but overlap stays possible (research/04:142-144).
  - **Action**: After the sentence ending "...because a person rerun inside the window cannot be told apart.", insert the research/04:148 edit 1 text verbatim, beginning "Several scoped Dispatch rows can match one tab-map entry by path B" and ending "...instead of `Orca pane session, not in scoped Runs` (line 495)." Replace the literal "(line 505)" and "(line 495)" inside the inserted text with the line numbers those passages have after Phase 2, or with a section reference ("as for duplicate Dispatch rows, in this bullet"), whichever is accurate; record the choice in `### Phase 3 Findings`.
  - **Output**: DESIGN 7.2 with the several-rows rule.
  - **Verification**: Verify: `grep -c 'conflict: one pane session matches several Dispatch rows' docs/designs/orchestrator-mode.md` is at least 1 in section 7.2; `grep -c 'pane moved to a later session'` is at least 1 in 7.2; any line number cited in the new text points at the passage it names. If the anchor sentence is not found, log it in `### Phase 3 Findings` and stop.
  - **Completion gate**: The rule is in 7.2. Once done, mark this item as complete.

- [ ] **3.2 — R3-B2 edit 2: the seven fixtures in the section 11 `test_classify.py` row**
  - **Context**: research/04:154-164 lists seven fixtures with Given, When and Then: `test_path_b_pane_reused_joins_later_row_only`, `test_path_b_two_windows_hold_session_is_conflict`, `test_path_b_shared_boundary_second_is_conflict`, `test_path_b_no_matching_window_holds`, `test_path_b_multi_row_result_ignores_row_order`, `test_path_b_entry_failing_window_note_order`, `test_path_b_rows_share_terminal_handle`. Placement (research/04:149, research/09 Gap 4): after "a row with no observable start time never joins by path B;" in the DESIGN section 11 `tests/sweep/test_classify.py` row (near line 739).
  - **Action**: Insert the seven fixture names at that point, each followed by its one-line Then from research/04:158-164, in the table order. The fixture texts must quote the note literals `joined by pane: latest session of the pane`, `pane moved to a later session` and `conflict: one pane session matches several Dispatch rows`.
  - **Output**: DESIGN section 11 `test_classify.py` row with the seven fixtures.
  - **Verification**: Verify: each of the seven names returns exactly one `grep -c` hit in DESIGN; the row keeps its cell count. If the anchor phrase is not found, log it in `### Phase 3 Findings` and stop.
  - **Completion gate**: The seven fixtures are in section 11. Once done, mark this item as complete.

- [ ] **3.3 — R3-B2 edits 3 and 4: the FR-010 row (12), D9 (13) and SP-29 (14)**
  - **Context**: research/04:150-151 and research/09 Gap 4 (09:164, 09:167). FR-010 row near DESIGN line 764; D9 near line 815; SP-29 near line 853.
  - **Action**: (3) In the FR-010 row, after "with a path-B join also needing the Dispatch row's time window", add ", and one rule for several rows matching one pane session (join only the one row whose window holds it; `conflict:` when two or more do)". (4) In D9, after "a path-B join also needs the Dispatch row's time window", and in SP-29, after "a path-B join needs the Dispatch row's time window", add "and, when several rows match one pane session, exactly one window holding it".
  - **Output**: DESIGN sections 12, 13 and 14 updated.
  - **Verification**: Verify: `grep -c 'exactly one window holding it' docs/designs/orchestrator-mode.md` returns 2 (D9 and SP-29); the FR-010 row contains `one rule for several rows matching one pane session`; `grep -n '^Total: 9 deviations.'` still returns one hit. If an anchor is missing, log it in `### Phase 3 Findings` and stop.
  - **Completion gate**: The three rows agree with 7.2. Once done, mark this item as complete.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:586-609

````markdown
## Phase 4: Design fix R3-B3 (the SPEC's three incomplete-case fixtures) and its gate

All Phase 4 edits go to DESIGN. Read research/04-design-fixes-r3.md section 4 (lines 178-215) and SPEC `merged-requirements.md` FR-010 (near line 104) before the first edit. Anchor by quoted text.

- [ ] **4.1 — R3-B3 edit 2: the list-incomplete bullet in 7.2**
  - **Context**: DESIGN 7.2 has no rule or note for the list-incomplete half of the FR-010 guard (research/04:182). The SPEC reasons are "Orca unavailable, worker list truncated, worker list call failed" (SPEC near line 104).
  - **Action**: Insert a new bullet before the bullet that begins "The guard's 'join completed' condition fails" (near DESIGN line 497), with the research/04:187 edit 2 text verbatim, from "List-incomplete cases (SPEC FR-010):" to "...even when its activity is older than the window."
  - **Output**: DESIGN 7.2 with the list-incomplete bullet.
  - **Verification**: Verify: `grep -n 'origin unknown: Orca unavailable\|origin unknown: worker list truncated\|origin unknown: worker list call failed' docs/designs/orchestrator-mode.md` shows all three literals in section 7.2, in that order. If the anchor bullet is not found, log it in `### Phase 4 Findings` and stop.
  - **Completion gate**: The bullet is in 7.2. Once done, mark this item as complete.

- [ ] **4.2 — R3-B3: name the per-Run source row `orca worker-list <run>` in 7.4**
  - **Context**: The new 7.2 bullet reads the `sources` row `orca worker-list <run>` and its `unscanned` field, but DESIGN section 7.4 shows only `{"name": str, ...}` for a source row (research/04:187). research/04 calls the name a design choice that needs the gate's approval.
  - **Action**: In section 7.4, beside the `sources` entry, add one sentence: "Each scoped Run's `worker-list` call has its own source row named `orca worker-list <run>`; a `call_failed` result sets its `unscanned` reason (for example `orca call failed (exit 1)`)." Do not change the JSON key set.
  - **Output**: DESIGN section 7.4 updated.
  - **Verification**: Verify: `grep -c 'orca worker-list <run>' docs/designs/orchestrator-mode.md` is at least 2 (7.2 and 7.4). If the `sources` entry is not found in 7.4, log it in `### Phase 4 Findings` and stop. Record in `### Phase 4 Findings` that the name is a design choice for the gate to approve.
  - **Completion gate**: The source row is named. Once done, mark this item as complete.

- [ ] **4.3 — R3-B3 edit 1 and fixtures: the section 11 `test_classify.py` row**
  - **Context**: The DESIGN section 11 `tests/sweep/test_classify.py` row (near line 739) says "the four incomplete cases" (research/04:186). Fixtures (research/04:191-200, research/09 Gap 4): `test_fr010_outage_older_transcript_unknown_not_historical`, `test_fr010_full_page_uncaptured_continuation`, `test_fr010_call_failed_incomplete_list`, `test_fr010_incomplete_notes_order`. The shared Given is at research/04:193. Keep the FR-010 complete-negative-join control beside them (research/04:202).
  - **Action**: Replace "the four incomplete cases" with the research/04:186 replacement text, keeping the four guard-case fixtures that the same cell lists later. Then add the four fixture names, each with its Then from research/04:197-200, quoting the three `origin unknown:` literals, next to the complete-negative-join control.
  - **Output**: DESIGN section 11 `test_classify.py` row updated.
  - **Verification**: Verify: `grep -c 'the four incomplete cases' docs/designs/orchestrator-mode.md` is 0; each of the four fixture names has exactly one hit; the words "outage" and "uncaptured continuation" appear in section 11; the complete-negative-join control is still in the row. If the phrase is not found, log it in `### Phase 4 Findings` and stop.
  - **Completion gate**: The row names the three SPEC cases and four fixtures. Once done, mark this item as complete.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:611-623

````markdown
- [ ] **4.4 — R3-B3 edit 3: the FR-010 row in section 12**
  - **Context**: research/04:188; FR-010 row near DESIGN line 764 (already edited by item 3.3).
  - **Action**: In the design column, after "completeness guard", add "with its three list-incomplete cases (outage, full page, `call_failed`) and". In the test column, add "the three SPEC incomplete-case fixtures" to the `sweep/test_classify.py` parenthesis.
  - **Output**: DESIGN section 12 FR-010 row updated.
  - **Verification**: Verify: the FR-010 row contains `three list-incomplete cases` and `the three SPEC incomplete-case fixtures`, and keeps its cell count. If the anchor is missing, log it in `### Phase 4 Findings` and stop.
  - **Completion gate**: The row is updated. Once done, mark this item as complete.

- [ ] **4.5 — R3-B3 edit 4: the Fix cycle 3 R3-B3 row**
  - **Context**: research/04:189 gives the row text, which also corrects the cycle 2 "changed three to four incomplete cases" wording.
  - **Action**: Append `| R3-B3 | <finding> | <change> |` after the R3-B2 row, with the finding "Three SPEC FR-010 fixtures (outage, full page, `call_failed`) were dropped from `test_classify.py`" and the change text of research/04:189, adding "and named the per-Run source row `orca worker-list <run>` (7.4)". Leave the rest of the cycle 2 R2-B1 row unchanged (item 2.6 already applied the m2 wording); the cycle 3 row corrects the "three to four incomplete cases" wording.
  - **Output**: DESIGN section 18 with the R3-B3 row.
  - **Verification**: Verify: the `### Fix cycle 3` table has R3-B1, R3-B2 and R3-B3 in that order.
  - **Completion gate**: The row is in place. Once done, mark this item as complete.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:760-790

````markdown
## Phase 5: Design fix R4 (reconcile DESIGN with master `5dc29d23`) and its gate

All Phase 5 edits go to DESIGN. research/07-reanchor-contract.md and research/08-reanchor-routing.md are authoritative here; where research/01 to research/06 disagree with them, research/07 and research/08 win. Read research/07 (173 lines) and research/08 (126 lines) in chunks of at most 150 lines before the first edit. "Routing row R1 to R8" means the DESIGN section 9 table rows; "design fix R4" is this phase.

- [ ] **5.1 — R4: renumber the coordinator-loop rule to WC-16 in DESIGN section 8**
  - **Context**: Master already has WC-14 "No turn ends between chain steps" (`src/superclaude/core/WORKER-CONTRACT.md:63`) and WC-15 "Context-safe reading and handoff files" (`WORKER-CONTRACT.md:64`), both from PR #434 and pinned at `tests/skills/test_worker_contract.py:156-164` and `:165-172` (research/07:98). The design's `### WC-14. Coordinator loop` (DESIGN section 8, heading "## 8. WC-14 and the never-as-worker list" near line 659, rule text near 668-670, pins near 677-680) collides with it. A second `"WC-14"` key in the `RULE_PHRASES` dict literal would silently replace the worker entry (research/07:142).
  - **Action**: In section 8 only: change the heading to "## 8. WC-16 and the never-as-worker list"; change `### WC-14. Coordinator loop` to `### WC-16. Coordinator loop`; change the `RULE_PHRASES` pin to key and ident `"WC-16"` with the phrase `"WC-16. Coordinator loop"`, inserted after `"WC-15"` (`test_worker_contract.py:165-172`) and before `"heartbeats"` (`:173`); change every other mention of the coordinator-loop rule in section 8 from WC-14 to WC-16. Add one sentence: "WC-14 and WC-15 on master are worker duties from PR #434 and are not changed." Do not rename references that mean the worker WC-14 (contract :124 "the WC-14 exception", :213, :289).
  - **Output**: DESIGN section 8 using WC-16 for the coordinator loop.
  - **Verification**: Verify: `grep -n 'WC-14' docs/designs/orchestrator-mode.md` lists no section 8 hit except the new "WC-14 and WC-15 on master" sentence; `grep -n 'WC-16. Coordinator loop' docs/designs/orchestrator-mode.md` shows the heading and the pin. Write the before and after `grep -n 'WC-14'` outputs to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/discovery/r4-wc14-hits.md`, each hit classed `coordinator loop (rename)`, `worker rule (keep)` or `historical name (keep)`; the third class is only for a hit that names the SPEC's or the REPORT's earlier WC-14 draft (section 13 row D6 near line 812, section 14 row 1.17 near line 835). If the section 8 heading is not found, log it in `### Phase 5 Findings` and stop.
  - **Completion gate**: Section 8 says WC-16. Once done, mark this item as complete.

- [ ] **5.2 — R4: renumber WC-14 to WC-16 in DESIGN sections 9 and 10 (routing rows R2 and R8, the `.gitignore` comment)**
  - **Context**: research/07:100 lists the coordinator-loop mentions outside section 8: the routing row R2 bullet (near DESIGN line 695), routing row R8 (near 701), and the section 10 `.gitignore` comment `(WC-14)` (near 715).
  - **Action**: Using `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/discovery/r4-wc14-hits.md`, change each `coordinator loop (rename)` hit in sections 9 and 10 to WC-16. The `.gitignore` comment text becomes `# superclaude sweep reports: dated, operator-local, never posted (WC-16). Never tracked.` In the routing row R2 bullet, also align the cadence with master's contract line 110 ("After every wake or timeout, at most once every 5 minutes, the coordinator runs one sweep:", `src/superclaude/core/WORKER-CONTRACT.md:110`): replace "**The coordinator sweeps on every wake.**" with "**The coordinator sweeps on every wake, at most once every 5 minutes.**" and change nothing else in that bullet (R4 removes the same unbounded claim from WC-16 in item 5.4).
  - **Output**: DESIGN sections 9 and 10 using WC-16, and the routing row R2 bullet with the 5-minute bound.
  - **Verification**: Verify: `grep -n 'WC-14' docs/designs/orchestrator-mode.md` shows no hit in sections 9 or 10; the `.gitignore` block in section 10 reads `(WC-16)`; `grep -c 'sweeps on every wake\.\*\*' docs/designs/orchestrator-mode.md` returns 0 and `grep -c 'sweeps on every wake, at most once every 5 minutes\.\*\*' docs/designs/orchestrator-mode.md` returns 1 (the R2 bullet). Update the hit list file with the result.
  - **Completion gate**: Sections 9 and 10 say WC-16 and the R2 bullet carries the 5-minute bound. Once done, mark this item as complete.

- [ ] **5.3 — R4: renumber WC-14 to WC-16 in DESIGN sections 1, 12, 13, 14, 15, 16 and 17 (status line, summary, FR-023, D6, step 1.17, rollback, open items)**
  - **Context**: research/07:100: the FR-023 row (near DESIGN line 777), step 1.17 (near 926) and the rollback table (near 953). BUILD-REQUEST R4 says "everywhere", and `grep -n 'WC-14' docs/designs/orchestrator-mode.md` at `5dc29d23` also hits section 1 (the status line near line 5, "Owner approval of the WC-14 text (section 8)", and the summary near line 13, "the WC-14 "Coordinator loop" contract text"), section 13 (row D6 near line 812, "WC-14 text of SPEC section 10"), section 14 (row 1.17 near line 835, "The REPORT's WC-14 draft") and section 17 (open item 20 near line 988, "GQ-11 (WC-14 approval)", and open item 21 near line 989, "PR #422 overlap with WC-14" and "WC-14 stays a deliverable") (qa/qa-task-research-alignment-report.md I-1).
  - **Action**: Change each remaining `coordinator loop (rename)` hit in sections 1, 12, 15, 16 and 17 to WC-16 (lines near 5, 13, 777, 926, 953, 988 and both mentions near 989). In section 13 row D6 (near 812) and section 14 row 1.17 (near 835), keep `WC-14` because it names the SPEC's and the REPORT's draft, and append " (WC-16 in this design)" right after that `WC-14`; class both hits `historical name (keep)` in the hit list file. Change no other text in those rows, and leave the `Total: 23 open items.` count unchanged.
  - **Output**: DESIGN sections 1, 12, 13, 14, 15, 16 and 17 using WC-16 for the coordinator loop.
  - **Verification**: Verify: every remaining `grep -n 'WC-14'` hit in DESIGN is classed `worker rule (keep)` or `historical name (keep)` in the hit list file, or is the section 8 "WC-14 and WC-15 on master" sentence; `grep -c 'WC-14 (WC-16 in this design)' docs/designs/orchestrator-mode.md` is 2; `grep -n '^Total: 23 open items.' docs/designs/orchestrator-mode.md` returns one hit. If a hit cannot be classed, log it in `### Phase 5 Findings` and stop.
  - **Completion gate**: No coordinator-loop mention of WC-14 remains. Once done, mark this item as complete.

- [ ] **5.4 — R4: align the WC-16 cadence text with master's "The sweep." (section 8)**
  - **Context**: Master's `### Liveness supervision` already defines a coordinator sweep: `WORKER-CONTRACT.md:110` "After every wake or timeout, at most once every 5 minutes, the coordinator runs one sweep:", pinned by `RULE_PHRASES["liveness-sweep-and-states"]` (`test_worker_contract.py:209-219`, phrase at :212). The design text says "On every coordinator wake, the coordinator runs `/sc:sweep` ... It sweeps on every wake", which reads against the 5-minute bound (research/07:134). `_check_repo_setup_gated` (`test_worker_contract.py:813-828`) fails on a contract line with a code span starting `uv` (research/07:156).
  - **Action**: In the DESIGN section 8 WC-16 text block, replace "On every coordinator wake, the coordinator runs `/sc:sweep` and reads its report before it acts. It sweeps on every wake and keeps a periodic sweep scheduled while work remains." with "On every coordinator wake, at most once every 5 minutes (the cadence of "The sweep." under `### Liveness supervision`), the coordinator runs `/sc:sweep` and reads its report before it acts. It keeps a periodic sweep scheduled while work remains." Keep the four pinned phrases verbatim: "WC-16. Coordinator loop", "On every coordinator wake", "it is never posted", "It never stops watching on its own". Add no `` `uv ...` `` code span. Add one sentence to section 8 saying WC-16 does not reword contract lines :110 or :151. The text now differs from SPEC section 10 (lines 404-408) in its heading id and its cadence, and SPEC line 415 and OQ-7 (SPEC line 583) say "Phase 1 sets no cadence", so record both differences in the existing deviation D6 and keep `Total: 9 deviations.`: (1) replace the section 8 sentence "The SPEC section 10 text (lines 404-408), unchanged, with one sentence appended at the end (SP-27, deviation D6):" with "The SPEC section 10 text (lines 404-408) with three changes, all deviation D6: the heading is renumbered WC-16 (R4); the cadence clause of contract line 110 is added and 'It sweeps on every wake' is dropped, because master already bounds the sweep to at most once every 5 minutes (R4); and one sentence is appended at the end (SP-27):"; (2) in the section 13 D6 row's third cell, replace "The same text with one sentence appended:" with "The same text renumbered WC-16, with master's cadence 'at most once every 5 minutes' (contract line 110) in place of 'It sweeps on every wake', and with one sentence appended:", and change nothing else in that row (item 5.3 already marked its `WC-14 (WC-16 in this design)` name).
  - **Output**: DESIGN section 8 WC-16 text with the 5-minute cadence, the section 8 "Final text." sentence and the D6 row recording both R4 differences.
  - **Verification**: Verify: the WC-16 block contains "at most once every 5 minutes" and each of the four pinned phrases (`grep -c` each at least 1); the phrase "It sweeps on every wake" appears only inside the quoted explanations in the "Final text." sentence and the D6 row (`grep -n` hit lines map to those two places, not to the WC-16 block); `grep -c '(lines 404-408), unchanged' docs/designs/orchestrator-mode.md` returns 0; the D6 row contains `renumbered WC-16` and `at most once every 5 minutes`; `grep -n '^Total: 9 deviations.' docs/designs/orchestrator-mode.md` returns one hit; the block has no code span starting `` `uv``. If an old sentence is not found verbatim, log the actual text in `### Phase 5 Findings` and stop.
  - **Completion gate**: The cadence text agrees with master and D6 records the difference from SPEC. Once done, mark this item as complete.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:792-818

````markdown
- [ ] **5.5 — R4: re-anchor the section 8 contract and test-pin lines**
  - **Context**: research/07:142-148 and :169-171 give the new lines on master: the fan-in paragraph and the worked-example heading moved from `WORKER-CONTRACT.md:156/158` to `:273/:275` (WC-16 goes between them); never-as-worker list `:23` unchanged; `NEVER_AS_WORKER` `:245-254` became `test_worker_contract.py:382-391`; the "seven" test `:545` became `:912`; the `"load"` assertion `:865` became `:1322` (def `:1318`); the equality check `:470` became `:837`; `_check_never_as_worker` `:398` became `:765`; the removal test is `:1081-1082`. The design lists four pins; a fifth is required: `RULE_PHRASES["never-as-worker"]` phrase at `test_worker_contract.py:89` must become `` `/sc:spawn`, `/sc:sweep` and `/sc:swarm-wizard`, `` (research/07:144).
  - **Action**: In DESIGN section 8 (placement near line 663, pins near 677-680, never-as-worker near 684-686), replace each old line number with its new one. Add the fifth pin (the :89 phrase edit) to the pin list, so it names five pin edits. Keep the rename of `test_never_as_worker_list_names_all_seven_commands` to `test_never_as_worker_list_names_every_listed_command`.
  - **Output**: DESIGN section 8 with master anchors and five pins.
  - **Verification**: Verify: `grep -n '156\|158\|245-254\|:545\|:865\|:470\|:398' docs/designs/orchestrator-mode.md` shows no section 8 hit that still points at an old contract or test line; the pin list has five entries; each new line number was checked by reading that line of `src/superclaude/core/WORKER-CONTRACT.md` or `tests/skills/test_worker_contract.py` (record the line text read in `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/discovery/r4-reanchor.md`).
  - **Completion gate**: Section 8 anchors match master. Once done, mark this item as complete.

- [ ] **5.6 — R4: re-anchor the `main.py` insertion point (DESIGN lines near 28, 915, 951)**
  - **Context**: PR #447 added the `issue-watch` pair to `src/superclaude/cli/main.py`: import at `:563`, `main.add_command(issue_watch_group, name="issue-watch")` at `:565`; `if __name__ == "__main__":` moved to `:568`; the file is 569 lines (research/08:15, :117). DESIGN still says "after line 561", the block 519-561, last pair reflect (559, 561) and `if __name__` 564.
  - **Action**: At DESIGN near line 28 change to block 519-565, last pair `issue-watch` (563, 565), `if __name__` at 568. At step 1.7 (near 915) and the rollback row (near 951) change "after line 561" to "after line 565".
  - **Output**: DESIGN with the 565 anchor.
  - **Verification**: Verify: `grep -n 'after line 561\|519-561' docs/designs/orchestrator-mode.md` returns nothing; `grep -c 'after line 565'` is at least 2; read `src/superclaude/cli/main.py` lines 559-569 and record line 565's text in `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/discovery/r4-reanchor.md`.
  - **Completion gate**: The insertion point is 565 everywhere. Once done, mark this item as complete.

- [ ] **5.7 — R4: make step 1.16a record-only (section 8 Gate and section 15)**
  - **Context**: DESIGN section 8 Gate (near line 661) and step 1.16a in sections 15.1/15.2 gate on the PR #422 overlap. #422 (`2327fbd3`) is merged on master; its 15 P2 conversions are in the contract (`WORKER-CONTRACT.md:304`) and the tests (`test_worker_contract.py:416-432`) (research/07:162). research/09 Gap 3 "1.16a" (research/09:113-115) defines the record-only step and its four points; item 7.19 writes exactly those four points to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/pr422-409-check.md`, so the DESIGN text must name the same four.
  - **Action**: Reword the section 8 Gate and the step 1.16a entries so step 1.16a is a record-only step that writes `artifacts/pr422-409-check.md` with research/09's four points: (1) the `gh pr view 422 --repo IronbellyOrg/IronClaude` state line (MERGED, merge commit `2327fbd3`); (2) `git merge-base --is-ancestor 2327fbd3 HEAD` succeeding; (3) `git merge-base --is-ancestor 495eb96d origin/master` failing, so the `495eb96d` pin stands and no layout diff is needed; (4) a note that every `WORKER-CONTRACT.md` and `test_worker_contract.py` line cited by steps 1.17 to 1.19 is re-read at HEAD before it is edited. Remove the "wait or move 1.17 to 1.19 to a follow-up PR" and rebase branches. Its gate on step 1.17 stays and is satisfied as soon as the record is written (research/09:115).
  - **Output**: DESIGN sections 8 and 15 with step 1.16a record-only.
  - **Verification**: Verify: `grep -n '1.16a' docs/designs/orchestrator-mode.md` shows each hit as record-only (no "wait for", "follow-up PR", "rebase" or "if #422 is open" wording in those lines); the step 1.16a entry names `2327fbd3`, `495eb96d` and the re-read note, matching the four points item 7.19 records. If 1.16a is absent from section 15, log it in `### Phase 5 Findings` and stop.
  - **Completion gate**: Step 1.16a is record-only. Once done, mark this item as complete.

- [ ] **5.8 — R4: record the new master test constraints in section 8**
  - **Context**: research/07:152-158. `_check_p2_set` (`test_worker_contract.py:1556`) asserts `UNATTENDED_EXPECT` has exactly 31 entries, so `sweep` is never added; `_check_no_unattended_sections` (`:831-839`) globs every `src/superclaude/commands/*.md`, so `sweep.md` has no `## Unattended mode`; the write-verb audit (`AUDIT_ROOTS` `:1940-1944`, categories `:1953-1955`) needs a `WRITE_VERB_CLASSIFICATION` row for any write-verb text in `sweep.md` or `sc-sweep-protocol/`, with `never-worker` available once `/sc:sweep` is on the list, and a `read-only` `gh api` entry must not look like a post (`_is_gh_api_post`, `:1966`); `RULE_PHRASES["liveness-sweep-and-states"]` (`:209-219`) and `["liveness-ladder-and-restart"]` (`:228-237`) must not be reworded; `_check_rule` (`:755-762`) needs the ident on the heading line.
  - **Action**: Add a short list "Constraints from master `5dc29d23`" to DESIGN section 8 after the pins, one bullet per constraint above. Add to the section 7.6 `sweep.md` spec (near lines 644-648): "`sweep.md` has no `## Unattended mode` section." Do not add a new deviation; the count stays `Total: 9 deviations.`
  - **Output**: DESIGN sections 7.6 and 8 with the constraints.
  - **Verification**: Verify: section 8 names `UNATTENDED_EXPECT` with 31, `WRITE_VERB_CLASSIFICATION`, and the two liveness pins; section 7.6 contains `no \`## Unattended mode\``; `grep -n '^Total: 9 deviations.'` still returns one hit.
  - **Completion gate**: The constraints are recorded. Once done, mark this item as complete.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:976-999

````markdown
## Phase 6: Design fix R5 (`--agent-wait`), OWNER DECISION OQ-1, and its gate

R5 is a human gate. Nothing in this phase resolves it on the owner's behalf. No recommended default is treated as approved unless the decision file says so. Every item after Phase 6 is blocked until item 6.2 is ticked. Once the owner's decision is recorded and applied (items 6.1 to 6.4), the R5 DESIGN edit is closed by its own QA gate (items 6.5 to 6.22, folder `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/r5/`), before any Phase 7 item runs.

- [ ] **6.1 — Record the OQ-1 decision request (L5, PENDING)**
  - **Context**: Master's coordinator sweep at `src/superclaude/core/WORKER-CONTRACT.md:110` runs "one prompt-wait listing (`worktree ps --agent-wait`)" (research/07:117). The INV-005 owner sign-off, condition 1 (SPEC section 13; NFR-014 at `merged-requirements.md:143`), allows `worktree ps` only without `--agent-wait`: "`worktree ps` never carries `--agent-wait`". DESIGN holds `FORBIDDEN_TOKENS = frozenset({"--include-remote", "--agent-wait"})` (DESIGN 7.3, near line 532) and forbids `--agent-wait` in step 1.0a (DESIGN 15.1, near line 873). The two texts disagree on whether the coordinator's sweep may use `--agent-wait`.
  - **Action**: Write `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/OQ-1-agent-wait-decision.md` containing: a frontmatter-style block `needs_human_decision: true` and `status: PENDING`; the question "May the coordinator's sweep run `worktree ps --agent-wait`, which INV-005 condition 1 forbids?"; the two options verbatim: "(a) extend the sign-off to `--agent-wait` after a lock check;" and "(b) keep "never" and fix the master contract text in a later PR."; what each option changes (a: a lock-check record, DESIGN sections 7.3, 11 and 15.1, the NFR-014 pin, and a design revision; b: one DESIGN section 8 sentence plus a follow-up PR against master's contract line 110); a recommendation line "Builder recommendation: (b), because it keeps the signed-off allowlist unchanged. This recommendation does NOT authorize adoption."; and an empty block with the lines `OPERATOR DECISION:`, `Chosen:`, `Decided by:`, `Decision source:`.
  - **Output**: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/OQ-1-agent-wait-decision.md`.
  - **Verification**: Verify: the file has `status: PENDING`, both options verbatim, the "does NOT authorize adoption" label and the four empty decision lines. Add OQ-1 to `### Open Questions` if it is not already there.
  - **Completion gate**: The decision request is recorded. Once done, mark this item as complete.

- [ ] **6.2 — HALT until the owner decides OQ-1 (L5)**
  - **Context**: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/OQ-1-agent-wait-decision.md` from item 6.1. The owner's own words in the session are the decision (APPROVED G1, `.dev/orca-command-refactor/decisions/APPROVED.md:71`); no separate grant file is created.
  - **Action**: Read the decision file. Branch 1: if `status` is PENDING or `Chosen:` is empty, apply the HALT rule with `blocker_reason: "OQ-1 (R5, --agent-wait) awaits the owner's decision in phase-outputs/plans/OQ-1-agent-wait-decision.md"` and STOP. Branch 2: if `Chosen:` is (a) or (b) with `Decided by:` and `Decision source:` filled (the source quotes the owner's words), set `status: RESOLVED` in the file, append the decision to `### Execution Log`, set the task frontmatter `status` back to "🟠 Doing" and clear `blocker_reason`.
  - **Output**: The decision file with `status: RESOLVED`, or a Blocked task.
  - **Verification**: Verify: on Branch 2 the decision file names the option, the decider and the source. On Branch 1, stop before marking this item complete until the blocker is resolved.
  - **Completion gate**: OQ-1 is RESOLVED. Once done, mark this item as complete.

- [ ] **6.3 — Apply the OQ-1 decision to DESIGN (L5, both branches)**
  - **Context**: The RESOLVED decision file from item 6.2; DESIGN section 8 (WC-16 text from item 5.4); the `### Fix cycle 3` table.
  - **Action**: Branch (b): in the DESIGN section 8 WC-16 text, add: "The `/sc:sweep` probes never include `--agent-wait` (INV-005 condition 1). The prompt-wait listing named in the contract's "The sweep." paragraph stays outside `/sc:sweep` until a later PR changes that contract text on master." Append the row `| R5 | Master's sweep runs \`worktree ps --agent-wait\`; INV-005 condition 1 forbids it | Owner chose (b): \`/sc:sweep\` keeps "never"; the master contract text is fixed in a later PR (8) |` to `### Fix cycle 3`, and add the follow-up PR to `### Open Questions` under OQ-1. Do not edit `WORKER-CONTRACT.md:110` in this task. Branch (a): do not edit DESIGN; apply the HALT rule with `blocker_reason: "R5 option (a) chosen: the allowlist change needs its own design revision (lock-check record; sections 7.3, 11, 15.1); re-run /task-builder"` and STOP.
  - **Output**: DESIGN section 8 and section 18 updated (branch b), or a Blocked task (branch a).
  - **Verification**: Verify on branch (b): `grep -n 'probes never include' docs/designs/orchestrator-mode.md` returns one hit in section 8 and that line contains `--agent-wait`; `FORBIDDEN_TOKENS` in 7.3 still lists `--agent-wait`; the `### Fix cycle 3` table ends with the R5 row; em-dash count 0. On branch (a), stop before marking this item complete until the blocker is resolved.
  - **Completion gate**: Branch (b) is applied. Once done, mark this item as complete.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1430-1435

````markdown
- [ ] **8.3 — Step 1.2: create `src/superclaude/cli/sweep/models.py`, with `ClassifiedRow` and the ten #409 dimensions (L2)**
  - **Context**: DESIGN section 7.2 (line 447), as revised by Phases 2 to 6: frozen dataclasses `SweepContext`, `SweepInput`, `OrcaObservation` (with `dispatch: str`, `run: str`, `session_join: str | None`, and the three R3-B1 fields `dispatch_started: datetime | None`, `dispatch_ended: datetime | None` and `dispatch_status: str | None`, parsed from the `worker-show` JSON paths `dispatch.dispatchedAt`, `dispatch.completedAt` and `dispatch.status`; all three are None for a row with no `worker-show` result, research/04:87), `ContractRecord`, `TranscriptTail` (with `first_record_ts: datetime | None` after `last_record_ts`, R3-B1, research/04:88), `TabMapEntry`, `SessionRow` (DESIGN line 459), `StatusParse`, `PackageRecord`, `WorktreeState`, `Classification`, `SafeToClose`, `SourceCoverage`, `SweepResult` (line 466), and the constants `JSON_SCHEMA_VERSION = 1`, `CLASSES` (8 names), `PACKAGE_STATES`, `SAFE_VALUES`. Live field names and the time format come from `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/discovery/1.0a-facts.md` (item 7.17); a fact still UNVERIFIED there keeps the DESIGN "behaviour until closed". research/09 Gap 2 gives the ten dimensions (REPORT:1245) and their values. Builder decisions (OQ-11 and OQ-14, not design facts): (1) `ClassifiedRow` is `row: SessionRow`, `classification: Classification`, `policy: str | None` (the `classify.policy_of` value, `"frozen"` or None), `safe: SafeToClose`, from the DESIGN line 466 words "row plus `Classification`, policy and `SafeToClose`" (research/09 Gap 2 "ClassifiedRow"); (2) `SessionRow` carries nine dimension fields, `lifecycle`, `phase`, `health`, `approval`, `freshness`, `result`, `admission`, `evidence_packet` (each `str = "unknown"`), `freshness_age_s: int | None = None` and `tests_review: str | None = None`; dimension 9 `policy` is not a `SessionRow` field and is printed from `ClassifiedRow.policy` (item 8.12), so the row holds no second copy of the freeze result.
  - **Action**: Create `src/superclaude/cli/sweep/models.py` with `from __future__ import annotations`, `dataclasses.dataclass(frozen=True)` classes and tuple-typed collections exactly as DESIGN section 7.2 lists them, plus `ClassifiedRow` and the dimension fields of decisions (1) and (2). Import only from the standard library (`dataclasses`, `datetime`, `pathlib`, `typing`). Add a one-line comment on `ClassifiedRow` and on the dimension block naming OQ-14 and OQ-11. The dimension fields are never JSON keys (DESIGN line 590 pins the v1 row key set).
  - **Output**: `src/superclaude/cli/sweep/models.py`.
  - **Verification**: Verify: every class and constant name in DESIGN section 7.2 appears once (`grep -c` per name); `grep -c 'dispatch_started: datetime | None'`, `grep -c 'dispatch_ended: datetime | None'`, `grep -c 'dispatch_status: str | None'` and `grep -c 'first_record_ts: datetime | None'` on `src/superclaude/cli/sweep/models.py` each return 1; `uv run python -c "import superclaude.cli.sweep.models"` exits 0; `uv run ruff check src/superclaude/cli/sweep/models.py` exits 0. If a DESIGN field cannot be typed from DESIGN or the 1.0a facts, log it in `### Phase 8 Findings` and stop before marking this item complete until it is settled.
  - **Completion gate**: The module imports and lints clean and holds every DESIGN 7.2 name. Once done, mark this item as complete.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1444-1449

````markdown
- [ ] **8.5 — Step 1.4a, code part: the git seam in `src/superclaude/cli/sweep/probes.py` (L2)**
  - **Context**: DESIGN step 1.4a (line 911) and sections 2.1 (line 39, GQ-103(1) lock-free git) and 7.3 (line 514): `ALLOWED_GIT = (("status", "--porcelain=v1", "-z", "--branch", "--untracked-files=all"),)`; `check_git_args(args)` raises `ValueError` for any args tuple not equal to an `ALLOWED_GIT` entry before any subprocess; `_git(cwd, *args, timeout)` builds `["git", "--no-optional-locks", "-C", str(cwd), *args]` and runs it with an env copy holding `GIT_OPTIONAL_LOCKS=0`; `GitCallFailed` is its error. research/05 summary point 3: the subprocess guard only catches calls made as `subprocess.run`, so probes calls `subprocess.run` through the module (`import subprocess`), never `from subprocess import run`. Output cap `OUTPUT_LIMIT` (8 MiB, DESIGN 7.3).
  - **Action**: Create `src/superclaude/cli/sweep/probes.py` holding only, for now, `import subprocess`, the `OUTPUT_LIMIT` constant, `ALLOWED_GIT`, `GitCallFailed`, `check_git_args` and `_git` as DESIGN states them (`capture_output=True`, `timeout=timeout`, `check=False`; non-zero exit, timeout or output over `OUTPUT_LIMIT` raise `GitCallFailed` with a reason). Item 8.10 adds the rest of the module.
  - **Output**: `src/superclaude/cli/sweep/probes.py` (git part).
  - **Verification**: Verify: `grep -n 'from subprocess' src/superclaude/cli/sweep/probes.py` prints nothing; `grep -n 'no-optional-locks\|GIT_OPTIONAL_LOCKS' src/superclaude/cli/sweep/probes.py` prints both; `uv run ruff check` on the file exits 0.
  - **Completion gate**: The git seam exists as DESIGN states. Once done, mark this item as complete.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1465-1470

````markdown
- [ ] **8.8 — Step 1.8 base part: `tests/sweep/conftest.py` with the subprocess guard and the seam fakes (L2)**
  - **Context**: DESIGN section 11 (lines 728-733): `patch_orca` and `patch_git` replace `probes._orca` and `probes._git` with fakes that record every argv and return fixture data, as `tests/cli/reflect/conftest.py` does; an autouse fixture patches `subprocess.run`, `subprocess.Popen` and `os.system` to raise `AssertionError`, stepping aside only for the one test carrying the `integration` marker (registered at `pyproject.toml:119`, `--strict-markers`); a fixed `now`; a `tmp_path` layout with `HOME` and `XDG_STATE_HOME` inside it. research/05 section 2 and summary point 3: the superclaude plugin adds `integration` to every test whose absolute path contains `/integration/` (`src/superclaude/pytest_plugin.py:216-222`), so the guard must read only the test function's own decorator marks: `any(m.name == "integration" for m in getattr(request.function, "pytestmark", []))`, never `request.node.get_closest_marker`. This item is placed before item 8.9 because the step 1.4a test needs these fakes (research/01 summary gap). `probes._orca` does not exist until item 8.10, so `patch_orca` uses `monkeypatch.setattr(probes, "_orca", fake, raising=False)`; item 10.1 adds the fixture files and the rest of the layout.
  - **Action**: Read `tests/cli/reflect/conftest.py` in chunks of at most 150 lines for the fake-recording shape. Create `tests/sweep/conftest.py` with: the autouse guard fixture `no_subprocess(request, monkeypatch)` using the own-marks check above; `patch_git` (records `(cwd, args, timeout)` and the env the real `_git` would build, returns canned porcelain bytes per worktree); `patch_orca` (records argv, returns canned `OrcaResult`-shaped data once item 8.10 lands); `fixed_now` (a timezone-aware UTC `datetime`); `sweep_home` (sets `HOME` and `XDG_STATE_HOME` under `tmp_path` with `monkeypatch.setenv`).
  - **Output**: `tests/sweep/conftest.py`.
  - **Verification**: Verify: `grep -n 'get_closest_marker' tests/sweep/conftest.py` prints nothing and `grep -n 'pytestmark' tests/sweep/conftest.py` prints the guard line; `uv run ruff check tests/sweep/conftest.py` exits 0.
  - **Completion gate**: The conftest exists with the guard and the two fakes. Once done, mark this item as complete.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1623-1628

````markdown
- [ ] **9.1 — Step 1.6: create `src/superclaude/cli/sweep/commands.py` (L2)**
  - **Context**: Gates: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/impl-core/gate-decision.md` PASS; OQ-2 (GQ-10, report location, `--output` default) and OQ-5 (GQ-61, `--window` default) RESOLVED. DESIGN section 7.1 commands signatures (lines 433-445): `sweep_group: click.Group` named `sweep`; `run(run_ids, window, root, output)` for `sweep run`; `_parse_window` (FR-003, `click.UsageError`, exit 2); `_find_root` (FR-004 walk, plain stat only); `_check_output` (FR-004 containment); `_check_run_ids` (regex from step 1.0a, `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/discovery/1.0a-facts.md`, deduplicated); `_publish(text, output_dir, now)`. Exit mapping (line 445): `click.UsageError` and `BindingError` exit 2 with the message; `ValueError` from an allowlist check, any other exception and every `_publish` failure exit 1 with a `[sweep <stage>]` stderr prefix; only `commands.run` calls `sys.exit`. DESIGN section 3.2 (lines 99-130), the seven `_publish` steps: stem `now.strftime("%Y%m%d-%H%M%S") + "-sweep"`; `os.makedirs(output_dir, exist_ok=True)` then re-resolve inside `<root>/.dev/sweeps/` (else `[sweep publish] output dir escaped <root>/.dev/sweeps/`); `os.open(output_dir / f".{stem}.{os.getpid()}.tmp", O_WRONLY | O_CREAT | O_EXCL, 0o666)`; write every byte, `os.fsync`, `os.close`; `os.link` to `stem.md`, then `stem-2.md` to `stem-99.md`, `FileExistsError` moving on, the first success being the commit point; none left gives `[sweep publish] report name space exhausted: <dir>`; then `os.unlink(tmp)`, failing with `[sweep publish] could not remove temp file <path>` and exit 1. The error table (lines 121-129) and the section 3.4 exit-1 rule (line 153) apply. DESIGN step 1.6 (line 914): no `run-list` fallback; `--output` default `<root>/.dev/sweeps/`. `_publish` runs only after every exit-2 check, `collect`, `classify_all` and `render` succeed (line 103). The six `[sweep publish]` messages in DESIGN section 3.2 (lines 106-128) are: `[sweep publish] output dir escaped <root>/.dev/sweeps/` (step 2), `[sweep publish] report name space exhausted: <dir>` (step 6), `[sweep publish] <error>` (`makedirs` fails), `[sweep publish] temp file exists: <path>` (`O_EXCL` fails), `[sweep publish] cannot link report: <error>` (`os.link` fails with anything but `FileExistsError`) and `[sweep publish] could not remove temp file <path>` (unlink after the commit point). Link-and-fsync precedents (research/02 section on atomic writes): the `os.link` plus `FileExistsError` handling at `src/superclaude/cli/sprint/recovery.py:424-434` (link at :433) and the `os.fsync` step at `src/superclaude/cli/swarm/atomic.py:28-31`; neither is a reusable helper (both use other names or `os.replace`), so `_publish` is written fresh.
  - **Action**: Create `src/superclaude/cli/sweep/commands.py` with the Click group and the `run` subcommand (options `--run` repeatable, `--window`, `--root`, `--output`, defaults from the OQ-2 and OQ-5 records), the five helpers and `_publish` exactly as above, printing one success JSON object (from `report.to_json`) on stdout after `_publish` returns. `_publish` is the only function that writes. No retry, no lock, no `os.rename`, no `os.replace`.
  - **Output**: `src/superclaude/cli/sweep/commands.py`.
  - **Verification**: Verify: `grep -nE 'os\.(rename|replace)|run-list' src/superclaude/cli/sweep/commands.py` prints nothing; `grep -c 'sys.exit' src/superclaude/cli/sweep/commands.py` hits only inside `run`; each fixed part of the six `[sweep publish]` messages listed in Context is found with `grep -F` in `src/superclaude/cli/sweep/commands.py`: `output dir escaped`, `report name space exhausted:`, `temp file exists:`, `cannot link report:` and `could not remove temp file` (one hit each at least), and the `makedirs` message `[sweep publish] <error>` is checked by reading the `makedirs` error branch and recording its line in `### Phase 9 Findings`; `uv run ruff check src/superclaude/cli/sweep/commands.py` exits 0.
  - **Completion gate**: commands.py matches DESIGN 3.2 and 7.1. Once done, mark this item as complete.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1776-1781

````markdown
- [ ] **10.1 — Step 1.8 rest: extend `tests/sweep/conftest.py` and add the fixture files (L2)**
  - **Context**: DESIGN section 11 lines 728-733: the `tmp_path` layout holds packages, contracts, transcripts and a ccsession `orca-tabs/` folder; fixtures copied from captured Orca output keep their source name, hand-made ones carry `synthetic` in the file name. Captured fixtures already exist from item 7.18 (`tests/sweep/fixtures/captured-*.json` plus `SOURCES.md`). Base fixtures from item 8.8: the guard, `patch_orca`, `patch_git`, `fixed_now`, `sweep_home`.
  - **Action**: Add to `tests/sweep/conftest.py` a `sweep_root` fixture that builds, under `tmp_path`, a root with `.dev/tasks/to-do/<pkg>/` packages (with `progress.md` ledgers and worker contracts), transcripts under `HOME`, and an `orca-tabs/` map under `XDG_STATE_HOME`, with small builder helpers the tests call. Hand-made fixture files form a closed set: read `tests/sweep/fixtures/SOURCES.md`, and for each of the eight `ALLOWED_ORCA` templates that has no `captured-` file there, write exactly one file with the name from this list: `synthetic-run-current.txt` (template 1, plain output), `synthetic-worker-list.json` (2), `synthetic-worker-show.json` (3), `synthetic-task-list-ready.json` (4), `synthetic-task-list.json` (5), `synthetic-worktree-ps.json` (6), `synthetic-worktree-list.json` (7) and `synthetic-worktree-current.json` (8). Shape each from the DESIGN section 7.2 field names and `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/discovery/1.0a-facts.md`, and add one `SOURCES.md` row per file naming the template and "hand-made, synthetic". Every other variant a test needs (a malformed body, the quoted-marker negative, an empty `run-current` body, byte-boundary inputs, the `orca-tabs/` entries) is built in memory or under `tmp_path` by the builder helpers, never as a file under `tests/sweep/fixtures/`. Do not edit the captured files.
  - **Output**: `tests/sweep/conftest.py` (extended); the `synthetic-*` files from the list above for exactly the templates `SOURCES.md` shows as not captured (none when all eight were captured); `tests/sweep/fixtures/SOURCES.md` with one row per new file.
  - **Verification**: Verify: `ls tests/sweep/fixtures/` shows only `captured-*` files, `SOURCES.md` and names from the eight-name list above; each `synthetic-*` file's template has no `captured-` file; each `synthetic-*` file has a `SOURCES.md` row; every `synthetic-*.json` file parses with `uv run python -c "import json,sys; [json.load(open(p)) for p in sys.argv[1:]]" tests/sweep/fixtures/synthetic-*.json` (skip when there is none); `uv run pytest tests/sweep -v` still passes.
  - **Completion gate**: The layout fixture exists and the existing tests pass. Once done, mark this item as complete.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1950-1955

````markdown
- [ ] **11.1 — Step 1.14: create `src/superclaude/commands/sweep.md` (L2)**
  - **Context**: DESIGN section 7.6 "**Command**" bullets (anchor the quoted heading `### 7.6 Command and skill surface`; lines 644-648 on the unrevised design). Pattern files: `src/superclaude/commands/issue.md` (title `# /sc:issue: ...` at :12, `## Triggers` :23, `## Usage` :27, `## Options` :34) and `src/superclaude/commands/graph.md` (`allowed-tools: Skill, ...` at :9, `## Activation` at :41-46 with "**MANDATORY**: Before executing any protocol steps, invoke:" and "> Skill sc:graph-protocol"). Skill frontmatter name form: `src/superclaude/skills/sc-graph-protocol/SKILL.md:2` (`name: sc:graph-protocol`). Option defaults: the OQ-2 (`--output`) and OQ-5 (`--window`) records in `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/` and `src/superclaude/cli/sweep/commands.py` (item 9.1).
  - **Action**: Create `src/superclaude/commands/sweep.md` with frontmatter `name: sweep`, a one-line description (no stop, retry, release, merge or removal wording), `allowed-tools: Skill` and `argument-hint: "[--run <id>]... [--window <N>h|<N>d] [--root <dir>] [--output <dir>]"`. Body: `# /sc:sweep: ...` title; `## Triggers` (explicit only: the coordinator on every wake, or the person); `## Usage`; `## Options` (one row per option with the defaults from `commands.py`); `## Activation` in the `graph.md` form invoking `Skill sc:sweep-protocol`, naming `~/.claude/skills/sc-sweep-protocol/SKILL.md` as the installed skill and the project `.claude/skills/sc-sweep-protocol/SKILL.md` copy as the dual surface (skills read `~/.claude/skills/` first). No `## Unattended mode` heading, no `--unattended` flag. One line states `/sc:sweep` is coordinator or person only and is on the never-as-worker list (`~/.claude/WORKER-CONTRACT.md`).
  - **Output**: `src/superclaude/commands/sweep.md`.
  - **Verification**: Verify: `grep -c 'src/superclaude' src/superclaude/commands/sweep.md` prints 0; `grep -n '^## Unattended mode\|--unattended' src/superclaude/commands/sweep.md` prints nothing; `grep -nF '~/.claude/skills/sc-sweep-protocol/SKILL.md' src/superclaude/commands/sweep.md` prints a line in the Activation block (the installed surface), and `grep -nP '(?<!~/)\.claude/skills/sc-sweep-protocol/SKILL\.md' src/superclaude/commands/sweep.md` prints a line in the Activation block (the project copy; the lookbehind rejects the installed path, so the installed path alone cannot satisfy this check). Record the output in `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/step-1.14-checks.md`.
  - **Completion gate**: The file exists and every check holds. Once done, mark this item as complete.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:2873-2877

````markdown
- **OQ-11 (`policy` dimension against `policy_of`), builder decision.** The #409 dimension 9 (`policy`) is rendered in the report only, from `ClassifiedRow.policy` (`frozen` or unknown); the dimension fields are never JSON keys. The executor or a QA gate may reopen it with evidence.
- **OQ-12 (POST diff-file substitution), deliberate placeholder fill.** The task-builder POST runner prompt's `--diff {BASE}..HEAD` is filled with `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/post/phase1.diff` (built by item 14.47), and `--task-log` is not added to the Skill args because the runner prompt is copied verbatim. Reason: this project commits only when the user asks, so `{BASE}..HEAD` would audit nothing. The path follows BUILD-REQUEST, not research/09's `artifacts/phase1-working-tree.diff`; it sits beside, not inside, the output root `reflect/post/audit/`, so reflect's `output_input_overlap` check does not fire. DESIGN and the three review files were untracked before the task, so the diff leaves out every path listed in `artifacts/baseline-untracked.txt`, and the DESIGN hunk compares DESIGN with the item 1.3 snapshot `artifacts/design-base.md`, not with a commit.
- **OQ-13 (UNVERIFIED until step 1.0a).** The live Orca field names and time format; where `completedAt` is written; the session-to-Dispatch join key; the `page.nextCursor` shape. No code item may treat these as facts before `artifacts/readonly-probe.md` records them.
- **OQ-14 (builder decisions that fill research/01 gaps).** The `ClassifiedRow` shape (item 8.3) and adding the transcript parser file to the FR-010 trace (research/09 Gap 4). A QA gate may reopen either with evidence.
- **OQ-15 (R4 cadence against SPEC section 10), builder decision.** SPEC line 415 and SPEC OQ-7 (line 583) say Phase 1 sets no cadence; master's contract line 110 already bounds the sweep to at most once every 5 minutes. Items 5.2 and 5.4 align WC-16 and routing row R2 with master and record the difference from the SPEC text, with the WC-16 renumbering, in the existing deviation D6, so the total stays `Total: 9 deviations.`. The Phase 14 fidelity gate treats this as a recorded deviation, not as an unrecorded SPEC change.
````

## Coverage slice

Owned rows (8): routing rows R1 to R8.

| ID | Source | Defining line | Match | All matched items | Items in phases 2 to 6 and 8 to 13 | Matrix note |
|---|---|---|---|---|---|---|
| R1 | parsed | docs/designs/orchestrator-mode.md:694 | exact | 13.2, 13.12, 14.20, 14.23 | 13.2, 13.12 | - |
| R2 | parsed | docs/designs/orchestrator-mode.md:695 | exact | 5.2, 5.11, 5.14, 5.19, 13.1, 13.4 | 5.2, 5.11, 5.14, 5.19, 13.1, 13.4 | - |
| R3 | parsed | docs/designs/orchestrator-mode.md:696 | exact | 10.2, 13.4 | 10.2, 13.4 | - |
| R4 | parsed | docs/designs/orchestrator-mode.md:697 | exact | 5.4, 13.3 | 5.4, 13.3 | - |
| R5 | parsed | docs/designs/orchestrator-mode.md:698 | exact | 6.3, 6.4, 7.13, 11.2, 11.6, 11.7, 11.8, 11.9, 11.10, 11.11, 11.12, 11.15, 11.16, 11.19, 11.20 | 6.3, 6.4, 11.2, 11.6, 11.7, 11.8, 11.9, 11.10, 11.11, 11.12, 11.15, 11.16, 11.19, 11.20 | - |
| R6 | parsed | docs/designs/orchestrator-mode.md:699 | exact | 13.5 | 13.5 | - |
| R7 | parsed | docs/designs/orchestrator-mode.md:700 | exact | 12.4, 12.6, 12.7, 12.8, 12.9, 12.10, 12.11, 12.12, 12.15, 12.16, 12.19, 12.20 | 12.4, 12.6, 12.7, 12.8, 12.9, 12.10, 12.11, 12.12, 12.15, 12.16, 12.19, 12.20 | - |
| R8 | parsed | docs/designs/orchestrator-mode.md:701 | exact | 5.2, 5.9, 5.11, 5.14, 5.19, 13.6, 13.12, 14.20, 14.23 | 5.2, 5.9, 5.11, 5.14, 5.19, 13.6, 13.12 | - |

Design-fix-touched rows (16): rows whose matched items include a phase 2 to 6 item. Judge only the design-fix consistency for these.

| ID | Source | Defining line | Match | All matched items | Items in phases 2 to 6 | Matrix note |
|---|---|---|---|---|---|---|
| FR-010 | parsed | docs/designs/orchestrator-mode.md:764 | exact | 2.5, 2.16, 3.3, 3.5, 3.7, 3.14, 4.1, 4.3, 4.4, 4.5, 4.7, 4.8, 4.9, 4.10, 4.11, 4.12, 4.13, 4.14, 4.15, 4.18, 4.19, 4.22, 4.23, 10.2, 14.11, 14.35 | 2.5, 2.16, 3.3, 3.5, 3.7, 3.14, 4.1, 4.3, 4.4, 4.5, 4.7, 4.8, 4.9, 4.10, 4.11, 4.12, 4.13, 4.14, 4.15, 4.18, 4.19, 4.22, 4.23 | - |
| FR-023 | parsed | docs/designs/orchestrator-mode.md:777 | exact | 5.3, 5.14, 5.19 | 5.3, 5.14, 5.19 | - |
| NFR-003 | parsed | docs/designs/orchestrator-mode.md:783 | exact | 2.16 | 2.16 | - |
| NFR-014 | parsed | docs/designs/orchestrator-mode.md:794 | exact | 2.16, 6.1, 6.5, 6.6, 6.7, 6.8, 6.9, 6.10, 6.11, 6.12, 6.13, 6.16, 6.17, 6.20, 6.21, 14.35 | 2.16, 6.1, 6.5, 6.6, 6.7, 6.8, 6.9, 6.10, 6.11, 6.12, 6.13, 6.16, 6.17, 6.20, 6.21 | - |
| GQ-103 | parsed | docs/designs/orchestrator-mode.md:39 | exact | 2.3, 2.7, 2.9, 7.7, 8.5 | 2.3, 2.7, 2.9 | - |
| D6 | parsed | docs/designs/orchestrator-mode.md:812 | exact | 5.1, 5.3, 5.4, 5.11 | 5.1, 5.3, 5.4, 5.11 | - |
| D9 | parsed | docs/designs/orchestrator-mode.md:815 | exact | 2.16, 3.3, 3.5, 3.7, 3.11, 3.13, 7.11, 7.12, 7.13, 7.21, 8.4, 8.15, 10.2, 10.5 | 2.16, 3.3, 3.5, 3.7, 3.11, 3.13 | - |
| SP-27 | parsed | docs/designs/orchestrator-mode.md:851 | exact | 5.4 | 5.4 | - |
| SP-29 | parsed | docs/designs/orchestrator-mode.md:853 | exact | 2.16, 3.3, 3.5, 3.7, 3.11, 3.14 | 2.16, 3.3, 3.5, 3.7, 3.11, 3.14 | - |
| step-1.0a | parsed | docs/designs/orchestrator-mode.md:829 | exact | 2.4, 2.10, 3.8, 4.9, 6.1, 6.6, 7.14, 7.15, 7.16, 7.17, 7.18, 8.10, 9.1, 10.3, 14.20, 14.34 | 2.4, 2.10, 3.8, 4.9, 6.1, 6.6 | - |
| step-1.7 | parsed | docs/designs/orchestrator-mode.md:915 | exact | 5.6, 5.19, 9.2, 9.5, 9.6, 9.7, 9.8, 9.9, 9.10, 9.11, 9.12, 9.15, 9.16, 9.19, 9.20 | 5.6, 5.19 | - |
| step-1.16a | parsed | docs/designs/orchestrator-mode.md:925 | exact | 5.7, 5.11, 5.14, 5.16, 7.19 | 5.7, 5.11, 5.14, 5.16 | - |
| step-1.17 | parsed | docs/designs/orchestrator-mode.md:835 | exact | 5.3, 5.7, 5.17, 5.19, 5.21, 6.9, 7.3, 7.19, 7.26, 12.1, 12.6, 12.7, 12.8, 12.9, 12.10, 12.11, 12.12, 12.15, 12.16, 12.19, 12.20 | 5.3, 5.7, 5.17, 5.19, 5.21, 6.9 | - |
| step-1.19 | parsed | docs/designs/orchestrator-mode.md:928 | exact | 5.7, 5.14, 5.17, 5.21, 7.3, 7.19, 7.26, 12.3, 12.6, 12.7, 12.8, 12.9, 12.10, 12.11, 12.12, 12.15, 12.16, 12.19, 12.20 | 5.7, 5.14, 5.17, 5.21 | - |
| INF-005 | inferred | docs/designs/orchestrator-mode.md:215 | containment | 2.12 | 2.12 | quote: B1: imports go one way, `commands -> {probes, classify, report} -> models`. (containment 0.6, best item 2.12) |
| INF-014 | inferred | docs/designs/orchestrator-mode.md:902 | containment | 5.4 | 5.4 | quote: Where the REPORT text and this design differ, this design wins (section 13, REPORT differences). (containment 0.6667, best item 5.4) |

How the matrix was built, verbatim from `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/coverage-matrix.yaml:9-22` (the match is literal, so `none` means no literal ID token, not proof of absence):

````yaml
matching:
  parsed: exact word-boundary token over item text (item heading to next item or ## / ### heading); fuzzy pass off (no --fuzzy-ids); range notation only for '..' or '-' forms, 'X to Y' not expanded
  step_ids: token must have 'step' or 'steps' within the 40 characters before it (avoids DESIGN line numbers and section numbers such as 1.4 colliding)
  routing_rows_R1_R8: token must have 'row' or 'rows' within the 40 characters before it and must not be followed by '-' (design-fix names R3-B1, R3-B2, R3-B3 are not routing rows; tasklist line 165)
  inferred: containment >= 0.6 of casefolded, stopword-stripped content words of the quote in a single item; best ratio wins; first item breaks ties
  spans: parsed spans taken at each ID's defining occurrence (table row, list item or heading section); INF quotes lie outside them (for example DESIGN line 47 is inside the GQ-103(1) heading section 39-50 and was dropped)
excluded_tokens:
  - token: GQ-100
    citation: docs/designs/orchestrator-mode.md:79
    reason: appears only as the upper bound of 'GQ-01 to GQ-100', which names the REPORT's own GQ rows, not a requirement of this design
  - token: M1 to M10, G-1
    reason: not in the Pass-1 ID families named by the request (FR, NFR, GQ, D-n, SP, steps 1.0a-1.29, R1-R8)
  - token: GQ-103(1), GQ-103(2), GQ-103(3)
    reason: folded into the single row GQ-103 (sub-parts of one GQ); GQ-103(2) at line 59 and GQ-103(3) at line 60 share the match
````
