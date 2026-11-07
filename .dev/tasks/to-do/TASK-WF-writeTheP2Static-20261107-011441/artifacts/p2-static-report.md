# P2 static report

Plan: `TASK-WF-writeTheP2Static-20261107-011441`. Scope: AC-2.1 (the static part) and AC-C1 to AC-C6 (spec sections 7.1 and 7.3), for the 15 commands converted in P2. The live checks (AC-2.2 to AC-2.9) and the P2 phase report belong to the P2 live plan. Nothing was installed, no live Orca run was made, and nothing under `.claude/` is staged.

## Check results

- PASS AC-2.1 (tests): `tests/skills/test_worker_contract.py` passes (684 tests, rc=0). It pins the 31-command set, the nested propagation of nine commands, 25 gate sentences with reversed-outcome negatives, and the artifacts clause of all 15 commands. Evidence: `./artifacts/ac-2.1-tests.txt`.
- PASS AC-2.1 (deletions): `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md` shows 3 added lines and 0 deleted lines. Evidence: `./artifacts/ac-2.1-deletions.txt` (empty).
- PASS AC-C1: Check SCAN prints nothing. Evidence: `./artifacts/ac-c1.txt` (empty).
- PASS AC-C2: `make sync-dev` and `make verify-sync` both exit 0. Evidence: `./artifacts/ac-c2.txt`.
- PASS AC-C3: No baseline-passing test fails (tests/skills 1318 -&gt; 1604 passed; wider run 9164 -&gt; 9165 passed); the 32 named test files and the `tests/troubleshoot/` folder (75 test files in all) each pass. Three baseline test ids are no longer collected because a task of this plan replaced them on purpose (listed in the comparison file). Evidence: `./artifacts/ac-c3-compare.md`, `./artifacts/wider-compare.md`.
- PASS AC-C4: No `.claude/` path is staged. Evidence: `./artifacts/ac-c4-index.txt` (empty).
- PASS AC-C5: The 15 converted command files show 0 deleted lines; `workflow.md` shows exactly 2 and `brainstorm.md` exactly 1, the two named exemptions. Evidence: `./artifacts/ac-c5.txt`.
- PASS AC-C6: 1 Orca profile line (`local-default`), `"nestedWorkerMaxDepth":1`. Evidence: `./artifacts/ac-c6-depth-setting.txt`.
- PASS lint: `make lint` exit 0, no new ERROR, ruff finding or WARN file; three existing size WARN lines grew and are recorded in the comparison file. Evidence: `./artifacts/lint-format-compare.md`.
- PASS format: the four edited test files are formatted. Evidence: `./artifacts/lint-format-compare.md`.
- PASS mirror check: the recommend pairs (2) and the workflow pairs (3) are byte-identical. Evidence: `./artifacts/mirror-check.txt` (empty).

Overall: PASS (11 of 11). The commands, exit codes and counts behind each line are in `./artifacts/static-checks-log.txt`.

Recorded WARN (does not fail): `make lint` already warned about five command files in the baseline (Check 3, more than 200 lines). The same five warn now. Three grew because of their new `## Unattended mode` section: `reflect.md` 305 -&gt; 319, `spec-panel.md` 462 -&gt; 476, `troubleshoot.md` 215 -&gt; 229. There are 0 new WARN files.

The FINAL whole-package review and the archive step of `/sc:implement` run after the commit and the PR (owner instruction, 2026-11-07); their result is in the ledger and in the PR.

## Decisions made where the spec was silent or ambiguous (D-P2-1 to D-P2-25)

Owner decisions of 2026-11-07: D-P2-1 to D-P2-21 are approved as written. D-P2-18 and D-P2-19 are approved as recommended and their alternatives are rejected. D-P2-22 to D-P2-25 were decided on 2026-11-07 by four `/sc:adversarial --depth quick` debates (one per decision, run as sub-agents; inputs and results in `./artifacts/debates/D-P2-2x/`): option A (the recommended one) won all four, so no code changed for them. D-P2-26 was added on your instruction (spec observation on reflect, below).

