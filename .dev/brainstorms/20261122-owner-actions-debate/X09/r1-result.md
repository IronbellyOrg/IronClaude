# X09 rehearsal, phases R0 to R3: result

Run on 2026-11-22 from the sandbox worktree rehearsal-r1. Sandbox only. Stopped at the end of R3 as told. R4 was not started.

## Summary table

| Phase | Result |
|---|---|
| R0 read only | Done. All checks as planned. |
| R1 sandbox setup | Done. Label, Project, three issues, config, approvers file, check-config, init-state, lock test all passed. Restart test only half done (cannot restart the workspace). |
| R2 shadow start | Running. First two ticks verified. Ends about 2026-11-23T11:27Z. |
| R3 drills | Done. DISABLED gives `disabled`; removing it restores `cycle_complete`; `enabled: false` gives `not_enabled`. Kill file removed. |

## R0 (read only)

- Tests: `uv run pytest tests/issue_watch -q` on a scratch copy of origin/master (6b17a7449, made with `git archive` into /tmp/ic-master-scratch because the IronClaude checkout is on branch docs/409-orca-dashboard-designs, which has no `issue_watch` folder): 3010 passed in 19 s.
- `GOVERNED_LEVELS_ALLOWED = False` at `src/superclaude/cli/issue_watch/launch.py` line 48 on origin/master.
- Cron: the `crontab` command is not installed, no cron daemon process is running, no user systemd folder. No cron line exists.
- Sandbox: `gh repo view` says PRIVATE, default branch main.
- Organisation issue fields: Priority, two date fields, Effort, Complexity and `Approved` (single choice, one option: `Yes`). So the `Approved` field exists.
- Projects before R1: three, none for the sandbox (IronOrca Dev number 3, Ironclaude - Development number 2, Coder - Development number 1).
- Sandbox labels before R1: only the GitHub defaults. Only issue 1 existed (assigned to clayphi); it was not touched.

## R1 (sandbox only)

Created on GitHub (all in IronbellyOrg/orchestrator-sandbox or the org Project):
- Label `issue-watch:trigger` (colour 0E8A16, description as repo_init.py writes it).
- Project 4 "orchestrator-sandbox watcher rehearsal": https://github.com/orgs/IronbellyOrg/projects/4 (node id PVT_kwDODPJUp84Bsty_). Linked to the sandbox repo (confirmed by a GraphQL read of the repo's projects).
- Status field options set (GraphQL `updateProjectV2Field`): Backlog, Research, Spec, Plan, Debug, In review, Done. The watcher allows Research, Spec, Plan, Debug (`predicates.py` line 300).
- Issue 2 https://github.com/IronbellyOrg/orchestrator-sandbox/issues/2 "Test: add an is_even function to calc.py"
- Issue 3 https://github.com/IronbellyOrg/orchestrator-sandbox/issues/3 "Test: add a docstring to calc.py"
- Issue 4 https://github.com/IronbellyOrg/orchestrator-sandbox/issues/4 "Test: add a test for subtract"
- Each issue: assigned to ironbelly (the launch login, which the setup doc section 6 requires for the watcher to consider it), carries the trigger label, is in Project 4 with Status Research. Nobody set `Approved` on any of them.

Local files (modes checked with stat):
- `/home/coder/.config/superclaude/issue-watch.d/` mode 700
- `/home/coder/.config/superclaude/issue-watch.d/orchestrator-sandbox.json` mode 600. Keys: schema_version 1, `enabled` false, repo, project_id PVT_kwDODPJUp84Bsty_, owner_account_id 7361222 (ironbelly), `approval_excluded_ids` [7361222], worktree `/home/coder/workspaces/worktrees/orchestrator-sandbox/Coordinator`, approvers_file, state_dir.
- `/home/coder/.config/superclaude/issue-watch.d/orchestrator-sandbox-approvers.txt` mode 600. Holds one id: 193966884 (clayphi). Account ids are not secrets.
- State dir `/home/coder/.local/state/superclaude/issue-watch/orchestrator-sandbox` mode 700 (dispatch.json, lock, audit.jsonl created by the watcher).
- No `claim_by` key: it is not in master (git grep on origin/master finds nothing), so it was omitted as the brief said.

Commands and results (full output saved in `/home/coder/.aidev/logs/r1-outputs.txt`):
- `check-config --config <file>`: "configuration is valid", 1 approver, exit 0.
- `init-state --config <file>`: "state created", exit 0.
- Baseline `once --dry-run`: `cycle_complete`, exit 0. Decisions for issues 2, 3, 4: all `not_approved` (expected, nobody approved).
- Lock test (setup doc 8.2): with `flock` holding the state lock, `once --dry-run` printed `cycle: lock_held`, exit 75. After release it ran normally (`cycle_complete`, exit 0). Passed.
- Restart test (setup doc 8.3): the before-state was recorded (dispatch.json created_at 2026-11-22T11:25:37Z; folder and file listing in the saved output). The restart itself was NOT done: restarting the workspace would kill this session and the shadow loop. NOT DONE.
- Non-dry `once` with `enabled: false`: `cycle: not_enabled`, exit 0, no external call.

## R2 start (shadow)

