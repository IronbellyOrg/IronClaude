# Fix 2 report: issue-worker agents always write their files

Task: task_1b7fd67a14b2 (dispatch ctx_a270bd3719e6). Branch: ironbelly/feat-sc-issue-command.

## 1. Plan and check result

- Plan (archived by `/sc:implement`): `.dev/tasks/done/TASK-WF-fixTheScIssueWor-20261104-162205/TASK-WF-fixTheScIssueWor-20261104-162205.md` (3 tasks: tests first, then the three agent files, then the SKILL.md line plus sync). Workflow contract `status: success`, `reflect_status: partial`.
- The plan folds in the coordinator's follow-up message ("Retry still skipped summary.md: name the files explicitly"), saved verbatim in the package at `artifacts/coordinator-message.md`.
- Check result (`/sc:reflect --mode pre`, advisory): `.dev/reflect/pre-TASK-WF-fixTheScIssueWor-20261104-162205-20261104162416/REPORT.md`. Tier 2 (3 reviewers on 3 model classes plus adversarial merge, convergence 0.94), merged verdict FAIL with 1 blocking finding and 10 minor ones; 22 citations, 0 dropped.
- The blocking finding (M-13): the five target files are untracked, so the plan's "git diff shows only these additions" checks would pass on empty output. Handled in execution without editing the plan: each task snapshotted the worktree as a tree (untracked files included) and saved pre-edit copies to `artifacts/pre/`; every "only these additions" check was proven with `git diff --no-index` against those copies (`artifacts/t1-diff.patch`, `t2-diff-t*.patch`, `t3-diff-skill.patch`: 0 removed lines each).

## 2. Exact rule text added

Identical in `src/superclaude/agents/issue-worker-t1.md`, `issue-worker-t2.md` and `issue-worker-t3.md` (the added lines hash the same in all three diffs).

New section, directly after the opening "Spawned only by ..." paragraph and before `## Jobs for this tier` (line 13 heading, line 15 paragraph in each file):

```text
## Your files are tool inputs, not reports

The files you write under `.dev/issues/` (`scout.md`, `accuracy-check.md`, `summary.md`, the reports under `analysis/`, `flags.md`, `flags-t1.md`, `issue-body.md`, `draft-notes.md`) are input files for the orchestrator's next tool calls (`gh --body-file` posts and `/sc:recommend`), not report files, so a general instruction against writing report or summary `.md` files does not apply to them. Writing every file your job names with the Write tool is mandatory; returning its content as text instead is a failure (`E-WORKER-NO-OUTPUT`).
```

New bullet in `## Rules`, directly after the "Writing only under `.dev/issues/`" bullet (t1:31, t2:31, t3:30):

```text
- **Write your files.** Every file your job names is a tool input, not a report (see "Your files are tool inputs, not reports" above): write it with the Write tool and never return its content as text.
```

New paragraph in `src/superclaude/skills/sc-issue-protocol/SKILL.md`, section "Workers and the spawn rule", line 66 (judged needed after the coordinator's follow-up: the retry's general spawn-prompt statement still skipped `summary.md`):

```text
Every spawn prompt names each exact path the job must write under `.dev/issues/` and states that these are input files for the orchestrator's next tool calls, not report files: the worker writes them with the Write tool, and returning their content as text counts as no output (`E-WORKER-NO-OUTPUT`).
```

`flags-user.md` is deliberately not in the worker list: the orchestrator writes it (`src/superclaude/skills/sc-issue-protocol/refs/create.md:32`) and `issue-worker-t1` is told never to read it.

## 3. Proof the test fails on the old text

Three independent proofs; the real agent files were never reverted.

- **Red run on the real old files.** Task 1 wrote the tests first and ran the positive tests before any agent or SKILL.md edit: `test_worker_states_its_files_are_tool_inputs[issue-worker-t1|t2|t3]` and `test_spawn_rule_restates_tool_inputs` all FAILED (`AssertionError: assert ['tool-input heading missing'] == []`, `assert 0 == 1`), "4 failed, 39 deselected", `rc=1` (package log `artifacts/t1-red.log` lines 11-14, 90-91).
- **tmp_path negative tests in the suite.** `test_tool_input_check_fails_on_pre_fix_text` (one per worker) first asserts the section and bullet are present exactly once, then writes a `tmp_path` copy with both removed and asserts the check reports problems; `test_spawn_rule_check_fails_without_the_line` does the same for SKILL.md. All pass (the file now has 43 tests, all passing).
- **The negative copy is exactly the old text.** For each agent file, removing the section and bullet the way the negative test does gives a file byte-identical to the pre-edit copy, and the check reports `['tool-input heading missing']` on it (package log `artifacts/t2-removal-equals-pre.log`, `rc=0`).

