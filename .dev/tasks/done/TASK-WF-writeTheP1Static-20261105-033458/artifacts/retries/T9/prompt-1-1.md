2adf057a1023f5c073648e94ca13b1978400fede
Review one task for spec compliance.

Task brief: Task T9 (plan file /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/TASK-WF-writeTheP1Static-20261105-033458.md, lines 179-192); AC ids T9.AC1 to T9.AC3 are the bullets under `Acceptance criteria:` in source order.

## Task 9: Convert `/sc:workflow`: section, worker contract for pre-creation STOPs, deferred staging, plugin mirrors

Depends on: Task 1

Files: `src/superclaude/commands/workflow.md`, `src/superclaude/skills/sc-workflow-protocol/SKILL.md`, `src/superclaude/skills/sc-workflow-protocol/refs/input-parse.md`, `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md`, their plugin copies `plugins/superclaude/commands/workflow.md`, `plugins/superclaude/skills/sc-workflow-protocol/SKILL.md`, `plugins/superclaude/skills/sc-workflow-protocol/refs/input-parse.md` and `plugins/superclaude/skills/sc-workflow-protocol/refs/return-contract.md`, `tests/commands/test_workflow_command.py` and `tests/skills/test_worker_contract.py`; spec section 3.1 row workflow, AC-1.4 and WC-9.

In `workflow.md`: add rows for `--unattended` and `--report-dir` to the Options table, one added example line to the Usage block (the existing usage lines and the `argument-hint` line are not edited), and the `## Unattended mode` section before `## Boundaries`. The section states: report directory is `--report-dir <dir>` only (the retired `--output` stays `E-LEGACY`; any line that mentions `--output` must also say "retired" or "Never"); the worker contract is `<report-dir>/return-contract.yaml`, written on every outcome including each pre-creation STOP (`E-NO-SOURCE`, `E-EMPTY-SOURCE`, `E-BAD-FLAG`, `E-LEGACY`, `E-PACKAGE-COLLISION`), with the STOP code in `reason`; once a package exists it lists the package's `return-contract.yaml` and `source.md` in `artifacts`, and the package's own rule for those STOPs (no package, no yaml) is unchanged; `report_path` is the plan `<id>.md`; the package statuses success, partial and failed map to succeeded, partial and failed; a `--handoff implement` is skipped (D-P1-5), recorded in the package contract as `partial` with one `unresolved` line; the reflect step runs as today, without `--unattended` and without `--remediate`; no person-mode flag and no other gate; the command does not stage `.dev/tasks` and leaves that to the coordinator (WC-9).

In `refs/input-parse.md` add a short "Worker flags" section: `--unattended` and `--report-dir <dir>` are removed from the arguments before the source is resolved and are never part of it; they are validated in the same pass as the other flags, before any write; under `--unattended` without exactly one report directory the command writes nothing and prints the contract's missing-directory error; under `--unattended` with a valid `--report-dir`, each pre-creation STOP also writes the worker contract. In `refs/return-contract.md` add a "Worker contract (`--unattended`)" section with the field list, the status mapping and the `artifacts` rule, leaving the existing "no package directory, no yaml" sentence unchanged. In `SKILL.md` add, after the `.dev/tasks/` paragraph of Wave 0 and without editing it, one paragraph saying that under `--unattended` that staging is deferred to the coordinator and naming `~/.claude/WORKER-CONTRACT.md`; the paragraph contains no Check WRITEVERB phrase. Then copy the four edited files byte-for-byte to the plugin paths (`cp`), and update the reason text of the `deferred:P1` classification entry for the `sc-workflow-protocol` `SKILL.md` staging line in `tests/skills/test_worker_contract.py` (same key, same category, reason now says the deferral is in force). Add this task's entry to `UNATTENDED_EXPECT`: flags `--handoff`; phrases `pre-creation`, `--handoff implement` and `does not stage`. Add tests to `tests/commands/test_workflow_command.py`: `refs/input-parse.md` has a "Worker flags" section that names `--report-dir`; `refs/return-contract.md` has the worker-contract section and still contains `no package directory, no yaml`; the plugin mirror test still passes. The `--output` retirement rule applies to every line this task adds to the command, the skill and the refs: a line that contains `--output` also says "retired" or "Never". The missing-report-directory refusal is the one of `~/.claude/WORKER-CONTRACT.md`; the refs never name it `E-MISSING-DIR` or `E-OUTPUT-PATH`, which the parse test forbids.

