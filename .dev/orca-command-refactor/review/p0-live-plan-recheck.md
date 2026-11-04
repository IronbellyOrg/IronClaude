# P0 live plan version 2: independent recheck

Date: 2026-11-04

Verdict: FAIL

Counts: D-001 to D-013 fixed 13 of 13. New findings: 3 blocking (N-01 to N-03), 6 minor (N-04 to N-09). Format gate: pass.

Plan: `.dev/tasks/to-do/TASK-WF-writeTheP0LivePl-20261103-215902/TASK-WF-writeTheP0LivePl-20261103-215902.md` (version 2, 152 lines). "plan:N" below means a line of that file. Every Orca claim was checked against `.dev/orca-command-refactor/review/p0-live-orca-help.txt` ("help:N"). `orca status --help`, `orca repo list --help` and `orca orchestration reply --help` were also run for this recheck. No other orca command was run.

The three blocking findings share one root cause. The Constraints say a failed live step is a recorded result, not a task failure (plan:25-26). But three groups of acceptance criteria still require the good outcome itself, or require evidence that the plan's own failure branches never produce. Each is a one-line wording fix, and it must be made before the first `T<id>: start` line (E-PLAN-CHANGED).

## D-001 to D-013

| ID | Fixed | Plan lines | Note |
|---|---|---|---|
| D-001 | yes | 24, 145, 148, 150 | Every `git add .dev/tasks` is followed by `git restore --staged -- <superseded package>`, and the executor's re-add after the archive move is named, citing managed-workspace.md:36. `staged.txt` is now titled the pre-archive snapshot. The phase report ends with the post-archive check. The rule is honoured only by the executor after FINAL, so the coordinator's post-archive check is the only safeguard. That matches what the fix asked for. |
| D-002 | yes, but see N-01 | 24, 51, 58 | The baseline is saved first, the AC compares against it, and `.dev/reflect/` is on the leave-untouched list. The new AC's last clause ("shows no modified tracked file") copies the reflect fix text, and it is false on a correct run (N-01). |
| D-003 | yes | 31, 35, 36, 43 | `<run_id>` = `result.run.id` of live-run.json. `--run` is passed on task-create, worker-start, check and worker-list. help:142, 164, 215 and 320 list `--run`. |
| D-004 | yes | 35, 37, 38 | Failed start: release by dispatch, then Step 7 and Remove. Stall proof: worker-stop, then task-update `--status failed --result cancelled` (help:365, 382-383). An unanswered wait or decision question gets a 60-minute cap, after which the worker is left for the person, with no prompt and no forced stop. This is consistent with orca-capabilities.md:111 and the no-prompt rule (qa.md:288). The edge gaps are in N-08. |
| D-005 | yes | 26 | Names the expected result of symptom-check.txt, says FAIL values in lc files are recorded results, says which files carry verdicts, and requires the recording-status last line and the evidence= citation rule. Residual risk: the qa.md:310 test ("a log cited ... shows a failure at its outcome line") is literal. Task 1 should therefore cite preflight.md or the AC line, not the raw pytest tail, on `evidence=`. |
| D-006 | yes | 44, 86, 112, 137, 151 | Saves lc<N>-worktree-list-after.json, lc<N>-head-after.txt and head-final.txt, and each AC cites its file. |
| D-007 | yes | 27 | A fix pass, a retry attempt (A2-A5) or a resume only rebuilds artifacts from saved evidence, including `retries/T<id>/artifacts-<k>/`, and never creates a worktree, Task or worker. A3-A5 revert to the Q0 snapshot, but the package is excluded from the revert domain (retry.md:202), so saved evidence survives. |
| D-008 | yes | 27 | Checks the worktree list and the worker list before the Worktree step, reuses what exists, and continues from the first step with no saved evidence. |
| D-009 | yes, with a wording gap (N-04) | 28, 51, 55 | Pre-run check file and help capture exist. Every procedure flag and selector appears in the help text: `--repo id:` help:15; `--base-branch` help:26; `--no-parent` help:37; `rm --worktree path: --force` help:76, 85-86; `--objective` help:121; `--spec --task-title --run` help:142; `--task --worktree --agent --run` help:164, 179; `check --run --ack --types --wait --timeout-ms` help:215; `worker-show --dispatch` help:255; `worker-read --source --cursor` help:274; `worker-release` help:297; `worker-list --run --terminal-state reclaimable` help:320; `worker-stop` help:345; `task-update --id --status --result --run` help:365; `observation.agentWait` help:268. The `--base-branch refs/heads/...` resolution claim (flag-check lines 34-40) matches the local refs: `git rev-parse` of HEAD and of `refs/heads/ironbelly/OrcaCLICommandRefactor-Specs` both print `8db29f11...` today. |
| D-010 | yes | 33, 44 | The branch name comes from `git -C <path> branch --show-current`, and after Remove the plan checks `git branch --list "<that name>"`. This matches the `worktree rm` Notes (help:94). |
| D-011 | yes | 22, 41, 94, 145 | Adds `index-after.txt`, records the worker's staging as the known WC-9 gap, and reworded line 22 to "The executor's own git-state changes". |
| D-012 | yes | 29 | Bash timeout of at least 300000 ms per wait; a tool timeout is re-issued and is not a check failure. |
| D-013 | yes | 94, 110 | The Evidence copy also copies the `<id>.md` plan file. |

