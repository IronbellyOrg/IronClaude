# Issue 691 Part B: plan result (planner agent, 2026-11-20)

## Where the plan is

- Package: /home/coder/workspaces/worktrees/IronClaude/issue-691-part-b/.dev/tasks/to-do/TASK-WF-planIssue691Part-20261120-204103/
- Main file: /home/coder/workspaces/worktrees/IronClaude/issue-691-part-b/.dev/tasks/to-do/TASK-WF-planIssue691Part-20261120-204103/TASK-WF-planIssue691Part-20261120-204103.md
- Also in the package: source.md (the brief), return-contract.yaml (status success), artifacts/codegraph-grounding.md
- Advisory review (reflect, Tier 1, status partial, no blocking finding): /home/coder/workspaces/worktrees/IronClaude/issue-691-part-b/.dev/reflect/pre-planIssue691Part-20261120204445/REPORT.md (untracked, outside .dev/tasks)
- Stage state: `git add .dev/tasks` done; nothing committed, nothing pushed, no GitHub write.

## Command to run it

From the worktree /home/coder/workspaces/worktrees/IronClaude/issue-691-part-b:

`/sc:implement .dev/tasks/to-do/TASK-WF-planIssue691Part-20261120-204103/TASK-WF-planIssue691Part-20261120-204103.md`

No flags are named by the protocol. The pull request is opened afterwards with `/sc:pr-submit --monitor 3`, not by the implementer's own gh calls.

## Ten-line summary

- Seven tasks in four phases; the diff touches four files: session-gov.sh, session-gov-selftest.sh, runbook-selftest.sh, observation-runbook.md (plus the package).
- The claim result is read from `$MAIN/.dev/issues/<n>/launch-result.json` (main checkout; the worktree copy skips the file, orca_worktree.py:477).
- Claim start = `date +%s` taken just before the claim is typed. Fresh = file mtime >= start and, when `launched_at` is a string, its epoch >= start. No skew allowance.
- Missing or stale file: `PENDING reason=claim-result-missing|stale` (exit 0, existing pending pattern; an already_launched claim lands here). Not an object / no string status / symlink: `FAIL claim-result` (exit 1).
- JSON only through `jq` (no eval); terminal handle checked against `^[0-9A-Za-z_-]+$` before `driver.sh adopt`.
- `claim_send`, `claim_has` replaced by a file reader; `launch_real` takes `terminal` and `layers` from the file; the whole `orca terminal list` lookup is deleted; `release_session` and `inode_record` read `.release` (placeholder is `<session id>` with a space) from a saved copy `$OB/claim-T<n>.json`.
- Found a latent order bug: `run_c` sets MAIN after `launch_real`; the plan moves it up.
- Runbook: lines 534, 546, 560, 566, 580, 635, 767, 769, 856 and appendix item 18 reworded line-neutrally (selftests pin lines 228, 505, 520, 536, 698 and read 536-697); script citations are re-pointed; section 6 gains rows.
- Selftests: stub orca writes the fixture file when the claim is typed and shows a deliberately wrong screen; new cases fresh, screen-ignored, missing, stale (mtime and launched_at), unreadable (3 forms + symlink), failed, already_launched (earlier file byte- and mtime-identical), terminal null, layers missing, resume with a text-only copy; plus a negative check against the master script.
- Done when: `bash .dev/issues/442/scripts/selftest.sh` ends with `SELFTEST_OK` (baseline on master today: SELFTEST_OK, exit 0), `bash -n`, `make sync-dev`, `make verify-sync`, `make lint` exit 0, diff limited to the four files.

## Owner-gated steps (the implementer must NOT run them; the coordinator asks the owner in chat after merge)

- Step 1: `superclaude install` (puts the Part A file writer into ~/.claude, which a live claim runs). Yes: installed. No: the live rerun cannot happen. Note the coordinator's separate duty to undo the earlier hand install (memory note uninstall-issue-691-install-after-restart).
- Step 2: live OB-H2 rerun on the disposable issues T1 to T4 only, to confirm a real claim leaves launch-result.json in the main checkout and the scripts pass reading it. Yes: Part B's live half is checked, then a follow-up edit may flip the runbook's UNVERIFIED sentence. No: Part B stays open.

## Open questions (none blocks starting)

- Keep the claim terminal's screen for liveness and dialog checks only (planned) or drop even that? Planned: keep, it is not result parsing.
- Keep the one-line `die resume` guard for a leftover text-only claim copy (Task 2)? It protects a live /tmp/ob that an earlier run filled; the owner may drop it.
- Add a fresh string `launched_at` fixture to Task 4 (reflect finding F-2, Medium). Not applied because reflect findings never edit the plan; the implementer may add it.

## Could not verify (UNVERIFIED)

- That a live claim passes a `--source` that resolves to the main checkout and leaves the file there (the owner-gated rerun decides).
- `shellcheck`: no binary in this workspace, and pre-commit is not installed; the repo's pre-commit config runs shellcheck --severity=warning in CI only.
- Whether `date -u -d` parses the real `launched_at` string on the target host (GNU date assumed; no fresh-launched_at fixture yet, see F-2).
- Run time of selftest.sh as a whole (it finished inside one 10-minute tool call here, exact time not recorded).
- The reflect pass ran Tier 1 with inline calibration and no evidence-validator agent; its zero-drop result is weak evidence.
