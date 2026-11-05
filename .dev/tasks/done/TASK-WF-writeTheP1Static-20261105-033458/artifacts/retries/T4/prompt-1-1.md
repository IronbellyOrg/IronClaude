65634ea0d55ae718d3a35cfbe30226eb6495c0a0
Review one task for spec compliance.

Task brief: Task T4 (plan file /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/TASK-WF-writeTheP1Static-20261105-033458.md, lines 103-116); AC ids T4.AC1 to T4.AC3 are the bullets under `Acceptance criteria:` in source order.

## Task 4: Convert `/sc:graph`: section, `init` refused, worker fields beside the existing contract

Depends on: Task 1

Files: `src/superclaude/commands/graph.md`, `src/superclaude/skills/sc-graph-protocol/SKILL.md` and `tests/commands/test_graph_command.py`; spec section 3.1 row graph and the WC-4 mapping.

In `graph.md`: add rows for `--unattended` and `--report-dir` to the Options table and two example lines to the Usage block (new lines only; the `argument-hint` line is not edited, so the existing frontmatter test and Check ADDITIVE stay untouched), and add the `## Unattended mode` section after the `## Init (user-typed only)` section and before `## Boundaries` (the init section must stay intact: the tests split it at the next `## `). The section states: report directory is `--output-dir <dir>` or `--report-dir <dir>`, and under `--unattended` one of them is required (the screen-only default does not satisfy it); with `--output-dir` the worker fields are added to the existing `<output-dir>/return-contract.yaml` beside every existing field, and with `--report-dir` the skill writes `<report-dir>/return-contract.yaml` with the same existing fields plus the worker fields (the screen report stays the only report); `command` keeps its existing value (D-P1-1); own status success and partial map to succeeded and partial, failed to failed, and the flag-STOP `blocked` to failed with the STOP in `reason`; `report_path` is null (the report is the screen report); "`init` is refused" under `--unattended` (contract failed, `reason` says init runs only when the user types it; it also stops the `--worktree-local` form); the `status` form is the only form that runs; no other gate; no nested invocation; it runs no codegraph build command and pushes, commits and stages nothing. The section says, in those words, that the command "refuses init" under `--unattended`.

