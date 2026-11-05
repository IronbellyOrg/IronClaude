b3a715d87785d0434ad57819a1c4373bef4dd17a
Review one task for spec compliance.

Task brief: Task T15 (plan file /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/TASK-WF-writeTheP1Static-20261105-033458.md, lines 269-290); AC ids T15.AC1 to T15.AC3 are the bullets under `Acceptance criteria:` in source order.

## Task 15: Run the P1 static checks and write the static report with the commit list for the owner's approval

Depends on: Task 14

Run these checks at the end of the static plan and save each output under `./artifacts/`:
- `make sync-dev` and then `make verify-sync` (AC-C2, exit 0) to `./artifacts/ac-c2.txt`;
- Check SCAN (AC-C1, prints nothing) to `./artifacts/ac-c1.txt`;
- `uv run pytest tests/skills/ -q -rf -p no:cacheprovider` compared with `./artifacts/ac-c3-baseline.txt` (AC-C3) to `./artifacts/ac-c3-compare.md`, which lists every baseline-passing test that now fails (must be none) and every new test;
- the wider run of Task 1 compared with `./artifacts/t1-baseline-wider.txt` to `./artifacts/wider-compare.md`, which, together with the AC-C3 comparison, lists the sixteen pre-existing test files of the Constraints (ten outside `tests/skills/`, six under it) and shows each passing;
- `git diff --cached --name-only | grep '^\.claude/' | grep -v '^\.claude/settings\.json$'` (AC-C4) to `./artifacts/ac-c4-index.txt`, which must be empty;
- Check ADDITIVE (AC-C5) for each of the sixteen converted command files and for `load.md`, saving one line per file to `./artifacts/ac-c5.txt`, with `business-panel.md` and `load.md` shown as the two named exemptions and their deletion counts (at most 4 and exactly 1);
- the AC-C6 command of spec section 7.1 to `./artifacts/ac-c6-depth-setting.txt`; every printed line must be `"nestedWorkerMaxDepth":1`, and a profile that prints nothing is recorded as using Orca's presumed default of 1;
- AC-1.1 (`uv run pytest tests/skills/test_worker_contract.py -q -p no:cacheprovider`) to `./artifacts/ac-1.1.txt`, and AC-1.4 (the two greps of Task 14) to `./artifacts/ac-1.4.txt`;
- `make lint` compared with `./artifacts/lint-baseline.txt`, and `uv run ruff format --check` on the five test files of Task 1 compared with `./artifacts/format-baseline.txt`, to `./artifacts/lint-format-compare.md`: a lint pass is `make lint` exit 0 with no new `ERROR` line and no new ruff finding; each new `WARN` line (for example a command file over 200 lines) is recorded in the compare file and does not fail; and no new unformatted file;
- `cmp` of the four workflow mirror pairs of Task 9 to `./artifacts/mirror-check.txt`, empty.

