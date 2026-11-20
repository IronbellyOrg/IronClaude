# Handoff: observation runbook for issue #442

- Task: task_b1ba9bf6b39b, dispatch ctx_fe443c642c7a, run run_93bfa00cae2b
- Worker terminal: term_f66a60bf-4e6a-4baf-8682-606b6c8c1e12
- Date: 2026-11-08
- Deliverable: `.dev/issues/442/observation-runbook.md` (untracked; nothing committed, pushed or posted)

## What was delivered

The runbook covers the 12 pending live observations: OB-H1 items 1 to 9, OB-H2, OB-H3 and OB-CTX. It has six sections.

1. Preconditions: an install check, a baseline of the real launch store, an isolated HOME for session A, and the disposable issues T1 to T4.
2. Every item, grouped into sessions A, A2, B, C, D and E. Each item gives its prompts, the evidence command, the PASS or FAIL rule, and the skipped test it replaces.
3. The order and the gate.
4. A results template (`.dev/issues/442/observation-results.md`) and what only a person can do.
5. Safety and cleanup.
6. Scripted path: the scripts and the order to run them in.

An appendix lists what was verified and what was not.

## Counts

- Verified: 25 commands or claims. 12 were run in a safe form, 5 were checked against `--help`, and 8 were checked by reading the source. The appendix of the runbook lists them all.
- Not verified: 14. Each is marked UNVERIFIED where it is used, with how to confirm it.
- Tests: `uv run pytest tests/hooks/test_launch_level_observations.py -q` gave 5 passed and 12 skipped (2026-11-08). The 12 skips are `test_pending_live_observation[<item>]` for the 12 items. The runbook names the skip each result replaces. No test file was changed.

## Findings while verifying

- **Launch store baseline**: `~/.claude/state/launch-level/` holds 1 session entry, 0 pending, and empty `jobs/` and `requests/`. Cleanup compares against this baseline.
- **Guard messages carry no code**: the guard prints a header, then `Blocked:`, `Why:` and `You can:` lines. The runbook maps each code to the start of its `Blocked:` text, from running the guard copy on synthetic payloads in a scratch HOME.
- **Preflight order** (`orca_worktree.py` lines 1212-1237): already-launched, then the stale prompt check, then `enforcement_preflight`, then the pending record is published. A refusal (bad JSON in the worktree `settings.local.json`, or `disableAllHooks`) therefore leaves no pending record. Session B step 1 checks both refusals.
- **`identify`**: on an ordinary shell it printed `{"status": "ordinary"}`.
- **`cd` does not persist** between governed Bash calls (the job-identity wrapper rewrites them), and a compound `cd ... && git push` is a PUSH-FORM block. So the protected-push test in session E points the worktree's own push URL (`git config --worktree remote.origin.pushurl`) at a local bare repository. This was verified in a scratch repository with git 2.47.3: the main checkout's push URL did not change. `gh pr merge` is never tested on the real PR. `git merge ob-442-no-such-ref` tests LL-MERGE instead.
- **Release text**: the person removes `sessions/<sid>` and `sessions/<sid>.ok` by hand. The session file is a hard link of the record (`refs/claim.md` line 119). The link count is not stated anywhere I found.

## Side effects of this worker

- `.venv/` in this worktree, created at 05:05:45 UTC when `uv run` first ran here. It is gitignored (`.gitignore` line 56).
- Scratch folders, which the person may remove (runbook section 5.2 step 8): `/tmp/ob-test.mSMoo6s9 /tmp/ob-nobind.KAee2L /tmp/ob-lvl.8OJgpT /tmp/ob-pf.N24iNc /tmp/ob-bl.uOMnH8 /tmp/ob-h2.2pa53gkJ /tmp/ob-wtc.CCf1E9vU /tmp/ob-b1.OzYPZX`.
- `/tmp/ob` does not exist yet. The person creates it in section 1.3.
- Nothing was written to the real `~/.claude`. No claim, session, issue, PR or comment was made.

## What I could not verify (open items)

1. Whether an Orca-launched agent loads the worktree's `.claude/settings.local.json`. This is the largest risk: if it does not, every probe-based field of OB-H2 and OB-H3 stays pending. The runbook checks it right after each launch.
2. Whether real payloads carry `tool_use_id` (filter F7) and `transcript_path` (U27, filter F6).
3. The order in which the probe and the guard run on the same event.
4. Whether Claude Code 2.1.319 accepts the `UserPromptExpansion`, `SubagentStop` and `Stop` registrations, and whether `--settings` hooks merge with the user hooks.
5. Whether the isolated HOME needs a fresh login.
6. Whether `/sc:pr-submit` syncs the branch after a web UI edit (O-10).
7. The expected `identify` result for a `setsid`-detached job. The design gives none, so the runbook asks for it to be recorded and reported if it reads as ordinary.
8. Whether `/clear` gives a new `session_id` and how the binding follows it (U18).
9. The session file's link count once the pending entry is gone.
10. Whether leftover `jobs/` or `requests/` entries can be removed by hand.
11. Whether `grep -E` matches the same way as Claude Code's matcher.

Not built, so the runbook cannot observe it: the L2 pre-push layer. The runbook records L2 as pending.

## What is left

A person runs the runbook at a real terminal, in order. They record results in `.dev/issues/442/observation-results.md`, then do the cleanup in section 5.2. No governed claim on a real issue may run until OB-H2 and OB-H3 both pass (runbook section 3).

The scripts are in `.dev/issues/442/scripts/`, and runbook section 6 lists them in run order. The live run on the four disposable issues T1 to T4 is Task 10 of the plan `.dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/TASK-WF-scriptThe442Obse-20261108-061618.md`.
