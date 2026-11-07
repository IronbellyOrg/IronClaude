7306d32925ff5ddca4cd302599c58c401d13ca04
Review one task for spec compliance.

Task brief: Repo root for every path in this task: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P2 (read files and run read-only git/grep commands from there).
Package folder (`./artifacts/...` paths in this task are relative to it): /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P2/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441

## Task 13: Convert `/sc:cli-eval`: run needs `--suite`, confirmations blocked, eval waits of at most 240 s

Depends on: Task 5

Files: `src/superclaude/commands/cli-eval.md`, `src/superclaude/skills/sc-cli-eval-protocol/SKILL.md`, `src/superclaude/skills/sc-cli-eval-protocol/refs/run-pipeline.md` and `src/superclaude/skills/sc-cli-eval-protocol/refs/integration-map.md`; spec section 3.2 row cli-eval, WC-10 and AC-2.1; D-P2-15, D-P2-18.

In the command: add rows for `--unattended` and `--report-dir` to the Options table and the `## Unattended mode` section before `## Boundaries`. The section states: report directory is `--report-dir <dir>` only; a missing pipeline (`create` or `run`) resolves as blocked; `run` without both `--suite` and `--output-dir <dir>` resolves as blocked, with the missing flag named in `blocked_question` (D-P2-18); the suite menu and the W3 "confirm the exact invocation" step are replaced by the command line as given: each other safety flag of W3 takes its command-line value or the CLI default, and the resolved set is the confirmed invocation; when the FR-G5 doctor preflight would fail, `run` resolves as blocked with the empty-HOME workaround offer in `blocked_question` and the workaround is not applied; the W0 "confirm with the user" cases resolve as blocked; the eval job is waited on in waits of at most 240 s each (WC-10), so the session can send a heartbeat between them; `report_path` is the run's `summary.md` (run) or the design spec (create), and `artifacts` lists `summary.json` and the files the run wrote, and paths git ignores are left out (WC-4); own `status` `success`, `partial`, `failed` map to the same worker values; nested invocations of the create pipeline: `/sc:spec-panel` receives `--unattended --report-dir <report-dir>/nested/spec-panel-<n>/`, `sc:adversarial-protocol` receives `--unattended --output <report-dir>/nested/adversarial-<n>/`, and `/sc:document` receives `--unattended --report-dir <report-dir>/nested/document-<n>/` with an explicit `--output`; `/sc:spec-panel` and `/sc:document` are command-only (no backing skill), so the create pipeline runs them as commands and never through the `Skill` tool, and the `technical-writer` agent alternative that `SKILL.md:109` offers for the documentation step is skipped under `--unattended` and recorded, because an agent run yields no nested directory; it pushes, commits and stages nothing. In `SKILL.md` add one added sentence at each gate line (missing `$1`, W0 confirmation, the W2 menu, the W3 confirmation, the "which pipeline" question) and at the eval wait (the existing "per-eval timeouts can reach 3600s" text stays); in `refs/run-pipeline.md` add an added sentence at the background wait: under `--unattended` each wait on the job is at most 240 s and is repeated until the job ends; in `refs/integration-map.md` add the `--unattended` arguments for the three nested calls. In `SKILL.md` the added line at the W3 confirmation states the D-P2-18 rule (the two required flags, the defaults for the rest, the blocked FR-G5 case). Add the entry: flags `--suite` and `--output-dir`; phrases `240 s`, `blocked_question`, `summary.json`, `the resolved set is the confirmed invocation`, `empty-HOME workaround`, `command-only` and `technical-writer`; nested `spec-panel`, `adversarial` and `document`; add `"cli-eval": ["spec-panel", "adversarial", "document"]` to `EXPECTED_NESTING`. Add a test that `refs/run-pipeline.md` names `240 s` on a line that also names `--unattended` (spec AC-2.1: "the eval wait step names a single-wait limit of at most 240 s"), and that it fails on the pre-change file.