Write `./artifacts/p1-static-report.md`. It has one PASS or FAIL line, with its evidence file, for AC-1.1, AC-1.4, AC-C1, AC-C2, AC-C3, AC-C4, AC-C5, AC-C6, lint, format and the mirror check, and it lists: the twelve decisions D-P1-1 to D-P1-12 of the Constraints; the items marked UNVERIFIED in this plan (business-panel frontmatter loading, index knowledge-base mode, and whether `--report-dir` is accepted by commands that already have a directory flag as the spec's section 2.1 wording implies); the exact list of repo paths this plan created or changed, in these groups: command files, skill files, plugin mirrors, test files; the plugin command copies left unmirrored (the converted commands other than workflow, each marked identical to or already different from its source before this plan); the list of the sixteen commands with their report-directory flag, as the input to the P1 live plan; and the spec observations for the coordinator (a worker field named `command` collides with the existing key in graph and impact; the spec's status mapping has no entry for brainstorm's `dry-run`; the spec's brainstorm row passes the flag to nested calls from P2 while this plan does it in P1 (D-P1-4); the brief-flag table of `WORKER-CONTRACT.md` still describes the P0-era brief (it lists `/sc:index-repo` as none and `/sc:init-lite` with `--output <file>` only, and says that at P0 no command accepts the flag); WC-5's "before P1" override ends at P1 while the P2 commands troubleshoot, release-split and tdd still write no worker contract until P2). Finish the task with `git add .dev/tasks` so the report and every artifact are staged, and never stage a `.claude/` path.

Acceptance criteria:
- [T15.AC1] `./artifacts/p1-static-report.md` has a PASS or FAIL line for each of the eleven checks listed above, each naming an evidence file that exists under `./artifacts/`, and every line reads PASS.
- [T15.AC2] `./artifacts/ac-c4-index.txt` is empty and `git diff --cached --name-only -- .dev/tasks` lists this package's files.
- [T15.AC3] The repo-path list in the report equals the set of paths printed by `git status --short --untracked-files=all -- src tests plugins` (paths only, status letters dropped), so files that changed before this plan under `.dev/` are not compared.
Global constraints: (plan `## Constraints`, plan lines 17-44, verbatim)
## Constraints

- Spec: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` is called "the spec" below, and "spec section N" means its section N. `./source.md` is the inline brief that started this plan. The spec is the authority; where a task cites a section it names the rows the task needs. Decisions: `.dev/orca-command-refactor/decisions/APPROVED.md`, including the 2026-11-05 heartbeat decision (looser reading of spec section 7.2 step 5 condition 4; WC-10 unchanged; P0 verdict PASS). That decision changes nothing in this static plan; it governs how the later live plan reads heartbeat gaps.
- This is the static plan of Phase P1 (spec section 6, last paragraph: each phase plan has a static part and a live part). It covers AC-1.1 and AC-1.4 (spec section 7.3) and the common checks AC-C1 to AC-C6 (spec section 7.1). The live checks AC-1.2, AC-1.3, AC-1.5, AC-1.6, AC-1.7 and AC-1.8 and the P1 phase report belong to the P1 live plan, which is written after this plan's checks pass. P2 to P4 get their own plans later.
- No task in this plan commits, pushes, installs into `~/.claude`, starts an Orca worker, runs an Orca command or asks the owner a question. Between this plan and the live plan, the coordinator session asks the owner, commits and runs the install as spec section 7.2 states, outside any plan run. Nothing under the `.claude/` folder is staged, ever (repo `CLAUDE.md`, "Never Stage or Commit `.claude/` Contents"); `make sync-dev` writes only gitignored `.claude/` copies. `.dev/tasks/` is always staged (`git add .dev/tasks`); staging is not committing.
- `src/superclaude/` is the source of truth. Installed primitives use installed paths only: a new section or sentence never contains `src/superclaude/` and never names an Orca command (spec SA-2; Check SCAN below). The only file under `src/superclaude/core/` that describes the coordinator side is `WORKER-CONTRACT.md`, and this plan does not edit it. The brief-flag table in that file lists the P0-era constraints; the general "Report directory" rule in its section 1 already covers the extra report directory that `--unattended` needs for index-repo and init-lite, so no table row changes.
- Mirrors. UNVERIFIED item 8 of the spec is resolved by the repo's own rule (`src/superclaude/commands/README.md`, step 3): only `help.md`, `recommend.md`, `workflow.md` and `implement.md` are copied byte-for-byte to `plugins/superclaude/commands/`, and `tests/commands/test_workflow_command.py::test_plugin_mirror_matches_src` plus `tests/commands/test_routing_plugin_parity.py` pin them. Of the files this plan edits, only `workflow.md` and the `sc-workflow-protocol` skill (which has a plugin copy) are pinned, so only they are mirrored (Task 9). The other plugin command copies (brainstorm, build, document, index-repo, index, load and test are identical today; analyze, business-panel, design and explain already differ) are not touched.
- Section skeleton. Every `## Unattended mode` section is a level-2 heading written exactly like that, placed immediately before the file's first `## Boundaries` heading (business-panel.md has only `## CRITICAL BOUNDARIES` and uses that; index-repo.md has neither and the section goes after `## Output Format`; graph.md and impact.md name their own anchors in their tasks), and holds only the command's own resolutions. It contains, in this order: an opening sentence that names `~/.claude/WORKER-CONTRACT.md` as the home of the shared rules and tells the reader to read it first; the switch (applies only when `--unattended` is a standalone argument token outside any quoted argument, otherwise nothing in the section applies and no contract is written: spec SA-1 and SA-3); the report directory (exactly one of `--report-dir <dir>` or the command's own directory flag, named per task; if the command has none, `--report-dir` only; `--report-dir` follows the same path rules as the command's own directory flag where it has one: never inside `.git/` or `.codegraph/`, never under the distributable skill, agent or command folders of a `.claude/` folder, created if missing and writable; a report directory that fails them counts as no report directory known, so nothing is written there and the refusal is printed in chat only, as section 1 of `~/.claude/WORKER-CONTRACT.md` says); the contract (`<report-dir>/return-contract.yaml` written on every outcome with `worker_contract_version`, `worker_status`, `command`, `report_path`, `artifacts` and `reason` when failed, naming this command's deliverables for `report_path` and `artifacts`); the person-mode refusals of this command, in every spelling the command accepts (the short form `-i`, the `=` form such as `--format=interactive` or `--mode=socratic`) (refused before any work, contract `worker_status: failed` with the refused flag in `reason`); the gate resolutions of this command (for a no-gate command, the single statement that it has none); the nested invocations of this command (or "none"); and the outward-action rule (the command pushes, commits and stages nothing under `--unattended`, spec WC-9). The section never repeats the shared rules' wording, the exact error text or the status mapping; it points to the contract file.
- Test data. `tests/skills/test_worker_contract.py` gets one entry per command in a dict `UNATTENDED_EXPECT` (Task 1 creates it empty): the command name maps to a dict with `flags` (tokens its section must contain), `phrases` (further text it must contain) and `nested` (the names of the nested commands that receive `--unattended` from this command; an empty list for every command except brainstorm). Each command task adds its own entry in the same task, so the suite is green after every task.
- Check SCAN (spec AC-C1; run after every task that edits a command, skill or core file). Pass: prints nothing.

  ```sh
  grep -rniE '\borca(-ide)?[[:space:]]+(orchestration|worktree|terminal|agent)\b' \
    src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core \
    src/superclaude/hooks src/superclaude/templates plugins/superclaude \
    | grep -v '^src/superclaude/skills/ccsession-tag/' \
    | grep -v '^src/superclaude/core/WORKER-CONTRACT\.md:' \
    | grep -v '^src/superclaude/core/HOW-WE-WORK\.md:' \
    | grep -v '^plugins/superclaude/core/WORKER-CONTRACT\.md:' \
    | grep -v '^plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK\.md:'
  ```

- Check ADDITIVE (spec AC-C5 / SA-4). For every command file a task edits, `git diff --numstat "$(git merge-base master HEAD)" -- src/superclaude/commands/<name>.md | awk '$2 != 0'` prints nothing. Edits to command files are added lines; an existing line is never reworded. The only two command files exempt are `business-panel.md` (the frontmatter move deletes the fence lines) and `load.md` (the usage-line fix replaces one line); their tasks say so. Skill and test files have no such rule.
- Check WRITEVERB (spec AC-0.9). New text in any command or skill file must not contain the audit's write-verb phrases: `git add`, `git commit`, `git push`, `git merge`, `git stash`, `git update-ref`, `git worktree add` or `remove`, `gh pr`, `gh api`. The test `tests/skills/test_worker_contract.py::test_every_write_verb_hit_is_classified` and `::test_classification_table_has_no_stale_entries` must still pass, so no classified line is edited. The one classified P1 line is the `.dev/tasks/` staging sentence in `src/superclaude/skills/sc-workflow-protocol/SKILL.md` (category `deferred:P1`); it stays word for word.
- Test commands. Every pytest run in this plan passes `-p no:cacheprovider`. After every test, lint or sync run, `git status --short` shows no tracked file changed by the run itself. The wider test run always passes `--ignore=tests/cli/eval/test_perf_home_setup.py`, because that test rewrites a tracked evidence file. UV for every Python command; no bare `python`, `python3` or `pip`.
- Pre-existing tests that read the files this plan edits, and must still pass: `tests/commands/test_workflow_command.py`, `tests/commands/test_graph_command.py`, `tests/commands/test_impact_command.py`, `tests/commands/test_routing_plugin_parity.py`, `tests/skills/test_brainstorm_protocol.py`, `tests/skills/test_codegraph_adoption.py`, `tests/skills/test_primitive_dual_surface_lookup.py`, `tests/skills/test_tier2_tavily_consistency.py`, `tests/skills/test_repo_inventory_nongit.py`, `tests/skills/test_worker_contract.py`, `tests/cli_portify/test_brainstorm_gaps.py`, `tests/cli/test_init_lite.py`, `tests/unit/test_cli_install.py`, `tests/roadmap/test_threshold_registry.py`, `tests/core/test_how_we_work_routing_table.py` and `tests/recommend/test_routing_refresh.py`. The graph and impact tests pin frontmatter, section order and word lists; the workflow tests pin the `--output` retirement (every line of the command, skill or a ref that contains `--output` must also contain `retired`, `E-LEGACY` or `Never`).
- Decisions this plan makes where the spec is silent or ambiguous (each is also reported to the coordinator). D-P1-1: the spec can be read two ways for graph and impact. Its worker field `command` is the exact command line, but their own contracts already write a `command` key holding the short name (`graph`, `impact`). This plan keeps the existing key and value (spec WC-4: an existing contract keeps every existing field), counts it as the worker `command` field and adds no second key; the owner approved this on 2026-11-05 (decisions file, section "P1 owner decisions"). D-P1-2: for the seven report-style no-gate commands (analyze, build, design, explain, index, test, business-panel) `--output <file>` is new and optional; under `--unattended` without it the report goes to `<report-dir>/<name>-report.md`, so the contract always has a `report_path`. D-P1-3: brainstorm's own status `dry-run` maps to `worker_status: succeeded` with `report_path: null` (the spec's mapping list lacks it). D-P1-4: the nested propagation rule (spec section 2.1) is applied to brainstorm: its adversarial call and its `/sc:analyze` enrichment get `--unattended` and a nested report directory; research enrichment and the `tasklist` and `task` handoffs are skipped and recorded. The owner confirmed this on 2026-11-05 after an adversarial debate (decisions file, section "P1 owner decisions"): spec section 2.1's nested rule applies to every called command that accepts the flag in this phase, and the spec's "from P2" wording covers research enrichment only. D-P1-5: workflow skips a `--handoff implement` under `--unattended` (implement has gates and accepts the flag only in P4) and records it in the package contract as `partial` with an `unresolved` line; its reflect step runs as today (gate-free without `--remediate`). D-P1-6: graph refuses `init` under `--unattended`. D-P1-7: document requires an explicit `--output` for the external, api and guide types under `--unattended`. D-P1-8: a failing test suite is a verdict in the `/sc:test` report, not a failed run; `worker_status` is `failed` only when the runner could not run. D-P1-9: adversarial's `report_path` is its merged output (null when the merge was not reached). D-P1-10: cleanup-audit's `--pass all` final report is named `.claude-audit/final-report.md`. D-P1-11: init-lite writes the worker contract also on `--dry-run`, so the exception in its skill covers Safety Invariant 2 as well as 3 (the spec row names only 3). D-P1-12: a command's consent line is never answered under `--unattended` by assuming consent: analyze modifies no source and design changes no architecture; `/sc:test --fix` is the caller's consent for non-destructive fixes only, and a destructive change to a test file is never made; `/sc:index` overwrites no existing manual documentation and writes only the `--output` path the caller passed (or the default report file).
- Nothing in this plan edits `WORKER-CONTRACT.md`, `HOW-WE-WORK.md`, `KNOWN_CORE_FILES`, any agent file, any other command or skill, or any Python module under `src/superclaude/cli/`.
Start sha: b3a715d87785d0434ad57819a1c4373bef4dd17a
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/p1-static-report.md b/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/p1-static-report.md
new file mode 100644
index 00000000..44c1f802
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/p1-static-report.md
@@ -0,0 +1,141 @@
+# P1 static report
+
+Plan: `TASK-WF-writeTheP1Static-20261105-033458`. Scope: AC-1.1, AC-1.4 and AC-C1 to AC-C6 (spec sections 7.1 and 7.3). The live checks (AC-1.2, AC-1.3, AC-1.5 to AC-1.8) and the P1 phase report belong to the P1 live plan.
+
+## Check results
+
+- PASS AC-1.1: `tests/skills/test_worker_contract.py` passes (394 tests). Evidence: `./artifacts/ac-1.1.txt`.
+- PASS AC-1.4: adversarial SKILL names `<output>/adversarial/return-contract.yaml`; the workflow ref has the worker-contract section. Evidence: `./artifacts/ac-1.4.txt`.
+- PASS AC-C1: Check SCAN prints nothing. Evidence: `./artifacts/ac-c1.txt`.
+- PASS AC-C2: `make sync-dev` and `make verify-sync` both exit 0. Evidence: `./artifacts/ac-c2.txt`.
+- PASS AC-C3: No baseline-passing test fails (tests/skills 1109 -> 1255 passed; wider run 6616 -> 6621 passed); the sixteen named test files each pass. Evidence: `./artifacts/ac-c3-compare.md, wider-compare.md`.
+- PASS AC-C4: No `.claude/` path is staged. Evidence: `./artifacts/ac-c4-index.txt`.
+- PASS AC-C5: Sixteen converted command files additive except business-panel (14 added, 4 deleted, limit 4) and load (1 added, 1 deleted). Evidence: `./artifacts/ac-c5.txt`.
+- PASS AC-C6: 1 Orca profile line(s), each `"nestedWorkerMaxDepth":1`. Evidence: `./artifacts/ac-c6-depth-setting.txt`.
+- PASS lint: `make lint` exit 0, no new ERROR, ruff finding or WARN; one existing size WARN grew and is recorded below. Evidence: `./artifacts/lint-format-compare.md`.
+- PASS format: The five test files are formatted. Evidence: `./artifacts/lint-format-compare.md`.
+- PASS mirror check: The four workflow mirror pairs are byte-identical. Evidence: `./artifacts/mirror-check.txt`.
+
+Overall: PASS (11 of 11).
+
+Recorded WARN (does not fail): `make lint` already warned about `src/superclaude/commands/brainstorm.md` in the baseline (201 lines, threshold 200). The warning grew to 217 lines because of the 16-line Unattended mode section. There are 0 new WARN lines and the warning count stays 5. Evidence: `./artifacts/lint-format-compare.md`.
+
+## Decisions made where the spec was silent (D-P1-1 to D-P1-12)
+
+- D-P1-1: graph and impact keep their existing `command` key (short name) as the worker `command` field and add no second key (spec WC-4). Owner approved on 2026-11-05.
+- D-P1-2: for analyze, build, design, explain, index, test and business-panel, `--output <file>` is new and optional; under `--unattended` without it the report goes to `<report-dir>/<name>-report.md`.
+- D-P1-3: brainstorm's own status `dry-run` maps to `worker_status: succeeded` with `report_path: null`.
+- D-P1-4: the nested propagation rule is applied to brainstorm in P1 (its `/sc:analyze` enrichment and adversarial call get `--unattended` and a nested report directory under `nested/<command>-<n>/`; `<n>` starts at 1 and is never reused). Research enrichment and the `tasklist` and `task` handoffs are skipped and recorded. Owner confirmed on 2026-11-05 after an adversarial debate.
+- D-P1-5: workflow skips `--handoff implement` under `--unattended` and records the package contract as `partial` with an `unresolved` line; its reflect step runs without the flag.
+- D-P1-6: graph refuses `init` under `--unattended`.
+- D-P1-7: document requires an explicit `--output` for the external, api and guide types under `--unattended`.
+- D-P1-8: a failing test suite is a verdict in the `/sc:test` report, not a failed run; `worker_status` is `failed` only when the runner could not run.
+- D-P1-9: adversarial's `report_path` is its merged output (null when the merge was not reached).
+- D-P1-10: cleanup-audit's `--pass all` final report is `.claude-audit/final-report.md`.
+- D-P1-11: init-lite writes the worker contract also on `--dry-run`, so the exception in its skill covers Safety Invariant 2 as well as 3.
+- D-P1-12: a consent line is never answered by assuming consent under `--unattended` (analyze modifies no source, design changes no architecture, test `--fix` makes non-destructive fixes only, index overwrites no existing manual documentation).
+
+## UNVERIFIED items
+
+- Business-panel frontmatter loading: the frontmatter was moved out of a code fence (keys byte-identical, including the trailing spaces on line 6). Whether Claude Code now parses that frontmatter, or loaded it before, was not run. A test pins only that it is not inside a fence.
+- Index knowledge-base mode (`--type docs`): the section says it does not wait for a person under `--unattended`. Whether the mode ever waits was not run.
+- Whether `--report-dir` is accepted by commands that already have a directory flag (adversarial, brainstorm, graph, impact), as the spec's section 2.1 wording implies. Each of their sections says exactly one of the two flags is required and that `--report-dir` follows the path rules of the existing flag. No live run was made. The P1 live plan covers it.
+
+## Repo paths created or changed under `src`, `tests` and `plugins`
+
+The list equals the paths printed by `git status --short --untracked-files=all -- src tests plugins`.
+
+### Command files (17)
+
+- `src/superclaude/commands/adversarial.md`
+- `src/superclaude/commands/analyze.md`
+- `src/superclaude/commands/brainstorm.md`
+- `src/superclaude/commands/build.md`
+- `src/superclaude/commands/business-panel.md`
+- `src/superclaude/commands/cleanup-audit.md`
+- `src/superclaude/commands/design.md`
+- `src/superclaude/commands/document.md`
+- `src/superclaude/commands/explain.md`
+- `src/superclaude/commands/graph.md`
+- `src/superclaude/commands/impact.md`
+- `src/superclaude/commands/index-repo.md`
+- `src/superclaude/commands/index.md`
+- `src/superclaude/commands/init-lite.md`
+- `src/superclaude/commands/load.md`
+- `src/superclaude/commands/test.md`
+- `src/superclaude/commands/workflow.md`
+
+### Skill files (10)
+
+- `src/superclaude/skills/sc-adversarial-protocol/SKILL.md`
+- `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`
+- `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md`
+- `src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md`
+- `src/superclaude/skills/sc-graph-protocol/SKILL.md`
+- `src/superclaude/skills/sc-impact-protocol/SKILL.md`
+- `src/superclaude/skills/sc-init-lite-protocol/SKILL.md`
+- `src/superclaude/skills/sc-workflow-protocol/SKILL.md`
+- `src/superclaude/skills/sc-workflow-protocol/refs/input-parse.md`
+- `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md`
+
+### Plugin mirrors (4)
+
+- `plugins/superclaude/commands/workflow.md`
+- `plugins/superclaude/skills/sc-workflow-protocol/SKILL.md`
+- `plugins/superclaude/skills/sc-workflow-protocol/refs/input-parse.md`
+- `plugins/superclaude/skills/sc-workflow-protocol/refs/return-contract.md`
+
+### Test files (6)
+
+- `tests/commands/test_graph_command.py`
+- `tests/commands/test_impact_command.py`
+- `tests/commands/test_workflow_command.py`
+- `tests/recommend/test_routing_refresh.py`
+- `tests/skills/test_brainstorm_protocol.py`
+- `tests/skills/test_worker_contract.py`
+
+## Plugin command copies left unmirrored
+
+Only `workflow.md` and the `sc-workflow-protocol` skill files are mirrored (they are pinned by tests). For the other converted commands:
+
+- Identical to the source before this plan, now behind it: brainstorm, build, document, index-repo, index, test.
+- Already different from the source before this plan: analyze, business-panel, design, explain.
+- No plugin copy exists: adversarial, cleanup-audit, graph, impact, init-lite.
+
+## The sixteen commands and their report-directory flag (input to the P1 live plan)
+
+- adversarial: `--output <dir>` (`-o`) or `--report-dir <dir>`
+- brainstorm: `--output <dir>` (`-o`) or `--report-dir <dir>`
+- graph: `--output-dir <dir>` or `--report-dir <dir>`
+- impact: `--output-dir <dir>` or `--report-dir <dir>`
+- cleanup-audit: `--report-dir <dir>` only
+- index-repo: `--report-dir <dir>` only
+- init-lite: `--report-dir <dir>` only (`--output` names the report file)
+- workflow: `--report-dir <dir>` only (`--output` stays retired)
+- analyze: `--report-dir <dir>` only
+- build: `--report-dir <dir>` only
+- business-panel: `--report-dir <dir>` only
+- design: `--report-dir <dir>` only
+- document: `--report-dir <dir>` only (`--output` is the documentation path)
+- explain: `--report-dir <dir>` only
+- index: `--report-dir <dir>` only (`--output` is the documentation path)
+- test: `--report-dir <dir>` only
+
+## Spec observations for the coordinator
+
+- A worker field named `command` collides with the existing key in graph and impact (resolved by D-P1-1).
+- The spec's status mapping has no entry for brainstorm's `dry-run` (resolved by D-P1-3).
+- The spec's brainstorm row passes the flag to nested calls from P2, while this plan does it in P1 (D-P1-4, owner confirmed).
+- The brief-flag table of `WORKER-CONTRACT.md` still describes the P0-era brief: it lists `/sc:index-repo` as none and `/sc:init-lite` with `--output <file>` only, and says that at P0 no command accepts the flag. This plan did not edit that file.
+- WC-5's "before P1" override ends at P1, while the P2 commands troubleshoot, release-split and tdd still write no worker contract until P2.
+
+## Plan gaps and deviations found while running the plan
+
+- The pre-existing test `tests/recommend/test_routing_refresh.py` is in the plan's must-still-pass list but asserted that design has no `--output`, which contradicts Task 10 (design now declares `--output`). Its assertion was changed to `"--output" in` the Usage section. This file is outside Task 11's listed files and is an extra changed test file in the list above.
+- Tasks 3, 4 and 5 (brainstorm, graph, impact) first wrote a shorter `--report-dir` path rule than the plan's section skeleton requires, and Task 9 (workflow) put the Nested bullet before the Gates bullet. After Task 14, before Task 15, a consistency sweep added the full path rule to the three sections and swapped the two workflow bullets (and re-copied the plugin mirror). These four edits happened outside the per-task review loop; the final review reads the result.
+- The old test `test_no_command_has_unattended_mode_section_after_p0` was replaced by `test_unattended_sections_match_the_listed_commands`, as Task 1 required. The new tests are listed in `./artifacts/ac-c3-compare.md`.
+- The fresh worktree `.venv` had no `ruff`; the baselines were retaken after `uv pip install -e ".[dev]"` (see `./artifacts/t1-accepted-failures.md`). The pre-existing failure list is empty.
+
+## Staging
+
+`git add .dev/tasks` stages this report and every artifact of this package. Nothing under `.claude/` is staged. Nothing is committed or pushed by this plan.