- D-P2-1 (approved): brainstorm's research-light row runs the `/sc:research` command nested (`--unattended --strategy planning --depth quick --report-dir <report-dir>/nested/research-<n>/`); research-deep (`tech-research`, no Unattended mode) is skipped and recorded in `enrichment_used` with `quality_tier: skipped`.
- D-P2-2 (approved): `--isolate-reviewers` is a flag of the `superclaude reflect run` wrapper, not of `/sc:reflect`; `/sc:reflect --unattended` creates no review snapshot and runs no git write.
- D-P2-3 (approved): `/sc:reflect --remediate` under `--unattended` follows the existing headless auto-accept rule; the plan route runs `sc:workflow` nested with `--handoff none`; the MDTM route (`--depth deep`) is skipped and recorded.
- D-P2-4 (approved): cleanup, improve and spec-panel get an optional file-valued `--output <file>` and default to `<report-dir>/<name>-report.md`; recommend writes `<report-dir>/recommendation.md`; review-translation writes `<report-dir>/context-summary.md` when blocked.
- D-P2-5 (approved): review-translation gains `--context <file>`; without it Phase 1 writes the summary and resolves as blocked, and the re-run with `--context` is a fresh run.
- D-P2-6 (approved): cli-portify takes `--report-dir` only; outside an IronClaude checkout it is `failed`; its new `--resume <contract>` reads `resume_phase` and `resume_substep`, and resuming past a gate counts as approval of that gate's artifact.
- D-P2-7 (approved): recommend refuses `--eval` under `--unattended` and skips its cache, plugin and telemetry writes.
- D-P2-8 (approved): cleanup and improve treat every "Safety Threshold" prompt as "Approval Required" (listed, not applied); improve refuses `--force`.
- D-P2-9 (approved): research refuses an explicit `--strategy intent` or `--strategy unified`; with no `--strategy` it uses `planning`.
- D-P2-10 (approved): spec-panel gains `--target-release <release>` and, under `--unattended` only, `--improve` (writes `<report-dir>/improved-spec.md`); `--mode socratic` is not refused.
- D-P2-11 (approved): tdd passes `--unattended` to its nested `/task` call; the `task` skill turns its two ask-the-user points into a returned question; tdd's other prompts take safe defaults.
- D-P2-12 (approved): `/sc:task` passes the nested flag to `sc:impact-protocol` and to its TFEP `/sc:troubleshoot` call; the TFEP report is written and listed, never committed.
- D-P2-13 (approved): tasklist Stage 10.5 passes `--unattended --output <report-dir>/nested/reflect-<n>/` to each reflect; its two HALT points resolve as blocked.
- D-P2-14 (approved): release-split maps `split-approved` and `no-split` to `succeeded`, `split-with-remediation` to `partial`, `failed` to `failed`; its nested brainstorm and adversarial calls get the flag.
- D-P2-15 (approved): cli-eval replaces the W3 "confirm the exact invocation" step with the command line as given, and blocks on `run` without `--suite`, on the W0 confirmations and on the missing-pipeline case; the create pipeline's three nested calls get the flag.
- D-P2-16 (approved): auggie-review refuses an explicit `--remediation-offer` under `--unattended`, as it refuses `--post-pr`; its `sc:impact-protocol` call is nested.
- D-P2-17 (approved): troubleshoot's Tier 2 fix debate (`sc:adversarial-protocol --compare`) is nested; the `--fix` offer resolves as blocked, so no remediation route runs.
- D-P2-18 (approved as written, alternative rejected): under `--unattended`, cli-eval `run` is blocked unless the command line carries `--suite` and `--output-dir`; every other safety flag takes the command-line value or the CLI default; an empty-HOME workaround is never applied on the worker's own choice.
- D-P2-19 (approved as written, alternative rejected): troubleshoot's `--diagnosability-handoff` is allowed under `--unattended`, packaged through a nested `sc:workflow-protocol`; the step that read the plan path from `.dev/tasks/to-do/<id>/return-contract.yaml` reads the nested worker contract instead.
- D-P2-20 (approved): the shared nested-result rule is added to `WORKER-CONTRACT.md` (Task 19): a nested `blocked` stops the caller as `blocked` with the nested question prefixed by the nested command's name; `failed` or a missing contract takes the caller's own failure path for that step; `succeeded` and `partial` count as the step completing.
- D-P2-21 (approved): tasklist Stage 9 (and the Stage 10 loop-back) passes `--compliance strict --unattended --report-dir <report-dir>/nested/task-<n>/` to every `sc:task` call.
- D-P2-22 (debate: option A won, 0.822 to 0.710): `workflow.md` has a two-line Check ADDITIVE exemption (its "Nested invocations" and "Contract" lines, whose `.dev/reflect/` wording would be false under `--unattended`). Alternative: keep one deleted line and add a new line beside the stale one.
- D-P2-23 (debate: option A won, 0.844 to 0.724; two open points, below): under `--unattended`, task-builder's CLI-mode reflect gate (`superclaude reflect run --depth deep --fix --promote`) is skipped as a whole and `reflect gate skipped (unattended)` goes into the task log. Alternative: run the gate with `--no-promote` and without `--fix`.
- D-P2-24 (debate: option A won for both sites, 0.823 to 0.788; residual risk: release-split Part 4 loses an independent `sc:analyze` check): release-split Part 4 uses inline verification instead of a nested `sc:analyze`, and reflect's Wave 1B optional `tech-research` call is skipped and recorded; neither adds a nested directory.
- D-P2-25 (debate: option A won; convergence 71.4%, status partial, four unresolved points all leaning A): release-split Part 3 can call `/sc:design`, `/sc:workflow` or `/sc:tasklist`, a call site no plan decision or spec row names. Under `--unattended` the section and skill make Part 3 write the specs inline (the skill's own Error Handling fallback), so release-split's nested list stays brainstorm and adversarial.
- D-P2-26 (your instruction on the reflect observation, 2026-11-07; changed after Task 21): reflect's UC-2 Step 1B.3 `sc:impact-protocol` call is a nested call like the adversarial and workflow ones. Under `--unattended` it receives `--unattended --output-dir <report-dir>/nested/impact-<n>/` in place of `<output>/artifacts/impact`, the contract is read from that directory and listed in `artifacts`, and a nested `blocked`, `failed` or missing contract counts as `graph:absent`. Files: `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (one added line after step 0 of Step 1B.3), `src/superclaude/commands/reflect.md` (its "Nested invocations" bullet), and `tests/skills/test_worker_contract.py` (reflect's nested list is now adversarial, workflow, impact, plus one test that the skill gives the flag and the directory). The spec row for reflect names the call.