Acceptance criteria:
- [T9.AC1] `grep -c '^## Unattended mode$' src/superclaude/commands/workflow.md` prints `1`; `cmp src/superclaude/commands/workflow.md plugins/superclaude/commands/workflow.md` and the three `cmp` calls for the skill files print nothing.
- [T9.AC2] `uv run pytest tests/commands/test_workflow_command.py tests/commands/test_routing_plugin_parity.py tests/skills/test_worker_contract.py tests/skills/test_task_workspace_smoke.py tests/skills/test_task_workspace_lifecycle.py -q -p no:cacheprovider` passes, including `test_plugin_mirror_matches_src`, `test_output_flag_is_retired_everywhere` and the write-verb audit with the unchanged classified line.
- [T9.AC3] Check ADDITIVE prints nothing for `workflow.md`; Check SCAN prints nothing.
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
Start sha: 2adf057a1023f5c073648e94ca13b1978400fede
Diff against the start snapshot: diff --git a/src/superclaude/commands/workflow.md b/src/superclaude/commands/workflow.md
index 5dd4f263..4683d852 100644
--- a/src/superclaude/commands/workflow.md
+++ b/src/superclaude/commands/workflow.md
@@ -28,6 +28,7 @@ Exactly one source: an existing file path (`@path` ok) **or** leftover `$ARGUMEN
              [--strategy systematic|agile|enterprise]
              [--depth quick|standard|deep]
              [--handoff none|design|implement|tasklist]
+/sc:workflow <path-or-prompt> --unattended --report-dir <dir>   # worker mode, see Unattended mode
 ```
 
 ## Options
@@ -38,6 +39,8 @@ Exactly one source: an existing file path (`@path` ok) **or** leftover `$ARGUMEN
 | `--strategy` | `systematic` | `systematic` \| `agile` \| `enterprise`. Enterprise + omitted depth → `deep` |
 | `--depth` | `standard` | `quick` \| `standard` \| `deep` |
 | `--handoff` | `none` | `none` / `design` / `tasklist` = text; `implement` = Skill invoke |
+| `--unattended` | off | Worker mode: no step waits for a person; see Unattended mode |
+| `--report-dir` | none | With `--unattended`, the directory that holds the worker contract |
 
 Banned (`E-LEGACY`): `--parallel`, `--validate`, `--depth shallow|normal`, and the retired `--output` (every plan goes to a new `.dev/tasks/to-do/<id>/` package; there is no destination override).
 
@@ -60,6 +63,18 @@ The full behavioral specification is in `~/.claude/skills/sc-workflow-protocol/S
 /sc:workflow "add logout to the header" --handoff none
 ```
 
+## Unattended mode
+
+The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:workflow` resolves itself.
+
+- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument (an inline prompt is a quoted argument); otherwise nothing here applies and no worker contract is written.
+- **Report directory.** `--report-dir <dir>` only; the retired `--output` stays `E-LEGACY`. Without `--report-dir` the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
+- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome, including each pre-creation STOP (`E-NO-SOURCE`, `E-EMPTY-SOURCE`, `E-BAD-FLAG`, `E-LEGACY`, `E-PACKAGE-COLLISION`), with the STOP code in `reason`. The package's own rule for those STOPs (no package, no yaml) is unchanged. Once a package exists, the contract lists the package's `return-contract.yaml` and `source.md` in `artifacts`. `report_path` is the plan `<id>.md`. The package statuses success, partial and failed map to succeeded, partial and failed.
+- **Handoff.** A `--handoff implement` is skipped (the implement executor accepts the flag only in a later phase) and recorded in the package contract as `partial` with one `unresolved` line. The `design` and `tasklist` handoffs are text and unchanged.
+- **Nested invocations.** The reflect step runs as today, without `--unattended` and without `--remediate`; in that form it has no gate.
+- **Gates.** None else, and no person-mode flag.
+- **Outward actions.** The command does not stage `.dev/tasks` and leaves that to the coordinator; it pushes and commits nothing.
+
 ## Boundaries
 
 **Will:** create one new package `.dev/tasks/to-do/<id>/` holding `<id>.md` (schema `workflow-plan/1.2`), `source.md` snapshot and `return-contract.yaml` (1.1). Never overwrites an existing package. Run `/sc:reflect --mode pre` (advisory, read-only on the plan) as the last plan-generation step, before any `--handoff`.

diff --git a/src/superclaude/skills/sc-workflow-protocol/SKILL.md b/src/superclaude/skills/sc-workflow-protocol/SKILL.md
index b730cc9c..e74be08f 100644
--- a/src/superclaude/skills/sc-workflow-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-workflow-protocol/SKILL.md
@@ -27,6 +27,8 @@ STOP codes in the ref. No package, no plan file, no yaml on a pre-creation STOP.
 
 `.dev/tasks/` is always staged (`git add .dev/tasks`): the package and its `artifacts/` included. Never gitignore it, never leave it untracked, and never write "never stage" about it in a generated plan (Constraints included). Staging is not committing.
 
