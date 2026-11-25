<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 2 (CLAY, variant-2-original.md) -->
<!-- Merge date: 2026-11-20T04:28:33Z -->

# Merged position (D02): scheduler for the issue-watcher poll

<!-- Source: Refactor plan Overview (neutral framing); base-selection.md (Selected Base rationale). Not a numbered change. -->
How to read this paper. It is a neutral paper of settled facts, contested points and what would settle them. It does not name a winner: the owner's weighting rule is applied later, in VERDICT.md. Variant 2 (CLAY, Orca automation with a no-agent precheck) is the text base because it won a tiebreaker (Variant 1 scored higher raw, 0.875 against 0.831, but the 4.4 point margin is under the 5 point threshold, and Variant 2 won 5 diff points against 3). That selects a document base, not a scheduler. The sections Claim, Mechanism and "What CLAY gets right" are the base text and state the CLAY position in its own voice. They are not this paper's conclusion. Facts from Variant 1 (OURS, cron with one dispatcher) and from the debate are added in the sections that follow, each tagged with its source.

<!-- Source: Base (original) -->
## Claim

Topic: Scheduler, cron or Orca automation. Author role of the base text: advocate for Clay's line.

The poll runs from one Orca automation, `orchestrator-poll`, trigger `*/5 * * * *`, whose precheck command starts `superclaude issue-watch once` detached and then exits 1. Orca records `skipped_precheck`, starts no agent and leaves no terminal. The owner's objection ("an automation starts an agent on each run") fails exactly where the precheck exits non-zero.

<!-- Source: Base (original) -->
## Mechanism

Orca's rule, from its CLI help on this host (`orca-ide automations create --help`): "Use --precheck to run a command only before scheduled runs; exit code 0 continues, any other exit, error, or timeout skips the run. Skips appear in Orca run history ... as skipped_precheck." The precheck loads the workspace environment (`bash -lc 'set -a; . ~/.aienv ...'`), starts the poll with `setsid nohup ... &`, and ends `exit 1` (design 4.8, `docs/designs/orchestrator.md:343-354`; ruling R4 at line 76).

<!-- Source: Variant 1 (Mechanism; Cited facts 2, 4), debate-transcript.md (A-001, Round 2 both advocates), invariant-probe.md (INV-015, INV-022, INV-023); diff-analysis.md A-001 - merged per Change #6 (new section) -->
## Which poll is scheduled

The two position papers do not compare the same command. The scheduler choice cannot be judged apart from which poll runs, so the comparison is written per command.

| Command | Where it exists | How it finds repos | New project |
|---|---|---|---|
| `superclaude issue-watch once` | Master and the PR 686 design. The PR 686 design reshapes `once` to one config with `orchestrator_repo` and no per-repo keys (`orchestrator.md:269`, reshape row at `:372`) | Reads `<orchestrator-repo>/repos.yaml`, which the orchestrator edits "on the user's word" or after a one-time proposal (`orchestrator.md:269`, `:302`) | Not enrolled automatically (INV-015) |
| `superclaude issue-watch run-all` | Only in the unpushed branch `ironbelly/issue-watcher-zero-setup-plan`, worktree `claim-handoff-planb` (`cli.py:432`; the branch has no upstream and no remote branch). The installed `/usr/local/bin/superclaude` on this host does not list it (handoff doc, line 26). The master snapshot and the PR 686 snapshot do not contain it | Lists repos with `orca repo list` on every tick and starts `superclaude issue-watch once --config <file>` once per repo, with per-repo configs in `issue-watch.d` (`dispatch.py:9`; R8, R16) | Enrolled automatically (INV-015) |

- Variant 1 (cron) describes `run-all`. Variant 2 (automation) describes `once` with `repos.yaml`. Part of C-002 and C-003 is therefore "which poll ships", not "which scheduler".
- Both advocates agree the scheduler is independent of the command in principle: a precheck can run `run-all` as easily as `once`, and cron can run `once` (A-001). Both agree the verdict should be written per command.
- For `once`, Variant 1 concedes that the automation route can ship today with `once` for one repo (a sequencing point). For `run-all`, both routes wait for the unpushed branch and a new `superclaude` build, so the missing command weakens neither scheduler more than the other (Variant 1 Round 2; Variant 2 Round 2).
- Open and blocking (INV-023, HIGH, UNADDRESSED): whether `run-all` can sit on top of the PR 686 poll after it merges. `run-all` passes per-repo configs to `once`; the PR 686 design has one config and `repos.yaml`, and a search of that design for `run-all`, `issue-watch.d` and `--config` finds nothing. The two polls differ in contract, not only in shape. Any verdict must say which poll the chosen scheduler runs.

