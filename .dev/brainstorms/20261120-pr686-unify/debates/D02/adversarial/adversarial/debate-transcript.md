# Adversarial Debate Transcript (D02: scheduler, cron or Orca automation)

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 statements, Round 2 rebuttals) plus Round 2.5 invariant probe; Round 3 not run (depth standard)
- Convergence achieved: 83.3% on diff points (15 of 18 agreed), but BLOCKED_BY_INVARIANTS (2 HIGH UNADDRESSED: INV-023, INV-024)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 2 (Variant 1 advocate = OURS, cron with one dispatcher; Variant 2 advocate = CLAY, Orca automation with a no-agent precheck)
- Advocates were run as separate Agent-tool subagents (general-purpose). Round 2 ran in sequence: Variant 1 first, then Variant 2 (who saw Variant 1's rebuttal).
- Process note: during Round 2 the Variant 2 advocate's read command printed a local Orca auth token (file `orca-runtime.json`) into its own transcript. It is not copied into any debate file. The owner may want to rotate it.
- Omissions check (A-001, A-002, A-003): all four advocate statements answered all three (no [OMISSION] flags).

The two Round 1 and two Round 2 statements below are the unedited files written by the advocates (`rounds/round1-advocate-1.md`, `rounds/round1-advocate-2.md`, `rounds/round2-advocate-1.md`, `rounds/round2-advocate-2.md`).

## Round 1: Advocate Statements

### Variant 1 Advocate (OURS)
Role: advocate for Variant 1. Opponent: Variant 2 (CLAY, Orca automation with a no-agent precheck).
Sources read: variant-1-original.md, variant-2-original.md, diff-analysis.md, plus the files named in the evidence below.

#### Position

Cron with one dispatcher stays the scheduler. I rate this about 60% likely to be the better choice, so it is a close call and I say so. The owner's written reason ("an automation starts an agent on each run") is not enough on its own, because with a non-zero precheck exit Orca skips the run. The case for cron rests on four things I verified:

1. An automation can start an agent by an ordinary click ("Run now"). Cron has no such path.
2. An automation needs a manual create step on each host, and the design forbids the orchestrator to do it.
3. Each tick's outcome is visible in a plain log under cron. Under the precheck pattern it is not visible in Orca.
4. The precheck pattern is proven only at two firings a day, not at 288.

#### Steelman of Variant 2

The strongest version of Variant 2 is this. The owner's objection is a fact about the default automation, not about the precheck pattern. Orca's own help says "exit code 0 continues, any other exit, error, or timeout skips the run" and that skips are recorded as `skipped_precheck`. So a precheck that starts the poll detached and exits 1 starts no agent and leaves no terminal. This is not theory: master's `agent-work-report/SKILL.md:30` says the waker automations "exit non-zero so Orca starts no agent and leaves no terminal (VERIFIED 2026-11-03)", and `waker.py:1` calls itself "the Orca automation's only job". The scheduler lives in the Orca runtime the poll has to reach anyway. Nothing in the Coder image has to change for the scheduler, so the open Coder issue 515 is not on the critical path. Clay asked for an automation on #450 before the owner wrote the objection. Variant 2 also lists its own weak points honestly (U6, U7, no automation on this host) and plans a 24-hour scheduled `--dry-run` shadow run.

What Variant 2 genuinely gets right:
- The "starts an agent" sentence is false for exit 1. I confirmed the CLI help text on this host (`orca-ide automations create --help`).
- The pattern ships on master today. I read `SKILL.md:30` in the master snapshot (`/home/coder/.cache/ic-snap-20261120/master/src/superclaude/skills/agent-work-report/SKILL.md`).
- Cron is running nowhere today, and its prerequisite is in another repository (Coder issue 515, open).
- An automation is not limited to one repo in any way that matters. Its precheck is any shell command, so it could run a dispatcher.

#### Key strengths claimed (Variant 1)

1. **No path from a scheduler mistake to a running model.** The CLI help on this host says: "Run now in Orca and orca automations run intentionally bypass the precheck." And the `orca automations create` usage line requires `--prompt` and `--provider`. So an automation named `orchestrator-poll` always carries a real prompt and provider, and one click starts a Claude session. Variant 2 admits this in its Cost section (bullet 2). Its only mitigation is a scheduled shadow run for the first test. That guards the first test, not later clicks by a person or a script. Cron has no such button.
2. **Every tick leaves a plain record.** The handoff doc (`/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/docs/designs/issue-watcher-zero-setup-coder-handoff.md:23`) redirects output to `~/.aidev/logs/issue-watch.log`, and the process exit code is the cycle's. Variant 2 says the poll's outcome "is not in Orca's history, only in `audit.jsonl` and `issue-watch status`" (its Cost bullet 3), and that the detached start hides exit 75 (its fact 5). With `setsid nohup ... &` followed by `exit 1`, Orca shows `skipped_precheck` whether the poll worked or crashed.
3. **Two lock layers, both verified in code.** `loop_lock` in the `claim-handoff-planb` worktree (`src/superclaude/cli/issue_watch/dispatch.py:154-171`) takes a non-blocking `flock` and raises `LoopLockHeld`. `flock -n` in the cron line sits on top. The per-repo lock is `record.py:382` in the master snapshot. A double firing cannot overlap.
4. **Tested under the real scheduler environment.** Requirements row R21 (`/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/releases/backlog/issue-watcher-zero-setup/requirements.md`) records the per-minute cron firing on time on 2026-11-18 and `orca repo list` working with only `HOME` and `PATH=/usr/bin:/bin`. The handoff doc line 28 records `gh auth status` staying logged in under `env -i` on 2026-11-20. Variant 2's U6 and U7 are still unobserved here, and `orca-ide automations list` on this host returns "No automations found" (I ran it).
5. **Zero-setup shape.** One entry, one dispatcher that lists repos each tick (row R16, same file). A new project needs no scheduler step. The template creates the crontab line once per boot (issue 515). An automation needs an owner-run creation step per host (Variant 2 Cost bullet 4: "Creating the automation is an owner step").
6. **Frequency of proof.** The master waker automations fire twice a day (`SKILL.md:30`: triggers `0 12,13 * * 1-5` and `0 14,15 * * 1-5`). A 5-minute poll is 288 firings a day, each adding one `skipped_precheck` run record in Orca history. Whether that is cheap or noisy is UNVERIFIED. The "VERIFIED 2026-11-03" label covers the twice-a-day case.

#### Weaknesses identified in Variant 2

1. **"Nothing outside this repo has to change" overstates.** The same paper lists "Creating the automation is an owner step" and cites N5 (the orchestrator may not create it). So there is a manual step per host, which is exactly the R1 zero-setup concern. (X-003.)
2. **The main safety claim depends on a gate the CLI says is bypassable.** Variant 2 concedes it in Cost bullet 2. The "starts no agent" guarantee holds only for scheduled runs.
3. **Evidence is from another cadence and, per Variant 2 itself, another host.** Variant 2 marks the waker evidence as read from the design and UNVERIFIED on this host (its Risk bullet 2). I found no automation on this host. The waker fires twice a day, not every 5 minutes (strength 6).
4. **The observability gap is real.** The outcome sits in `audit.jsonl` and `issue-watch status`, a second place to look, while the scheduler's own screen says "skipped" for every tick.
5. **Survival across an image update is an inference.** Variant 2 marks it UNVERIFIED (its fact 6). Cron's reset is a known cost, but issue 515 plans a boot step for it.
6. **Schedule semantics need workarounds.** `waker.py` (master snapshot, around lines 46-52) computes local time itself and fires at two UTC hours to cope with time zones. That does not affect a `*/5` trigger, so I count it as minor. Whether the schedule fires when the Orca app is not running is not stated in Variant 2's evidence (its own Risk bullet 3).

#### Concessions

1. The owner's stated reason (requirements Context list; Coder 515 body) is true only for exit 0. Variant 1's own Risk section says not to lean on it. I do not.
2. Cron runs nowhere today and its prerequisite is open in another repository (Coder 515). That is a real schedule risk. Partial offset: the handoff doc line 26 says the installed `/usr/local/bin/superclaude` on this host does not list `run-all`, so the template must ship a new build anyway. The Coder-side dependency is therefore partly shared, not unique to cron. How much is shared is UNVERIFIED.
3. An automation's `--workspace` binding does not by itself stop it from running a dispatcher, because the precheck is an arbitrary shell command. My "bound to one repo" sentence (Variant 1 Mechanism bullet 3) is weaker than I wrote it.
4. Orca's help says a trigger can be "a 5-field cron expression". So U7 (does it accept `*/5`) is largely answered by the help text, though not by a run.
5. "Debated and rejected" is not backed by the debate folder (Variant 1 Risk bullet 2). I have no evidence that the owner weighed the precheck pattern.
6. The six-field FU-2 line in the older runbook is wrong for cron 3.0pl1 (Variant 1 Cost). Not run here: UNVERIFIED by a test.

#### Shared-assumption responses

**A-001: QUALIFY.** The scheduler choice is independent of the poll command only once the command exists. In the `claim-handoff-planb` worktree, `run-all` is defined at `cli.py:432` and `dispatch.py` holds the loop lock. The handoff doc line 26 says the installed build does not have it. Master has only the per-repo `once` (I did not re-check master's CLI here: UNVERIFIED). So both variants depend on merging the dispatcher work. After that, either scheduler can run it. Before that, Variant 2 can ship today with `once` for one repo, and I concede that sequencing point.

**A-002: QUALIFY.** Each workspace does need its own scheduler set-up under both variants. The difference is who does it. Cron's entry is made by the template at every boot (issue 515), with no person. An automation lives in Orca's user data, is created by the owner (N5), and whether it survives an image update is UNVERIFIED. So the assumption is true but hides the main cost difference.

**A-003: ACCEPT.** A 5-minute tick all day is reasonable for both. Both papers use `*/5 * * * *`, and Orca's help accepts a 5-field cron expression. A 5-minute cadence does raise the cost of Variant 2's per-tick run record (strength 6).

#### Per-point positions

| Point | Winner | Confidence | Evidence |
|---|---|---|---|
| C-001 starts an agent each run | Variant 2 on the narrow fact; it does not decide the choice | 80% | CLI help: any non-zero exit "skips the run"; Variant 1 Risk bullet 1 already concedes it. "Run now" still bypasses (help text) |
| C-002 fit to one dispatcher over many repos | Draw, slight edge Variant 2 | 55% Variant 2 | The precheck is any shell command, so an automation could call `run-all`; cron's only edge is that nobody creates it per host |
| C-003 outside dependencies | Variant 2, narrowly | 55% | Cron needs Coder 515 (open); but handoff doc line 26 shows the template needs a new `superclaude` build anyway, and the automation needs an owner step |
| C-004 failure modes that start a model | Variant 1 | 75% | CLI help: "Run now ... bypass the precheck"; `--prompt` and `--provider` required; Variant 2 Cost bullet 2 concedes |
| X-001 "starts an agent on each run" | Variant 2 | 85% | Same as C-001. Variant 1 already says it is true only at exit 0 |
| X-002 what an automation is bound to | Variant 2 | 65% | The precheck can run any command; the binding limits the agent workspace, not the shell command |
| X-003 manual set-up per host | Variant 1 | 75% | Variant 2 Cost bullet 4 against its fact 6; N5 and O3/O4 are cited by both papers, but `orchestrator.md` is not in the worktree I checked, so UNVERIFIED by me |

### Variant 2 Advocate (CLAY)
#### Round 1 statement: Variant 2 advocate (CLAY, Orca automation with a no-agent precheck)

Debate: D02 scheduler, cron or Orca automation. Round 1. Author role: advocate for Variant 2.
Date: 2026-11-20. Read-only run: no automation created or run, nothing written to GitHub.

#### Position

Variant 2 holds: the poll runs from one Orca automation whose precheck starts `superclaude issue-watch once` detached and exits 1. I claim three things and no more.

1. The owner's written reason against automations ("it starts an agent session with a prompt on each run", requirements line 18) is false for this pattern. Variant 1 admits this itself (its Risk, bullet 1).
2. The pattern is already on master and has run on Clay's host, so it is not speculative.
3. It needs nothing outside this repository, while cron needs Coder issue 515, which is open, so cron is not scheduling the watcher anywhere today.

I do not claim automations beat cron on every axis. Run now, the zero-setup goal and the direction of failure favour cron, and I say so below.

#### Steelman of Variant 1

The strongest version of Variant 1: a scheduler whose only job is "run this command every 5 minutes" should be one that cannot start a model. Cron cannot. An Orca automation can, by three routes: a click on Run now, `orca automations run`, or an edit that drops the `exit 1` (the precheck then exits 0 and a Claude session starts every 5 minutes). Orca's own help says so: "Run now in Orca and orca automations run intentionally bypass the precheck". The automation also has two required parameters it does not use (`--prompt`, `--provider`). Under cron nobody can fail by accident into "the scheduler started an agent".

Beyond that, Variant 1 is the owner's decided line (requirements R6 and R16, 2026-11-18). It matches the zero-setup goal: the template installs cron and writes the entry on every boot, so no person creates anything per host, whereas the automation is an owner-run step (O3, O4) and design N5 forbids the orchestrator from doing it. Cron was tested on this host (R21: a per-minute entry fired on time, `orca repo list` worked under an empty environment; handoff doc: `gh auth status` stayed logged in). It has a two-layer lock (`flock -n` plus the dispatcher's `loop_lock`, `dispatch.py` around line 154). And Variant 1 is honest about its own weak spot: it says its argument "must not lean on" the owner's sentence, and that "debated and rejected" is not backed by the debate folder.

What it genuinely gets right: the failure direction of a script-only automation is worse than cron's (a mistake spends tokens, where a cron mistake spends nothing), and the zero-setup goal is a real owner requirement that cron serves and an automation, today, does not.

#### Key strengths claimed (Variant 2)

1. The owner's blocker does not hold. Orca help, re-read today with `orca-ide automations create --help`: "Use --precheck to run a command only before scheduled runs; exit code 0 continues, any other exit, error, or timeout skips the run" and "Skips appear in Orca run history ... as skipped_precheck". Every failure of the precheck (crash, timeout, non-zero exit) skips. Only exit 0 continues. So the dangerous direction needs one specific mistake, and the design appends an explicit `; exit 1` after the detached start (`docs/designs/orchestrator.md:350`).
2. The pattern is on master and in use. `src/superclaude/skills/agent-work-report/SKILL.md:30` (master snapshot, read today): the waker automations "run the script as its precheck command, detached, and exits non-zero so Orca starts no agent and leaves no terminal (VERIFIED 2026-11-03)". `waker.py` comments record real firings (2026-11-04: the run opened 8 seconds after the wake line; 2026-11-18: a usage-limit error four minutes after it). Same host, same Orca, same shape. Cron has produced no firing of the watcher anywhere.
3. No cross-repo dependency. Cron's crontab is outside the persisted home volume and resets on an image update (R6), so cron needs the image change, the daemon start and a per-boot entry from `startup.sh` (Coder 515, open). On this host today `crontab -l` prints nothing and the cron daemon runs only because it was started by hand on 2026-11-18 20:20:37 (`ps`, read today). So "cron works" is shown for a hand-started daemon, not for the installed path.
4. The cron environment is a real cost Variant 1 pays. R21: cron's environment is only `PATH=/usr/bin:/bin` with no `~/.aienv`, so `orca`, `gh`, `superclaude` and `uv` are not found by name. The cron line therefore needs a PATH line and a hard-coded `--orca /home/coder/.config/orca/linux-orca-cli-shim/orca` (handoff doc, cron block). The precheck is `bash -lc` and the design sources `~/.aienv` and `~/.env` first (`orchestrator.md:350`); U6 already shows `command -v superclaude gh orca ccsession` finds all four in a login shell (`orchestrator.md:1264`).
5. The poll needs Orca anyway. It wakes sessions through `orca`, so a host where the Orca server is down cannot complete a poll under either scheduler. Variant 1's "no hidden dependency on Orca's scheduler semantics" protects against a failure the poll cannot survive anyway. (Whether the schedule fires while the Orca app is closed is UNVERIFIED; here the server runs headless.)
6. The unknowns have a plan. U6 and U7 are listed with checks (`orchestrator.md:1264-1265`); creation is `--disabled`; the 24-hour shadow run is a scheduled `--dry-run`, so the first runs do not use the Run now bypass (`orchestrator.md:966`). Orca also offers `--missed-run-grace-minutes` and `orca automations runs --id` for history (read from help today).

#### Weaknesses identified in Variant 1

1. Cron schedules nothing that matters today. The Coder issue 515 work (package, daemon start, per-boot entry, `flock -n`, log) is open and in another repository; Variant 1's own Cost says so. Its R21 evidence is a hand-started daemon and a test entry that was removed (R21: "Test entry removed, crontab is empty again"). My `ps` and `crontab -l` today agree.
2. The command Variant 1 schedules is not shipped. The handoff doc says the `/usr/local/bin/superclaude` on this machine does not list `run-all`. `run-all` lives only in the unpushed branch `claim-handoff-planb`. Master and the PR 686 design have `once`. Variant 1 argues for a scheduler of a command that cannot yet run from a clean install.
3. "The log holds the outcome" is thin. Cron discards a job's exit code; the cron line writes stdout and stderr to `issue-watch.log`, and `flock -n` exits silently when it loses the race. Variant 2 has the same weakness (outcome in `audit.jsonl` and `poll.log`), so this is a wash, not a cron advantage. Variant 1's fact 7 (Orca history shows only `skipped_precheck`) is true, but under cron too nothing shows "the poll crashed" unless a person reads the log.
4. "A scheduler that cannot start an agent" is true of cron but not of the system. The poll itself starts agent sessions (claims, wakes) through Orca. That risk lives in the poll's own launch guards and is the same under both schedulers. The automation's only extra exposure is the Run now click and a dropped `exit 1`.
5. The owner's reason is partly wrong and Variant 1 knows it. Requirements line 18 says an automation "starts an agent session with a prompt on each run"; Variant 1's Risk concedes this is "true only when the precheck exits 0". Its Risk bullet 2 adds that the debate folder covers one dispatcher against one entry per project and assumes cron. So the cron decision was not tested against the precheck pattern Clay proposed on 2026-11-18 17:00:32.
6. Variant 1's own source disagrees with itself about this host. Requirements line 18: "This host has no `crontab` command"; R21: cron 3.0pl1 installed. Today `/usr/bin/crontab` and `/usr/sbin/cron` both exist. Which statement was true when, I cannot tell (UNVERIFIED), so the "tested on this host" evidence has an unexplained gap.

#### Concessions

1. Run now and `orca automations run` bypass the precheck and start a real Claude session in the orchestrator workspace (Orca help, quoted above). Cron has no such hazard. My mitigation is partial: a scheduled shadow run, and (my suggestion, not in the design) a prompt that tells the agent to do nothing and stop, so a stray click costs one idle turn. The design's current prompt, "unused: the precheck never lets a run start", gives a session no instruction either way.
2. Dropping `exit 1` turns a quiet automation into a token burn every 5 minutes. The design checks this only by observation (`orca automations runs`, the shadow run). Cron has no equivalent exposure.
3. Creating the automation is an owner step (O3, O4) and N5 forbids the orchestrator from doing it (`orchestrator.md:762`, `:1025`). Against R1 and R17 ("nothing in the setup is manual") this is a real mark against Variant 2, unless a template startup step can run `orca automations create`, which I have not verified (UNVERIFIED).
4. Official documentation describes automations as prompts run through an agent and documents the precheck only as a gate. The script-only use rests on the gate semantics, the master skill's VERIFIED note and about two weeks of waker runs. The `*/5` step syntax (U7) and PATH in the precheck shell (U6) are not verified on this host: `orca-ide automations list` today prints "No automations found".
5. Variant 2's paper is loose: "Nothing outside this repo has to change" sits beside "Creating the automation is an owner step". These are two claims (no change to another repository, versus one owner command per host), but the wording invites the reading Variant 1 gave it (X-003).
6. Cron is the owner's recorded decision (R6, R16, 2026-11-18). If the owner reaffirms it knowing the precheck semantics, I have no further argument.

#### Shared-assumption responses

- A-001: QUALIFY. The scheduler choice does not change the poll command in principle: a precheck can run `run-all` as easily as `once`, and cron can run `once`. But the papers do compare different commands (`once` from the PR 686 design, `run-all` from the unpushed branch), so part of the contest (C-002, C-003) is really "which command ships", not "which scheduler". Neither paper states this. I accept it as a gap in both and ask that the verdict be written per command.
- A-002: QUALIFY. Both schedulers need one set-up per host: one crontab per workspace boot (automatic if Coder 515 lands) or one automation per Orca host (manual today; automatic only if a template startup step can create it, UNVERIFIED). The unit is the same, but the costs are not equal: cron's can be automated by the template, the automation's currently cannot.
- A-003: ACCEPT. A 5-minute tick fits the poll's 240-second deadline (`orchestrator.md:322`), and both sides quote the same cadence. The automation also has `--missed-run-grace-minutes`, and cron has no catch-up; neither changes the cadence.

#### Per-point positions

| Point | Winner | Confidence | Evidence |
|---|---|---|---|
| C-001 (does an automation start an agent every run) | Variant 2 | 90% | Orca help: "any other exit, error, or timeout skips the run"; `SKILL.md:30` VERIFIED 2026-11-03; Variant 1 Risk bullet 1 concedes "true only when the precheck exits 0". |
| C-002 (fit to one dispatcher over many repos) | Variant 2, narrowly | 60% | The precheck is arbitrary shell; the `--workspace` binding names the workspace of a run that never starts. The design routes repos from `repos.yaml` (`orchestrator.md:37`, `:59`). Residual: whether the precheck's working directory matters is UNVERIFIED, and `run-all` itself is unmerged. |
| C-003 (dependencies outside this repo) | Variant 2 | 55% | Cron needs Coder 515 (open) and a per-boot entry; crontab resets on image update (R6). Variant 1 wins the sub-point "zero manual setup" (see X-003). Net: Variant 2 on cross-repo dependency, but the owner's R1 and R17 weigh the other way. |
| C-004 (failure modes that start a model) | Variant 1 | 70% | Run now and `orca automations run` bypass the precheck (Orca help); a dropped `exit 1` starts an agent every 5 minutes. Cron has neither. My mitigations (shadow run, harmless prompt) reduce but do not remove it. |
| X-001 (automation starts an agent on each run) | Variant 2 | 90% | Same evidence as C-001; the CLI help settles the exit-1 case. |
| X-002 (what an automation is bound to) | Variant 2 | 65% | The binding selects the workspace of an agent run that the precheck prevents; the poll reads repos from its own config. Variant 1's "bound to one repo" is true of the option and irrelevant to a script-only precheck. |
| X-003 (manual per-host set-up) | Variant 1 | 60% | Design O3, O4 and N5 make creation an owner step; my Cost section says so. The "nothing outside this repo" sentence is true only for repository changes, not for set-up effort. |

## Round 2: Rebuttals

### Variant 1 Rebuttal
#### Round 2 rebuttal: Variant 1 advocate (OURS, cron with one dispatcher), debate D02

Role: advocate for Variant 1. Opponent: Variant 2 (CLAY, Orca automation with a no-agent precheck).
Date: 2026-11-20. Read-only run: no automation created or run, nothing written to GitHub.
Read first: variant-1-original.md, variant-2-original.md, diff-analysis.md, rounds/round1-advocate-1.md, rounds/round1-advocate-2.md.
Checked myself today: `ps`, `crontab -l`, `orca-ide automations list`, `dpkg -l cron`, `/var/log/apt/history.log`, `git log` and `ls-remote` in the worktree `claim-handoff-planb`, the code of `run-all` and `loop_lock`, the snapshots in `/home/coder/.cache/ic-snap-20261120/`, and the open Coder issue 515 (read with `gh`, no write).

#### Summary of where I stand

The opponent is right on four of the five facts I was asked to check, and I say so below. My Round 1 lean (about 60% that cron is the better choice) drops to about 50%. It is now a toss-up on the evidence, and it is the owner's decision (R6, R16), not a point either of us can win by argument. What survives of Variant 1 is narrow: cron cannot be started by a click, and a cron mistake spends no tokens. What does not survive: "cron is tested on this host" as a proof of the install path, "cron's log is better" as an advantage, and "a scheduler that cannot start an agent" as a statement about the whole system.

#### Responses to criticisms

##### Weakness 1 (cron schedules nothing today; the daemon runs only because it was started by hand and the crontab is empty)

Verified, and the opponent is right. Evidence from this host today:

- `ps` shows `/usr/sbin/cron`, owner root, parent PID 1 (`./coder agent`), start time Wed Nov 18 20:20:37 2026, up 1 day 7 hours. It is the hand-started daemon from R21.
- `crontab -l` prints nothing. The test entry was removed (R21 says so).
- New fact, worse than the opponent knew: cron is not in the image at all. `/var/log/apt/history.log` shows `Commandline: apt install cron`, `Requested-By: coder (1000)`, on 2026-11-18 18:40:49. `dpkg` and file birth times agree (`/usr/sbin/cron` born 2026-11-18 18:40). Coder issue 515 (open, last comment 2026-11-18 18:45) says the same: "cron is now installed there ... no cron daemon is running". So the image needs a change, which is exactly issue 515.
- There is no syslog and no `/var/log/cron*` on this host, so cron leaves no record of its own firing.

What I keep: R21 tested the mechanism (cron fires on time, `orca repo list` works with `PATH=/usr/bin:/bin`, `gh auth status` stays logged in), and that part does not depend on how the daemon was started. What I give up: R21 does not test the install path (package in the image, daemon from `startup.sh`, entry recreated each boot). That path is issue 515, and it is not done. I stated "the scheduler is already tested on this host" in Round 1 and that was too strong. The honest version is "the mechanism is tested, the install path is not".

Counterweight, not a rescue: the opponent's own evidence is the same kind. No automation exists on this host (`orca-ide automations list` prints "No automations found" today). Its two weeks of waker runs are on Clay's host and are read from the design.

##### Weakness 2 (the command Variant 1 schedules, `run-all`, is not shipped)

Verified. `run-all` is at `src/superclaude/cli/issue_watch/cli.py:432` in the worktree `claim-handoff-planb`, on branch `ironbelly/issue-watcher-zero-setup-plan`. `git ls-remote --heads origin` finds no such branch on the fork. The branch has no upstream, three commits ahead of `origin/master`, and uncommitted changes. The master snapshot's `issue_watch/cli.py` has `once`, `status`, `check-config`, `init-state` and `reset`, with no `run-all` and no `dispatch.py`. The PR 686 snapshot (`pr-p`) is the same. The `pr-a` snapshot adds `repos.py`, `route.py` and `wake.py` but no `dispatch.py` either. The handoff doc (line 26) says the installed `/usr/local/bin/superclaude` does not list `run-all`.

What this means for the scheduler choice: very little, and I think the opponent half agrees. A precheck is any shell command, so an automation can run `run-all` as easily as cron can run `once`. The gap belongs to the poll, not the scheduler, and it hits both variants the same way: both need a new build in the template before the command exists. Where it does matter is the diff-analysis point A-001. The two papers compare different commands (`run-all` against `once` plus `repos.yaml`), so C-002 and C-003 are partly "which poll ships". I accept the opponent's request to write the verdict per command. What I will not accept is the inference that unshipped `run-all` weakens cron specifically. It weakens the whole zero-setup plan equally.

##### Weakness 3 ("the log holds the outcome" is thin; cron discards the exit code; a wash)

Mostly verified, so mostly conceded. Facts:

- Cron does not keep a job's exit code. The cron line sends output to `~/.aidev/logs/issue-watch.log` with `>> ... 2>&1`, so the log is the only record, and it is only as good as the lines the command prints.
- `run-all` does print one line per repo and one overall line every tick (`_report` in `cli.py`: `sweep: clean`, `sweep: waiting until ...`, `sweep: unhealthy (a child failed)`, `sweep: error ...`). So a finished tick does leave a line, and an unhealthy one says so. That part of my claim holds.
- A tick that loses the outer `flock -n` leaves nothing at all (flock exits silently). A tick that cron never fired also leaves nothing. With no syslog on this host, "cron stopped" and "nothing to do" look the same in the log, except that a normal tick prints a `sweep:` line, so a long gap in the log is the signal.
- The precheck pattern has the same outcome record: the design redirects the poll to `<state_dir>/poll.log` and `audit.jsonl`. On outcome, it is a wash, as the opponent says.
- The opponent's pattern does have one thing cron lacks: Orca history gets a `skipped_precheck` row at every firing. That is a heartbeat for the scheduler (not for the poll). I should have credited it. Cost side: 288 rows a day, retention unknown (UNVERIFIED).

So my Round 1 strength 2 ("every tick leaves a plain record") shrinks to "a finished tick leaves a plain line and a plain exit code for anyone who runs the command by hand". Not an advantage over the poll log under the precheck.

One thing I checked that helps no one but is worth recording: the two lock layers do not collide. The outer lock is `~/.aidev/issue-watch.lock` (from `flock`), the inner one is `<state dir>/issue-watch/run-all.lock` (`dispatch.py:154-171`). Different files, so the cron line will not deadlock itself. The inner lock only matters when a person runs `run-all` by hand while cron's run is going.

##### Weakness 4 ("a scheduler that cannot start an agent" is moot because the poll itself starts agents under both)

Half right. As a sentence about the system it is wrong, and I withdraw it in that form. The poll claims issues and launches coordinators and workers through Orca under both schedulers.

What survives is a difference in kind, not in whether agents exist:

- Agent starts by the poll are gated: an approved issue, the predicates, one launch per sweep (R26), and a launch guard that allows one fixed prompt. They happen only when there is work.
- An agent start by the scheduler layer is ungated and unconditional. If the precheck ever exits 0, or someone clicks Run now, a Claude session starts in the orchestrator workspace with the unused prompt, and with a dropped `exit 1` it repeats 288 times a day. Orca's help on this host says it in one line: "Run now in Orca and orca automations run intentionally bypass the precheck". The usage line also requires `--prompt` and `--provider`.

So the right claim is: no mistake at the scheduler layer can start an unguarded model run under cron. It is a real but narrow safety margin. Cost of the failure is bounded for one click (one idle session), and large only for the dropped `exit 1`. The design appends `exit 1` by hand in the command text (`orchestrator.md:350`), and a scheduled shadow run would catch a dropped one on the first fire. I rate this risk as low-probability. It still points the right way, and the opponent concedes the direction in their Concessions 1 and 2.

##### Weakness 5 (the owner's reason is partly wrong and Variant 1 knows it; the cron decision was not tested against the precheck pattern)

Conceded in full. I said so in my Round 1 Concession 1 and 5, and in Variant 1's own Risk section. I add one verified detail: the only text about automations in the owner's requirements is line 18, and it was written in the single commit `d0a0a433b` (2026-11-19), a day after Clay's #450 comment (2026-11-18 17:00:32, per the opponent's fact 9, which I did not re-read). I did not find the precheck pattern weighed anywhere in the owner's folder. What this proves is that the decision was not tested against the pattern. It does not prove the decision is wrong. The owner can still choose cron knowing the semantics, because the real reasons (zero setup R1, one dispatcher R16, no click path) do not need line 18's sentence.