+Under `--unattended` that staging is deferred to the coordinator (`~/.claude/WORKER-CONTRACT.md`): this run does not stage `.dev/tasks`. Also apply the `## Unattended mode` section of the `workflow` command file: the installed copy `~/.claude/commands/sc/workflow.md`, or the project copy `.claude/commands/sc/workflow.md`.
+
 `--strategy enterprise` and omitted `--depth` → set `deep` + INFO.
 
 ## Wave 1 — Structure

diff --git a/src/superclaude/skills/sc-workflow-protocol/refs/input-parse.md b/src/superclaude/skills/sc-workflow-protocol/refs/input-parse.md
index 5988f1ee..311a22a1 100644
--- a/src/superclaude/skills/sc-workflow-protocol/refs/input-parse.md
+++ b/src/superclaude/skills/sc-workflow-protocol/refs/input-parse.md
@@ -11,6 +11,10 @@ Validate every input and flag **before any write**. These STOPs create no packag
 
 `--output` is **retired**: any `--output` / `--output=…` token → STOP `E-LEGACY` ("`--output` removed; every plan is written to `.dev/tasks/to-do/<id>/`"). It is never parsed as a destination.
 
+## Worker flags
+
+`--unattended` and `--report-dir <dir>` are removed from the arguments before the source is resolved and are never part of it. They are validated in the same pass as the other flags, before any write. Under `--unattended` without exactly one report directory (`--report-dir`; the retired `--output` is never a report directory) the command writes nothing and prints the refusal of `~/.claude/WORKER-CONTRACT.md` (rule WC-4). Under `--unattended` with a valid `--report-dir`, each pre-creation STOP of this ref also writes the worker contract `<report-dir>/return-contract.yaml` (fields in `refs/return-contract.md`); the STOP codes, and the rule that these STOPs create no package, are unchanged.
+
 ## Package identity
 
 Every generation creates one **new** package under the current checkout: `.dev/tasks/to-do/<id>/`. Regeneration never reuses, merges into, or overwrites an existing package.

