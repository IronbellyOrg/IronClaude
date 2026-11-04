# Tier 1 reflection card: P0 live plan (UC-1, pre-execution)

- Spec: `.dev/tasks/to-do/TASK-WF-writeTheP0LivePl-20261103-215902/source.md`
- Tasklist: `.dev/tasks/to-do/TASK-WF-writeTheP0LivePl-20261103-215902/TASK-WF-writeTheP0LivePl-20261103-215902.md` (below: `plan`)
- Executor rules graded against: `~/.claude/skills/sc-implement-protocol/SKILL.md`, `~/.claude/skills/sc-implement-protocol/refs/qa.md`, `~/.claude/skills/sc-implement-protocol/refs/managed-workspace.md`
- Coverage: `artifacts/coverage-matrix.yaml` (parsed 0, inferred 24, coverage_pct_union 0.75, parsed-sparse). Excerpts: `artifacts/grounding-hunks.md`.
- Findings: 3 blocking, 8 should-fix, 6 minor (17 total).

Severity key: **blocking** = the executor would halt, breach a quotable Constraint, or get FINAL `issues` (`E-ARCHIVE-BLOCKED`); **should-fix** = a correct run can produce a false FAIL or an unverifiable AC, or the executor has to guess; **minor** = clarity.

## Analyzer: root cause and deviation

### F-001: The executor's own re-staging after the archive breaks the "leave unstaged" Constraint
- Severity: blocking
- Claim: Task 5 unstages the superseded package with `git restore --staged`. But the managed executor must run `git add .dev/tasks` again after the helper moves the package to `done/`, and the ledger rule keeps `.dev/tasks` staged. That re-add stages the untracked superseded package `.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/`, which the plan's Constraints and source.md say must stay unstaged. `staged.txt` is taken before the archive, so it would show a clean result that no longer holds.
- Evidence:
  - `plan:24` "Leave `.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/` untouched and unstaged."
  - `plan:139` "run `git add .dev/tasks` followed by `git restore --staged .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950`"
  - `~/.claude/skills/sc-implement-protocol/refs/managed-workspace.md:36` "After the helper moves a package to `done/`, the new path needs `git add .dev/tasks` again."
  - `~/.claude/skills/sc-implement-protocol/refs/ledger.md:3` "A managed package's ledger (`<pkg>/progress.md`) sits under `.dev/tasks/`, which is always staged (`git add .dev/tasks`)."
  - `git status --porcelain` (run now) lists `?? .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/`, so a bare `git add .dev/tasks` stages it.
- Tag: Grounded
- Fix: Add a Constraints bullet: "Every `git add .dev/tasks` this run makes, including the executor's re-add after the archive move, is immediately followed by `git restore --staged -- .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950`." Retitle `staged.txt` as the pre-archive snapshot and say that the coordinator checks `git diff --cached --name-only` once more after `archived` is reported.

### F-002: The managed FINAL will read the intended failure logs as failures and block the archive
- Severity: blocking
- Claim: The managed FINAL returns `issues` when a log cited on a task's latest `complete` line shows a failure at its outcome line. Task 1's evidence log `symptom-check.txt` is required to show three failing tests, and a live check that fails is recorded on purpose. The plan never tells the FINAL reviewer that those failures are the expected outcome. So the FINAL can return `issues`, which gives `E-ARCHIVE-BLOCKED`, even when every task did what it should.
- Evidence:
  - `~/.claude/skills/sc-implement-protocol/refs/qa.md:310` "`issues` when an AC is unmet at the end state, ... a plan `## Constraints` item is violated, or a log cited on a task's latest `complete` line shows a failure at its outcome line."
  - `plan:50` "`./artifacts/symptom-check.txt` shows `test_clean_tree_passes_ruff_check`, `test_synthetic_import_anthropic_is_flagged_by_ruff` and `test_ban_message_references_fr_g1` failing."
  - `plan:25` "A failed live check is a recorded result: it is not retried, rerun or repaired ... A task is compliant when its check ran as written and every step's result is recorded faithfully"
