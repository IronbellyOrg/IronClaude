```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.81
citations_total: 53
citations_revalidated: 53
citations_dropped: 1
citations_inferred: 1
citation_budget_policy: sampled
coverage_degraded: parsed-sparse
```

> **Citation budget: sampled mode (policy label only)**
> - `citations_total: 53` is above the 20 threshold, so the policy label is `sampled`; the evidence validator nevertheless re-read every citation, so `citations_revalidated: 53`.
> - `citations_dropped: 1`: the inferred-requirement row INF-006, whose quote did not match its cited line. That forces `status: partial`. The validator found 0 unfounded `file:line` citations and 8 weak ones (line numbers off or claim partly inferred); all 8 were corrected in this report, not dropped. The two citations added after validation (`WORKER-CONTRACT.md:184`, brainstorm `SKILL.md:335`) were re-read by the orchestrator.
> - `citations_dropped_extrapolated: 1` (all citations were re-read, so the sample count is the population count).
> - The extrapolated value is telemetry, not a verdict.

# Reflect report (pre-execution): P1 static plan

- Plan: `.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/TASK-WF-writeTheP1Static-20261105-033458.md` (cited as `plan:N`)
- Driving document: `.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/source.md` (the brief) and the spec `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (cited as `spec:N`)
- Tier 2: three reviewers (sonnet, haiku, opus), blind calibration (0.81, 0.80, 0.82), a two-round adversarial debate, an invariant probe and a merge through the adversarial protocol (`adversarial/merged-verdict.yaml`, `merge_method: adversarial`, convergence 1.00 after round 2).
- **Verdict: PARTIAL.** No structural defect in the plan's design. 8 blocking findings (MF-01 to MF-08), each with a concrete edit to a named task, and 12 minor notes (MF-09 to MF-20). Two open owner questions.
- Coverage is `parsed-sparse`: the brief has no numbered requirement ids, so all requirements are inferred. After the evidence validator dropped INF-006 (quote mismatch), 13 inferred rows survive and 7 are matched by the matcher: `coverage_pct_union` 0.54 (was 0.50), `unmapped_requirements_union` INF-001, INF-002, INF-003, INF-009, INF-010, INF-014 (six rows, all paraphrases the matcher misses; the plan's Constraints and tasks cover them, and the reviewers walked the spec rows by hand and found no missing deliverable beyond the findings below), `S_dev_density` 0.46 (was 0.50).

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation (file:line) | Match result |
|---|---|---|---|
| INF-001 | Static plan only: the edits and the checks that need no live Orca run. The live plan is written later. | `.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/source.md:1` | unmatched by the matcher; plan Constraints cover it |
| INF-002 | including the 2026-11-05 heartbeat decision (looser reading of section 7.2 step 5 condition 4 accepted; WC-10 unchanged; P0 verdict PASS) | `.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/source.md:3` | unmatched by the matcher; plan Constraints cover it |
| INF-003 | the WC-4 contract, the report-directory rule, the flag parse rule and the person-mode refusal (section 2.1) for the P1 commands only | `.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/source.md:5` | unmatched by the matcher; covered by the skeleton |
| INF-004 | --unattended is added to a command only in the phase that converts its gates | `.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/source.md:5` | Task 3 |
| INF-005 | output flags for commands that lack one | `.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/source.md:5` | Task 1 (matcher) |
| INF-007 | adversarial, brainstorm, cleanup-audit, graph, impact, index-repo, init-lite, workflow (ready, no gate change) and analyze, build, business-panel, design, document, explain, index, test (no gate) | `.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/source.md:5` | Tasks 2 to 12 |
| INF-008 | /sc:load gets its usage-line fix only and never gains the flag. | `.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/source.md:5` | Task 13 |
| INF-009 | the LIVE plan holds the section 7.2 live checks (AC-1.2, AC-1.3, AC-1.5, AC-1.6, AC-1.7, AC-1.8) and the phase report, and is written after the static checks pass | `.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/source.md:7` | unmatched by the matcher; plan Constraints cover it |
| INF-010 | the exact files to edit (installed-path rules apply: never hardcode src/superclaude/ paths inside installed primitives; edit the src/superclaude/ sources and run make sync-dev) | `.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/source.md:9` | unmatched by the matcher; plan Constraints and Task 15 cover it |
| INF-011 | acceptance criteria that are observable (a command, a grep, a test) | `.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/source.md:9` | every task |
| INF-012 | the tests to add or extend (tests/skills/test_worker_contract.py and the per-command tests) | `.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/source.md:9` | Tasks 1, 4, 5, 14 |
| INF-013 | Include the static checks of section 7.1 and 7.3 that apply to P1 (AC-1.1, AC-1.4, AC-C1 to AC-C6), make lint, the ruff format check, make verify-sync, and the pre-existing tests that read the edited files. | `.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/source.md:9` | Task 15 |
| INF-014 | Do not execute the plan: no /sc:implement, no commit, no push, no superclaude install, no live Orca run. Stage nothing under .claude/. | `.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/source.md:11` | unmatched by the matcher; plan Constraints cover it |

Postscript (dropped by the evidence validator): INF-006 was dropped because its quote added the word "the" ("the small fixes to the ready commands"; `source.md:5` reads "the small fixes to ready commands"). The row was unmatched by the matcher anyway; the small fixes it names are in Tasks 2, 6, 7, 8 and 9.

## Findings (gap registry)

Severity: blocking = wrong behaviour or a missing required deliverable; minor = clarity, wording or a note. Every blocking finding was confirmed against the files by at least two sources (card, calibrator, advocate, or the probe re-read).

### MF-01 (blocking): graph and impact skills cannot take the new flags or write the worker contract under `--report-dir`

- **Evidence:** `src/superclaude/skills/sc-graph-protocol/SKILL.md:27` ("`--output-dir` ... created if missing"); `src/superclaude/skills/sc-impact-protocol/SKILL.md:49`; `.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/TASK-WF-writeTheP1Static-20261105-033458.md:111` (Task 4's skill edit touches only the contract table, not the flag table)
- **Edit:** Tasks 4 and 5 add the two flag rows to each skill's flag table, edit graph step G-O and the "(only with `--output-dir`)" heading, impact step 10 and its write-scope sentence, and state where `impact.md` lands and that the worker contract at `<report-dir>` lists the command's own contract in `artifacts`. Add a test that each flag table names both flags.

### MF-02 (blocking): the graph `init` refusal must be a skill stop, not a step after Init

- **Evidence:** `src/superclaude/commands/graph.md:40` (the skill runs first); `src/superclaude/commands/graph.md:48` (the init guard is the first Init step, after the skill returned).
- **Edit:** Task 4 adds a stop row to the skill's flag table: positional `init` with `--unattended` gives `blocked`, mapped to `failed`, reason "init runs only when the user types it". No new enum value.

### MF-03 (blocking): init-lite hands its work to a strict command-line tool; the plan does not keep the new flags off it or say who writes the contract on `--dry-run`

- **Evidence:** `src/superclaude/skills/sc-init-lite-protocol/SKILL.md:57`; `src/superclaude/commands/init-lite.md:94`
- **Edit:** Task 8 adds Activation bullets for both flags, states that the skill consumes both and never forwards them, that the skill writes `<report-dir>/return-contract.yaml` after the tool returns on every outcome including `--dry-run`, and adds an "except under `--unattended`, the worker contract" line next to the `--dry-run` Will Not line.

### MF-04 (blocking): Task 15's path-list equality fails on files that changed before the plan

- **Evidence:** `.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/TASK-WF-writeTheP1Static-20261105-033458.md:289`
- **Edit:** Task 15 compares paths only, scoped to `git status --short --untracked-files=all -- src tests plugins`.

### MF-05 (blocking): Task 14's nested-propagation test has no rule for what counts as a nested invocation

- **Evidence:** `.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/TASK-WF-writeTheP1Static-20261105-033458.md:261`; `src/superclaude/skills/sc-workflow-protocol/SKILL.md:58`
- **Edit:** Tasks 1 and 14 add a data field `UNATTENDED_EXPECT[cmd]["nested"]` (brainstorm: analyze and adversarial; workflow: none) and assert `nested/<c>-` only for those.

### MF-06 (blocking): brainstorm can write its contract to a suffixed directory, and early stops write no contract

- **Evidence:** `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:108` ("If exists and non-empty, append `-N` suffix"); `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:105` (step 7 can stop the run); `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:335` (the contract is described only in the Return Contract section, after those steps).
- **Edit:** Task 3: under `--unattended` use the passed directory exactly, never suffixed; refuse a directory that already holds a `return-contract.yaml`; every stop writes a `failed` worker contract.

### MF-07 (blocking): `--report-dir` has none of the path rules the commands' own directory flags have

- **Evidence:** `src/superclaude/skills/sc-graph-protocol/SKILL.md:27` (blocks `.git` and `.codegraph`); `src/superclaude/skills/sc-adversarial-protocol/SKILL.md:397` (forbidden output prefixes); `src/superclaude/core/WORKER-CONTRACT.md:15` ("Report directory").
- **Edit:** the section skeleton and Tasks 2, 4, 5: `--report-dir` gets the same path rules as the command's own directory flag; a rejected or unwritable report directory counts as "no report directory known" and the refusal is printed in chat only.

### MF-08 (blocking): consent steps are left open in commands the plan calls "no gate"

- **Evidence:** `src/superclaude/commands/test.md:106` ("without explicit permission"); `src/superclaude/commands/analyze.md:100` ("without explicit user consent"); `src/superclaude/commands/design.md:99` ("without explicit design approval").
- **Edit:** new decision D-P1-12: under `--unattended` consent is never given (so `/sc:test --fix` is refused or applies no fix, and analyze and design do not modify anything). Tasks 10 and 11 state the result in each section.

### Minor notes (MF-09 to MF-20)

- **MF-09:** brainstorm Wave 0 step 7 stops before the plan's handoff-skip rule (`src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:105`); the handoff ref still forwards `--interactive` (`src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md:101`); `-i` is the short form (`src/superclaude/commands/brainstorm.md:59`). Task 3: skip step 7, add the ref, refuse `-i`.
- **MF-10:** the Python copy of the Check SCAN pattern uses a POSIX class that Python does not read the same way (`.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/TASK-WF-writeTheP1Static-20261105-033458.md:29`). Task 1: give `re.compile(r"\borca(-ide)?\s+(orchestration|worktree|terminal|agent)\b", re.I)` and a negative case.
- **MF-11:** "final boundaries heading" disagrees with Tasks 3, 6, 9 for files with two boundaries headings (`.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/TASK-WF-writeTheP1Static-20261105-033458.md:24`; `src/superclaude/commands/brainstorm.md:177`). Skeleton: "the first `## Boundaries` heading".
- **MF-12:** `tests/test_cleanup_audit_structure.py` tests the Python pipeline (`tests/test_cleanup_audit_structure.py:17`) and is in neither baseline; drop it from Task 6; the `tests/skills/` count is six, not seven.
- **MF-13:** D-P1-1 (`.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:72` vs the existing short-name `command` key). Reword the lead-in; the coordinator ratifies in the Task 15 report.
- **MF-14:** the lint comparison needs a definition of pass (`Makefile:406`, the over-200-lines branch, prints a WARN line and does not fail). Pass = exit 0, no new ERROR, no ruff finding; new WARN lines recorded.
- **MF-15:** adversarial also has `-i` and `-o` (`src/superclaude/commands/adversarial.md:68`). Task 2 names both.
- **MF-16:** the `--output` retirement test covers the refs Task 9 edits (`tests/commands/test_workflow_command.py:124`). Task 9 applies the rule there and forbids naming the new error `E-MISSING-DIR` (`tests/commands/test_workflow_command.py:127`).
- [INFERRED] **MF-17:** the spec's init-lite row names only Safety Invariant 3 (`.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:147`); because the contract is also written on `--dry-run`, Invariant 2 needs the same exception (inference from the plan's own Task 8 text). Add decision D-P1-11.
- **MF-18:** plugin command copies other than workflow go stale by design (`src/superclaude/commands/README.md:9`). Task 15: one inventory line.
- **MF-19:** `src/superclaude/commands/business-panel.md:6` has trailing spaces; Task 11 requires keys and values byte-for-byte unchanged and keeps the at-most-4-deleted-lines bound.
- **MF-20:** the brief-flag table in `src/superclaude/core/WORKER-CONTRACT.md:196` still lists `/sc:index-repo` as "none", and `src/superclaude/core/WORKER-CONTRACT.md:184` still says "At P0 no command accepts it"; outside this plan's files; a note for the coordinator only.