Review findings accepted as they stand (owner, 2026-11-07): the remaining 13 medium and 13 low findings of the plan review were not fixed and the plan was not re-reviewed.

## P1-C5: decided NO

Question: does a worker that carries a command out by reading its file, with no `Skill` call, satisfy WC-7? Owner answer, 2026-11-07: NO. The command must be run for real, with a `Skill` or slash-command call at the top level. The plan's sentences that call P1-C5 open are superseded by `./artifacts/owner-decision-p1-c5.md`, which every reviewer received with the constraints. No task in this plan changed.

- The P2 live plan must make spec section 7.2 step 5 condition 2 require the `Skill` or slash-command call, and must fail a worker that made none.
- Follow-ups for you (this plan edits none of these files):
  - (a) the `APPROVED.md` row for P1-C5;
  - (b) the wording of spec section 7.2 step 5;
  - (c) owner accepted the 11 P1 rows (lc01, lc02, lc04, lc05, lc06, lc07, lc08, lc14, lc17, lc18, lc22) recorded PASS on condition 2, as they stand; P1 is not reopened and nothing is re-run; add this to the `APPROVED.md` row for P1-C5.

## UNVERIFIED items

- cli-portify's `{work_dir}` stays undefined in the skill (as the plan says). The new delivery-gate resume point (`resume_phase: 4`, `resume_substep: "delivery"`) was added to the skill's "Resume under `--unattended`" paragraph (`src/superclaude/skills/sc-cli-portify-protocol/SKILL.md:576`); the skill's existing resume sections 3c and 4a do not carry it, and no run was made.
- research's default `--strategy` and `--depth` when the flags are omitted were not run.
- The directory the TFEP report goes to was not run.
- Whether the reflect and troubleshoot plugin copies differ from their sources beyond the first hunk was not examined (they already differed before this plan).
- Whether the running Orca app re-reads the depth setting file (AC-C6, spec text) was not run.
- No live run was made for any of the 15 commands: every `--unattended` behavior above is pinned by text and tests only.

## Repo paths created or changed under `src`, `tests` and `plugins`

The list equals the paths printed by `git status --short --untracked-files=all -- src tests plugins` (52 paths).

### Command files (17)