##### Weakness 6 (requirements line 18 says no `crontab` command; R21 says cron 3.0pl1 is installed)

Resolved: both statements are true, at different times. Line 18 ("This host has no `crontab` command") was true until 2026-11-18 18:40:49. `apt install cron` ran at 18:40:49 as the user `coder`, and R21 describes the host afterwards ("the package is installed ... the daemon was not running ... tested 2026-11-18"). The two lines were written into one file in one commit (`d0a0a433b`, 2026-11-19) with no note that they describe different moments, which is why they read as a contradiction. Today `/usr/bin/crontab` and `/usr/sbin/cron` exist, as the opponent saw.

This does not rescue "tested on this host" as evidence for the install path. It makes the install-path gap clearer: the package got onto this host by a person typing `apt install`, and nothing in the image or `startup.sh` does it yet. I am recording that as the sixth item I concede.

#### New evidence

Everything below was read or run today, read-only.

1. Cron came from a hand `apt install` (18:40:49 on 2026-11-18, `Requested-By: coder`), the daemon from a hand start (20:20:37, parent PID 1), and the crontab is empty. So today cron schedules nothing and the image has no cron. This confirms the opponent's Weakness 1 and goes slightly beyond it.
2. Orca, by contrast, is already in the image and running: `/opt/Orca/orca-ide ... --serve` has been up since 2026-11-18 15:02:30 with user data in `/home/coder/.config/orca`. That supports the opponent's point that the scheduler is part of a runtime the poll needs anyway. It is still unknown whether the schedule fires with no GUI window (the server is headless, and I could not confirm where the scheduler lives).
3. `run-all` exists only in the local worktree. No remote branch has it and neither master nor the PR 686 or `pr-a` snapshots contain it.
4. `run-all` prints a `sweep:` line every tick and exits 0 or 1 (75 when the inner lock is held). Cron keeps the line (through the redirect) and drops the exit code. No syslog on this host.
5. Outer and inner locks use different files (`~/.aidev/issue-watch.lock` and `<state dir>/issue-watch/run-all.lock`), so the two layers are safe together.
6. The automation CLI help still says what Round 1 said: `--prompt` and `--provider` are required, a non-zero precheck skips the run and records `skipped_precheck`, Run now and `orca automations run` bypass the precheck, and `--missed-run-grace-minutes` exists. Cron has no catch-up for a missed tick.
7. Coder issue 515 is still open and has had no comment since 2026-11-18 18:45.

