# Round 2 rebuttal: Variant 1 advocate (OURS, cron with one dispatcher), debate D02

Role: advocate for Variant 1. Opponent: Variant 2 (CLAY, Orca automation with a no-agent precheck).
Date: 2026-11-20. Read-only run: no automation created or run, nothing written to GitHub.
Read first: variant-1-original.md, variant-2-original.md, diff-analysis.md, rounds/round1-advocate-1.md, rounds/round1-advocate-2.md.
Checked myself today: `ps`, `crontab -l`, `orca-ide automations list`, `dpkg -l cron`, `/var/log/apt/history.log`, `git log` and `ls-remote` in the worktree `claim-handoff-planb`, the code of `run-all` and `loop_lock`, the snapshots in `/home/coder/.cache/ic-snap-20261120/`, and the open Coder issue 515 (read with `gh`, no write).

## Summary of where I stand

The opponent is right on four of the five facts I was asked to check, and I say so below. My Round 1 lean (about 60% that cron is the better choice) drops to about 50%. It is now a toss-up on the evidence, and it is the owner's decision (R6, R16), not a point either of us can win by argument. What survives of Variant 1 is narrow: cron cannot be started by a click, and a cron mistake spends no tokens. What does not survive: "cron is tested on this host" as a proof of the install path, "cron's log is better" as an advantage, and "a scheduler that cannot start an agent" as a statement about the whole system.

## Responses to criticisms

### Weakness 1 (cron schedules nothing today; the daemon runs only because it was started by hand and the crontab is empty)

Verified, and the opponent is right. Evidence from this host today:

- `ps` shows `/usr/sbin/cron`, owner root, parent PID 1 (`./coder agent`), start time Wed Nov 18 20:20:37 2026, up 1 day 7 hours. It is the hand-started daemon from R21.
- `crontab -l` prints nothing. The test entry was removed (R21 says so).
- New fact, worse than the opponent knew: cron is not in the image at all. `/var/log/apt/history.log` shows `Commandline: apt install cron`, `Requested-By: coder (1000)`, on 2026-11-18 18:40:49. `dpkg` and file birth times agree (`/usr/sbin/cron` born 2026-11-18 18:40). Coder issue 515 (open, last comment 2026-11-18 18:45) says the same: "cron is now installed there ... no cron daemon is running". So the image needs a change, which is exactly issue 515.
- There is no syslog and no `/var/log/cron*` on this host, so cron leaves no record of its own firing.

What I keep: R21 tested the mechanism (cron fires on time, `orca repo list` works with `PATH=/usr/bin:/bin`, `gh auth status` stays logged in), and that part does not depend on how the daemon was started. What I give up: R21 does not test the install path (package in the image, daemon from `startup.sh`, entry recreated each boot). That path is issue 515, and it is not done. I stated "the scheduler is already tested on this host" in Round 1 and that was too strong. The honest version is "the mechanism is tested, the install path is not".

Counterweight, not a rescue: the opponent's own evidence is the same kind. No automation exists on this host (`orca-ide automations list` prints "No automations found" today). Its two weeks of waker runs are on Clay's host and are read from the design.

### Weakness 2 (the command Variant 1 schedules, `run-all`, is not shipped)

Verified. `run-all` is at `src/superclaude/cli/issue_watch/cli.py:432` in the worktree `claim-handoff-planb`, on branch `ironbelly/issue-watcher-zero-setup-plan`. `git ls-remote --heads origin` finds no such branch on the fork. The branch has no upstream, three commits ahead of `origin/master`, and uncommitted changes. The master snapshot's `issue_watch/cli.py` has `once`, `status`, `check-config`, `init-state` and `reset`, with no `run-all` and no `dispatch.py`. The PR 686 snapshot (`pr-p`) is the same. The `pr-a` snapshot adds `repos.py`, `route.py` and `wake.py` but no `dispatch.py` either. The handoff doc (line 26) says the installed `/usr/local/bin/superclaude` does not list `run-all`.

What this means for the scheduler choice: very little, and I think the opponent half agrees. A precheck is any shell command, so an automation can run `run-all` as easily as cron can run `once`. The gap belongs to the poll, not the scheduler, and it hits both variants the same way: both need a new build in the template before the command exists. Where it does matter is the diff-analysis point A-001. The two papers compare different commands (`run-all` against `once` plus `repos.yaml`), so C-002 and C-003 are partly "which poll ships". I accept the opponent's request to write the verdict per command. What I will not accept is the inference that unshipped `run-all` weakens cron specifically. It weakens the whole zero-setup plan equally.