- `src/superclaude/commands/auggie-review.md`
- `src/superclaude/commands/brainstorm.md`
- `src/superclaude/commands/cleanup.md`
- `src/superclaude/commands/cli-eval.md`
- `src/superclaude/commands/cli-portify.md`
- `src/superclaude/commands/improve.md`
- `src/superclaude/commands/recommend.md`
- `src/superclaude/commands/reflect.md`
- `src/superclaude/commands/release-split.md`
- `src/superclaude/commands/research.md`
- `src/superclaude/commands/review-translation.md`
- `src/superclaude/commands/spec-panel.md`
- `src/superclaude/commands/task.md`
- `src/superclaude/commands/tasklist.md`
- `src/superclaude/commands/tdd.md`
- `src/superclaude/commands/troubleshoot.md`
- `src/superclaude/commands/workflow.md`

### Skill and ref files (25)

- `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md`
- `src/superclaude/skills/sc-auggie-review-protocol/refs/remediation-handoff.md`
- `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`
- `src/superclaude/skills/sc-cli-eval-protocol/SKILL.md`
- `src/superclaude/skills/sc-cli-eval-protocol/refs/integration-map.md`
- `src/superclaude/skills/sc-cli-eval-protocol/refs/run-pipeline.md`
- `src/superclaude/skills/sc-cli-portify-protocol/SKILL.md`
- `src/superclaude/skills/sc-recommend/SKILL.md`
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md`
- `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md`
- `src/superclaude/skills/sc-release-split-protocol/SKILL.md`
- `src/superclaude/skills/sc-release-split-protocol/refs/adversarial-integration.md`
- `src/superclaude/skills/sc-review-translation-protocol/SKILL.md`
- `src/superclaude/skills/sc-task-protocol/SKILL.md`
- `src/superclaude/skills/sc-tasklist-protocol/SKILL.md`
- `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
- `src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md`
- `src/superclaude/skills/sc-troubleshoot-protocol/refs/remediation-handoff.md`
- `src/superclaude/skills/sc-workflow-protocol/SKILL.md`
- `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md`
- `src/superclaude/skills/task-builder/SKILL.md`
- `src/superclaude/skills/task/SKILL.md`
- `src/superclaude/skills/tdd/SKILL.md`
- `src/superclaude/skills/tdd/refs/build-request-template.md`
- `src/superclaude/skills/tdd/refs/validation-checklists.md`

### Core file (1)

- `src/superclaude/core/WORKER-CONTRACT.md`

### Plugin mirrors (5)

- `plugins/superclaude/commands/recommend.md`
- `plugins/superclaude/commands/workflow.md`
- `plugins/superclaude/skills/sc-recommend/SKILL.md`
- `plugins/superclaude/skills/sc-workflow-protocol/SKILL.md`
- `plugins/superclaude/skills/sc-workflow-protocol/refs/return-contract.md`

### Test files (4)

- `tests/commands/test_workflow_command.py`
- `tests/skills/test_brainstorm_protocol.py`
- `tests/skills/test_sc_recommend_routing_contract.py`
- `tests/skills/test_worker_contract.py`

## Plugin command copies left unmirrored

Only `recommend.md` and `workflow.md` (and the `sc-recommend` and `sc-workflow-protocol` skill files) are mirrored, because tests pin them. For the other converted commands (`./artifacts/unmirrored-plugin-copies.txt`):

- Identical to the source before this plan, now behind it: improve, task.
- Already different from the source before this plan: cleanup, research, spec-panel, reflect, troubleshoot, brainstorm.
- No plugin copy exists: auggie-review, cli-eval, cli-portify, review-translation, release-split, tdd, tasklist.
- `src/superclaude/core/WORKER-CONTRACT.md` has no plugin copy.

## The fifteen commands, their report-directory flag and required brief flags (input to the P2 live plan)

Under `--unattended` the brief passes exactly one report directory. The brief flags below are the ones the `WORKER-CONTRACT.md` table now requires.

