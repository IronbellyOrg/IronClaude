d9e07ac03f797d7e8752e18927555da8b2083805
Review one task for spec compliance.

Task brief: Task T3 (plan file /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1/.dev/tasks/to-do/TASK-WF-writeTheP1Static-20261105-033458/TASK-WF-writeTheP1Static-20261105-033458.md, lines 88-101); AC ids T3.AC1 to T3.AC3 are the bullets under `Acceptance criteria:` in source order.

## Task 3: Convert `/sc:brainstorm`: section, research enrichment off, nested adversarial and analyze calls

Depends on: Task 1

Files: `src/superclaude/commands/brainstorm.md`, `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`, `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md` and `tests/skills/test_brainstorm_protocol.py`; spec section 3.1 row brainstorm, AC-1.1 (research enrichment) and the nested propagation rule (spec section 2.1).

In `brainstorm.md`: add rows for `--unattended` and `--report-dir` to the Options table, one added example line after the existing lines of the Usage block (no existing line is reworded), and the `## Unattended mode` section before `## Boundaries`. The section states, with these exact phrases: report directory is `--output <dir>` or `--report-dir <dir>`; the worker fields are added to the command's own `<output>/return-contract.yaml` beside every existing field, including its own `status`, and with `--report-dir` instead the worker contract is a separate `<report-dir>/return-contract.yaml` that lists the own contract in `artifacts`; `report_path` is `merged-requirements.md` (null when not reached or on dry-run); own status success, partial, failed and dry-run map to succeeded, partial, failed and succeeded (D-P1-3); `--interactive` and its short form `-i` are refused (`-o` is the short form of `--output`) and the Socratic dialogue proceeds on best available context (no other gate); the output directory is used "exactly as passed", never with the usual `-N` suffix, and a directory (the output or the report directory) that already holds a `return-contract.yaml` is refused before any work as no usable report directory, chat only, so no earlier contract is overwritten; the worker contract is written on every other outcome, including each stop of the skill's Wave 0 (the stop text goes to `reason`), and the Wave 0 handoff-prerequisite stop (step 7) is skipped under `--unattended` because the `tasklist` and `task` handoffs are skipped; "research enrichment is off" under `--unattended`, which covers the automatic route and an explicit `--research light` or `--research deep`, each recorded in `enrichment_used` with `quality_tier: skipped`; nested invocations: the `/sc:analyze` codebase enrichment receives `--unattended --report-dir <report-dir>/nested/analyze-<n>/` and the Wave 3 adversarial call receives `--unattended --output <report-dir>/nested/adversarial-<n>/` in place of `<output>/adversarial/`, with `adversarial_artifacts_dir` and the nested contracts listed in `artifacts`; `<n>` starts at 1 for each nested command, and the one retry of a nested call that the skill already makes (the adversarial `F1` retry) uses the next number, so a nested directory is never reused; the `tasklist` and `task` handoffs are skipped, recorded as `status: partial` with one line in `unresolved_conflicts` (their skills do not accept the flag at this phase); `design` and `none` handoffs are unchanged.

In `SKILL.md`: add the same behaviour where the protocol acts: in the Wave 2A enrichment matrix a sentence that under `--unattended` the research rows are skipped and the codebase row passes the flag and nested directory; in Wave 0 step 7 the skip and in step 8 the exact-directory rule; in Wave 3 step 1 an `--unattended` variant of the argument block, and the same variant in `refs/handoff-routing.md` (its argument block there passes `--output <output>/adversarial/` and forwards `--interactive`, neither of which is used under `--unattended`); in Wave 4 the skipped-handoff rule; in "Return Contract" the worker fields (`worker_contract_version`, `worker_status`, `command`, `report_path`, `artifacts`, `reason`) and the status mapping. The Wave 2A section must still contain none of the forbidden Tavily tokens of `tests/skills/test_brainstorm_protocol.py`. Add this task's entry to `UNATTENDED_EXPECT`: flags `--output`, `-o`, `--interactive` and `-i`; nested `analyze` and `adversarial`; phrases `research enrichment is off`, `exactly as passed`, `never reused`, `nested/analyze-`, `nested/adversarial-` and `dry-run`. Add a test to `tests/skills/test_brainstorm_protocol.py` that reads the skill and asserts the Wave 3 `--unattended` variant names `nested/adversarial-` the Wave 2A section names `nested/analyze-` and `skipped`, the skill's Wave 0 says `exactly as passed`, and `refs/handoff-routing.md` names `nested/adversarial-`.