diff --git a/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/ac-c3-compare.md b/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/ac-c3-compare.md
new file mode 100644
index 00000000..a6aecfa1
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/ac-c3-compare.md
@@ -0,0 +1,36 @@
+# AC-C3 compare (tests/skills/)
+
+- Baseline: 1109 passed in 14.13s (rc=0)
+- Current: 1255 passed in 12.66s (rc=0)
+- Baseline-passing tests that now fail: 0
+- Verdict: PASS
+
+## New test functions in this plan (all changed test files; parametrized cases add more ids)
+- tests/commands/test_graph_command.py::test_graph_skill_documents_worker_flags_and_contract
+- tests/commands/test_graph_command.py::test_graph_unattended_section_follows_init_section
+- tests/commands/test_impact_command.py::test_impact_skill_documents_worker_flags_fields_and_cap
+- tests/commands/test_impact_command.py::test_impact_unattended_section_between_outputs_and_boundaries
+- tests/commands/test_workflow_command.py::test_worker_flags_and_worker_contract_are_documented_in_refs
+- tests/skills/test_brainstorm_protocol.py::test_brainstorm_unattended_nested_directories_are_named
+- tests/skills/test_worker_contract.py::test_ac_1_4_assertion_holds
+- tests/skills/test_worker_contract.py::test_ac_1_4_check_fails_when_phrase_removed
+- tests/skills/test_worker_contract.py::test_business_panel_frontmatter_is_not_inside_a_code_fence
+- tests/skills/test_worker_contract.py::test_cleanup_audit_names_final_report_and_contract_write_exception
+- tests/skills/test_worker_contract.py::test_explain_declares_write_under_tool_coordination
+- tests/skills/test_worker_contract.py::test_index_repo_output_format_states_where_the_files_land
+- tests/skills/test_worker_contract.py::test_init_lite_contract_exception_and_pass_through_are_documented
+- tests/skills/test_worker_contract.py::test_load_usage_line_declares_checkpoint_and_load_is_not_converted
+- tests/skills/test_worker_contract.py::test_nested_check_fails_on_nested_text_without_a_nested_list
+- tests/skills/test_worker_contract.py::test_nested_propagation_text_matches_the_nested_list
+- tests/skills/test_worker_contract.py::test_no_section_check_fails_when_an_unconverted_command_has_one
+- tests/skills/test_worker_contract.py::test_only_brainstorm_lists_nested_commands
+- tests/skills/test_worker_contract.py::test_p1_command_set_is_complete
+- tests/skills/test_worker_contract.py::test_p1_set_check_fails_on_a_missing_extra_or_repeated_command
+- tests/skills/test_worker_contract.py::test_unattended_section_check_fails_on_synthetic_defects
+- tests/skills/test_worker_contract.py::test_unattended_section_check_fails_when_token_removed
+- tests/skills/test_worker_contract.py::test_unattended_section_check_forbids_nested_text_without_a_nested_list
+- tests/skills/test_worker_contract.py::test_unattended_section_content
+- tests/skills/test_worker_contract.py::test_unattended_section_helper_reads_only_its_own_section
+- tests/skills/test_worker_contract.py::test_unattended_sections_match_the_listed_commands
+- tests/skills/test_worker_contract.py::test_unconverted_command_has_no_unattended_section
+- !! REMOVED in tests/skills/test_worker_contract.py: ['test_no_command_has_unattended_mode_section_after_p0']