### Weakness 3 ("the log holds the outcome" is thin; cron discards the exit code; a wash)

Mostly verified, so mostly conceded. Facts:

- Cron does not keep a job's exit code. The cron line sends output to `~/.aidev/logs/issue-watch.log` with `>> ... 2>&1`, so the log is the only record, and it is only as good as the lines the command prints.
- `run-all` does print one line per repo and one overall line every tick (`_report` in `cli.py`: `sweep: clean`, `sweep: waiting until ...`, `sweep: unhealthy (a child failed)`, `sweep: error ...`). So a finished tick does leave a line, and an unhealthy one says so. That part of my claim holds.
- A tick that loses the outer `flock -n` leaves nothing at all (flock exits silently). A tick that cron never fired also leaves nothing. With no syslog on this host, "cron stopped" and "nothing to do" look the same in the log, except that a normal tick prints a `sweep:` line, so a long gap in the log is the signal.
- The precheck pattern has the same outcome record: the design redirects the poll to `<state_dir>/poll.log` and `audit.jsonl`. On outcome, it is a wash, as the opponent says.
- The opponent's pattern does have one thing cron lacks: Orca history gets a `skipped_precheck` row at every firing. That is a heartbeat for the scheduler (not for the poll). I should have credited it. Cost side: 288 rows a day, retention unknown (UNVERIFIED).

So my Round 1 strength 2 ("every tick leaves a plain record") shrinks to "a finished tick leaves a plain line and a plain exit code for anyone who runs the command by hand". Not an advantage over the poll log under the precheck.

One thing I checked that helps no one but is worth recording: the two lock layers do not collide. The outer lock is `~/.aidev/issue-watch.lock` (from `flock`), the inner one is `<state dir>/issue-watch/run-all.lock` (`dispatch.py:154-171`). Different files, so the cron line will not deadlock itself. The inner lock only matters when a person runs `run-all` by hand while cron's run is going.

### Weakness 4 ("a scheduler that cannot start an agent" is moot because the poll itself starts agents under both)

Half right. As a sentence about the system it is wrong, and I withdraw it in that form. The poll claims issues and launches coordinators and workers through Orca under both schedulers.

What survives is a difference in kind, not in whether agents exist:

- Agent starts by the poll are gated: an approved issue, the predicates, one launch per sweep (R26), and a launch guard that allows one fixed prompt. They happen only when there is work.
- An agent start by the scheduler layer is ungated and unconditional. If the precheck ever exits 0, or someone clicks Run now, a Claude session starts in the orchestrator workspace with the unused prompt, and with a dropped `exit 1` it repeats 288 times a day. Orca's help on this host says it in one line: "Run now in Orca and orca automations run intentionally bypass the precheck". The usage line also requires `--prompt` and `--provider`.

So the right claim is: no mistake at the scheduler layer can start an unguarded model run under cron. It is a real but narrow safety margin. Cost of the failure is bounded for one click (one idle session), and large only for the dropped `exit 1`. The design appends `exit 1` by hand in the command text (`orchestrator.md:350`), and a scheduled shadow run would catch a dropped one on the first fire. I rate this risk as low-probability. It still points the right way, and the opponent concedes the direction in their Concessions 1 and 2.

### Weakness 5 (the owner's reason is partly wrong and Variant 1 knows it; the cron decision was not tested against the precheck pattern)

Conceded in full. I said so in my Round 1 Concession 1 and 5, and in Variant 1's own Risk section. I add one verified detail: the only text about automations in the owner's requirements is line 18, and it was written in the single commit `d0a0a433b` (2026-11-19), a day after Clay's #450 comment (2026-11-18 17:00:32, per the opponent's fact 9, which I did not re-read). I did not find the precheck pattern weighed anywhere in the owner's folder. What this proves is that the decision was not tested against the pattern. It does not prove the decision is wrong. The owner can still choose cron knowing the semantics, because the real reasons (zero setup R1, one dispatcher R16, no click path) do not need line 18's sentence.

### Weakness 6 (requirements line 18 says no `crontab` command; R21 says cron 3.0pl1 is installed)