Acceptance criteria:
- `grep -c '^## Unattended mode$' src/superclaude/commands/cli-eval.md` prints `1`, and `grep -n '240 s' src/superclaude/skills/sc-cli-eval-protocol/refs/run-pipeline.md` shows the new wait line.
- `uv run pytest tests/skills/test_worker_contract.py tests/skills/test_review_severity_rule.py tests/core/test_how_we_work_routing_table.py tests/unit/test_cli_install.py -q -p no:cacheprovider` passes.
- Check ADDITIVE prints nothing for `cli-eval.md`; Check SCAN prints nothing.

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
Start sha: 7306d32925ff5ddca4cd302599c58c401d13ca04
Diff against the start snapshot: diff --git a/src/superclaude/commands/cli-eval.md b/src/superclaude/commands/cli-eval.md
index 10d806ab..2698b108 100644
--- a/src/superclaude/commands/cli-eval.md
+++ b/src/superclaude/commands/cli-eval.md
@@ -37,6 +37,8 @@ underlying `superclaude eval` CLI — selection and monitoring are orchestration
 | `--agents` | create | `opus,sonnet,haiku` | Advocate specs for adversarial variant generation |
 | `--suite` | run | (menu) | Pre-select a suite by name; otherwise an interactive menu is shown |
 | `--eval` | run | (all) | Pre-select a single eval id to drill into / filter |
+| `--unattended` | both | off | Worker mode for a coordinator; applies only as a standalone argument token. Behaviour is in `## Unattended mode`; without it nothing changes |
+| `--report-dir` | both | — | With `--unattended`: the directory that holds the worker contract and the report |
 
 ## Behavioral Summary
 
@@ -72,6 +74,18 @@ hardcoded flag list or schema field.
 Do NOT proceed with protocol execution using only this command file.
 The full behavioral specification is in the protocol skill.
 