- Script: `/home/coder/.local/state/superclaude/issue-watch/orchestrator-sandbox/shadow.sh` (mode 700). Every command in it carries `--dry-run`. It runs `run-all --dry-run` first, then 288 ticks of `once --dry-run` 300 s apart, then `run-all --dry-run` again, each under `flock -n -E 99` on `/home/coder/.aidev/orchestrator-sandbox-shadow.lock` in `env -i HOME=/home/coder PATH=/home/coder/.local/bin:/usr/local/bin:/usr/bin:/bin`.
- Started 2026-11-22T11:26:41Z with `setsid nohup`. PID 1919079 (saved in `/home/coder/.aidev/logs/r2-shadow.pid`; the first number printed by the shell, 1919076, was the short-lived `setsid` wrapper).
- Log: `/home/coder/.aidev/logs/orchestrator-sandbox-shadow.log` (stdout of the script: `orchestrator-sandbox-shadow.stdout` in the same folder). Expected end about 2026-11-23T11:27Z.
- Verified: start `run-all --dry-run` exit 0, listing would_generate for Coder, IronClaude, IronOrca, Ironbrain, Ironeye (generates nothing), skipped path_in_tmp for one temp repo, orchestrator-sandbox skipped `not_enabled`. Tick 1 (11:26:46Z) and tick 2 (11:31:50Z) both `cycle_complete`, exit 0.
- dispatch.json hash at start saved in `/home/coder/.aidev/logs/r2-dispatch-hash-start.txt` (3ff2e6c9...). It was unchanged after tick 4.
- No config exists for any repo other than the sandbox (issue-watch.d holds only the two sandbox files). The older default `~/.config/superclaude/issue-watch.json` (and its .bak) existed before this task and was not touched.

## R3 (timed off drills)

- 11:31:59Z created `DISABLED` in the sandbox state dir. Next shadow tick (tick 3, 11:36:50Z): `cycle: disabled`, exit 0, audit line reason `disabled`, 0 GitHub calls.
- 11:37:44Z removed `DISABLED` (confirmed gone by `ls`). Next tick (tick 4, 11:41:50Z): `cycle_complete`, exit 0. Normal restored.
- `enabled: false` gives `not_enabled` for a non-dry `once` (shown in R1, 11:26:12Z; audit line `"dry_run": false, "reason": "not_enabled"`). I did not force any other non-dry run. The doc says a dry run ignores `enabled`, and the shadow ticks confirm it (they ran fully with enabled false).

## What did not match the plan or the docs

1. `once` has no `--orca` option on master or on the installed build (`once --help` lists only `--dry-run` and `--config`). The brief's command line would fail with a usage error. I left `--orca` off the `once` ticks (a dry run never calls Orca) and used `--orca` only on `run-all --dry-run`, which does have it.
2. Setup doc section 8.3 asks for a workspace restart. Not possible without killing the session and loop; the before-state is recorded only.
3. The installed `superclaude` is the tool build of commit 2ea524514 (PR 707), master is now 6b17a7449. `git diff --stat` of `src/superclaude/cli/issue_watch` and `tests/issue_watch` between the two is empty, so the ticks use the same watcher code as master.
4. The IronClaude checkout at /home/coder/workspaces/IronClaude is on branch docs/409-orca-dashboard-designs and has no `issue_watch` folder, so the tests were run on a scratch export of origin/master (see R0). The checkout has staged files from other work; I did not touch them.
5. `gh label create` printed nothing but the label exists (confirmed with `gh label list`). `gh project link` also printed nothing; link confirmed by GraphQL.
6. I did not create a `Pipeline` project field. The watcher reads it, but a missing field reads as no value (None), which is the only level allowed now. Add it only if R4 needs it.
7. The Coordinator worktree already existed (branch ironbelly/Coordinator, origin = the sandbox repo), so nothing was skipped for that.
8. All three test issues carry the trigger label. The plan's later gate (S17) says exactly one issue may carry it before any enabled run; remove the label from the other two then.

## Not done / blocked

- The restart test (see above).
- The four decisions the shadow pass needs (right approver would launch, wrong approver `not_approved`, ironbelly approving `not_approved`, edit after approval `edited_after_approval`): only `not_approved` for no approval has been seen so far. The others need someone to set the `Approved` field, which I must not do.

## What the owner still must do

1. Decide who approves: ask clayphi (id 193966884, already in the approvers file) to set `Approved` = Yes on one test issue (suggest issue 2) after the trigger label, and to leave the other two unapproved. A dry run then shows `launched` (would launch) for it. Do not edit issue 2 after the approval, or the decision becomes `edited_after_approval` (which is itself one of the four wanted decisions).
2. For the "ironbelly approving" decision, the ironbelly login would have to set `Approved` on issue 3 (a person doing it by hand; I did not). Dry runs only, enabled stays false, so no launch can follow.
3. Check the shadow log after 24 hours (`/home/coder/.aidev/logs/orchestrator-sandbox-shadow.log`): zero `cycle_crashed`, every tick exit 0 or a named skip, `dispatch.json` hash still 3ff2e6c9..., no gaps over 15 minutes.
4. R4 and everything after need a separate go. Nothing was launched, claimed or approved.

## Hard limits check

No real `run-all`; no `first_run`; no cron or systemd; enabled false in the sandbox config; no GitHub write outside the sandbox repo and Project 4; no Approved field set; no token or runtime file read; UV used for Python.