## Not merged (rejected in the debate)

The downgrade of brainstorm nesting (the plan discloses it as D-P1-4); the unconfirmed R1-09; reviewer 1's claim that impact ends "blocked" on bad flags (impact's `--output-dir` has a default at `src/superclaude/skills/sc-impact-protocol/SKILL.md:29`); "seven" files under `tests/skills/`; "bad flags blocked" wording in the graph and impact tables.

## Open owner questions

1. **D-P1-1, graph and impact `command` key.** The spec says the worker `command` field is the exact command line (`.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:72`); the existing contracts carry `graph` and `impact`. The plan keeps the short name. Recommended: keep it and ratify.
2. **D-P1-4, brainstorm nested scope.** The spec's brainstorm row passes the flag to nested calls "from P2" (`.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:142`); the plan does it in P1. Recommended: keep it, confirm in the Task 15 report.

## Inferred-claim audit

- `citations_inferred: 1`
- Inferred-fraction: `1 / 53` = 0.02

## Recommendations

### Recommendation R-001: Make the graph and impact skills accept and write the worker contract under `--report-dir`

- **File:** `.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/TASK-WF-writeTheP1Static-20261105-033458.md` (Tasks 4 and 5)
- **Change:** add the flag-table rows, the step and heading edits, the `impact.md` placement sentence, the init stop row (MF-01, MF-02, MF-07).
- **Verifier:** `grep -n 'report-dir' ` on the Task 4 and Task 5 text shows the rows; a fresh reviewer read of both tasks.
- **Linked deviation(s):** MF-01, MF-02, MF-07
- **Priority:** P0

### Recommendation R-002: Close the init-lite and brainstorm contract gaps

- **File:** `.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/TASK-WF-writeTheP1Static-20261105-033458.md` (Tasks 3 and 8)
- **Change:** per MF-03, MF-06 and MF-09.
- **Verifier:** a fresh reviewer read of Tasks 3 and 8.
- **Linked deviation(s):** MF-03, MF-06, MF-09
- **Priority:** P0

### Recommendation R-003: Fix the two checks that fail on a correct run and add the consent decision

- **File:** `.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/TASK-WF-writeTheP1Static-20261105-033458.md` (Tasks 1, 10, 11, 14, 15 and the decision list)
- **Change:** per MF-04, MF-05 and MF-08.
- **Verifier:** a fresh reviewer read of those tasks.
- **Linked deviation(s):** MF-04, MF-05, MF-08
- **Priority:** P0

### Recommendation R-004: Apply the minor notes in the same edit pass

- **File:** `.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/TASK-WF-writeTheP1Static-20261105-033458.md`
- **Change:** MF-10 to MF-19 as listed.
- **Verifier:** the plan gate checks (no checkbox lines, no absolute paths) still pass.
- **Linked deviation(s):** MF-10 to MF-19
- **Priority:** P2