D-014 (base ref) is settled. Plan:31 and plan:33 use `refs/heads/ironbelly/OrcaCLICommandRefactor-Specs` and keep the HEAD check (`8db29f11`) as the run-time proof.

## New findings

### N-01: blocking. Task 1's last AC is false on a correct run

- Claim: the AC requires `status-end-t1.txt` to show "no modified tracked file". The working tree already has a modified tracked file outside the package, and this plan never touches it. A correct run's `status-end-t1.txt` therefore shows it, the AC is unmet, and no fix pass can make it true without writing outside the package (plan:21). Task 1 goes to the retry ladder and halts with E-HALT-QA. Every later task depends on Task 1.
- Evidence: plan:58, "lists no path that is not in `./artifacts/status-baseline.txt` or under this package, and shows no modified tracked file." `git status --porcelain` run for this recheck (2026-11-04) prints ` M docs/memory/reflect/deviation-patterns-OrcaCLICommandRefactor-Specs.md`, plus `AM` for this package's plan and return-contract. The clause came from the D-002 fix text (merged-verdict.yaml:23, "and no tracked file is modified").
- Fix: change the clause to "and shows no tracked file modified that is not already modified in `./artifacts/status-baseline.txt`, apart from this package's own files".

### N-02: blocking. Task 3 and 4 ACs require the worker to behave, not the result to be recorded

- Claim: Task 3 requires `lc2-step6.md` to show that README.md was not modified, and Task 4 requires `lc3-step6.md` to show that the inputs were not modified. If the worker does modify them, a faithful Step 6 records a FAIL. Plan:25-26 call that a recorded result and say the task stays compliant, but these ACs would then be unmet, so QA fails, the ladder cannot repair it (plan:25 forbids a re-run), and the run halts. The same applies to the end-state ACs: if `orca worktree rm` fails and the failure is faithfully recorded, the worktree is still listed, and the only allowed alternative is "left for the person under the Step 3 exit rule".
- Evidence: plan:111, "`lc2-step6.md` shows `README.md` was not modified in the disposable worktree". Plan:136, "`lc3-step6.md` shows the two input files were not modified in the disposable worktree". Plan:86, 112 and 137, "does not list the `p0-live-<name>` worktree ... or `lc<N>-result.md` records the worker and worktree as left for the person under the Step 3 exit rule". Against this, plan:26 says "A FAIL inside an `lc<N>-*` step file ... is a recorded result, not a task failure".
- Fix: reword these ACs to "states whether README.md (or the two inputs) was modified, with the status line as evidence". Change the end-state alternative to "or `lc<N>-result.md` records why the worktree remains (Step 3 exit rule, or a recorded Remove FAIL)".

### N-03: blocking. AC-0.5 and AC-0.6 cannot be met on the plan's own failure branches

- Claim: if the setup fails, the plan skips to Remove and no worker is started (plan:33). If worker-start fails, no transcript exists and Step 5 is never run (plan:35). In both cases there is no elapsed time and no transcript, yet Task 2's ACs require measured seconds, a yes/no answer with a quoted transcript excerpt, and a Step 5 source line. The task fails QA even though it recorded the failure faithfully. Also, plan:79 requires the excerpt to show "at least one named call", which cannot exist when the honest answer is "no".
- Evidence: plan:79, "write `./artifacts/ac-0.6.md` stating yes or no ... with a quoted excerpt showing at least one named call such as `Bash` or `Skill`". Plan:84, "`./artifacts/ac-0.5.md` states the measured seconds and PASS or FAIL". Plan:85, "`./artifacts/ac-0.6.md` states yes or no with a quoted transcript excerpt, and `./artifacts/lc1-step5.md` names the source". Plan:33, "Any failure here fails step 1: record it, skip to Remove, and do not dispatch".
- Fix: let ac-0.5.md and ac-0.6.md record FAIL or "not measured / not answerable: <reason>" when no worker started or no transcript exists. Let ac-0.6.md quote the excerpt that supports either answer. Optionally answer AC-0.6 from the first later check that has a transcript, with the phase report naming which one.

