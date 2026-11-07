e88b2ff9c763bb8a8c57dcf6ff150161cc209c7e
Review one task for spec compliance.

Task brief: Repo root for every path in this task: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P2 (read files and run read-only git/grep commands from there).
Package folder (`./artifacts/...` paths in this task are relative to it): /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P2/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441

## Task 18: Change the `/sc:brainstorm` section: research-light runs `/sc:research` nested, research-deep skipped

Depends on: Task 4

Files: `src/superclaude/commands/brainstorm.md`, `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`, `tests/skills/test_brainstorm_protocol.py` and `tests/skills/test_worker_contract.py`; spec section 3.1 row brainstorm (P2 part), section 6 row P2, AC-2.1; D-P2-1.

In `brainstorm.md` replace exactly one line, the section's "Research" line that says research enrichment is off, with a line saying: under `--unattended`, the research-light route (automatic, or an explicit `--research light`) invokes `/sc:research` with `--unattended --strategy planning --depth quick --report-dir <report-dir>/nested/research-<n>/`, listed in `artifacts`, also when the call failed; the research-deep route (automatic, or an explicit `--research deep`) invokes `tech-research`, which has no Unattended mode, so research-deep is skipped and recorded in `enrichment_used` with `quality_tier: skipped` (D-P2-1). This is the one named exemption of Check ADDITIVE for this file. In `SKILL.md` replace the first sentence of the "Under `--unattended`" paragraph below the enrichment matrix (the sentence that skips both research rows) with the same rule; the rest of the paragraph (the codebase row and `nested/analyze-<n>/`) stays word for word. In `tests/skills/test_worker_contract.py`: in the brainstorm entry replace the phrase `research enrichment is off` with `nested/research-` and `research-deep is skipped`, add `research` to its `nested` list and to `EXPECTED_NESTING["brainstorm"]`; replace the AC-1.4 case `brainstorm-section` and `_check_brainstorm_research_off` with a P2 check that the section names `nested/research-` and `research-deep is skipped` and no longer contains `research enrichment is off` (each part must make the check fail when broken). In `tests/skills/test_brainstorm_protocol.py` add a test that the Wave 2A "Under `--unattended`" paragraph names `/sc:research`, `nested/research-` and `quality_tier: skipped`, and no longer says "the two research rows are skipped".

Acceptance criteria:
- `git diff --numstat "$(git merge-base master HEAD)" -- src/superclaude/commands/brainstorm.md` shows exactly one deleted line, and `grep -c 'research enrichment is off' src/superclaude/commands/brainstorm.md` prints `0`.
- `uv run pytest tests/skills/test_worker_contract.py tests/skills/test_brainstorm_protocol.py tests/skills/test_codegraph_adoption.py tests/cli_portify/test_brainstorm_gaps.py tests/skills/test_tier2_tavily_consistency.py -q -p no:cacheprovider` passes; the Wave 2A section still has none of the forbidden Tavily tokens.
- Check SCAN prints nothing.

Global constraints: ## Constraints