+## Unattended mode
+
+The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:cli-eval` resolves itself.
+
+- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument; otherwise nothing here applies and no worker contract is written.
+- **Report directory.** `--report-dir <dir>` only (the `run` pipeline's `--output-dir` names the eval run directory, not the report directory). Without it the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
+- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome, for both pipelines. `report_path` is the run's `summary.md` (run) or the design spec (create). `artifacts` lists `summary.json` and the other files the run wrote; paths git ignores are left out (WC-4), and the report names the run directory. The skill's own `status` values `success`, `partial` and `failed` map to `succeeded`, `partial` and `failed`.
+- **Person-mode flags.** None is refused.
+- **Gates.** Under `--unattended` a missing pipeline (`create` or `run`) resolves as blocked, and so does every W0 "confirm with the user" case. `run` without both `--suite` and `--output-dir` resolves as blocked, with the missing flag named in `blocked_question`, so no suite menu is shown and two workers never share a run directory. The W3 "confirm the exact invocation" step is replaced by the command line as given: each other safety flag takes its command-line value or the CLI default, and the resolved set is the confirmed invocation. The doctor preflight still runs, and an FR-G5 preflight failure resolves as blocked, with the empty-HOME workaround offer in `blocked_question`; the empty-HOME workaround is not applied on the worker's own choice. The eval job is waited on in waits of at most 240 s each (WC-10), so the session can send a heartbeat between them, and the waits repeat until the job ends.
+- **Nested invocations.** In the create pipeline `/sc:spec-panel` receives `--unattended --report-dir <report-dir>/nested/spec-panel-<n>/`, `sc:adversarial-protocol` receives `--unattended --output <report-dir>/nested/adversarial-<n>/`, and `/sc:document` receives `--unattended --report-dir <report-dir>/nested/document-<n>/` with an explicit `--output`, each `<n>` counting from 1 per nested command and never reused (a retry takes the next number); each contract is listed in `artifacts`, also when the call failed. `/sc:spec-panel` and `/sc:document` are command-only (no backing skill), so the create pipeline runs them as commands and never through the `Skill` tool; the `technical-writer` agent alternative for the documentation step is skipped under `--unattended` and recorded, because an agent run yields no nested directory. A nested contract is read by the nested-result rule of `~/.claude/WORKER-CONTRACT.md`.
+- **Outward actions.** It pushes, commits and stages nothing.
+
 ## Boundaries
 
 **Will:**
diff --git a/src/superclaude/skills/sc-cli-eval-protocol/SKILL.md b/src/superclaude/skills/sc-cli-eval-protocol/SKILL.md
index 933d21f2..9f815bc8 100644
--- a/src/superclaude/skills/sc-cli-eval-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-cli-eval-protocol/SKILL.md
@@ -37,6 +37,7 @@ adds NO flags to the `superclaude eval` CLI.
 ### Required (STOP if missing)
 
 - `$1` ∈ {`create`, `run`} — the pipeline selector. STOP and ask if neither is present.
+  Under `--unattended` (shared rules: `~/.claude/WORKER-CONTRACT.md`) this question is not asked: a missing `$1` resolves as blocked, with the which-pipeline question in `blocked_question`.
 
 ### Optional
 
@@ -56,6 +57,7 @@ adds NO flags to the `superclaude eval` CLI.
    user before proceeding — do NOT substitute a remembered value. The digest is the ONLY authority
    for flags/fields the rest of this protocol uses. If you ever need a flag/field not in the digest,
    re-invoke the loader; never hardcode.
+   Under `--unattended` this confirmation is not asked: the missing or moved source resolves as blocked, with that source in `blocked_question`.
 
 **Refs Loaded**: none yet. (The digest the loader returns supersedes any remembered contract.)
 
@@ -81,6 +83,7 @@ claim (flags, schema fields) in the Wave-0 digest.
 Invoke the `/sc:spec-panel` command: `@<stem>-spec.md --mode critique --focus requirements,architecture`
 (spec-panel is command-only — its protocol is inline in the command, there is no `sc:spec-panel` skill).
 Fold the panel's findings back into the spec. Do not reimplement a review panel.
+Under `--unattended` (shared rules: `~/.claude/WORKER-CONTRACT.md`) add `--unattended --report-dir <report-dir>/nested/spec-panel-<n>/` (`<n>` counts from 1 per nested command and is never reused) and list the nested contract in `artifacts`, also when the call failed; run it as a command, never through the `Skill` tool.
 
 ### W3 — Produce 2-3 competing designs + debate/merge (REUSE)
 
@@ -90,6 +93,7 @@ isolation). Then merge them with `Skill sc:adversarial-protocol`:
 - Mode-B (generate then merge): `--source <stem>-spec.md --generate eval-suite --agents <agents>`.
 - Mode-A (you already wrote the variants): `--compare designA.md,designB.md,designC.md`.
 Capture the merged design + transcript under `.dev/eval-workspaces/cli-eval/design/`.
+Under `--unattended` (shared rules: `~/.claude/WORKER-CONTRACT.md`) add `--unattended --output <report-dir>/nested/adversarial-<n>/` to either mode (a retry takes the next `<n>`) and list the nested contract in `artifacts`, also when the call failed.
 
 ### W4 — Author the manifest schema-first (DELEGATE)
 
@@ -109,6 +113,7 @@ Update the inventory in `docs/guides/suites-guide.md` and the "what lives in thi
 `src/superclaude/cli/eval/suites/README.md` via the `/sc:document` command (or the `technical-writer`
 agent — `document` is command-only, so use the command, not a `Skill` call).
 Optionally run `evidence-validator` over the doc edits to confirm every cite resolves.
+Under `--unattended` (shared rules: `~/.claude/WORKER-CONTRACT.md`) run `/sc:document` as a command with `--unattended --report-dir <report-dir>/nested/document-<n>/` and an explicit `--output`, and list the nested contract in `artifacts`, also when the call failed; the `technical-writer` agent alternative above is skipped and recorded, because an agent run yields no nested directory.
 
 **Create return contract**: see the Return Contract section.
 
@@ -131,6 +136,7 @@ Present the suites as an `AskUserQuestion` menu (name — version — eval_count
 drill in with `uv run superclaude eval describe --suite <name>` and show its evals, isolation
 strategy, timeouts, and any `no_pty: skip` markers. Honor `--suite`/`--eval` pre-selections by
 pre-filling the menu.
+Under `--unattended` (shared rules: `~/.claude/WORKER-CONTRACT.md`) no menu is shown: the suite is the `--suite` value, and `run` without `--suite` resolves as blocked, with the missing flag named in `blocked_question`.
 
 ### W3 — Confirm the invocation + flags (AskUserQuestion)
 
@@ -145,12 +151,15 @@ Before launching, confirm the EXACT invocation with the user: the suite (+ optio
   `skip_reason="--no-pty"`. Make clear whether the user wants a real run (omit `--no-pty`) or the
   CI-canary skip path.
 
+Under `--unattended` (shared rules: `~/.claude/WORKER-CONTRACT.md`) this confirmation is not asked: `run` needs both `--suite` and `--output-dir <dir>` (else it resolves as blocked, the missing flag named in `blocked_question`), each other safety flag takes its command-line value or the CLI's own default, and the resolved set is the confirmed invocation. If the FR-G5 doctor preflight would fail, `run` resolves as blocked with the empty-HOME workaround offer in `blocked_question`, and the workaround is not applied.
+
 ### W4 — Monitor a live run (background Bash + Monitor)
 
 Launch `uv run superclaude eval run --suite <name> [confirmed flags]` as a **background** Bash job and
 attach a **Monitor** that emits per-eval PASS/SKIP/FAIL/ERROR signals and the terminal exit (per-eval
 timeouts can reach 3600s, so do not block). Capture the run output path. Prefer `--verbose` (not only
 `--json`) so a non-production-executor warning is not suppressed (see W5 authoritativeness).
+Under `--unattended` (shared rules: `~/.claude/WORKER-CONTRACT.md`) wait on the job in waits of at most 240 s each (WC-10), repeated until the job ends; the 3600s above is the per-eval timeout, not a single wait.
 
 ### W5 — Parse + report (DELEGATE)
 
@@ -207,6 +216,8 @@ stubbed PASS is never reported as a real eval pass.
 | All evals SKIPPED (e.g. `--no-pty`) | Report as skipped, NOT pass; state why | Offer the real-run (no `--no-pty`) invocation |
 | Non-production/stubbed executor (canned PASS) | Label run NON-AUTHORITATIVE; state what unblocks a real run | Re-run `--verbose` to surface the warning `--json` suppressed |
 
+Under `--unattended` (shared rules: `~/.claude/WORKER-CONTRACT.md`) the `$1` not create/run row, the fresh-context row and the FR-G5 row are not asked or worked around: each resolves as blocked, with its question in `blocked_question` (for FR-G5, the empty-HOME workaround offer).
+
 ## Will Do
 
 - Re-read + cite the live eval contract surface before every create/run action.
diff --git a/src/superclaude/skills/sc-cli-eval-protocol/refs/run-pipeline.md b/src/superclaude/skills/sc-cli-eval-protocol/refs/run-pipeline.md
index 8db2bdb7..ef35f29c 100644
--- a/src/superclaude/skills/sc-cli-eval-protocol/refs/run-pipeline.md
+++ b/src/superclaude/skills/sc-cli-eval-protocol/refs/run-pipeline.md
@@ -56,6 +56,8 @@ grep -E --line-buffered "PASS|FAIL|SKIP|ERROR|TIMEOUT|INTERRUPT|summary.json|Tra
 Report per-eval signals as they stream and the terminal exit code. Silence is not success — if the
 job crashes, the filter must still emit something.
 
+Under `--unattended` each wait on the job is at most 240 s and is repeated until the job ends, so the session can send a heartbeat between waits (the per-eval timeout above is not a single wait).
+
 **Authoritativeness probe**: prefer `--verbose` over (or in addition to) `--json` for the run, because
 `--json` suppresses the executor warning line. The harness may run a non-production executor (e.g. a
 milestone-gated `_NullLifecycleExecutor` that emits canned PASS before the real PTY executor lands);
diff --git a/src/superclaude/skills/sc-cli-eval-protocol/refs/integration-map.md b/src/superclaude/skills/sc-cli-eval-protocol/refs/integration-map.md
index b948ff6d..8e6597fe 100644
--- a/src/superclaude/skills/sc-cli-eval-protocol/refs/integration-map.md
+++ b/src/superclaude/skills/sc-cli-eval-protocol/refs/integration-map.md
@@ -59,6 +59,14 @@ Or delegate to the `technical-writer` agent for the inventory-table edits. Targe
 Task the `evidence-validator` agent over the doc edits to confirm every `file:line` cite resolves and
 no unfounded claim slipped in. Read-only; drops/【flags unfounded items.
 
+## Arguments under `--unattended`
+
+Under `--unattended` (shared rules: `~/.claude/WORKER-CONTRACT.md`) the three calls above gain these arguments. `<n>` counts from 1 per nested command and is never reused (a retry takes the next number), and each nested contract is listed in `artifacts`, also when the call failed:
+
+- `/sc:spec-panel`: `--unattended --report-dir <report-dir>/nested/spec-panel-<n>/`, run as a command.
+- `Skill sc:adversarial-protocol`: `--unattended --output <report-dir>/nested/adversarial-<n>/`.
+- `/sc:document`: `--unattended --report-dir <report-dir>/nested/document-<n>/` and an explicit `--output`, run as a command; the `technical-writer` agent alternative is skipped and recorded.
+
 ## Notes on nesting (important when testing in a subagent)
 
 `/sc:spec-panel` and `/sc:adversarial` themselves fan out to sub-agents. An Agent-tool subagent
diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index 186f1818..eb87608c 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -532,6 +532,21 @@ UNATTENDED_EXPECT: dict = {
         ],
         "nested": ["impact", "troubleshoot"],
     },
+    "cli-eval": {
+        "flags": ["--suite", "--output-dir"],
+        "phrases": [
+            "240 s",
+            "blocked_question",
+            "summary.json",
+            "the resolved set is the confirmed invocation",
+            "empty-HOME workaround",
+            "command-only",
+            "technical-writer",
+            "`run` without both `--suite` and `--output-dir` resolves as blocked",
+            "an FR-G5 preflight failure resolves as blocked",
+        ],
+        "nested": ["spec-panel", "adversarial", "document"],
+    },
 }
 
 # Commands with an `## Unattended mode` section after P2 (./source.md section 6