- Tag: Grounded
- Fix: Add a Constraints bullet that names the expected outcome of each log: "`symptom-check.txt` passes when it shows exactly those three failures; an `lc<N>-*` step file showing FAIL is a recorded result, not a task failure; only `lc<N>-result.md`, `ac-0.5.md` and `ac-0.6.md` carry verdicts." In Tasks 2-4, have every `lc<N>-result.md` end with a line `Recording status: complete (verdict recorded, not a task failure)`, so the FINAL's outcome line is that line and not a raw FAIL.

### F-003: No way out when a worker waits on a person or asks for a decision
- Severity: blocking
- Claim: Step 3 says "keep waiting until `worker_done` arrives". Its only exit is Orca's final-turn stall proof. Step 2 can find the worker parked on a prompt only a person can answer (non-null `agentWait`), and step 3 refuses decision questions. In both cases the worker never sends `worker_done` and never ends its turn, and Orca's guidance says a waiting worker is healthy and must not be stopped for silence. The executor would wait forever or make up a stop and release procedure, which Constraint 7 forbids ("not ... repaired"). The spec's settle rule needs a positive stall proof before a stop.
- Evidence:
  - `plan:33` "keep waiting until `worker_done` arrives. ... a request for a decision is not answered, and step 3 fails."
  - `.dev/orca-command-refactor/inventory/orca-capabilities.md:129` "observation.agentWait names a worker parked on a prompt only a human can answer ... A waiting worker is healthy, not failed."
  - `src/superclaude/core/WORKER-CONTRACT.md:73` "A crashed or stalled attempt is settled by the coordinator: after Orca's positive stall proof it stops the worker and sets the old Task `failed --result cancelled`"
- Tag: Grounded
- Fix: Add a Settle sub-bullet to the procedure: "When a step-2 sample shows non-null `agentWait`, or a `question` asks for a decision, record step 2 or step 3 FAIL with that sample or message as the proof. Then stop the worker (the `worker-stop` flag form captured in Task 1, see F-005), run `task-update --status failed --result cancelled`, and continue with Step 4, Step 5, Step 6, the evidence copy, Step 7 and Remove, recording each one." State that this is the only stop the executor makes.

### F-004: Step 7 drops `--run`, and the run that Task 1 creates is never used
- Severity: should-fix
- Claim: Spec 7.2 step 7 scopes the reclaimable list to the run. The plan's step 7 has no `--run`, and the run id saved in Task 1 is never passed to any later call. "The list returns no rows" then covers every run on the machine, so a reclaimable worker from any other session makes a correct check FAIL.
- Evidence:
  - `spec:293` "`ORCA orchestration worker-list --run <run_id> --terminal-state reclaimable --json` returns no rows"
  - `plan:38` "`orca orchestration worker-list --terminal-state reclaimable --json` ... Pass: the list returns no rows."
  - `plan:46` "`orca orchestration run-create --objective ...` and save the receipt to `./artifacts/live-run.json`" (no later use of the run id)
- Tag: Grounded
- Fix: In step 7 use `worker-list --run <run_id from ./artifacts/live-run.json> --terminal-state reclaimable --json`. In step 1, pass the run id to `task-create`/`worker-start` if `--help` (F-005) shows a `--run` flag, and save it in `lc<N>-step1.txt`.