#### Concessions

1. "The scheduler is already tested on this host" is true for the mechanism only. The install path (image package, daemon at boot, per-boot entry) is untested and sits in an open issue in another repository (Weakness 1).
2. The cross-repo dependency is real and cron-specific as to the scheduler: the image has no cron today. My Round 1 offset (the template needs a new `superclaude` build anyway) is valid but only partly cancels it, because the opponent's route needs no new daemon, package or boot step.
3. "A scheduler that cannot start an agent" is not a property of the system, since the poll starts agents under both. I keep only the narrower claim in the Weakness 4 section.
4. On outcome record, cron is not better than the precheck pattern. Cron drops the exit code and leaves nothing for a lost lock or a missed tick. The precheck pattern also gives Orca history a heartbeat row per firing.
5. The sentence in my Round 1 position that a manual create step "per host" is the main cost of Variant 2 is weaker than I made it. Design N5 forbids the orchestrator from creating an automation; it does not say a template boot script cannot. I did not find or test any way to do it, so it remains UNVERIFIED either way, but it is a design rule, not a proven technical limit.
6. Requirements line 18 and R21 do not contradict each other; they describe different times. I leaned on neither, but I should have noticed the 18:40 install and drawn the "not in the image" conclusion myself.
7. Carried over from Round 1 and unchanged: the owner's sentence is true only for exit 0, "debated and rejected" is not backed by the folder, `*/5` is accepted by the help text in all likelihood, and the six-field FU-2 line is wrong for cron 3.0pl1 (not run here).

