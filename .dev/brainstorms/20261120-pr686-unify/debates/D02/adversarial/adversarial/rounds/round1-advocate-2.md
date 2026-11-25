# Round 1 statement: Variant 2 advocate (CLAY, Orca automation with a no-agent precheck)

Debate: D02 scheduler, cron or Orca automation. Round 1. Author role: advocate for Variant 2.
Date: 2026-11-20. Read-only run: no automation created or run, nothing written to GitHub.

## Position

Variant 2 holds: the poll runs from one Orca automation whose precheck starts `superclaude issue-watch once` detached and exits 1. I claim three things and no more.

1. The owner's written reason against automations ("it starts an agent session with a prompt on each run", requirements line 18) is false for this pattern. Variant 1 admits this itself (its Risk, bullet 1).
2. The pattern is already on master and has run on Clay's host, so it is not speculative.
3. It needs nothing outside this repository, while cron needs Coder issue 515, which is open, so cron is not scheduling the watcher anywhere today.

I do not claim automations beat cron on every axis. Run now, the zero-setup goal and the direction of failure favour cron, and I say so below.

## Steelman of Variant 1

The strongest version of Variant 1: a scheduler whose only job is "run this command every 5 minutes" should be one that cannot start a model. Cron cannot. An Orca automation can, by three routes: a click on Run now, `orca automations run`, or an edit that drops the `exit 1` (the precheck then exits 0 and a Claude session starts every 5 minutes). Orca's own help says so: "Run now in Orca and orca automations run intentionally bypass the precheck". The automation also has two required parameters it does not use (`--prompt`, `--provider`). Under cron nobody can fail by accident into "the scheduler started an agent".

Beyond that, Variant 1 is the owner's decided line (requirements R6 and R16, 2026-11-18). It matches the zero-setup goal: the template installs cron and writes the entry on every boot, so no person creates anything per host, whereas the automation is an owner-run step (O3, O4) and design N5 forbids the orchestrator from doing it. Cron was tested on this host (R21: a per-minute entry fired on time, `orca repo list` worked under an empty environment; handoff doc: `gh auth status` stayed logged in). It has a two-layer lock (`flock -n` plus the dispatcher's `loop_lock`, `dispatch.py` around line 154). And Variant 1 is honest about its own weak spot: it says its argument "must not lean on" the owner's sentence, and that "debated and rejected" is not backed by the debate folder.

What it genuinely gets right: the failure direction of a script-only automation is worse than cron's (a mistake spends tokens, where a cron mistake spends nothing), and the zero-setup goal is a real owner requirement that cron serves and an automation, today, does not.

## Key strengths claimed (Variant 2)

1. The owner's blocker does not hold. Orca help, re-read today with `orca-ide automations create --help`: "Use --precheck to run a command only before scheduled runs; exit code 0 continues, any other exit, error, or timeout skips the run" and "Skips appear in Orca run history ... as skipped_precheck". Every failure of the precheck (crash, timeout, non-zero exit) skips. Only exit 0 continues. So the dangerous direction needs one specific mistake, and the design appends an explicit `; exit 1` after the detached start (`docs/designs/orchestrator.md:350`).
2. The pattern is on master and in use. `src/superclaude/skills/agent-work-report/SKILL.md:30` (master snapshot, read today): the waker automations "run the script as its precheck command, detached, and exits non-zero so Orca starts no agent and leaves no terminal (VERIFIED 2026-11-03)". `waker.py` comments record real firings (2026-11-04: the run opened 8 seconds after the wake line; 2026-11-18: a usage-limit error four minutes after it). Same host, same Orca, same shape. Cron has produced no firing of the watcher anywhere.
3. No cross-repo dependency. Cron's crontab is outside the persisted home volume and resets on an image update (R6), so cron needs the image change, the daemon start and a per-boot entry from `startup.sh` (Coder 515, open). On this host today `crontab -l` prints nothing and the cron daemon runs only because it was started by hand on 2026-11-18 20:20:37 (`ps`, read today). So "cron works" is shown for a hand-started daemon, not for the installed path.
4. The cron environment is a real cost Variant 1 pays. R21: cron's environment is only `PATH=/usr/bin:/bin` with no `~/.aienv`, so `orca`, `gh`, `superclaude` and `uv` are not found by name. The cron line therefore needs a PATH line and a hard-coded `--orca /home/coder/.config/orca/linux-orca-cli-shim/orca` (handoff doc, cron block). The precheck is `bash -lc` and the design sources `~/.aienv` and `~/.env` first (`orchestrator.md:350`); U6 already shows `command -v superclaude gh orca ccsession` finds all four in a login shell (`orchestrator.md:1264`).
5. The poll needs Orca anyway. It wakes sessions through `orca`, so a host where the Orca server is down cannot complete a poll under either scheduler. Variant 1's "no hidden dependency on Orca's scheduler semantics" protects against a failure the poll cannot survive anyway. (Whether the schedule fires while the Orca app is closed is UNVERIFIED; here the server runs headless.)
6. The unknowns have a plan. U6 and U7 are listed with checks (`orchestrator.md:1264-1265`); creation is `--disabled`; the 24-hour shadow run is a scheduled `--dry-run`, so the first runs do not use the Run now bypass (`orchestrator.md:966`). Orca also offers `--missed-run-grace-minutes` and `orca automations runs --id` for history (read from help today).