- auggie-review: `--output-dir <dir>` or `--report-dir <dir>`. Brief: `--output-dir <dir>`; never `--post-pr` (or `--remediation-offer`).
- cleanup: `--report-dir <dir>` only. No further brief flag.
- improve: `--report-dir <dir>` only. No further brief flag (`--force` is refused).
- cli-eval: `--report-dir <dir>` only. Brief: `run` with `--suite <name>` and `--output-dir <dir>` (the eval run directory) plus `--report-dir <dir>`; other safety flags as wanted, else the CLI defaults.
- cli-portify: `--report-dir <dir>` only. Brief: `--report-dir <dir>`; `--resume <contract>` to continue past an approval gate.
- recommend: `--report-dir <dir>` only. No further brief flag (`--eval` is refused).
- research: `--report-dir <dir>` only. No further brief flag (an explicit `--strategy intent` or `unified` is refused).
- review-translation: `--report-dir <dir>` only. Brief: `--report-dir <dir>`; `--context <file>` once the context is confirmed.
- spec-panel: `--report-dir <dir>` only (`--output` is file-valued). Brief: `--report-dir <dir>`; `--target-release <release>` for TDD inputs.
- task: `--report-dir <dir>` only. No further brief flag.
- tasklist: `--output <output-dir>` or `--report-dir <dir>`. No further brief flag.
- reflect: `--output <dir>` or `--report-dir <dir>`. Brief: `--remediate` is allowed under `--unattended` (the headless rule answers it); `--no-promote` when the coordinator owns folder moves.
- release-split: `--output <dir>` (`-o`) or `--report-dir <dir>`. Brief: spec-shaped input; default `--r1-scope`; never `--interactive`; its gates resolve as blocked.
- tdd: `--report-dir <dir>` only (`--output` names the TDD file). Brief: a precise component prompt, not a bare topic; `--output <file>`; its gates resolve as blocked.
- troubleshoot: `--output-dir <dir>` or `--report-dir <dir>`. Brief: no `--fix` under `--unattended` (the offer resolves as blocked); a short `--depth deep` input resolves as blocked.

## Spec observations for the coordinator

- Brainstorm's research-light row names `Skill sc-research-protocol`, which does not exist in this repo (D-P2-1).
  - /sc:research is a command, there is no skill protocol like the others
- `--isolate-reviewers` is a flag of the `superclaude reflect run` Python CLI, not of `/sc:reflect` (D-P2-2).
  - Confirmed
- `/sc:task` never reaches the `task` or `task-builder` skills, so their `deferred:P2` entries are reached only through tdd, reflect and troubleshoot.
  - confirmed
- The spec's tasklist row names only Stage 10.5, while Stage 9 also calls `sc:task` (D-P2-21).
- The spec does not say how a nested `blocked` result reaches the caller, which D-P2-20 settles.
  - Update accordingly or if no update is avbailable, /sc:brainstorm --depth quick
  - Done after Task 21: an update was available, so no brainstorm was needed. Spec section 2.1 (the "Nested propagation rule" term) now carries the D-P2-20 rule word for word. 
- Release-split Part 3 can call `/sc:design`, `/sc:workflow` or `/sc:tasklist`, which no spec row names (D-P2-25).
  - Update the spec to naem this
  - Done after Task 21: the spec's release-split row (section 3.1) now names Part 3 (specs written inline under `--unattended`) and Part 4 (inline verification), as decided by the D-P2-24 and D-P2-25 debates.
- Reflect's UC-2 Step 1B.3 calls `sc:impact-protocol` (a command that accepts `--unattended`). No plan decision or spec row names that call, and reflect's nested list was pinned to adversarial and workflow, so the call was left unchanged when Task 21 ran.
  - update the spec accordingly
  - Done after Task 21: the spec's reflect row (section 3.1) now names the call as nested (`nested/impact-<n>/`) and names the skipped Wave 1B `tech-research` call, and the command, skill and tests follow it (D-P2-26).
- cli-eval's `refs/create-pipeline.md` repeats the three create-pipeline call sites without the `--unattended` arguments. The plan's file list leaves it out; `SKILL.md` and `refs/integration-map.md` carry the arguments. No edit was made.
  - Confirmed

Open points left by the debates (recorded, no change made):

- D-P2-23: `src/superclaude/skills/task-builder/SKILL.md` (the paragraph at about line 410) does not say whether the builder leaves the CLI-mode reflect gate item out of the generated task or writes it in skip form. The spec (section 2.1) says a skip is recorded "in its contract", the text says "in the task log"; whether tdd's `artifacts` list reaches the task log is UNVERIFIED. Without that gate the coordinator runs `/sc:reflect --mode post --no-promote` itself as a plan step.
- D-P2-24: release-split Part 4 loses an independent `sc:analyze` check (unproven, recorded as residual risk by the debate).
- cli-eval's `refs/create-pipeline.md` (your note: "Confirmed"): no edit made, as the observation says.