### F-005: Several Orca flags and receipt fields are used without any check
- Severity: should-fix
- Claim: The repo's Orca capability record documents removal as `worktree rm --worktree id:<repoId>::<worktreePath>`, and records `--no-parent` only for `worktree set`. The plan uses `worktree rm --worktree path:<path>` and `worktree create ... --no-parent`. `check --ack <delivery_id>`, `worktree list --json`, `run-create --objective` and the receipt field `coordinator_handle` (used in an AC) appear nowhere in the record. A flag that does not exist fails in the middle of a live check. That gets recorded as a live-check FAIL that reopens spec section 1, or forces a change to Constraint text (F-017).
- Evidence:
  - `.dev/orca-command-refactor/inventory/orca-capabilities.md:115` "`[CLI]` line 100: \"ORCA worktree rm --worktree id:<repoId>::<worktreePath> --force --json\""
  - `.dev/orca-command-refactor/changes/CR-01-feature-worktree-hierarchy.md:50` "`worktree create --parent-worktree <selector>`, `worktree set --parent-worktree` / `--no-parent`"
  - `plan:29` "`orca worktree create --repo id:de550e99-... --name p0-live-<name> --base-branch ironbelly/OrcaCLICommandRefactor-Specs --no-parent --json`"
  - `plan:51` "holds a run id whose `coordinator_handle` equals the session's `ORCA_TERMINAL_HANDLE`."
- Tag: Grounded (that the record lacks these flags); [INFERRED] (whether the flags exist in Orca 1.4.237)
- Fix: In Task 1, save `orca <verb> --help` for `worktree create`, `worktree rm`, `worktree list`, `orchestration run-create`, `task-create`, `worker-start`, `check`, `worker-show`, `worker-read`, `worker-release`, `worker-list` and `worker-stop` to `./artifacts/orca-help.txt`. Add an AC that every flag and selector the procedure uses appears in that output, and that `coordinator_handle` (or its real field name) appears in `live-run.json`. Fix the procedure text before Task 2 if one is missing; the plan has not been pinned yet.

### F-006: The branch-remaining check probably looks for the wrong name
- Severity: should-fix
- Claim: `git branch --list p0-live-<name>*` assumes Orca names the branch exactly after `--name`. This worktree was created by Orca with the name `OrcaCLICommandRefactor-Specs`, and its branch is `ironbelly/OrcaCLICommandRefactor-Specs`, which points to a user prefix. The check would print nothing, and Task 5 would wrongly report that no branch remains.
- Evidence:
  - `plan:39` "plus `git branch --list p0-live-<name>*` to record whether its branch remains."
  - `.dev/orca-command-refactor/changes/CR-01-feature-worktree-hierarchy.md:41` "observed as `/home/coder/workspaces/worktrees/<repo>/<name>` for this spec's own Orca-created worktree"; current branch `ironbelly/OrcaCLICommandRefactor-Specs` (`git rev-parse --abbrev-ref HEAD`).
- Tag: [INFERRED]
- Fix: Save `git -C <path> branch --show-current` to `lc<N>-branch.txt` before Remove, then check `git branch --list <that exact name>`.

### F-007: The workflow worker runs `git add .dev/tasks`, and nothing records it
- Severity: should-fix
- Claim: At P0 no command defers its own staging (no `--unattended` yet), so the `/sc:workflow` worker stages `.dev/tasks` in the disposable worktree. The contract says a worker outside a grant "never runs `git add` (including `git add .dev/tasks`)". Step 6 checks paths only, so a staged path under the new package passes and the gap is never recorded. It also contradicts the plan's claim that worktree create and remove are the only git-state changes.
- Evidence:
  - `src/superclaude/skills/sc-workflow-protocol/SKILL.md:28` "`.dev/tasks/` is always staged (`git add .dev/tasks`)"
  - `src/superclaude/core/WORKER-CONTRACT.md:42` "Outside that grant a worker never runs `git add` (including `git add .dev/tasks`)"
  - `plan:22` "The only git-state changes are the disposable worktrees that `orca worktree create` makes and `orca worktree rm` removes"
- Tag: Grounded
- Fix: In Step 6, also save `git -C <path> diff --cached --name-only` to `lc<N>-index-after.txt`. In Task 3, have `lc2-step6.md` and the phase report record the staging as a known P0 WC-9 gap that P1's deferral closes. Reword `plan:22` to "the executor's own git-state changes".