Acceptance criteria:
- [T3.AC1] `grep -c '^## Unattended mode$' src/superclaude/commands/brainstorm.md` prints `1`, `grep -c 'research enrichment is off' src/superclaude/commands/brainstorm.md` prints `1`, and `grep -c 'exactly as passed' src/superclaude/commands/brainstorm.md` prints `1`.
- [T3.AC2] `uv run pytest tests/skills/test_worker_contract.py tests/skills/test_brainstorm_protocol.py tests/skills/test_codegraph_adoption.py tests/cli_portify/test_brainstorm_gaps.py tests/skills/test_primitive_dual_surface_lookup.py -q -p no:cacheprovider` passes, including the new entry and test.
- [T3.AC3] Check ADDITIVE prints nothing for `brainstorm.md`; Check SCAN prints nothing; the new text has no Check WRITEVERB phrase.
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
Start sha: d9e07ac03f797d7e8752e18927555da8b2083805
Diff against the start snapshot: diff --git a/src/superclaude/commands/brainstorm.md b/src/superclaude/commands/brainstorm.md
index 60b2f572..9315ef6e 100644
--- a/src/superclaude/commands/brainstorm.md
+++ b/src/superclaude/commands/brainstorm.md
@@ -38,6 +38,7 @@ A topic string (free-form text). File references via `@<path>` are supported.
   [--blind] [--convergence FLOAT] [--interactive] \
   [--handoff none|design|tasklist|task] [--output DIR] \
   [--dry-run] [--resume-from PATH] [--force-stale]
+/sc:brainstorm "<topic>" --unattended --report-dir DIR   # worker mode, see Unattended mode
 ```
 
 ## Options
@@ -62,6 +63,8 @@ A topic string (free-form text). File references via `@<path>` are supported.
 | `--dry-run` | | `false` | Execute Waves 0–2B, skip 3-4, print agent-spec preview |
 | `--resume-from` | | — | Resume from a saved seed-brief, skipping Socratic dialogue |
 | `--force-stale` | | `false` | Allow `--resume-from` even if domain re-classification differs |
+| `--unattended` | | `false` | Worker mode: no step waits for a person; see Unattended mode |
+| `--report-dir` | | — | With `--unattended`, the directory that holds the worker contract (instead of `--output`, never both) |
 
 **Flag interactions** (enforced in Wave 0):
 
@@ -142,6 +145,19 @@ Produces a versioned return contract with stable + telemetry blocks.
 
 Do NOT proceed with protocol execution using only this command file. The full behavioral specification is in the protocol skill at `~/.claude/skills/sc-brainstorm-protocol/SKILL.md`.
 
+## Unattended mode
+
+The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:brainstorm` resolves itself. `<report-dir>` below is the one report directory the caller passes.
+
+- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument (the topic is a quoted argument); otherwise nothing here applies and no worker contract is written.
+- **Report directory.** Exactly one of `--output <dir>` (short form `-o`) or `--report-dir <dir>`; both, or neither, is refused before any work. A directory the caller passes is used exactly as passed, never with the usual `-N` suffix. One that already holds a `return-contract.yaml`, or that cannot be created or written, is refused before any work as no usable report directory (printed in chat only), so no earlier contract is overwritten.
+- **Contract.** With `--output` the worker fields are added to the command's own `<output>/return-contract.yaml` beside every existing field, its own `status` included. With `--report-dir` the worker contract is a separate `<report-dir>/return-contract.yaml` that lists the own contract in `artifacts`. It is written on every other outcome, including each stop of Wave 0 of the skill (the stop text goes to `reason`). `report_path` is `merged-requirements.md` (null when the merge was not reached, and on `--dry-run`). The own status values success, partial, failed and dry-run map to succeeded, partial, failed and succeeded.
+- **Person-mode flags.** `--interactive` and its short form `-i` are refused before any work (contract `worker_status: failed`, the flag in `reason`). The Socratic dialogue proceeds on the best available context, and there is no other gate.
+- **Research.** Under `--unattended`, research enrichment is off: the automatic route and an explicit `--research light` or `--research deep` are skipped, each recorded in `enrichment_used` with `quality_tier: skipped`.
+- **Nested invocations.** The `/sc:analyze` codebase enrichment receives `--unattended --report-dir <report-dir>/nested/analyze-<n>/`, and the Wave 3 adversarial call receives `--unattended --output <report-dir>/nested/adversarial-<n>/` in place of `<output>/adversarial/`. `adversarial_artifacts_dir` and the nested contracts are listed in `artifacts`. `<n>` starts at 1 for each nested command, and the one retry of a nested call (the adversarial `F1` retry) uses the next number, so a nested directory is never reused.
+- **Handoffs.** The `tasklist` and `task` handoffs are skipped and recorded: `status: partial` with one line in `unresolved_conflicts` (their skills do not accept the flag at this phase), and the Wave 0 check that their skills are installed is skipped too. The `design` and `none` handoffs are unchanged.
+- **Outward actions.** It pushes, commits and stages nothing.
+
 ## Boundaries
 
 **Will:**

