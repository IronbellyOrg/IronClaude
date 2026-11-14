# Reviewer brief 1: analyzer lens, UC-1 pre-execution

This brief is self-contained. `sc-reflect-protocol` Step 3B.0 wrote it for a Tier-2 UC-1 (pre-execution) run. You audit a proposed tasklist against its driving spec before any of it is executed. Everything you need is below or in the files listed under "Files you may Read".

**Run facts**

- Repository root (your grounding root): `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode`. Every path in this brief is relative to it.
- OUT: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre`.
- SPEC, the driving spec of this run: `docs/designs/orchestrator-mode.md` (1013 lines).
- TASKLIST, the plan under review: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md` (2892 lines, 355 items).
- Tier-1 card: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/reflection-card-t1.yaml`. Coverage matrix: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/coverage-matrix.yaml`.
- Reviewer 1 of 3. Persona: analyzer. Model class: claude-gw-tier1b (the sonnet slot). Agent type: `reflect-reviewer` (read-only).

**Names used in the hunks**

- The TASKLIST calls this run's SPEC "DESIGN". When the TASKLIST says "SPEC", it means `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md`, the upstream requirements file of the design. In this brief, SPEC always means `docs/designs/orchestrator-mode.md`.
- "R3-B1", "R3-B2", "R3-B3", "design fix R4" and "design fix R5" are design-fix work in TASKLIST phases 2 to 6. "Routing row R1" to "routing row R8" are the rows of the SPEC section 9 table. They are different things (TASKLIST line 165).
- SPEC line numbers in the hunks are the current, unrevised SPEC. TASKLIST phases 2 to 6 edit the SPEC, so later TASKLIST items find SPEC text by heading (TASKLIST line 1414).
- "research/NN" in the TASKLIST means `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/research/NN-*.md`.

**Your slice**

Requirement coverage and ordering: the 26 FR rows, the 15 NFR rows and the 35 step rows (steps 1.0a to 1.29) of the coverage matrix, judged against TASKLIST phases 7 to 14 (items 7.1 to 14.49). Phases 2 to 6 only edit the SPEC; a match there is not delivery, so the slice table lists phase 7 to 14 matches in their own column.

**Out of scope (other reviewers cover it)**

- Reviewer 2 (qa): verification soundness, HALT gates, QA gate sizing, the test-plan case lists, and the GQ, D, SP and INF rows.
- Reviewer 3 (refactorer): the design-fix phases 2 to 6 and scope creep or missing reuse in the planned code.

**How to review**

1. For each row in the Coverage slice, find the TASKLIST item or items in phases 7 to 14 that deliver the requirement. Treat the matrix `matched_items` and `semantic_note` as leads only: the T1 card says the match is literal (card lines 21-25). Give each row one verdict. For `covered-in-substance`, cite both the TASKLIST item and the SPEC section 11 or 12 row it relies on.
2. Ordering. For each step row, compare where its delivering item sits in the TASKLIST with the "Gate before the step" column of the SPEC section 15.2 table (hunks H5 and H6) and with the section 8 gate (H7). Report an item that runs before the item delivering its gate step. Also report a gate the TASKLIST adds or removes compared with that column, and say whether the TASKLIST states its reason (for example TASKLIST line 164).
3. Requirements that the SPEC assigns to a commit or a phase grouping (SPEC lines 703-708, step 1.4a "The first code commit", step 1.23 "in the same commit as 1.21") are part of your ordering check; the TASKLIST rule that nothing is committed is at TASKLIST line 157.
4. Confirm, refine or contradict T1 findings F4, F6 and F8 and the FR, NFR and steps groups of the T1 gap registry.
5. Typical gap classes for this slice: `missing`, `partial`, `traceability`, `ordering`.

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

**Output contract**

Write one YAML reviewer card to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/reviewer-cards/reviewer-1-card.yaml`. If your tool set has no Write tool (the fixed `reflect-reviewer` type has none), return the complete YAML as your final message, with nothing before or after it; the orchestrator saves it to that path unchanged.

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
reviewer: 1
persona: analyzer
model_class: claude-gw-tier1b
brief: .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/reviewer-briefs/reviewer-1.md
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
  - id: R1-G<k>
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

Source: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/reflection-card-t1.yaml:1-30`

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

coverage:
  parsed_count: 120
  inferred_count: 15
  matched_parsed: 66
  matched_inferred: 10
  coverage_pct: 0.5500
  coverage_pct_union: 0.5630
  unmapped_requirements: 54
  unmapped_requirements_union: 59
  coverage_degraded: null   # parsed-sparse does not fire: inferred (15) is not greater than parsed (120)
  note: >-
    The match is literal (word-boundary ID tokens). Most of the 54 unmapped parsed IDs are covered in
    substance through delegation to DESIGN rows (for example item 10.2 delegates to the DESIGN section 11
    row "FR-006 to FR-010, FR-012 to FR-015", which the range rule does not expand because it is written
    with "to"). The literal figure therefore understates real coverage; see the gap registry.

signals:
  S_scope: 355          # tasklist item count; above 10, exits the T1 STOP path
  S_domains: 5          # code, tests, docs, config, infra; 3 or more escalates
  S_dev_density: 0.437  # 59 unmapped / 135 union rows; above 0.20 escalates
````

Source: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/reflection-card-t1.yaml:102-119`

````yaml
  - id: F4
    severity: MEDIUM
    category: Refinement
    tag: Grounded
    claim: >-
      Traceability is weak: 54 of 120 parsed SPEC IDs never appear as a literal token in the tasklist
      (coverage_pct 0.55). Most are covered by delegation to DESIGN rows, for example item 10.2 cites the
      DESIGN section 11 row "FR-006 to FR-010, FR-012 to FR-015", which covers FR-007, FR-008, FR-009,
      FR-013 and FR-014 in substance only. Whether GQ-105 (`FINAL:`), D8 (`unpushed`), SP-07
      (`guard refused:`), SP-21, SP-22 and SP-26 are covered can be checked only by following the
      delegation, because their literal strings appear nowhere in the tasklist.
    evidence:
      - .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1784
      - .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/coverage-matrix.yaml
    recommendation: >-
      In each test-creation item (10.x) and doc item (13.x, 14.x), list the SPEC IDs it covers explicitly
      instead of a "to" range, and add a final QA item that greps the tasklist for every ID in the
      coverage-matrix unmapped list. Success: a re-run of this coverage map reaches coverage_pct 0.90 or more.
````

Source: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/reflection-card-t1.yaml:142-159`

````yaml
  - id: F6
    severity: LOW
    category: Refinement
    tag: Grounded
    claim: >-
      Commit-grouping requirements cannot be checked because the task never commits: "R1, R2 and R3 land in
      one commit", step 1.4a "The first code commit", and step 1.23 "in the same commit as 1.21". The
      tasklist documents this choice, so it is a Refinement, but the one-commit invariant is left to the
      later user-requested commit with nothing that reminds the committer.
    evidence:
      - docs/designs/orchestrator-mode.md:705
      - docs/designs/orchestrator-mode.md:911
      - docs/designs/orchestrator-mode.md:932
      - .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:157
      - .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1414
    recommendation: >-
      Add a hand-off note to the final task output listing the commit groupings the user must keep
      (R1+R2+R3 together; 1.21 with 1.23). Success: the final report names both groupings.
````

Source: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/reflection-card-t1.yaml:174-188`

````yaml
  - id: F8
    severity: LOW
    category: Refinement
    tag: Grounded
    claim: >-
      Ordering is sound with one benign change: SPEC step 1.4a depends on 1.2, and the tasklist builds it
      after 1.1 to 1.3, which still satisfies "before any other probe code" because 1.4 follows it. The
      Phase 7 owner gates precede all code (item 6.2 gate and Phase 7 procedure), R5 follows 1.14, R7
      follows 1.18 and R8 follows 1.16, matching the SPEC dependency column.
    evidence:
      - docs/designs/orchestrator-mode.md:911
      - docs/designs/orchestrator-mode.md:912
      - docs/designs/orchestrator-mode.md:929
      - .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1414
    recommendation: none
````

Source: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/reflection-card-t1.yaml:214-254`

````yaml
gap_registry:
  - group: FR
    ids: [FR-007, FR-008, FR-009, FR-013, FR-014]
    status: covered in substance
    via: "item 10.2 delegates to the DESIGN section 11 test_classify.py row (range written with 'to')"
  - group: FR
    ids: [FR-011, FR-016, FR-017, FR-018, FR-019, FR-020, FR-022, FR-024, FR-026]
    status: substance-only candidates
    via: "DESIGN section 11 test rows and the 8.x build items; see semantic_note per row in coverage-matrix.yaml"
  - group: NFR
    ids: [NFR-002, NFR-005, NFR-007, NFR-008, NFR-009, NFR-011, NFR-012, NFR-015]
    status: substance-only candidates
    via: "NFR-002 by item 8.x readonly tests (step 1.4a); NFR-012 by the gate items 14.1 to 14.4; others via DESIGN section 11 rows"
  - group: GQ
    ids: [GQ-111, GQ-112, GQ-113]
    status: missing
    via: "F1: no GAPS line 138 rule in the tasklist"
  - group: GQ
    ids: [GQ-101, GQ-102, GQ-104, GQ-105, GQ-106, GQ-107, GQ-108, GQ-109, GQ-110]
    status: substance-only candidates
    via: "DESIGN section 2.2 citations; GQ-105 (FINAL:) has no literal string in the tasklist"
  - group: D
    ids: [D2, D7, D8]
    status: substance-only candidates
    via: "DESIGN section 16 rows; D8 (unpushed) has no literal string in the tasklist"
  - group: SP
    ids: [SP-07, SP-09, SP-19, SP-20, SP-21, SP-22, SP-23, SP-25, SP-26, SP-28]
    status: substance-only candidates
    via: "DESIGN section 17 rows; SP-07 (guard refused:), SP-21, SP-22 and SP-26 need delegation checks"
  - group: steps
    ids: ["1.21", "1.22", "1.23", "1.24", "1.25", "1.26", "1.27"]
    status: covered in substance
    via: "items 13.1 to 13.5 (steps 1.21 to 1.24) and 14.1 to 14.4 (steps 1.25 to 1.27) name the routing rows, not the step numbers"
  - group: INF
    ids: [INF-006, INF-007, INF-008, INF-009, INF-012]
    status: missing
    via: "B3, B4, B5 (F5); R1/R2/R3 one commit (F6); .dev/sweeps/ only (F5)"
  - group: INF
    ids: [INF-001]
    status: false positive match
    via: "0.714 lexical match to item 7.26; the GAPS line 138 rule itself is absent (F1)"
````

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-08T10:11:39Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode

Hunk index (why each hunk is here):

- H1 `docs/designs/orchestrator-mode.md:749-778`: SPEC section 12 traceability: FR-001 to FR-026, design element and test file.
- H2 `docs/designs/orchestrator-mode.md:779-800`: SPEC section 12 traceability: NFR-001 to NFR-015, G-1, GQ and SPEC section 11 rows.
- H3 `docs/designs/orchestrator-mode.md:724-747`: SPEC section 11 test plan by file: the case lists the FR and NFR rows delegate to.
- H4 `docs/designs/orchestrator-mode.md:864-877`: SPEC section 15.1 rules for the step 1.0a capture.
- H5 `docs/designs/orchestrator-mode.md:896-921`: SPEC section 15.1 end and section 15.2 step table, steps 1.0a to 1.13, with the gate column.
- H6 `docs/designs/orchestrator-mode.md:922-943`: SPEC section 15.2 step table, steps 1.14 to 1.29, and the `.gitignore` placement note.
- H7 `docs/designs/orchestrator-mode.md:659-662`: SPEC section 8 gate on steps 1.17 to 1.19.
- H8 `docs/designs/orchestrator-mode.md:703-708`: SPEC section 9 rules, including the R1, R2 and R3 one-commit rule.
- H9 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:155-165`: TASKLIST key constraints: QA rule, no commit, owner-decision gating (line 164), naming (line 165).
- H10 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1136-1140`: TASKLIST Phase 7 intro: which decisions gate which steps.
- H11 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1212-1231`: Items 7.11 to 7.13: D9 sign-off and the step 1.0b record.
- H12 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1263-1282`: Items 7.17 to 7.19: step 1.0a facts, fixtures and the step 1.16a record.
- H13 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1412-1421`: Phase 8 intro and item 8.1 pre-flight.
- H14 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1423-1442`: Items 8.2 to 8.4: steps 1.1, 1.2 and 1.3.
- H15 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1444-1463`: Items 8.5 to 8.7: step 1.4a code part, `.gitignore`, test package.
- H16 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1465-1491`: Items 8.8 to 8.11: conftest, step 1.4a tests, step 1.4, re-run.
- H17 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1493-1505`: Items 8.12 and 8.13: step 1.5 and the Phase 8 validation.
- H18 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1621-1649`: Phase 9: items 9.1 to 9.4, steps 1.6 and 1.7 and the step 1.4 live check.
- H19 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1772-1795`: Phase 10 intro and items 10.1 to 10.3: steps 1.8 to 1.10.
- H20 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1797-1823`: Items 10.4 to 10.7: steps 1.11 to 1.13.
- H21 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1946-1976`: Phase 11 intro and items 11.1 to 11.4: steps 1.14 to 1.16 and 1.20.
- H22 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:2099-2129`: Phase 12 intro and items 12.1 to 12.4: steps 1.17 to 1.19 and 1.24a.
- H23 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:2252-2275`: Phase 13 intro and items 13.1 to 13.3: steps 1.21 and 1.22.
- H24 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:2277-2303`: Items 13.4 to 13.7: steps 1.23, 1.24, 1.24b and the `.gitignore` check.
- H25 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:2433-2463`: Phase 14 items 14.1 to 14.4: steps 1.25 to 1.27.
- H26 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:2465-2491`: Items 14.5 to 14.8: steps 1.28 and 1.29.

### docs/designs/orchestrator-mode.md:749-778

````markdown
## 12. Traceability

Every SPEC requirement (SPEC lines 95 to 120 and 130 to 144) maps to the design element that meets it and the test file that checks it. Test file names are those of section 11; `tests/sweep/` is shortened to `sweep/`.

| ID | Design element (section) | Test file |
|---|---|---|
| FR-001 | `sweep_group`, `commands.run`; `main.py` registration (7.1, 7.6, step 1.7) | `sweep/test_cli_registration.py` |
| FR-002 | `_check_run_ids`, `bind_run`, `BindingError`; first call per Run is `worker-list` (5, 7.1) | `sweep/test_cli_contract.py` |
| FR-003 | `_parse_window` (7.1) | `sweep/test_cli_contract.py` |
| FR-004 | `_find_root`, `_check_output`, re-check in `_publish` (3.2, 7.1) | `sweep/test_cli_contract.py` |
| FR-005 | `SweepResult` rows and worktrees; `summary` reconciliation (6, 7.2, 7.4) | `sweep/test_cli_contract.py` |
| FR-006 | `classify.RULES`, `CLASSES`; rule 6 wording and SP-07 (7.1, 7.2) | `sweep/test_classify.py` (SP-07 `guard refused:` case), `sweep/test_report.py` (no `admitted` or `accepted`) |
| FR-007 | `SweepContext`; `last_activity` source rule (7.2) | `sweep/test_classify.py` |
| FR-008 | Rule 9 `fallback`; could not determine as its own class (7.2) | `sweep/test_classify.py` |
| FR-009 | Rule 2 `orca_exit_proof` decline and note (7.2) | `sweep/test_classify.py` |
| FR-010 | `person_started` tri-state, completeness guard with its four join-incomplete cases (the fourth is the path-B earlier pane session), worker defined by a join to a scoped Dispatch row, with a path-B join also needing the Dispatch row's time window, SP-29 other-Run rule as narrowed by D9 with the `origin not proved` note on every no-entry True, `read_tab_map` (2.2 GQ-108, 7.1, 7.2, 13) | `sweep/test_classify.py` (the D9 join fixtures and the SPEC line 236 fixture), `sweep/test_report.py` (SP-16 literal) |
| FR-011 | `SECTIONS` order and the (a) sort (7.5) | `sweep/test_report.py` |
| FR-012 | `safe_to_close`; `worktree` never `yes` (7.1, 7.2) | `sweep/test_classify.py` |
| FR-013 | `removable` with the named condition; M7 `unpushed`; a worktree removed mid-sweep is unscanned (7.1, 7.2) | `sweep/test_classify.py`, `sweep/test_probes_allowlist.py` (`parse_status`, worktree-removed fixture) |
| FR-014 | `package_state`, `PACKAGE_STATES`; `FINAL:` only at line start (2.2 GQ-102, GQ-105; 7.1, 7.2) | `sweep/test_classify.py` (one fixture per state, the `FINAL:` inside-text negative) |
| FR-015 | `mark_shared_packages`; `--untracked-files=all` in `ALLOWED_GIT` (2.2 GQ-101, 7.3) | `sweep/test_classify.py` |
| FR-016 | `sanitize`, `cell` (7.1, 2.2 GQ-107) | `sweep/test_report.py` |
| FR-017 | `_publish` naming and suffixes; `to_json` printed after the commit point (3, 7.4) | `sweep/test_cli_contract.py` |
| FR-018 | Exit mapping in `commands.run` (3.4, 7.1) | `sweep/test_cli_contract.py` |
| FR-019 | `OrcaResult` `unavailable`; disk-only continuation; banner (5, 7.1) | `sweep/test_cli_contract.py` |
| FR-020 | `Budget` (7.1); byte limits in the readers (7.1, 7.3); WC-13 rows under Retained problems (7.2) | `sweep/test_probes_allowlist.py` (budget cases, the nine byte-limit boundary fixtures), `sweep/test_report.py` (header line, WC-13 Retained problems line) |
| FR-021 | Read-only package; `FORBIDDEN` list held in the test only (7.3) | `sweep/test_probes_allowlist.py` |
| FR-022 | `/sc:sweep` command and `sc-sweep-protocol` skill (7.6) | `tests/commands/test_sweep_command.py` |
| FR-023 | WC-14 and the never-as-worker addition (8) | `tests/skills/test_worker_contract.py` |
| FR-024 | R1 to R8 (9) | `tests/recommend/`, `tests/core/`, `tests/commands/test_routing_plugin_parity.py` |
````

### docs/designs/orchestrator-mode.md:779-800

````markdown
| FR-025 | `.gitignore` line (10) | `sweep/test_readonly.py` (real-git test) |
| FR-026 | `OrcaResult` kinds and the result parser in `_orca` (7.1) | `sweep/test_probes_allowlist.py` |
| NFR-001 | One write in `_publish`; exit 0 only after the temp file is removed (3.2, 3.4) | `sweep/test_readonly.py` (snapshot diff), `sweep/test_cli_contract.py` (unlink-failure case exits 1) |
| NFR-002 | `_git` argv and env (2.1, 7.1, 7.3) | `sweep/test_readonly.py` |
| NFR-003 | `check_orca_argv`, `check_git_args`, `orca_binary` (7.1, 7.3) | `sweep/test_probes_allowlist.py` |
| NFR-004 | Pure `classify.py` and `report.py` (4, 7.1) | `sweep/test_classify.py` (AST test) |
| NFR-005 | `render` and `to_json` read no clock; `collected` interval in `SweepInput` (7.1, 7.4) | `sweep/test_report.py` |
| NFR-006 | Lazy `__getattr__` in `__init__.py` (7.1) | `sweep/test_cli_registration.py` |
| NFR-007 | `Budget` 90 s; skill timeout 120000 ms; one re-read of a changed input only while the budget allows (7.1, 7.2, 7.6) | `sweep/test_probes_allowlist.py` (budget cases, changed-contract fixture), `tests/commands/test_sweep_command.py` |
| NFR-008 | `unscanned:` reasons flow to could not determine (6, 7.2) | `sweep/test_report.py` |
| NFR-009 | JSON v1 key set (7.4) | `sweep/test_cli_contract.py` |
| NFR-010 | `RULES` order pinned by name (7.2) | `sweep/test_classify.py` |
| NFR-011 | `~/.claude/...` paths in the command and skill (7.6) | `tests/commands/test_sweep_command.py`; step 1.28 grep |
| NFR-012 | Repo gates (15.2, steps 1.25 to 1.27) | none (gate commands) |
| NFR-013 | Patched seams and the autouse subprocess guard (11) | every `sweep/` file through `conftest.py` |
| NFR-014 | `ALLOWED_ORCA` eight templates (7.3) | `sweep/test_probes_allowlist.py` |
| NFR-015 | `CHECKED_ORCA_VERSION`, `read_orca_version` (7.1) | `sweep/test_report.py` |
| G-1 | `_publish` and the exit-1 rule, including exit 1 when the temp unlink fails after the commit point (3) | `sweep/test_cli_contract.py` (publication cases, unlink-failure case), `sweep/test_readonly.py` |
| GQ-101 to GQ-110 | Section 2.2 | as the FR rows above name them |
| SPEC section 11 failure modes (lines 440-454) | Observation rules (7.2): worktree removed, unreadable transcript or contract, list and show disagree, unknown schema field, path escapes its source, input changed, duplicate Dispatch, remote hosts. The other rows map to the FR, NFR and D rows above: 438 and 439 to FR-019 and FR-026, 441 to NFR-002 and NFR-015, 444 to FR-008, 445 to FR-020, 447 to NFR-003, 448 to FR-017, 449 to FR-016, 453 to D2 | `sweep/test_probes_allowlist.py` (440, 443, 446, 450, 451, 452), `sweep/test_classify.py` (442), `sweep/test_report.py` (454) |
| SPEC section 7 cross-cutting notes (lines 236, 259, 261, 269) | SP-16 literal, rule 6 wording and SP-07, WC-13 note, `FINAL:` reading (7.2) | `sweep/test_classify.py`, `sweep/test_report.py` |