### F-008: Nothing says what to do on resume, so a re-run can start a second worker
- Severity: should-fix
- Claim: If the executor stops inside Tasks 2-4 (for example `E-RESUME-NEEDED`) and is run again, the procedure starts again from Worktree. A second `worktree create --name p0-live-<name>` either collides with the kept branch or starts a second worker. Constraint 7 forbids that ("no second worker is started for it").
- Evidence:
  - `plan:25` "it is not retried, rerun or repaired, and no second worker is started for it."
  - `plan:39` "The branch is not deleted."
  - `~/.claude/skills/sc-implement-protocol/SKILL.md:34` "`E-RESUME-NEEDED` | Something outside the step failed ...; re-run the same command"
- Tag: Grounded
- Fix: Add a Resume sub-bullet: "On re-entry, if `./artifacts/lc<N>-step1.txt` exists, never create a worktree or start a worker again. Continue from the first step that has no evidence file, using the dispatch_id and path saved in `lc<N>-step1.txt` and `lc<N>-worktree.json`. If `lc<N>-worktree.json` exists but `lc<N>-step1.txt` does not, reuse that worktree."

## QA: coverage and acceptance

### F-009: Task 1's git-status AC fails on a correct run: five untracked paths exist, not four
- Severity: should-fix
- Claim: The AC allows "the four untracked folders that existed before the plan". The worktree already has five untracked paths outside this package. The fifth is `.dev/reflect/pre-TASK-WF-writeTheP0LivePl-...`, written by the plan's own Wave-4 reflect. A reviewer reading the AC literally finds an unlisted change.
- Evidence:
  - `plan:52` "`git status --porcelain` shows no change outside this package and the four untracked folders that existed before the plan."
  - `git status --porcelain` (run now): two `.dev/brainstorms/...` folders, `.dev/reflect/pre-TASK-WF-writeTheP0LivePl-20261103-215902-20261103220351/`, `.dev/review-loop-convergence/`, `.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/`, plus this package.
- Tag: Grounded
- Fix: List the allowed paths by name, including `.dev/reflect/pre-TASK-WF-writeTheP0LivePl-20261103-215902-*`. Better: save `git status --porcelain` at the start of Task 1 to `./artifacts/status-baseline.txt`, and make the AC "no path beyond status-baseline.txt and this package".

### F-010: Several ACs have no saved evidence file
- Severity: should-fix
- Claim: The managed reviewer works from the diff and the package's `./artifacts/` files. These ACs name live state that no file records: "`orca worktree list --json` no longer lists ... and the feature worktree's HEAD is unchanged" (Tasks 2-4), Task 1's `git status` check and Task 5's `git rev-parse HEAD`. A claim the reviewer cannot verify with no evidence row counts as `ac-outcome-missing=yes`, which is blocking and costs a fix pass.
- Evidence:
  - `plan:80` "`orca worktree list --json` no longer lists the `p0-live-troubleshoot` worktree, and the feature worktree's HEAD is unchanged." (same at `plan:106`, `plan:131`)
  - `plan:145` "`git rev-parse HEAD` still prints `8db29f1165508187b7a14a48f2f66793e269d596`."
  - `~/.claude/skills/sc-implement-protocol/refs/qa.md:87` "a claim the reviewer could not verify has no evidence row (`ac-outcome-missing=yes`, anchored on the AC words)."
- Tag: Grounded
- Fix: Add saved outputs: `orca worktree list --json` to `lc<N>-worktree-list-after.json`, `git rev-parse HEAD` to `lc<N>-head-after.txt`, Task 1's status into `preflight.md`, and Task 5's HEAD to `./artifacts/head-final.txt`. Have each AC cite its file.