In `SKILL.md`: add `--unattended` and `--report-dir` rows to the flag table (`--report-dir` follows the `--output-dir` path rules; a positional `init` together with `--unattended` is a stop row: `status: blocked`, reason "init runs only when the user types it", written to the report directory and mapped to `worker_status: failed`; a stop yields no `init.form`, so the command's Init steps never run and `graph.md` needs no ordering change); edit step G-O and the heading "(only with `--output-dir`)" so the contract is written with `--output-dir` or, under `--unattended`, with `--report-dir`; in the `return-contract.yaml` section add one table row per worker field marked "only with `--unattended`"; and extend the `Will Not` line about writing so it also allows `<report-dir>/return-contract.yaml` under `--unattended`. Do not name any build or write verb in the skill (`test_graph_init_only_in_command`), and mention no path under `src/superclaude/` except the existing guide line (`test_graph_guide_lookup_line`). Add this task's entry to `UNATTENDED_EXPECT`: flags `--output-dir`; phrases `refuses init` and `report_path`. Add a test to `tests/commands/test_graph_command.py` that the new section lies after the Init section, that the skill's contract section names `worker_status`, and that the skill's flag table names `--unattended` and `--report-dir`.

Acceptance criteria:
- [T4.AC1] `grep -c '^## Unattended mode$' src/superclaude/commands/graph.md` prints `1`, and `uv run pytest tests/commands/test_graph_command.py tests/skills/test_worker_contract.py tests/skills/test_codegraph_adoption.py -q -p no:cacheprovider` passes, including every pre-existing graph test.
- [T4.AC2] `grep -n 'worker_status' src/superclaude/skills/sc-graph-protocol/SKILL.md` shows the new rows inside the `return-contract.yaml` section, and `grep -n -e '--report-dir' src/superclaude/skills/sc-graph-protocol/SKILL.md` shows the flag-table row, the step G-O text and the contract section.
- [T4.AC3] Check ADDITIVE prints nothing for `graph.md`; Check SCAN prints nothing.
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
Start sha: 65634ea0d55ae718d3a35cfbe30226eb6495c0a0
Diff against the start snapshot: diff --git a/src/superclaude/commands/graph.md b/src/superclaude/commands/graph.md
index 7159cf93..02df46aa 100644
--- a/src/superclaude/commands/graph.md
+++ b/src/superclaude/commands/graph.md
@@ -22,6 +22,8 @@ Codegraph usage rules: read `~/.claude/CODEGRAPH.md` (in a dev checkout without
 /sc:graph status --output-dir .dev/graph  # also write return-contract.yaml
 /sc:graph init                            # index this worktree (user-typed only)
 /sc:graph init --worktree-local           # nested worktree: build its own index instead of the parent's
+/sc:graph status --unattended --output-dir .dev/graph/run1   # worker mode: contract written there
+/sc:graph status --unattended --report-dir .dev/graph/run1   # worker mode: contract in the report directory
 ```
 
 ## Options
@@ -31,6 +33,8 @@ Codegraph usage rules: read `~/.claude/CODEGRAPH.md` (in a dev checkout without
 | `status` \| `init` | `status` | Positional subcommand. Any other word, or two positionals, STOPs with `status: blocked`. |
 | `--worktree-local` | `false` | Only with `init`: build a worktree-local index for a nested worktree that answers from the parent index. With `status` it STOPs. |
 | `--output-dir <dir>` | unset (screen only) | Write `return-contract.yaml` there. Must not be inside `.git/` or `.codegraph/` of the worktree. |
+| `--unattended` | `false` | Worker mode: no step waits for a person; see Unattended mode. |
+| `--report-dir <dir>` | unset | With `--unattended`, the directory that holds the worker contract (instead of `--output-dir`, never both). |
 
 There is no `--caller` flag: no skill calls `/sc:graph`. The skill also accepts an internal `--post-init <exit-code>` that only this command body passes after its init call.
 
@@ -52,6 +56,17 @@ These steps run only for `init`, after the skill's preflight returned `init.form
    Record the exit code. Never prefix the call with environment variables.
 3. **Verify.** Invoke `> Skill sc:graph-protocol` again with `status --post-init <exit-code>`, plus the user's `--output-dir` if given. The skill re-checks the index once and reports `success`, `partial` or `failed`.
 
+## Unattended mode
+
+The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:graph` resolves itself.
+
+- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument; otherwise nothing here applies and no worker contract is written.
+- **Report directory.** Exactly one of `--output-dir <dir>` or `--report-dir <dir>` is required; the screen-only default does not satisfy it, and both, or neither, is refused before any work. `--report-dir` follows the path rules of `--output-dir` (not inside `.git/` or `.codegraph/` of the worktree, created if missing and writable); a directory that fails them counts as no report directory known, so the refusal is printed in chat only.
+- **Contract.** With `--output-dir` the worker fields are added to the existing `<output-dir>/return-contract.yaml` beside every existing field. With `--report-dir` the skill writes `<report-dir>/return-contract.yaml` with the same existing fields plus the worker fields. The report is the screen report, so `report_path` is null. `command` keeps its existing value (`graph`). The own status values success and partial map to succeeded and partial, failed to failed, and the flag-STOP `blocked` to failed with the STOP in `reason`.
+- **Init.** The command refuses init under `--unattended` (contract failed; `reason` says init runs only when the user types it), also in its `--worktree-local` form. The skill stops before the Init steps of this file can start, so only the `status` form runs.
+- **Gates.** None else. Nested invocations: none.
+- **Outward actions.** It runs no codegraph build command and pushes, commits and stages nothing.
+
 ## Boundaries
 
 **Will:**

diff --git a/src/superclaude/skills/sc-graph-protocol/SKILL.md b/src/superclaude/skills/sc-graph-protocol/SKILL.md
index b6d1985b..4fbee179 100644
--- a/src/superclaude/skills/sc-graph-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-graph-protocol/SKILL.md
@@ -26,6 +26,8 @@ Indexing model (Phase 2): the session-start hook starts an init in every new che
 | `--worktree-local` | bool | `false` | only with `init` | given with `status` → "`--worktree-local` applies only to `init`" |
 | `--output-dir` | path | unset (screen only) | absolute after resolution; not inside `<worktree_root>/.git/` or `<worktree_root>/.codegraph/`; created if missing | inside `.git`/`.codegraph` → blocked; not creatable or writable → `status: failed`, reason printed only |
 | `--post-init <exit-code>` | int 0-255 | unset | set only by `commands/graph.md` after its init call; requires `status` | misuse can only fill the `init` block of the contract; it runs nothing |
+| `--unattended` | bool | `false` | standalone argument token outside any quoted argument; needs exactly one of `--output-dir` / `--report-dir` | a positional `init` with `--unattended` → `status: blocked`, reason "init runs only when the user types it", written to the report directory with `worker_status: failed` (`subcommand: init`, `init.requested: true`, `init.form: null`); no `init.form` is returned, so the Init steps of the command never run. Neither flag, or both → no work, refusal printed in chat only |
+| `--report-dir` | path | unset | only with `--unattended`; same rules as `--output-dir` | inside `.git`/`.codegraph` → blocked, printed in chat only; not creatable or writable → printed in chat only |
 
 There is no `--caller` flag.
 
@@ -61,7 +63,7 @@ There is no `--caller` flag.
    | `error` | `check_codegraph_error` | first error line, verbatim |
    | otherwise | `none` | "index ready" |
 
-5. **G-O Outputs.** Print the screen report. If `--output-dir` is set, write `<output-dir>/return-contract.yaml`.
+5. **G-O Outputs.** Print the screen report. If `--output-dir` is set, write `<output-dir>/return-contract.yaml`; under `--unattended` with `--report-dir`, write `<report-dir>/return-contract.yaml` instead (the same fields plus the worker fields).
 
 ## `init` (preflight only; the command body runs the build)
 
@@ -82,7 +84,7 @@ There is no `--caller` flag.
    `form: worktree_local` also needs the session's working directory to equal `worktree_root`; otherwise blocked, `refused_reason: cwd_mismatch`, and the report names the directory to run `/sc:graph init --worktree-local` from. The skill returns `init.form` to the command body and runs no build command.
 2. **G-V Re-check.** When the command body calls back with `status --post-init <exit-code>`, re-run G-R once and fill the `init` block (`ran: true`, `exit_code`).
 
-## `return-contract.yaml` (only with `--output-dir`)
+## `return-contract.yaml` (only with `--output-dir`, or with `--report-dir` under `--unattended`)
 
 | Field | Type | Allowed values / rule |
 |---|---|---|
@@ -91,7 +93,7 @@ There is no `--caller` flag.
 | `subcommand` | enum | `status` \| `init` (`init` whenever `--post-init` is set or the preflight ran) |
 | `status` | enum | `success` \| `partial` \| `blocked` \| `failed` |
 | `contract_path` | string | absolute path of this file |
-| `output_dir` | string | absolute |
+| `output_dir` | string | absolute (the report directory when `--report-dir` was given) |
 | `checked_at`, `access`, `index_state`, `worktree_root`, `worktree_relation`, `cli_version`, `pin`, `pin_match` | see Readiness check | |
 | `mcp_tools_listed` | bool | `true` when `mcp__codegraph__codegraph_callers` is in the tool list |
 | `counts` | map or null | `{files: int, nodes: int, edges: int}` |
@@ -106,6 +108,11 @@ There is no `--caller` flag.
 | `init.ran` | bool | `true` only when `--post-init` was given |
 | `init.exit_code` | int or null | |
 | `init.refused_reason` | enum or null | `disabled` \| `absent` \| `init_running` \| `already_initialized` \| `nested_worktree` \| `worktree_local_not_nested` \| `status_error` \| `cwd_mismatch` \| `null` |
+| `worker_contract_version` | string | `"1"` (only with `--unattended`) |
+| `worker_status` | enum | `succeeded` \| `partial` \| `failed` (only with `--unattended`); from `status`: `success` → `succeeded`, `partial` → `partial`, `failed` → `failed`, a flag STOP `blocked` → `failed` |
+| `report_path` | null | always `null`: the report is the screen report (only with `--unattended`) |
+| `artifacts` | list[string] | `[]`: the contract is the only file written (only with `--unattended`) |
+| `reason` | string | the STOP or refusal text, when `worker_status` is `failed` (only with `--unattended`) |
 
 Status rules: `status` → `success` only when `index_state: fresh`, `pin_match: true` and `mcp_tools_listed: true`; `partial` for any other state (the report is complete, the index is not ready); `blocked` for a flag STOP. `init` → `blocked` on a preflight refusal; `failed` when `init.exit_code` is not 0; `success` when exit 0 and the re-check reads `fresh`; `partial` when exit 0 but the re-check is not `fresh`.
 
@@ -155,4 +162,4 @@ Eight lines, fixed order:
 - Build, rebuild, sync or remove an index, or change telemetry or MCP registration
 - Run CLI `codegraph status` while `pgrep -f 'codegraph\.js (init|index)'` prints a line
 - Be called by another skill or agent
-- Write or Edit any file other than `<output-dir>/return-contract.yaml`
+- Write or Edit any file other than `<output-dir>/return-contract.yaml` (or `<report-dir>/return-contract.yaml` under `--unattended`)

diff --git a/tests/commands/test_graph_command.py b/tests/commands/test_graph_command.py
index 8152f6d5..61db300c 100644
--- a/tests/commands/test_graph_command.py
+++ b/tests/commands/test_graph_command.py
@@ -145,6 +145,19 @@ def test_graph_init_only_in_command():
     assert hits and all(h == "codegraph init" for h in hits)
 
 
+def test_graph_unattended_section_follows_init_section():
+    text = _text(_COMMAND)
+    init = text.index("## Init (user-typed only)")
+    assert init < text.index("## Unattended mode") < text.index("## Boundaries")
+
+
+def test_graph_skill_documents_worker_flags_and_contract():
+    skill = _text(_SKILL)
+    assert "worker_status" in _section(skill, "## `return-contract.yaml`")
+    flags = _section(skill, "## Inputs and flags")
+    assert "`--unattended`" in flags and "`--report-dir`" in flags
+
+
 def test_graph_init_user_typed_guard():
     init = _section(_text(_COMMAND), "## Init (user-typed only)")
     assert "/sc:graph init" in init

diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index 4878a2e3..81c0923a 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -295,6 +295,11 @@ UNATTENDED_EXPECT: dict = {
         ],
         "nested": ["analyze", "adversarial"],
     },
+    "graph": {
+        "flags": ["--output-dir"],
+        "phrases": ["refuses init", "report_path"],
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
