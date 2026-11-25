# Round 1 statement: Variant 1 advocate (OURS, cron with one dispatcher), debate D02

Role: advocate for Variant 1. Opponent: Variant 2 (CLAY, Orca automation with a no-agent precheck).
Sources read: variant-1-original.md, variant-2-original.md, diff-analysis.md, plus the files named in the evidence below.

## Position

Cron with one dispatcher stays the scheduler. I rate this about 60% likely to be the better choice, so it is a close call and I say so. The owner's written reason ("an automation starts an agent on each run") is not enough on its own, because with a non-zero precheck exit Orca skips the run. The case for cron rests on four things I verified:

1. An automation can start an agent by an ordinary click ("Run now"). Cron has no such path.
2. An automation needs a manual create step on each host, and the design forbids the orchestrator to do it.
3. Each tick's outcome is visible in a plain log under cron. Under the precheck pattern it is not visible in Orca.
4. The precheck pattern is proven only at two firings a day, not at 288.

## Steelman of Variant 2

The strongest version of Variant 2 is this. The owner's objection is a fact about the default automation, not about the precheck pattern. Orca's own help says "exit code 0 continues, any other exit, error, or timeout skips the run" and that skips are recorded as `skipped_precheck`. So a precheck that starts the poll detached and exits 1 starts no agent and leaves no terminal. This is not theory: master's `agent-work-report/SKILL.md:30` says the waker automations "exit non-zero so Orca starts no agent and leaves no terminal (VERIFIED 2026-11-03)", and `waker.py:1` calls itself "the Orca automation's only job". The scheduler lives in the Orca runtime the poll has to reach anyway. Nothing in the Coder image has to change for the scheduler, so the open Coder issue 515 is not on the critical path. Clay asked for an automation on #450 before the owner wrote the objection. Variant 2 also lists its own weak points honestly (U6, U7, no automation on this host) and plans a 24-hour scheduled `--dry-run` shadow run.

What Variant 2 genuinely gets right:
- The "starts an agent" sentence is false for exit 1. I confirmed the CLI help text on this host (`orca-ide automations create --help`).
- The pattern ships on master today. I read `SKILL.md:30` in the master snapshot (`/home/coder/.cache/ic-snap-20261120/master/src/superclaude/skills/agent-work-report/SKILL.md`).
- Cron is running nowhere today, and its prerequisite is in another repository (Coder issue 515, open).
- An automation is not limited to one repo in any way that matters. Its precheck is any shell command, so it could run a dispatcher.

## Key strengths claimed (Variant 1)

1. **No path from a scheduler mistake to a running model.** The CLI help on this host says: "Run now in Orca and orca automations run intentionally bypass the precheck." And the `orca automations create` usage line requires `--prompt` and `--provider`. So an automation named `orchestrator-poll` always carries a real prompt and provider, and one click starts a Claude session. Variant 2 admits this in its Cost section (bullet 2). Its only mitigation is a scheduled shadow run for the first test. That guards the first test, not later clicks by a person or a script. Cron has no such button.
2. **Every tick leaves a plain record.** The handoff doc (`/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/docs/designs/issue-watcher-zero-setup-coder-handoff.md:23`) redirects output to `~/.aidev/logs/issue-watch.log`, and the process exit code is the cycle's. Variant 2 says the poll's outcome "is not in Orca's history, only in `audit.jsonl` and `issue-watch status`" (its Cost bullet 3), and that the detached start hides exit 75 (its fact 5). With `setsid nohup ... &` followed by `exit 1`, Orca shows `skipped_precheck` whether the poll worked or crashed.
3. **Two lock layers, both verified in code.** `loop_lock` in the `claim-handoff-planb` worktree (`src/superclaude/cli/issue_watch/dispatch.py:154-171`) takes a non-blocking `flock` and raises `LoopLockHeld`. `flock -n` in the cron line sits on top. The per-repo lock is `record.py:382` in the master snapshot. A double firing cannot overlap.
4. **Tested under the real scheduler environment.** Requirements row R21 (`/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/releases/backlog/issue-watcher-zero-setup/requirements.md`) records the per-minute cron firing on time on 2026-11-18 and `orca repo list` working with only `HOME` and `PATH=/usr/bin:/bin`. The handoff doc line 28 records `gh auth status` staying logged in under `env -i` on 2026-11-20. Variant 2's U6 and U7 are still unobserved here, and `orca-ide automations list` on this host returns "No automations found" (I ran it).
5. **Zero-setup shape.** One entry, one dispatcher that lists repos each tick (row R16, same file). A new project needs no scheduler step. The template creates the crontab line once per boot (issue 515). An automation needs an owner-run creation step per host (Variant 2 Cost bullet 4: "Creating the automation is an owner step").
6. **Frequency of proof.** The master waker automations fire twice a day (`SKILL.md:30`: triggers `0 12,13 * * 1-5` and `0 14,15 * * 1-5`). A 5-minute poll is 288 firings a day, each adding one `skipped_precheck` run record in Orca history. Whether that is cheap or noisy is UNVERIFIED. The "VERIFIED 2026-11-03" label covers the twice-a-day case.