@@ -1232,6 +1247,7 @@ EXPECTED_NESTING = {
     "auggie-review": ["impact"],
     "troubleshoot": ["adversarial", "workflow"],
     "task": ["impact", "troubleshoot"],
+    "cli-eval": ["spec-panel", "adversarial", "document"],
 }
 
 
@@ -1240,6 +1256,27 @@ def test_nested_lists_match_the_p2_nesting():
     assert listed == EXPECTED_NESTING
 
 
+_CLI_EVAL_RUN_REF = (
+    _REPO / "src/superclaude/skills/sc-cli-eval-protocol/refs/run-pipeline.md"
+)
+
+
+def _check_eval_wait_limit(text: str) -> None:
+    assert any("--unattended" in ln and "240 s" in ln for ln in text.splitlines()), (
+        "no line names --unattended and a 240 s single-wait limit"
+    )
+
+
+def test_cli_eval_eval_wait_names_a_single_wait_limit_of_240_s():
+    # spec AC-2.1: the eval wait step names a single-wait limit of at most 240 s.
+    text = _read(_CLI_EVAL_RUN_REF)
+    _check_eval_wait_limit(text)
+    with pytest.raises(AssertionError):
+        _check_eval_wait_limit(text.replace("240 s", ""))
+    with pytest.raises(AssertionError):
+        _check_eval_wait_limit(text.replace("--unattended", ""))
+
+
 def test_nested_check_fails_on_nested_text_without_a_nested_list():
     # graph has an empty nested list, so any nested/ text in its section must fail.
     section = _unattended_section("graph")
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