diff --git a/src/superclaude/skills/sc-brainstorm-protocol/SKILL.md b/src/superclaude/skills/sc-brainstorm-protocol/SKILL.md
index 2451583c..0d9f86bd 100644
--- a/src/superclaude/skills/sc-brainstorm-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-brainstorm-protocol/SKILL.md
@@ -90,6 +90,8 @@ Orchestrate parallel brainstorming via:
 
 **Purpose**: Validate inputs, environment, downstream skills.
 
+**Under `--unattended`** apply the `## Unattended mode` section of the `brainstorm` command file (installed copy `~/.claude/commands/sc/brainstorm.md`, or the project copy `.claude/commands/sc/brainstorm.md`) and `~/.claude/WORKER-CONTRACT.md`. Before step 1, resolve the one report directory (`--output` / `-o` or `--report-dir`) and refuse `--interactive` / `-i`. With no directory or both, or one that cannot be used, print the refusal in chat and stop without writing. Once a usable directory is known, every STOP of this wave also writes the worker contract with `worker_status: failed` and the STOP text in `reason`.
+
 **Behavioral Instructions**:
 
 1. Parse `$ARGUMENTS` into topic + flags. Reject empty topic. STOP if empty: `"Brainstorm requires a topic. Usage: /sc:brainstorm \"<topic>\""`
@@ -105,7 +107,9 @@ Orchestrate parallel brainstorming via:
 7. **Handoff prereq validation** (no silent downgrade):
    - If `--handoff task` AND `task-builder` skill missing → STOP: `"task-builder skill missing. Re-run with --handoff tasklist (if sc-tasklist-protocol installed) or --handoff design (text-only)."`
    - If `--handoff tasklist` AND `sc-tasklist-protocol` missing → STOP similarly
+   - Under `--unattended` this step is skipped: the `tasklist` and `task` handoffs are skipped in Wave 4, so their skills are not needed.
 8. Create output directory (default `.dev/brainstorms/<ts>-<slug>/`). If exists and non-empty, append `-N` suffix. Cap N at 99 (STOP on N=100); WARN at N≥10.
+   - Under `--unattended`, a directory the caller passes (`--output` or `--report-dir`) is used exactly as passed: no `-N` suffix, and one that already holds a `return-contract.yaml` was refused before step 1.
 9. Validate model aliases: read env vars `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL`. An unset variable is not an error: the alias resolves to Claude Code's built-in model for `opus`/`sonnet`/`haiku` (Coder workspaces no longer set these, Coder issue #270). If `--models` provided, validate each alias resolves to one of the known aliases.
 10. If `--strategy enterprise` and `--depth` not explicitly set → set `--depth deep` + INFO log.
 
@@ -188,6 +192,8 @@ Orchestrate parallel brainstorming via:
 
    Research depth/params are owned by `/sc:research` and `tech-research` — see RESEARCH_CONFIG.md; brainstorm selects the route only.
 
+   **Under `--unattended`**: the two research rows are skipped, also for an explicit `--research light` or `--research deep` (recorded in `enrichment_used` with `quality_tier: skipped`). The codebase row invokes `/sc:analyze` with `--unattended --report-dir <report-dir>/nested/analyze-<n>/` (`<n>` starts at 1); the `mcp__auggie__codebase-retrieval` alternative is unchanged and writes no nested contract. The nested contract is listed in `artifacts`.
+
 2. **Quality-tier tracking** (mandatory per enrichment source):
    - `primary` — first-choice source ran cleanly
    - `fallback_1` — primary failed, used codegraph and native Glob/Grep (codebase) or WebSearch (research)
@@ -277,6 +283,21 @@ Orchestrate parallel brainstorming via:
 
    (NOTE: `--generate spec` not `--generate requirements` per spec §10 decision; brainstorm reframes spec output as requirements.)
 
+   **Under `--unattended`** the argument block is instead (`--interactive` was refused in Wave 0, so it is never forwarded):
+
+   ```
+   --unattended
+   --source <output>/seed-brief.md
+   --generate spec
+   --agents <composed-spec-from-Wave-2B>
+   --depth <passthrough>
+   --convergence <passthrough, default 0.75>
+   --output <report-dir>/nested/adversarial-<n>/
+   [--blind if flagged]
+   ```
+
+   `<n>` starts at 1; the F1 retry in step 5 uses the next number, so a nested directory is never reused. The adversarial artifacts are under that nested directory, and `adversarial_artifacts_dir` points there.
+
 2. **Invoke**: `Skill sc-adversarial-protocol` with above arguments. Direct skill invocation, not command — per sc:roadmap pattern.
 
 3. **Consume return contract** (inline from Skill response):