### N-04: minor. The claim "every verb checked" leaves out three verbs

- Claim: Task 1 calls `orca status --json` and `orca repo list --json`, and Step 3's factual answers need `orca orchestration reply`. None of the three is in the flag-check table or in Task 1's orca-help.txt list, and `reply` is never named in the plan. All three exist with the needed flags, so nothing fails at run time.
- Evidence: plan:28, "every verb and flag in this plan was checked against Orca 1.4.237's `--help`". plan:51, the verb list for orca-help.txt. `p0-live-orca-flag-check.md`:9-23 has no `status`, `repo list` or `reply` rows. Live `--help`: `orca status [--json]`, `orca repo list [--json]`, `orca orchestration reply --id <msg_id> --body <text> [--run <run_id>] ... [--json]`.
- Fix: add `status`, `repo list` and `orchestration reply` to the Task 1 help list, and name `reply --id <message_id> --body <text> --run <run_id> --json` in Step 3.

### N-05: minor. Inbox handling acks only worker_done and does not match messages to their worker

- Claim: the procedure acks only the worker_done delivery. A `question` or `escalation` delivery that was handled but not acked may be replayed to every later `check --wait`. Under exit (b), lc1's worker keeps running into Tasks 3-4 on the same run. Its late `worker_done` or question can then arrive in lc2's or lc3's wait, and Step 3 ("exactly one `worker_done`") does not say to match messages by dispatch or task id.
- Evidence: help:249, "A bound Run replays the same Delivery until --ack or all its messages are marked read, even with --types; process every message before acknowledging". plan:37, "Save the `worker_done` message ..., then acknowledge its delivery". plan:38, "leave the worker and its worktree running ... and move to the next task".
- Fix: ack every delivery after processing it, and count or answer only messages whose dispatch id or task id belongs to this check. Whether a `reply` marks a question read is not known, so this is minor, not blocking.

### N-06: minor. The main Step 3 wait has no overall cap

- Claim: "a growing transcript means keep waiting" is unbounded. The 60-minute cap applies only after a non-null agentWait or an unanswered decision question.
- Evidence: plan:37, "a growing transcript means keep waiting". plan:38, "if 60 minutes pass after that sample". The spec has the same rule (spec:285).
- Fix (optional): add an overall cap, for example 120 minutes per check, after which the worker is recorded and left for the person as under exit (b).

### N-07: minor. "Only these files carry verdicts" conflicts with step files that hold verdicts

- Evidence: plan:26, "Only `lc<N>-result.md`, `ac-0.5.md`, `ac-0.6.md` and `p0-phase-report.md` carry verdicts". But plan:40 asks `lc<N>-step5.md` for "one verdict and a quoted excerpt for each condition", and plan:54 asks preflight.md for checks that each "passes".
- Fix: say "carry check verdicts that FINAL reads as outcomes", or call the step-5 entries "findings".

### N-08: minor. The failure branches use values that may not exist

- Evidence: plan:35, "release whatever the receipt says it still owns ... when it names a dispatch, then go to Step 7", where Step 7 (plan:43) needs `<dispatch_id>`. plan:33, "skip to Remove", where Remove (plan:44) needs `<path>` and `lc<N>-branch.txt`, and neither exists if `worktree create` itself failed.
- Fix: say "Step 7 and Remove run only for what exists; otherwise record them as not run, with the reason".

### N-09: minor. The executor's own test extras are bound by Constraint 23

- Evidence: plan:23, "Test runs set `PYTHONDONTWRITEBYTECODE=1` and pass `-p no:cacheprovider`". SKILL.md:132 Q6 runs lint and tests when they are present. A plain `uv run pytest` extras run would be a quotable breach that FINAL can read.
- Fix: none needed in the plan. The executor must apply Constraint 23 to its Q6 extras, or skip them, because the tasks touch only `./artifacts/`.

## Format gate