## Weaknesses identified in Variant 1

1. Cron schedules nothing that matters today. The Coder issue 515 work (package, daemon start, per-boot entry, `flock -n`, log) is open and in another repository; Variant 1's own Cost says so. Its R21 evidence is a hand-started daemon and a test entry that was removed (R21: "Test entry removed, crontab is empty again"). My `ps` and `crontab -l` today agree.
2. The command Variant 1 schedules is not shipped. The handoff doc says the `/usr/local/bin/superclaude` on this machine does not list `run-all`. `run-all` lives only in the unpushed branch `claim-handoff-planb`. Master and the PR 686 design have `once`. Variant 1 argues for a scheduler of a command that cannot yet run from a clean install.
3. "The log holds the outcome" is thin. Cron discards a job's exit code; the cron line writes stdout and stderr to `issue-watch.log`, and `flock -n` exits silently when it loses the race. Variant 2 has the same weakness (outcome in `audit.jsonl` and `poll.log`), so this is a wash, not a cron advantage. Variant 1's fact 7 (Orca history shows only `skipped_precheck`) is true, but under cron too nothing shows "the poll crashed" unless a person reads the log.
4. "A scheduler that cannot start an agent" is true of cron but not of the system. The poll itself starts agent sessions (claims, wakes) through Orca. That risk lives in the poll's own launch guards and is the same under both schedulers. The automation's only extra exposure is the Run now click and a dropped `exit 1`.
5. The owner's reason is partly wrong and Variant 1 knows it. Requirements line 18 says an automation "starts an agent session with a prompt on each run"; Variant 1's Risk concedes this is "true only when the precheck exits 0". Its Risk bullet 2 adds that the debate folder covers one dispatcher against one entry per project and assumes cron. So the cron decision was not tested against the precheck pattern Clay proposed on 2026-11-18 17:00:32.
6. Variant 1's own source disagrees with itself about this host. Requirements line 18: "This host has no `crontab` command"; R21: cron 3.0pl1 installed. Today `/usr/bin/crontab` and `/usr/sbin/cron` both exist. Which statement was true when, I cannot tell (UNVERIFIED), so the "tested on this host" evidence has an unexplained gap.

## Concessions

