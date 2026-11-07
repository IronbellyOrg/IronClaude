f328099e253f3285c5dbd993bf892467c0520883
Review one task for spec compliance.

Task brief: Repo root for every path in this task: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P2 (read files and run read-only git/grep commands from there).
Package folder (`./artifacts/...` paths in this task are relative to it): /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P2/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441

## Task 21: Run the P2 static checks and write the static report with the commit list for the owner's approval

Depends on: Task 20

Run these checks at the end of the static plan and save each output under `./artifacts/`:
- `make sync-dev` and then `make verify-sync` (AC-C2, exit 0) to `./artifacts/ac-c2.txt`;
- Check SCAN (AC-C1, prints nothing) to `./artifacts/ac-c1.txt`;
- `uv run pytest tests/skills/ -q -rf -p no:cacheprovider` compared with `./artifacts/ac-c3-baseline.txt` (AC-C3) to `./artifacts/ac-c3-compare.md`, which lists every baseline-passing test that now fails (must be none) and every new test;
- the wider run of Task 1 compared with `./artifacts/t1-baseline-wider.txt` to `./artifacts/wider-compare.md`, which, together with the AC-C3 comparison, lists every pre-existing test file named in the Constraints and shows each passing;
- `git diff --cached --name-only | grep '^\.claude/' | grep -v '^\.claude/settings\.json$'` (AC-C4) to `./artifacts/ac-c4-index.txt`, which must be empty;
- Check ADDITIVE (AC-C5) for each of the fifteen converted command files and for `workflow.md` and `brainstorm.md`, one line per file to `./artifacts/ac-c5.txt`, with `workflow.md` (exactly two deleted lines) and `brainstorm.md` (exactly one) shown as the two named exemptions;
- the AC-C6 command of spec section 7.1 to `./artifacts/ac-c6-depth-setting.txt`; every printed line must be `"nestedWorkerMaxDepth":1`, and a profile that prints nothing is recorded as using Orca's presumed default of 1;
- AC-2.1: `uv run pytest tests/skills/test_worker_contract.py -q -p no:cacheprovider` to `./artifacts/ac-2.1-tests.txt`, and the deletions check on `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md` (spec section 7.3 code block) to `./artifacts/ac-2.1-deletions.txt`, which must be empty;
- `make lint` compared with `./artifacts/lint-baseline.txt`, and `uv run --extra dev ruff format --check` on the test files this plan edited compared with `./artifacts/format-baseline.txt`, to `./artifacts/lint-format-compare.md`: a pass is `make lint` exit 0 with no new `ERROR` line and no new ruff finding; each new `WARN` line is recorded and does not fail; no new unformatted file;
- `cmp` of the recommend pairs (Task 6) and the workflow pairs (Task 17) to `./artifacts/mirror-check.txt`, empty.

Write `./artifacts/p2-static-report.md` from the P1 static report's structure (`.dev/tasks/done/TASK-WF-writeTheP1Static-20261105-033458/artifacts/p1-static-report.md`). It has one PASS or FAIL line, with its evidence file, for AC-2.1 (tests), AC-2.1 (deletions), AC-C1, AC-C2, AC-C3, AC-C4, AC-C5, AC-C6, lint, format and the mirror check, and it lists: the decisions D-P2-1 to D-P2-24 of the Constraints (D-P2-1 to D-P2-21 approved by the owner on 2026-11-07, D-P2-18 and D-P2-19 as written with their alternatives rejected; D-P2-22 to D-P2-24 for owner approval); the open owner question P1-C5 (WC-7 and the Skill-call question), stated in full and marked as an open question for the P2 live plan only that does not gate this work; the items marked UNVERIFIED in this plan (cli-portify's undefined `{work_dir}`; research's default `--strategy` and `--depth` when the flags are omitted; the directory the TFEP report goes to; whether the reflect and troubleshoot plugin copies differ beyond their first hunk); the exact list of repo paths this plan created or changed, in these groups: command files, skill and ref files, core file, plugin mirrors, test files; the plugin command copies left unmirrored (each marked identical to or already different from its source before this plan); the list of the fifteen P2 commands with their report-directory flag and their required brief flags, as the input to the P2 live plan; and the spec observations for the coordinator (brainstorm's research-light row names a skill that does not exist; `--isolate-reviewers` is a CLI flag, not a `/sc:reflect` flag; `/sc:task` never reaches the `task` or `task-builder` skills, so their `deferred:P2` entries are reached only through tdd, reflect and troubleshoot; the spec's tasklist row names only Stage 10.5, while Stage 9 also calls `sc:task` (D-P2-21); the spec does not say how a nested `blocked` result reaches the caller, which D-P2-20 settles). Finish the task with `git add .dev/tasks` so the report and every artifact are staged, and stage no `.claude/` path.