- Spec: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` is called "the spec" below, and "spec section N" means its section N. `./source.md` is the brief that started this plan. The spec is the authority; where a task cites a section it names the rows the task needs. Decisions: `.dev/orca-command-refactor/decisions/APPROVED.md`, plus the owner decisions that `./source.md` states in full because PR #417, which records them in that file, merged (576b6659) after this worktree's base: the P1 verdict is PASS (P2 may start), and F1 (an `artifacts` clause lists only files the run wrote, names the ignored files it leaves out and points at WC-4 for the reason with the words "left out (WC-4)", never restates the reason and never contains the literal write-verb text of Check WRITEVERB).
- Open owner question, listed and not decided here (P1-C5): eleven P1 workers carried out their command by reading its file in the top-level session with no `Skill` call, and spec section 7.2 step 5 condition 2 was recorded PASS for them. Whether that satisfies WC-7 decides how the P2 live plan judges condition 2. No task in this plan depends on the answer; Task 21 lists it in the static report.
- This is the static plan of Phase P2 (spec section 6, last paragraph). It covers AC-2.1 (spec section 7.3) and the common checks AC-C1 to AC-C6 (spec section 7.1). The live checks AC-2.2 to AC-2.9 and the P2 phase report belong to the P2 live plan, written after this plan's checks pass.
- No task in this plan commits, pushes, installs into `~/.claude`, starts an Orca worker, runs an Orca command or asks the owner a question. Nothing under the `.claude/` folder is staged, ever (repo `CLAUDE.md`, its absolute rule on `.claude/` contents); `make sync-dev` writes only gitignored `.claude/` copies. `.dev/tasks/` is always staged (`git add .dev/tasks`); staging is not committing.
- `src/superclaude/` is the source of truth. Installed primitives use installed paths only: a new section or sentence never contains `src/superclaude/` and never names an Orca command (spec SA-2; Check SCAN below). P2 touches no safety rule and adds no outward capability: where a command has an outward default (auggie-review posting, task's `commit` and `push` and its committed TFEP report) the change only turns it off under `--unattended` (spec section 6 row P2, WC-9). Without `--unattended` every prompt, gate, default and output path stays as it is today (spec SA-1, SA-3); every new sentence in a command or skill that changes behaviour starts with, or sits under, "Under `--unattended`".
- Mirrors. Only `help.md`, `recommend.md`, `workflow.md` and `implement.md` are copied byte-for-byte to `plugins/superclaude/commands/`, and only the `sc-recommend` and `sc-workflow-protocol` skill folders have pinned plugin copies (`tests/commands/test_routing_plugin_parity.py`, `tests/skills/test_task_workspace_smoke.py`, `tests/commands/test_workflow_command.py::test_plugin_mirror_matches_src`). So Task 6 mirrors recommend and Task 17 mirrors workflow; no other plugin copy is touched. Before this plan: the plugin copies of cleanup, research, spec-panel, reflect, troubleshoot and brainstorm already differ from their sources; improve and task are identical but not pinned; auggie-review, cli-eval, cli-portify, review-translation, release-split, tdd and tasklist have none; `src/superclaude/core/WORKER-CONTRACT.md` has no plugin copy.
- Section skeleton (the P1 rule, unchanged). Every `## Unattended mode` section is a level-2 heading written exactly like that, placed immediately before the file's first `## Boundaries` heading, and holds only the command's own resolutions. In this order: an opening sentence that names `~/.claude/WORKER-CONTRACT.md` as the home of the shared rules and tells the reader to read it first; the switch (applies only when `--unattended` is a standalone argument token outside any quoted argument, otherwise nothing in the section applies and no contract is written: spec SA-1, SA-3); the report directory (exactly one of `--report-dir <dir>` or the command's own directory flag, named per task; `--report-dir` follows the same path rules as the command's own directory flag where it has one; a report directory that fails them counts as no report directory known, so nothing is written and the refusal is printed in chat only); the contract (`<report-dir>/return-contract.yaml` written on every outcome with `worker_contract_version`, `worker_status`, `command`, `report_path`, `artifacts`, `blocked_question` when blocked and `reason` when failed, naming this command's deliverables; the `artifacts` clause follows F1); the person-mode refusals (every spelling the command accepts; refused before any work with `worker_status: failed` and the refused flag in `reason`); the gate resolutions, each naming its gate and how it resolves; the nested invocations (or "none"); the outward-action rule (the command pushes, commits and stages nothing under `--unattended`, WC-9). A `blocked` resolution writes `worker_status: blocked` with the exact question the command would have asked in `blocked_question` and stops. The section never repeats the shared rules' wording, the exact error text or the status mapping rules of WC-4; it states only this command's own status mapping where it has its own status values.
- Nested propagation (spec section 2.1). Under `--unattended`, a nested call to a command that accepts `--unattended` at P2 (the 16 P1 commands and the 15 of this plan) passes `--unattended` and a report directory `<report-dir>/nested/<command>-<n>/` through that command's own directory flag or `--report-dir`, `<n>` counting from 1 per nested command and never reused (a retry takes the next number), and the caller lists the nested contract in `artifacts`, also when the call failed. A nested directory exists only for a call that actually ran. A call to something that does not accept the flag (`tech-research`, `task-builder`, the MDTM `task` skill, an Agent-tool subagent) is either made gate-free as its task states or skipped and recorded in the caller's contract. A nested call's result is read from its worker contract by the rule Task 19 adds to `~/.claude/WORKER-CONTRACT.md` (D-P2-20): `blocked` stops the caller as `blocked` with the nested question; `failed` or a missing contract takes the caller's own documented failure path for that step. Every task that adds a nested call also checks the callee's skill for every other `Skill sc:`, `/sc:` or `Invoke` call site of the same command, so no nested call is left without the flag.
- Test data. `tests/skills/test_worker_contract.py` keeps `UNATTENDED_EXPECT` (command name to `flags`, `phrases`, `nested`) and its data-driven tests; each command task adds its own entry in the same task, so the suite is green after every task. Rules from P1 that every task follows: pin each rule with an exact phrase, never a single token that a clause can contain while saying the opposite; a check that replaces old wording also asserts the old wording is absent, on the line that carries the rule; text a test reads with `_artifacts_clause` sits after the first backticked `artifacts` on its line; every new check fails on the pre-change text (each task's acceptance criteria name the pre-change failure).
- Gate sentences. Each command's `## Unattended mode` section contains the sentences below word for word (flags in backticks, as written here), each command task adds them to that command's `UNATTENDED_EXPECT` `phrases`, and Task 20's `P2_GATES` table is built from this same list. The format is: command, the sentence, then its outcome words `=>` and the opposite words `!=` that the reverse-outcome negative test substitutes.
  - cleanup: "every item under "Approval Required" is listed as not applied" => `not applied` != `applied`.
  - improve: the cleanup sentence, and "`--force` is refused" => `refused` != `honoured`.
  - research: "an explicit `--strategy intent` or `--strategy unified` is refused" => `refused` != `honoured`.
  - spec-panel: "a TDD input without `--target-release` resolves as blocked" => `blocked` != `answered`.
  - recommend: "the one clarifying question resolves as blocked" => `blocked` != `asked`.
  - review-translation: "Phase 1 without `--context` resolves as blocked" => `blocked` != `confirmed`; "Phase 7 resolves to SKIP IMPLEMENTATION" => `SKIP IMPLEMENTATION` != `IMPLEMENT FIXES`.
  - release-split: "the tasklist-input warning resolves as blocked" and "`--r1-scope custom` resolves as blocked" => `blocked` != `prompted`.
  - cli-portify: "each of the three approval gates resolves as blocked" => `blocked` != `approved`.
  - auggie-review: "`--unattended` implies `--no-post-pr` and `--no-remediation-offer`" => `implies` != `allows`; "`--post-pr` and `--remediation-offer` are refused" => `refused` != `honoured`.
  - troubleshoot: "the short input STOP resolves as blocked" and "the `--fix` offer resolves as blocked" => `blocked` != `shown`.
  - task: "confidence below 0.70 resolves as blocked" and "every FULL STOP resolves as blocked" => `blocked` != `reported to the user`; "EXEMPT `commit` and `push` are refused" => `refused` != `allowed`.
  - cli-eval: "`run` without both `--suite` and `--output-dir` resolves as blocked" => `blocked` != `confirmed`; "an FR-G5 preflight failure resolves as blocked" => `blocked` != `worked around`.
  - tdd: "a bare topic resolves as blocked" and "a TDD that is already complete resolves as blocked" => `blocked` != `re-run`.
  - tasklist: "the unresolved High or Medium HALT resolves as blocked" and "the `needs_human_decision` HALT resolves as blocked" => `blocked` != `escalated`.
  - reflect: "`--remediate` is answered by the headless auto-accept rule" => `headless auto-accept rule` != `yes/no prompt`.
- F1 clause (source.md owner decision F1). In every P2 section, the contract bullet carries the `artifacts` clause so that the text after its first backticked `artifacts` contains `paths git ignores are left out (WC-4)` and contains neither `git add` nor `git refuses`; a report that names where those files went (cleanup and improve list every changed file; cli-eval names the run directory) says so in one short sentence in the same bullet. Task 20 pins this for all fifteen commands. Task 17's edit of the workflow contract line keeps the same tokens.
- A skip that makes no nested call (release-split Part 4, reflect Wave 1B, D-P2-24) adds no `nested/` entry, and its wording never contains the text `nested/`, because the P1 section check asserts that text is absent for a command whose nested list is empty.
- Check SCAN (spec AC-C1; run after every task that edits a command, skill, agent or core file). Pass: prints nothing.

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

- Check ADDITIVE (spec AC-C5 / SA-4). For every command file a task edits, `git diff --numstat "$(git merge-base master HEAD)" -- src/superclaude/commands/<name>.md | awk '$2 != 0'` prints nothing. The only two command files exempt are `workflow.md` and `brainstorm.md`: their P1 sections hold lines that P2 must replace (the spec's own P2 row changes them), so `workflow.md` may show exactly two deleted lines (its "Nested invocations" line and its "Contract" line, whose `.dev/reflect/` run-directory wording turns false under `--unattended`; D-P2-22) and `brainstorm.md` exactly one (its "Research" line); their tasks say which. Skill, ref and test files have no such rule, except `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md`, which must show zero deleted lines (AC-2.1, SA-6).
- Check WRITEVERB (spec AC-0.9). New text in any command or skill file must not contain the audit's write-verb phrases (`git add`, `git commit`, `git push`, `git merge`, `git stash`, `git update-ref`, `git worktree add` or `remove`, `gh pr`, `gh api`). `tests/skills/test_worker_contract.py::test_every_write_verb_hit_is_classified` and `::test_classification_table_has_no_stale_entries` must still pass, so no classified line is edited. The eleven `deferred:P2` entries keep their key and category; Tasks 10, 14 and 15 rewrite only their reason text to say the deferral is in force, as P1 did for its `deferred:P1` entry. Wherever a task says to add a sentence at a line that is a classified key (the auggie-review posting lines, the reflect snapshot lines, the task and task-builder staging lines), it adds a new line after that line; the classified line itself is never touched.
- Test commands. Every pytest run passes `-p no:cacheprovider`. Task 1 runs `uv sync --extra dev` once, so `make lint` and every ruff call use the project's pinned ruff; ruff is always called as `uv run --extra dev ruff`. After every test, lint or sync run, `git status --short` shows no tracked file changed by the run itself. The wider test run always passes `--ignore=tests/cli/eval/test_perf_home_setup.py`, because that test rewrites a tracked evidence file. UV for every Python command; no bare `python`, `python3` or `pip`.
- Pre-existing tests that read the files this plan edits, and must still pass: `tests/skills/test_worker_contract.py`, `tests/skills/test_brainstorm_protocol.py`, `tests/skills/test_codegraph_adoption.py`, `tests/skills/test_tier2_tavily_consistency.py`, `tests/skills/test_primitive_dual_surface_lookup.py`, `tests/skills/test_sc_recommend_routing_contract.py`, `tests/skills/test_review_severity_rule.py`, `tests/skills/test_task_workspace_smoke.py`, `tests/skills/test_task_builder_merge.py`, `tests/skills/test_reflect_input_snapshot.py`, `tests/skills/test_issue_protocol.py`, `tests/skills/test_model_alias_policy.py`, `tests/commands/test_workflow_command.py`, `tests/commands/test_routing_plugin_parity.py`, `tests/commands/test_research_command.py`, `tests/commands/test_impact_command.py`, `tests/commands/test_auggie_review_remediation_chain.py`, `tests/commands/test_auggie_review_revagent.py`, `tests/pr_submit/test_static_grep.py`, `tests/core/test_how_we_work_routing_table.py`, `tests/recommend/test_routing_refresh.py`, `tests/recommend/test_dispatch.py`, `tests/docs/test_onboarding_deck.py`, `tests/unit/test_cli_install.py`, `tests/unit/test_cli_doctor.py`, `tests/agents/test_tavily_tool_parity.py`, `tests/tasklist/test_tasklist_cli.py`, `tests/tasklist/test_bash_policy_contract.py`, `tests/cli/reflect/test_remediation_route_table.py`, `tests/cli/test_tdd_extract_prompt.py`, `tests/cli_portify/test_brainstorm_gaps.py`, `tests/cli/eval/test_workflow_vs_task_builder_companion.py` and the `tests/troubleshoot/` folder. Notable pins: `test_static_grep.py` requires every auggie-review flag the command uses to be a real Options-table row; `test_how_we_work_routing_table.py` requires `--no-post-pr` and `--no-remediation-offer` in the auggie-review command; `test_routing_refresh.py` requires `--preview` to stay out of the cleanup and improve `## Usage` sections; `test_research_command.py` pins the research `### Adaptive Depth` section; the workflow tests pin the `--output` retirement (a line that contains `--output` in the workflow command, skill or refs also says "retired" or "Never").
- Decisions this plan makes where the spec is silent or ambiguous, each recorded for owner approval in the static report (owner decisions of 2026-11-07: D-P2-1 to D-P2-21 are approved as written, with D-P2-18 and D-P2-19 taken as recommended and their alternatives rejected; D-P2-22 to D-P2-24 are new and wait for approval in the static report):
  - D-P2-1 (the open conflict of `./source.md`): brainstorm's research enrichment. The research-light row names `Skill sc-research-protocol`, which does not exist in this repo (only `src/superclaude/skills/tech-research/` exists), and offers `/sc:research` as the alternative. Under `--unattended` the research-light row invokes the `/sc:research` command with `--unattended --strategy planning --depth quick --report-dir <report-dir>/nested/research-<n>/`. The research-deep row invokes `tech-research`, which is not one of the spec's 39 commands and has no Unattended mode, so it is skipped and recorded in `enrichment_used` with `quality_tier: skipped` (spec section 2.1: a step whose callee does not accept the flag is skipped and recorded).
  - D-P2-2: `--isolate-reviewers` is a flag of the `superclaude reflect run` Python CLI only (`src/superclaude/cli/reflect/commands.py`, off by default), not of `/sc:reflect`. The skill's review-snapshot steps (`git worktree add` and `remove`, Step 0.5e) belong to that wrapper, so `/sc:reflect --unattended` creates no review snapshot and runs no git write; the reflect section says so and the three `deferred:P2` reflect entries keep their category with a reason that says this.
  - D-P2-3: `/sc:reflect --remediate` under `--unattended` follows the existing headless auto-accept rule whatever the terminal state (spec section 3.1 row reflect): AUTO-FIXABLE registers are authored without the yes/no prompt, HUMAN-REQUIRED registers author nothing auto-runnable, as today. The plan route invokes `sc:workflow` with `--unattended --report-dir <report-dir>/nested/workflow-<n>/ --handoff none`. The MDTM route (`--depth deep`) is skipped and recorded, because `task-builder` is not a command and its CLI-mode staging is refused by WC-9.
  - D-P2-4: commands that gain a report file get an optional file-valued `--output <file>` and a default `<report-dir>/<name>-report.md` (cleanup, improve, spec-panel); recommend writes its handoff envelope to `<report-dir>/recommendation.md`; review-translation writes its blocked context summary to `<report-dir>/context-summary.md`.
  - D-P2-5: review-translation gains `--context <file>`, a context summary the caller has already confirmed. Without it under `--unattended`, Phase 1 writes the summary and resolves as blocked; the re-run with `--context` is a fresh run (spec row: "add a resume input, or fresh run").
  - D-P2-6: cli-portify takes `--report-dir` only, because its `--output` names the generated Python package directory, where a contract would ship with the code. Outside an IronClaude checkout (its release-spec template is missing) the run is `failed` with that reason. Its new `--resume <contract>` reads `resume_phase` and `resume_substep` from a prior contract, and a resume past an approval gate counts as the caller's approval of that gate's artifact.
  - D-P2-7: recommend refuses `--eval` under `--unattended` (its with-resource runs are paid runs, WC-9) and skips its `.claude/cache/` lookup, plugin and telemetry writes (shared files, WC-11); reads are unchanged.
  - D-P2-8: cleanup and improve treat every "Safety Threshold" prompt as "Approval Required" (listed, not applied); improve refuses `--force` under `--unattended`, because it widens what is applied without confirmation.
  - D-P2-9: research refuses an explicit `--strategy intent` or `--strategy unified` under `--unattended`; with no `--strategy` the run uses `--strategy planning`.
  - D-P2-10: spec-panel gains `--target-release <release>` (usable in any run; when given, the TDD `target_release` question is not asked) and, under `--unattended` only, `--improve`: the Improve step runs only when `--improve` is passed and then writes `<report-dir>/improved-spec.md`; the input specification is never modified. `--mode socratic` is not refused (unlike business-panel in P1): it only writes its questions into the report and does not wait, which the section states.
  - D-P2-11: tdd passes `--unattended` after the task file path to its nested `/task` call; the `task` skill gains a paragraph that, when that token is present, turns its two ask-the-user points into a returned question (tdd then writes its blocked contract) and defers its `.dev/tasks` staging. `/task` writes no worker contract, so tdd lists no nested directory. tdd's other prompts resolve as: "TDD already complete, update or re-run" blocked; the build request's cleanup question defaults to keeping the sources; the archive confirmation defaults to not archiving.
  - D-P2-12: `/sc:task` under `--unattended` passes the nested flag to its `sc:impact-protocol` call (`nested/impact-<n>/`) and its TFEP `/sc:troubleshoot` call (`nested/troubleshoot-<n>/`); the TFEP report is written and listed in `artifacts`, never committed.
  - D-P2-13: tasklist Stage 10.5 under `--unattended` passes `--unattended --output <report-dir>/nested/reflect-<n>/` to each reflect (`<n>` in phase order) in place of `TASKLIST_ROOT/validation/reflect-pre/phase-<P>/`, and `validation/ValidationReport.md` cites those directories. Its two HALT points (unresolved High or Medium findings, a `needs_human_decision` item) resolve as blocked.
  - D-P2-14: release-split's own status maps `split-approved` and `no-split` to `succeeded`, `split-with-remediation` to `partial`, `failed` to `failed`; its nested `sc:brainstorm` and `sc:adversarial-protocol` calls get the nested flag and directories.
  - D-P2-15: cli-eval under `--unattended` replaces the W3 "confirm the exact invocation" step with the command line as given; `run` without `--suite` is blocked; the W0 confirmations, the missing-pipeline case and the "which pipeline" question are blocked; the create pipeline's `/sc:spec-panel`, `sc:adversarial-protocol` and `/sc:document` calls get the nested flag and directories.
  - D-P2-16: auggie-review refuses an explicit `--remediation-offer` under `--unattended`, as it refuses `--post-pr`; its diff- and PR-mode `sc:impact-protocol` call gets `nested/impact-<n>/`.
  - D-P2-17: troubleshoot's Tier 2 fix debate (`sc:adversarial-protocol --compare`) gets `--unattended --output <report-dir>/nested/adversarial-<n>/` in place of `<output-dir>/adversarial/`; the `--fix` offer resolves as blocked, so the remediation routes and their `sc:impact-protocol` call never run under `--unattended`.
  - D-P2-18 (closes reflect finding INV-001): the cli-eval skill names "the safety flags from the digest" (`--no-pty`, `--no-mcp`, `--json`, `--junit`, `--timeout-mult`, `--keep-home`, `--max-disk-mb`, `--output-dir`; `src/superclaude/skills/sc-cli-eval-protocol/SKILL.md:138`). Under `--unattended`, `run` is blocked unless the command line carries `--suite` and `--output-dir <dir>` (the run directory, so the coordinator knows where the run writes and two workers never share it, WC-11); every other safety flag takes the value on the command line, or the CLI's own default when absent, and that resolved set is the confirmed invocation. The FR-G5 empty-HOME workaround is never applied on the worker's own choice: when the doctor preflight would fail, `run` resolves as blocked with the workaround offer in `blocked_question`. Owner decision 2026-11-07: approved as written; the alternative (require every one of the eight safety flags explicitly) is rejected.
  - D-P2-19: troubleshoot's opt-in `--diagnosability-handoff` (packaging via `sc:workflow-protocol`, `sc-troubleshoot-protocol/refs/diagnosability-audit.md:245`) passes `--unattended --report-dir <report-dir>/nested/workflow-<n>/ --handoff none` under `--unattended`, and its step that reads `.dev/tasks/to-do/<id>/return-contract.yaml` reads the nested worker contract instead (its `report_path` is the plan path). Owner decision 2026-11-07: approved as written, so `--diagnosability-handoff` is allowed under `--unattended`; the alternative (refuse it) is rejected.
  - D-P2-20 (closes reflect finding INV-002): one shared rule, added to the nested propagation rule of `~/.claude/WORKER-CONTRACT.md` by Task 19: when a nested call's worker contract says `blocked`, the caller stops at that step and writes its own contract with `worker_status: blocked`, `blocked_question` set to the nested question prefixed with the nested command's name, and the nested contract in `artifacts`; when it says `failed` or no nested contract exists, the caller takes its own documented failure path for that step (fallback, skip and record, or stop), and if that ends the run it writes `worker_status: failed` with the nested command and its reason in `reason`; `succeeded` and `partial` count as the step completing.
  - D-P2-21: tasklist Stage 9 delegates patching to `sc:task` (`sc-tasklist-protocol/SKILL.md:1539-1542`, re-entered by the Stage 10 loop-back at :1557). Under `--unattended` every Stage 9 call, loop-backs included, passes `--compliance strict --unattended --report-dir <report-dir>/nested/task-<n>/`. The spec's tasklist row names only Stage 10.5; this applies spec section 2.1's nested rule to the second call site and is a spec observation for the coordinator.
  - D-P2-22 (closes reflect findings M-06 and M-17): `workflow.md` gets a two-line Check ADDITIVE exemption: its "Nested invocations" line (`workflow.md:75`) and its "Contract" line (`workflow.md:72`), whose `.dev/reflect/` run-directory wording would otherwise contradict the new nested folder. Alternative for the owner: keep one deleted line and add a new line beside the stale one (rejected here, because it leaves a false sentence in the section).
  - D-P2-23 (closes reflect findings M-11 and M-18): under `--unattended`, task-builder's CLI-mode reflect gate (`superclaude reflect run --depth deep --fix --promote`, `task-builder/SKILL.md:2237`) is skipped as a whole, not only its staging step, and `reflect gate skipped (unattended)` goes into the task log: its `--fix` loop auto-runs a corrective `/task` and its `--promote` moves folders, which the coordinator owns (WC-9). Alternative for the owner: run the gate with `--no-promote` and without `--fix`.
  - D-P2-24 (closes reflect findings M-07 and M-08): two nested-call sites that no spec row names are skipped, not nested: release-split Part 4 ("Skill `sc:analyze` or inline verification", `sc-release-split-protocol/SKILL.md:324`) uses inline verification, and reflect's Wave 1B optional `tech-research` call (`sc-reflect-protocol/SKILL.md:632`, `--depth deep` only) is skipped and recorded because `tech-research` has no Unattended mode (as D-P2-1 decides for brainstorm). Neither adds a nested directory or a nested-list entry.
- Owner decisions of 2026-11-07, recorded here before execution: (1) D-P2-18 and D-P2-19 are approved as written and their alternatives rejected; D-P2-1 to D-P2-17, D-P2-20 and D-P2-21 stand as written. (2) The remaining 13 medium and 13 low review findings are accepted as-is: they are not fixed and the plan is not re-reviewed. (3) P1-C5 (whether a worker that carries out a command by reading its file, with no `Skill` call, satisfies WC-7) is not decided; it stays an open owner question for the P2 live plan only and does not gate this work. (4) Constraints unchanged: no push, no PR, no `superclaude install`, no live Orca run, nothing under `.claude/` staged, and no commit; the run stops after Task 21 and reports the static results and the exact commit list for the owner's approval.
- Nothing in this plan edits `HOW-WE-WORK.md`, `KNOWN_CORE_FILES`, any agent file, any Python module under `src/superclaude/cli/`, or any command or skill not named in a task. The only core file edited is `WORKER-CONTRACT.md` (Task 19: its brief section, and one added line under the nested propagation rule for D-P2-20).

### Owner decision recorded after the plan was pinned (supersedes the plan's P1-C5 sentences)

Recorded here, not in the plan, because the plan is hash-pinned by the ledger after the first `T<id>: start` line (`E-PLAN-CHANGED`; `refs/managed-workspace.md` of the implement protocol). This file supersedes every plan sentence that calls P1-C5 open:

- Constraints, bullet "Open owner question, listed and not decided here (P1-C5)".
- Constraints, bullet "Owner decisions of 2026-11-07", item (3).
- Task 21, the report requirement "the open owner question P1-C5 (WC-7 and the Skill-call question), stated in full".

## The decision

A worker that carries a command out by reading its file, with no `Skill` call, does NOT satisfy WC-7. The command must be run for real: a `Skill` or slash-command call, at the top level. P1-C5 is therefore decided, not open, and no task in this plan changes.

## What follows

- The P2 live plan must make spec section 7.2 step 5 condition 2 require the `Skill` or slash-command call, and must fail a worker that made none.
- The static report (Task 21) states P1-C5 as decided and lists these follow-ups, none of which this task edits (the spec, `decisions/APPROVED.md` and the P1 reports stay untouched):
  - (a) the `APPROVED.md` row for P1-C5;
  - (b) the wording of spec section 7.2 step 5;
  - (c) owner accepted the 11 P1 rows (lc01, lc02, lc04, lc05, lc06, lc07, lc08, lc14, lc17, lc18, lc22) recorded PASS on condition 2, as they stand; P1 is not reopened and nothing is re-run; add this to the `APPROVED.md` row for P1-C5.

The ruling itself holds for P2 and later phases: the command must be run for real (a `Skill` or slash-command call).
Start sha: e88b2ff9c763bb8a8c57dcf6ff150161cc209c7e
Diff against the start snapshot: diff --git a/src/superclaude/commands/brainstorm.md b/src/superclaude/commands/brainstorm.md
index f42bcdb8..ab8db87d 100644
--- a/src/superclaude/commands/brainstorm.md
+++ b/src/superclaude/commands/brainstorm.md
@@ -153,7 +153,7 @@ The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This sect
 - **Report directory.** Exactly one of `--output <dir>` (short form `-o`) or `--report-dir <dir>`; both, or neither, is refused before any work. A directory the caller passes is used exactly as passed, never with the usual `-N` suffix. One that already holds a `return-contract.yaml`, one inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, is refused before any work as no usable report directory (printed in chat only), so no earlier contract is overwritten.
 - **Contract.** With `--output` the worker fields are added to the command's own `<output>/return-contract.yaml` beside every existing field, its own `status` included. With `--report-dir` the worker contract is a separate `<report-dir>/return-contract.yaml` that lists the own contract in `artifacts`. It is written on every other outcome, including each stop of Wave 0 of the skill (the stop text goes to `reason`). `report_path` is `merged-requirements.md` (null when the merge was not reached, and on `--dry-run`). The own status values success, partial, failed and dry-run map to succeeded, partial, failed and succeeded.
 - **Person-mode flags.** `--interactive` and its short form `-i` are refused before any work (contract `worker_status: failed`, the flag in `reason`). The Socratic dialogue proceeds on the best available context, and there is no other gate.
-- **Research.** Under `--unattended`, research enrichment is off: the automatic route and an explicit `--research light` or `--research deep` are skipped, each recorded in `enrichment_used` with `quality_tier: skipped`.
+- **Research.** Under `--unattended`, the research-light route (automatic, or an explicit `--research light`) invokes `/sc:research` with `--unattended --strategy planning --depth quick --report-dir <report-dir>/nested/research-<n>/`, and its contract is listed in `artifacts`, also when the call failed; the research-deep route (automatic, or an explicit `--research deep`) invokes `tech-research`, which has no Unattended mode, so research-deep is skipped and recorded in `enrichment_used` with `quality_tier: skipped`.
 - **Nested invocations.** The `/sc:analyze` codebase enrichment receives `--unattended --report-dir <report-dir>/nested/analyze-<n>/`, and the Wave 3 adversarial call receives `--unattended --output <report-dir>/nested/adversarial-<n>/` in place of `<output>/adversarial/`. `adversarial_artifacts_dir` and the nested contracts are listed in `artifacts`. `<n>` starts at 1 for each nested command, and the one retry of a nested call (the adversarial `F1` retry) uses the next number, so a nested directory is never reused. A codebase scan through `mcp__auggie__codebase-retrieval` or through the `fallback_1` tier (codegraph, then Glob and Grep) is not a nested command and writes no nested directory and no nested contract, so `nested/analyze-<n>/` is written only by a `/sc:analyze` call; `enrichment_used` records the scan's tier, which does not show whether that directory exists.
 - **Handoffs.** The `tasklist` and `task` handoffs are skipped and recorded: `status: partial` with one line in `unresolved_conflicts` (their skills do not accept the flag at this phase), and the Wave 0 check that their skills are installed is skipped too. The `design` and `none` handoffs are unchanged.
 - **Outward actions.** It pushes, commits and stages nothing.
diff --git a/src/superclaude/skills/sc-brainstorm-protocol/SKILL.md b/src/superclaude/skills/sc-brainstorm-protocol/SKILL.md
index ce27509a..469fbd29 100644
--- a/src/superclaude/skills/sc-brainstorm-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-brainstorm-protocol/SKILL.md
@@ -192,7 +192,7 @@ Orchestrate parallel brainstorming via:
 
    Research depth/params are owned by `/sc:research` and `tech-research` — see RESEARCH_CONFIG.md; brainstorm selects the route only.
 
-   **Under `--unattended`**: the two research rows are skipped, also for an explicit `--research light` or `--research deep` (recorded in `enrichment_used` with `quality_tier: skipped`). The codebase row invokes `/sc:analyze` with `--unattended --report-dir <report-dir>/nested/analyze-<n>/` (`<n>` starts at 1); the `mcp__auggie__codebase-retrieval` alternative and the `fallback_1` tier (codegraph, then native Glob and Grep, `refs/handoff-routing.md` Tier 2) are unchanged and write no nested directory and no nested contract, so `nested/analyze-<n>/` is written only by a `/sc:analyze` call, and `enrichment_used` does not show whether it exists. The nested contract is listed in `artifacts`, also when the call failed.
+   **Under `--unattended`**: the research-light row invokes `/sc:research` with `--unattended --strategy planning --depth quick --report-dir <report-dir>/nested/research-<n>/` (`<n>` starts at 1; also for an explicit `--research light`) and lists the nested contract in `artifacts`, also when the call failed; the research-deep row invokes `tech-research`, which has no Unattended mode, so research-deep is skipped, also for an explicit `--research deep`, and recorded in `enrichment_used` with `quality_tier: skipped`. The codebase row invokes `/sc:analyze` with `--unattended --report-dir <report-dir>/nested/analyze-<n>/` (`<n>` starts at 1); the `mcp__auggie__codebase-retrieval` alternative and the `fallback_1` tier (codegraph, then native Glob and Grep, `refs/handoff-routing.md` Tier 2) are unchanged and write no nested directory and no nested contract, so `nested/analyze-<n>/` is written only by a `/sc:analyze` call, and `enrichment_used` does not show whether it exists. The nested contract is listed in `artifacts`, also when the call failed.
 
 2. **Quality-tier tracking** (mandatory per enrichment source):
    - `primary` — first-choice source ran cleanly
diff --git a/tests/skills/test_brainstorm_protocol.py b/tests/skills/test_brainstorm_protocol.py
index 6d25de77..6277d949 100644
--- a/tests/skills/test_brainstorm_protocol.py
+++ b/tests/skills/test_brainstorm_protocol.py
@@ -84,6 +84,17 @@ def test_brainstorm_unattended_codebase_scan_writes_no_nested_directory():
             assert tier.count(phrase) == 1, f"{name}: {phrase}"
 
 
+def test_brainstorm_unattended_research_light_runs_nested_and_deep_is_skipped():
+    """Under --unattended research-light is a nested /sc:research call; research-deep is skipped (D-P2-1)."""
+    lead = "**Under `--unattended`**"
+    parts = _wave2a_section().split(lead, 1)
+    assert len(parts) == 2, "Wave 2A missing the Under --unattended paragraph"
+    paragraph = re.split(r"\n\s*\n", parts[1], maxsplit=1)[0]
+    for phrase in ("/sc:research", "nested/research-", "quality_tier: skipped"):
+        assert phrase in paragraph, phrase
+    assert "the two research rows are skipped" not in paragraph
+
+
 def test_brainstorm_no_tavily_param_duplication():
     """Wave-2A enrichment matrix routes only — no Tavily params / map/crawl tool names."""
     section = _wave2a_section()
diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index 298f2369..c4df4456 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -307,7 +307,8 @@ UNATTENDED_EXPECT: dict = {
     "brainstorm": {
         "flags": ["--output", "-o", "--interactive", "-i"],
         "phrases": [
-            "research enrichment is off",
+            "nested/research-",
+            "research-deep is skipped",
             "exactly as passed",
             "never reused",
             "nested/analyze-",
@@ -316,7 +317,7 @@ UNATTENDED_EXPECT: dict = {
             "writes no nested directory and no nested contract",
             "only by a `/sc:analyze` call",
         ],
-        "nested": ["analyze", "adversarial"],
+        "nested": ["analyze", "adversarial", "research"],
     },
     "graph": {
         "flags": ["--output-dir"],
@@ -1157,8 +1158,11 @@ def _check_workflow_ref(text: str) -> None:
     )
 
 
-def _check_brainstorm_research_off(section: str) -> None:
-    assert "research enrichment is off" in section, "section lacks the research line"
+def _check_brainstorm_research_nested(section: str) -> None:
+    # P2 (D-P2-1): research-light runs /sc:research nested, research-deep is skipped.
+    assert "nested/research-" in section, "section lacks the nested research directory"
+    assert "research-deep is skipped" in section, "section lacks the research-deep skip"
+    assert "research enrichment is off" not in section, "section keeps the P1 line"
 
 
 def _check_nested_text(section: str, expect: dict) -> None:
@@ -1201,8 +1205,8 @@ _AC14_CASES = (
     (
         "brainstorm-section",
         lambda: _unattended_section("brainstorm"),
-        _check_brainstorm_research_off,
-        ["research enrichment is off"],
+        _check_brainstorm_research_nested,
+        ["nested/research-", "research-deep is skipped"],
     ),
 )
 _AC14_REMOVALS = [
@@ -1277,6 +1281,12 @@ def test_ac_1_4_check_fails_when_phrase_removed(case, getter, check, phrase):
         check(text.replace(phrase, ""))
 
 
+def test_brainstorm_research_check_fails_on_the_p1_research_line():
+    section = _unattended_section("brainstorm")
+    with pytest.raises(AssertionError):
+        _check_brainstorm_research_nested(section + "\nresearch enrichment is off\n")
+
+
 @pytest.mark.parametrize("cmd", sorted(UNATTENDED_EXPECT))
 def test_nested_propagation_text_matches_the_nested_list(cmd):
     _check_nested_text(_unattended_section(cmd), UNATTENDED_EXPECT[cmd])
@@ -1285,7 +1295,7 @@ def test_nested_propagation_text_matches_the_nested_list(cmd):
 # command -> nested commands that receive --unattended; each P2 task adds or extends
 # its own key in the task that gives the command a nested call.
 EXPECTED_NESTING = {
-    "brainstorm": ["analyze", "adversarial"],
+    "brainstorm": ["analyze", "adversarial", "research"],
     "workflow": ["reflect"],
     "release-split": ["brainstorm", "adversarial"],
     "auggie-review": ["impact"],
Delta diff from the previous reviewed tree (empty on the first review): (none)
Earlier blocking findings of this start (empty on the first review): (none)
Saved-probe re-check hit locations (may be empty): (none)

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
