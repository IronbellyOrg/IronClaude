a07be8dcd1c742234d8e0c070804fdb5de05329d
Review one task for spec compliance.

Task brief: Task T5 (plan file /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/TASK-WF-writeTheP1Static-20261105-033458.md, lines 118-131); AC ids T5.AC1 to T5.AC3 are the bullets under `Acceptance criteria:` in source order.

## Task 5: Convert `/sc:impact`: section and worker fields beside the existing capped contract

Depends on: Task 1

Files: `src/superclaude/commands/impact.md`, `src/superclaude/skills/sc-impact-protocol/SKILL.md` and `tests/commands/test_impact_command.py`; spec section 3.1 row impact and the WC-4 mapping.

In `impact.md`: add rows for `--unattended` and `--report-dir` to the Options table and one example line to the Usage block (new lines only; the `argument-hint` line is not edited), and add the `## Unattended mode` section before `## Boundaries` and after `## Outputs`. The section states: report directory is `--output-dir <dir>` or `--report-dir <dir>`; under `--unattended` the brief passes an explicit `--output-dir` or `--report-dir` (the default `<worktree>/.dev/impact/...` directory does not satisfy it); with `--output-dir` the worker fields (`worker_contract_version`, `worker_status`, `artifacts`, and `reason` when failed) are added to the existing `<output-dir>/return-contract.yaml` beside every existing field, and with `--report-dir` alone `impact.md` and the command's own contract stay in the default directory while the skill writes `<report-dir>/return-contract.yaml` with the existing fields plus the worker fields, listing `impact.md` and the own contract in `artifacts`; `command` and `report_path` keep their existing values (D-P1-1; `report_path` is already `impact.md`); own status success, partial, failed and `blocked` map to succeeded, partial, failed and failed (flag STOP in `reason`); no gate, since the command never stops its caller and falls back to Grep; no nested invocation; it edits no code, runs no tests and pushes, commits and stages nothing.

In `SKILL.md`: add `--unattended` and `--report-dir` rows to the flag table (`--report-dir` follows the `--output-dir` path rules); edit step 10 and the write-scope sentence so that, under `--unattended`, the skill also writes `<report-dir>/return-contract.yaml` (the existing outputs are written as today); in section 5 add the worker fields as rows marked "only with `--unattended`" and state that they count toward the existing 6 KB cap (the cap itself is unchanged). Add this task's entry to `UNATTENDED_EXPECT`: flags `--output-dir`; phrases `explicit`. Add a test to `tests/commands/test_impact_command.py` that the skill's flag table names `--unattended` and `--report-dir`, that its section 5 names `worker_status` and still states the 40-row and 6 KB cap, and that `## Unattended mode` precedes `## Boundaries`.