````

### docs/designs/orchestrator-mode.md:724-747

````markdown
## 11. Test plan mapped to files

Seven new files under `tests/sweep/` (the REPORT names, steps 1.8 to 1.13), one new command test, and edits to four existing test files. Every test runs with the seams patched; none starts Orca, ccsession or Claude (NFR-013).

Shared setup in `tests/sweep/conftest.py` (step 1.8):

- `patch_orca` and `patch_git` replace `probes._orca` and `probes._git` with fakes that record every argv and return fixture data, as `tests/cli/reflect/conftest.py` does for its seams.
- An autouse fixture patches `subprocess.run`, `subprocess.Popen` and `os.system` to raise `AssertionError`. It steps aside only for a test carrying the existing `integration` marker, which is used by exactly one test, the real-git test below. `pyproject.toml` runs pytest with `--strict-markers`, and `integration` is already registered there, so no new marker and no `pyproject.toml` edit is needed.
- A fixed `now` and a `tmp_path` layout with `HOME` and `XDG_STATE_HOME` moved inside it, holding packages, contracts, transcripts and a ccsession `orca-tabs/` folder.
- Fixtures copied from captured Orca output keep their source name; hand-made ones carry `synthetic` in the file name until step 1.0a replaces them.

| File | Covers | Main cases |
|---|---|---|
| `tests/sweep/test_readonly.py` (created at step 1.4a, extended at 1.11) | NFR-002, FR-025, GQ-103(1), GQ-110, NFR-001, NFR-013 | Step 1.4a part: every recorded `_git` argv has `--no-optional-locks` at index 1 and `-C <path>` after it; the child env holds `GIT_OPTIONAL_LOCKS=0`; one git argv per discovered worktree; the one `integration`-marked real-git test in a `tmp_path` repository with the four SPEC assertions (control, `check-ignore` of `.dev/sweeps/x.md` succeeds, of `.dev/tasks/to-do/x.md` fails, a file under `.dev/sweeps/` leaves `git status --porcelain` unchanged). Step 1.11 part: the snapshot diff (path, size, `st_mtime_ns`, SHA-256) over the root, `HOME` and the XDG dirs: exactly one added report file plus the output directory when new; no temp file and no second name for the report remain after exit 0 |
| `tests/sweep/test_probes_allowlist.py` | NFR-003, NFR-014, FR-021, FR-026, FR-020, NFR-007, GQ-109, M7, SPEC section 11 failure modes | Full-sweep recording: each argv equals one template token for token, argv[0] is `$ORCA_CLI_COMMAND` when set, else `orca-ide`; zero argv for `worktree list` and `worktree current`; exact-set pin of the eight templates; negatives that raise `ValueError` before a subprocess (`check`, `inbox`, `worker-read`, `gate-list`, an extra flag, `--include-remote`, `--agent-wait`, `run-list`); the FR-021 forbidden list held in the test; git negatives (`rev-parse`, `log`, `branch`, `--version`, any `stash` form). Result classes: each unavailable cause on call one, the quoted-marker negative fixture, a middle `worker-show` exit 1, a malformed zero-exit body, the empty `run-current` body, and the captured no-binding fixture (gated on 1.0a). Budget: 60 rows give 50 `worker-show` and `bound_reached == 10`; 50 rows give 50 and 0; 2 Runs of 40 get 25 each; with 20 s left the per-call timeout is at most 20 s; full-timeout fakes finish under 120 s and still publish. Byte limits: a contract over 1 MiB is unscanned with a reason; a ledger over 1 MiB is read as head and tail (GQ-105); nine boundary fixtures at limit minus 1, at the limit and at limit plus 1 for each of the 1 MiB contract and ledger limit, the 256 KiB transcript tail and the 8 MiB subprocess output (SPEC line 297; the limit is hit only when size is over it, section 7.3). Failure modes (section 7.2 observation rules): the worktree directory deleted between the two seams gives that worktree `unscanned: worktree not readable` while the others continue (SPEC line 440); list and show disagree and the `worker-show` value is used (443); one missing and one extra `worker-show` key leave the field None and raise nothing (446); a symlink-out fixture is rejected with `unscanned: outside root` (450); a contract changed between two reads gets one re-read, and a contract that changes on every read gets `conflict: inconsistent observation` (451); a duplicate Dispatch fixture with two states gives one `orca:<dispatch>` row with `conflict: duplicate Dispatch rows disagree` (452). `parse_status` cases for M7: `ahead 3`, upstream with no ahead, no upstream, `[gone]`, detached HEAD, `No commits yet`, a rename pair in `-z` form, a `??` path under `.dev/tasks/` |
| `tests/sweep/test_classify.py` | FR-006 to FR-010, FR-012 to FR-015, NFR-010, NFR-004, GQ-101, GQ-102, GQ-105, GQ-108, SP-07, SP-16, SP-24, SP-26, SP-29, D9, WC-13, M6, M9, SPEC section 11 unreadable inputs | One parametrized case per rule 1 to 9, reaching every name in `CLASSES`; rule-name order pin `[r.name for r in RULES]`; window cases (5 h old row, windows under and at 6 h; record timestamp older than mtime); the four FR-008 inputs; a late-heartbeat live row is never `stalled (proved)` (SPEC line 444); the two FR-009 cases with the exact note; rule 1 decline notes (M6); rule 5 four-condition case; a future timestamp gives unknown age and never idle; FR-010 complete-negative join, the four incomplete cases, the five exemptions and the SP-29 two-Run fixture (none of the R2 transcripts True or Historical); `person_started` None for every unjoined transcript while `session_join` is None; the D9 join fixtures: a transcript joined to a scoped Dispatch row through its tab-map entry (path B) is False and shown as `orca:<dispatch>`, a tab-map entry that joins no scoped row gives None with note `Orca pane session, not in scoped Runs` even when the guard holds, under path A a transcript with no tab-map entry and no join is True when the guard holds and carries note `origin not proved: no tab-map entry; may be a worker of a Run outside the scope` (the declared D9 limit), and a worker of an unscoped Run with no tab-map entry, placed in the same worktree, is never True without that note; a path-B scoped row whose `session_join` matches no tab-map entry makes every unjoined transcript None with the SP-16 literal; the R2-B1 pane-reuse fixtures under path B, one each for `/clear`, a resume and a person rerunning the command in the tab: the worker's earlier transcript has no entry and is None with note `earlier pane session not joinable (tab map keeps only the latest session)`, never True or Historical; the later session, whose earliest timestamp is outside the Dispatch row's window, does not join, the row is could not determine with note `pane moved to a later session`, and that later transcript is None with the same note; a later session inside the window is False with note `joined by pane: latest session of the pane`; a row with no observable start time never joins by path B; when guard cases 1 and 2 hold together, the transcript carries the SP-16 literal first, then `tab map join not observable`; the SPEC line 236 fixture (worker rows present, no transcript joined) gives the same; SP-07: a contract body whose later line quotes `guard refused:` is not finished (SPEC line 259); a `progress.md` with `FINAL:` inside other text is not `archive-blocked` (269); a truncated-JSONL transcript (last record cut mid-object, no complete record with both `timestamp` and `sessionId`) and an unreadable contract (open raises `OSError`) each give could not determine with their `unscanned:` note (442); a transcript cut only in its last line that still has an earlier complete record with both fields stays readable and is classified normally; a transcript whose open raises `OSError` gives `unscanned: transcript not readable`; an Orca row with a non-null `parent` carries `WC-13 violation, review` and keeps its class (261); FR-012 over all fixtures (`worktree` never `yes`); one FR-013 fixture per condition with the condition named; one FR-014 fixture per state including `conflict`; the FR-015 fixtures (44 committed folders in 3 worktrees give no flag, one modified folder in 3 worktrees gives one line naming all 3, one `??` path marks a package active); the FR-005 person-session fixture uses an active session (M9); AST import test that `classify.py` and `report.py` import none of `subprocess`, `click`, `os`, `shutil` |
| `tests/sweep/test_report.py` | FR-011, FR-016, NFR-005, NFR-008, NFR-015, SP-23, SP-24, FR-020 header line, FR-006 (rule 6 wording), SP-16, WC-13, SPEC section 11 remote coverage | Heading order equals section 7.5; (a) sort with 3 ages plus one unknown, tie-break by ID; (b) never prints question text; injection fixture (`a\|b`, ANSI, bidi override, `<script>`, a Markdown link) keeps the column count and leaves no active tag or link; a 300-character cell prints 200 characters ending `...` while the JSON value is whole; render twice gives equal bytes and equal JSON apart from `report_path`; source-loss fixture gives could not determine with the `unscanned:` reason, never finished, failed, not frozen or a recommendation; version line for `1.4.245-aidev02.780594c521aa`, `1.4.246` and a missing file; the `bound_reached` line text; the SP-24 footnote; the empty-section string; the `next inspection` map has an entry for every rule name and no stop, retry, release, merge or removal word; rule 6 wording: a finished row's report text and JSON contain neither `admitted` nor `accepted` (SPEC line 259); the remote-coverage fixture: `## Source coverage` has the `remote hosts` row with coverage `unknown` and the Scope line carries `(lower bound: remote hosts not scanned)`, never a no-sessions line (454); the WC-13 row appears under `## Retained problems` (380); the SP-16 literal `could not join Orca workers to transcripts (tab map empty or stale)` appears under `## Could not determine` (236); a True row with the `origin not proved` note prints the note in its row and in the JSON `notes` (D9); the last line is `Report complete` |
| `tests/sweep/test_cli_registration.py` | FR-001, NFR-006 | `superclaude sweep --help` and `sweep run --help` exit 0 under `CliRunner`; importing `superclaude.cli.sweep` records no seam call and does not import `commands` until `sweep_group` is read |
| `tests/sweep/test_cli_contract.py` | FR-002, FR-003, FR-004, FR-005, FR-017, FR-018, FR-019, NFR-009, G-1 (section 3) | Run id cases (`""`, `'r;x'`, duplicate, unknown-Run then R2); the three binding tests and the fourth gated on 1.0a; disk-only continuation prints `unscanned: orca unavailable`; the FR-003 parser cases; the FR-004 output and root cases; the FR-005 fixture (4 rows, 2 worktrees, `(4/4)`) and the reconciliation equalities; golden v1 key set and types at every level; zero counts present; `waiting` lists hold ids only; two runs with one injected `now` give `stem.md` and `stem-2.md`; one test per exit code. Publication cases from section 3: a link failure, a full disk on write, `stem.md` to `stem-99.md` all taken, an existing temp name, and an output path that escapes after `makedirs` each exit 1 with no file at a report name and no success JSON; a print failure after the commit point exits 1 and leaves one complete report; `os.unlink` patched to raise after a successful `os.link` gives exit 1, no success JSON, exactly one complete report ending in `Report complete`, and a stderr line `[sweep publish] could not remove temp file <path>` naming the temp path; an existing earlier report is byte-identical afterwards |
| `tests/commands/test_sweep_command.py` (new, step 1.16) | FR-022, NFR-011, NFR-007 (static half) | The section 7.6 assertions |
| `tests/skills/test_worker_contract.py` (edit, step 1.19) | FR-023 | The section 8 pins |
| `tests/core/test_how_we_work_routing_table.py`, `tests/recommend/test_routing_refresh.py` (edits); `tests/commands/test_routing_plugin_parity.py` (unchanged, must pass) | FR-024 | R1 to R5 of section 9 |

NFR-012 is checked by the gates of steps 1.25 to 1.27, not by a test file. Run line for the sweep tests: `uv run pytest tests/sweep -v`.
````

### docs/designs/orchestrator-mode.md:864-877

````markdown
## 15. REPORT step mapping for `/task-builder`

### 15.1 What step 1.0a captures

Step 1.0a replaces the REPORT version (REPORT steps list, lines 1237 to 1300). It is a manual, pre-implementation capture run by the person or the coordinator, never by a test, and it writes only its own notes file.

Rules for the capture:

- It runs against an existing Run that the person names. It creates no Run, Task or Dispatch; the REPORT's throwaway Run is dropped.
- It issues only the eight `ALLOWED_ORCA` templates of section 7.3, with the binary `orca-ide` or `$ORCA_CLI_COMMAND`. No `worker-read` (with or without `--source transcript`), no `gate-list`, no `check`, no `inbox`, no `--include-remote`, no `--agent-wait`, and no `git stash` in any form.
- `--json` is tried only where a template already has it. Whether `run-current` needs `--json` is answered by reading its plain output and, only if that is not parseable, by recording the fact for an owner note (M2); the capture does not run `run-current --json`.
- `worker-show` and `task-list` are each run once before and once after all other reads. The two outputs must be identical apart from timestamps; that is the only live check that these reads change nothing (M4). A difference stops the build and goes to the owner.
- Output goes to `.dev/tasks/<pkg>/artifacts/readonly-probe.md` in the task package (always staged, CLAUDE.md rule). Sanitized samples that become test fixtures are copied under `tests/sweep/fixtures/` with their source named.

````

### docs/designs/orchestrator-mode.md:896-921

````markdown
If an item cannot be captured, it stays UNVERIFIED in section 17 and the code path it feeds keeps its could-not-determine behaviour (for example, no `session_join` means `person_started` None for every unmatched transcript).

