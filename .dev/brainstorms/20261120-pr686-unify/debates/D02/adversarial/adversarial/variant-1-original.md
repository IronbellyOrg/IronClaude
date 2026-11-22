# Position OURS (D02): cron with one dispatcher runs the poll

Topic: Scheduler, cron or Orca automation. Author role: advocate for the owner's line.

## Claim

The poll must run from plain cron: ONE cron entry runs ONE dispatcher (`superclaude issue-watch run-all`), which lists repos with `orca repo list` and runs each repo's cycle. A scheduler whose only job is "run this command every 5 minutes" should be a scheduler that cannot start an agent.

## Mechanism

- Cron runs `/usr/bin/flock -n /home/coder/.aidev/issue-watch.lock /usr/local/bin/superclaude issue-watch run-all --orca <shim> >> ~/.aidev/logs/issue-watch.log` every 5 minutes. The command is a plain process: it exits with the cycle's own exit code, and the log holds the outcome.
- The dispatcher takes its own `flock` (`dispatch.py:154-171` in worktree `claim-handoff-planb`), and the per-repo cycle keeps its lock (master `src/superclaude/cli/issue_watch/record.py:382`, exit 75 `lock_held`). Two layers, no overlap.
- Cron fits the one-dispatcher shape (R16): the dispatcher discovers repos on every tick, so a new project needs no scheduler change. An Orca automation is bound to one `--repo` or `--workspace`.
- The only thing cron needs from outside this repo is the template: install `cron`, start the daemon at every boot, recreate the entry once per boot (Coder issue 515, open).

## Cited facts

1. Owner decision, requirements R6 and R16 (`/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:36-37`): cron is the scheduler (owner decided 2026-11-18); one entry, one dispatcher; one entry per project was rejected with reasons.
2. R21 (same file, line 49): cron 3.0pl1-197 is installed on this image. A per-minute entry fired on time (20:25:01Z and 20:26:01Z) on 2026-11-18. `orca repo list` run with only `HOME` and `PATH=/usr/bin:/bin` worked (6 repos). The handoff doc (`docs/designs/issue-watcher-zero-setup-coder-handoff.md:28`) records that `gh auth status` stayed logged in under cron's empty environment (tested 2026-11-20).
3. Coder issue 515 (https://github.com/IronbellyOrg/Coder/issues/515, read with `gh`, open; the Coder-repo issue for the cron work) lists the whole job: install cron, start the daemon from `startup.sh`, entry exactly once per boot, `flock -n`, log under `~/.aidev/logs/`. It notes the crontab sits outside the persisted home volume and resets on an image update, so a boot step recreates it. An owner comment of 2026-11-18 18:45 confirms the package part works on this base image.
4. The ready crontab line exists: `*/5 * * * * /usr/bin/flock -n ... superclaude issue-watch run-all --orca ...` (`docs/designs/issue-watcher-zero-setup-coder-handoff.md:23`).
5. Orca's own CLI help for `automations create` (read-only run on this host): `--prompt` and `--provider` are required parameters of every automation. The official documentation (https://orca.dev/docs/cli/automations) says automations "run a prompt on a schedule" through an agent and documents the shell precheck only as a gate; a script-only mode is not documented.
6. The same CLI help says "Run now in Orca and `orca automations run` intentionally bypass the precheck". So a person who clicks Run now on `orchestrator-poll` starts a Claude session with the prompt "unused: the precheck never lets a run start" (design 4.8, `docs/designs/orchestrator.md:348-349`).
7. Under the precheck pattern the poll's outcome stays invisible to Orca: the design says so itself ("the poll's own exit code is in `audit.jsonl` ... not in Orca's run history", `orchestrator.md:354`). Orca history shows only `skipped_precheck`, so "ok" and "the poll crashed" look the same there.
8. Design 4.8 lists its own unverified points: `superclaude` on the PATH of Orca's precheck shell (U6), and that `*/5 * * * *` is accepted by this Orca version (U7) (`orchestrator.md:1264-1265`). `orca automations list` on this host returns "No automations found", so nothing is proven here.
9. Clay's design forbids the orchestrator to create, edit, remove or run an automation (N5, `orchestrator.md:762`) and lists creation as an owner-run step (O3 and O4, `orchestrator.md:1025`). Automation set-up is therefore a manual step per host, against the zero-setup goal (R1).

## Cost

- Cron needs the Coder image change (issue 515, a separate repo, still open), so cron is not running anywhere today.
- The old runbook's FU-2 line is six-field (`0 */5 * * * *`, `docs/designs/issue-watcher-setup.md:288`, `:676`); cron 3.0pl1 takes five fields. The zero-setup handoff already uses five (`*/5 * * * *`). The runbook line must be fixed (not run here: UNVERIFIED by a test).
- Cron and Orca are two services to keep up at boot.

## Risk

- The owner's written reason ("an Orca automation starts an agent session with a prompt on each run", requirements line 18; Coder 515 body) is true only when the precheck exits 0. With `--precheck` ending in a non-zero exit, the CLI help says the run is skipped. Our argument must not lean on that sentence.
- The statement "debated and rejected" is not backed by the owner's debate folder: the only mention of automations in `.dev/releases/backlog/issue-watcher-zero-setup/` is requirements line 18; the debate covers one dispatcher against one entry per project and assumes cron.

## What OURS gets right

- Choose the scheduler that cannot fail by starting a model. Under cron no edit mistake, wrong exit code or "Run now" click can start an agent every 5 minutes; with an automation any of the three can.
- The scheduler is already tested on this host (R21), and the dispatcher lock plus `flock -n` plus a log file give a plain, auditable record of every tick.
- Cron has no hidden dependency on Orca's scheduler semantics (time zone: `waker.py:46-50`; missed-run grace: undocumented).
- One entry for all repos matches the one-dispatcher decision.
