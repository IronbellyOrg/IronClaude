# Position CLAY (D02): an Orca automation with a no-agent precheck runs the poll

Topic: Scheduler, cron or Orca automation. Author role: advocate for Clay's line.

## Claim

The poll runs from one Orca automation, `orchestrator-poll`, trigger `*/5 * * * *`, whose precheck command starts `superclaude issue-watch once` detached and then exits 1. Orca records `skipped_precheck`, starts no agent and leaves no terminal. The owner's objection ("an automation starts an agent on each run") fails exactly where the precheck exits non-zero.

## Mechanism

Orca's rule, from its CLI help on this host (`orca-ide automations create --help`): "Use --precheck to run a command only before scheduled runs; exit code 0 continues, any other exit, error, or timeout skips the run. Skips appear in Orca run history ... as skipped_precheck." The precheck loads the workspace environment (`bash -lc 'set -a; . ~/.aienv ...'`), starts the poll with `setsid nohup ... &`, and ends `exit 1` (design 4.8, `docs/designs/orchestrator.md:343-354`; ruling R4 at line 76).

## Cited facts

1. The pattern is already on master and in use: `src/superclaude/skills/agent-work-report/SKILL.md:30` (master, via PR 684, the work-report skill move): "Each runs the script as its precheck command, detached, and exits non-zero so Orca starts no agent and leaves no terminal (VERIFIED 2026-11-03)", with the exact `bash -lc '...setsid nohup python3 waker.py <mode> ... &'; exit 1` line.
2. `waker.py` (`src/superclaude/skills/agent-work-report/scripts/waker.py:1-2`) opens with "The waker: the Orca automation's only job". Its comments record real firings: 2026-11-04 (the run opened 8 seconds after the wake line, lines 314-317) and 2026-11-18 (a usage-limit error four minutes after the wake line, lines 144-146). So the pattern has run on Clay's host for about two weeks.
3. A second definition in master uses the same shape: `scripts/merged_pr_log_orca_automation.md:17-23` (the merged pull request log; written, not switched on).
4. The official Orca documentation (https://orca.dev/docs/cli/automations) calls the precheck "a lightweight shell command" and says a "non-zero exit records a skipped run". The CLI help adds that Run now and `orca automations run` bypass it. Gating is documented behaviour.
5. The poll is detached, so the 60-second precheck limit does not apply to it (`orchestrator.md:322`); the poll keeps its own `flock` on `state_dir/lock` (master `record.py:382`; exit 75 hidden by the detach, seen in `status` and the audit log, `orchestrator.md:329`).
6. Nothing outside this repo has to change: no image, no cron package, no daemon start, no per-boot crontab step. Coder issue 515 says the crontab "is outside home and is reset on image updates" and needs a boot step; Orca's user data lives in `/home/coder/.config/orca` (process list: `--user-data-dir=/home/coder/.config/orca`), on the persisted home volume (issue 515 text). That an automation survives an image update is an inference, not a test (UNVERIFIED).
7. The design lists its own weak points and plans a check: U6 (PATH inside the precheck shell; partly verified, `bash -lc 'command -v superclaude gh orca ccsession'` finds all four, `orchestrator.md:1264`), U7 (accepts `*/5`: create with `--disabled` and read the next run), and a 24-hour shadow run with `--dry-run` as a scheduled run before switch-on (`orchestrator.md:354`, `:966`).
8. Orca keeps run history and a schedule view; `orca automations list` shows the next run (design O3/O4, `orchestrator.md:1025`).
9. Clay's #450 comment of 2026-11-18 17:00:32 already asked for "an Orca automation, not cron" (G-history.md); issue 655 ruling R4 says the same. The owner's reason (requirements line 18; Coder 515) was written afterwards.

## Cost

- `--prompt` and `--provider` are required and unused; the prompt must say so ("unused: the precheck never lets a run start").
- "Run now" and `orca automations run` bypass the precheck, so a click starts a real Claude session in the orchestrator workspace. The design handles this only by using a scheduled shadow run (`orchestrator.md:354`).
- The poll's own outcome is not in Orca's history, only in `audit.jsonl` and `issue-watch status`.
- Creating the automation is an owner step (O3 and O4); N5 forbids the orchestrator from doing it.

## Risk

- Official documentation does not describe a script-only automation: the precheck is documented as a gate. The pattern rests on documented precheck semantics plus about two weeks of waker runs.
- This host has no automation yet (`orca automations list`: none), so U6 and U7 are still to be observed here. The waker automations run on Clay's host (read from the design: UNVERIFIED on this host).
- Whether the schedule keeps firing when the Orca app or server is not running is not stated in the documentation I could read. On this host the Orca server runs headless (`orca-ide --serve`, up since boot).

## What CLAY gets right

- It has evidence that the stated blocker against automations does not hold: a precheck that exits non-zero starts no agent, and a master skill documents it as VERIFIED.
- It adds no new service: the scheduler is part of the Orca runtime the poll must reach anyway to wake sessions.
- It removes a cross-repo dependency: no template change in another repository (Coder issue 515).