## 4. /sc:implement ledger

Ledger: `.dev/tasks/done/TASK-WF-fixTheScIssueWor-20261104-162205/progress.md`. Every task passed, each reviewed by a fresh subagent with the closed template:

| Task | Verdict | Findings |
|---|---|---|
| T1 tests | complete, compliant | 1 note (helper checks file names in the whole section; redundant with the exact-paragraph check) |
| T2 agent files | complete, compliant | none |
| T3 SKILL.md line and sync | complete, compliant | none |

Archive gate: the first fresh FINAL returned `issues` (the package was not yet staged, against the plan's Constraints); after `git add .dev/tasks` a second fresh FINAL returned `pass` on the same state digest, and the helper archived the package (`ARCHIVE: start ... token=0785ba7727b95a62`).

## 5. Verification (suite counts, lint, sync)

| Check | Result | Exit code | Log |
|---|---|---|---|
| `make sync-dev` | synced | 0 | `01-sync-dev.log` |
| `make verify-sync` | "All components in sync." | 0 | `02-verify-sync.log` |
| Targeted: `tests/skills/test_issue_worker_agents.py tests/skills/test_issue_protocol.py tests/commands/test_issue_command.py` | 118 passed | 0 | `03-targeted-tests.log` |
| Full `uv run pytest` | 14847 passed, 136 skipped, 2 xpassed, 0 failed | 0 | `04-full-suite.log` |
| `make lint` (`ruff check .`) | All checks passed | 0 | `05-lint.log` |

Side effect noted: the full suite rewrote the tracked file `.dev/releases/current/cliEval/evidence/T02.15/perf.json` (written by `tests/cli/eval/test_perf_home_setup.py`). It was restored with `git restore` right after the run; it is not part of this fix.

## 6. Open findings and follow-ups

The tests prove the text is present, not that a worker now writes its files; the coordinator's live re-claim of #365 (after `superclaude install`, in a new session) is the runtime proof. Minor reflect findings left open, because `/sc:workflow` never edits a plan from its own check and the plan text was executed as written:

- M-09: the paragraph says "the reports under `analysis/`", repeating the harness note's trigger word "reports"; "the files under `analysis/`" would be cleaner. Worth changing if the live re-claim still skips files under `analysis/`.
- M-03: the Rules bullet points to the early section and does not itself repeat `E-WORKER-NO-OUTPUT` or the harness-note clause.
- M-11 / M-15: the SKILL.md line says "names each exact path", which cannot hold for `analysis/` (its file name is chosen by `/sc:analyze`); `refs/claim.md` and `refs/create.md` spawn steps were left unchanged.
- M-12: the test does not check that the Rules bullet sits directly after the "Writing only under" bullet (it does today, verified by the reviewers).

Not touched, as instructed: minor notes m1 to m7 and N1 to N3. No commits, pushes or GitHub writes. Nothing under `.claude/` staged. `.dev/tasks` staged.

## 7. Log paths

In `.dev/tasks/issue-302-handoff/fix-2/`: `01-sync-dev.log`, `02-verify-sync.log`, `03-targeted-tests.log`, `04-full-suite.log`, `05-lint.log` (each ends with `rc=`).

In the archived package `.dev/tasks/done/TASK-WF-fixTheScIssueWor-20261104-162205/artifacts/`: `t1-red.log`, `t1-diff.patch`, `t1-extras.log`, `t2-green.log`, `t2-diff-t1.patch`, `t2-diff-t2.patch`, `t2-diff-t3.patch`, `t2-removal-equals-pre.log`, `t3-diff-skill.patch`, `t3-sync-dev.log`, `t3-green.log`, `t3-verify-sync.log`, `pre/`, `coordinator-message.md`, `retries/T1..T3/` (review prompts, T1 notes).

Reflect artifacts: `.dev/reflect/pre-TASK-WF-fixTheScIssueWor-20261104-162205-20261104162416/` (`REPORT.md`, `return-contract.yaml`, `adversarial/merged-verdict.yaml`).