#### Updated per-point positions

| Point | Winner | Confidence | Change from Round 1 | Reason |
|---|---|---|---|---|
| C-001 does an automation start an agent each run | Variant 2 (on the narrow fact only; it does not decide the choice) | 90% | up from 80% | Help text: any non-zero exit skips. Variant 1's Risk already says so. Run now still bypasses. |
| C-002 fit to one dispatcher over many repos | Variant 2, slightly | 55% | unchanged | A precheck is any shell command, so it can run `run-all`. Cron's edge is only that nobody creates it per host. Also shared with A-001: `run-all` is unshipped. |
| C-003 dependencies outside this repository | Variant 2 | 60% | up from 55% | The image has no cron (hand `apt install`), the daemon is hand-started, issue 515 is open. Offsets: the template needs a new build for either route, and the automation needs an owner step today. |
| C-004 failure modes that start a model | Variant 1 | 70% | down from 75% | Run now and a dropped `exit 1` are real and cron has neither. The harm per click is one idle session, and a scheduled shadow run would catch a dropped `exit 1` early, so the margin is small. |
| X-001 "starts an agent on each run" | Variant 2 | 90% | up from 85% | Same as C-001. |
| X-002 what an automation is bound to | Variant 2 | 65% | unchanged | The binding picks the workspace of a run the precheck prevents; the shell command can do anything. |
| X-003 manual set-up per host | Variant 1, narrowly | 55% | down from 75% | O3, O4 and N5 make creation an owner step today. But N5 binds the orchestrator, not a boot script, and the cron route has its own unfinished boot work (issue 515). Owner's R1 and R17 still weigh toward whichever route is fully automatic, and only cron has a tested path to that. |
| A-001 scheduler choice does not change the poll command | Neither; the opponent for naming the gap | 60% Variant 2 | moved from "qualify" to agreeing | Both papers compare different commands. The scheduler is independent in principle, but the verdict should be written per command. `run-all` ships nowhere but one unpushed local branch. |
| A-002 every workspace needs its own scheduler set-up | Variant 1, narrowly | 55% | down from the Round 1 framing | Cron's set-up can be done by the template at boot (tested mechanism, install path open). An automation's boot-time creation is unverified, and so is its survival of an image update. |
| A-003 a 5-minute tick all day is right | Draw | 60% agreement | unchanged | Both use `*/5`. Variant 2 adds up to 288 `skipped_precheck` rows a day, with retention unverified. |