Resolved: both statements are true, at different times. Line 18 ("This host has no `crontab` command") was true until 2026-11-18 18:40:49. `apt install cron` ran at 18:40:49 as the user `coder`, and R21 describes the host afterwards ("the package is installed ... the daemon was not running ... tested 2026-11-18"). The two lines were written into one file in one commit (`d0a0a433b`, 2026-11-19) with no note that they describe different moments, which is why they read as a contradiction. Today `/usr/bin/crontab` and `/usr/sbin/cron` exist, as the opponent saw.

This does not rescue "tested on this host" as evidence for the install path. It makes the install-path gap clearer: the package got onto this host by a person typing `apt install`, and nothing in the image or `startup.sh` does it yet. I am recording that as the sixth item I concede.

## New evidence

Everything below was read or run today, read-only.

1. Cron came from a hand `apt install` (18:40:49 on 2026-11-18, `Requested-By: coder`), the daemon from a hand start (20:20:37, parent PID 1), and the crontab is empty. So today cron schedules nothing and the image has no cron. This confirms the opponent's Weakness 1 and goes slightly beyond it.
2. Orca, by contrast, is already in the image and running: `/opt/Orca/orca-ide ... --serve` has been up since 2026-11-18 15:02:30 with user data in `/home/coder/.config/orca`. That supports the opponent's point that the scheduler is part of a runtime the poll needs anyway. It is still unknown whether the schedule fires with no GUI window (the server is headless, and I could not confirm where the scheduler lives).
3. `run-all` exists only in the local worktree. No remote branch has it and neither master nor the PR 686 or `pr-a` snapshots contain it.
4. `run-all` prints a `sweep:` line every tick and exits 0 or 1 (75 when the inner lock is held). Cron keeps the line (through the redirect) and drops the exit code. No syslog on this host.
5. Outer and inner locks use different files (`~/.aidev/issue-watch.lock` and `<state dir>/issue-watch/run-all.lock`), so the two layers are safe together.
6. The automation CLI help still says what Round 1 said: `--prompt` and `--provider` are required, a non-zero precheck skips the run and records `skipped_precheck`, Run now and `orca automations run` bypass the precheck, and `--missed-run-grace-minutes` exists. Cron has no catch-up for a missed tick.
7. Coder issue 515 is still open and has had no comment since 2026-11-18 18:45.

## Concessions

1. "The scheduler is already tested on this host" is true for the mechanism only. The install path (image package, daemon at boot, per-boot entry) is untested and sits in an open issue in another repository (Weakness 1).
2. The cross-repo dependency is real and cron-specific as to the scheduler: the image has no cron today. My Round 1 offset (the template needs a new `superclaude` build anyway) is valid but only partly cancels it, because the opponent's route needs no new daemon, package or boot step.
3. "A scheduler that cannot start an agent" is not a property of the system, since the poll starts agents under both. I keep only the narrower claim in the Weakness 4 section.
4. On outcome record, cron is not better than the precheck pattern. Cron drops the exit code and leaves nothing for a lost lock or a missed tick. The precheck pattern also gives Orca history a heartbeat row per firing.
5. The sentence in my Round 1 position that a manual create step "per host" is the main cost of Variant 2 is weaker than I made it. Design N5 forbids the orchestrator from creating an automation; it does not say a template boot script cannot. I did not find or test any way to do it, so it remains UNVERIFIED either way, but it is a design rule, not a proven technical limit.
6. Requirements line 18 and R21 do not contradict each other; they describe different times. I leaned on neither, but I should have noticed the 18:40 install and drawn the "not in the image" conclusion myself.
7. Carried over from Round 1 and unchanged: the owner's sentence is true only for exit 0, "debated and rejected" is not backed by the folder, `*/5` is accepted by the help text in all likelihood, and the six-field FU-2 line is wrong for cron 3.0pl1 (not run here).

## Updated per-point positions

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

## What would change my mind

One fact: a scheduled (not Run now) run of a `*/5 * * * *` automation with a `; exit 1` precheck, created `--disabled` first and then enabled on this host, firing for 24 hours under the headless Orca server, with the history showing only `skipped_precheck` rows, no session started, and the automation still present after an Orca server restart.

- If that holds, I move to Variant 2 as the better choice (about 65%), because the one cron advantage that rests on a tested path (R21) would no longer outweigh cron's open image work (issue 515).
- If the automation stops firing when no window is open, is lost on restart, or fills the history without bound, I move back to Variant 1 (about 70%).

A second, smaller fact would also move me: whether `orca automations create` can be run by a template boot script (idempotently, before the first tick). If yes, X-003 goes to Variant 2.
