# P1 static report

Plan: `TASK-WF-writeTheP1Static-20261105-033458`. Scope: AC-1.1, AC-1.4 and AC-C1 to AC-C6 (spec sections 7.1 and 7.3). The live checks (AC-1.2, AC-1.3, AC-1.5 to AC-1.8) and the P1 phase report belong to the P1 live plan.

## Check results

- PASS AC-1.1: `tests/skills/test_worker_contract.py` passes (394 tests). Evidence: `./artifacts/ac-1.1.txt`.
- PASS AC-1.4: adversarial SKILL names `<output>/adversarial/return-contract.yaml`; the workflow ref has the worker-contract section. Evidence: `./artifacts/ac-1.4.txt`.
- PASS AC-C1: Check SCAN prints nothing. Evidence: `./artifacts/ac-c1.txt`.
- PASS AC-C2: `make sync-dev` and `make verify-sync` both exit 0. Evidence: `./artifacts/ac-c2.txt`.
- PASS AC-C3: No baseline-passing test fails (tests/skills 1109 -> 1255 passed; wider run 6616 -> 6621 passed); the sixteen named test files each pass. Evidence: `./artifacts/ac-c3-compare.md, wider-compare.md`.
- PASS AC-C4: No `.claude/` path is staged. Evidence: `./artifacts/ac-c4-index.txt`.
- PASS AC-C5: Sixteen converted command files additive except business-panel (14 added, 4 deleted, limit 4) and load (1 added, 1 deleted). Evidence: `./artifacts/ac-c5.txt`.
- PASS AC-C6: 1 Orca profile line(s), each `"nestedWorkerMaxDepth":1`. Evidence: `./artifacts/ac-c6-depth-setting.txt`.
- PASS lint: `make lint` exit 0, no new ERROR, ruff finding or WARN; one existing size WARN grew and is recorded below. Evidence: `./artifacts/lint-format-compare.md`.
- PASS format: The five test files are formatted. Evidence: `./artifacts/lint-format-compare.md`.
- PASS mirror check: The four workflow mirror pairs are byte-identical. Evidence: `./artifacts/mirror-check.txt`.

Overall: PASS (11 of 11).

Recorded WARN (does not fail): `make lint` already warned about `src/superclaude/commands/brainstorm.md` in the baseline (201 lines, threshold 200). The warning grew to 217 lines because of the 16-line Unattended mode section. There are 0 new WARN lines and the warning count stays 5. Evidence: `./artifacts/lint-format-compare.md`.

## Decisions made where the spec was silent (D-P1-1 to D-P1-12)

- D-P1-1: graph and impact keep their existing `command` key (short name) as the worker `command` field and add no second key (spec WC-4). Owner approved on 2026-11-05.
- D-P1-2: for analyze, build, design, explain, index, test and business-panel, `--output <file>` is new and optional; under `--unattended` without it the report goes to `<report-dir>/<name>-report.md`.
- D-P1-3: brainstorm's own status `dry-run` maps to `worker_status: succeeded` with `report_path: null`.
- D-P1-4: the nested propagation rule is applied to brainstorm in P1 (its `/sc:analyze` enrichment and adversarial call get `--unattended` and a nested report directory under `nested/<command>-<n>/`; `<n>` starts at 1 and is never reused). Research enrichment and the `tasklist` and `task` handoffs are skipped and recorded. Owner confirmed on 2026-11-05 after an adversarial debate.
- D-P1-5: workflow skips `--handoff implement` under `--unattended` and records the package contract as `partial` with an `unresolved` line; its reflect step runs without the flag.
- D-P1-6: graph refuses `init` under `--unattended`.
- D-P1-7: document requires an explicit `--output` for the external, api and guide types under `--unattended`.
- D-P1-8: a failing test suite is a verdict in the `/sc:test` report, not a failed run; `worker_status` is `failed` only when the runner could not run.
- D-P1-9: adversarial's `report_path` is its merged output (null when the merge was not reached).
- D-P1-10: cleanup-audit's `--pass all` final report is `.claude-audit/final-report.md`.
- D-P1-11: init-lite writes the worker contract also on `--dry-run`, so the exception in its skill covers Safety Invariant 2 as well as 3.
- D-P1-12: a consent line is never answered by assuming consent under `--unattended` (analyze modifies no source, design changes no architecture, test `--fix` makes non-destructive fixes only, index overwrites no existing manual documentation).

## UNVERIFIED items

- Business-panel frontmatter loading: the frontmatter was moved out of a code fence (keys byte-identical, including the trailing spaces on line 6). Whether Claude Code now parses that frontmatter, or loaded it before, was not run. A test pins only that it is not inside a fence.
- Index knowledge-base mode (`--type docs`): the section says it does not wait for a person under `--unattended`. Whether the mode ever waits was not run.
- Whether `--report-dir` is accepted by commands that already have a directory flag (adversarial, brainstorm, graph, impact), as the spec's section 2.1 wording implies. Each of their sections says exactly one of the two flags is required and that `--report-dir` follows the path rules of the existing flag. No live run was made. The P1 live plan covers it.

## Repo paths created or changed under `src`, `tests` and `plugins`

The list equals the paths printed by `git status --short --untracked-files=all -- src tests plugins`.

### Command files (17)