Overall: about 50% that cron is the better scheduler, down from about 60%. I would not call a win for either side on the evidence now in the folder. If the owner keeps R6, nothing here is a reason to overturn it; if the owner wants the image untouched, Variant 2 is a fair route.

#### What would change my mind

One fact: a scheduled (not Run now) run of a `*/5 * * * *` automation with a `; exit 1` precheck, created `--disabled` first and then enabled on this host, firing for 24 hours under the headless Orca server, with the history showing only `skipped_precheck` rows, no session started, and the automation still present after an Orca server restart.

- If that holds, I move to Variant 2 as the better choice (about 65%), because the one cron advantage that rests on a tested path (R21) would no longer outweigh cron's open image work (issue 515).
- If the automation stops firing when no window is open, is lost on restart, or fills the history without bound, I move back to Variant 1 (about 70%).

A second, smaller fact would also move me: whether `orca automations create` can be run by a template boot script (idempotently, before the first tick). If yes, X-003 goes to Variant 2.

### Variant 2 Rebuttal
#### Round 2 rebuttal: Variant 2 advocate (CLAY, Orca automation with a no-agent precheck), debate D02

Role: advocate for Variant 2. Opponent: Variant 1 (OURS, cron with one dispatcher).
Date: 2026-11-20. Read-only run: no automation created or run, nothing written to GitHub, one output file.
Read first: variant-1-original.md, variant-2-original.md, diff-analysis.md, rounds/round1-advocate-1.md, rounds/round1-advocate-2.md, rounds/round2-advocate-1.md.
Checked myself today (all read-only): `orca-ide automations create --help`, `edit --help`, `runs --help`, `list --json`; `ps`; the files under `/home/coder/.config/orca` (names and key names only); the installed Orca code in `/opt/Orca/resources/app.asar` and `app.asar.unpacked` (read by byte offset, nothing extracted); the master snapshot `docs/designs/orchestrator.md` (4.8, 5.9 N5, 12) and `agent-work-report/SKILL.md:30`; the official page https://orca.dev/docs/cli/automations.