diff --git a/src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md b/src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md
index aeaacc9a..337ca24b 100644
--- a/src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md
+++ b/src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md
@@ -39,3 +39,18 @@ A failed *generation* (no valid plan) and a failed *execution handoff* (valid pl
 STOPs before the package exists (`E-NO-SOURCE`, `E-EMPTY-SOURCE`, `E-LEGACY` including retired `--output`, `E-BAD-FLAG`, `E-PACKAGE-COLLISION`): chat only — **no package directory, no yaml**.
 
 After the package exists: any STOP → write the `failed` contract; delete a draft `<id>.md` that failed the gate.
+
+## Worker contract (`--unattended`)
+
+Written to `<report-dir>/return-contract.yaml` (the one directory passed with `--report-dir`, never the package) on every outcome. The package contract above is unchanged.
+
+```yaml
+worker_contract_version: "1"
+worker_status: succeeded | partial | failed
+command: <the exact command line>
+report_path: <repo path of the plan <id>.md, in to-do/ or, after an archive, done/> | null
+artifacts: [<package return-contract.yaml>, <package source.md>]   # [] before a package exists
+reason: <the STOP code or the failure>                              # only when failed
+```
+
+Status mapping: package `success` → `succeeded`, `partial` → `partial`, `failed` → `failed`. A pre-creation STOP → `failed` with the STOP code in `reason` and `report_path: null`. A skipped `--handoff implement` makes the package contract `partial` with one `unresolved` line.

diff --git a/plugins/superclaude/commands/workflow.md b/plugins/superclaude/commands/workflow.md
index 5dd4f263..4683d852 100644
--- a/plugins/superclaude/commands/workflow.md
+++ b/plugins/superclaude/commands/workflow.md
@@ -28,6 +28,7 @@ Exactly one source: an existing file path (`@path` ok) **or** leftover `$ARGUMEN
              [--strategy systematic|agile|enterprise]
              [--depth quick|standard|deep]
              [--handoff none|design|implement|tasklist]
+/sc:workflow <path-or-prompt> --unattended --report-dir <dir>   # worker mode, see Unattended mode
 ```
 
 ## Options
@@ -38,6 +39,8 @@ Exactly one source: an existing file path (`@path` ok) **or** leftover `$ARGUMEN
 | `--strategy` | `systematic` | `systematic` \| `agile` \| `enterprise`. Enterprise + omitted depth → `deep` |
 | `--depth` | `standard` | `quick` \| `standard` \| `deep` |
 | `--handoff` | `none` | `none` / `design` / `tasklist` = text; `implement` = Skill invoke |
+| `--unattended` | off | Worker mode: no step waits for a person; see Unattended mode |
+| `--report-dir` | none | With `--unattended`, the directory that holds the worker contract |
 
 Banned (`E-LEGACY`): `--parallel`, `--validate`, `--depth shallow|normal`, and the retired `--output` (every plan goes to a new `.dev/tasks/to-do/<id>/` package; there is no destination override).
 
@@ -60,6 +63,18 @@ The full behavioral specification is in `~/.claude/skills/sc-workflow-protocol/S
 /sc:workflow "add logout to the header" --handoff none
 ```
 
+## Unattended mode
+
+The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:workflow` resolves itself.
+
+- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument (an inline prompt is a quoted argument); otherwise nothing here applies and no worker contract is written.
+- **Report directory.** `--report-dir <dir>` only; the retired `--output` stays `E-LEGACY`. Without `--report-dir` the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
+- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome, including each pre-creation STOP (`E-NO-SOURCE`, `E-EMPTY-SOURCE`, `E-BAD-FLAG`, `E-LEGACY`, `E-PACKAGE-COLLISION`), with the STOP code in `reason`. The package's own rule for those STOPs (no package, no yaml) is unchanged. Once a package exists, the contract lists the package's `return-contract.yaml` and `source.md` in `artifacts`. `report_path` is the plan `<id>.md`. The package statuses success, partial and failed map to succeeded, partial and failed.
+- **Handoff.** A `--handoff implement` is skipped (the implement executor accepts the flag only in a later phase) and recorded in the package contract as `partial` with one `unresolved` line. The `design` and `tasklist` handoffs are text and unchanged.
+- **Nested invocations.** The reflect step runs as today, without `--unattended` and without `--remediate`; in that form it has no gate.
+- **Gates.** None else, and no person-mode flag.
+- **Outward actions.** The command does not stage `.dev/tasks` and leaves that to the coordinator; it pushes and commits nothing.
+
 ## Boundaries
 
 **Will:** create one new package `.dev/tasks/to-do/<id>/` holding `<id>.md` (schema `workflow-plan/1.2`), `source.md` snapshot and `return-contract.yaml` (1.1). Never overwrites an existing package. Run `/sc:reflect --mode pre` (advisory, read-only on the plan) as the last plan-generation step, before any `--handoff`.

diff --git a/plugins/superclaude/skills/sc-workflow-protocol/SKILL.md b/plugins/superclaude/skills/sc-workflow-protocol/SKILL.md
index b730cc9c..e74be08f 100644
--- a/plugins/superclaude/skills/sc-workflow-protocol/SKILL.md
+++ b/plugins/superclaude/skills/sc-workflow-protocol/SKILL.md
@@ -27,6 +27,8 @@ STOP codes in the ref. No package, no plan file, no yaml on a pre-creation STOP.
 
 `.dev/tasks/` is always staged (`git add .dev/tasks`): the package and its `artifacts/` included. Never gitignore it, never leave it untracked, and never write "never stage" about it in a generated plan (Constraints included). Staging is not committing.
 
+Under `--unattended` that staging is deferred to the coordinator (`~/.claude/WORKER-CONTRACT.md`): this run does not stage `.dev/tasks`. Also apply the `## Unattended mode` section of the `workflow` command file: the installed copy `~/.claude/commands/sc/workflow.md`, or the project copy `.claude/commands/sc/workflow.md`.
+
 `--strategy enterprise` and omitted `--depth` → set `deep` + INFO.
 
 ## Wave 1 — Structure

diff --git a/plugins/superclaude/skills/sc-workflow-protocol/refs/input-parse.md b/plugins/superclaude/skills/sc-workflow-protocol/refs/input-parse.md
index 5988f1ee..311a22a1 100644
--- a/plugins/superclaude/skills/sc-workflow-protocol/refs/input-parse.md
+++ b/plugins/superclaude/skills/sc-workflow-protocol/refs/input-parse.md
@@ -11,6 +11,10 @@ Validate every input and flag **before any write**. These STOPs create no packag
 
 `--output` is **retired**: any `--output` / `--output=…` token → STOP `E-LEGACY` ("`--output` removed; every plan is written to `.dev/tasks/to-do/<id>/`"). It is never parsed as a destination.
 
+## Worker flags
+
+`--unattended` and `--report-dir <dir>` are removed from the arguments before the source is resolved and are never part of it. They are validated in the same pass as the other flags, before any write. Under `--unattended` without exactly one report directory (`--report-dir`; the retired `--output` is never a report directory) the command writes nothing and prints the refusal of `~/.claude/WORKER-CONTRACT.md` (rule WC-4). Under `--unattended` with a valid `--report-dir`, each pre-creation STOP of this ref also writes the worker contract `<report-dir>/return-contract.yaml` (fields in `refs/return-contract.md`); the STOP codes, and the rule that these STOPs create no package, are unchanged.
+
 ## Package identity
 
 Every generation creates one **new** package under the current checkout: `.dev/tasks/to-do/<id>/`. Regeneration never reuses, merges into, or overwrites an existing package.

diff --git a/plugins/superclaude/skills/sc-workflow-protocol/refs/return-contract.md b/plugins/superclaude/skills/sc-workflow-protocol/refs/return-contract.md
index aeaacc9a..337ca24b 100644
--- a/plugins/superclaude/skills/sc-workflow-protocol/refs/return-contract.md
+++ b/plugins/superclaude/skills/sc-workflow-protocol/refs/return-contract.md
@@ -39,3 +39,18 @@ A failed *generation* (no valid plan) and a failed *execution handoff* (valid pl
 STOPs before the package exists (`E-NO-SOURCE`, `E-EMPTY-SOURCE`, `E-LEGACY` including retired `--output`, `E-BAD-FLAG`, `E-PACKAGE-COLLISION`): chat only — **no package directory, no yaml**.
 
 After the package exists: any STOP → write the `failed` contract; delete a draft `<id>.md` that failed the gate.
+
+## Worker contract (`--unattended`)
+
+Written to `<report-dir>/return-contract.yaml` (the one directory passed with `--report-dir`, never the package) on every outcome. The package contract above is unchanged.
+
+```yaml
+worker_contract_version: "1"
+worker_status: succeeded | partial | failed
+command: <the exact command line>
+report_path: <repo path of the plan <id>.md, in to-do/ or, after an archive, done/> | null
+artifacts: [<package return-contract.yaml>, <package source.md>]   # [] before a package exists
+reason: <the STOP code or the failure>                              # only when failed
+```
+
+Status mapping: package `success` → `succeeded`, `partial` → `partial`, `failed` → `failed`. A pre-creation STOP → `failed` with the STOP code in `reason` and `report_path: null`. A skipped `--handoff implement` makes the package contract `partial` with one `unresolved` line.

diff --git a/tests/commands/test_workflow_command.py b/tests/commands/test_workflow_command.py
index b44a4484..5beb52b7 100644
--- a/tests/commands/test_workflow_command.py
+++ b/tests/commands/test_workflow_command.py
@@ -129,6 +129,14 @@ def test_output_flag_is_retired_everywhere():
     assert "Validate every input and flag **before any write**" in parse
 
 
+def test_worker_flags_and_worker_contract_are_documented_in_refs():
+    parse, contract = _ref("input-parse.md"), _ref("return-contract.md")
+    worker_flags = parse.split("## Worker flags", 1)[1].split("\n## ", 1)[0]
+    assert "--report-dir" in worker_flags
+    assert "## Worker contract (`--unattended`)" in contract
+    assert "no package directory, no yaml" in contract
+
+
 def test_naming_and_collision_policy_is_specified():
     parse = _ref("input-parse.md")
     for token in (

diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index fe77bf5c..cc6dda9e 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -324,6 +324,11 @@ UNATTENDED_EXPECT: dict = {
         "phrases": ["the one write besides the report", "Safety Invariants 2 and 3"],
         "nested": [],
     },
+    "workflow": {
+        "flags": ["--handoff"],
+        "phrases": ["pre-creation", "--handoff implement", "does not stage"],
+        "nested": [],
+    },
 }
 
 # Commands with an `## Unattended mode` section after P1 (./source.md section 6
@@ -1679,7 +1684,7 @@ WRITE_VERB_CLASSIFICATION = {
         '`.dev/tasks/` is always staged (`git add .dev/tasks`): the package and its `artifacts/` included. Never gitignore it, never leave it untracked, and never write "never stage" about it in a generated plan (Constraints included). Staging is not committing.',
     ): (
         "deferred:P1",
-        "/sc:workflow is converted in P1; under --unattended its .dev/tasks staging defers to the coordinator (WC-9)",
+        "/sc:workflow is converted in P1; under --unattended the deferral of its .dev/tasks staging to the coordinator is in force (WC-9)",
     ),
     (
         "src/superclaude/skills/task/SKILL.md",

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