- `src/superclaude/commands/adversarial.md`
- `src/superclaude/commands/analyze.md`
- `src/superclaude/commands/brainstorm.md`
- `src/superclaude/commands/build.md`
- `src/superclaude/commands/business-panel.md`
- `src/superclaude/commands/cleanup-audit.md`
- `src/superclaude/commands/design.md`
- `src/superclaude/commands/document.md`
- `src/superclaude/commands/explain.md`
- `src/superclaude/commands/graph.md`
- `src/superclaude/commands/impact.md`
- `src/superclaude/commands/index-repo.md`
- `src/superclaude/commands/index.md`
- `src/superclaude/commands/init-lite.md`
- `src/superclaude/commands/load.md`
- `src/superclaude/commands/test.md`
- `src/superclaude/commands/workflow.md`

### Skill files (10)

- `src/superclaude/skills/sc-adversarial-protocol/SKILL.md`
- `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`
- `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md`
- `src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md`
- `src/superclaude/skills/sc-graph-protocol/SKILL.md`
- `src/superclaude/skills/sc-impact-protocol/SKILL.md`
- `src/superclaude/skills/sc-init-lite-protocol/SKILL.md`
- `src/superclaude/skills/sc-workflow-protocol/SKILL.md`
- `src/superclaude/skills/sc-workflow-protocol/refs/input-parse.md`
- `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md`

### Plugin mirrors (4)

- `plugins/superclaude/commands/workflow.md`
- `plugins/superclaude/skills/sc-workflow-protocol/SKILL.md`
- `plugins/superclaude/skills/sc-workflow-protocol/refs/input-parse.md`
- `plugins/superclaude/skills/sc-workflow-protocol/refs/return-contract.md`

### Test files (6)

- `tests/commands/test_graph_command.py`
- `tests/commands/test_impact_command.py`
- `tests/commands/test_workflow_command.py`
- `tests/recommend/test_routing_refresh.py`
- `tests/skills/test_brainstorm_protocol.py`
- `tests/skills/test_worker_contract.py`

## Plugin command copies left unmirrored

Only `workflow.md` and the `sc-workflow-protocol` skill files are mirrored (they are pinned by tests). For the other converted commands:

- Identical to the source before this plan, now behind it: brainstorm, build, document, index-repo, index, test.
- Already different from the source before this plan: analyze, business-panel, design, explain.
- No plugin copy exists: adversarial, cleanup-audit, graph, impact, init-lite.

## The sixteen commands and their report-directory flag (input to the P1 live plan)

- adversarial: `--output <dir>` (`-o`) or `--report-dir <dir>`
- brainstorm: `--output <dir>` (`-o`) or `--report-dir <dir>`
- graph: `--output-dir <dir>` or `--report-dir <dir>`
- impact: `--output-dir <dir>` or `--report-dir <dir>`
- cleanup-audit: `--report-dir <dir>` only
- index-repo: `--report-dir <dir>` only
- init-lite: `--report-dir <dir>` only (`--output` names the report file)
- workflow: `--report-dir <dir>` only (`--output` stays retired)
- analyze: `--report-dir <dir>` only
- build: `--report-dir <dir>` only
- business-panel: `--report-dir <dir>` only
- design: `--report-dir <dir>` only
- document: `--report-dir <dir>` only (`--output` is the documentation path)
- explain: `--report-dir <dir>` only
- index: `--report-dir <dir>` only (`--output` is the documentation path)
- test: `--report-dir <dir>` only

## Spec observations for the coordinator

- A worker field named `command` collides with the existing key in graph and impact (resolved by D-P1-1).
- The spec's status mapping has no entry for brainstorm's `dry-run` (resolved by D-P1-3).
- The spec's brainstorm row passes the flag to nested calls from P2, while this plan does it in P1 (D-P1-4, owner confirmed).
- The brief-flag table of `WORKER-CONTRACT.md` still describes the P0-era brief: it lists `/sc:index-repo` as none and `/sc:init-lite` with `--output <file>` only, and says that at P0 no command accepts the flag. This plan did not edit that file.
- WC-5's "before P1" override ends at P1, while the P2 commands troubleshoot, release-split and tdd still write no worker contract until P2.

## Plan gaps and deviations found while running the plan

- The pre-existing test `tests/recommend/test_routing_refresh.py` is in the plan's must-still-pass list but asserted that design has no `--output`, which contradicts Task 10 (design now declares `--output`). Its assertion was changed to `"--output" in` the Usage section. This file is outside Task 11's listed files and is an extra changed test file in the list above.
- Tasks 3, 4 and 5 (brainstorm, graph, impact) first wrote a shorter `--report-dir` path rule than the plan's section skeleton requires, and Task 9 (workflow) put the Nested bullet before the Gates bullet. After Task 14, before Task 15, a consistency sweep added the full path rule to the three sections and swapped the two workflow bullets (and re-copied the plugin mirror). The first final review (archive gate attempt 1) then found the same gap in Task 2 (adversarial), whose section pointed only at the skill's output-path guard, which refuses the `.claude/` skill, agent and command folders but not `.git/` or `.codegraph/`; the full rule was added there too. These five edits happened outside the per-task review loop; the ledger holds the `FINAL: issues` line of attempt 1 and the final review of attempt 2 reads the result.
- The old test `test_no_command_has_unattended_mode_section_after_p0` was replaced by `test_unattended_sections_match_the_listed_commands`, as Task 1 required. The new tests are listed in `./artifacts/ac-c3-compare.md`.
- The fresh worktree `.venv` had no `ruff`; the baselines were retaken after `uv pip install -e ".[dev]"` (see `./artifacts/t1-accepted-failures.md`). The pre-existing failure list is empty.

## Staging

`git add .dev/tasks` stages this report and every artifact of this package. Nothing under `.claude/` is staged. Nothing is committed or pushed by this plan.