#### Summary of where I stand

The opponent's Round 2 is fair and I concede most of it. My own Round 1 lean was "Variant 2 on cross-repo dependency and on the owner's stated reason, Variant 1 on failure direction and zero-setup". After checking the five asked points, two of them move toward Variant 2 (retention is capped, survival is likely) and two stay with Variant 1 (the exposure exists, and nobody has fired an automation on this host). The honest overall position: about 55% that the automation is the better scheduler on technical merits, with the first real firing on this host still missing. The owner's decision R6 stands until someone shows the owner the precheck semantics. That is still a toss-up, and I do not claim a win.

#### Responses

##### (a) The narrowed safety claim: "no scheduler-layer mistake can start an unguarded model run under cron"

I accept the sentence as true. Cron has no Run now button and no exit code that starts a model. What I dispute is how much it is worth. Three checks:

1. What a Run now or `orca automations run` does. I confirmed in the installed code that `runPrecheck` returns nothing at all for any run whose trigger is not `scheduled` (it tests `r.trigger!=='scheduled'||!n.precheck` and returns null). So a manual run really does skip the gate, as the CLI help says. The result is one Claude session in the orchestrator workspace with the prompt "unused: the precheck never lets a run start". It is one idle turn, bounded. It needs a person to click, or an agent with the Orca CLI to type `orca automations run`. The design closes the second route for the orchestrator: N5 puts `orca automations create`, `edit`, `remove` and `run` on the denylist that `refuse()` applies to every verb (`orchestrator.md:762`, `:767`). It does not close it for a model typing a command by hand (the design says so under "Stated limits", line 769). So the route exists but is narrow.
2. A dropped `exit 1`. This is the larger one: the precheck then exits 0 and a session starts at every tick, up to 288 a day. How likely is it? The `exit 1` is written once, at create time, and is typed by hand in the command text (`orchestrator.md:350`). The only planned edit of the command is the switch-on step, which removes `--dry-run` from it (`orchestrator.md:354`). That one edit is where the mistake would happen. Detection is quick: the first scheduled tick after switch-on shows a new terminal in the workspace and a `dispatched` row instead of `skipped_precheck` in `orca automations runs --id`. That puts the worst case at a few sessions before somebody looks, not 288. I rate this low probability and bounded loss, but I do not call it zero.
3. Things in the design and in the Orca code that shrink it. From the code: a precheck that crashes, times out, or cannot resolve its workspace is treated as a failed precheck and the run is skipped. I read that branch: when the workspace target does not resolve, `runPrecheck` returns a failure result built from the error, not a pass. So every failure of the gate fails closed. Only a clean exit 0 starts an agent. From the design: the shadow run is a scheduled one, so the first runs never use the bypass (`orchestrator.md:354`).

Two cheap improvements that are not in the design today, offered as suggestions and not as facts about master:

- Replace the hand-typed `...; exit 1` with a fixed command such as `superclaude issue-watch tick`, whose code starts the poll detached and then returns 1 on every path, with a unit test that asserts it. The "dropped `exit 1`" mistake then cannot happen by editing the command, because the command never needs editing. The `--dry-run` choice moves into the poll's own config.
- Make the automation's prompt an instruction ("do nothing and stop") instead of "unused". A stray Run now then costs one short reply.

One more comparison that the opponent's claim leaves out: a dropped `--dry-run` during the shadow period is the same kind of edit mistake under cron, and it would wake real agents there too. So the extra exposure of the automation is only the unguarded idle session, not edit mistakes in general.

Size of the risk, my honest reading: a real but small margin in cron's favour. It does not decide the choice. I keep C-004 with Variant 1, at a lower confidence than in Round 1.

##### (b) N5 binds the orchestrator, not a boot script; can a template boot script create the automation idempotently?

Agreed on the first half: N5 is a rule about what the orchestrator may run, not a technical limit. My Round 1 sentence that creation is "an owner step" described the design's O3 and O4, not what is possible. I checked the second half read-only:

- The CLI has no "create if absent" flag. `orca automations create --help` lists no creation key. The Orca code does have a `creationKey` parameter: when a create call carries a key that an existing automation already has, the existing one is returned and nothing new is made. But that key exists only in the internal call (`shared/rpc-contract/automation-params.js:150`), and I found no CLI flag that sets it. So I cannot count on it.
- Names are not unique. The create path does not check the name, so a second `create --name orchestrator-poll` would make a second automation.
- A boot script can still be idempotent in the ordinary way: `orca automations list --json`, look for `name == "orchestrator-poll"`, and create only when it is absent. `list --json` works here today (it returns an empty `automations` array). One boot script, run once per boot, makes the check-then-create race harmless in practice. If it did create two, each tick would start two polls and the second would exit 75 on the poll's own lock (`record.py:382`), so the failure is quiet.
- What the script needs that cron does not: the Orca server must be up when it runs (it talks to the Orca runtime), and `--workspace path:<orchestrator-repo>` must name a worktree that already exists in Orca. Cron needs neither. So a boot script is possible but has an ordering condition in `startup.sh` that nobody has written or tested.
- What it saves: if the automation survives an image update (see (c)), the script is a safety net that normally finds the automation already there. Cron's entry has to be recreated at every boot.

Net for X-003: the design's "owner step" is a design choice, not a wall. But no such script exists, and the opponent is right that "zero setup" is proven today for neither route. I move X-003 from 60% Variant 1 to a draw, 50%.

##### (c) Where the automation is stored, and does it survive an Orca restart or an image update

Read-only findings:

- Storage. Automations are part of the profile state: `/home/coder/.config/orca/profiles/local-default/profile-state.db` (an SQLite database with a write-ahead log; the older `orca-data.json` in the same folder still has `automations` and `automationRuns` keys, both empty arrays, and a `sqlite-export` from 2026-10-27 shows the move). The Orca code writes each created automation into the state and flushes it at once (`state.automations=[...]` then `flush()`), and each run row the same way.
- That folder is on the persisted home volume. `/home/coder` is its own device (`/dev/sdb`, ext4, 1.3 TB), and Orca's program is on the image side at `/opt/Orca`. The proof that this folder outlives image updates is in its own dates: files in `~/.config/orca` date from 2026-10-24 and 2026-10-27, while the installed `app.asar` is from 2026-11-08 and the running server started 2026-11-18 15:02:30 (version `1.4.245-aidev02`). The profile and its repo list survived at least one program update and several restarts. Automations live in the same store, so they should do the same. I did not create one to test it, so this stays an inference. It is stronger than Round 1, because it rests on the folder's own history, not on the text of issue 515 alone.
- Restart behaviour. On start, the scheduler recomputes from the stored `nextRunAt`. A run that was due while the server was down is run once if it is inside the missed-run grace window, otherwise recorded as `skipped_missed`. The create path defaults that window to 720 minutes (`missedRunGraceMinutes ?? 720`), and `--missed-run-grace-minutes` sets it. So after a restart there is catch-up. Cron has none.
- Also noted: the build has code that carries "dormant" automations across an Orca-managed upgrade (`orcad-migration-dormant-automation-validation.js`). I read it only to see that upgrades are expected to keep automations. I did not test one.