diff --git a/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/wider-compare.md b/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/wider-compare.md
new file mode 100644
index 00000000..05a70347
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/wider-compare.md
@@ -0,0 +1,25 @@
+# Wider run compare
+
+- Baseline: 6616 passed, 29 skipped, 1 xpassed, 5 warnings in 317.10s (0:05:17)
+- Current: 6621 passed, 29 skipped, 1 xpassed, 5 warnings in 318.35s (0:05:18) (rc=0)
+- Baseline-passing tests that now fail: 0
+- Verdict: PASS
+
+## The sixteen pre-existing test files of the Constraints (each run alone)
+
+- tests/commands/test_workflow_command.py: ============================== 18 passed in 0.25s ==============================
+- tests/commands/test_graph_command.py: ============================== 52 passed in 0.12s ==============================
+- tests/commands/test_impact_command.py: ============================== 81 passed in 0.11s ==============================
+- tests/commands/test_routing_plugin_parity.py: ============================== 5 passed in 0.03s ===============================
+- tests/skills/test_brainstorm_protocol.py: ============================== 2 passed in 0.02s ===============================
+- tests/skills/test_codegraph_adoption.py: ============================== 50 passed in 0.08s ==============================
+- tests/skills/test_primitive_dual_surface_lookup.py: ============================== 3 passed in 0.02s ===============================
+- tests/skills/test_tier2_tavily_consistency.py: ============================== 5 passed in 0.03s ===============================
+- tests/skills/test_repo_inventory_nongit.py: ============================== 5 passed in 0.25s ===============================
+- tests/skills/test_worker_contract.py: ============================= 394 passed in 0.66s ==============================
+- tests/cli_portify/test_brainstorm_gaps.py: ============================== 16 passed in 0.27s ==============================
+- tests/cli/test_init_lite.py: ============================== 44 passed in 0.33s ==============================
+- tests/unit/test_cli_install.py: ============================== 96 passed in 0.63s ==============================
+- tests/roadmap/test_threshold_registry.py: ============================== 23 passed in 5.38s ==============================
+- tests/core/test_how_we_work_routing_table.py: ============================== 79 passed in 0.21s ==============================
+- tests/recommend/test_routing_refresh.py: ============================= 248 passed in 1.45s ==============================