## Debates, spec edits and the global install (after Task 21)

- The four decisions D-P2-22 to D-P2-25 were first dispatched as four Orca workers (run `run_8acd21534f6b`). All four refused before running, correctly: the brief guard found `~/.claude/commands/sc/adversarial.md` without an `## Unattended mode` section while this worktree's `.claude/commands/sc/adversarial.md` has one ("command copies disagree (stale copy)"). The fix is `superclaude install`, which the constraints of this work ruled out, so it was not run. The four debates were then run as ordinary sub-agents calling `/sc:adversarial --depth quick` without `--unattended` (no guard applies to them). The P2 live plan needs the global install first.
- Spec file `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` edited three times, as you instructed in this report: section 2.1 (nested-result rule), the reflect row and the release-split row of section 3.1. Nothing else in the spec, and not `APPROVED.md` or the P1 reports, was edited (the P1-C5 follow-ups (a), (b), (c) above are still yours).
- A separate session works the six leftover `refs/superclaude/implement/` refs of two other plans in worktree `finish-leftover-implement-plans` (branch `ironbelly/finish-leftover-implement-plans`) and will open its own PR.

## Plan gaps and process notes

- The plan was edited once before the run, to record your owner decisions; its hash is pinned in the ledger and it was not edited again. Your P1-C5 answer and the acceptance of the 11 P1 rows arrived after that, so they are in `./artifacts/owner-decision-p1-c5.md`, which was added to the constraints slot of every later reviewer prompt. A first ledger and retries folder made before the plan edit are kept in `./artifacts/superseded-ledger/`.
- Reviewer prompts: each saved prompt is in `./artifacts/retries/T<n>/`; because reviewers must not read the retries folder, a byte-identical copy was placed in `/tmp/impl2/prompts/` (outside the repo) and each reviewer was told to read that copy. The helper scripts that built the prompts and the evidence logs are in `/tmp/impl2/` and are not part of the repo.
- Task 11: a first saved prompt was built, then removed and rebuilt before any reviewer read it, because the pre-review test run failed on a capitalised gate sentence (fixed in the command).
- Blocking findings from reviewers, each fixed and re-reviewed by a fresh reviewer: Task 3 (gate sentences missing from the checked phrases), Task 6 (skill paragraph covered 2 of 5 clarification sites), Task 8 (both `--output` and `--report-dir` allowed), Task 12 (Contract bullet lacked "written on every outcome"), Task 14 (tdd skill never told the builder the caller is unattended), Task 15 (reflect skill Phase A lacked the unattended workflow arguments).
- cleanup's gate sentence was missing from its test entry after Task 2 (found in Task 3's review); it was added in Task 20, test file only.
- Check ADDITIVE: local `master` is behind `HEAD`, so the plan's literal command (against the merge base with `master`) cannot see edits to lines that P1 added. `ac-c5.txt` shows both columns: against the merge base and against `HEAD` (the P2 start).
- Minor reviewer notes (not blocking) are in `./artifacts/retries/T<n>/notes.md` and cited in the ledger with `notes@` tokens.

## Commit list for your approval (nothing is committed)

Group 1, product changes (52 paths, the list above): 17 command files, 25 skill and ref files, 1 core file, 5 plugin mirrors, 4 test files. Added after Task 21 (group 1b): `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (three owner-requested edits, see below).

Group 2, the plan package (already staged or staged by this task): everything under `.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/` (the plan, `source.md`, `return-contract.yaml`, `progress.md`, and `artifacts/`).

Group 3, plan-review evidence the package cites, currently untracked (recommended: include, as the P1 closeout commit did):

- `.dev/reflect/pre-TASK-WF-writeTheP2Static-20261107-011441-20261107013500/` (the plan review folder, named in the package's `return-contract.yaml`)
- `docs/memory/reflect/deviation-patterns-OrcaCLICommandRefactor-P2.md`

Never staged: anything under `.claude/` (the `make sync-dev` copies there are gitignored).

## Staging

`git add .dev/tasks` stages this report and every artifact of this package. Nothing under `.claude/` is staged. Nothing is committed or pushed by this plan.