### F-011: An absent `agentWait` counts as a pass
- Severity: minor
- Claim: "Never non-null" is also true when the field is missing, and Orca says a missing field means it never looked. Step 2 can pass without Orca ever checking.
- Evidence: `plan:32` "Pass: `observation.agentWait` is never non-null."; `.dev/orca-command-refactor/inventory/orca-capabilities.md:129` "An absent field means it never looked"
- Tag: Grounded
- Fix: Record `absent` separately in each sample line. Write step 2 as "PASS (observed)" only when at least one sample is a non-absent null; otherwise "PASS (not observed)", and carry that wording into the phase report.

### F-012: The unattended-section grep exits 1 on its passing result
- Severity: minor
- Claim: With two files and no match, `grep -c` prints `file:0` for each file and exits 1. An executor that treats a non-zero exit as failure records a false FAIL.
- Evidence: `plan:30` "`grep -c '^## Unattended mode' <path>/.claude/commands/sc/<command>.md ~/.claude/commands/sc/<command>.md` ... must show 0 for both copies"
- Tag: [INFERRED] (standard grep exit behaviour)
- Fix: State "exit 1 with both counts 0 is the pass; exit 2 (a file is missing) is a FAIL."

### F-013: The wait command runs longer than the default Bash tool timeout
- Severity: minor
- Claim: `check --wait --timeout-ms 240000` blocks for up to 240 s. The executor's Bash tool defaults to 120 s, so the call is killed first unless the plan sets a longer timeout.
- Evidence: `plan:32` "`orca orchestration check --wait --types \"worker_done,escalation,question\" --timeout-ms 240000 --json`"
- Tag: [INFERRED] (Claude Code Bash default timeout of 120000 ms)
- Fix: Add "run each wait with a Bash tool timeout of at least 300000 ms".

### F-014: AC-0.6 needs a transcript read that the plan does not place
- Severity: minor
- Claim: AC-0.6 must be answered "before Step 5". Before step 5, though, the transcript is read only when a wait ends with no message, which may never happen. The executor has to add a read the plan does not name.
- Evidence: `plan:73` "Before Step 5, answer AC-0.6 (spec line 303) from this worker's transcript"; `plan:33` "When a turn ends with no message, read `orca orchestration worker-read ... --source transcript --json`"
- Tag: Grounded
- Fix: "After Step 4, read the first page with `worker-read --dispatch <id> --source transcript --json`, save it as `lc1-ac06-page.json`, and answer AC-0.6 from it."

## Refactorer: structure

### F-015: The brief's `Worktree:` slot uses text the template does not offer
- Severity: minor
- Claim: The template allows only "shared feature worktree" or "child worktree created by Orca with worker-start --worktree new-child ...". The briefs use a third, free-text value. 7.2 does call for a disposable worktree, so the deviation is justified, but the plan does not say so.
- Evidence: `src/superclaude/core/WORKER-CONTRACT.md:174` "Worktree: <shared feature worktree | child worktree created by Orca with worker-start --worktree new-child --base-branch <feature branch>>"; `plan:67` "Worktree: disposable worktree created by Orca from ironbelly/OrcaCLICommandRefactor-Specs for this check only; you are its only writer."
- Tag: Grounded
- Fix: Add one sentence to Constraints: "The `Worktree:` slot names the 7.2 disposable worktree, a deliberate departure from the two template values (spec line 282)."

### F-016: The `Depends on:` lines do nothing and one of them misleads
- Severity: minor
- Claim: The executor ignores dependency fields and runs tasks in source order. Task 4's "Depends on: Task 2" suggests it could run beside Task 3, which never happens and should not happen, because the coordinator runs one live check at a time.
- Evidence: `~/.claude/skills/sc-implement-protocol/SKILL.md:79` "Ignore MDTM fields (`depends-on`, `agent:`, `wave:`, `compliance:`) except `independent`."; `plan:112` "Depends on: Task 2"
- Tag: Grounded
- Fix: Change it to "Depends on: Task 3", or drop all four lines and say "tasks run strictly in order".

