# Worker final report: issue #331 (GitHub issue watcher)

Worker: term_8b57635d-61f8-4b87-9b31-0d29c9351282, task task_0b795fb7069a, dispatch ctx_58a8c8b54cbd.

## Outcome

- PR #447 (delivery): https://github.com/IronbellyOrg/IronClaude/pull/447 was merged by `ironbelly` at 06:27:42Z, before its review findings were fixed. Not merged by this worker.
- PR #448 (follow-up, owner-requested, Refs #331): https://github.com/IronbellyOrg/IronClaude/pull/448. Final monitor status: both reviewers clean on head 193c3d98 after one fix round, CI all green, PR open, ready (not draft), mergeable, NOT merged.
- Comment linking the follow-up was added to merged PR #447.

## Chain artifacts

- Claim comments: https://github.com/IronbellyOrg/IronClaude/issues/331#issuecomment-6703550680 (accuracy check, verdict out_of_date) and https://github.com/IronbellyOrg/IronClaude/issues/331#issuecomment-6703550840 (claim; ClickUp skipped, no token).
- Brainstorm: `.dev/brainstorms/20261107-064825-github-issue-watcher/` (`merged-requirements.md`, `spec-final.md`).
- Spec-panel: ran; result in `.dev/brainstorms/20261107-064825-github-issue-watcher/spec-panel-review.md` and `spec-refactor-log.md`.
- Design: `docs/designs/issue-watcher.md`; owner runbook `docs/designs/issue-watcher-setup.md`.
- Task file: `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md` (status Done).

## Files changed

- PR #447: nine modules under `src/superclaude/cli/issue_watch/`, two registration lines in `src/superclaude/cli/main.py`, `tests/issue_watch/` (19 test files, 19 fixtures), the two docs above.
- PR #448: `src/superclaude/cli/issue_watch/cycle.py`, `src/superclaude/cli/issue_watch/launch.py`, `tests/issue_watch/test_cycle.py`, `tests/issue_watch/test_launch.py`, and `.dev/tasks` records (fix record `phase-outputs/reports/pr447-followup-fix-record.md`, task log entry).

## PR #448 scope and review

- F1 (Augment, high): `validate_approvers` opened the approvers file by path after `lstat`; now opens first and checks type, owner, mode and (st_dev, st_ino) on the open descriptor.
- F3 (Codex, medium): second Orca probe reused the first probe's timeout; `find_orca` now takes a callable asked before each probe, and the cycle re-reads the remaining deadline.
- G1 (Augment round 1, medium): a FIFO swapped in after `lstat` could hang the open; fixed with `O_NONBLOCK` (commit 193c3d98), failing-first test added, thread replied and resolved.
- Round 2 re-review: Augment clean, Codex clean (both on 193c3d98). CI: all five checks passed.
- Not fixed on purpose (owner scope): F2, Augment, low: stale status line at the top of `docs/designs/issue-watcher.md`.

## Test results (final state of #448 branch)

- `tests/issue_watch`: 2655 passed (also under xdist). Wider affected set: 2685 passed, 1 pre-existing skip (`tests/swarm/test_cli_registration.py:127`, untouched).
- `make lint` exit 0; pinned ruff 0.15.20 check and format clean; `make verify-sync` in sync; detect-secrets hook exit 0.
- Failing-first: the new F1 and F3 tests were run against the unfixed source in a temporary copy; 10 fail there and pass with the fixes; the FIFO test also fails on the previous commit.

## Deviations and exceptions

- Review-cycle exceptions: 3 (research Gate 3, research Gate 5, task-builder research gate each closed with edits applied but not re-reviewed; coordinator-approved).
- POST reflect returned FAIL / needs_human_decision with one low regression R-1 (launch could start up to one local save after the 120 s cut-off). R-1 was fixed as a second commit (new test fails pre-fix) and is NOT re-verified by a reflect. R-2 to R-7 and D-2 to D-4 accepted as notes. R-2/R-3: new reasons `cycle_complete` (exit 0) and `cycle_crashed` (exit 1), owner-accepted; reason-table count is 59 in code against 57 in design and spec (to fix at design).
- PRE reflect: fail / not signed off (PRE-1 to PRE-13), recorded in the task file.
- Troubleshoot dispatch skipped for F1, F3 and G1 by coordinator decision (verified findings, small fixes with in-repo precedent, failing-first tests, independent re-review on the new head). Disclosed in the PR body.
- Pointer prompts used for sub-agents; one Gate C report was overwritten by a mis-targeted agent and restored (logged).
- Stray untracked files left unstaged on purpose: `.dev/brainstorms/20261107-064825-github-issue-watcher/`, `.dev/issues/331/`, `docs/memory/reflect/deviation-patterns-issue-331-github-issue-watcher.md`.

## Not verified / skipped

- Full test suite runs in CI only; CI on #448 passed. A reviewer's earlier local full run had 4 failures outside issue_watch (missing ruff module in the tool environment, shared /tmp collision, xdist thread-id check).
- gh and Orca reply shapes are assumed (fixtures under `tests/issue_watch/fixtures/_assumed_shape/`); Orca behaviours are owner checks in the runbook. Nothing deployed, scheduled or run live.
- Five of the new per-probe tests also pass on the old code (not failing-first). F1 race is simulated by renaming inside a wrapped `os.open`; no foreign-owner test (needs root).
- Impact-analysis wave recorded as partial (graph absent). Spec-fidelity agent verified 13 of 43 FR/NFR ids by reading code; the rest rest on test names and the AC trace. Design 166 / spec 197 `failed` entry followed by rate-limit or timeout is unreachable (owner may confirm).

## Owner note

The poller is registered as `superclaude issue-watch` but is not scheduled and ships with `enabled: false`. It must not be enabled before the F1 fix in PR #448 is merged.