Acceptance criteria:
- [T5.AC1] `grep -c '^## Unattended mode$' src/superclaude/commands/impact.md` prints `1`, and `uv run pytest tests/commands/test_impact_command.py tests/skills/test_worker_contract.py tests/skills/test_codegraph_adoption.py -q -p no:cacheprovider` passes, including every pre-existing impact test (section order, closed token list, no mutating verbs).
- [T5.AC2] `grep -n '6 KB' src/superclaude/skills/sc-impact-protocol/SKILL.md` still shows the cap and shows the new worker-field sentence, and `grep -n -e '--report-dir' src/superclaude/skills/sc-impact-protocol/SKILL.md` shows the flag-table row, step 10 and the write-scope sentence.
- [T5.AC3] Check ADDITIVE prints nothing for `impact.md`; Check SCAN prints nothing.
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
Start sha: a07be8dcd1c742234d8e0c070804fdb5de05329d
Diff against the start snapshot: diff --git a/src/superclaude/commands/impact.md b/src/superclaude/commands/impact.md
index adb245c9..a82df3e2 100644
--- a/src/superclaude/commands/impact.md
+++ b/src/superclaude/commands/impact.md
@@ -22,6 +22,7 @@ Codegraph usage rules: read `~/.claude/CODEGRAPH.md` (in a dev checkout without
 /sc:impact --diff                               # symbols changed in the working tree vs HEAD
 /sc:impact --diff origin/master --tests         # symbols a branch changed, plus advisory tests
 /sc:impact parse_config --caller sc-implement-protocol --output-dir .dev/impact/t3
+/sc:impact parse_config --unattended --report-dir .dev/impact/run1   # worker mode: contract written there
 ```
 
 ## Options
@@ -36,6 +37,8 @@ Codegraph usage rules: read `~/.claude/CODEGRAPH.md` (in a dev checkout without
 | `--test-depth` | codegraph's own | 1-5, only with `--tests`. |
 | `--output-dir` | `<worktree>/.dev/impact/<slug>-<timestamp>/` | Where `impact.md` and `return-contract.yaml` are written. Never inside `.git/` or `.codegraph/`. |
 | `--caller` | unset | Name of the calling skill; shortens chat output to three lines (status, degraded tokens, contract path). |
+| `--unattended` | `false` | Worker mode: no step waits for a person; see Unattended mode. |
+| `--report-dir` | unset | With `--unattended`, the directory that holds the worker contract (instead of `--output-dir`, never both). |
 
 ## Activation
 
@@ -49,6 +52,16 @@ Pass the user's arguments unchanged. Do NOT proceed with protocol execution usin
 - `<output-dir>/impact.md`: the human report (12 fixed sections).
 - `<output-dir>/return-contract.yaml`: the capped machine contract (at most 40 dependent rows, 6 KB). Calling skills read only this file.
 
+## Unattended mode
+
+The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:impact` resolves itself.
+
+- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument; otherwise nothing here applies and no worker contract is written.
+- **Report directory.** Exactly one of `--output-dir <dir>` or `--report-dir <dir>`, passed explicitly: the default `<worktree>/.dev/impact/...` directory does not satisfy it, and both, or neither, is refused before any work. `--report-dir` follows the path rules of `--output-dir` (never inside `.git/` or `.codegraph/`, created if missing and writable); a directory that fails them counts as no report directory known, so the refusal is printed in chat only.
+- **Contract.** With `--output-dir` the worker fields (`worker_contract_version`, `worker_status`, `artifacts`, and `reason` when failed) are added to the existing `<output-dir>/return-contract.yaml` beside every existing field. With `--report-dir` alone, `impact.md` and the command's own contract stay in the default directory, and the skill writes `<report-dir>/return-contract.yaml` with the existing fields plus the worker fields, listing `impact.md` and the own contract in `artifacts`. `command` and `report_path` keep their existing values (`report_path` is already `impact.md`). The own status values success, partial and failed map to succeeded, partial and failed, and a flag-STOP `blocked` maps to failed with the STOP in `reason`.
+- **Gates.** None: the command never stops its caller and falls back to Grep. Nested invocations: none.
+- **Outward actions.** It edits no code, runs no tests, and pushes, commits and stages nothing.
+
 ## Boundaries
 
 **Will:**

diff --git a/src/superclaude/skills/sc-impact-protocol/SKILL.md b/src/superclaude/skills/sc-impact-protocol/SKILL.md
index 40c56f5c..c580aa74 100644
--- a/src/superclaude/skills/sc-impact-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-impact-protocol/SKILL.md
@@ -18,7 +18,7 @@ Codegraph usage rules: read `~/.claude/CODEGRAPH.md` (in a dev checkout without
 
 ## 1. Flags (step 1 validates them)
 
-| Flag | Default | Validation | STOP → `status: blocked` (contract still written when `--output-dir` resolves) |
+| Flag | Default | Validation | STOP → `status: blocked` (contract still written when `--output-dir` resolves, or `--report-dir` under `--unattended`) |
 |---|---|---|---|
 | `<symbol>...` | none | 1-30 items, each `^[A-Za-z_$][A-Za-z0-9_$]*$` | none and no `--diff`; both symbols and `--diff`; more than 30; a dotted or path-qualified name ("pass the bare name; codegraph has no `Class/method` addressing") |
 | `--diff [<base>]` | `HEAD` when given without a value | `git rev-parse --verify --quiet <base>^{commit}` succeeds | the ref does not resolve |
@@ -28,6 +28,8 @@ Codegraph usage rules: read `~/.claude/CODEGRAPH.md` (in a dev checkout without
 | `--test-depth` | unset | integer 1-5, only with `--tests` | without `--tests`; outside 1-5 |
 | `--output-dir` | `<worktree_root>/.dev/impact/<slug>-<YYYYMMDDTHHMMSSZ>/`; `<slug>` = first symbol or `diff-<base>`, lowercased, non-alphanumerics → `-`, max 40 chars | absolute after resolution; not inside `.git/` or `.codegraph/`; created if missing; existing outputs are overwritten | inside `.git`/`.codegraph` → blocked; not creatable or writable → `status: failed`, reason printed |
 | `--caller` | unset | `^[a-z0-9][a-z0-9:-]{0,63}$` | malformed |
+| `--unattended` | `false` | standalone argument token outside any quoted argument; needs exactly one of `--output-dir` / `--report-dir`, passed explicitly | neither or both (the default directory does not satisfy it) → no work, the refusal is printed in chat only |
+| `--report-dir` | unset | only with `--unattended`; same rules as `--output-dir` | inside `.git`/`.codegraph` → blocked, printed in chat only; not creatable or writable → printed in chat only |
 
 With `--caller` set, chat output is three lines: status, `degraded`, contract path. Without it, print the `## Summary` table of `impact.md`.
 
@@ -46,7 +48,7 @@ With `--caller` set, chat output is three lines: status, `degraded`, contract pa
 | 7 | Call-site confirmation | the guide's call-site procedure CS1-CS5 (section 4 below) for the rows shown in `impact.md` tables: first 5 `prod` rows with `hop: 1` per symbol (sort order of step 10), at most 20 per run. A `hop` 2 row (step 5) is never confirmed: its body need not call the queried symbol, so it keeps `resolution: def-line`, is cited only as a definition and is never dropped by CS5 | `resolution: call-site-verified` with `call_site_line`; rows over the budget stay `def-line` (graph) or `unresolved` (grep) and are only counted (token `graph:unresolved`); failing rows are dropped from the tables and counted in `call_sites.dropped` |
 | 8 | Tests (only `--tests`) | changed files = definition files (symbol mode) or D1 files that exist (diff mode); `codegraph affected <file>... --json --quiet` (+ `--depth <--test-depth>`), files as arguments, never a pipeline | `tests[]` with `source: affected`. Heuristic: for each changed `<stem>.<ext>`, Glob `**/test_<stem>.*`, `**/<stem>_test.*`, `**/<stem>.test.*`, `**/<stem>.spec.*`, plus every `test` partition file of steps 4-5 → `source: heuristic`; both → `both`. `selection_source: advisory` when `affected` contributed, else `heuristic_only`. Unparsable JSON → `graph:parse_failed`, heuristic only. Skipped when `index_state` is not `fresh` or `stale` |
 | 9 | Grep fallback (lookups not allowed in step 2, or the CLI transport failed) | symbol mode: Grep `(^|[^A-Za-z0-9_$])<sym>\s*\(` over the worktree, excluding `.git/`, `.codegraph/`, `.dev/`; cap 100 hits per symbol. Diff mode: D1 and D2 still run (git only); D3-D4 need codegraph and do not run, so no symbol is derived | symbol mode: rows `source: grep`, `resolution: unresolved`, `caller: null`, partition by step 6; definitions from the step-3 Grep. Diff mode: every D1 file goes to `unmapped_files[]` with `reason: no_graph`, no dependent row is invented, and step 8's heuristic still uses the D1 files. `status: partial` |
-| 10 | Write outputs | Write `<output-dir>/impact.md` (section 6), then `<output-dir>/return-contract.yaml` (section 5) | rows sorted by `symbol`, `partition` (prod first), `file`, `def_line`; the contract holds at most 40 dependent rows and 6 KB, the rest only in `impact.md` |
+| 10 | Write outputs | Write `<output-dir>/impact.md` (section 6), then `<output-dir>/return-contract.yaml` (section 5); under `--unattended` with `--report-dir` also `<report-dir>/return-contract.yaml` (the existing fields plus the worker fields, listing `impact.md` and the own contract in `artifacts`) | rows sorted by `symbol`, `partition` (prod first), `file`, `def_line`; the contract holds at most 40 dependent rows and 6 KB, the rest only in `impact.md` |
 
 Sort before the step-7 selection, so the confirmed rows are deterministic. Same inputs and the same index give byte-identical files.
 
@@ -94,6 +96,12 @@ Every row carries `resolution: def-line|call-site-verified|unresolved`. Rows are
 | `tests[]` | list[map] or `[]` | with `--tests`: `{path, source: heuristic \| affected \| both}`, sorted by path |
 | `selection_source` | enum or null | `advisory` \| `heuristic_only`; `null` without `--tests` |
 | `errors[]` | list[string] | one line per failed call, verbatim first line |
+| `worker_contract_version` | string | `"1"` (only with `--unattended`) |
+| `worker_status` | enum | `succeeded` \| `partial` \| `failed` (only with `--unattended`); from `status`: `success` → `succeeded`, `partial` → `partial`, `failed` → `failed`, a flag STOP `blocked` → `failed` |
+| `artifacts` | list[string] | other files written: `[]` with `--output-dir`; `impact.md` and the own contract with `--report-dir` (only with `--unattended`) |
+| `reason` | string | the STOP or failure text, when `worker_status` is `failed` (only with `--unattended`) |
+
+The contract holds at most 40 dependent rows and 6 KB. The worker fields (only with `--unattended`) count toward that 6 KB cap; the cap itself is unchanged.
 
 Status merge, `failed > blocked > partial > success`:
 
@@ -179,7 +187,7 @@ The run continues, outputs are written, and the caller is never stopped.
 
 ## Will Not
 
-- Edit code, run tests, or build, sync or remove an index (Write and Edit touch only `impact.md` and `return-contract.yaml` under `--output-dir`)
+- Edit code, run tests, or build, sync or remove an index (Write and Edit touch only `impact.md` and `return-contract.yaml` under `--output-dir`, and `<report-dir>/return-contract.yaml` under `--unattended`)
 - Use a file-mode `codegraph_node` call without `"symbolsOnly": true`
 - Run CLI `codegraph status` while `pgrep -f 'codegraph\.js (init|index)'` prints a line
 - Prefix a CLI call with environment variables

diff --git a/tests/commands/test_impact_command.py b/tests/commands/test_impact_command.py
index 295699a5..c5b81388 100644
--- a/tests/commands/test_impact_command.py
+++ b/tests/commands/test_impact_command.py
@@ -257,6 +257,24 @@ def test_impact_advisory_rule():
     assert "no consumer may change a severity, gate or verdict" in advisory
 
 
+def test_impact_unattended_section_between_outputs_and_boundaries():
+    text = _text(_COMMAND)
+    assert (
+        text.index("## Outputs")
+        < text.index("## Unattended mode")
+        < text.index("## Boundaries")
+    )
+
+
+def test_impact_skill_documents_worker_flags_fields_and_cap():
+    skill = _text(_SKILL)
+    flags = _section(skill, "## 1. Flags")
+    assert "`--unattended`" in flags and "`--report-dir`" in flags
+    contract = _section(skill, "## 5. `return-contract.yaml`")
+    assert "worker_status" in contract
+    assert "40 dependent rows" in contract and "6 KB" in contract
+
+
 def test_impact_status_only_cli_transport_before_grep_fallback():
     steps = _section(_text(_SKILL), "## 2. Step sequence")
     cli = steps.index("Status-only branch transport")

diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index 81c0923a..1b262ce0 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -300,6 +300,11 @@ UNATTENDED_EXPECT: dict = {
         "phrases": ["refuses init", "report_path"],
         "nested": [],
     },
+    "impact": {
+        "flags": ["--output-dir"],
+        "phrases": ["explicit"],
+        "nested": [],
+    },
 }
 
 # Commands with an `## Unattended mode` section after P1 (./source.md section 6

Delta diff from the previous reviewed tree (empty on the first review): (empty)
Earlier blocking findings of this start (empty on the first review): (empty)
Saved-probe re-check hit locations (may be empty): (empty)

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