Acceptance criteria:
- `./artifacts/p2-static-report.md` has a PASS or FAIL line for each of the eleven checks listed above, each naming an evidence file that exists under `./artifacts/`, and every line reads PASS.
- `./artifacts/ac-c4-index.txt` and `./artifacts/ac-2.1-deletions.txt` are empty, and `git diff --cached --name-only -- .dev/tasks` lists this package's files.
- The repo-path list in the report equals the set of paths printed by `git status --short --untracked-files=all -- src tests plugins` minus the paths already in `./artifacts/status-baseline.txt` (paths only, status letters dropped), and the report lists this package's files under `.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/` in a separate group.

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
Start sha: f328099e253f3285c5dbd993bf892467c0520883
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/p2-static-report.md b/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/p2-static-report.md
new file mode 100644
index 00000000..7b157614
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/p2-static-report.md
@@ -0,0 +1,212 @@
+# P2 static report
+
+Plan: `TASK-WF-writeTheP2Static-20261107-011441`. Scope: AC-2.1 (the static part) and AC-C1 to AC-C6 (spec sections 7.1 and 7.3), for the 15 commands converted in P2. The live checks (AC-2.2 to AC-2.9) and the P2 phase report belong to the P2 live plan. Nothing is committed, pushed or installed, no live Orca run was made, and nothing under `.claude/` is staged.
+
+## Check results
+
+- PASS AC-2.1 (tests): `tests/skills/test_worker_contract.py` passes (681 tests, rc=0). It pins the 31-command set, the nested propagation of nine commands, 25 gate sentences with reversed-outcome negatives, and the artifacts clause of all 15 commands. Evidence: `./artifacts/ac-2.1-tests.txt`.
+- PASS AC-2.1 (deletions): `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md` shows 3 added lines and 0 deleted lines. Evidence: `./artifacts/ac-2.1-deletions.txt` (empty).
+- PASS AC-C1: Check SCAN prints nothing. Evidence: `./artifacts/ac-c1.txt` (empty).
+- PASS AC-C2: `make sync-dev` and `make verify-sync` both exit 0. Evidence: `./artifacts/ac-c2.txt`.
+- PASS AC-C3: No baseline-passing test fails (tests/skills 1318 -> 1601 passed; wider run 9164 -> 9165 passed); the 32 named test files and the `tests/troubleshoot/` folder (75 test files in all) each pass. Three baseline test ids are no longer collected because a task of this plan replaced them on purpose (listed in the comparison file). Evidence: `./artifacts/ac-c3-compare.md`, `./artifacts/wider-compare.md`.
+- PASS AC-C4: No `.claude/` path is staged. Evidence: `./artifacts/ac-c4-index.txt` (empty).
+- PASS AC-C5: The 15 converted command files show 0 deleted lines; `workflow.md` shows exactly 2 and `brainstorm.md` exactly 1, the two named exemptions. Evidence: `./artifacts/ac-c5.txt`.
+- PASS AC-C6: 1 Orca profile line (`local-default`), `"nestedWorkerMaxDepth":1`. Evidence: `./artifacts/ac-c6-depth-setting.txt`.
+- PASS lint: `make lint` exit 0, no new ERROR, ruff finding or WARN file; three existing size WARN lines grew and are recorded in the comparison file. Evidence: `./artifacts/lint-format-compare.md`.
+- PASS format: the four edited test files are formatted. Evidence: `./artifacts/lint-format-compare.md`.
+- PASS mirror check: the recommend pairs (2) and the workflow pairs (3) are byte-identical. Evidence: `./artifacts/mirror-check.txt` (empty).
+
+Overall: PASS (11 of 11). The commands, exit codes and counts behind each line are in `./artifacts/static-checks-log.txt`.
+
+Recorded WARN (does not fail): `make lint` already warned about five command files in the baseline (Check 3, more than 200 lines). The same five warn now. Three grew because of their new `## Unattended mode` section: `reflect.md` 305 -> 319, `spec-panel.md` 462 -> 476, `troubleshoot.md` 215 -> 229. There are 0 new WARN files.
+
+Not run: the FINAL whole-package review and the archive step of `/sc:implement`. You asked to stop after Task 21. Archiving moves this package folder from `to-do/` to `done/`, so it changes the paths in the commit list below; run it after you approve the list.
+
+## Decisions made where the spec was silent or ambiguous (D-P2-1 to D-P2-25)
+
+Owner decisions of 2026-11-07: D-P2-1 to D-P2-21 are approved as written. D-P2-18 and D-P2-19 are approved as recommended and their alternatives are rejected. D-P2-22 to D-P2-25 wait for your approval.
+
+- D-P2-1 (approved): brainstorm's research-light row runs the `/sc:research` command nested (`--unattended --strategy planning --depth quick --report-dir <report-dir>/nested/research-<n>/`); research-deep (`tech-research`, no Unattended mode) is skipped and recorded in `enrichment_used` with `quality_tier: skipped`.
+- D-P2-2 (approved): `--isolate-reviewers` is a flag of the `superclaude reflect run` wrapper, not of `/sc:reflect`; `/sc:reflect --unattended` creates no review snapshot and runs no git write.
+- D-P2-3 (approved): `/sc:reflect --remediate` under `--unattended` follows the existing headless auto-accept rule; the plan route runs `sc:workflow` nested with `--handoff none`; the MDTM route (`--depth deep`) is skipped and recorded.
+- D-P2-4 (approved): cleanup, improve and spec-panel get an optional file-valued `--output <file>` and default to `<report-dir>/<name>-report.md`; recommend writes `<report-dir>/recommendation.md`; review-translation writes `<report-dir>/context-summary.md` when blocked.
+- D-P2-5 (approved): review-translation gains `--context <file>`; without it Phase 1 writes the summary and resolves as blocked, and the re-run with `--context` is a fresh run.
+- D-P2-6 (approved): cli-portify takes `--report-dir` only; outside an IronClaude checkout it is `failed`; its new `--resume <contract>` reads `resume_phase` and `resume_substep`, and resuming past a gate counts as approval of that gate's artifact.
+- D-P2-7 (approved): recommend refuses `--eval` under `--unattended` and skips its cache, plugin and telemetry writes.
+- D-P2-8 (approved): cleanup and improve treat every "Safety Threshold" prompt as "Approval Required" (listed, not applied); improve refuses `--force`.
+- D-P2-9 (approved): research refuses an explicit `--strategy intent` or `--strategy unified`; with no `--strategy` it uses `planning`.
+- D-P2-10 (approved): spec-panel gains `--target-release <release>` and, under `--unattended` only, `--improve` (writes `<report-dir>/improved-spec.md`); `--mode socratic` is not refused.
+- D-P2-11 (approved): tdd passes `--unattended` to its nested `/task` call; the `task` skill turns its two ask-the-user points into a returned question; tdd's other prompts take safe defaults.
+- D-P2-12 (approved): `/sc:task` passes the nested flag to `sc:impact-protocol` and to its TFEP `/sc:troubleshoot` call; the TFEP report is written and listed, never committed.
+- D-P2-13 (approved): tasklist Stage 10.5 passes `--unattended --output <report-dir>/nested/reflect-<n>/` to each reflect; its two HALT points resolve as blocked.
+- D-P2-14 (approved): release-split maps `split-approved` and `no-split` to `succeeded`, `split-with-remediation` to `partial`, `failed` to `failed`; its nested brainstorm and adversarial calls get the flag.
+- D-P2-15 (approved): cli-eval replaces the W3 "confirm the exact invocation" step with the command line as given, and blocks on `run` without `--suite`, on the W0 confirmations and on the missing-pipeline case; the create pipeline's three nested calls get the flag.
+- D-P2-16 (approved): auggie-review refuses an explicit `--remediation-offer` under `--unattended`, as it refuses `--post-pr`; its `sc:impact-protocol` call is nested.
+- D-P2-17 (approved): troubleshoot's Tier 2 fix debate (`sc:adversarial-protocol --compare`) is nested; the `--fix` offer resolves as blocked, so no remediation route runs.
+- D-P2-18 (approved as written, alternative rejected): under `--unattended`, cli-eval `run` is blocked unless the command line carries `--suite` and `--output-dir`; every other safety flag takes the command-line value or the CLI default; an empty-HOME workaround is never applied on the worker's own choice.
+- D-P2-19 (approved as written, alternative rejected): troubleshoot's `--diagnosability-handoff` is allowed under `--unattended`, packaged through a nested `sc:workflow-protocol`; the step that read the plan path from `.dev/tasks/to-do/<id>/return-contract.yaml` reads the nested worker contract instead.
+- D-P2-20 (approved): the shared nested-result rule is added to `WORKER-CONTRACT.md` (Task 19): a nested `blocked` stops the caller as `blocked` with the nested question prefixed by the nested command's name; `failed` or a missing contract takes the caller's own failure path for that step; `succeeded` and `partial` count as the step completing.
+- D-P2-21 (approved): tasklist Stage 9 (and the Stage 10 loop-back) passes `--compliance strict --unattended --report-dir <report-dir>/nested/task-<n>/` to every `sc:task` call.
+- D-P2-22 (awaiting approval): `workflow.md` has a two-line Check ADDITIVE exemption (its "Nested invocations" and "Contract" lines, whose `.dev/reflect/` wording would be false under `--unattended`). Alternative: keep one deleted line and add a new line beside the stale one.
+- D-P2-23 (awaiting approval): under `--unattended`, task-builder's CLI-mode reflect gate (`superclaude reflect run --depth deep --fix --promote`) is skipped as a whole and `reflect gate skipped (unattended)` goes into the task log. Alternative: run the gate with `--no-promote` and without `--fix`.
+- D-P2-24 (awaiting approval): release-split Part 4 uses inline verification instead of a nested `sc:analyze`, and reflect's Wave 1B optional `tech-research` call is skipped and recorded; neither adds a nested directory.
+- D-P2-25 (new, awaiting approval): release-split Part 3 can call `/sc:design`, `/sc:workflow` or `/sc:tasklist`, a call site no plan decision or spec row names. Under `--unattended` the section and skill make Part 3 write the specs inline (the skill's own Error Handling fallback), so release-split's nested list stays brainstorm and adversarial.
+
+Review findings accepted as they stand (owner, 2026-11-07): the remaining 13 medium and 13 low findings of the plan review were not fixed and the plan was not re-reviewed.
+
+## P1-C5: decided NO
+
+Question: does a worker that carries a command out by reading its file, with no `Skill` call, satisfy WC-7? Owner answer, 2026-11-07: NO. The command must be run for real, with a `Skill` or slash-command call at the top level. The plan's sentences that call P1-C5 open are superseded by `./artifacts/owner-decision-p1-c5.md`, which every reviewer received with the constraints. No task in this plan changed.
+
+- The P2 live plan must make spec section 7.2 step 5 condition 2 require the `Skill` or slash-command call, and must fail a worker that made none.
+- Follow-ups for you (this plan edits none of these files):
+  - (a) the `APPROVED.md` row for P1-C5;
+  - (b) the wording of spec section 7.2 step 5;
+  - (c) owner accepted the 11 P1 rows (lc01, lc02, lc04, lc05, lc06, lc07, lc08, lc14, lc17, lc18, lc22) recorded PASS on condition 2, as they stand; P1 is not reopened and nothing is re-run; add this to the `APPROVED.md` row for P1-C5.
+
+## UNVERIFIED items
+
+- cli-portify's `{work_dir}` stays undefined in the skill (as the plan says). The new delivery-gate resume point (`resume_phase: 4`, `resume_substep: "delivery"`) was added to the skill's "Resume under `--unattended`" paragraph (`src/superclaude/skills/sc-cli-portify-protocol/SKILL.md:576`); the skill's existing resume sections 3c and 4a do not carry it, and no run was made.
+- research's default `--strategy` and `--depth` when the flags are omitted were not run.
+- The directory the TFEP report goes to was not run.
+- Whether the reflect and troubleshoot plugin copies differ from their sources beyond the first hunk was not examined (they already differed before this plan).
+- Whether the running Orca app re-reads the depth setting file (AC-C6, spec text) was not run.
+- No live run was made for any of the 15 commands: every `--unattended` behavior above is pinned by text and tests only.
+
+## Repo paths created or changed under `src`, `tests` and `plugins`
+
+The list equals the paths printed by `git status --short --untracked-files=all -- src tests plugins` (52 paths).
+
+### Command files (17)
+
+- `src/superclaude/commands/auggie-review.md`
+- `src/superclaude/commands/brainstorm.md`
+- `src/superclaude/commands/cleanup.md`
+- `src/superclaude/commands/cli-eval.md`
+- `src/superclaude/commands/cli-portify.md`
+- `src/superclaude/commands/improve.md`
+- `src/superclaude/commands/recommend.md`
+- `src/superclaude/commands/reflect.md`
+- `src/superclaude/commands/release-split.md`
+- `src/superclaude/commands/research.md`
+- `src/superclaude/commands/review-translation.md`
+- `src/superclaude/commands/spec-panel.md`
+- `src/superclaude/commands/task.md`
+- `src/superclaude/commands/tasklist.md`
+- `src/superclaude/commands/tdd.md`
+- `src/superclaude/commands/troubleshoot.md`
+- `src/superclaude/commands/workflow.md`
+
+### Skill and ref files (25)
+
+- `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md`
+- `src/superclaude/skills/sc-auggie-review-protocol/refs/remediation-handoff.md`
+- `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`
+- `src/superclaude/skills/sc-cli-eval-protocol/SKILL.md`
+- `src/superclaude/skills/sc-cli-eval-protocol/refs/integration-map.md`
+- `src/superclaude/skills/sc-cli-eval-protocol/refs/run-pipeline.md`
+- `src/superclaude/skills/sc-cli-portify-protocol/SKILL.md`
+- `src/superclaude/skills/sc-recommend/SKILL.md`
+- `src/superclaude/skills/sc-reflect-protocol/SKILL.md`
+- `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md`
+- `src/superclaude/skills/sc-release-split-protocol/SKILL.md`
+- `src/superclaude/skills/sc-release-split-protocol/refs/adversarial-integration.md`
+- `src/superclaude/skills/sc-review-translation-protocol/SKILL.md`
+- `src/superclaude/skills/sc-task-protocol/SKILL.md`
+- `src/superclaude/skills/sc-tasklist-protocol/SKILL.md`
+- `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
+- `src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md`
+- `src/superclaude/skills/sc-troubleshoot-protocol/refs/remediation-handoff.md`
+- `src/superclaude/skills/sc-workflow-protocol/SKILL.md`
+- `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md`
+- `src/superclaude/skills/task-builder/SKILL.md`
+- `src/superclaude/skills/task/SKILL.md`
+- `src/superclaude/skills/tdd/SKILL.md`
+- `src/superclaude/skills/tdd/refs/build-request-template.md`
+- `src/superclaude/skills/tdd/refs/validation-checklists.md`
+
+### Core file (1)
+
+- `src/superclaude/core/WORKER-CONTRACT.md`
+
+### Plugin mirrors (5)
+
+- `plugins/superclaude/commands/recommend.md`
+- `plugins/superclaude/commands/workflow.md`
+- `plugins/superclaude/skills/sc-recommend/SKILL.md`
+- `plugins/superclaude/skills/sc-workflow-protocol/SKILL.md`
+- `plugins/superclaude/skills/sc-workflow-protocol/refs/return-contract.md`
+
+### Test files (4)
+
+- `tests/commands/test_workflow_command.py`
+- `tests/skills/test_brainstorm_protocol.py`
+- `tests/skills/test_sc_recommend_routing_contract.py`
+- `tests/skills/test_worker_contract.py`
+
+## Plugin command copies left unmirrored
+
+Only `recommend.md` and `workflow.md` (and the `sc-recommend` and `sc-workflow-protocol` skill files) are mirrored, because tests pin them. For the other converted commands (`./artifacts/unmirrored-plugin-copies.txt`):
+
+- Identical to the source before this plan, now behind it: improve, task.
+- Already different from the source before this plan: cleanup, research, spec-panel, reflect, troubleshoot, brainstorm.
+- No plugin copy exists: auggie-review, cli-eval, cli-portify, review-translation, release-split, tdd, tasklist.
+- `src/superclaude/core/WORKER-CONTRACT.md` has no plugin copy.
+
+## The fifteen commands, their report-directory flag and required brief flags (input to the P2 live plan)
+
+Under `--unattended` the brief passes exactly one report directory. The brief flags below are the ones the `WORKER-CONTRACT.md` table now requires.
+
+- auggie-review: `--output-dir <dir>` or `--report-dir <dir>`. Brief: `--output-dir <dir>`; never `--post-pr` (or `--remediation-offer`).
+- cleanup: `--report-dir <dir>` only. No further brief flag.
+- improve: `--report-dir <dir>` only. No further brief flag (`--force` is refused).
+- cli-eval: `--report-dir <dir>` only. Brief: `run` with `--suite <name>` and `--output-dir <dir>` (the eval run directory) plus `--report-dir <dir>`; other safety flags as wanted, else the CLI defaults.
+- cli-portify: `--report-dir <dir>` only. Brief: `--report-dir <dir>`; `--resume <contract>` to continue past an approval gate.
+- recommend: `--report-dir <dir>` only. No further brief flag (`--eval` is refused).
+- research: `--report-dir <dir>` only. No further brief flag (an explicit `--strategy intent` or `unified` is refused).
+- review-translation: `--report-dir <dir>` only. Brief: `--report-dir <dir>`; `--context <file>` once the context is confirmed.
+- spec-panel: `--report-dir <dir>` only (`--output` is file-valued). Brief: `--report-dir <dir>`; `--target-release <release>` for TDD inputs.
+- task: `--report-dir <dir>` only. No further brief flag.
+- tasklist: `--output <output-dir>` or `--report-dir <dir>`. No further brief flag.
+- reflect: `--output <dir>` or `--report-dir <dir>`. Brief: `--remediate` is allowed under `--unattended` (the headless rule answers it); `--no-promote` when the coordinator owns folder moves.
+- release-split: `--output <dir>` (`-o`) or `--report-dir <dir>`. Brief: spec-shaped input; default `--r1-scope`; never `--interactive`; its gates resolve as blocked.
+- tdd: `--report-dir <dir>` only (`--output` names the TDD file). Brief: a precise component prompt, not a bare topic; `--output <file>`; its gates resolve as blocked.
+- troubleshoot: `--output-dir <dir>` or `--report-dir <dir>`. Brief: no `--fix` under `--unattended` (the offer resolves as blocked); a short `--depth deep` input resolves as blocked.
+
+## Spec observations for the coordinator
+
+- Brainstorm's research-light row names `Skill sc-research-protocol`, which does not exist in this repo (D-P2-1).
+- `--isolate-reviewers` is a flag of the `superclaude reflect run` Python CLI, not of `/sc:reflect` (D-P2-2).
+- `/sc:task` never reaches the `task` or `task-builder` skills, so their `deferred:P2` entries are reached only through tdd, reflect and troubleshoot.
+- The spec's tasklist row names only Stage 10.5, while Stage 9 also calls `sc:task` (D-P2-21).
+- The spec does not say how a nested `blocked` result reaches the caller, which D-P2-20 settles.
+- Release-split Part 3 can call `/sc:design`, `/sc:workflow` or `/sc:tasklist`, which no spec row names (D-P2-25).
+- Reflect's UC-2 Step 1B.3 calls `sc:impact-protocol` (a command that accepts `--unattended`). No plan decision or spec row names that call, and reflect's nested list is pinned to adversarial and workflow, so the call was left unchanged. It needs your decision, like D-P2-25.
+- cli-eval's `refs/create-pipeline.md` repeats the three create-pipeline call sites without the `--unattended` arguments. The plan's file list leaves it out; `SKILL.md` and `refs/integration-map.md` carry the arguments. No edit was made.
+
+## Plan gaps and process notes
+
+- The plan was edited once before the run, to record your owner decisions; its hash is pinned in the ledger and it was not edited again. Your P1-C5 answer and the acceptance of the 11 P1 rows arrived after that, so they are in `./artifacts/owner-decision-p1-c5.md`, which was added to the constraints slot of every later reviewer prompt. A first ledger and retries folder made before the plan edit are kept in `./artifacts/superseded-ledger/`.
+- Reviewer prompts: each saved prompt is in `./artifacts/retries/T<n>/`; because reviewers must not read the retries folder, a byte-identical copy was placed in `/tmp/impl2/prompts/` (outside the repo) and each reviewer was told to read that copy. The helper scripts that built the prompts and the evidence logs are in `/tmp/impl2/` and are not part of the repo.
+- Task 11: a first saved prompt was built, then removed and rebuilt before any reviewer read it, because the pre-review test run failed on a capitalised gate sentence (fixed in the command).
+- Blocking findings from reviewers, each fixed and re-reviewed by a fresh reviewer: Task 3 (gate sentences missing from the checked phrases), Task 6 (skill paragraph covered 2 of 5 clarification sites), Task 8 (both `--output` and `--report-dir` allowed), Task 12 (Contract bullet lacked "written on every outcome"), Task 14 (tdd skill never told the builder the caller is unattended), Task 15 (reflect skill Phase A lacked the unattended workflow arguments).
+- cleanup's gate sentence was missing from its test entry after Task 2 (found in Task 3's review); it was added in Task 20, test file only.
+- Check ADDITIVE: local `master` is behind `HEAD`, so the plan's literal command (against the merge base with `master`) cannot see edits to lines that P1 added. `ac-c5.txt` shows both columns: against the merge base and against `HEAD` (the P2 start).
+- Minor reviewer notes (not blocking) are in `./artifacts/retries/T<n>/notes.md` and cited in the ledger with `notes@` tokens.
+
+## Commit list for your approval (nothing is committed)
+
+Group 1, product changes (52 paths, the list above): 17 command files, 25 skill and ref files, 1 core file, 5 plugin mirrors, 4 test files.
+
+Group 2, the plan package (already staged or staged by this task): everything under `.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/` (the plan, `source.md`, `return-contract.yaml`, `progress.md`, and `artifacts/`).
+
+Group 3, plan-review evidence the package cites, currently untracked (recommended: include, as the P1 closeout commit did):
+
+- `.dev/reflect/pre-TASK-WF-writeTheP2Static-20261107-011441-20261107013500/` (the plan review folder, named in the package's `return-contract.yaml`)
+- `docs/memory/reflect/deviation-patterns-OrcaCLICommandRefactor-P2.md`
+
+Never staged: anything under `.claude/` (the `make sync-dev` copies there are gitignored).
+
+## Staging
+
+`git add .dev/tasks` stages this report and every artifact of this package. Nothing under `.claude/` is staged. Nothing is committed or pushed by this plan.
diff --git a/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/lint-format-compare.md b/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/lint-format-compare.md
new file mode 100644
index 00000000..ced6968e
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/lint-format-compare.md
@@ -0,0 +1,23 @@
+# Lint and format comparison
+
+Baseline files: `lint-baseline.txt`, `format-baseline.txt` (HEAD 576b6659, before this plan). After files: `lint-after.txt`, `format-after.txt` (after Task 20).
+
+| Check | Baseline | After | Result |
+|---|---|---|---|
+| `make lint` exit code | 0 | 0 | PASS |
+| Policy checker `Errors:` | 0 | 0 | PASS (no new ERROR line) |
+| Policy checker `Warnings:` | 5 | 5 | PASS (no new file warns) |
+| `uv run ruff check .` | All checks passed | All checks passed | PASS (no new ruff finding) |
+| `uv run --extra dev ruff format --check` on the four test files this plan edited (`tests/skills/test_worker_contract.py`, `tests/skills/test_brainstorm_protocol.py`, `tests/commands/test_workflow_command.py`, `tests/skills/test_sc_recommend_routing_contract.py`) | 4 files already formatted, rc=0 | 4 files already formatted, rc=0 | PASS (no new unformatted file) |
+
+## Warning lines
+
+The same five files warn before and after: `brainstorm.md`, `reflect.md`, `spawn.md`, `spec-panel.md`, `troubleshoot.md` (Check 3, line count above the warn threshold of 200). Three of the five grew because this plan added their `## Unattended mode` section; none is a new warning:
+
+| File | Lines before | Lines after |
+|---|---|---|
+| `reflect.md` | 305 | 319 |
+| `spec-panel.md` | 462 | 476 |
+| `troubleshoot.md` | 215 | 229 |
+
+`brainstorm.md` (217) and `spawn.md` (210) are unchanged. No other command file crossed the threshold.
diff --git a/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/wider-compare.md b/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/wider-compare.md
new file mode 100644
index 00000000..0f0f4c90
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/wider-compare.md
@@ -0,0 +1,92 @@
+# Wider run comparison
+
+| Run | File | Result |
+|---|---|---|
+| Baseline (HEAD 576b6659, before this plan) | `t1-baseline-wider.txt` | 9164 passed, 30 skipped, 1 xpassed, 5 warnings in 434.43s (0:07:14), rc=0 |
+| After Task 20 | `wider-run.txt` | 9165 passed, 30 skipped, 1 xpassed, 5 warnings in 427.24s (0:07:07), rc=0 |
+
+Command (both runs): `uv run pytest tests/core tests/commands tests/recommend tests/cli tests/cli_portify tests/unit tests/roadmap tests/tasklist tests/troubleshoot tests/pr_submit tests/docs tests/agents -q -rf -p no:cacheprovider --ignore=tests/cli/eval/test_perf_home_setup.py` (the ignored test rewrites a tracked evidence file).
+
+Failures after the plan: 0. Baseline-passing tests that now fail: none. Passed count rose by 1 (9164 to 9165): the one test this plan added outside tests/skills is in `tests/commands/test_workflow_command.py` (Task 17); the other new tests are in `tests/skills/` (see `ac-c3-compare.md`). The skipped, xpassed and warning counts are unchanged.
+
+## Pre-existing test files named in the plan Constraints
+
+The plan names 33 entries (32 files and the `tests/troubleshoot/` folder). They were run together after Task 20 (`uv run pytest <files> -q -p no:cacheprovider`: 75 test files, all passing, 2329 tests). Per-file results are in `named-files-results.txt`.
+
+```text
+PASS tests/agents/test_tavily_tool_parity.py: 4 tests, 0 failed, 0 skipped
+PASS tests/cli/eval/test_workflow_vs_task_builder_companion.py: 125 tests, 0 failed, 0 skipped
+PASS tests/cli/reflect/test_remediation_route_table.py: 4 tests, 0 failed, 0 skipped
+PASS tests/cli/test_tdd_extract_prompt.py: 68 tests, 0 failed, 0 skipped
+PASS tests/cli_portify/test_brainstorm_gaps.py: 16 tests, 0 failed, 0 skipped
+PASS tests/commands/test_auggie_review_remediation_chain.py: 12 tests, 0 failed, 0 skipped
+PASS tests/commands/test_auggie_review_revagent.py: 12 tests, 0 failed, 0 skipped
+PASS tests/commands/test_impact_command.py: 81 tests, 0 failed, 0 skipped
+PASS tests/commands/test_research_command.py: 2 tests, 0 failed, 0 skipped
+PASS tests/commands/test_routing_plugin_parity.py: 5 tests, 0 failed, 0 skipped
+PASS tests/commands/test_workflow_command.py: 19 tests, 0 failed, 0 skipped
+PASS tests/core/test_how_we_work_routing_table.py: 79 tests, 0 failed, 0 skipped
+PASS tests/docs/test_onboarding_deck.py: 3 tests, 0 failed, 0 skipped
+PASS tests/pr_submit/test_static_grep.py: 21 tests, 0 failed, 0 skipped
+PASS tests/recommend/test_dispatch.py: 16 tests, 0 failed, 0 skipped
+PASS tests/recommend/test_routing_refresh.py: 248 tests, 0 failed, 0 skipped
+PASS tests/skills/test_brainstorm_protocol.py: 4 tests, 0 failed, 0 skipped
+PASS tests/skills/test_codegraph_adoption.py: 50 tests, 0 failed, 0 skipped
+PASS tests/skills/test_issue_protocol.py: 78 tests, 0 failed, 0 skipped
+PASS tests/skills/test_model_alias_policy.py: 13 tests, 0 failed, 0 skipped
+PASS tests/skills/test_primitive_dual_surface_lookup.py: 3 tests, 0 failed, 0 skipped
+PASS tests/skills/test_reflect_input_snapshot.py: 15 tests, 0 failed, 0 skipped
+PASS tests/skills/test_review_severity_rule.py: 62 tests, 0 failed, 0 skipped
+PASS tests/skills/test_sc_recommend_routing_contract.py: 28 tests, 0 failed, 0 skipped
+PASS tests/skills/test_task_builder_merge.py: 68 tests, 0 failed, 0 skipped
+PASS tests/skills/test_task_workspace_smoke.py: 4 tests, 0 failed, 0 skipped
+PASS tests/skills/test_tier2_tavily_consistency.py: 5 tests, 0 failed, 0 skipped
+PASS tests/skills/test_worker_contract.py: 681 tests, 0 failed, 0 skipped
+PASS tests/tasklist/test_bash_policy_contract.py: 2 tests, 0 failed, 0 skipped
+PASS tests/tasklist/test_tasklist_cli.py: 70 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/backtest/test_backtest_e1.py: 2 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/backtest/test_backtest_e2.py: 2 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/backtest/test_backtest_e3.py: 2 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/backtest/test_backtest_e4.py: 2 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/backtest/test_backtest_e5.py: 2 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/backtest/test_backtest_status_separation.py: 3 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/backtest/test_catch_rate_aggregation.py: 7 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/backtest/test_catch_rate_schema.py: 19 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/backtest/test_git_replay_integration.py: 2 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/backtest/test_git_replay_unit.py: 4 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/backtest/test_path_resolution.py: 1 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/backtest/test_replay_executor.py: 6 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/backtest/test_waiver_regreen.py: 1 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/test_behaviour_definition_row.py: 3 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/test_calibrator_assertions.py: 46 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/test_calibrator_eval_cases.py: 35 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/test_codegraph_grounding.py: 5 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/test_cosmetic_counter.py: 1 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/test_counter_key.py: 1 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/test_diagnostic_worker_contract.py: 50 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/test_discriminator_form.py: 2 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/test_discriminator_rows.py: 5 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/test_hardening_h0.py: 2 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/test_hardening_h1.py: 1 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/test_hardening_h2.py: 2 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/test_hardening_h3.py: 3 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/test_hardening_h4.py: 2 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/test_hardening_output_contract.py: 3 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/test_hardening_verdict.py: 6 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/test_hardstop_verdicts.py: 4 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/test_hc_rename_guard.py: 1 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/test_headline_threshold.py: 2 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/test_inline_fallback_parity.py: 3 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/test_locus_card.py: 16 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/test_menu_equality.py: 14 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/test_primitive_differential.py: 3 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/test_primitivegrep_targeting.py: 1 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/test_producers_enumeration.py: 7 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/test_regression_sysbox.py: 3 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/test_threshold_bracket.py: 3 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/test_timestamp_tolerance.py: 3 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/test_validator_assertions.py: 122 tests, 0 failed, 0 skipped
+PASS tests/troubleshoot/test_verdict_source.py: 3 tests, 0 failed, 0 skipped
+PASS tests/unit/test_cli_doctor.py: 30 tests, 0 failed, 0 skipped
+PASS tests/unit/test_cli_install.py: 96 tests, 0 failed, 0 skipped
+```
diff --git a/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/static-checks-log.txt b/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/static-checks-log.txt
new file mode 100644
index 00000000..c9095fd6
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/static-checks-log.txt
@@ -0,0 +1,9 @@
+HEAD=576b6659d23d296a20645c970ac01123e320aaf4 merge-base(master,HEAD)=80f361804b155e3fec842cc552b8f4f0c71b2cdd date=2026-11-07T06:13:57Z
+AC-C2 -> ac-c2.txt: sync-dev rc=0 verify-sync rc=0 
+AC-C1 -> ac-c1.txt: 0 bytes (pass = 0)
+AC-C4 -> ac-c4-index.txt: 0 bytes (pass = 0). Note: .dev/tasks is staged at the end of this task, after this check.
+AC-C5 -> ac-c5.txt: 17 PASS, 0 FAIL
+AC-C6 -> ac-c6-depth-setting.txt
+AC-2.1 deletions -> ac-2.1-deletions.txt: 0 bytes (pass = 0); numstat for the record: 3 0 src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md
+mirror check -> mirror-check.txt: 0 bytes (pass = 0)
+unmirrored -> unmirrored-plugin-copies.txt
diff --git a/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/ac-c5.txt b/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/ac-c5.txt
new file mode 100644
index 00000000..9ca59e93
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/ac-c5.txt
@@ -0,0 +1,19 @@
+# AC-C5 (Check ADDITIVE): added/deleted lines per command file. master = merge base of master and HEAD (the plan's literal command); HEAD = the P2 start.
+# Local master is behind HEAD, so the master column cannot see edits to lines P1 added; the HEAD column does.
+PASS auggie-review: vs master [14 0]; vs HEAD [14 0]
+PASS cleanup: vs master [15 0]; vs HEAD [15 0]
+PASS improve: vs master [15 0]; vs HEAD [15 0]
+PASS cli-eval: vs master [14 0]; vs HEAD [14 0]
+PASS cli-portify: vs master [16 0]; vs HEAD [16 0]
+PASS recommend: vs master [16 0]; vs HEAD [16 0]
+PASS research: vs master [13 0]; vs HEAD [13 0]
+PASS review-translation: vs master [15 0]; vs HEAD [15 0]
+PASS spec-panel: vs master [14 0]; vs HEAD [14 0]
+PASS task: vs master [14 0]; vs HEAD [14 0]
+PASS tasklist: vs master [14 0]; vs HEAD [14 0]
+PASS reflect: vs master [14 0]; vs HEAD [14 0]
+PASS release-split: vs master [14 0]; vs HEAD [14 0]
+PASS tdd: vs master [14 0]; vs HEAD [14 0]
+PASS troubleshoot: vs master [14 0]; vs HEAD [14 0]
+PASS workflow: vs master [15 0]; vs HEAD [2 2] (named exemption: exactly 2 deleted lines)
+PASS brainstorm: vs master [16 0]; vs HEAD [1 1] (named exemption: exactly 1 deleted line)
diff --git a/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/ac-c6-depth-setting.txt b/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/ac-c6-depth-setting.txt
new file mode 100644
index 00000000..68e9eb08
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/ac-c6-depth-setting.txt
@@ -0,0 +1,6 @@
+$ grep -ho '"nestedWorkerMaxDepth":[0-9]*' "${ORCA_RUNTIME_SOURCE_PROFILE_PATH:-$HOME/.config/orca}"/profiles/*/orca-data.json   (AC-C6, spec section 7.1)
+profiles dir: /home/coder/.config/orca/profiles/
+/home/coder/.config/orca/profiles/local-default/orca-data.json
+--- command output:
+"nestedWorkerMaxDepth":1
+--- grep rc=0
diff --git a/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/ac-c2.txt b/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/ac-c2.txt
new file mode 100644
index 00000000..8d0b05dd
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/ac-c2.txt
@@ -0,0 +1,230 @@
+$ make sync-dev
+🔄 Syncing src/superclaude/ → .claude/ for local development...
+✅ Sync complete.
+   Skills:    39 directories
+   Agents:    48 files
+   Commands:  46 files
+   Hooks:     14 files
+   Templates: 52 files
+sync-dev rc=0
+$ make verify-sync
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
+  ✅ launch-job-identity.sh
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
diff --git a/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/unmirrored-plugin-copies.txt b/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/unmirrored-plugin-copies.txt
new file mode 100644
index 00000000..8d7f3e33
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/unmirrored-plugin-copies.txt
@@ -0,0 +1,19 @@
+# plugin command copies left unmirrored by this plan: plugin copy compared with its source before this plan (HEAD) and now
+cleanup: before this plan different; now different
+research: before this plan different; now different
+spec-panel: before this plan different; now different
+reflect: before this plan different; now different
+troubleshoot: before this plan different; now different
+brainstorm: before this plan different; now different
+improve: before this plan identical; now different
+task: before this plan identical; now different
+auggie-review: no plugin copy
+cli-eval: no plugin copy
+cli-portify: no plugin copy
+review-translation: no plugin copy
+release-split: no plugin copy
+tdd: no plugin copy
+tasklist: no plugin copy
+# whole-folder comparison of the two pinned mirror folders (a difference here that is not in mirror-check.txt predates this plan)
+Only in plugins/superclaude/skills/sc-recommend/refs: HOW-WE-WORK.md
+# folder comparison done
Delta diff from the previous reviewed tree (empty on the first review): diff --git a/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/ac-c6-depth-setting.txt b/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/ac-c6-depth-setting.txt
index 423d1a1b..68e9eb08 100644
--- a/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/ac-c6-depth-setting.txt
+++ b/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/ac-c6-depth-setting.txt
@@ -1,4 +1,4 @@
-$ grep -ho nestedWorkerMaxDepth <profiles>/*/orca-data.json   (AC-C6)
+$ grep -ho '"nestedWorkerMaxDepth":[0-9]*' "${ORCA_RUNTIME_SOURCE_PROFILE_PATH:-$HOME/.config/orca}"/profiles/*/orca-data.json   (AC-C6, spec section 7.1)
 profiles dir: /home/coder/.config/orca/profiles/
 /home/coder/.config/orca/profiles/local-default/orca-data.json
 --- command output:
diff --git a/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/p2-static-report.md b/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/p2-static-report.md
index 889de195..7b157614 100644
--- a/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/p2-static-report.md
+++ b/.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/p2-static-report.md
@@ -66,7 +66,7 @@ Question: does a worker that carries a command out by reading its file, with no
 
 ## UNVERIFIED items
 
-- cli-portify's `{work_dir}` stays undefined in the skill (as the plan says). The new delivery-gate resume point (`resume_phase: 4`, `resume_substep: "delivery"`) was added to the skill's resume points (3c and 4a); no run was made.
+- cli-portify's `{work_dir}` stays undefined in the skill (as the plan says). The new delivery-gate resume point (`resume_phase: 4`, `resume_substep: "delivery"`) was added to the skill's "Resume under `--unattended`" paragraph (`src/superclaude/skills/sc-cli-portify-protocol/SKILL.md:576`); the skill's existing resume sections 3c and 4a do not carry it, and no run was made.
 - research's default `--strategy` and `--depth` when the flags are omitted were not run.
 - The directory the TFEP report goes to was not run.
 - Whether the reflect and troubleshoot plugin copies differ from their sources beyond the first hunk was not examined (they already differed before this plan).
Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B4 ac=T21.AC1 at=.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/ac-c6-depth-setting.txt:1 anchor="$ grep -ho nestedWorkerMaxDepth <profiles>/*/orca-data.json   (AC-C6)" chk=n,y,n,n family=evidence-header fix=change the header to the spec 7.1 command first=A1 origin=new: the header misstates the command that was run
F1.2 sev=blocking trigger=B4 ac=scope at=.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/p2-static-report.md:69 anchor="added to the skill's resume points (3c and 4a)" chk=n,y,n,n family=report-wording fix=say it was added to the skill's Resume under --unattended paragraph first=A1 origin=new: the delivery resume point is at src/superclaude/skills/sc-cli-portify-protocol/SKILL.md:576, not in the 3c and 4a sections (lines 561 and 568)
Saved-probe re-check hit locations (may be empty): .dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/ac-c6-depth-setting.txt:1
.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/p2-static-report.md:69
.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/ac-c5.txt:1
.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/artifacts/unmirrored-plugin-copies.txt:1

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