Pass.
- No checkbox or numbered lines anywhere, fenced code included (`grep -nE '^\s*([-*] \[[ xX]\]|[0-9]+[.)] )'` found nothing).
- `## Task 1` to `## Task 5` are contiguous (plan:49, 62, 90, 116, 141). Each Phase heading has one Task before the next Phase. `Depends on:` names only lower tasks (plan:64, 92, 118, 143).
- Five `Acceptance criteria:` blocks, each with at least one bullet.
- Front matter has `schema: workflow-plan/1.2`, and the slug equals the folder and file name. The sibling `return-contract.yaml` has `contract_version: "1.1"`, the same slug and `status: success`, and `source.md` exists. Managed detection (managed-workspace.md:7-12) passes.

## Self-Audit

Checked:
- The plan text, the driving request (source.md) and the merged verdict (D-001 to D-023).
- The flag-check file and all 14 verbs in the help capture. `status`, `repo list` and `reply` were checked live with `--help`.
- Executor rules: managed-workspace.md (staging at :36, PLAN pin at :43, FINAL at :49-61), retry.md (ladder, and the revert domain that excludes the package), and qa.md (the Halt table, the closed interrupt list at :276-288, and the managed FINAL at :310). SKILL.md: Q0-Q8, task enumeration, AC QUALIFY and Q6 extras.
- Spec 7.2 (:281-293) and the 7.3 P0 rows (:298-305), and WORKER-CONTRACT.md: the brief guard (:16-20); no command has an `## Unattended mode` section in src or in `~/.claude`, so the P0 briefs pass the guard. Also WC-5 at P0 (:57) and WC-9 staging (:42).
- Command flags: troubleshoot `--type test` and `--output-dir` (troubleshoot.md:8, 50, 56); adversarial `--compare` with comma-separated paths, `--depth quick` and `--output` (adversarial.md:39, 66, 69).
- Report-file sources: troubleshoot report-template.md `**Status**:`, adversarial artifact-templates.md `## Metadata` / `Status:`, and workflow return-contract.md.
- Inputs: option-a.md and option-b.md at commit 8db29f11 have 23 and 25 lines. The three accepted failing tests are in t1-accepted-failures.md:24-26.
- Live facts: `cmp ~/.claude/WORKER-CONTRACT.md src/superclaude/core/WORKER-CONTRACT.md` exits 0, HEAD and the branch ref are `8db29f11`, and current git status was read.

Not checked: Orca's runtime behaviour (ack/replay, receipt field shapes beyond the flag check's quoted receipt, liveness), because only `--help` was allowed. No tests, worktrees, runs or workers were created, and no git state was changed. The only file written is this report.

## Recheck after fix pass 1 (2026-11-04)

Verdict: FAIL

Counts: N-01, N-02 and N-03 are fixed. 1 new blocking finding (R-01), which the N-02 rewording introduced. 0 new minor findings. Format gate: still pass. The minor findings N-04 to N-09 were not rechecked, as instructed.

The plan now has 151 lines. "plan:N" refers to the current file. The Constraints (plan:17-45) were re-read and still match version 2. `git diff` against the staged copy shows edits only in the Task bodies and the acceptance criteria.

| ID | Fixed | Plan lines | Note |
|---|---|---|---|
| N-01 | yes | 58 | The AC now reads "shows no tracked file modified that is not already modified in `./artifacts/status-baseline.txt`, apart from this package's own files". The existing ` M docs/memory/reflect/deviation-patterns-OrcaCLICommandRefactor-Specs.md` is in the baseline, so a correct run meets the AC. |
| N-02 | yes for the Step 6 ACs; the end-state ACs were reworded but see R-01 | 111, 136; 86, 112, 137 | plan:111 and plan:136 now say "states whether ... was modified ..., with the status line(s) as evidence", which a faithful FAIL record can meet. The end-state ACs now allow "a recorded Remove FAIL", but the reordering created R-01. |
| N-03 | yes | 79, 84, 85 | ac-0.5.md may record `not measured: <reason>` and ac-0.6.md may record `not answerable: <reason>`. The excerpt now only has to "support the answer", with the named-call requirement limited to "yes". The step-5 AC accepts "`lc1-result.md` records Step 5 as not run". The fallback for Tasks 3-4 ("uses the transcript source unless `ac-0.6.md` says no") matches Step 5's rule at plan:40. |

### R-01: blocking. The end-state ACs now require lc<N>-head-after.txt even when Remove did not run