<!-- Source: Base (original), with fact 6 modified per Change #5 and a new fact 9 added per Change #2 -->
## Cited facts

1. The pattern is already on master and in use: `src/superclaude/skills/agent-work-report/SKILL.md:30` (master, via PR 684, the work-report skill move): "Each runs the script as its precheck command, detached, and exits non-zero so Orca starts no agent and leaves no terminal (VERIFIED 2026-11-03)", with the exact `bash -lc '...setsid nohup python3 waker.py <mode> ... &'; exit 1` line.
2. `waker.py` (`src/superclaude/skills/agent-work-report/scripts/waker.py:1-2`) opens with "The waker: the Orca automation's only job". Its comments record real firings: 2026-11-04 (the run opened 8 seconds after the wake line, lines 314-317) and 2026-11-18 (a usage-limit error four minutes after the wake line, lines 144-146). So the pattern has run on Clay's host for about two weeks.
3. A second definition in master uses the same shape: `scripts/merged_pr_log_orca_automation.md:17-23` (the merged pull request log; written, not switched on).
4. The official Orca documentation (https://orca.dev/docs/cli/automations) calls the precheck "a lightweight shell command" and says a "non-zero exit records a skipped run". The CLI help adds that Run now and `orca automations run` bypass it. Gating is documented behaviour.
5. The poll is detached, so the 60-second precheck limit does not apply to it (`orchestrator.md:322`); the poll keeps its own `flock` on `state_dir/lock` (master `record.py:382`; exit 75 hidden by the detach, seen in `status` and the audit log, `orchestrator.md:329`).
<!-- Source: Base (original, modified) - fact 6 rewritten per Change #5 to repair the overbroad sentence "Nothing outside this repo has to change" (base weakness K4, X-003); the Coder 515 and persistence sentences are base text. Support: Variant 2 Round 2 concession 4, Variant 1 Round 2 concession 5 -->
6. No image change, no cron package, no daemon start and no per-boot crontab step are needed for the scheduler. One creation step per Orca host is still needed. The design makes it an owner-run step (O3 and O4, `orchestrator.md:1025`), and N5 forbids the orchestrator from creating the automation (`orchestrator.md:762`). N5 binds the orchestrator, not a boot script: a boot script could run `orca automations list --json` and then `create` if the name is absent, but no such script exists and none has been tested (UNVERIFIED). Coder issue 515 says the crontab "is outside home and is reset on image updates" and needs a boot step; Orca's user data lives in `/home/coder/.config/orca` (process list: `--user-data-dir=/home/coder/.config/orca`), on the persisted home volume (issue 515 text). That an automation survives an image update is an inference, not a test (UNVERIFIED).
<!-- Source: Base (original) -->
7. The design lists its own weak points and plans a check: U6 (PATH inside the precheck shell; partly verified, `bash -lc 'command -v superclaude gh orca ccsession'` finds all four, `orchestrator.md:1264`), U7 (accepts `*/5`: create with `--disabled` and read the next run), and a 24-hour shadow run with `--dry-run` as a scheduled run before switch-on (`orchestrator.md:354`, `:966`).
8. Orca keeps run history and a schedule view; `orca automations list` shows the next run (design O3/O4, `orchestrator.md:1025`).
<!-- Source: Variant 1, Cited fact 2 (with limits from Variant 1 Round 2 concession 1 and Round 2 new evidence 1) - merged per Change #2 (new fact) -->
9. What cron has been tested for on this host: a per-minute cron entry fired on time (20:25:01Z and 20:26:01Z) on 2026-11-18 (requirements R21, `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:49`). `orca repo list` run with only `HOME` and `PATH=/usr/bin:/bin` worked (6 repos). The handoff doc (`docs/designs/issue-watcher-zero-setup-coder-handoff.md:28`) records that `gh auth status` stayed logged in under cron's empty environment (tested 2026-11-20). This tests the mechanism, not the install path. Cron was installed by hand (`apt install cron`, requested by `coder`, 2026-11-18 18:40:49), the daemon was started by hand (2026-11-18 20:20:37), the crontab is empty today and Coder issue 515 is open. The installed cron is version 3.0pl1-197 (R21).
<!-- Source: Base (original) - renumbered from 9 to 10 because of the new fact 9 (Change #2) -->
10. Clay's #450 comment of 2026-11-18 17:00:32 already asked for "an Orca automation, not cron" (G-history.md); issue 655 ruling R4 says the same. The owner's reason (requirements line 18; Coder 515) was written afterwards.

<!-- Source: Base (original), with bullet 2 replaced per Change #1 and a new bullet 5 added per Change #3 -->
## Cost

<!-- Source: Base (original) -->
- `--prompt` and `--provider` are required and unused; the prompt must say so ("unused: the precheck never lets a run start").
<!-- Source: Variant 1, Mechanism and Cited facts 5, 6; debate-transcript.md Round 2 (both advocates, Variant 2 concessions 1 and 2) - merged per Change #1 (replaces base bullet 2) -->
- "Run now" and `orca automations run` bypass the precheck, so a click starts a real Claude session in the orchestrator workspace, with the prompt "unused: the precheck never lets a run start" (design 4.8, `orchestrator.md:348-349`). Variant 2's advocate confirmed in the installed Orca code that a run whose trigger is not scheduled skips the precheck. A second path: if the `exit 1` is dropped (the switch-on step edits the precheck command, `orchestrator.md:354`), the precheck exits 0 and a session starts at every tick, up to 288 a day. Cron has neither path. Both advocates agree the harm is bounded: one idle session per click, and a few sessions at most for a dropped `exit 1`, because the first scheduled tick shows a new terminal and a `dispatched` row instead of `skipped_precheck`. The design handles the first-run case by using a scheduled shadow run, so its first runs do not use the bypass (`orchestrator.md:354`). Two mitigations were offered by Variant 2's advocate in Round 2. They are suggestions, not facts about master and not in the design: (a) replace the hand-typed `...; exit 1` with a fixed command whose code starts the poll detached and returns 1 on every path, covered by a unit test; (b) make the automation prompt an instruction ("do nothing and stop") so a stray click costs one short reply.
<!-- Source: Base (original) -->
- The poll's own outcome is not in Orca's history, only in `audit.jsonl` and `issue-watch status`.
- Creating the automation is an owner step (O3 and O4); N5 forbids the orchestrator from doing it.
<!-- Source: Variant 1, Cost bullet 2; debate-transcript.md Round 2 concession 7 (Variant 1); diff-analysis.md C-010 and U-004 - merged per Change #3 (new bullet) -->
- The old runbook's cron line is six fields (`0 */5 * * * *`, `docs/designs/issue-watcher-setup.md:288`, `:676`); cron 3.0pl1 takes five. The zero-setup handoff already uses five (`*/5 * * * *`). Not run here: UNVERIFIED by a test. The base's design 4.8 drops cron entirely, so the fix applies only if cron stays. Both advocates agree it is a documentation defect, not a decision factor (C-010).

<!-- Source: Base (original), with a new sentence per Change #2 and a new bullet per Change #4 -->
## Risk

<!-- Source: Base (original) -->
- Official documentation does not describe a script-only automation: the precheck is documented as a gate. The pattern rests on documented precheck semantics plus about two weeks of waker runs.
- This host has no automation yet (`orca automations list`: none), so U6 and U7 are still to be observed here. The waker automations run on Clay's host (read from the design: UNVERIFIED on this host).
- Whether the schedule keeps firing when the Orca app or server is not running is not stated in the documentation I could read. On this host the Orca server runs headless (`orca-ide --serve`, up since boot).
<!-- Source: Variant 1, Cited fact 2; debate-transcript.md Round 2 concession 1 (Variant 1), Scoring Matrix C-006 (Draw, 70%) - merged per Change #2 (one sentence in Risk) -->
- The evidence for each scheduler is partial: cron's mechanism was tested on this host but its install path was not (fact 9), and the waker pattern is marked VERIFIED only for two firings a day on another host, with no automation fired here (the debate scored this point, C-006, a draw).
<!-- Source: Variant 1, Risk bullet 2; debate-transcript.md Round 1 and Round 2 (both advocates); invariant-probe.md INV-028 - merged per Change #4 (new bullet) -->
- The statement "debated and rejected" is not backed by the owner's debate folder. The only mention of automations in `.dev/releases/backlog/issue-watcher-zero-setup/` is requirements line 18; the debate there covers one dispatcher against one entry per project and assumes cron. Both advocates and the fault-finder (INV-028) agree. The owner's written reason ("an Orca automation starts an agent session with a prompt on each run", requirements line 18 and the Coder 515 body) is true only when the precheck exits 0. Consequence: if cron stays, the written reason must be restated (INV-028 names the real reasons: zero setup R1, one dispatcher R16, no click path), or the next reader will reopen D02 on a false premise.

<!-- Source: Base (original) -->
## What CLAY gets right

- It has evidence that the stated blocker against automations does not hold: a precheck that exits non-zero starts no agent, and a master skill documents it as VERIFIED.
- It adds no new service: the scheduler is part of the Orca runtime the poll must reach anyway to wake sessions.
- It removes a cross-repo dependency: no template change in another repository (Coder issue 515).

<!-- Source: invariant-probe.md INV-024, INV-008, INV-011, INV-017, INV-020 (with INV-001 and INV-026 context); debate-transcript.md Round 2.5 - merged per Change #7 (new section) -->
## What the scheduler choice does not settle

These items stay open whichever scheduler is chosen, or are decided by something other than the scheduler.

- **Zero setup (R1, R17) is not decided by cron or by an automation (INV-024, HIGH, UNADDRESSED).** Falsifiers that hold today: (a) Coder issue 515 is open, cron was installed and started by hand (fact 9); (b) each host must run `superclaude install --force` once, a manual step, until then guard version 1 applies (handoff doc, lines 63-65); (c) the owner creates the `Approved` org field once (handoff doc, line 57); (d) Coder issue 516 (open, last update 2026-11-18T18:45) must create the `Coordinator` worktree, and without it `run-all` skips the repo with `worktree_invalid` (`dispatch.py:279-280`). Only (a) was debated. Cron fixes the scheduler step and not the others. The automation route has its own creation step (fact 6).
- **A sweep can outlast the tick (INV-011, MEDIUM).** `LOOP_CAP_S = 270.0` and `CHILD_TIMEOUT_S = 255.0` (`dispatch.py:52-53`): the loop stops starting children at 270 s, and a child started at 269 s may run 255 s more, about 525 s against a 300 s tick. The next tick then loses `flock -n` silently (cron) or exits 75 hidden by the detach (automation, `orchestrator.md:329`). The papers compared only the 240 s single-repo deadline with the tick. The probe reads this as making skipped ticks routine with 6 repos on a slow GitHub day; that reading was not measured.
- **Nobody reads a silent scheduler failure (INV-008, MEDIUM).** `flock -n` exits silently when it loses the race, cron drops the exit code, and the automation hides exit 75. The only "stale" logic in master is per entry (`cycle.py:1251`, `cli.py:152-168`), not "no sweep ran in N minutes". This host has no syslog and no `/var/log/cron*`. Both advocates agree a gap in the log is the signal, but nothing reads that gap under either scheduler.
- **The automation is coupled to the orchestrator checkout path (INV-017, MEDIUM).** It is bound to `--workspace path:<orchestrator-repo>` (`orchestrator.md:349`). Per Variant 2's reading of the installed code (not re-checked by the fault-finder), an unresolvable workspace counts as a failed precheck and the run is skipped. If that checkout moves or is removed, the poll stops and leaves only skip rows in a 100-row history. Under cron a bad worktree is a named, logged skip per repo (`worktree_invalid`, `dispatch.py:279-281`). The orchestrator checkout is also the live session worktree (requirements Findings, last bullet), so churn there is real.
- **Two workspaces for one user (INV-020, MEDIUM).** `/home/coder` is a persisted per-workspace volume (issue 515 body), so each workspace has its own scheduler, `state_dir` and lock. Locks are host-local under both schedulers; only GitHub-side checks (the assignee rule and re-read, `orchestrator.md:316-317`) narrow the window between two hosts. This does not separate the two schedulers, and no paper tested duplicate claims across hosts.
- **Project enrolment follows the poll, not the scheduler (INV-015, MEDIUM).** See "Which poll is scheduled".

<!-- Source: debate-transcript.md (Metadata, Scoring Matrix, Convergence Assessment, Round 2 "What would change my mind" of both advocates); invariant-probe.md (INV-023, INV-024, INV-026) - merged per Change #8 (new closing section) -->
## Debate outcome (D02)

### Process

Depth standard: Round 1 statements, Round 2 rebuttals and a Round 2.5 invariant probe. Round 3 was not run. The two advocates ran as separate agents; Variant 1's advocate argued for cron with one dispatcher, Variant 2's advocate for the Orca automation. Convergence: 15 of 18 diff points resolved (83.3%, threshold 80%). Status: BLOCKED_BY_INVARIANTS, because two HIGH invariants are UNADDRESSED (below).

### Point results

These are point-level results from the debate's scoring matrix. They are not summed into a choice in this paper. Confidence is the mean of the two advocates' Round 2 figures where both gave one.

| Point | Topic | Point-level result | Confidence |
|---|---|---|---|
| S-001 | Section order | Draw | 90% |
| S-002 | What the Risk sections hold | Draw | 90% |
| C-001 | Does an automation start an agent on each run | Variant 2 (automation): the owner's sentence is true only at exit 0 | 91% |
| C-002 | Fit to one dispatcher over many repos | Variant 2, narrow; per-command question (INV-023) | 56% |
| C-003 | Dependencies outside this repository | Variant 2; offsets: both routes need a new `superclaude` build, the automation needs a creation step | 60% |
| C-004 | Failure modes that start a model | Variant 1 (cron): small margin, harm bounded | 67% |
| C-005 | Observability of each tick | Draw | 70% |
| C-006 | Evidence the scheduler works | Draw | 70% |
| C-007 | Documentation support | Variant 1, narrow: script-only use is undocumented officially | 55% |
| C-008 | Survives an image update | Unresolved | 50% |
| C-009 | Known-unverified items | Draw | 80% |
| C-010 | Six-field cron line in the old runbook | Variant 1 (doc fix, not a decision factor) | 85% |
| X-001 | "Starts an agent on each run" | Variant 2 | 91% |
| X-002 | What an automation is bound to | Variant 2: the binding gives the precheck its working directory only | 67% |
| X-003 | Manual set-up per host | Unresolved | 50% |
| A-001 | Scheduler choice does not change the poll command | Both: write the verdict per command | 60% |
| A-002 | Every workspace needs its own scheduler set-up | Unresolved | 50% |
| A-003 | A 5-minute tick all day is right | Draw | 60% |

### Unresolved points

- **C-008, an automation surviving an image update.** Variant 2's advocate puts it at 65% (the profile is on the persisted volume and its file dates predate the program update; an inference). Variant 1's advocate did not accept it. Untested either way.
- **X-003, manual set-up per host.** Variant 1 55%, Variant 2 50%. N5 binds the orchestrator, not a boot script, and a boot script doing `list --json` then `create` is possible; none exists. Cron's boot work (issue 515) is also unfinished.
- **A-002, one scheduler set-up per workspace.** Variant 1 55% for cron, Variant 2 55% for the automation. Each route's boot step is unwritten.

### Blocking invariants

- **INV-023:** which poll the scheduler runs. See "Which poll is scheduled".
- **INV-024:** the scheduler does not decide zero setup. See "What the scheduler choice does not settle".

Five MEDIUM invariants were raised as warnings and do not block: INV-008, INV-011, INV-015, INV-017, INV-020 (all covered in the two sections above).

### Where the advocates ended

After Round 2, Variant 1's advocate put it at about 50% that cron is the better scheduler (down from about 60%). Variant 2's advocate put it at about 55% that the automation is the better scheduler on technical merits, resting mostly on two inferences (survival of the automation, and firing with no window open) that were read from files and code, not run. Both call it a toss-up. Both state that the owner's recorded decision (R6 and R16, 2026-11-18) is not overturned by anything in the debate folder unless the decisive fact below appears. This paper does not choose between them; the owner's weighting rule is applied in VERDICT.md.

### The decisive fact

Both advocates name the same fact. A `*/5 * * * *` automation with a `; exit 1` precheck, created `--disabled` and then enabled on this host under the present headless Orca server, fires on its schedule for 1 to 24 hours (Variant 2's advocate asked for at least one hour; Variant 1's for 24 hours). The history shows only `skipped_precheck` rows, no session is started, and the automation is still listed after an Orca server restart. It cannot be obtained read-only: creating an automation was out of bounds for the debate, and `orca automations list` is empty (INV-026).

- If it holds, Variant 1's advocate moves to about 65% for the automation and Variant 2's advocate to about 70%; Variant 2's advocate would also ask for the fixed always-exit-1 command and the "do nothing" prompt (Cost, mitigations a and b).
- If the automation stops firing when no window is open, is lost on restart, or fills the history without bound, Variant 1's advocate moves to about 70% for cron. Variant 2's advocate would concede outright (about 75%) if the scheduler records `skipped_unavailable` or nothing with no window open, or the automation is gone after a restart.

A second, smaller fact would move both advocates on X-003: a template boot script that runs `orca automations list --json` and then `create`, shown to leave exactly one automation after two boots in a row, and shown to run before the first tick.