## Weaknesses identified in Variant 2

1. **"Nothing outside this repo has to change" overstates.** The same paper lists "Creating the automation is an owner step" and cites N5 (the orchestrator may not create it). So there is a manual step per host, which is exactly the R1 zero-setup concern. (X-003.)
2. **The main safety claim depends on a gate the CLI says is bypassable.** Variant 2 concedes it in Cost bullet 2. The "starts no agent" guarantee holds only for scheduled runs.
3. **Evidence is from another cadence and, per Variant 2 itself, another host.** Variant 2 marks the waker evidence as read from the design and UNVERIFIED on this host (its Risk bullet 2). I found no automation on this host. The waker fires twice a day, not every 5 minutes (strength 6).
4. **The observability gap is real.** The outcome sits in `audit.jsonl` and `issue-watch status`, a second place to look, while the scheduler's own screen says "skipped" for every tick.
5. **Survival across an image update is an inference.** Variant 2 marks it UNVERIFIED (its fact 6). Cron's reset is a known cost, but issue 515 plans a boot step for it.
6. **Schedule semantics need workarounds.** `waker.py` (master snapshot, around lines 46-52) computes local time itself and fires at two UTC hours to cope with time zones. That does not affect a `*/5` trigger, so I count it as minor. Whether the schedule fires when the Orca app is not running is not stated in Variant 2's evidence (its own Risk bullet 3).

## Concessions

1. The owner's stated reason (requirements Context list; Coder 515 body) is true only for exit 0. Variant 1's own Risk section says not to lean on it. I do not.
2. Cron runs nowhere today and its prerequisite is open in another repository (Coder 515). That is a real schedule risk. Partial offset: the handoff doc line 26 says the installed `/usr/local/bin/superclaude` on this host does not list `run-all`, so the template must ship a new build anyway. The Coder-side dependency is therefore partly shared, not unique to cron. How much is shared is UNVERIFIED.
3. An automation's `--workspace` binding does not by itself stop it from running a dispatcher, because the precheck is an arbitrary shell command. My "bound to one repo" sentence (Variant 1 Mechanism bullet 3) is weaker than I wrote it.
4. Orca's help says a trigger can be "a 5-field cron expression". So U7 (does it accept `*/5`) is largely answered by the help text, though not by a run.
5. "Debated and rejected" is not backed by the debate folder (Variant 1 Risk bullet 2). I have no evidence that the owner weighed the precheck pattern.
6. The six-field FU-2 line in the older runbook is wrong for cron 3.0pl1 (Variant 1 Cost). Not run here: UNVERIFIED by a test.

## Shared-assumption responses

**A-001: QUALIFY.** The scheduler choice is independent of the poll command only once the command exists. In the `claim-handoff-planb` worktree, `run-all` is defined at `cli.py:432` and `dispatch.py` holds the loop lock. The handoff doc line 26 says the installed build does not have it. Master has only the per-repo `once` (I did not re-check master's CLI here: UNVERIFIED). So both variants depend on merging the dispatcher work. After that, either scheduler can run it. Before that, Variant 2 can ship today with `once` for one repo, and I concede that sequencing point.

**A-002: QUALIFY.** Each workspace does need its own scheduler set-up under both variants. The difference is who does it. Cron's entry is made by the template at every boot (issue 515), with no person. An automation lives in Orca's user data, is created by the owner (N5), and whether it survives an image update is UNVERIFIED. So the assumption is true but hides the main cost difference.

**A-003: ACCEPT.** A 5-minute tick all day is reasonable for both. Both papers use `*/5 * * * *`, and Orca's help accepts a 5-field cron expression. A 5-minute cadence does raise the cost of Variant 2's per-tick run record (strength 6).

## Per-point positions

| Point | Winner | Confidence | Evidence |
|---|---|---|---|
| C-001 starts an agent each run | Variant 2 on the narrow fact; it does not decide the choice | 80% | CLI help: any non-zero exit "skips the run"; Variant 1 Risk bullet 1 already concedes it. "Run now" still bypasses (help text) |
| C-002 fit to one dispatcher over many repos | Draw, slight edge Variant 2 | 55% Variant 2 | The precheck is any shell command, so an automation could call `run-all`; cron's only edge is that nobody creates it per host |
| C-003 outside dependencies | Variant 2, narrowly | 55% | Cron needs Coder 515 (open); but handoff doc line 26 shows the template needs a new `superclaude` build anyway, and the automation needs an owner step |
| C-004 failure modes that start a model | Variant 1 | 75% | CLI help: "Run now ... bypass the precheck"; `--prompt` and `--provider` required; Variant 2 Cost bullet 2 concedes |
| X-001 "starts an agent on each run" | Variant 2 | 85% | Same as C-001. Variant 1 already says it is true only at exit 0 |
| X-002 what an automation is bound to | Variant 2 | 65% | The precheck can run any command; the binding limits the agent workspace, not the shell command |
| X-003 manual set-up per host | Variant 1 | 75% | Variant 2 Cost bullet 4 against its fact 6; N5 and O3/O4 are cited by both papers, but `orchestrator.md` is not in the worktree I checked, so UNVERIFIED by me |