diff --git a/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/lint-format-compare.md b/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/lint-format-compare.md
new file mode 100644
index 00000000..2f80365c
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/lint-format-compare.md
@@ -0,0 +1,13 @@
+# Lint and format compare
+
+- make lint: baseline rc=0, current rc=0; ruff 'All checks passed!' = True
+- New ERROR lines: 0
+- New WARN lines (a warning for a file that had none in the baseline; recorded, do not fail): 0
+- Existing WARN lines whose size grew (recorded, do not fail): 1
+  - brainstorm.md: 201 lines in the baseline, 217 lines now
+- Warning count baseline: Warnings: 5; current: Warnings: 5
+- LINT verdict: PASS
+
+- ruff format --check (five test files): baseline rc=0, current rc=0
+- Current output: 5 files already formatted
+- FORMAT verdict: PASS

diff --git a/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/ac-c5.txt b/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/ac-c5.txt
new file mode 100644
index 00000000..3c40ee00
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/ac-c5.txt
@@ -0,0 +1,17 @@
+PASS adversarial.md added=14 deleted=0 (additive, limit 0 deleted)
+PASS brainstorm.md added=16 deleted=0 (additive, limit 0 deleted)
+PASS cleanup-audit.md added=17 deleted=0 (additive, limit 0 deleted)
+PASS graph.md added=15 deleted=0 (additive, limit 0 deleted)
+PASS impact.md added=13 deleted=0 (additive, limit 0 deleted)
+PASS index-repo.md added=19 deleted=0 (additive, limit 0 deleted)
+PASS init-lite.md added=17 deleted=0 (additive, limit 0 deleted)
+PASS workflow.md added=15 deleted=0 (additive, limit 0 deleted)
+PASS analyze.md added=14 deleted=0 (additive, limit 0 deleted)
+PASS build.md added=14 deleted=0 (additive, limit 0 deleted)
+PASS business-panel.md added=14 deleted=4 (exemption (frontmatter move), limit at most 4 deleted)
+PASS design.md added=14 deleted=0 (additive, limit 0 deleted)
+PASS document.md added=14 deleted=0 (additive, limit 0 deleted)
+PASS explain.md added=15 deleted=0 (additive, limit 0 deleted)
+PASS index.md added=15 deleted=0 (additive, limit 0 deleted)
+PASS test.md added=15 deleted=0 (additive, limit 0 deleted)
+PASS load.md added=1 deleted=1 (exemption (usage-line fix), limit exactly 1 deleted)