1. Run now and `orca automations run` bypass the precheck and start a real Claude session in the orchestrator workspace (Orca help, quoted above). Cron has no such hazard. My mitigation is partial: a scheduled shadow run, and (my suggestion, not in the design) a prompt that tells the agent to do nothing and stop, so a stray click costs one idle turn. The design's current prompt, "unused: the precheck never lets a run start", gives a session no instruction either way.
2. Dropping `exit 1` turns a quiet automation into a token burn every 5 minutes. The design checks this only by observation (`orca automations runs`, the shadow run). Cron has no equivalent exposure.
3. Creating the automation is an owner step (O3, O4) and N5 forbids the orchestrator from doing it (`orchestrator.md:762`, `:1025`). Against R1 and R17 ("nothing in the setup is manual") this is a real mark against Variant 2, unless a template startup step can run `orca automations create`, which I have not verified (UNVERIFIED).
4. Official documentation describes automations as prompts run through an agent and documents the precheck only as a gate. The script-only use rests on the gate semantics, the master skill's VERIFIED note and about two weeks of waker runs. The `*/5` step syntax (U7) and PATH in the precheck shell (U6) are not verified on this host: `orca-ide automations list` today prints "No automations found".
5. Variant 2's paper is loose: "Nothing outside this repo has to change" sits beside "Creating the automation is an owner step". These are two claims (no change to another repository, versus one owner command per host), but the wording invites the reading Variant 1 gave it (X-003).
6. Cron is the owner's recorded decision (R6, R16, 2026-11-18). If the owner reaffirms it knowing the precheck semantics, I have no further argument.

## Shared-assumption responses

- A-001: QUALIFY. The scheduler choice does not change the poll command in principle: a precheck can run `run-all` as easily as `once`, and cron can run `once`. But the papers do compare different commands (`once` from the PR 686 design, `run-all` from the unpushed branch), so part of the contest (C-002, C-003) is really "which command ships", not "which scheduler". Neither paper states this. I accept it as a gap in both and ask that the verdict be written per command.
- A-002: QUALIFY. Both schedulers need one set-up per host: one crontab per workspace boot (automatic if Coder 515 lands) or one automation per Orca host (manual today; automatic only if a template startup step can create it, UNVERIFIED). The unit is the same, but the costs are not equal: cron's can be automated by the template, the automation's currently cannot.
- A-003: ACCEPT. A 5-minute tick fits the poll's 240-second deadline (`orchestrator.md:322`), and both sides quote the same cadence. The automation also has `--missed-run-grace-minutes`, and cron has no catch-up; neither changes the cadence.

## Per-point positions

| Point | Winner | Confidence | Evidence |
|---|---|---|---|
| C-001 (does an automation start an agent every run) | Variant 2 | 90% | Orca help: "any other exit, error, or timeout skips the run"; `SKILL.md:30` VERIFIED 2026-11-03; Variant 1 Risk bullet 1 concedes "true only when the precheck exits 0". |
| C-002 (fit to one dispatcher over many repos) | Variant 2, narrowly | 60% | The precheck is arbitrary shell; the `--workspace` binding names the workspace of a run that never starts. The design routes repos from `repos.yaml` (`orchestrator.md:37`, `:59`). Residual: whether the precheck's working directory matters is UNVERIFIED, and `run-all` itself is unmerged. |
| C-003 (dependencies outside this repo) | Variant 2 | 55% | Cron needs Coder 515 (open) and a per-boot entry; crontab resets on image update (R6). Variant 1 wins the sub-point "zero manual setup" (see X-003). Net: Variant 2 on cross-repo dependency, but the owner's R1 and R17 weigh the other way. |
| C-004 (failure modes that start a model) | Variant 1 | 70% | Run now and `orca automations run` bypass the precheck (Orca help); a dropped `exit 1` starts an agent every 5 minutes. Cron has neither. My mitigations (shadow run, harmless prompt) reduce but do not remove it. |
| X-001 (automation starts an agent on each run) | Variant 2 | 90% | Same evidence as C-001; the CLI help settles the exit-1 case. |
| X-002 (what an automation is bound to) | Variant 2 | 65% | The binding selects the workspace of an agent run that the precheck prevents; the poll reads repos from its own config. Variant 1's "bound to one repo" is true of the option and irrelevant to a script-only precheck. |
| X-003 (manual per-host set-up) | Variant 1 | 60% | Design O3, O4 and N5 make creation an owner step; my Cost section says so. The "nothing outside this repo" sentence is true only for repository changes, not for set-up effort. |