### F-017: Putting the whole live-check procedure in Constraints makes any forced change a blocking breach
- Severity: should-fix
- Claim: The full procedure, with every flag, sits under `## Constraints`. Any deviation from it, even one forced by a flag Orca rejects (F-005), is a quoted-constraint breach, which is blocking. A FAIL recorded faithfully is fine, but a corrected command line is not. A wrong flag in the plan therefore halts the executor instead of being recorded.
- Evidence: `plan:28` "Live-check procedure, followed by Tasks 2, 3 and 4 ..." (inside `## Constraints`, `plan:17`); `~/.claude/skills/sc-implement-protocol/refs/qa.md:52` "`quoted-constraint-breach` ... The diff violates a parent `## Constraints` ... item or an explicit task instruction"
- Tag: Grounded
- Fix: Move the procedure into its own `## Live-check procedure` section, referenced from Tasks 2-4. Keep only the true prohibitions in Constraints (no edits, no git writes, no retry, the executor makes every Orca call). Add a rule that a flag correction backed by `orca-help.txt` is recorded in `lc<N>-result.md`.

## Self-Audit (what was checked)

- source.md line 1 in full, and every plan line 1-146.
- Every spec citation the plan makes, checked against the spec: 83-100 (2.3), 238, 278 (AC-C6), 281-293 (7.2), 298-305 (7.3 P0). The line numbers and wording match. The plan's only departure from 7.2 is step 7's missing `--run` (F-004). Its step-2 wait of 240 s instead of 900 s is a stricter, allowed choice.
- WORKER-CONTRACT.md section 5 (lines 165-202). The plan's guard line matches line 170 byte for byte. The `P0 only:` lines fill the slot as line 185 allows. The troubleshoot brief has no `--fix` or `--depth`, as line 201 requires. The workflow brief passes `--handoff none` (line 202). The adversarial brief passes `--output` (line 191).
- The inputs: the three accepted failures are at `t1-accepted-failures.md:24-26`. `ac-c6-depth-setting.txt` shows `"nestedWorkerMaxDepth":1`. `decisions/D1/option-a.md` and `option-b.md` are committed at `8db29f11` (`git cat-file -e`) and have 23 and 25 lines. `README.md:53` has `## Installation`. `8db29f11` resolves to `8db29f1165508187b7a14a48f2f66793e269d596`.
- The report-file rules: troubleshoot `--output-dir` and `--type test` exist (`src/superclaude/commands/troubleshoot.md:8,50,56`). The `**Status**:` line is at `report-template.md:14`. The workflow contract's `status` is at `return-contract.md:7`. The adversarial `Status:` line is at `artifact-templates.md:298`. The `--compare` comma form is at `adversarial.md:39`. merge-log.md is written to `<output-dir>/adversarial/` (`sc-adversarial-protocol/SKILL.md:2072`).
- The executor rules: tasks run in order, a Constraints breach is blocking, the FINAL `issues` conditions (`qa.md:310`), the closed list of interrupts (`qa.md:276-288`), and managed staging (`managed-workspace.md:36`).
- Not checked: Orca's live `--help` output (running Orca was out of scope), so F-005 and F-006 are partly inferred.

## Self-assessment

| Dimension | Score | Basis |
|---|---|---|
| Citation grounding | 0.90 | Every finding cites file:line with a quote. F-006, F-012 and F-013 rest partly on inference and are tagged [INFERRED]. |
| Coverage completeness | 0.75 | coverage_pct_union 0.75 by the mechanical rule. All six unmapped rows are covered in substance, but the rubric scores the measured value. |
| Deviation-classification clarity | 0.85 | Each finding has one severity tied to a named executor rule. F-002 and F-017 depend on how the FINAL reviewer reads a recorded FAIL. |
| Risk surface coverage | 0.85 | Covers halt paths, archive blocking, Constraint breaches, false FAILs and resume. Live Orca behaviour (setup, transcript shape) can only be checked by running it. |
| Recommendation actionability | 0.90 | Every fix names the plan line, file or command to change and its success check. |
| **Mean (C)** | **0.85** | |