diff --git a/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/ac-c6-depth-setting.txt b/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/ac-c6-depth-setting.txt
new file mode 100644
index 00000000..4eb562fb
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/ac-c6-depth-setting.txt
@@ -0,0 +1,2 @@
+"nestedWorkerMaxDepth":1
+grep rc=0

diff --git a/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/ac-c2.txt b/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/ac-c2.txt
new file mode 100644
index 00000000..b4152966
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/ac-c2.txt
@@ -0,0 +1,227 @@
+🔄 Syncing src/superclaude/ → .claude/ for local development...
+✅ Sync complete.
+   Skills:    39 directories
+   Agents:    48 files
+   Commands:  46 files
+   Hooks:     13 files
+   Templates: 52 files
+sync-dev rc=0
+🔍 Verifying src/superclaude/ ↔ .claude/ sync...
+
+=== Skills ===
+  ✅ ccsession-tag
+  ✅ confidence-check
+  ✅ operational-guide
+  ✅ prd
+  ✅ readme
+  ✅ roadmap
+  ✅ sc-adversarial-protocol
+  ✅ sc-auggie-review-protocol
+  ✅ sc-bare-review
+  ✅ sc-brainstorm-protocol
+  ✅ sc-cleanup-audit-protocol
+  ✅ sc-cli-eval-protocol
+  ✅ sc-cli-portify-protocol
+  ✅ sc-crash-recovery
+  ✅ sc-graph-protocol
+  ✅ sc-impact-protocol
+  ✅ sc-implement-protocol
+  ✅ sc-init-lite-protocol
+  ✅ sc-issue-protocol
+  ✅ sc-pm-protocol
+  ✅ sc-post-release-protocol
+  ✅ sc-pr-submit-protocol
+  ✅ sc-recommend
+  ✅ sc-reflect-protocol
+  ✅ sc-release-split-protocol
+  ✅ sc-review-translation-protocol
+  ✅ sc-roadmap-protocol
+  ✅ sc-swarm-wizard-protocol
+  ✅ sc-task-protocol
+  ✅ sc-tasklist-protocol
+  ✅ sc-troubleshoot-protocol
+  ✅ sc-validate-roadmap-protocol
+  ✅ sc-validate-tests-protocol
+  ✅ sc-workflow-protocol
+  ✅ task-builder
+  ✅ task
+  ✅ tdd
+  ✅ tech-reference
+  ✅ tech-research
+
+=== Agents ===
+  ✅ audit-analyzer.md
+  ✅ audit-comparator.md
+  ✅ audit-consolidator.md
+  ✅ audit-scanner.md
+  ✅ audit-validator.md
+  ✅ auggie-reviewer.md
+  ✅ backend-architect.md
+  ✅ business-panel-experts.md
+  ✅ confidence-calibrator.md
+  ✅ debate-orchestrator.md
+  ✅ deep-research-agent.md
+  ✅ deep-research.md
+  ✅ devops-architect.md
+  ✅ eval-docs-loader.md
+  ✅ eval-run-reporter.md
+  ✅ eval-suite-author.md
+  ✅ evidence-validator.md
+  ✅ frontend-architect.md
+  ✅ implement-retry-adviser.md
+  ✅ issue-worker-t1.md
+  ✅ issue-worker-t2.md
+  ✅ issue-worker-t3.md
+  ✅ learning-guide.md
+  ✅ merge-executor.md
+  ✅ performance-engineer.md
+  ✅ pm-agent.md
+  ✅ python-expert.md
+  ✅ quality-engineer.md
+  ✅ refactoring-expert.md
+  ✅ reflect-reviewer.md
+  ✅ repo-index.md
+  ✅ requirements-analyst.md
+  ✅ reuse-auditor.md
+  ✅ rf-analyst.md
+  ✅ rf-assembler.md
+  ✅ rf-qa-qualitative.md
+  ✅ rf-qa.md
+  ✅ rf-task-builder.md
+  ✅ rf-task-executor.md
+  ✅ rf-task-researcher.md
+  ✅ rf-team-lead.md
+  ✅ root-cause-analyst.md
+  ✅ security-engineer.md
+  ✅ self-review.md
+  ✅ socratic-mentor.md
+  ✅ system-architect.md
+  ✅ technical-writer.md
+  ✅ troubleshoot-analyst.md
+
+=== Commands ===
+  ✅ adversarial.md
+  ✅ agent.md
+  ✅ analyze.md
+  ✅ auggie-review.md
+  ✅ brainstorm.md
+  ✅ build.md
+  ✅ business-panel.md
+  ✅ cleanup-audit.md
+  ✅ cleanup.md
+  ✅ cli-eval.md
+  ✅ cli-portify.md
+  ✅ design.md
+  ✅ document.md
+  ✅ explain.md
+  ✅ git.md
+  ✅ graph.md
+  ✅ help.md
+  ✅ impact.md
+  ✅ implement.md
+  ✅ improve.md
+  ✅ index-repo.md
+  ✅ index.md
+  ✅ init-lite.md
+  ✅ issue.md
+  ✅ load.md
+  ✅ pm.md
+  ✅ post-release.md
+  ✅ pr-submit.md
+  ✅ recommend.md
+  ✅ reflect.md
+  ✅ release-split.md
+  ✅ research.md
+  ✅ review-translation.md
+  ✅ roadmap.md
+  ✅ save.md
+  ✅ spawn.md
+  ✅ spec-panel.md
+  ✅ swarm-wizard.md
+  ✅ task.md
+  ✅ tasklist.md
+  ✅ tdd.md
+  ✅ test.md
+  ✅ troubleshoot.md
+  ✅ validate-roadmap.md
+  ✅ validate-tests.md
+  ✅ workflow.md
+
+=== Hooks ===
+  ✅ auggie-flag-clear.sh
+  ✅ block-bare-python.sh
+  ✅ codegraph-session-start.sh
+  ✅ freshness-file-changed.sh
+  ✅ freshness-post-read.sh
+  ✅ freshness-pre-edit.sh
+  ✅ freshness-session-start.sh
+  ✅ freshness-subagent-start.sh
+  ✅ freshness-subagent-stop.sh
+  ✅ freshness-user-prompt.sh
+  ✅ reject-workspace-writes.sh
+  ✅ sc-recommend-phase0.sh
+  ✅ pragmatic-subagent.js
+
+=== Templates ===
+  ✅ workflow/05_prd_template.md
+  ✅ workflow/03_project_plan_template.md
+  ✅ workflow/03_component_authoring_template.md
+  ✅ workflow/00_mdtm_template_simple_task.md
+  ✅ workflow/01_mdtm_template_generic_task__gfdoc.md
+  ✅ workflow/06_architecture_proposal_template.md
+  ✅ workflow/02_mdtm_template_complex_task.md
+  ✅ workflow/04_feature_brief_template.md
+  ✅ workflow/changelog_template.md
+  ✅ workflow/01_mdtm_template_generic_task.md
+  ✅ workflow/99_mdtm_template_generic_task_old.md
+  ✅ documents/prd_template.md
+  ✅ documents/operational_guide_template.md
+  ✅ documents/GFxAI_Master_Documentation_Template.md
+  ✅ documents/tdd_template.md
+  ✅ documents/agent_template_analysis.md
+  ✅ documents/supplemental-doc-creation-checklist.md
+  ✅ documents/agent_template_qa.md
+  ✅ documents/skill_template.md
+  ✅ documents/roadmap_template.md
+  ✅ documents/agent_template_worker.md
+  ✅ documents/release-spec-template.md
+  ✅ documents/supplemental_doc_template.md
+  ✅ documents/technical_reference_template.md
+  ✅ documents/readme_template.md
+  ✅ modularization-template-review/qa-fix-summary_template.md
+  ✅ modularization-template-review/qa-task-research-alignment_report_template.md
+  ✅ modularization-template-review/analyst-synthesis-review_report_template.md
+  ✅ modularization-template-review/research-notes_template.md
+  ✅ modularization-template-review/synthetic-dnsp-finding.contract
+  ✅ modularization-template-review/INDEX.md
+  ✅ modularization-template-review/qa-task-validation-structure_report_template.md
+  ✅ modularization-template-review/qa-cross-source-contradictions_template.md
+  ✅ modularization-template-review/track-scope-map_template.md
+  ✅ modularization-template-review/claim-evidence-matrix_template.md
+  ✅ modularization-template-review/qa-inventory_report_template.md
+  ✅ modularization-template-review/analyst-coverage-matrix_template.md
+  ✅ modularization-template-review/codebase-research_template.md
+  ✅ modularization-template-review/analyst-completeness_report_template.md
+  ✅ modularization-template-review/analyst-gap-analysis_template.md
+  ✅ modularization-template-review/qa-lens_report_template.md
+  ✅ modularization-template-review/qa-consolidated-findings_template.md
+  ✅ modularization-template-review/qa-task-validation-b2_report_template.md
+  ✅ modularization-template-review/qa-research-gap_report_template.md
+  ✅ modularization-template-review/qa-research-evidence_report_template.md
+  ✅ modularization-template-review/qa-qualitative-operational_report_template.md
+  ✅ modularization-template-review/qa-qualitative-sufficiency_report_template.md
+  ✅ modularization-template-review/analyst-cross-validation_report_template.md
+  ✅ modularization-template-review/qa-acceptance-methodology-audit_template.md
+  ✅ modularization-template-review/pipeline-complete_report_template.md
+  ✅ modularization-template-review/qa-source-fidelity_template.md
+  ✅ modularization-template-review/qa-research-depth_report_template.md
+  ✅ modularization-template-review/web-research_template.md
+
+=== Installer Registration ===
+  ✅ _FRESHNESS_SCRIPTS matches src/superclaude/hooks/scripts/*.sh and *.js
+
+=== Hooks Cross-Consistency ===
+  ✅ hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes
+
+✅ All components in sync.
+verify-sync rc=0

diff --git a/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/ac-c1.txt b/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/ac-c1.txt
new file mode 100644
index 00000000..e69de29b

diff --git a/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/ac-c4-index.txt b/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/ac-c4-index.txt
new file mode 100644
index 00000000..e69de29b

diff --git a/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/mirror-check.txt b/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/mirror-check.txt
new file mode 100644
index 00000000..e69de29b

diff --git a/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/ac-1.1.txt b/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/ac-1.1.txt
new file mode 100644
index 00000000..bdcb3dbc
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/ac-1.1.txt
@@ -0,0 +1,5 @@
+........................................................................ [ 81%]
+.......................................................................  [100%]
+
+============================= 394 passed in 0.70s ==============================
+rc=0

diff --git a/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/ac-1.4.txt b/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/ac-1.4.txt
new file mode 100644
index 00000000..d29bd2d2
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/ac-1.4.txt
@@ -0,0 +1,8 @@
+## grep adversarial SKILL
+385:    └── return-contract.yaml        # This skill's own return contract (every invocation)
+430:The contract is written to `<output>/adversarial/return-contract.yaml`, with the fields below under a `return_contract:` block, on every invocation including failures.
+2091:  file: "<output>/adversarial/return-contract.yaml (every invocation, failures included; the fields sit under a return_contract: block)"
+## grep workflow ref
+3:Write `.dev/tasks/to-do/<id>/return-contract.yaml`. Paths inside the package are package-relative (`./…`) so the file stays valid after the package moves to `done/`:
+45:Written to `<report-dir>/return-contract.yaml` (the one directory passed with `--report-dir`, never the package) on every outcome. The package contract above is unchanged.
+52:artifacts: [<package return-contract.yaml>, <package source.md>]   # [] before a package exists

Delta diff from the previous reviewed tree (empty on the first review): diff --git a/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/p1-static-report.md b/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/p1-static-report.md
index 5571afec..44c1f802 100644
--- a/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/p1-static-report.md
+++ b/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/p1-static-report.md
@@ -12,13 +12,13 @@ Plan: `TASK-WF-writeTheP1Static-20261105-033458`. Scope: AC-1.1, AC-1.4 and AC-C
 - PASS AC-C4: No `.claude/` path is staged. Evidence: `./artifacts/ac-c4-index.txt`.
 - PASS AC-C5: Sixteen converted command files additive except business-panel (14 added, 4 deleted, limit 4) and load (1 added, 1 deleted). Evidence: `./artifacts/ac-c5.txt`.
 - PASS AC-C6: 1 Orca profile line(s), each `"nestedWorkerMaxDepth":1`. Evidence: `./artifacts/ac-c6-depth-setting.txt`.
-- PASS lint: `make lint` exit 0, no new ERROR or ruff finding; one new WARN recorded below. Evidence: `./artifacts/lint-format-compare.md`.
+- PASS lint: `make lint` exit 0, no new ERROR, ruff finding or WARN; one existing size WARN grew and is recorded below. Evidence: `./artifacts/lint-format-compare.md`.
 - PASS format: The five test files are formatted. Evidence: `./artifacts/lint-format-compare.md`.
 - PASS mirror check: The four workflow mirror pairs are byte-identical. Evidence: `./artifacts/mirror-check.txt`.
 
 Overall: PASS (11 of 11).
 
-Recorded WARN (does not fail): `make lint` shows a new size warning for `src/superclaude/commands/brainstorm.md` (217 lines, threshold 200), caused by the 16-line Unattended mode section. The total warning count stays 5. Evidence: `./artifacts/lint-format-compare.md`.
+Recorded WARN (does not fail): `make lint` already warned about `src/superclaude/commands/brainstorm.md` in the baseline (201 lines, threshold 200). The warning grew to 217 lines because of the 16-line Unattended mode section. There are 0 new WARN lines and the warning count stays 5. Evidence: `./artifacts/lint-format-compare.md`.
 
 ## Decisions made where the spec was silent (D-P1-1 to D-P1-12)
 



diff --git a/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/lint-format-compare.md b/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/lint-format-compare.md
index 41f24f1f..2f80365c 100644
--- a/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/lint-format-compare.md
+++ b/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/lint-format-compare.md
@@ -2,8 +2,9 @@
 
 - make lint: baseline rc=0, current rc=0; ruff 'All checks passed!' = True
 - New ERROR lines: 0
-- New WARN lines (recorded, do not fail): 1
-  - ⚠️  WARN [Check 3]: brainstorm.md (217 lines, warn threshold 200)
+- New WARN lines (a warning for a file that had none in the baseline; recorded, do not fail): 0
+- Existing WARN lines whose size grew (recorded, do not fail): 1
+  - brainstorm.md: 201 lines in the baseline, 217 lines now
 - Warning count baseline: Warnings: 5; current: Warnings: 5
 - LINT verdict: PASS
 

Earlier blocking findings of this start (empty on the first review): F1.1 ac=T15.AC1 at=.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/p1-static-report.md:21 anchor=.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/lint-baseline.txt:57 chk=amiss:n,false:y,harm:n,constraint:n family=lint-warn-claim fix=Reword p1-static-report.md lines 15 and 21 and lint-format-compare.md line 5. brainstorm.md already had a size WARN in the baseline (201 lines). It grew to 217 lines, so it is not a new WARN. Say "one existing WARN grew from 201 to 217 lines; the WARN count stays 5" and report 0 new WARN lines. covers="each new `WARN` line (for example a command file over 200 lines) is recorded in the compare file": The report and the compare file call the brainstorm.md warning "new". lint-baseline.txt:57 shows `brainstorm.md (201 lines, warn threshold 200)`, so the warning was already there. The report's own "total warning count stays 5" contradicts it. This does not change the lint PASS.

Saved-probe re-check hit locations (may be empty): .dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/p1-static-report.md:21, .dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/p1-static-report.md:15, .dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/artifacts/lint-format-compare.md:5


Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