So (c) goes to Variant 2 at about 65%: stored on the persisted volume, with no observed loss, and not tested by me.

##### (d) The 288 `skipped_precheck` rows a day, retention unknown

Retention is now known, from the installed code. The function that prunes run history keeps the newest 100 runs in a finished state per automation, and it is called with that default at load and every time a run row is created (`Uoe(e, t=100)`; I found three call sites and none passes another number). Pending and running rows are kept besides. Consequences:

- The history cannot grow without bound. At 12 ticks an hour, 100 rows cover about 8 hours and 20 minutes. Storage is a non-issue.
- It also means the Orca history is a short heartbeat, not a record. Over a weekend it keeps nothing of Friday. So my Round 1 line "Orca keeps run history" must not be read as an audit trail. The record of what the poll did stays in `audit.jsonl`, `poll.log` and `issue-watch status`, exactly as the design says, and the opponent is right that under both routes a person must read those.
- The 2 writes per tick (create the row, then mark it skipped) are small. The profile database's write-ahead log is already 4 MB and busy with terminal state.
- What I did not check: how the Orca desktop table shows 100 identical `skipped_precheck` rows (noise in the UI). The waker automation fires twice a day, so "VERIFIED 2026-11-03" does not cover this cadence, as the opponent said. Retention is bounded, but "works at 288 a day" is still unobserved.

##### (e) Does the Orca schedule fire with no GUI window?

Evidence, none of it a firing:

- The official page does not say. I fetched https://orca.dev/docs/cli/automations: it says schedules "reside on the local computer or supported connected Orca hosts", gives a 30-minute missed-run grace example, and states no retention. It does not say whether a schedule runs after the window is closed or Orca is quit, and it does not describe headless operation. So the documentation is silent, as I said in Round 1.
- The installed code is more informative. The scheduler is a class in the main process that runs `setInterval(evaluateDueRuns, 60000)` (`tickMs` defaults to 60 000 ms). It is started with `start()` and does not wait for a window. The precheck runs in that same main-process path (`runPrecheck`, then the run is marked `skipped_precheck` before any dispatch). The part that needs a renderer is the dispatch of an agent: `canDispatch` is true when a renderer is ready or when the build has a `headlessDispatcher`, and the build has one, switched on by a `headless` option, with a separate keep-alive routine for headless mode. So the program is written to run automations without a window, including the dispatch.
- This host: `ps` shows the server `orca-ide --serve --serve-json --serve-port 6768` (pid 476, since 2026-11-18 15:02:30), a virtual display `Xvfb :99` that Orca itself started, and zero `--type=renderer` processes. So there is no window and no page rendering at all. That is the setting the code's headless path is built for.
- What I could not confirm: which switch turns the `headless` option on for `--serve`. I searched for it and found only an end-to-end test variable (`ORCA_E2E_HEADLESS`) near it, so the link between `--serve` and the headless dispatcher is by inference. If it is off, then with no renderer `canDispatch` is false for every tick, and the scheduler may record `skipped_unavailable` instead of running the precheck. That would stop the poll silently. This is the one real unknown that decides whether the automation works here at all. Round 1 called it "UNVERIFIED"; it is now "supported by the code, not run".

Position on (e): likely yes, untested. This is the point where I am most exposed, and I say so.

#### New evidence

All read-only, today.

1. Run history is capped at 100 finished runs per automation (installed code, `Uoe(e,t=100)`, three call sites, none overrides). About 8 hours 20 minutes at a 5-minute tick.
2. The scheduler is a 60-second main-process timer, not a renderer task. The precheck is evaluated and the run marked `skipped_precheck` before any dispatch to an agent. A failed workspace lookup also counts as a failed precheck and skips.
3. A manual run bypasses the precheck in code, not only in the help text (`runPrecheck` returns nothing unless the trigger is `scheduled`).
4. Missed-run catch-up exists: policy `run_once_within_grace`, default window 720 minutes, `skipped_missed` beyond the window plus two ticks.
5. `creationKey` exists in the internal RPC but not as a CLI flag; automation names are not unique. A boot script would have to use `list --json` then `create`.
6. Storage is `profiles/local-default/profile-state.db` under the persisted home volume; the folder's file dates (2026-10-24 and 2026-10-27) predate the installed program (2026-11-08) and the running server (2026-11-18), so the profile has survived at least one update.
7. This host: Orca server headless with a virtual display and no renderer process. `orca-ide automations list --json` returns an empty list, so no firing evidence exists here for either route.
8. The master design's own treatment of the exposure: N5 lists `orca automations run` as refused for orchestrator verbs (`orchestrator.md:762`), and the shadow run is a scheduled one (`:354`). No master file I read mentions the Run now bypass in the work-report skill (`SKILL.md:30` has the VERIFIED note and the exact command, and nothing about a click).
9. Process note: one of my read commands printed the contents of `orca-runtime.json`, which includes a local auth token; my redaction pattern did not match. The token is in my tool output only. I did not copy it anywhere and it is not in this file. It is a local-socket token of this Orca instance; the owner may want to know it was shown in a transcript.

#### Concessions