Pre-implementation steps: 1.0a (this capture), 1.0b (owner decisions) and 1.16a (PR #422 overlap check) run before any code for the steps they gate. Step 1.29 is a manual check after the build.

### 15.2 Step table

REPORT step numbers are kept so the task file can cite the REPORT; one step is new (1.4a). "Pre" marks a pre-implementation step. Where the REPORT text and this design differ, this design wins (section 13, REPORT differences).

| Step | Pre | Work | Design section | Gate before the step |
|---|---|---|---|---|
| 1.0a | Pre | Read-only capture of section 15.1 | 15.1 | An existing Run named by the person |
| 1.0b | Pre | Owner decisions GQ-10, GQ-11, GQ-35, GQ-61, GQ-63, and sign-off on the D9 narrowing of SP-29 (section 13); read `.dev/orca-command-refactor/decisions/APPROVED.md`; record in `.dev/tasks/<pkg>/artifacts/owner-decisions.md` | 8 | none |
| 1.1 | | `src/superclaude/cli/sweep/__init__.py` with lazy `__getattr__` | 7.1 | none |
| 1.2 | | `models.py` | 7.2 | none |
| 1.3 | | `classify.py`, the 9 rules | 7.1, 7.2 | 1.2 |
| 1.4a | | `probes._git`, `ALLOWED_GIT`, `check_git_args`, and `tests/sweep/test_readonly.py` with the NFR-002 recorded-argv, env and real-git tests, plus the `.gitignore` lines. The first code commit | 2.1, 7.3, 10, 11 | 1.2 |
| 1.4 | | Rest of `probes.py`: `_orca`, `ALLOWED_ORCA`, `Budget`, `OrcaResult`, `bind_run`, `collect`, readers. Live check saved to `.dev/tasks/<pkg>/artifacts/sweep-live-check-1.4.json`; no `--include-remote` timing | 7.1, 7.3 | 1.0a (parsers, regexes), 1.4a |
| 1.5 | | `report.py`: `sanitize`, `cell`, `render`, `to_json`, `SECTIONS`; no `write_report` | 7.1, 7.4, 7.5, D1 | 1.3 |
| 1.6 | | `commands.py`: `run`, `_parse_window`, `_find_root`, `_check_output`, `_check_run_ids`, `_publish`; no `run-list` fallback; `--output` default `<root>/.dev/sweeps/` | 3, 5, 7.1 | 1.4, 1.5 |
| 1.7 | | Register `sweep_group` in `src/superclaude/cli/main.py` with the deferred-import pattern (after line 561) | 7.1 | 1.6 |
| 1.8 | | `tests/sweep/conftest.py` and fixtures | 11 | 1.0a for captured fixtures |
| 1.9 | | `tests/sweep/test_classify.py` | 11 | 1.3 |
| 1.10 | | `tests/sweep/test_probes_allowlist.py` | 11 | 1.4 |
| 1.11 | | Extend `tests/sweep/test_readonly.py` with the NFR-001 snapshot diff and NFR-013 | 11 | 1.6 |
| 1.12 | | `tests/sweep/test_report.py` | 11 | 1.5 |
| 1.13 | | `tests/sweep/test_cli_registration.py` and `tests/sweep/test_cli_contract.py` | 11 | 1.7 |
````

### docs/designs/orchestrator-mode.md:922-943

````markdown
| 1.14 | | `src/superclaude/commands/sweep.md` | 7.6 | 1.7 |
| 1.15 | | `src/superclaude/skills/sc-sweep-protocol/SKILL.md`, recommending nothing | 7.6 | 1.14 |
| 1.16 | | `tests/commands/test_sweep_command.py` | 7.6, 11 | 1.15 |
| 1.16a | Pre | `gh pr view 422 --repo IronbellyOrg/IronClaude --json state,files` and the #409 diff check; results to `.dev/tasks/<pkg>/artifacts/` | 8 | none; must finish before 1.17 |
| 1.17 | | WC-14 in `src/superclaude/core/WORKER-CONTRACT.md` | 8 | 1.0b (GQ-11 answered), 1.16a |
| 1.18 | | `WORKER-CONTRACT.md` line 23, never-as-worker list | 8 | 1.17 |
| 1.19 | | Pins in `tests/skills/test_worker_contract.py` and the rename | 8 | 1.18 |
| 1.20 | | R5 | 9 | 1.14 |
| 1.21 | | R1 and R2 | 9 | 1.14 |
| 1.22 | | R4 | 9 | 1.21 |
| 1.23 | | R3, in the same commit as 1.21 | 9 | 1.21 |
| 1.24 | | R6 | 9 | 1.14 |
| 1.24a | | R7 | 9 | 1.18 |
| 1.24b | | R8 | 9 | 1.16 |
| 1.25 | | `make sync-dev`, then `make verify-sync`; no `.claude/` path staged | 9 | 1.24b |
| 1.26 | | `make lint`, `uv run ruff check .`, `uv run ruff format --check src/ tests/` | none | 1.25 |
| 1.27 | | `uv run pytest tests/sweep tests/commands tests/core tests/skills tests/recommend`, then `uv run pytest` | 11 | 1.26 |
| 1.28 | | `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}`, every hit justified | 7.6 | 1.27 |
| 1.29 | Manual | `superclaude sweep --help` under a pipx install; output saved to `.dev/tasks/<pkg>/artifacts/sweep-help-pipx.txt` | 7.6 | 1.28 |

The `.gitignore` lines (section 10) have no REPORT step of their own. They go into step 1.4a because the real-git test created there copies the repository `.gitignore`, so its FR-025 check-ignore assertions fail until the line exists.

````

### docs/designs/orchestrator-mode.md:659-662

````markdown
## 8. WC-14 and the never-as-worker list

**Gate.** Steps 1.17 to 1.19 are written only after the owner answers GQ-11 (step 1.0b) and the PR #422 overlap check (step 1.16a) is done. WC-14 and its pins stay deliverables of this PR whatever #422 does (SPEC line 420).

````

### docs/designs/orchestrator-mode.md:703-708

````markdown
Rules:

- R1, R2 and R3 land in one commit. Editing R1 or R2 without R3 fails the parity test.
- The level table is not touched, so the `src/superclaude/core/CLAUDE.md` level-table copy (project CLAUDE.md, Key Documentation Files) needs no re-run. If a later edit touches the level table, that copy is re-run in the same commit.
- R1 and R6 avoid the words stop, retry, release, merge and removal in the sweep's description.
- No `.claude/` path is staged; `make sync-dev` then `make verify-sync` (step 1.25) refresh the dev copies.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:155-165

````markdown
### Key Constraints
- **QA:** `QA_INTENSITY: full`, `QA_GATE_REQUIREMENTS: PER_PHASE`. Every gate runs report-only agents first (`fix_authorization: false`), then one consolidation item, then ONE rf-qa fix agent (`fix_authorization: true`, skipped when every finding is minor), then verification by at least 1 rf-qa and 1 rf-qa-qualitative, at most 2 fix cycles per gate. The lens agents of one gate are spawned in the SAME message, in parallel, and so are the two verifiers of one cycle. Minor findings never fail a gate. Halt order on every cycle transition: regression first, then monotonicity, then the hard cap. Each gate keeps a `cycle-ledger.md` with the PASS set and the F set and count of every cycle, so the regression check has its input. The halt strings are byte-exact: `Regression detected on Item X.Y, previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.` and `[HALT-MONOTONICITY] |F|=<n>`. Every phase from 2 to 14 except the human-gate items has a gate; each gate writes only to its own folder: `qa/r3-b1/`, `qa/r3-b2/`, `qa/r3-b3/`, `qa/r4/`, `qa/r5/`, `qa/decisions/`, `qa/impl-core/`, `qa/impl-cli/`, `qa/tests/`, `qa/cmd-skill/`, `qa/contract/`, `qa/docs/`, `qa/final/`, `qa/fidelity/`.
- **No commit, push or merge.** `/task` never commits, pushes or merges; this file has no commit or push item. Commits happen only when the user asks. The PR is opened later only through `/sc:pr-submit --monitor 3`. Any `gh` command carries `--repo IronbellyOrg/IronClaude`.
- **Staging:** never stage a `.claude/` path except `.claude/settings.json`; always stage `.dev/tasks/` (`git add .dev/tasks`). Staging is not committing.
- **UV only:** every Python command is `uv run ...`; never `python -m`, `pip install` or `python script.py`.
- **Installed primitives** (`sweep.md`, `sc-sweep-protocol/SKILL.md`, `WORKER-CONTRACT.md`, `HOW-WE-WORK.md`) name `~/.claude/...` paths, never `src/superclaude/...`.
- **No live Orca, ccsession or Claude launch in any test.** Step 1.0a uses only the eight allowlisted Orca read templates; the step 1.4 live check runs only the built `superclaude sweep run` (itself allowlisted).
- **WC-9 lock retry is out of scope.** No item in this task runs or implements the WC-9 lock retry; that work is tracked in IronbellyOrg/IronClaude#446.
- **Reading discipline:** the executor reads every file in chunks of at most 150 lines (Read with `offset` and `limit`), and anchors every design edit by quoted text, never by a line number alone (review-3 line numbers are 6 lower than the current design, research/04 Summary "Line drift"; every R3 edit also shifts later lines).
- **Owner decisions:** no recommended default is treated as approved unless the decision file says so. Where REPORT line 1238 and DESIGN disagree on what an unanswered decision blocks, DESIGN wins (DESIGN section 15.2 opening sentence), so the whole step 1.0b set gates steps 1.17 to 1.19 and the D9 sign-off gates the classify step 1.3.
- **Naming:** the BUILD-REQUEST design fixes are written "design fix R4" and "design fix R5"; the DESIGN section 9 rows are written "routing row R1" to "routing row R8". They are different things.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1136-1140

````markdown
## Phase 7: Pre-implementation gates 1.0b, 1.0a and 1.16a, and the decisions gate

These are human gates. Each decision has a record item (PENDING) and a HALT item. No recommended default is treated as approved unless the decision file says so. Which rule wins: REPORT line 1238 says unanswered decisions other than GQ-11 "keep the working default", but DESIGN section 15.2 (rows 1.17 and 1.3 gates; section 17 open items 20 and 22) blocks steps 1.17 to 1.19 on the whole 1.0b set and blocks the classify step on D9. DESIGN wins (DESIGN section 15.2 opening sentence). APPROVED rows answer none of the five GQs (research/09 Gap 1, "APPROVED.md" table). The owner's own words in the session are the decision (APPROVED G1, line 71); no separate grant file is created.

Every decision-record item below writes its file with: `needs_human_decision: true`, `status: PENDING`, the question quoted, the options quoted, a recommendation line ending "This recommendation does NOT authorize adoption." (or the no-recommendation sentence for GQ-63), the steps the decision blocks, and the empty block `OPERATOR DECISION:`, `Chosen:`, `Decided by:`, `Decision source:`. Every HALT item below follows the item 6.2 procedure: Branch 1 (PENDING or empty `Chosen:`) applies the HALT rule with the `blocker_reason` the item names and STOPS; Branch 2 (all four lines filled, the source quoting the owner's words) sets `status: RESOLVED`, appends the decision to `### Execution Log`, resets the task `status` to "🟠 Doing" and clears `blocker_reason`.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1212-1231

````markdown
- [ ] **7.11 — Record the D9 sign-off (OQ-7, L5, PENDING)**
  - **Context**: DESIGN section 13 D9 and section 7.2: a worker is a transcript joined to a scoped Dispatch row; an unjoined tab-map entry gives `person_started` None with note `Orca pane session, not in scoped Runs`. DESIGN section 17 open item 22: "the classify step does not start until the owner signs off D9 or names a stricter rule".
  - **Action**: Read DESIGN section 13 (anchor the quoted heading `## 13. Deviations from SPEC`) to quote D9 in full. Write `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/OQ-7-D9-signoff-decision.md` with these parts: `needs_human_decision: true`; `status: PENDING`; the question quoted; the options quoted; the recommendation line below, which ends "This recommendation does NOT authorize adoption."; the steps this decision blocks; and the empty block `OPERATOR DECISION:`, `Chosen:`, `Decided by:`, `Decision source:`. Options: "(a) sign off D9 as written;" "(b) name a stricter rule." Recommendation: "(a) D9 as written. This recommendation does NOT authorize adoption." Blocks: item 8.4 (step 1.3, classify) and every later item.
  - **Output**: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/OQ-7-D9-signoff-decision.md`.
  - **Verification**: Verify: `status: PENDING`, D9 quoted from DESIGN with its line, both options, the label and the four empty decision lines.
  - **Completion gate**: The request is recorded. Once done, mark this item as complete.

- [ ] **7.12 — HALT until the owner signs off D9 (OQ-7, L5)**
  - **Context**: The decision record `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/OQ-7-D9-signoff-decision.md`, written by item 7.11.
  - **Action**: Read the decision file named in Context. Branch 1: if its `status` is PENDING or its `Chosen:` line is empty, apply the HALT rule (set frontmatter `status` to "⚪ Blocked", set `blocker_reason` to the text below, append it to `### Execution Log`, STOP, and do not tick this item) with `blocker_reason: "OQ-7 (D9 sign-off) awaits the owner's decision in phase-outputs/plans/OQ-7-D9-signoff-decision.md"`. Branch 2: if `Chosen:`, `Decided by:` and `Decision source:` are all filled and the source quotes the owner's words, set `status: RESOLVED` in the decision file, append the decision (OQ id, chosen option, decider, source) to `### Execution Log`, set the task frontmatter `status` back to "🟠 Doing" and clear `blocker_reason`. On Branch 2 with option (b), apply the HALT rule with `blocker_reason: "D9 replaced by a stricter rule; DESIGN sections 7.2, 11, 13 and 14 need a revision; re-run /task-builder"` and STOP.
  - **Output**: The decision file with `status: RESOLVED`, or a Blocked task.
  - **Verification**: Verify: on Branch 2 with (a), the file names the option, decider and source. Otherwise stop before marking this item complete until the blocker is resolved.
  - **Completion gate**: D9 is signed off. Once done, mark this item as complete.

- [ ] **7.13 — Compile `artifacts/owner-decisions.md` (step 1.0b, L6)**
  - **Context**: The six RESOLVED files `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/OQ-2-*` to `OQ-7-*`, the RESOLVED OQ-1 file from item 6.2, and `.dev/orca-command-refactor/decisions/APPROVED.md` (90 lines; read in one chunk).
  - **Action**: Write `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/owner-decisions.md` with: one row per decision (OQ-1 R5, GQ-10, GQ-11, GQ-35, GQ-61, GQ-63, D9): option chosen, the owner's words as given, decider, source, the steps it unblocks; then the APPROVED constraint table from research/09 Gap 1 (D3 :10, D4 :11, D5 :12, GIT :13, L3 :20, CR-01 :25, PATHS :29, UPSTREAM :30, B1 :35, B1-N1 :36, S4 :47, G1 :71, F1 :90), each row re-read from APPROVED and quoted with its line. Add no grant file (APPROVED G1).
  - **Output**: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/owner-decisions.md`.
  - **Verification**: Verify: seven decision rows, each matching its RESOLVED file; every APPROVED quote matches its line; no decision row says "default" without the owner's words.
  - **Completion gate**: The file is written. Once done, mark this item as complete.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1263-1282

````markdown
- [ ] **7.17 — Record the 1.0a facts the code needs (L1)**
  - **Context**: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe.md`; DESIGN section 7.2 (after design fix R3-B1: `dispatch.dispatchedAt`, `dispatch.completedAt`, `first_record_ts`) and section 7.3; DESIGN section 17 open items 1 to 11, 15, 16, 22 and 23.
  - **Action**: Write `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/discovery/1.0a-facts.md` with one row per open item 1 to 11, 15, 16, 22 and 23: CLOSED with the fact and its readonly-probe section, or STILL UNVERIFIED (the DESIGN "behaviour until closed" applies). Include: the live field names for the Dispatch start and end times and their time format; the `session_join` field; `agentWait`, `liveness.verdict` and `status` names; the `worker-list` page size and cursor field (`page.nextCursor` or other); the worktree path field; the Run and Dispatch id samples and the regexes `RUN_ID_RE` and `DISPATCH_ID_RE` written from them; the version string. Branch: if a live field name differs from the name DESIGN section 7.2 or 7.3 uses, apply the HALT rule with `blocker_reason: "Step 1.0a: live field <name> differs from DESIGN <section> <name>; the design needs a fix before step 1.2"` and STOP.
  - **Output**: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/discovery/1.0a-facts.md`.
  - **Verification**: Verify: every listed open item has a row; every CLOSED row cites a readonly-probe section. If open item 2 stays unverified, apply the HALT rule with `blocker_reason: "Step 1.0a: no Run or Dispatch id sample; steps 1.4 and 1.6 cannot start (DESIGN 17 item 2)"` and stop before marking this item complete until the blocker is resolved.
  - **Completion gate**: The facts file is written with no open HALT. Once done, mark this item as complete.

- [ ] **7.18 — Copy sanitized 1.0a samples into `tests/sweep/fixtures/` (L2)**
  - **Context**: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/readonly-probe.md`; DESIGN section 11 ("Fixtures copied from captured Orca output keep their source name; hand-made ones carry `synthetic` in the file name until step 1.0a replaces them") and section 15.1.
  - **Action**: For each captured JSON output (items 1 to 8, 13), write one file `tests/sweep/fixtures/captured-<template>.json` (for example `captured-worker-list.json`, `captured-worker-show-<n>.json`). Sanitize: replace home paths with `/home/user`, session ids and pane keys with stable fake values of the same shape (keep joins between files consistent), and user names with `user`; keep every field name and value type. Write `tests/sweep/fixtures/SOURCES.md` naming, per file, the readonly-probe section and template it came from and the sanitize rules applied.
  - **Output**: `tests/sweep/fixtures/captured-*.json` and `tests/sweep/fixtures/SOURCES.md`.
  - **Verification**: Verify: `grep -rn '/home/coder\|coder' tests/sweep/fixtures/` returns nothing; each JSON file parses (`uv run python -c "import json,sys; [json.load(open(p)) for p in sys.argv[1:]]" tests/sweep/fixtures/captured-*.json`); `SOURCES.md` has a row per file. If nothing was captured, write `SOURCES.md` saying so and log it in `### Phase 7 Findings`.
  - **Completion gate**: The fixtures and `SOURCES.md` are written. Once done, mark this item as complete.

- [ ] **7.19 — Record step 1.16a, PR #422 and #409 (record-only, L3)**
  - **Context**: DESIGN step 1.16a (record-only after design fix R4); research/09 Gap 3 "1.16a": #422 is MERGED at `2327fbd3` and `495eb96d` is not an ancestor of `origin/master`.
  - **Action**: Run `gh pr view 422 --repo IronbellyOrg/IronClaude --json state,mergedAt,mergeCommit`, `git merge-base --is-ancestor 2327fbd3 HEAD; echo "exit=$?"` and `git merge-base --is-ancestor 495eb96d origin/master; echo "exit=$?"`. Write `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/pr422-409-check.md` with: (1) the `gh` state line; (2) the first ancestor check (expect exit 0); (3) the second (expect exit 1, so the `495eb96d` pin stands and no layout diff is needed); (4) the note "every `WORKER-CONTRACT.md` and `test_worker_contract.py` line cited by steps 1.17 to 1.19 is re-read at HEAD before it is edited (items 12.1 to 12.3)". No fetch, rebase, push or PR action.
  - **Output**: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/pr422-409-check.md`.
  - **Verification**: Verify: four points recorded with the command outputs. If #422 is not MERGED or check 2 fails, apply the HALT rule with `blocker_reason: "Step 1.16a: PR #422 state or ancestry differs from research/09; DESIGN step 1.16a needs a revision"` and stop before marking this item complete until the blocker is resolved.
  - **Completion gate**: The record is written and matches. Once done, mark this item as complete.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1412-1421

````markdown
## Phase 8: Core package, steps 1.1 to 1.5, and the impl-core gate

Every DESIGN line number below is the line on the unrevised design (1013 lines at `5dc29d23`); Phases 2 to 6 move them, so the executor re-locates each by its section heading and reads DESIGN "as revised by Phases 2 to 6" in chunks of at most 150 lines. Where DESIGN and REPORT differ, DESIGN wins (DESIGN section 15.2, line 902). No item in this phase commits: the DESIGN step 1.4a words "The first code commit" (line 911) are not run, because commits happen only when the user asks.

- [ ] **8.1 — Pre-flight: confirm every pre-implementation gate passed (L5)**
  - **Context**: BUILD-REQUEST "MANDATORY PHASE ORDER" items 2 and 3: the design fixes and the R5 HALT block every code task. The six gate files are `gate-decision.md` in each of `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/r3-b1/`, `qa/r3-b2/`, `qa/r3-b3/`, `qa/r4/`, `qa/r5/` and `qa/decisions/` (same task folder). The eight decision records, all under `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/`, are `OQ-1-agent-wait-decision.md`, `OQ-2-GQ-10-report-location-decision.md`, `OQ-3-GQ-11-rule-id-decision.md`, `OQ-4-GQ-35-409-pin-decision.md`, `OQ-5-GQ-61-window-decision.md`, `OQ-6-GQ-63-done-next-decision.md`, `OQ-7-D9-signoff-decision.md` and `OQ-8-run-id-decision.md`. Also `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/owner-decisions.md` and `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/discovery/1.0a-facts.md`. A `grep -L` alone passes when a file is missing, so each record is checked for existence and content.
  - **Action**: Run `grep -h 'gate: PASS' .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/r3-b1/gate-decision.md .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/r3-b2/gate-decision.md .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/r3-b3/gate-decision.md .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/r4/gate-decision.md .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/r5/gate-decision.md .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/decisions/gate-decision.md` (expect 6 lines). Then run `D=.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans; for f in OQ-1-agent-wait-decision.md OQ-2-GQ-10-report-location-decision.md OQ-3-GQ-11-rule-id-decision.md OQ-4-GQ-35-409-pin-decision.md OQ-5-GQ-61-window-decision.md OQ-6-GQ-63-done-next-decision.md OQ-7-D9-signoff-decision.md OQ-8-run-id-decision.md; do if test -f "$D/$f" && grep -q 'status: RESOLVED' "$D/$f"; then echo "OK $f"; else echo "MISSING-OR-UNRESOLVED $f"; fi; done` (expect 8 lines starting `OK`), and `test -s` on `owner-decisions.md` and `1.0a-facts.md` at the paths in Context (expect exit 0 each). Write every output and one PASS or FAIL line per check to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/impl-preflight.md`.
  - **Output**: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/impl-preflight.md`.
  - **Verification**: Verify: six gate PASS lines, eight `OK` lines (no `MISSING-OR-UNRESOLVED` line) and both `test -s` checks at exit 0. Otherwise apply the HALT rule with `blocker_reason: "Implementation pre-flight: gate or decision <name> not passed"` and stop before marking this item complete until the blocker is resolved.
  - **Completion gate**: The pre-flight record says PASS. Once done, mark this item as complete.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1423-1442

````markdown
- [ ] **8.2 — Step 1.1: create `src/superclaude/cli/sweep/__init__.py` (L2)**
  - **Context**: DESIGN section 7.1 (line 353): `__init__.__getattr__(name)` serves only `"sweep_group"`, so importing the package runs no seam and imports no `commands` module (test case DESIGN line 741). Pattern to copy: `src/superclaude/cli/recommend/__init__.py:12-20` (lazy `__getattr__` importing `from .commands import recommend_group`, else `AttributeError`, plus `__all__`).
  - **Action**: Create `src/superclaude/cli/sweep/__init__.py` with a one-line module docstring, `def __getattr__(name: str)` that returns `sweep_group` from `.commands` when `name == "sweep_group"` and otherwise raises `AttributeError(f"module {__name__!r} has no attribute {name!r}")`, and `__all__ = ["sweep_group"]`. Nothing else.
  - **Output**: `src/superclaude/cli/sweep/__init__.py`.
  - **Verification**: Verify: the file matches the recommend pattern line for line apart from names, and `uv run ruff check src/superclaude/cli/sweep/__init__.py` exits 0. Record the command and result in `### Phase 8 Findings` only when it fails.
  - **Completion gate**: The file exists and lints clean. Once done, mark this item as complete.

- [ ] **8.3 — Step 1.2: create `src/superclaude/cli/sweep/models.py`, with `ClassifiedRow` and the ten #409 dimensions (L2)**
  - **Context**: DESIGN section 7.2 (line 447), as revised by Phases 2 to 6: frozen dataclasses `SweepContext`, `SweepInput`, `OrcaObservation` (with `dispatch: str`, `run: str`, `session_join: str | None`, and the three R3-B1 fields `dispatch_started: datetime | None`, `dispatch_ended: datetime | None` and `dispatch_status: str | None`, parsed from the `worker-show` JSON paths `dispatch.dispatchedAt`, `dispatch.completedAt` and `dispatch.status`; all three are None for a row with no `worker-show` result, research/04:87), `ContractRecord`, `TranscriptTail` (with `first_record_ts: datetime | None` after `last_record_ts`, R3-B1, research/04:88), `TabMapEntry`, `SessionRow` (DESIGN line 459), `StatusParse`, `PackageRecord`, `WorktreeState`, `Classification`, `SafeToClose`, `SourceCoverage`, `SweepResult` (line 466), and the constants `JSON_SCHEMA_VERSION = 1`, `CLASSES` (8 names), `PACKAGE_STATES`, `SAFE_VALUES`. Live field names and the time format come from `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/discovery/1.0a-facts.md` (item 7.17); a fact still UNVERIFIED there keeps the DESIGN "behaviour until closed". research/09 Gap 2 gives the ten dimensions (REPORT:1245) and their values. Builder decisions (OQ-11 and OQ-14, not design facts): (1) `ClassifiedRow` is `row: SessionRow`, `classification: Classification`, `policy: str | None` (the `classify.policy_of` value, `"frozen"` or None), `safe: SafeToClose`, from the DESIGN line 466 words "row plus `Classification`, policy and `SafeToClose`" (research/09 Gap 2 "ClassifiedRow"); (2) `SessionRow` carries nine dimension fields, `lifecycle`, `phase`, `health`, `approval`, `freshness`, `result`, `admission`, `evidence_packet` (each `str = "unknown"`), `freshness_age_s: int | None = None` and `tests_review: str | None = None`; dimension 9 `policy` is not a `SessionRow` field and is printed from `ClassifiedRow.policy` (item 8.12), so the row holds no second copy of the freeze result.
  - **Action**: Create `src/superclaude/cli/sweep/models.py` with `from __future__ import annotations`, `dataclasses.dataclass(frozen=True)` classes and tuple-typed collections exactly as DESIGN section 7.2 lists them, plus `ClassifiedRow` and the dimension fields of decisions (1) and (2). Import only from the standard library (`dataclasses`, `datetime`, `pathlib`, `typing`). Add a one-line comment on `ClassifiedRow` and on the dimension block naming OQ-14 and OQ-11. The dimension fields are never JSON keys (DESIGN line 590 pins the v1 row key set).
  - **Output**: `src/superclaude/cli/sweep/models.py`.
  - **Verification**: Verify: every class and constant name in DESIGN section 7.2 appears once (`grep -c` per name); `grep -c 'dispatch_started: datetime | None'`, `grep -c 'dispatch_ended: datetime | None'`, `grep -c 'dispatch_status: str | None'` and `grep -c 'first_record_ts: datetime | None'` on `src/superclaude/cli/sweep/models.py` each return 1; `uv run python -c "import superclaude.cli.sweep.models"` exits 0; `uv run ruff check src/superclaude/cli/sweep/models.py` exits 0. If a DESIGN field cannot be typed from DESIGN or the 1.0a facts, log it in `### Phase 8 Findings` and stop before marking this item complete until it is settled.
  - **Completion gate**: The module imports and lints clean and holds every DESIGN 7.2 name. Once done, mark this item as complete.

- [ ] **8.4 — Step 1.3: create `src/superclaude/cli/sweep/classify.py`, the nine rules (L2, D9-gated)**
  - **Context**: Gate: OQ-7 (D9 sign-off) RESOLVED in `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/OQ-7-D9-signoff-decision.md` (item 7.11) and DESIGN open item 22 (line 990): "the classify step does not start until the owner signs off D9". DESIGN section 7.1 (classify signatures from line 353; `policy_of` at line 413) and section 7.2 (RULES order, the path A and path B joins, D9, the four guard cases, the observation rules) as revised by R3-B1 (time window: UTC parse; `first_record_ts`, cut to whole seconds, must lie from `dispatch_started` to `dispatch_ended`, both ends included, or to `collected_start` when `dispatch_ended` is None and `dispatch_status` is `pending` or `dispatched`; a row whose `dispatch_started` is None, or whose `dispatch_status` is anything else while `dispatch_ended` is None, has no observable window and gets the note `Dispatch time window not observable`, research/04:90), R3-B2 (unique-containing-window rule and the notes `conflict: one pane session matches several Dispatch rows` and `pane moved to a later session`) and R3-B3 (the `origin unknown:` notes). Signatures: `Rule(name, match)`, `RULES` in the order `blocked_contract`, `orca_exit_proof`, `fenced`, `waiting_signal`, `working`, `finished`, `idle`, `person_active`, `fallback`; `classify`, `policy_of`, `package_state`, `mark_shared_packages`, `safe_to_close`, `removable`, `classify_all`. NFR-004 (DESIGN line 739 AST case): no import of `subprocess`, `click`, `os` or `shutil`.
  - **Action**: If the OQ-7 record is not RESOLVED with D9 signed off, apply the HALT rule with `blocker_reason: "Step 1.3 blocked: D9 sign-off (OQ-7) not recorded"` and stop. Otherwise create `src/superclaude/cli/sweep/classify.py` as pure functions over `models` types, one `Rule` per DESIGN rule, the joins and notes with their exact DESIGN strings, and `classify_all` returning `SweepResult` whose `rows` are `ClassifiedRow(row, classification, policy_of(row), safe_to_close(...))`. Fill the nine `SessionRow` dimension fields only from the sources research/09 Gap 2 lists (REPORT:1248) that the row already carries; a dimension with no Phase 1 source (`phase`, `approval`, `admission`, `tests_review`) keeps its default. No clock read: every time comes from `SweepContext.now`.
  - **Output**: `src/superclaude/cli/sweep/classify.py`.
  - **Verification**: Verify: `grep -nE '^(import|from) ' src/superclaude/cli/sweep/classify.py` lists none of `subprocess`, `click`, `os`, `shutil`, `time`; the rule names in `RULES` appear in the DESIGN order; every note string DESIGN 7.2 and the R3 fixes quote appears byte-exact (`grep -F`); `uv run ruff check` on the file exits 0.
  - **Completion gate**: The module is written, pure and lint-clean. Once done, mark this item as complete.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1444-1463

````markdown
- [ ] **8.5 — Step 1.4a, code part: the git seam in `src/superclaude/cli/sweep/probes.py` (L2)**
  - **Context**: DESIGN step 1.4a (line 911) and sections 2.1 (line 39, GQ-103(1) lock-free git) and 7.3 (line 514): `ALLOWED_GIT = (("status", "--porcelain=v1", "-z", "--branch", "--untracked-files=all"),)`; `check_git_args(args)` raises `ValueError` for any args tuple not equal to an `ALLOWED_GIT` entry before any subprocess; `_git(cwd, *args, timeout)` builds `["git", "--no-optional-locks", "-C", str(cwd), *args]` and runs it with an env copy holding `GIT_OPTIONAL_LOCKS=0`; `GitCallFailed` is its error. research/05 summary point 3: the subprocess guard only catches calls made as `subprocess.run`, so probes calls `subprocess.run` through the module (`import subprocess`), never `from subprocess import run`. Output cap `OUTPUT_LIMIT` (8 MiB, DESIGN 7.3).
  - **Action**: Create `src/superclaude/cli/sweep/probes.py` holding only, for now, `import subprocess`, the `OUTPUT_LIMIT` constant, `ALLOWED_GIT`, `GitCallFailed`, `check_git_args` and `_git` as DESIGN states them (`capture_output=True`, `timeout=timeout`, `check=False`; non-zero exit, timeout or output over `OUTPUT_LIMIT` raise `GitCallFailed` with a reason). Item 8.10 adds the rest of the module.
  - **Output**: `src/superclaude/cli/sweep/probes.py` (git part).
  - **Verification**: Verify: `grep -n 'from subprocess' src/superclaude/cli/sweep/probes.py` prints nothing; `grep -n 'no-optional-locks\|GIT_OPTIONAL_LOCKS' src/superclaude/cli/sweep/probes.py` prints both; `uv run ruff check` on the file exits 0.
  - **Completion gate**: The git seam exists as DESIGN states. Once done, mark this item as complete.

- [ ] **8.6 — Step 1.4a: add `.dev/sweeps/` to `.gitignore` (L2)**
  - **Context**: DESIGN section 10 (line 710) as renumbered by R4 (item 5.2): two lines after `.gitignore:254` (`.dev/sprint-state/`, the end of the sprint-state block at :250-254). DESIGN line 942: the lines go into step 1.4a because the real-git test (item 8.9) copies the repository `.gitignore`. Expected text: `# superclaude sweep reports: dated, operator-local, never posted (WC-16). Never tracked.` then `.dev/sweeps/`.
  - **Action**: Read `.gitignore:245-260`, then insert the two DESIGN section 10 lines (as revised; WC-16, not WC-14) after the `.dev/sprint-state/` line, anchored by that quoted text. Do not touch any `.claude/` or `.dev/tasks/` rule.
  - **Output**: `.gitignore` (two added lines).
  - **Verification**: Verify: `git check-ignore -q .dev/sweeps/x.md; echo $?` prints 0 and `git check-ignore -q .dev/tasks/to-do/x.md; echo $?` prints 1; `git diff --stat -- .gitignore` shows 2 insertions. Write the outputs to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/gitignore-check.md`.
  - **Completion gate**: Both check-ignore results match. Once done, mark this item as complete.

- [ ] **8.7 — Create `tests/sweep/__init__.py` (L2)**
  - **Context**: research/05 section 3 ("Does `tests/sweep/` need `__init__.py`? Yes."): pytest runs with `rootdir` imports, and test module basenames such as `test_readonly.py` must not collide with other test folders. BUILD-REQUEST TESTING_REQUIREMENTS: "`tests/sweep/__init__.py` is required."
  - **Action**: Create `tests/sweep/__init__.py` as an empty file.
  - **Output**: `tests/sweep/__init__.py`.
  - **Verification**: Verify: `test -f tests/sweep/__init__.py` exits 0.
  - **Completion gate**: The file exists. Once done, mark this item as complete.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1465-1491

````markdown
- [ ] **8.8 — Step 1.8 base part: `tests/sweep/conftest.py` with the subprocess guard and the seam fakes (L2)**
  - **Context**: DESIGN section 11 (lines 728-733): `patch_orca` and `patch_git` replace `probes._orca` and `probes._git` with fakes that record every argv and return fixture data, as `tests/cli/reflect/conftest.py` does; an autouse fixture patches `subprocess.run`, `subprocess.Popen` and `os.system` to raise `AssertionError`, stepping aside only for the one test carrying the `integration` marker (registered at `pyproject.toml:119`, `--strict-markers`); a fixed `now`; a `tmp_path` layout with `HOME` and `XDG_STATE_HOME` inside it. research/05 section 2 and summary point 3: the superclaude plugin adds `integration` to every test whose absolute path contains `/integration/` (`src/superclaude/pytest_plugin.py:216-222`), so the guard must read only the test function's own decorator marks: `any(m.name == "integration" for m in getattr(request.function, "pytestmark", []))`, never `request.node.get_closest_marker`. This item is placed before item 8.9 because the step 1.4a test needs these fakes (research/01 summary gap). `probes._orca` does not exist until item 8.10, so `patch_orca` uses `monkeypatch.setattr(probes, "_orca", fake, raising=False)`; item 10.1 adds the fixture files and the rest of the layout.
  - **Action**: Read `tests/cli/reflect/conftest.py` in chunks of at most 150 lines for the fake-recording shape. Create `tests/sweep/conftest.py` with: the autouse guard fixture `no_subprocess(request, monkeypatch)` using the own-marks check above; `patch_git` (records `(cwd, args, timeout)` and the env the real `_git` would build, returns canned porcelain bytes per worktree); `patch_orca` (records argv, returns canned `OrcaResult`-shaped data once item 8.10 lands); `fixed_now` (a timezone-aware UTC `datetime`); `sweep_home` (sets `HOME` and `XDG_STATE_HOME` under `tmp_path` with `monkeypatch.setenv`).
  - **Output**: `tests/sweep/conftest.py`.
  - **Verification**: Verify: `grep -n 'get_closest_marker' tests/sweep/conftest.py` prints nothing and `grep -n 'pytestmark' tests/sweep/conftest.py` prints the guard line; `uv run ruff check tests/sweep/conftest.py` exits 0.
  - **Completion gate**: The conftest exists with the guard and the two fakes. Once done, mark this item as complete.

- [ ] **8.9 — Step 1.4a test part: `tests/sweep/test_readonly.py` (recorded argv, env, the real-git test) and run it (L2 then L3)**
  - **Context**: DESIGN section 11 line 737, "Step 1.4a part": every recorded `_git` argv has `--no-optional-locks` at index 1 and `-C <path>` after it; the child env holds `GIT_OPTIONAL_LOCKS=0`; one git argv per discovered worktree; one `integration`-marked real-git test in a `tmp_path` repository with the four SPEC assertions (control; `check-ignore` of `.dev/sweeps/x.md` succeeds; of `.dev/tasks/to-do/x.md` fails; a file under `.dev/sweeps/` leaves `git status --porcelain` unchanged). BUILD-REQUEST: "The real-git test copies the repo `.gitignore`." Real-git precedent: `tests/pr_submit/test_conflict_scripts.py:46` (`GIT = shutil.which("git")`) and `:48-64` (`_FIXED_IDENTITY`, `_base_env` with `HOME` at :63). Until item 8.10 adds `collect`, "one git argv per discovered worktree" is tested by calling `_git` once per path in a two-worktree list built by the test; item 10.4 re-points it at `collect`.
  - **Action**: Create `tests/sweep/test_readonly.py` with: (1) a test that monkeypatches `probes.subprocess.run` with a recorder (inside the test, after the guard) and asserts argv index 1 is `--no-optional-locks`, index 2 is `-C`, index 3 is the path, and `env["GIT_OPTIONAL_LOCKS"] == "0"`; (2) a test that `check_git_args` raises `ValueError` for `("rev-parse",)` and passes the `ALLOWED_GIT` entry; (3) the per-worktree count test; (4) `@pytest.mark.integration` plus `@pytest.mark.skipif(shutil.which("git") is None, ...)` real-git test: `git init` in `tmp_path`, copy the repository `.gitignore` (found from `Path(__file__).resolve().parents[2] / ".gitignore"`) into it, run the four assertions with a fixed identity env, all through `subprocess.run` (allowed because the test carries its own marker). Then run `uv run pytest tests/sweep -v` and save stdout to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/step-1.4a-pytest.txt`.
  - **Output**: `tests/sweep/test_readonly.py` and `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/step-1.4a-pytest.txt`.
  - **Verification**: Verify: the run exits 0 with the integration test PASSED (not skipped) when git is present; a deliberate check that the guard works: the saved output shows no test reaching a real subprocess except the marked one. On a failure, fix the code or test, re-run, and log each re-run in `### Phase 8 Findings`.
  - **Completion gate**: `uv run pytest tests/sweep -v` passes and the output is saved. Once done, mark this item as complete.

- [ ] **8.10 — Step 1.4: the rest of `src/superclaude/cli/sweep/probes.py` (L2)**
  - **Context**: Gate: step 1.0a facts (item 7.17) and item 8.9 passed. DESIGN section 7.1 probes signatures (from line 353): `Budget(shows=50, total_s=90.0, per_call_s=10.0, clock=time.monotonic)` with `share_shows`, `take_show`, `call_timeout`, `cut`; `OrcaResult(kind, data, reason)` with kinds `ok`, `no_binding`, `unavailable`, `call_failed`; `BindingError`; `orca_binary()` (`$ORCA_CLI_COMMAND` when set, else `ORCA_BINARY_DEFAULT = "orca-ide"`); `check_orca_argv`; `_orca(*args, timeout)`; `bind_run(budget)`; `collect(ctx, runs, root, budget)`; readers `read_worktree`, `parse_status`, `read_packages`, `read_ledger`, `read_contract`, `read_transcript_tail`, `read_tab_map`, `read_orca_version`. DESIGN section 7.3 (line 514): `ALLOWED_ORCA` (exactly 8 templates), `FORBIDDEN_TOKENS = frozenset({"--include-remote", "--agent-wait"})` (unchanged by the R5 decision, item 6.3), `ORCA_VERSION_FILE`, `CONTRACT_LIMIT = LEDGER_LIMIT` 1 MiB, `LEDGER_SPLIT` 512 KiB, `TRANSCRIPT_TAIL` 256 KiB, `WORKER_LIST_PAGE` 100 (or the page size the 1.0a facts record); a limit is hit only when the size is over it. The FR-021 forbidden verb list lives only in the test (item 10.3). From the 1.0a facts: the field names, the time format, `RUN_ID_RE`, `DISPATCH_ID_RE`, the cursor field. Readers return data plus a `SourceCoverage` row and never raise past `collect` (DESIGN line 392). `--include-remote` timing is dropped (DESIGN line 912).
  - **Action**: Append these names to `src/superclaude/cli/sweep/probes.py` in DESIGN order. `_orca` calls `check_orca_argv` before `subprocess.run` (through the module), caps output at `OUTPUT_LIMIT`, and maps results to `OrcaResult` kinds as DESIGN states. Every path a reader opens is re-resolved and rejected with `unscanned: outside root` when it escapes. No write, no lock, no network.
  - **Output**: `src/superclaude/cli/sweep/probes.py` (complete).
  - **Verification**: Verify: `grep -c` finds each DESIGN 7.1 probes name and 7.3 constant; a count of `ALLOWED_ORCA` entries is 8; `grep -nE 'open\([^)]*["'"'"'](w|a|x)' src/superclaude/cli/sweep/probes.py` prints nothing; `uv run ruff check` on the file exits 0.
  - **Completion gate**: probes.py holds every DESIGN name and opens nothing for writing. Once done, mark this item as complete.

- [ ] **8.11 — Re-run the sweep tests after step 1.4 (L3)**
  - **Context**: Items 8.5 to 8.10. The step 1.4a tests must still pass now that `probes.py` is complete; `patch_orca` now targets a real `_orca`.
  - **Action**: In `tests/sweep/conftest.py`, remove the `raising=False` argument from the `monkeypatch.setattr(probes, "_orca", fake, raising=False)` call in the `patch_orca` fixture (item 8.8), so the default `raising=True` applies, anchored by that quoted call; change nothing else in the file. Then run `uv run pytest tests/sweep -v` and save stdout to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/step-1.4-pytest.txt`.
  - **Output**: the edited `tests/sweep/conftest.py` and `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/step-1.4-pytest.txt`.
  - **Verification**: Verify: `grep -n 'raising=False' tests/sweep/conftest.py` prints nothing; `grep -n 'setattr(probes, "_orca"' tests/sweep/conftest.py` prints the `patch_orca` line; the pytest run exits 0. On a failure, fix the code, re-run, and log each re-run in `### Phase 8 Findings`.
  - **Completion gate**: The run passes. Once done, mark this item as complete.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1493-1505

````markdown
- [ ] **8.12 — Step 1.5: create `src/superclaude/cli/sweep/report.py` (L2)**
  - **Context**: Gates: OQ-4 (GQ-35, #409 layout pin), OQ-5 (GQ-61, window) and OQ-6 (GQ-63) RESOLVED (items 7.5 to 7.10). DESIGN sections 7.1 (report signatures: `CHECKED_ORCA_VERSION = "1.4.245"` at line 424, `CELL_MAX = 200`, `SECTIONS` with 12 functions, `sanitize`, `cell`, `render`, `to_json`), 7.4 (line 554, JSON v1 schema and the pinned key set at line 590), 7.5 (line 592, layout: headings `## Source coverage` to `## What I could not determine`, the empty-section string, a cell cut to 200 characters ending `...`, the `next inspection` map, last line `Report complete`) and D1 (no `write_report`; publication lives in `commands._publish`, DESIGN line 88). Every `SECTIONS` function is pure over `SweepResult` (line 594). The Sessions table starts with the ten #409 dimensions (DESIGN line 634): nine from `SessionRow`, and dimension 9 `policy` printed as `frozen` when `ClassifiedRow.policy == "frozen"`, else `unknown`, never `not frozen` (OQ-11; DESIGN line 740 forbids a `not frozen` claim from a source loss). The dimensions are not JSON keys (research/09 Gap 2). The `next inspection` map has no stop, retry, release, merge or removal word.
  - **Action**: Create `src/superclaude/cli/sweep/report.py` importing only `json`, `re`, `unicodedata` (if needed) and `models`, with the names above in DESIGN order. `sanitize` neutralises `|`, ANSI escapes, bidi controls, HTML tags and Markdown links so the column count holds; `to_json` emits the v1 key set exactly, with zero counts present and `waiting` lists of ids only.
  - **Output**: `src/superclaude/cli/sweep/report.py`.
  - **Verification**: Verify: `grep -nE '^(import|from) ' src/superclaude/cli/sweep/report.py` lists none of `subprocess`, `click`, `os`, `shutil`, `time`, `datetime.now`; `grep -n 'write_report' src/superclaude/cli/sweep/report.py` prints nothing; `grep -niE '\b(stop|retry|release|merge|remov)' src/superclaude/cli/sweep/report.py` prints only lines that are not user-facing text (log each hit and why in `### Phase 8 Findings`); `uv run ruff check` on the file exits 0.
  - **Completion gate**: report.py is pure and holds every DESIGN name. Once done, mark this item as complete.

- [ ] **8.13 — Validation after Phase 8 (L3)**
  - **Context**: BUILD-REQUEST VALIDATION_REQUIREMENTS: a validation item after each implementation phase. Files of items 8.2 to 8.12.
  - **Action**: Run, in order, `uv run ruff check src/superclaude/cli/sweep tests/sweep`, `uv run ruff format --check src/superclaude/cli/sweep tests/sweep`, `uv run python -c "import superclaude.cli.sweep.classify, superclaude.cli.sweep.probes, superclaude.cli.sweep.report"` and `uv run pytest tests/sweep -v`. Write each command, exit code and the last 30 output lines to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/phase8-validation.md`, with one PASS or FAIL line each.
  - **Output**: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/phase8-validation.md`.
  - **Verification**: Verify: four PASS lines. On a FAIL, fix (a format failure is fixed with `uv run ruff format` on the named files only), re-run, and log each re-run in `### Phase 8 Findings`.
  - **Completion gate**: All four checks PASS. Once done, mark this item as complete.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1621-1649

````markdown
## Phase 9: CLI shell, steps 1.6 and 1.7, the step 1.4 live check, and the impl-cli gate

- [ ] **9.1 — Step 1.6: create `src/superclaude/cli/sweep/commands.py` (L2)**
  - **Context**: Gates: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/impl-core/gate-decision.md` PASS; OQ-2 (GQ-10, report location, `--output` default) and OQ-5 (GQ-61, `--window` default) RESOLVED. DESIGN section 7.1 commands signatures (lines 433-445): `sweep_group: click.Group` named `sweep`; `run(run_ids, window, root, output)` for `sweep run`; `_parse_window` (FR-003, `click.UsageError`, exit 2); `_find_root` (FR-004 walk, plain stat only); `_check_output` (FR-004 containment); `_check_run_ids` (regex from step 1.0a, `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/discovery/1.0a-facts.md`, deduplicated); `_publish(text, output_dir, now)`. Exit mapping (line 445): `click.UsageError` and `BindingError` exit 2 with the message; `ValueError` from an allowlist check, any other exception and every `_publish` failure exit 1 with a `[sweep <stage>]` stderr prefix; only `commands.run` calls `sys.exit`. DESIGN section 3.2 (lines 99-130), the seven `_publish` steps: stem `now.strftime("%Y%m%d-%H%M%S") + "-sweep"`; `os.makedirs(output_dir, exist_ok=True)` then re-resolve inside `<root>/.dev/sweeps/` (else `[sweep publish] output dir escaped <root>/.dev/sweeps/`); `os.open(output_dir / f".{stem}.{os.getpid()}.tmp", O_WRONLY | O_CREAT | O_EXCL, 0o666)`; write every byte, `os.fsync`, `os.close`; `os.link` to `stem.md`, then `stem-2.md` to `stem-99.md`, `FileExistsError` moving on, the first success being the commit point; none left gives `[sweep publish] report name space exhausted: <dir>`; then `os.unlink(tmp)`, failing with `[sweep publish] could not remove temp file <path>` and exit 1. The error table (lines 121-129) and the section 3.4 exit-1 rule (line 153) apply. DESIGN step 1.6 (line 914): no `run-list` fallback; `--output` default `<root>/.dev/sweeps/`. `_publish` runs only after every exit-2 check, `collect`, `classify_all` and `render` succeed (line 103). The six `[sweep publish]` messages in DESIGN section 3.2 (lines 106-128) are: `[sweep publish] output dir escaped <root>/.dev/sweeps/` (step 2), `[sweep publish] report name space exhausted: <dir>` (step 6), `[sweep publish] <error>` (`makedirs` fails), `[sweep publish] temp file exists: <path>` (`O_EXCL` fails), `[sweep publish] cannot link report: <error>` (`os.link` fails with anything but `FileExistsError`) and `[sweep publish] could not remove temp file <path>` (unlink after the commit point). Link-and-fsync precedents (research/02 section on atomic writes): the `os.link` plus `FileExistsError` handling at `src/superclaude/cli/sprint/recovery.py:424-434` (link at :433) and the `os.fsync` step at `src/superclaude/cli/swarm/atomic.py:28-31`; neither is a reusable helper (both use other names or `os.replace`), so `_publish` is written fresh.
  - **Action**: Create `src/superclaude/cli/sweep/commands.py` with the Click group and the `run` subcommand (options `--run` repeatable, `--window`, `--root`, `--output`, defaults from the OQ-2 and OQ-5 records), the five helpers and `_publish` exactly as above, printing one success JSON object (from `report.to_json`) on stdout after `_publish` returns. `_publish` is the only function that writes. No retry, no lock, no `os.rename`, no `os.replace`.
  - **Output**: `src/superclaude/cli/sweep/commands.py`.
  - **Verification**: Verify: `grep -nE 'os\.(rename|replace)|run-list' src/superclaude/cli/sweep/commands.py` prints nothing; `grep -c 'sys.exit' src/superclaude/cli/sweep/commands.py` hits only inside `run`; each fixed part of the six `[sweep publish]` messages listed in Context is found with `grep -F` in `src/superclaude/cli/sweep/commands.py`: `output dir escaped`, `report name space exhausted:`, `temp file exists:`, `cannot link report:` and `could not remove temp file` (one hit each at least), and the `makedirs` message `[sweep publish] <error>` is checked by reading the `makedirs` error branch and recording its line in `### Phase 9 Findings`; `uv run ruff check src/superclaude/cli/sweep/commands.py` exits 0.
  - **Completion gate**: commands.py matches DESIGN 3.2 and 7.1. Once done, mark this item as complete.

- [ ] **9.2 — Step 1.7: register `sweep_group` in `src/superclaude/cli/main.py` (L2)**
  - **Context**: research/08 section 3(c): the last deferred registration is `src/superclaude/cli/main.py:563` (import) and `:565` (`main.add_command(issue_watch_group, name="issue-watch")`); `if __name__ == "__main__":` is at `:568`; the sweep pair goes after line 565, not 561 (DESIGN step 1.7, as re-anchored by item 5.6). Pattern: `main.py:563-565`, the import line carrying `# noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports`.
  - **Action**: Read `src/superclaude/cli/main.py:555-569`. After the line `main.add_command(issue_watch_group, name="issue-watch")`, anchored by that quoted text, insert a blank line, `from superclaude.cli.sweep import sweep_group  # noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports`, a blank line and `main.add_command(sweep_group, name="sweep")`.
  - **Output**: `src/superclaude/cli/main.py` (4 added lines).
  - **Verification**: Verify: `uv run superclaude sweep --help` and `uv run superclaude sweep run --help` exit 0 and list `run` and the four options; `git diff --stat -- src/superclaude/cli/main.py` shows 4 insertions and 0 deletions. Save the help outputs to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/step-1.7-help.txt`.
  - **Completion gate**: Both help commands exit 0. Once done, mark this item as complete.

- [ ] **9.3 — Step 1.4 live check against the OQ-8 Run (L3, live, read-only)**
  - **Context**: DESIGN step 1.4 (line 912): "Live check saved to `.dev/tasks/<pkg>/artifacts/sweep-live-check-1.4.json`; no `--include-remote` timing". The check runs here, not in Phase 8, because `superclaude sweep run` exists only after items 9.1 and 9.2. research/09 Gap 3: the design gives no pass rule; the only one is REPORT:1247: record each worker's state, then run the sweep once through Bash with timeout 120000 ms; "Pass = exit 0, the probe calls finish inside the 90 s budget, every row carries a class, each recorded worker gets the class its recorded state maps to under step 1.3 (could not determine where step 1.3 says so), and no row is could not determine because of a probe error or timeout." The Run id is the one in `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/OQ-8-run-id-decision.md` (item 7.15). Only allowlisted reads: the `worker-list` template, which DESIGN section 7.3 (line 523) and `ALLOWED_ORCA` in `src/superclaude/cli/sweep/probes.py` hold as `("orchestration", "worker-list", "--run", "<run>", "--json")`, run with the binary `orca-ide` (`ORCA_CLI_COMMAND` is unset at build time, research/09 Gap 3; if `ORCA_CLI_COMMAND` is set when this item runs, use its value as the binary instead); never `--include-remote`, `--agent-wait`, `worker-read`, `gate-list`, `check` or `inbox`. The run writes one report under `<root>/.dev/sweeps/`, which item 8.6 gitignores.
  - **Action**: (0) Run `grep -n '"worker-list"' src/superclaude/cli/sweep/probes.py` and confirm the `ALLOWED_ORCA` entry is `("orchestration", "worker-list", "--run", "<run>", "--json")`; if it differs, apply the HALT rule before any live call with `blocker_reason: "Step 1.4 live check: ALLOWED_ORCA worker-list entry differs from DESIGN 7.3"`. (1) Run exactly `orca-ide orchestration worker-list --run <id> --json` (Bash timeout 30000 ms; when `ORCA_CLI_COMMAND` is set, the same argv after its value in place of `orca-ide`), with `<id>` the Run id from the OQ-8 record, and save its JSON to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/sweep-live-check-1.4-workers.json`. (2) Run `uv run superclaude sweep run --run <id>` through Bash with timeout 120000 and save stdout to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/sweep-live-check-1.4.json`, plus exit code, stderr and wall time to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/sweep-live-check-1.4.md`. (3) Read the report at `report_path` in chunks of at most 150 lines and write, in the `.md` record, one line per recorded worker: worker id, recorded state, expected class under step 1.3, reported class, match yes or no. (4) Write the five REPORT:1247 pass conditions with PASS or FAIL each.
  - **Output**: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/sweep-live-check-1.4.json`, `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/sweep-live-check-1.4-workers.json`, `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/sweep-live-check-1.4.md`.
  - **Verification**: Verify: the `.md` record quotes the exact step (1) command, and its argv after the binary equals the `ALLOWED_ORCA` entry with `<run>` filled (`orchestration worker-list --run <id> --json`, nothing added); all five conditions PASS. If Orca is unavailable or the Run no longer exists, apply the HALT rule with `blocker_reason: "Step 1.4 live check: Run <id> not readable (<reason>); the person names another Run (OQ-8)"` and stop before marking this item complete until the blocker is resolved. A condition that FAILs because of the code is fixed in `probes.py`, `classify.py` or `commands.py`, the 9.4 validation is re-run, and this item is re-run; log each re-run in `### Phase 9 Findings`.
  - **Completion gate**: The live check record shows five PASS lines. Once done, mark this item as complete.

- [ ] **9.4 — Validation after Phase 9 (L3)**
  - **Context**: BUILD-REQUEST VALIDATION_REQUIREMENTS. Files of items 9.1 and 9.2.
  - **Action**: Run, in order, `uv run ruff check src/superclaude/cli tests/sweep`, `uv run ruff format --check src/superclaude/cli/sweep src/superclaude/cli/main.py tests/sweep`, `uv run superclaude sweep --help` and `uv run pytest tests/sweep tests/unit -v`. Write each command, exit code and the last 30 output lines to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/phase9-validation.md`, with one PASS or FAIL line each.
  - **Output**: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/phase9-validation.md`.
  - **Verification**: Verify: four PASS lines. On a FAIL, fix, re-run, and log each re-run in `### Phase 9 Findings`.
  - **Completion gate**: All four checks PASS. Once done, mark this item as complete.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1772-1795

````markdown
## Phase 10: Sweep tests, steps 1.8 to 1.13, and the tests gate

Every test runs with the seams patched; none starts Orca, ccsession or Claude (DESIGN section 11, line 726, NFR-013). The case lists live in the DESIGN section 11 table (lines 735-745 on the unrevised design) and, after Phases 2 to 4, also include the R3-B1 (6 plus 4), R3-B2 (7) and R3-B3 (3) fixtures those phases added to sections 11 and 12. Each test item reads its DESIGN row in full, writes one test (or one parametrized case) per listed case, and records in its result file which DESIGN case each test name covers.

- [ ] **10.1 — Step 1.8 rest: extend `tests/sweep/conftest.py` and add the fixture files (L2)**
  - **Context**: DESIGN section 11 lines 728-733: the `tmp_path` layout holds packages, contracts, transcripts and a ccsession `orca-tabs/` folder; fixtures copied from captured Orca output keep their source name, hand-made ones carry `synthetic` in the file name. Captured fixtures already exist from item 7.18 (`tests/sweep/fixtures/captured-*.json` plus `SOURCES.md`). Base fixtures from item 8.8: the guard, `patch_orca`, `patch_git`, `fixed_now`, `sweep_home`.
  - **Action**: Add to `tests/sweep/conftest.py` a `sweep_root` fixture that builds, under `tmp_path`, a root with `.dev/tasks/to-do/<pkg>/` packages (with `progress.md` ledgers and worker contracts), transcripts under `HOME`, and an `orca-tabs/` map under `XDG_STATE_HOME`, with small builder helpers the tests call. Hand-made fixture files form a closed set: read `tests/sweep/fixtures/SOURCES.md`, and for each of the eight `ALLOWED_ORCA` templates that has no `captured-` file there, write exactly one file with the name from this list: `synthetic-run-current.txt` (template 1, plain output), `synthetic-worker-list.json` (2), `synthetic-worker-show.json` (3), `synthetic-task-list-ready.json` (4), `synthetic-task-list.json` (5), `synthetic-worktree-ps.json` (6), `synthetic-worktree-list.json` (7) and `synthetic-worktree-current.json` (8). Shape each from the DESIGN section 7.2 field names and `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/discovery/1.0a-facts.md`, and add one `SOURCES.md` row per file naming the template and "hand-made, synthetic". Every other variant a test needs (a malformed body, the quoted-marker negative, an empty `run-current` body, byte-boundary inputs, the `orca-tabs/` entries) is built in memory or under `tmp_path` by the builder helpers, never as a file under `tests/sweep/fixtures/`. Do not edit the captured files.
  - **Output**: `tests/sweep/conftest.py` (extended); the `synthetic-*` files from the list above for exactly the templates `SOURCES.md` shows as not captured (none when all eight were captured); `tests/sweep/fixtures/SOURCES.md` with one row per new file.
  - **Verification**: Verify: `ls tests/sweep/fixtures/` shows only `captured-*` files, `SOURCES.md` and names from the eight-name list above; each `synthetic-*` file's template has no `captured-` file; each `synthetic-*` file has a `SOURCES.md` row; every `synthetic-*.json` file parses with `uv run python -c "import json,sys; [json.load(open(p)) for p in sys.argv[1:]]" tests/sweep/fixtures/synthetic-*.json` (skip when there is none); `uv run pytest tests/sweep -v` still passes.
  - **Completion gate**: The layout fixture exists and the existing tests pass. Once done, mark this item as complete.

- [ ] **10.2 — Step 1.9: create `tests/sweep/test_classify.py` (L2 then L3)**
  - **Context**: DESIGN section 11 line 739 (`test_classify.py` row: FR-006 to FR-010, FR-012 to FR-015, NFR-010, NFR-004, D9, WC-13, M6, M9, and the full case list from "One parametrized case per rule 1 to 9" through "AST import test that `classify.py` and `report.py` import none of `subprocess`, `click`, `os`, `shutil`"), plus the R3-B1 time-window fixtures, the R3-B2 several-Dispatch-rows fixtures and the R3-B3 FR-010 fixtures (outage, full page, `call_failed`, with the `origin unknown:` notes) as revised in DESIGN sections 11 and 12. Module under test: `src/superclaude/cli/sweep/classify.py` (item 8.4).
  - **Action**: Create `tests/sweep/test_classify.py` covering every case in that row and the R3 fixtures, using `fixed_now` and builders from `conftest.py`, asserting class names and note strings byte-exact. The AST test parses `classify.py` and `report.py` with `ast` and checks their imports. Run `uv run pytest tests/sweep/test_classify.py -v` and save stdout to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/test-classify.txt`, followed by a case-to-test map.
  - **Output**: `tests/sweep/test_classify.py` and `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/test-classify.txt`.
  - **Verification**: Verify: exit 0, and the map lists every DESIGN case with a test name. A test that exposes a code bug is fixed in the code, not weakened; log each fix in `### Phase 10 Findings`.
  - **Completion gate**: The tests pass and the map is complete. Once done, mark this item as complete.

- [ ] **10.3 — Step 1.10: create `tests/sweep/test_probes_allowlist.py` (L2 then L3)**
  - **Context**: DESIGN section 11 line 738 (`test_probes_allowlist.py` row: full-sweep recording; argv[0] from `$ORCA_CLI_COMMAND`, else `orca-ide`; zero argv for `worktree list` and `worktree current`; exact-set pin of the eight templates; negatives raising `ValueError` before a subprocess (`check`, `inbox`, `worker-read`, `gate-list`, an extra flag, `--include-remote`, `--agent-wait`, `run-list`); the FR-021 forbidden list held in the test; git negatives (`rev-parse`, `log`, `branch`, `--version`, any `stash` form); result classes; the budget cases; the nine byte-boundary fixtures; the failure modes; the `parse_status` M7 cases). The captured no-binding fixture case is gated on step 1.0a (`.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/discovery/1.0a-facts.md`). Module under test: `src/superclaude/cli/sweep/probes.py`.
  - **Action**: Create `tests/sweep/test_probes_allowlist.py` covering every case in the row, with the FR-021 forbidden verb list written as a literal in the test file (DESIGN 7.3: it lives only in the test). Budget tests inject a fake `clock`. Run `uv run pytest tests/sweep/test_probes_allowlist.py -v` and save stdout plus a case-to-test map to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/test-probes-allowlist.txt`.
  - **Output**: `tests/sweep/test_probes_allowlist.py` and `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/test-probes-allowlist.txt`.
  - **Verification**: Verify: exit 0, the map is complete, and no test waits on a real clock (full-timeout fakes finish under 120 s per DESIGN). A test that exposes a code bug is fixed in the code; log each fix in `### Phase 10 Findings`.
  - **Completion gate**: The tests pass and the map is complete. Once done, mark this item as complete.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1797-1823

````markdown
- [ ] **10.4 — Step 1.11: extend `tests/sweep/test_readonly.py` with the NFR-001 snapshot diff and NFR-013 (L2 then L3)**
  - **Context**: DESIGN section 11 line 737, "Step 1.11 part": the snapshot diff (path, size, `st_mtime_ns`, SHA-256) over the root, `HOME` and the XDG dirs gives exactly one added report file plus the output directory when new; no temp file and no second name for the report remain after exit 0. Item 8.9 created the file; its per-worktree count test is now re-pointed at `probes.collect` with `patch_git`. NFR-013: no live Orca, ccsession or Claude launch.
  - **Action**: Add to `tests/sweep/test_readonly.py`: a `snapshot(paths)` helper (walk with `os.walk`, record path, size, `st_mtime_ns`, SHA-256); a test that snapshots `sweep_root`, `HOME` and the XDG dirs, invokes `superclaude sweep run` through `click.testing.CliRunner` with `patch_orca` and `patch_git`, snapshots again and asserts the diff is exactly the report (plus `.dev/sweeps/` when new) and no `.tmp` file; the re-pointed per-worktree test. Run `uv run pytest tests/sweep/test_readonly.py -v` and save stdout to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/test-readonly.txt`.
  - **Output**: `tests/sweep/test_readonly.py` (extended) and `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/test-readonly.txt`.
  - **Verification**: Verify: exit 0 and the real-git integration test still PASSED. Log any code fix in `### Phase 10 Findings`.
  - **Completion gate**: The tests pass. Once done, mark this item as complete.

- [ ] **10.5 — Step 1.12: create `tests/sweep/test_report.py` (L2 then L3)**
  - **Context**: DESIGN section 11 line 740 (`test_report.py` row: heading order equals section 7.5; the (a) sort and (b) no question text; the injection fixture; the 300-character cell; render twice gives equal bytes; the source-loss fixture; the version lines for `1.4.245-aidev02.780594c521aa`, `1.4.246` and a missing file; the `bound_reached` line; the SP-24 footnote; the empty-section string; the `next inspection` map; rule 6 wording without `admitted` or `accepted`; remote coverage; the WC-13 row; the SP-16 literal; the D9 `origin not proved` note; the last line `Report complete`). Builder decisions under test: the ten dimensions appear as Sessions-table columns and not as JSON keys; dimension 9 prints `frozen` or `unknown`, never `not frozen` (OQ-11, item 8.12). The layout follows the OQ-4 (GQ-35) and OQ-6 (GQ-63) records. Module under test: `src/superclaude/cli/sweep/report.py`.
  - **Action**: Create `tests/sweep/test_report.py` covering every case in the row plus the two builder-decision cases. Run `uv run pytest tests/sweep/test_report.py -v` and save stdout plus a case-to-test map to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/test-report.txt`.
  - **Output**: `tests/sweep/test_report.py` and `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/test-report.txt`.
  - **Verification**: Verify: exit 0 and the map is complete. Log any code fix in `### Phase 10 Findings`.
  - **Completion gate**: The tests pass and the map is complete. Once done, mark this item as complete.

- [ ] **10.6 — Step 1.13: create `tests/sweep/test_cli_registration.py` (L2 then L3)**
  - **Context**: DESIGN section 11 line 741: `superclaude sweep --help` and `sweep run --help` exit 0 under `CliRunner`; importing `superclaude.cli.sweep` records no seam call and does not import `commands` until `sweep_group` is read (FR-001, NFR-006). Registration at `src/superclaude/cli/main.py` after the issue-watch pair (item 9.2).
  - **Action**: Create `tests/sweep/test_cli_registration.py` with: the two help tests through `CliRunner` on `superclaude.cli.main.main`; a lazy-import test that removes `superclaude.cli.sweep` and `superclaude.cli.sweep.commands` from `sys.modules` (via `monkeypatch.delitem(..., raising=False)`), imports the package, asserts `superclaude.cli.sweep.commands` is not in `sys.modules` and the seam fakes recorded nothing, then reads `sweep_group` and asserts it is a `click.Group`. Run `uv run pytest tests/sweep/test_cli_registration.py -v` and save stdout to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/test-cli-registration.txt`.
  - **Output**: `tests/sweep/test_cli_registration.py` and `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/test-cli-registration.txt`.
  - **Verification**: Verify: exit 0. Log any code fix in `### Phase 10 Findings`.
  - **Completion gate**: The tests pass. Once done, mark this item as complete.

- [ ] **10.7 — Step 1.13: create `tests/sweep/test_cli_contract.py` (L2 then L3)**
  - **Context**: DESIGN section 11 line 742 (`test_cli_contract.py` row: run id cases `""`, `'r;x'`, duplicate, unknown-Run then R2; the three binding tests and the fourth gated on 1.0a; disk-only continuation printing `unscanned: orca unavailable`; the FR-003 parser cases; the FR-004 output and root cases; the FR-005 fixture (4 rows, 2 worktrees, `(4/4)`) and the reconciliation equalities; the golden v1 key set; zero counts; `waiting` lists of ids; two runs with one `now` giving `stem.md` and `stem-2.md`; one test per exit code; the section 3 publication cases including `os.unlink` patched to raise after a successful `os.link` and the `[sweep publish] could not remove temp file <path>` line; an earlier report byte-identical afterwards). Module under test: `src/superclaude/cli/sweep/commands.py` (`_publish` per DESIGN section 3.2).
  - **Action**: Create `tests/sweep/test_cli_contract.py` covering every case in the row, using `CliRunner`, `patch_orca`, `patch_git`, `sweep_root` and `monkeypatch.setattr` on `os.link`, `os.unlink`, `os.write` and `os.makedirs` inside `commands` for the publication failures. Run `uv run pytest tests/sweep/test_cli_contract.py -v` and save stdout plus a case-to-test map to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/test-cli-contract.txt`.
  - **Output**: `tests/sweep/test_cli_contract.py` and `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/test-cli-contract.txt`.
  - **Verification**: Verify: exit 0 and the map is complete. Log any code fix in `### Phase 10 Findings`.
  - **Completion gate**: The tests pass and the map is complete. Once done, mark this item as complete.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:1946-1976

````markdown
## Phase 11: Command and skill surface, steps 1.14 to 1.16 and 1.20, and the cmd-skill gate

These two primitives are installed to `~/.claude/` and run in other projects, so neither may name a `src/superclaude/` path (DESIGN 7.6 opening, NFR-011; project CLAUDE.md "Never Hardcode `src/superclaude/` Paths in Installed Primitives"). Edit only the `src/superclaude/` side; `make sync-dev` (item 14.1) makes the `.claude/` copies, which are never staged. Routing row R5 (item 11.2) lands directly after `sweep.md` is created (item 11.1), before any later test run, because creating `sweep.md` makes `tests/recommend/test_routing_refresh.py` fail until `"sweep"` is in `_POST_REFRESH_ADDITIONS` (research/03 ordering constraint 2). Phase 11 is closed by its own cmd-skill gate (items 11.6 to 11.21); the docs gate at the end of Phase 13 re-reads these files together with the Phase 12 and 13 changes.

- [ ] **11.1 — Step 1.14: create `src/superclaude/commands/sweep.md` (L2)**
  - **Context**: DESIGN section 7.6 "**Command**" bullets (anchor the quoted heading `### 7.6 Command and skill surface`; lines 644-648 on the unrevised design). Pattern files: `src/superclaude/commands/issue.md` (title `# /sc:issue: ...` at :12, `## Triggers` :23, `## Usage` :27, `## Options` :34) and `src/superclaude/commands/graph.md` (`allowed-tools: Skill, ...` at :9, `## Activation` at :41-46 with "**MANDATORY**: Before executing any protocol steps, invoke:" and "> Skill sc:graph-protocol"). Skill frontmatter name form: `src/superclaude/skills/sc-graph-protocol/SKILL.md:2` (`name: sc:graph-protocol`). Option defaults: the OQ-2 (`--output`) and OQ-5 (`--window`) records in `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/` and `src/superclaude/cli/sweep/commands.py` (item 9.1).
  - **Action**: Create `src/superclaude/commands/sweep.md` with frontmatter `name: sweep`, a one-line description (no stop, retry, release, merge or removal wording), `allowed-tools: Skill` and `argument-hint: "[--run <id>]... [--window <N>h|<N>d] [--root <dir>] [--output <dir>]"`. Body: `# /sc:sweep: ...` title; `## Triggers` (explicit only: the coordinator on every wake, or the person); `## Usage`; `## Options` (one row per option with the defaults from `commands.py`); `## Activation` in the `graph.md` form invoking `Skill sc:sweep-protocol`, naming `~/.claude/skills/sc-sweep-protocol/SKILL.md` as the installed skill and the project `.claude/skills/sc-sweep-protocol/SKILL.md` copy as the dual surface (skills read `~/.claude/skills/` first). No `## Unattended mode` heading, no `--unattended` flag. One line states `/sc:sweep` is coordinator or person only and is on the never-as-worker list (`~/.claude/WORKER-CONTRACT.md`).
  - **Output**: `src/superclaude/commands/sweep.md`.
  - **Verification**: Verify: `grep -c 'src/superclaude' src/superclaude/commands/sweep.md` prints 0; `grep -n '^## Unattended mode\|--unattended' src/superclaude/commands/sweep.md` prints nothing; `grep -nF '~/.claude/skills/sc-sweep-protocol/SKILL.md' src/superclaude/commands/sweep.md` prints a line in the Activation block (the installed surface), and `grep -nP '(?<!~/)\.claude/skills/sc-sweep-protocol/SKILL\.md' src/superclaude/commands/sweep.md` prints a line in the Activation block (the project copy; the lookbehind rejects the installed path, so the installed path alone cannot satisfy this check). Record the output in `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/step-1.14-checks.md`.
  - **Completion gate**: The file exists and every check holds. Once done, mark this item as complete.

- [ ] **11.2 — Step 1.20, routing row R5: add `"sweep"` to `_POST_REFRESH_ADDITIONS` (L2 then L3)**
  - **Context**: DESIGN section 9 row R5 (line 698 on the unrevised design). `tests/recommend/test_routing_refresh.py:33` is `_POST_REFRESH_ADDITIONS = {"graph", "impact", "issue"}`; the assertion that uses it is at :648 (`assert shipped - _POST_REFRESH_ADDITIONS == active`). DESIGN 15.2 gates step 1.20 on step 1.14 (item 11.1), because the shipped command set now contains `sweep`. research/03 ordering constraint 2 (`research/03-integration-points.md:109`): R5 lands no later than the step that creates `sweep.md`, because the new `sweep.md` file, not the guide, trips the :648 assertion. This item therefore runs directly after item 11.1, and no item between them runs a test.
  - **Action**: Re-read `tests/recommend/test_routing_refresh.py:30-36` at HEAD. Replace the quoted line `_POST_REFRESH_ADDITIONS = {"graph", "impact", "issue"}` with `_POST_REFRESH_ADDITIONS = {"graph", "impact", "issue", "sweep"}`. No other edit. Run `uv run pytest tests/recommend/test_routing_refresh.py -v` and save stdout to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/r5-routing-refresh.txt`.
  - **Output**: the edited `tests/recommend/test_routing_refresh.py` and `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/r5-routing-refresh.txt`.
  - **Verification**: Verify: exit 0 and `git diff --stat -- tests/recommend/test_routing_refresh.py` shows 1 insertion and 1 deletion. On a failure that names another command, log it in `### Phase 11 Findings` and HALT with `blocker_reason: "R5 routing-refresh test fails on a command other than sweep"`; stop before marking this item complete until the blocker is resolved.
  - **Completion gate**: The test passes. Once done, mark this item as complete.

- [ ] **11.3 — Step 1.15: create `src/superclaude/skills/sc-sweep-protocol/SKILL.md` (L2, gated on OQ-6)**
  - **Context**: DESIGN section 7.6 "**Skill**" bullets (lines 650-655 on the unrevised design): `allowed-tools: Bash(superclaude sweep run:*), Bash(uv run --frozen --no-sync superclaude sweep run:*), Read`; steps (1) to (5); no recommendation, no proposed action, no edit, stage or delete. Frontmatter pattern: `src/superclaude/skills/sc-graph-protocol/SKILL.md:1-11` (`name:`, `description:`, `allowed-tools:`, then the extended-metadata HTML comment). The DONE / NEXT output style follows `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/OQ-6-GQ-63-done-next-decision.md` (items 7.9 and 7.10; GQ-63 has no recommendation). Permission syntax: the design's `:*` form is kept (Open Question OQ-9).
  - **Action**: Read the OQ-6 record; if it is not `status: RESOLVED`, apply the HALT rule with `blocker_reason: "Step 1.15 needs OQ-6 (GQ-63) resolved"` and STOP. Otherwise create the skill directory and `SKILL.md` with `name: sc:sweep-protocol`, a one-line description, the `allowed-tools` literal exactly as DESIGN 7.6 states, and a body with the five numbered steps: (1) run `superclaude sweep run <args>` with Bash timeout 120000; (2) only when step 1 fails with "command not found", run `uv run --frozen --no-sync superclaude sweep run <args>` with timeout 120000; (3) on exit 0, parse stdout JSON and take only `report_path` and `summary`, then Read the report at `report_path` in chunks of at most 150 lines; (4) print the `summary` counts and the report path, in the form the OQ-6 record chose; (5) on exit 1 or 2, print the stderr line and stop. A `## Boundaries` section says the skill recommends nothing, proposes no action and never edits, stages or deletes a file. The text must not contain the words stop, retry, release, merge or removal as advice (step 5 "stop" is the skill halting, so phrase it "end the run" to keep the test simple).
  - **Output**: `src/superclaude/skills/sc-sweep-protocol/SKILL.md`.
  - **Verification**: Verify: `grep -c 'src/superclaude' src/superclaude/skills/sc-sweep-protocol/SKILL.md` prints 0; `grep -n '^allowed-tools: Bash(superclaude sweep run:\*), Bash(uv run --frozen --no-sync superclaude sweep run:\*), Read$' src/superclaude/skills/sc-sweep-protocol/SKILL.md` prints one line; `grep -n '120000' ...` prints two lines; `grep -niw 'stop\|retry\|release\|merge\|removal' src/superclaude/skills/sc-sweep-protocol/SKILL.md` prints nothing. Record the output in `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/step-1.15-checks.md`.
  - **Completion gate**: The file exists and every check holds. Once done, mark this item as complete.

- [ ] **11.4 — Step 1.16: create `tests/commands/test_sweep_command.py` (L2 then L3)**
  - **Context**: DESIGN section 7.6 "**Test**" bullet (line 657 on the unrevised design) lists every assertion. Pattern: `tests/commands/test_graph_command.py:11-19` (`_REPO = Path(__file__).resolve().parents[2]`, `_COMMAND`, `_SKILL` paths, pure file-content assertions, CI-safe). Files under test: `src/superclaude/commands/sweep.md` (item 11.1) and `src/superclaude/skills/sc-sweep-protocol/SKILL.md` (item 11.3).
  - **Action**: Create `tests/commands/test_sweep_command.py` with a module docstring in the `test_graph_command.py` style and one test per assertion: the command `allowed-tools: Skill` literal and the skill `allowed-tools` literal, exactly; the two surfaces inside the `## Activation` block (slice the text from that heading to the next `## `), as two separate assertions: the installed path `~/.claude/skills/sc-sweep-protocol/SKILL.md` as a plain substring, and the project copy with `re.search(r"(?<!~/)\.claude/skills/sc-sweep-protocol/SKILL\.md", activation)`, so the installed path alone cannot satisfy the project-copy assertion; the PATH-first order (the index of `superclaude sweep run` step 1 is before the `uv run --frozen --no-sync` step) and the `command not found` trigger; `--no-sync` and `--frozen` in the fallback literal; `120000`; no `## Unattended mode` heading in `sweep.md`; no `src/superclaude/` substring in either file; and a word-boundary regex test that the skill text has none of stop, retry, release, merge, removal. Run `uv run pytest tests/commands/test_sweep_command.py -v` and save stdout to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/test-sweep-command.txt`.
  - **Output**: `tests/commands/test_sweep_command.py` and `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/test-sweep-command.txt`.
  - **Verification**: Verify: exit 0 and one test per DESIGN 7.6 assertion. A failure is fixed in the primitive, not by weakening the test; log each fix in `### Phase 11 Findings`.
  - **Completion gate**: The tests pass. Once done, mark this item as complete.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:2099-2129

````markdown
## Phase 12: Contract rule WC-16, steps 1.17 to 1.19 and routing row R7, and the contract gate

DESIGN section 8 (as revised by design fix R4 in Phase 5) is the source of every text in this phase. The rule is WC-16, never WC-14: master `5dc29d23` already has WC-14 and WC-15 (PR #434), and a second `"WC-14"` key in the `RULE_PHRASES` dict literal would silently replace the worker WC-14 entry (research/07 section (d)). The existing WC-14 references at `WORKER-CONTRACT.md` :124, :213 and :289 mean the worker rule and are not touched. The `### Liveness supervision` lines :110 ("The sweep.") and :151 (L1 probe row) are not reworded; they are pinned by `RULE_PHRASES["liveness-sweep-and-states"]` and `["liveness-ladder-and-restart"]` (`tests/skills/test_worker_contract.py:209-219`, :228-237). No item here runs or implements the WC-9 lock retry (IronbellyOrg/IronClaude#446). Phase 12 is closed by its own contract gate (items 12.6 to 12.21, folder `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/contract/`) before Phase 13 builds the R2 bullet on WC-16.

- [ ] **12.1 — Step 1.17: insert `### WC-16. Coordinator loop` into `src/superclaude/core/WORKER-CONTRACT.md` (L2)**
  - **Context**: Gates: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/OQ-3-GQ-11-rule-id-decision.md` (items 7.3 and 7.4) must be `status: RESOLVED` with option (a), and `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/pr422-409-check.md` (item 7.19) must exist; DESIGN section 8 "**Gate.**" paragraph. Placement: after the `### Fan-in rule (several workers, then one merge)` paragraph (heading at `WORKER-CONTRACT.md:271`, paragraph at :273) and before `### Worked example: gate hit, answer, new Task` (:275) (research/07 summary). Text: the fenced `### WC-16. Coordinator loop` block in DESIGN section 8 "**Final text.**" as revised in Phase 5, including the alignment with the 5-minute sweep bound at contract :110 that design fix R4 wrote. Test constraints (research/07 section (e)): `_check_rule` (`test_worker_contract.py:755-762`) needs the ident on the heading line; `_check_repo_setup_gated` (:813-828) fails on a code span starting with `uv`, `make`, `bash` and similar, so the paragraph names `` `/sc:sweep` `` only and never `` `uv run superclaude sweep run` ``.
  - **Action**: Read both gate files; if either gate fails, apply the HALT rule with `blocker_reason: "Step 1.17 needs OQ-3 resolved to WC-16 and the 1.16a record"` and STOP. Re-read `src/superclaude/core/WORKER-CONTRACT.md:265-280` at HEAD and confirm the two quoted headings. Re-read DESIGN section 8 (anchor the quoted heading that begins `## 8. WC-16`) and copy the fenced rule text byte-for-byte. Insert it, with one blank line before and after, between the fan-in paragraph (anchor its quoted last sentence "the coordinator reports the single admitted result, or the failure, to the person.") and the quoted `### Worked example: gate hit, answer, new Task` heading.
  - **Output**: the edited `src/superclaude/core/WORKER-CONTRACT.md` and `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/step-1.17-checks.md`.
  - **Verification**: Verify: `grep -n '^### WC-16. Coordinator loop$' src/superclaude/core/WORKER-CONTRACT.md` prints one line between the two headings; `grep -c '^### WC-14' src/superclaude/core/WORKER-CONTRACT.md` is unchanged from `git show HEAD:src/superclaude/core/WORKER-CONTRACT.md | grep -c '^### WC-14'`; `git diff -U0 -- src/superclaude/core/WORKER-CONTRACT.md` shows only added lines; the four pin phrases `WC-16. Coordinator loop`, `On every coordinator wake`, `it is never posted`, `It never stops watching on its own` each occur in the inserted text. If DESIGN section 8 drops one of those phrases, log it in `### Phase 12 Findings` and use the phrases the revised DESIGN pins instead. Write the outputs to the checks file.
  - **Completion gate**: The rule is in place and every check holds. Once done, mark this item as complete.

- [ ] **12.2 — Step 1.18: add `/sc:sweep` to the never-as-worker list at `WORKER-CONTRACT.md:23` (L2)**
  - **Context**: DESIGN section 8 "**Never-as-worker addition.**" (line 684 on the unrevised design): only the command list changes, giving "`/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn`, `/sc:sweep` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while ...". `WORKER-CONTRACT.md:23` is still byte-identical to the old base (research/07 citation row for :23). `_check_never_as_worker` (`tests/skills/test_worker_contract.py:765`) needs the term line to stay one line.
  - **Action**: Re-read `src/superclaude/core/WORKER-CONTRACT.md:20-26` at HEAD. Replace the quoted fragment `` `/sc:spawn` and `/sc:swarm-wizard`, plus `/sc:pr-submit` `` on line 23 with `` `/sc:spawn`, `/sc:sweep` and `/sc:swarm-wizard`, plus `/sc:pr-submit` ``. Nothing else on the line changes.
  - **Output**: the edited `src/superclaude/core/WORKER-CONTRACT.md`.
  - **Verification**: Verify: `grep -c 'Never-as-worker list' src/superclaude/core/WORKER-CONTRACT.md` is unchanged; `grep -n '`/sc:spawn`, `/sc:sweep` and `/sc:swarm-wizard`' src/superclaude/core/WORKER-CONTRACT.md` prints line 23; the line has no line break inside it.
  - **Completion gate**: Line 23 carries `/sc:sweep`. Once done, mark this item as complete.

- [ ] **12.3 — Step 1.19: the five contract-test pin edits in `tests/skills/test_worker_contract.py` (L2 then L3)**
  - **Context**: DESIGN section 8 "**Pins**" (as revised by design fix R4) and research/07 sections (d) and (e). Current anchors, re-read at HEAD before each edit: `RULE_PHRASES = {` at :25; the `"never-as-worker"` entry at :86-92 with its phrase at :89-90; `"WC-15"` at :165-172 and `"heartbeats"` at :173; `NEVER_AS_WORKER = (` at :382-391 (8 entries, last `"/sc:pr-submit"`); `def test_never_as_worker_list_names_all_seven_commands():` at :912; `assert "load" not in UNATTENDED_COMMANDS` at :1322. Unchanged by design: `UNATTENDED_EXPECT` (:438) stays at 31 entries checked by `_check_p2_set` (:1556); the equality assertion at :837 holds because `sweep.md` has no `## Unattended mode`.
  - **Action**: Make exactly these five edits, each anchored by quoted text: (1) insert after the `"WC-15"` entry and before `"heartbeats": (` the entry `"WC-16": ("WC-16", ["WC-16. Coordinator loop", "On every coordinator wake", "it is never posted", "It never stops watching on its own"]),` formatted like the WC-15 entry (phrases as the revised DESIGN pins them); (2) change the `"never-as-worker"` phrase string at :89 from `` "`/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, " `` to `` "`/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn`, `/sc:sweep` and `/sc:swarm-wizard`, " ``, splitting the literal across two adjacent strings if `ruff format` needs the line shorter; (3) add `"/sc:sweep",` to `NEVER_AS_WORKER` after `"/sc:pr-submit",`, giving 9 entries; (4) rename `test_never_as_worker_list_names_all_seven_commands` to `test_never_as_worker_list_names_every_listed_command`, body unchanged; (5) add `    assert "sweep" not in UNATTENDED_COMMANDS` on the line after `    assert "load" not in UNATTENDED_COMMANDS`. Then run `grep -nE 'git (add|commit|push|merge|stash|update-ref|worktree (add|remove))|gh (pr|api)' src/superclaude/commands/sweep.md src/superclaude/skills/sc-sweep-protocol/SKILL.md`; if it prints a line, add a `WRITE_VERB_CLASSIFICATION` row with category `never-worker` for it (research/07 section (e): table at :2016-3126, categories at :1953-1955), otherwise record that no row is needed. Run `uv run pytest tests/skills/test_worker_contract.py -v` and save stdout to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/step-1.19-pytest.txt`.
  - **Output**: the edited `tests/skills/test_worker_contract.py` and `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/step-1.19-pytest.txt`.
  - **Verification**: Verify: exit 0; `grep -c '"WC-14": (' tests/skills/test_worker_contract.py` is 1 and `grep -c '"WC-16": (' ...` is 1; `test_contract_states_rule[WC-16]`, `test_contract_states_rule[never-as-worker]` and the parametrized removal case for `/sc:sweep` appear as PASSED; `grep -c 'names_all_seven_commands' tests/skills/test_worker_contract.py` is 0. A failure is fixed in the contract or the pin, never by deleting a pin; log each fix in `### Phase 12 Findings`.
  - **Completion gate**: The five edits are in place and the file passes. Once done, mark this item as complete.

- [ ] **12.4 — Step 1.24a, routing row R7: add `/sc:sweep` to the developer-guide copy of the list (L2)**
  - **Context**: DESIGN section 9 row R7 (line 700 on the unrevised design); DESIGN 15.2 orders step 1.24a after step 1.18 (item 12.2). `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:991` reads "- The never-as-worker list (`~/.claude/WORKER-CONTRACT.md`, section 1): `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while decision D3 keeps it off workers. ...".
  - **Action**: Re-read lines 988-994 at HEAD. Replace the quoted fragment `` `/sc:spawn` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while decision D3 `` with `` `/sc:spawn`, `/sc:sweep` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while decision D3 ``. No other edit.
  - **Output**: the edited developer guide and `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/r7-check.md` holding the before and after line and the line-23 contract text side by side.
  - **Verification**: Verify: the command order in the guide line equals the order in `WORKER-CONTRACT.md:23`; `git diff --stat` on the guide shows 1 insertion and 1 deletion.
  - **Completion gate**: The two lists match. Once done, mark this item as complete.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:2252-2275

````markdown
## Phase 13: Routing and documentation rows R1 to R4, R6 and R8, `.gitignore` check, and the docs gate

All row texts come from DESIGN section 9 as revised in Phase 5 (WC-16, not WC-14). The anchors below are CONFIRMED on `5dc29d23` by research/08 section 3 (a) and re-read for this build. R2 is applied before R1 so R2's anchor is not shifted by R1 (BUILD-REQUEST phase order item 4); every edit is still anchored by quoted text. R1, R2 and R3 belong together: editing R1 or R2 without R3 fails `tests/commands/test_routing_plugin_parity.py:38` (DESIGN 9 rules). The level table is not touched, so the `src/superclaude/core/CLAUDE.md` level-table copy needs no re-run. R1 and R6 avoid the words stop, retry, release, merge and removal. The report-location text `.dev/sweeps/` follows the OQ-2 (GQ-10) record; if OQ-2 chose another location, use that location in every row of this phase and log it in `### Phase 13 Findings`.

- [ ] **13.1 — Routing row R2: add the coordinator-sweep bullet to `## Orca coordination` (L2)**
  - **Context**: DESIGN section 9 row R2 (line 695 on the unrevised design). `src/superclaude/core/HOW-WE-WORK.md:396` `## Orca coordination`; :403 the bullet that begins "- **Some commands are never workers.**"; :404 the bullet that begins "- **Orca creates the worktrees.**". research/08 section 3 (d): master has no sweep or wake text in the guide, so the bullet duplicates nothing.
  - **Action**: Re-read `src/superclaude/core/HOW-WE-WORK.md:396-405` at HEAD. Insert one new line directly after the quoted line "- **Some commands are never workers.** `/sc:pr-submit` and the other commands on the never-as-worker list in `~/.claude/WORKER-CONTRACT.md` stay with the coordinator or the person." and before "- **Orca creates the worktrees.**": the R2 bullet from the revised DESIGN (item 5.2 aligned it with master's 5-minute sweep bound at `src/superclaude/core/WORKER-CONTRACT.md:110`), which reads "- **The coordinator sweeps on every wake, at most once every 5 minutes.** WC-16 in `~/.claude/WORKER-CONTRACT.md` has the coordinator run `/sc:sweep` and read its report before it acts. The sweep is read-only and is itself never a worker." If the revised DESIGN R2 bullet differs from this text, copy the DESIGN text and log the difference in `### Phase 13 Findings`.
  - **Output**: the edited `src/superclaude/core/HOW-WE-WORK.md`.
  - **Verification**: Verify: `grep -n 'The coordinator sweeps on every wake, at most once every 5 minutes\.' src/superclaude/core/HOW-WE-WORK.md` prints line 404; `grep -c 'sweeps on every wake\.\*\*' src/superclaude/core/HOW-WE-WORK.md` is 0; `grep -c 'WC-14' ` on the new line is 0; `grep -c 'src/superclaude'` on the new line is 0.
  - **Completion gate**: The bullet is in place. Once done, mark this item as complete.

- [ ] **13.2 — Routing row R1: add the `/sc:sweep` row to the other-commands table (L2)**
  - **Context**: DESIGN section 9 row R1 (line 694 on the unrevised design). `src/superclaude/core/HOW-WE-WORK.md:318` `<!-- other-commands:v1 -->`, header at :320-321, the `/sc:spawn` row at :333 (begins "| `/sc:spawn` | Requested decomposition with"), blank line :334, closing prose :335, `<!-- /other-commands -->` :337. R2 (item 13.1) is below this table, so these lines are unchanged.
  - **Action**: Re-read `src/superclaude/core/HOW-WE-WORK.md:316-338` at HEAD. Insert directly after the quoted `/sc:spawn` row the line "| `/sc:sweep` | Read-only supervision snapshot of the bound Orca Run, its worktrees and person-started sessions. Writes one dated report under `.dev/sweeps/` and prints JSON; it changes nothing else and recommends nothing. Coordinator or person only, never a worker. |" (the revised DESIGN R1 text).
  - **Output**: the edited `src/superclaude/core/HOW-WE-WORK.md`.
  - **Verification**: Verify: `grep -n '^| `/sc:sweep` |' src/superclaude/core/HOW-WE-WORK.md` prints line 334, between the two table markers; `grep -niwE 'stop|retry|release|merge|removal'` on that line prints nothing.
  - **Completion gate**: The row is in place. Once done, mark this item as complete.

- [ ] **13.3 — Routing row R4: add `"sc:sweep"` to `_OTHER_COMMANDS` (L2)**
  - **Context**: DESIGN section 9 row R4 (line 697 on the unrevised design). `tests/core/test_how_we_work_routing_table.py:27` `_OTHER_COMMANDS = {` (entries from :28, `"sc:spawn"` at :33).
  - **Action**: Re-read lines 24-45 at HEAD. Insert `    "sc:sweep",` on the line after the quoted `    "sc:spawn",`. No other edit.
  - **Output**: the edited `tests/core/test_how_we_work_routing_table.py`.
  - **Verification**: Verify: `git diff --stat -- tests/core/test_how_we_work_routing_table.py` shows 1 insertion; `uv run pytest tests/core/test_how_we_work_routing_table.py -v` exits 0 (save stdout to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/r1-r4-routing-table.txt`).
  - **Completion gate**: The test passes. Once done, mark this item as complete.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:2277-2303

````markdown
- [ ] **13.4 — Routing row R3: byte-copy the guide to the plugin refs copy (L2 then L3)**
  - **Context**: DESIGN section 9 row R3; project CLAUDE.md "Key Documentation Files" (copy `HOW-WE-WORK.md` byte-for-byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`); parity test `tests/commands/test_routing_plugin_parity.py:38` (`filecmp.cmp(..., shallow=False)`). research/08 section 3 (b): the two files were identical on `5dc29d23`.
  - **Action**: Run `cp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, then `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md; echo "exit=$?"` and `uv run pytest tests/commands/test_routing_plugin_parity.py -v`. Save both outputs to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/r3-parity.txt`.
  - **Output**: the updated plugin copy and `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/r3-parity.txt`.
  - **Verification**: Verify: `cmp` prints nothing with `exit=0`, the parity test exits 0, and `git diff --stat -- plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` shows exactly 2 insertions (the R1 row and the R2 bullet).
  - **Completion gate**: The files are byte-identical and the test passes. Once done, mark this item as complete.

- [ ] **13.5 — Routing row R6: add the `/sc:sweep` row to the user guide (L2)**
  - **Context**: DESIGN section 9 row R6 (line 699 on the unrevised design). `docs/user-guide/commands.md:105` `### 8. UTILITIES`; table header :107-108 (`| Command | Purpose | File | Changes files? |`); the `/sc:issue` row at :115 (begins "| [`/sc:issue`](#scissue---github-issue-claim-and-create) |"); `/sc:recommend` at :116. research/08 section 2.4: :115 text changed in place on master, position unchanged.
  - **Action**: Re-read lines 105-118 at HEAD. Insert after the quoted `/sc:issue` row the line "| `/sc:sweep` | Read-only snapshot of a Run, its worktrees and person sessions | `sweep.md` | Report only (writes `.dev/sweeps/`) |".
  - **Output**: the edited `docs/user-guide/commands.md`.
  - **Verification**: Verify: the new row is line 116 with four cells; `grep -niwE 'stop|retry|release|merge|removal'` on it prints nothing; `git diff --stat` shows 1 insertion.
  - **Completion gate**: The row is in place. Once done, mark this item as complete.

- [ ] **13.6 — Step 1.24b, routing row R8: add the CHANGELOG entry (L2)**
  - **Context**: DESIGN section 9 row R8 (line 701 on the unrevised design) lists the contents: `superclaude sweep run`, `/sc:sweep`, `sc-sweep-protocol`, WC-16, `.dev/sweeps/` ignored. Style (research/08 section 3 (a) R8): under `CHANGELOG.md:5` `## [Unreleased]`, a topic heading `### <title>` (first at :7, `### ccsession: a shim never forwards to another shim`) with `#### Added (<topic>)` sub-headings (:19); there is no bare `### Added`. DESIGN 15.2 orders step 1.24b after step 1.16 (item 11.4).
  - **Action**: Re-read `CHANGELOG.md:1-22` at HEAD. Insert, after the quoted `## [Unreleased]` line and its blank line and before the quoted `### ccsession: a shim never forwards to another shim`, the block: `### sweep: read-only supervision snapshot (Phase 1)`, blank line, `#### Added (sweep)`, blank line, then bullets naming `superclaude sweep run` (read-only, one dated report plus JSON), the `/sc:sweep` command and the `sc-sweep-protocol` skill, the WC-16 coordinator-loop rule and `/sc:sweep` on the never-as-worker list, `.dev/sweeps/` added to `.gitignore`, and the tests (`tests/sweep/`, `tests/commands/test_sweep_command.py`), then one blank line. Use only facts already true in the tree; the bullets must not use the words stop, retry, release, merge or removal as advice.
  - **Output**: the edited `CHANGELOG.md`.
  - **Verification**: Verify: `grep -n '^### sweep: read-only supervision snapshot (Phase 1)$' CHANGELOG.md` prints line 7; `grep -n '^#### Added (sweep)$' CHANGELOG.md` prints one line; `grep -c 'WC-14' ` on the inserted block is 0.
  - **Completion gate**: The entry is in place. Once done, mark this item as complete.

- [ ] **13.7 — Check the `.gitignore` entry and the docs (L3)**
  - **Context**: Item 8.6 added `.dev/sweeps/` to `.gitignore` after `.dev/sprint-state/` (:254); `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/gitignore-check.md`. `.dev/tasks/` must stay tracked (project CLAUDE.md "`.dev/tasks/` Is Always Staged").
  - **Action**: Run `git check-ignore -v .dev/sweeps/x.md; echo "exit=$?"` (expect exit 0), `git check-ignore -v .dev/tasks/x.md; echo "exit=$?"` (expect exit 1) and `grep -n 'WC-14' .gitignore` (expect no hit in the sweep comment). Append the outputs to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/gitignore-check.md`.
  - **Output**: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/gitignore-check.md` (appended).
  - **Verification**: Verify: the three expectations hold. On a miss, fix `.gitignore`, re-run and log it in `### Phase 13 Findings`.
  - **Completion gate**: The three checks hold. Once done, mark this item as complete.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:2433-2463

````markdown
## Phase 14: Final validation, step 1.28 grep, step 1.29 pipx check, final QA gate, fidelity gate, diff file, POST reflect, Done

No item in this phase commits, pushes or merges. The only staging is `git add .dev/tasks` in item 14.49. The PR is opened later, outside this task, only via `/sc:pr-submit --monitor 3` with every gh command carrying `--repo IronbellyOrg/IronClaude`. No item runs or implements the WC-9 lock retry (IronbellyOrg/IronClaude#446).

- [ ] **14.1 — Validation: `make sync-dev`, `make verify-sync` and the `.claude/` staging check (L3)**
  - **Context**: BUILD-REQUEST VALIDATION_REQUIREMENTS; project CLAUDE.md "Never Stage or Commit `.claude/` Contents" (only `.claude/settings.json` may be staged) and "Component Sync" (`make sync-dev` copies `src/superclaude/{skills,agents,commands,hooks,templates}` to `.claude/`; `make verify-sync` checks both sides). Phases 11 to 13 added `src/superclaude/commands/sweep.md` and `src/superclaude/skills/sc-sweep-protocol/SKILL.md` and edited `src/superclaude/core/WORKER-CONTRACT.md` and `src/superclaude/core/HOW-WE-WORK.md`.
  - **Action**: Run `make sync-dev`, then `make verify-sync`, then `git diff --cached --name-only -- .claude/` and `git status --short -- .claude/`. Write each command, its exit code and its last 30 output lines to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/phase14-sync.md`, with one PASS or FAIL line each. Pass: both make targets exit 0; the cached list holds no path other than `.claude/settings.json`. Do not stage anything in this item.
  - **Output**: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/phase14-sync.md`.
  - **Verification**: Verify: four PASS lines. If a `.claude/` path other than `settings.json` is staged, run `git restore --staged -- <that path>` (index-only, the file is kept), re-run the check and log it in `### Phase 14 Findings`. On a sync FAIL, fix the `src/superclaude/` side, re-run and log each re-run.
  - **Completion gate**: All four checks PASS. Once done, mark this item as complete.

- [ ] **14.2 — Validation: `make lint`, `uv run ruff check .` and `uv run ruff format --check src/ tests/` (L3)**
  - **Context**: BUILD-REQUEST VALIDATION_REQUIREMENTS. New Python files: `src/superclaude/cli/sweep/` (six modules), `tests/sweep/`, `tests/commands/test_sweep_command.py`; edited: `src/superclaude/cli/main.py`, `tests/skills/test_worker_contract.py`, `tests/core/test_how_we_work_routing_table.py`, `tests/recommend/test_routing_refresh.py`.
  - **Action**: Run the three commands in order. Write each command, exit code and last 30 output lines to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/phase14-lint.md` with one PASS or FAIL line each.
  - **Output**: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/phase14-lint.md`.
  - **Verification**: Verify: three PASS lines (exit 0). On a FAIL in a file this task created or edited, fix it (for format, `uv run ruff format <that file>` on that file only), re-run all three and log each re-run in `### Phase 14 Findings`. A FAIL only in a file this task did not touch (compare `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/baseline-git-status.txt`) is logged as a pre-existing finding and does not fail this item.
  - **Completion gate**: Three PASS lines, or only pre-existing failures logged. Once done, mark this item as complete.

- [ ] **14.3 — Validation: the scoped test run (L3)**
  - **Context**: BUILD-REQUEST VALIDATION_REQUIREMENTS: `uv run pytest tests/sweep tests/commands tests/core tests/skills tests/recommend`. No test may launch Orca, ccsession or Claude (the `tests/sweep/conftest.py` guard from item 8.8 blocks real subprocess calls except under the test's own `integration` marker).
  - **Action**: Run `uv run pytest tests/sweep tests/commands tests/core tests/skills tests/recommend -v`. Write the command, exit code, the pass/fail/skip counts and the last 40 output lines to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/phase14-scoped-pytest.md` with one PASS or FAIL line.
  - **Output**: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/phase14-scoped-pytest.md`.
  - **Verification**: Verify: exit 0 and 0 failed. On a FAIL, fix the cause in this task's files, re-run and log each re-run in `### Phase 14 Findings`.
  - **Completion gate**: The scoped run PASSes. Once done, mark this item as complete.

- [ ] **14.4 — Validation: the full test run (L3)**
  - **Context**: BUILD-REQUEST VALIDATION_REQUIREMENTS: the full `uv run pytest` after the scoped run; `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/baseline-git-status.txt` (item 1.3) is the tree before this task.
  - **Action**: Run `uv run pytest` with a Bash timeout of 600000 ms (run it in the background and wait if it needs longer). Write the command, exit code, counts and the list of failing test ids to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/phase14-full-pytest.md` with one PASS or FAIL line.
  - **Output**: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/phase14-full-pytest.md`.
  - **Verification**: Verify: exit 0. For each failing test, decide from `git stash`-free evidence (does the failing test import or read a file this task changed? `git diff --stat $(cat .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/base-commit.txt)`) whether this task caused it; fix every task-caused failure and re-run; record any failure not caused by this task as pre-existing in `### Phase 14 Findings` with its test id and reason.
  - **Completion gate**: The full run PASSes, or every remaining failure is logged as pre-existing with evidence. Once done, mark this item as complete.
````

### .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:2465-2491

````markdown
- [ ] **14.5 — Step 1.28: the scoped primitive-path grep and the full-tree count (L3)**
  - **Context**: DESIGN step 1.28 (near DESIGN line 939, "every hit justified"); research/09-gap-fill.md Gap 3 "1.28, the primitive-path grep" (research/09:117-125): the full command gave 168 hits at `5dc29d23` (commands 18, skills 132, agents 9, core 0, hooks 9); the scoped form must return no output; the full-tree count must stay 168. Project CLAUDE.md "Never Hardcode `src/superclaude/` Paths in Installed Primitives".
  - **Action**: Run `grep -rn 'src/superclaude' src/superclaude/commands/sweep.md src/superclaude/skills/sc-sweep-protocol/ src/superclaude/core/WORKER-CONTRACT.md src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md; echo "exit=$?"` and `grep -rn 'src/superclaude' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core src/superclaude/hooks | wc -l`. Write both commands and outputs to `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/step-1.28-grep.md` with one PASS or FAIL line each.
  - **Output**: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/step-1.28-grep.md`.
  - **Verification**: Verify: the scoped grep prints nothing and `exit=1` (0 hits); the full count is 168. If item 1.3 recorded a base other than `5dc29d23`, re-run the full count at that base reading only (`git grep -n 'src/superclaude' $(cat .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/base-commit.txt) -- src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core src/superclaude/hooks | wc -l`) and compare against that number instead. On a hit, replace it with the installed `~/.claude/...` path (dual surface where a lookup needs it), run `make sync-dev`, re-run this item and log it in `### Phase 14 Findings`.
  - **Completion gate**: 0 scoped hits and an unchanged full-tree count. Once done, mark this item as complete.

- [ ] **14.6 — Step 1.29: record the OQ-10 pipx decision request (L5, PENDING)**
  - **Context**: DESIGN step 1.29 (near DESIGN line 940): "`superclaude sweep --help` under a pipx install; output saved to `.dev/tasks/<pkg>/artifacts/sweep-help-pipx.txt`", marked Manual. REPORT:1300: run once "from a directory that is not a uv project, time limit 30 s"; pass = exit 0 and the help lists the `run` subcommand. research/09:131: the `superclaude` on PATH is a pipx master install (`git+https://github.com/IronbellyOrg/IronClaude`) with no `sweep`. research/09:135: option A `pipx run --spec <worktree path> superclaude sweep --help` leaves the installed tool alone, read from help text only (that a local path works as `--spec` is UNVERIFIED); option B `pipx install --force <worktree path>`, then reinstall from master, changes the person's installed tool, an install under D4 (`.dev/orca-command-refactor/decisions/APPROVED.md:11`), so it needs the owner's approval and the coordinator runs it.
  - **Action**: Write `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/OQ-10-pipx-decision.md` containing `needs_human_decision: true` and `status: PENDING`; the question "How should step 1.29 put the branch code under pipx?"; the two options verbatim: "(A) from /tmp, first run `pipx run --spec <worktree path> superclaude --version` with no time limit, which only builds and caches pipx's own temporary environment, then run `pipx run --spec <worktree path> superclaude sweep --help` with a 30 s limit on the help run only (REPORT:1300); the installed superclaude is not changed; that a local path works as --spec is UNVERIFIED." and "(B) the coordinator runs `pipx install --force <worktree path>`, runs `superclaude sweep --help` from /tmp, then reinstalls from `git+https://github.com/IronbellyOrg/IronClaude`; this changes the person's installed tool and needs owner approval (D4)."; the line "Builder recommendation: (A), because it changes no installed tool. This recommendation does NOT authorize adoption."; and the empty lines `OPERATOR DECISION:`, `Chosen:`, `Decided by:`, `Decision source:`.
  - **Output**: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/OQ-10-pipx-decision.md`.
  - **Verification**: Verify: `status: PENDING`, both options, the "does NOT authorize adoption" label and the four empty decision lines. Add OQ-10 to `### Open Questions` if it is not already there.
  - **Completion gate**: The decision request is recorded. Once done, mark this item as complete.

- [ ] **14.7 — HALT until the owner decides OQ-10 (L5)**
  - **Context**: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/OQ-10-pipx-decision.md` from item 14.6. The owner's own words in the session are the decision (APPROVED G1, `.dev/orca-command-refactor/decisions/APPROVED.md:71`).
  - **Action**: Read the decision file. Branch 1: if `status` is PENDING or `Chosen:` is empty, apply the HALT rule with `blocker_reason: "OQ-10 (step 1.29 pipx check) awaits the owner's decision in phase-outputs/plans/OQ-10-pipx-decision.md"` and STOP. Branch 2: if `Chosen:` is (A) or (B) with `Decided by:` and `Decision source:` filled, set `status: RESOLVED`, append the decision to `### Execution Log`, set the task `status` back to "🟠 Doing" and clear `blocker_reason`.
  - **Output**: The decision file with `status: RESOLVED`, or a Blocked task.
  - **Verification**: Verify: on Branch 2 the file names the option, the decider and the source. On Branch 1, stop before marking this item complete until the blocker is resolved.
  - **Completion gate**: OQ-10 is RESOLVED. Once done, mark this item as complete.

- [ ] **14.8 — Step 1.29: run or collect the pipx check (L3, both branches)**
  - **Context**: The RESOLVED `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/plans/OQ-10-pipx-decision.md`; pass rule REPORT:1300 (exit 0, the help lists `run`); output path DESIGN step 1.29 `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/sweep-help-pipx.txt`. No test runs this; it is a manual check (DESIGN line 940; research/09:136).
  - **Action**: Branch (A): REPORT:1300 sets the 30 s limit for the help run only, and on a cold pipx cache `pipx run --spec` first builds a wheel from the worktree and installs its runtime dependencies, so run two calls. First the untimed warm-up, which only fills pipx's own cache and leaves the installed tool unchanged: `WT=$(git rev-parse --show-toplevel); cd /tmp && pipx run --spec "$WT" superclaude --version > "$WT/.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/sweep-help-pipx-warmup.txt" 2>&1; echo "exit=$?" >> "$WT/.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/sweep-help-pipx-warmup.txt"`. If the warm-up exit is not 0, log its output in `### Phase 14 Findings` and apply the HALT rule with `blocker_reason: "step 1.29 pipx warm-up failed: <exit line>"`. Then the timed help run, which reuses the cached environment: `WT=$(git rev-parse --show-toplevel); cd /tmp && timeout 30 pipx run --spec "$WT" superclaude sweep --help > "$WT/.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/sweep-help-pipx.txt" 2>&1; echo "exit=$?" >> "$WT/.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/sweep-help-pipx.txt"`. Branch (B): the install is the coordinator's (D4); apply the HALT rule with `blocker_reason: "OQ-10 option (B): the coordinator runs the pipx install, superclaude sweep --help from /tmp and the reinstall from master, and saves output plus exit code to .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/sweep-help-pipx.txt"` and STOP; on resume, read the saved file. Do not run `pipx install` from this task on either branch.
  - **Output**: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/sweep-help-pipx.txt` holding the help output and an `exit=<n>` line.
  - **Verification**: Verify: the file ends with `exit=0` and lists `run` as a command. If it shows `exit=124` (30 s limit) or another non-zero code, log the output in `### Phase 14 Findings` and apply the HALT rule with `blocker_reason: "step 1.29 pipx check failed: <exit line>"`; stop before marking this item complete until the blocker is resolved.
  - **Completion gate**: `exit=0` and `run` are in the saved file. Once done, mark this item as complete.
````

## Coverage slice

76 rows: every FR, NFR and STEP row of `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/reflect/pre/coverage-matrix.yaml`, in matrix order. "Items in phases 7 to 14" keeps only the matched items that can deliver.

| ID | Source | Defining line | Match | All matched items | Items in phases 7 to 14 | Matrix note |
|---|---|---|---|---|---|---|
| FR-001 | parsed | docs/designs/orchestrator-mode.md:755 | exact | 10.6 | 10.6 | - |
| FR-002 | parsed | docs/designs/orchestrator-mode.md:756 | exact | 9.10 | 9.10 | - |
| FR-003 | parsed | docs/designs/orchestrator-mode.md:757 | exact | 9.1, 9.10, 10.7 | 9.1, 9.10, 10.7 | - |
| FR-004 | parsed | docs/designs/orchestrator-mode.md:758 | exact | 9.1, 9.10, 10.7 | 9.1, 9.10, 10.7 | - |
| FR-005 | parsed | docs/designs/orchestrator-mode.md:759 | exact | 10.7 | 10.7 | - |
| FR-006 | parsed | docs/designs/orchestrator-mode.md:760 | exact | 10.2 | 10.2 | - |
| FR-007 | parsed | docs/designs/orchestrator-mode.md:761 | none | none | none | no literal ID token in any item; substance-only candidates by design section 12 test file ['test_classify.py']: ['2.5', '2.13', '3.2', '4.3', '4.4', '4.5'] |
| FR-008 | parsed | docs/designs/orchestrator-mode.md:762 | none | none | none | no literal ID token in any item; substance-only candidates by design section 12 test file ['test_classify.py']: ['2.5', '2.13', '3.2', '4.3', '4.4', '4.5'] |
| FR-009 | parsed | docs/designs/orchestrator-mode.md:763 | none | none | none | no literal ID token in any item; substance-only candidates by design section 12 test file ['test_classify.py']: ['2.5', '2.13', '3.2', '4.3', '4.4', '4.5'] |
| FR-010 | parsed | docs/designs/orchestrator-mode.md:764 | exact | 2.5, 2.16, 3.3, 3.5, 3.7, 3.14, 4.1, 4.3, 4.4, 4.5, 4.7, 4.8, 4.9, 4.10, 4.11, 4.12, 4.13, 4.14, 4.15, 4.18, 4.19, 4.22, 4.23, 10.2, 14.11, 14.35 | 10.2, 14.11, 14.35 | - |
| FR-011 | parsed | docs/designs/orchestrator-mode.md:765 | none | none | none | no literal ID token in any item; substance-only candidates by design section 12 test file ['test_report.py']: ['10.5', '10.11'] |
| FR-012 | parsed | docs/designs/orchestrator-mode.md:766 | exact | 10.2 | 10.2 | - |
| FR-013 | parsed | docs/designs/orchestrator-mode.md:767 | none | none | none | no literal ID token in any item; substance-only candidates by design section 12 test file ['test_classify.py', 'test_probes_allowlist.py']: ['2.5', '2.13', '3.2', '4.3', '4.4', '4.5'] |
| FR-014 | parsed | docs/designs/orchestrator-mode.md:768 | none | none | none | no literal ID token in any item; substance-only candidates by design section 12 test file ['test_classify.py']: ['2.5', '2.13', '3.2', '4.3', '4.4', '4.5'] |
| FR-015 | parsed | docs/designs/orchestrator-mode.md:769 | exact | 10.2 | 10.2 | - |
| FR-016 | parsed | docs/designs/orchestrator-mode.md:770 | none | none | none | no literal ID token in any item; substance-only candidates by design section 12 test file ['test_report.py']: ['10.5', '10.11'] |
| FR-017 | parsed | docs/designs/orchestrator-mode.md:771 | none | none | none | no literal ID token in any item; substance-only candidates by design section 12 test file ['test_cli_contract.py']: ['10.7', '10.11'] |
| FR-018 | parsed | docs/designs/orchestrator-mode.md:772 | none | none | none | no literal ID token in any item; substance-only candidates by design section 12 test file ['test_cli_contract.py']: ['10.7', '10.11'] |
| FR-019 | parsed | docs/designs/orchestrator-mode.md:773 | none | none | none | no literal ID token in any item; substance-only candidates by design section 12 test file ['test_cli_contract.py']: ['10.7', '10.11'] |
| FR-020 | parsed | docs/designs/orchestrator-mode.md:774 | none | none | none | no literal ID token in any item; substance-only candidates by design section 12 test file ['test_probes_allowlist.py', 'test_report.py']: ['2.5', '2.13', '10.3', '10.5', '10.10', '10.11'] |
| FR-021 | parsed | docs/designs/orchestrator-mode.md:775 | exact | 8.10, 10.3 | 8.10, 10.3 | - |
| FR-022 | parsed | docs/designs/orchestrator-mode.md:776 | none | none | none | no literal ID token in any item; substance-only candidates by design section 12 test file ['test_sweep_command.py']: ['11.4', '11.5', '11.6', '11.7', '11.8', '11.9'] |
| FR-023 | parsed | docs/designs/orchestrator-mode.md:777 | exact | 5.3, 5.14, 5.19 | none | - |
| FR-024 | parsed | docs/designs/orchestrator-mode.md:778 | none | none | none | no literal ID token in any item; substance-only candidates by design section 12 test file ['test_routing_plugin_parity.py']: ['13.4'] |
| FR-025 | parsed | docs/designs/orchestrator-mode.md:779 | exact | 7.1 | 7.1 | - |
| FR-026 | parsed | docs/designs/orchestrator-mode.md:780 | none | none | none | no literal ID token in any item; substance-only candidates by design section 12 test file ['test_probes_allowlist.py']: ['2.5', '2.13', '10.3', '10.10'] |
| NFR-001 | parsed | docs/designs/orchestrator-mode.md:781 | exact | 10.4 | 10.4 | - |
| NFR-002 | parsed | docs/designs/orchestrator-mode.md:782 | none | none | none | no literal ID token in any item; substance-only candidates by design section 12 test file ['test_readonly.py']: ['8.7', '8.9', '8.14', '8.15', '8.16', '8.17'] |
| NFR-003 | parsed | docs/designs/orchestrator-mode.md:783 | exact | 2.16 | none | - |
| NFR-004 | parsed | docs/designs/orchestrator-mode.md:784 | exact | 8.4, 10.2 | 8.4, 10.2 | - |
| NFR-005 | parsed | docs/designs/orchestrator-mode.md:785 | none | none | none | no literal ID token in any item; substance-only candidates by design section 12 test file ['test_report.py']: ['10.5', '10.11'] |
| NFR-006 | parsed | docs/designs/orchestrator-mode.md:786 | exact | 10.6 | 10.6 | - |
| NFR-007 | parsed | docs/designs/orchestrator-mode.md:787 | none | none | none | no literal ID token in any item; substance-only candidates by design section 12 test file ['test_probes_allowlist.py', 'test_sweep_command.py']: ['2.5', '2.13', '10.3', '10.10', '11.4', '11.5'] |
| NFR-008 | parsed | docs/designs/orchestrator-mode.md:788 | none | none | none | no literal ID token in any item; substance-only candidates by design section 12 test file ['test_report.py']: ['10.5', '10.11'] |
| NFR-009 | parsed | docs/designs/orchestrator-mode.md:789 | none | none | none | no literal ID token in any item; substance-only candidates by design section 12 test file ['test_cli_contract.py']: ['10.7', '10.11'] |
| NFR-010 | parsed | docs/designs/orchestrator-mode.md:790 | exact | 10.2 | 10.2 | - |
| NFR-011 | parsed | docs/designs/orchestrator-mode.md:791 | none | none | none | no literal ID token in any item; substance-only candidates by design section 12 test file ['test_sweep_command.py']: ['11.4', '11.5', '11.6', '11.7', '11.8', '11.9'] |
| NFR-012 | parsed | docs/designs/orchestrator-mode.md:792 | none | none | none | no literal ID token in any item; substance-only candidates by keyword ['make lint']: ['14.2', '14.25', '14.29', '14.38', '14.42'] |
| NFR-013 | parsed | docs/designs/orchestrator-mode.md:793 | exact | 10.4 | 10.4 | - |
| NFR-014 | parsed | docs/designs/orchestrator-mode.md:794 | exact | 2.16, 6.1, 6.5, 6.6, 6.7, 6.8, 6.9, 6.10, 6.11, 6.12, 6.13, 6.16, 6.17, 6.20, 6.21, 14.35 | 14.35 | - |
| NFR-015 | parsed | docs/designs/orchestrator-mode.md:795 | none | none | none | no literal ID token in any item; substance-only candidates by design section 12 test file ['test_report.py']: ['10.5', '10.11'] |
| step-1.0a | parsed | docs/designs/orchestrator-mode.md:829 | exact | 2.4, 2.10, 3.8, 4.9, 6.1, 6.6, 7.14, 7.15, 7.16, 7.17, 7.18, 8.10, 9.1, 10.3, 14.20, 14.34 | 7.14, 7.15, 7.16, 7.17, 7.18, 8.10, 9.1, 10.3, 14.20, 14.34 | - |
| step-1.0b | parsed | docs/designs/orchestrator-mode.md:907 | exact | 7.13 | 7.13 | - |
| step-1.1 | parsed | docs/designs/orchestrator-mode.md:908 | exact | 8.2 | 8.2 | - |
| step-1.2 | parsed | docs/designs/orchestrator-mode.md:909 | exact | 7.17, 7.26, 8.3 | 7.17, 7.26, 8.3 | - |
| step-1.3 | parsed | docs/designs/orchestrator-mode.md:910 | exact | 7.11, 8.4, 9.3, 9.9 | 7.11, 8.4, 9.3, 9.9 | - |
| step-1.4a | parsed | docs/designs/orchestrator-mode.md:911 | exact | 8.5, 8.6, 8.8, 8.9, 8.11, 8.14, 8.15, 8.16, 8.17, 8.18, 8.19, 8.20, 8.23, 8.24, 8.27, 8.28 | 8.5, 8.6, 8.8, 8.9, 8.11, 8.14, 8.15, 8.16, 8.17, 8.18, 8.19, 8.20, 8.23, 8.24, 8.27, 8.28 | - |
| step-1.4 | parsed | docs/designs/orchestrator-mode.md:830 | exact | 7.14, 7.17, 8.10, 8.11, 8.14, 8.15, 8.16, 8.17, 8.18, 8.19, 8.20, 8.23, 8.24, 8.27, 8.28, 9.3, 14.16 | 7.14, 7.17, 8.10, 8.11, 8.14, 8.15, 8.16, 8.17, 8.18, 8.19, 8.20, 8.23, 8.24, 8.27, 8.28, 9.3, 14.16 | - |
| step-1.5 | parsed | docs/designs/orchestrator-mode.md:831 | exact | 7.5, 7.7, 7.9, 8.12 | 7.5, 7.7, 7.9, 8.12 | - |
| step-1.6 | parsed | docs/designs/orchestrator-mode.md:832 | exact | 7.1, 7.7, 7.17, 7.26, 9.1 | 7.1, 7.7, 7.17, 7.26, 9.1 | - |
| step-1.7 | parsed | docs/designs/orchestrator-mode.md:915 | exact | 5.6, 5.19, 9.2, 9.5, 9.6, 9.7, 9.8, 9.9, 9.10, 9.11, 9.12, 9.15, 9.16, 9.19, 9.20 | 9.2, 9.5, 9.6, 9.7, 9.8, 9.9, 9.10, 9.11, 9.12, 9.15, 9.16, 9.19, 9.20 | - |
| step-1.8 | parsed | docs/designs/orchestrator-mode.md:916 | exact | 8.8, 10.1 | 8.8, 10.1 | - |
| step-1.9 | parsed | docs/designs/orchestrator-mode.md:917 | exact | 10.2 | 10.2 | - |
| step-1.10 | parsed | docs/designs/orchestrator-mode.md:918 | exact | 10.3 | 10.3 | - |
| step-1.11 | parsed | docs/designs/orchestrator-mode.md:919 | exact | 10.4 | 10.4 | - |
| step-1.12 | parsed | docs/designs/orchestrator-mode.md:920 | exact | 7.7, 10.5 | 7.7, 10.5 | - |
| step-1.13 | parsed | docs/designs/orchestrator-mode.md:921 | exact | 10.6, 10.7 | 10.6, 10.7 | - |
| step-1.14 | parsed | docs/designs/orchestrator-mode.md:833 | exact | 11.1, 11.2, 11.6, 11.7, 11.8, 11.9, 11.10, 11.11, 11.12, 11.15, 11.16, 11.19, 11.20 | 11.1, 11.2, 11.6, 11.7, 11.8, 11.9, 11.10, 11.11, 11.12, 11.15, 11.16, 11.19, 11.20 | - |
| step-1.15 | parsed | docs/designs/orchestrator-mode.md:834 | exact | 11.3, 11.6, 11.7, 11.8, 11.9, 11.10, 11.11, 11.12, 11.15, 11.16, 11.19, 11.20 | 11.3, 11.6, 11.7, 11.8, 11.9, 11.10, 11.11, 11.12, 11.15, 11.16, 11.19, 11.20 | - |
| step-1.16 | parsed | docs/designs/orchestrator-mode.md:924 | exact | 11.4, 13.6 | 11.4, 13.6 | - |
| step-1.16a | parsed | docs/designs/orchestrator-mode.md:925 | exact | 5.7, 5.11, 5.14, 5.16, 7.19 | 7.19 | - |
| step-1.17 | parsed | docs/designs/orchestrator-mode.md:835 | exact | 5.3, 5.7, 5.17, 5.19, 5.21, 6.9, 7.3, 7.19, 7.26, 12.1, 12.6, 12.7, 12.8, 12.9, 12.10, 12.11, 12.12, 12.15, 12.16, 12.19, 12.20 | 7.3, 7.19, 7.26, 12.1, 12.6, 12.7, 12.8, 12.9, 12.10, 12.11, 12.12, 12.15, 12.16, 12.19, 12.20 | - |
| step-1.18 | parsed | docs/designs/orchestrator-mode.md:927 | exact | 12.2, 12.4 | 12.2, 12.4 | - |
| step-1.19 | parsed | docs/designs/orchestrator-mode.md:928 | exact | 5.7, 5.14, 5.17, 5.21, 7.3, 7.19, 7.26, 12.3, 12.6, 12.7, 12.8, 12.9, 12.10, 12.11, 12.12, 12.15, 12.16, 12.19, 12.20 | 7.3, 7.19, 7.26, 12.3, 12.6, 12.7, 12.8, 12.9, 12.10, 12.11, 12.12, 12.15, 12.16, 12.19, 12.20 | - |
| step-1.20 | parsed | docs/designs/orchestrator-mode.md:929 | exact | 11.2 | 11.2 | - |
| step-1.21 | parsed | docs/designs/orchestrator-mode.md:930 | none | none | none | no literal ID token in any item; substance-only candidates by keyword ['routing row R1', 'row R1', 'R1 and R2']: ['13.2', '14.20'] |
| step-1.22 | parsed | docs/designs/orchestrator-mode.md:931 | none | none | none | no literal ID token in any item; substance-only candidates by keyword ['_OTHER_COMMANDS']: ['13.3'] |
| step-1.23 | parsed | docs/designs/orchestrator-mode.md:932 | none | none | none | no literal ID token in any item; substance-only candidates by keyword ['plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md']: ['1.4', '13.4', '13.8', '13.9', '13.10', '13.11'] |
| step-1.24 | parsed | docs/designs/orchestrator-mode.md:933 | none | none | none | no literal ID token in any item; substance-only candidates by keyword ['docs/user-guide/commands.md']: ['1.4', '5.10', '13.5', '13.9', '13.10', '13.11'] |
| step-1.24a | parsed | docs/designs/orchestrator-mode.md:934 | exact | 12.4 | 12.4 | - |
| step-1.24b | parsed | docs/designs/orchestrator-mode.md:935 | exact | 13.6 | 13.6 | - |
| step-1.25 | parsed | docs/designs/orchestrator-mode.md:936 | none | none | none | no literal ID token in any item; substance-only candidates by keyword ['make sync-dev']: ['14.1', '14.5', '14.25', '14.29', '14.38', '14.42'] |
| step-1.26 | parsed | docs/designs/orchestrator-mode.md:937 | none | none | none | no literal ID token in any item; substance-only candidates by keyword ['make lint']: ['14.2', '14.25', '14.29', '14.38', '14.42'] |
| step-1.27 | parsed | docs/designs/orchestrator-mode.md:938 | none | none | none | no literal ID token in any item; substance-only candidates by keyword ['uv run pytest tests/sweep tests/commands']: ['14.3', '14.12', '14.25', '14.29', '14.38', '14.42'] |
| step-1.28 | parsed | docs/designs/orchestrator-mode.md:939 | exact | 14.5, 14.10, 14.11, 14.12, 14.13, 14.14, 14.15, 14.16, 14.17, 14.18, 14.19, 14.20, 14.21, 14.22, 14.23, 14.26, 14.27, 14.30, 14.31 | 14.5, 14.10, 14.11, 14.12, 14.13, 14.14, 14.15, 14.16, 14.17, 14.18, 14.19, 14.20, 14.21, 14.22, 14.23, 14.26, 14.27, 14.30, 14.31 | - |
| step-1.29 | parsed | docs/designs/orchestrator-mode.md:940 | exact | 14.6, 14.7, 14.8, 14.12, 14.20, 14.34 | 14.6, 14.7, 14.8, 14.12, 14.20, 14.34 | - |

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