@@ -328,6 +349,8 @@ Based on `--handoff` value:
   3. Invoke `Skill task-builder` with `--source <output>/merged-requirements.md --template <detected>`
   4. Capture task file path(s). Append to return contract.
 
+- **Under `--unattended`**: `tasklist` and `task` are skipped (their skills do not accept the flag at this phase). Invoke nothing, set `handoff_action: none` and `handoff_output_path: null`, set `status: partial`, and add one line to `unresolved_conflicts` naming the skipped handoff. `design` and `none` behave as above.
+
 **Exit Criteria**: Handoff complete (or skipped). Return contract finalized. Emit: `"Wave 4 complete: handoff=<value>. Output: <path>."`
 
 ## 4. Return Contract
@@ -353,6 +376,21 @@ handoff_output_path: <path> | null
 unresolved_conflicts: [<list of strings>]
 ```
 
+### Worker fields (only with `--unattended`)
+
+Added beside the fields above in `<output>/return-contract.yaml` (with `--report-dir`: written to `<report-dir>/return-contract.yaml`, which lists the own contract in `artifacts`), on every outcome:
+
+```yaml
+worker_contract_version: "1"
+worker_status: succeeded | partial | failed
+command: <the exact command line>
+report_path: <output>/merged-requirements.md | null   # null when the merge was not reached, and on dry-run
+artifacts: [<every other file written, adversarial_artifacts_dir, the nested contracts>]
+reason: <the STOP or refused flag>                     # only when failed
+```
+
+Status mapping: `success` → `succeeded`, `partial` → `partial`, `failed` → `failed`, `dry-run` → `succeeded`.
+
 ### Telemetry Block (non-stable)
 
 ```yaml

diff --git a/src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md b/src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md
index a04df563..da21ebbb 100644
--- a/src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md
+++ b/src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md
@@ -100,6 +100,8 @@ Optional pass-throughs:
 - `--blind` (if brainstorm `--blind` was set)
 - `--interactive` (if brainstorm `--interactive` was set)
 
+**Under `--unattended`** the argument string is the same except: `--unattended` is added; `--output` is `<report-dir>/nested/adversarial-<n>/` in place of `<output>/adversarial/` (`<n>` starts at 1, and the F1 retry uses the next number, so a nested directory is never reused); and `--interactive` is never forwarded, because brainstorm refuses it. The nested worker contract `<report-dir>/nested/adversarial-<n>/return-contract.yaml` and the returned `artifacts_dir` are listed in the `artifacts` of the brainstorm contract.
+
 ### Return contract consumption (inline from Skill response)
 
 Expected response fields (from sc-adversarial-protocol):

diff --git a/tests/skills/test_brainstorm_protocol.py b/tests/skills/test_brainstorm_protocol.py
index d27b6208..cb4a2ab2 100644
--- a/tests/skills/test_brainstorm_protocol.py
+++ b/tests/skills/test_brainstorm_protocol.py
@@ -29,6 +29,24 @@ def _wave2a_section() -> str:
     return re.split(r"\n###\s*Wave ", parts[1], maxsplit=1)[0]
 
 
+def _wave_section(n: str) -> str:
+    text = _BRAINSTORM.read_text(encoding="utf-8")
+    parts = re.split(rf"###\s*Wave {n}\b", text, maxsplit=1)
+    assert len(parts) == 2, f"brainstorm SKILL missing the 'Wave {n}' section"
+    return re.split(r"\n###\s*Wave ", parts[1], maxsplit=1)[0]
+
+
+def test_brainstorm_unattended_nested_directories_are_named():
+    """Under --unattended the nested calls get their own directories (P1 worker contract)."""
+    wave3 = _wave_section("3")
+    assert "--unattended" in wave3 and "nested/adversarial-" in wave3
+    wave2a = _wave2a_section()
+    assert "nested/analyze-" in wave2a and "skipped" in wave2a
+    assert "exactly as passed" in _wave_section("0")
+    refs = _BRAINSTORM.parent / "refs" / "handoff-routing.md"
+    assert "nested/adversarial-" in refs.read_text(encoding="utf-8")
+
+
 def test_brainstorm_no_tavily_param_duplication():
     """Wave-2A enrichment matrix routes only — no Tavily params / map/crawl tool names."""
     section = _wave2a_section()

diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index aedd13e3..4878a2e3 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -283,6 +283,18 @@ UNATTENDED_EXPECT: dict = {
         "phrases": ["<output>/adversarial/return-contract.yaml", "artifacts"],
         "nested": [],
     },
+    "brainstorm": {
+        "flags": ["--output", "-o", "--interactive", "-i"],
+        "phrases": [
+            "research enrichment is off",
+            "exactly as passed",
+            "never reused",
+            "nested/analyze-",
+            "nested/adversarial-",
+            "dry-run",
+        ],
+        "nested": ["analyze", "adversarial"],
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