1. The opponent's narrowed safety claim is true as written. Cron has no scheduler-layer path to an unguarded model run. I only dispute its size.
2. "Run now" bypasses the precheck in the code, not just in the help text. The design's prompt gives that session no instruction. My two improvements (a fixed always-exit-1 command, and a "do nothing" prompt) are not in the design.
3. The 288-rows-a-day concern is answered on storage but not on usefulness: Orca keeps only about 8 hours. It is a heartbeat, not an audit trail. The poll's own outcome is in `audit.jsonl` and `poll.log` under both routes.
4. N5 is a design rule, not a technical limit; a boot script could create the automation. But no boot script exists, it needs the Orca server up and the orchestrator worktree to exist, and it is not idempotent by flag, only by a list-then-create check. "Nothing outside this repo changes" in my Round 1 paper remains an overstatement for set-up effort.
5. No automation exists on this host and I observed no firing. The headless claim rests on reading code. The waker evidence is from Clay's host and is twice a day.
6. The image has no cron today (the opponent's `apt install` finding). That strengthens C-003 for Variant 2, but only a little: both routes need a new `superclaude` build, and the automation needs a creation step.
7. The owner decided R6 and R16 on 2026-11-18. Nothing here proves the owner wrong; it shows the stated reason was incomplete.

#### Updated per-point positions

| Point | Winner | Confidence | Change from Round 1 | Reason |
|---|---|---|---|---|
| C-001 does an automation start an agent each run | Variant 2 | 92% | up from 90% | Code and help agree: a scheduled run starts an agent only on exit 0; crash, timeout and unresolvable workspace all skip. Variant 1's Risk already says it. |
| C-002 fit to one dispatcher over many repos | Variant 2, narrowly | 58% | down from 60% | The precheck is any shell command and `--workspace` only sets its working directory. Residual: `run-all` is unpushed, so the real comparison is per command. |
| C-003 dependencies outside this repository | Variant 2 | 60% | up from 55% | No cron in the image (hand `apt install`, issue 515 open). Offsets: both routes need a new `superclaude` build, and the automation needs a creation step and an Orca-up ordering condition. |
| C-004 failure modes that start a model | Variant 1 | 65% | down from 70% | Run now and a dropped `exit 1` are real; cron has neither. The loss is one idle session per click, and a few at most for a dropped `exit 1` that the first tick shows. A fixed always-exit-1 command would remove the second one. |
| X-001 "starts an agent on each run" | Variant 2 | 92% | up from 90% | Same as C-001. |
| X-002 what an automation is bound to | Variant 2 | 70% | up from 65% | The binding gives the precheck its working directory; an unresolvable workspace skips, which is the safe direction. It does not limit what the shell command does. |
| X-003 manual set-up per host | Draw | 50% | down from 60% for Variant 1 | N5 binds the orchestrator, not a boot script; `list --json` then `create` is a workable idempotent step. But no such script exists and it has an ordering need that cron lacks. |
| A-001 scheduler choice does not change the poll command | Variant 2, for naming the gap | 60% | unchanged | Write the verdict per command: for `once` the automation can ship today; for `run-all` both routes wait for the unpushed branch. |
| A-002 every workspace needs its own scheduler set-up | Variant 2, narrowly | 55% | up from a qualified draw | The automation is stored on the persisted volume and should survive updates, so set-up is once per host. Cron's entry is rebuilt every boot (issue 515). Both can be automated; the automation's survival is inferred, not tested. |
| A-003 a 5-minute tick all day is right | Draw | 60% agreement | unchanged | Both quote `*/5`. Retention is capped at 100 rows, so the 288-a-day load is harmless for storage; the unobserved part is the UI view. |

Overall: about 55% that the automation is the better scheduler on the merits, resting almost entirely on points (c) and (e), which are inferences from files and code, not runs. About 45% that cron is, because it is the owner's decision and it has the one real safety margin.

#### What would change my mind

One fact: a `*/5 * * * *` automation with a `; exit 1` precheck, created `--disabled` and then enabled on this host under the present headless server, fires on schedule for at least one hour with only `skipped_precheck` rows, starts no session, and is still listed after an Orca server restart.

- If that holds, I move to Variant 2 at about 70%, and I would ask for the always-exit-1 command and the "do nothing" prompt as part of the design.
- If the scheduler records `skipped_unavailable` or nothing at all with no window open, or the automation is gone after a restart, I concede to Variant 1 outright (about 75%), because the whole case for the automation depends on it firing without a window.

A second, smaller fact would also move me: a template boot script that runs `list --json` then `create` and is shown to leave exactly one automation after two boots in a row. If that holds, X-003 goes to Variant 2.

## Round 2.5: Invariant Probe

Full table in `invariant-probe.md` (28 findings: 11 ADDRESSED, 17 UNADDRESSED; UNADDRESSED HIGH 2, MEDIUM 5, LOW 10). The orchestrator re-checked these facts read-only: `LOOP_CAP_S = 270.0` and `CHILD_TIMEOUT_S = 255.0` in `dispatch.py:52-53` (worktree `claim-handoff-planb`); `run-all` is at `cli.py:432` of that worktree only and appears nowhere under the master snapshot `src/`; the master design `orchestrator.md` has 0 matches for `run-all` or `issue-watch.d` and reads repos from `repos.yaml`; the cron daemon is pid 1169996 started Wed Nov 18 20:20:37 2026.

Blocking items (HIGH and UNADDRESSED):
- INV-023: `run-all` starts `once --config <file>` per repo with per-repo configs, while the PR 686 design reshapes `once` to one config with `orchestrator_repo` and `repos.yaml`. The two polls differ in contract. The verdict must say which poll the scheduler runs.
- INV-024: choosing cron alone does not give zero setup: Coder issue 515 open, a per-host `superclaude install --force`, the owner-created `Approved` org field, and Coder issue 516 (the `Coordinator` worktree) all remain. The scheduler does not decide zero setup.

MEDIUM warnings (do not block): INV-008 (nobody notices a silent scheduler failure under either route), INV-011 (a sweep can take up to about 525 s against a 300 s tick), INV-015 (`once` with `repos.yaml` does not auto-enrol a new project; `run-all` does), INV-017 (the automation is coupled to an orchestrator checkout path that can move), INV-020 (two workspaces for one user have separate locks).

## Scoring Matrix

Winner values: V1 = OURS (cron), V2 = CLAY (automation), Draw = no difference that matters. Confidence is the mean of the two advocates' Round 2 figures where both gave one.

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| S-001 | Draw | 90% | Same six sections; no effect on the decision. |
| S-002 | Draw | 90% | Both Risk sections are self-critical; no effect. |
| C-001 | V2 | 91% | CLI help: any non-zero precheck exit skips the run; installed code treats crash, timeout and unresolvable workspace as a skip; V1's own Risk concedes. |
| C-002 | V2 (narrow) | 56% | A precheck is any shell command, so an automation can run a dispatcher; but the polls differ in contract (INV-023), so this is a per-command question. |
| C-003 | V2 | 60% | Image has no cron (hand `apt install` 2026-11-18 18:40:49, hand-started daemon, empty crontab, issue 515 open). Offsets: both routes need a new `superclaude` build; automation needs a creation step. |
| C-004 | V1 | 67% | "Run now" and a dropped `exit 1` start a Claude session; cron has neither. Harm bounded (one idle session; a few at most), so the margin is small. |
| C-005 | Draw | 70% | Both advocates concede neither gives a better record of the poll's outcome; Orca keeps only 100 finished rows (about 8 hours 20 minutes). |
| C-006 | Draw | 70% | Cron: mechanism tested here, install path untested. Automation: pattern verified for the waker twice a day on another host, never fired here. |
| C-007 | V1 (narrow) | 55% | Script-only use is undocumented officially; V2 conceded it; the code supports it. |
| C-008 | Unresolved | 50% | V2 65% (profile on the persisted volume, files predate program updates, inferred); V1 did not accept it. Untested either way. |
| C-009 | Draw | 80% | Both list their open unknowns. |
| C-010 | V1 (doc fix) | 85% | The six-field FU-2 line is wrong for cron 3.0pl1 (not run here); both agree it is a doc defect, not a decision factor. |
| X-001 | V2 | 91% | Same evidence as C-001. |
| X-002 | V2 | 67% | The binding gives the precheck its working directory only; it does not limit the shell command. |
| X-003 | Unresolved | 50% | V1 55% (creation is an owner step in design O3, O4), V2 50% (N5 binds the orchestrator, not a boot script; a boot script could do list-then-create; none exists). |
| A-001 | Both: write the verdict per command | 60% | `run-all` is unpushed; `once` is the PR 686 poll. |
| A-002 | Unresolved | 50% | V1 55% cron, V2 55% automation; each route's boot step is unwritten. |
| A-003 | Draw | 60% | Both accept a 5-minute tick; sweep time can exceed it (INV-011). |

## Convergence Assessment
- Points resolved: 15 of 18 (unresolved: C-008, X-003, A-002)
- Alignment: 83.3%
- Threshold: 80%
- Taxonomy coverage: L1 (S-001, S-002, C-010), L2 (C-002, C-003, X-002, A-002), L3 (C-004, A-001): all covered
- Invariant gate: 2 HIGH UNADDRESSED (INV-023, INV-024) block convergence; Round 3 is not available at depth standard
- Status: BLOCKED_BY_INVARIANTS (reported as not converged for the return contract; status partial)
- Overall lean of the two advocates after Round 2: V1 advocate about 50% that cron is the better scheduler; V2 advocate about 55% that the automation is. Both state it is a toss-up and that the owner's recorded decision (R6, R16) stands unless one decisive fact appears: a scheduled `*/5` automation with a `; exit 1` precheck firing headless for 1 to 24 hours with only `skipped_precheck` rows, no session started, and surviving a server restart. That fact cannot be obtained read-only.