- Claim: the edit reordered the end-state ACs so that the head-after clause comes first and stands alone. The "or" alternative now attaches only to the worktree-list clause ("why it remains", where "it" is the worktree). The head-after file is written only by the Remove step. Under the Step 3 exit rule (b), Remove is recorded as not run, so `lc<N>-head-after.txt` never exists. On that plan-designed path the AC is unmet and cannot be repaired without a forbidden re-run, so the task halts. Version 2 did not have this defect: its semicolon form ("does not list ..., and ... head-after ... shows ...; or `lc<N>-result.md` records the worker and worktree as left for the person") let the alternative cover both clauses.
- Evidence: plan:86, "`./artifacts/lc1-head-after.txt` shows `8db29f1165508187b7a14a48f2f66793e269d596`, and `./artifacts/lc1-worktree-list-after.json` does not list the `p0-live-troubleshoot` worktree, or `lc1-result.md` records why it remains (the Step 3 exit rule, or a recorded Remove FAIL)". plan:112 and plan:137 say the same for lc2 and lc3. plan:38, "record Step 7 and Remove as not run because the worker is not settled, and move to the next task". plan:44, where Remove is the only step that saves "the feature worktree's `git rev-parse HEAD` to `./artifacts/lc<N>-head-after.txt`".
- Fix (any one of these, in the three ACs):
  - Make the alternative cover both clauses: "Either `lc<N>-head-after.txt` shows `8db29f11...` and `lc<N>-worktree-list-after.json` does not list the `p0-live-<name>` worktree, or `lc<N>-result.md` records why the worktree remains (the Step 3 exit rule, or a recorded Remove FAIL)".
  - Or make the head-after clause conditional: "when Remove ran, `lc<N>-head-after.txt` shows ...".

### Self-Audit (fix pass 1)

Checked:
- Re-read plan:17-151.
- Compared each edited AC with its Fix line and with the Constraints it must agree with (plan:25-26 recorded-result rule; plan:33, 35 and 38 failure branches; plan:40 Step 5 source rule; plan:44, the Remove outputs).
- Checked that every failure branch (setup failure, worker-start failure, stall proof (a), exit (b), Remove FAIL) has an AC wording that a faithful record can meet. Only exit (b) against the head-after clause fails, which is R-01.
- Format gate re-run: no checkbox or numbered lines, 5 `Acceptance criteria:` blocks, Tasks 1-5 contiguous, and `Depends on:` lines unchanged.

The plan was not edited. No orca command was run in this recheck.

## Recheck after fix pass 2 (2026-11-04)

Verdict: PASS with notes

Counts: R-01 is fixed in all three places. No new blocking findings and no new minor findings. Format gate: still pass. The notes are the minor findings N-04 to N-09 from the first recheck, which are still open by the owner's choice and were not rechecked here.

| ID | Fixed | Plan lines | Note |
|---|---|---|---|
| R-01 | yes | 86, 112, 137 | Each criterion now reads "Either `./artifacts/lc<N>-head-after.txt` shows `8db29f1165508187b7a14a48f2f66793e269d596` and `./artifacts/lc<N>-worktree-list-after.json` does not list the `p0-live-<name>` worktree, or `lc<N>-result.md` records why the worktree remains (the Step 3 exit rule, or a recorded Remove FAIL)". "Either" makes the alternative cover both clauses. Under exit (b), where plan:38 records Remove as not run and no head-after file exists, the second branch is met. When Remove runs (plan:44 writes both files), the first branch is met, or a recorded Remove FAIL meets the second. |

New findings: none.
- Each criterion is the same text with only `<N>` and the worktree name changed: lc1/troubleshoot, lc2/workflow, lc3/adversarial.
- Each still matches the files plan:44 writes and the exit paths at plan:33, 35 and 38.
- Earlier fixes are still present at plan:58 (N-01), plan:84-85 (N-03), and plan:111 and plan:136 (N-02).

### Self-Audit (fix pass 2)

Checked:
- The plan still has 151 lines.
- Every `head-after` mention (plan:44, 86, 112, 137) was read in full.
- The earlier fixed lines (58, 84-85, 111, 136) and the Step 3 exit rule (38) were spot-read.
- Format gate re-run: no checkbox or numbered lines, 5 `Acceptance criteria:` blocks, Tasks 1-5 contiguous (plan:49, 62, 90, 116, 141), `Depends on:` names only lower tasks (plan:64, 92, 118, 143).

The plan was not edited. No orca command was run.
