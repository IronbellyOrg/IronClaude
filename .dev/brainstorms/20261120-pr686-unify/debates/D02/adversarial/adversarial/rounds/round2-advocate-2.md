# Round 2 rebuttal: Variant 2 advocate (CLAY, Orca automation with a no-agent precheck), debate D02

Role: advocate for Variant 2. Opponent: Variant 1 (OURS, cron with one dispatcher).
Date: 2026-11-20. Read-only run: no automation created or run, nothing written to GitHub, one output file.
Read first: variant-1-original.md, variant-2-original.md, diff-analysis.md, rounds/round1-advocate-1.md, rounds/round1-advocate-2.md, rounds/round2-advocate-1.md.
Checked myself today (all read-only): `orca-ide automations create --help`, `edit --help`, `runs --help`, `list --json`; `ps`; the files under `/home/coder/.config/orca` (names and key names only); the installed Orca code in `/opt/Orca/resources/app.asar` and `app.asar.unpacked` (read by byte offset, nothing extracted); the master snapshot `docs/designs/orchestrator.md` (4.8, 5.9 N5, 12) and `agent-work-report/SKILL.md:30`; the official page https://orca.dev/docs/cli/automations.

## Summary of where I stand

The opponent's Round 2 is fair and I concede most of it. My own Round 1 lean was "Variant 2 on cross-repo dependency and on the owner's stated reason, Variant 1 on failure direction and zero-setup". After checking the five asked points, two of them move toward Variant 2 (retention is capped, survival is likely) and two stay with Variant 1 (the exposure exists, and nobody has fired an automation on this host). The honest overall position: about 55% that the automation is the better scheduler on technical merits, with the first real firing on this host still missing. The owner's decision R6 stands until someone shows the owner the precheck semantics. That is still a toss-up, and I do not claim a win.

## Responses

### (a) The narrowed safety claim: "no scheduler-layer mistake can start an unguarded model run under cron"

I accept the sentence as true. Cron has no Run now button and no exit code that starts a model. What I dispute is how much it is worth. Three checks:

1. What a Run now or `orca automations run` does. I confirmed in the installed code that `runPrecheck` returns nothing at all for any run whose trigger is not `scheduled` (it tests `r.trigger!=='scheduled'||!n.precheck` and returns null). So a manual run really does skip the gate, as the CLI help says. The result is one Claude session in the orchestrator workspace with the prompt "unused: the precheck never lets a run start". It is one idle turn, bounded. It needs a person to click, or an agent with the Orca CLI to type `orca automations run`. The design closes the second route for the orchestrator: N5 puts `orca automations create`, `edit`, `remove` and `run` on the denylist that `refuse()` applies to every verb (`orchestrator.md:762`, `:767`). It does not close it for a model typing a command by hand (the design says so under "Stated limits", line 769). So the route exists but is narrow.
2. A dropped `exit 1`. This is the larger one: the precheck then exits 0 and a session starts at every tick, up to 288 a day. How likely is it? The `exit 1` is written once, at create time, and is typed by hand in the command text (`orchestrator.md:350`). The only planned edit of the command is the switch-on step, which removes `--dry-run` from it (`orchestrator.md:354`). That one edit is where the mistake would happen. Detection is quick: the first scheduled tick after switch-on shows a new terminal in the workspace and a `dispatched` row instead of `skipped_precheck` in `orca automations runs --id`. That puts the worst case at a few sessions before somebody looks, not 288. I rate this low probability and bounded loss, but I do not call it zero.
3. Things in the design and in the Orca code that shrink it. From the code: a precheck that crashes, times out, or cannot resolve its workspace is treated as a failed precheck and the run is skipped. I read that branch: when the workspace target does not resolve, `runPrecheck` returns a failure result built from the error, not a pass. So every failure of the gate fails closed. Only a clean exit 0 starts an agent. From the design: the shadow run is a scheduled one, so the first runs never use the bypass (`orchestrator.md:354`).

Two cheap improvements that are not in the design today, offered as suggestions and not as facts about master:

- Replace the hand-typed `...; exit 1` with a fixed command such as `superclaude issue-watch tick`, whose code starts the poll detached and then returns 1 on every path, with a unit test that asserts it. The "dropped `exit 1`" mistake then cannot happen by editing the command, because the command never needs editing. The `--dry-run` choice moves into the poll's own config.
- Make the automation's prompt an instruction ("do nothing and stop") instead of "unused". A stray Run now then costs one short reply.

One more comparison that the opponent's claim leaves out: a dropped `--dry-run` during the shadow period is the same kind of edit mistake under cron, and it would wake real agents there too. So the extra exposure of the automation is only the unguarded idle session, not edit mistakes in general.

Size of the risk, my honest reading: a real but small margin in cron's favour. It does not decide the choice. I keep C-004 with Variant 1, at a lower confidence than in Round 1.

### (b) N5 binds the orchestrator, not a boot script; can a template boot script create the automation idempotently?

Agreed on the first half: N5 is a rule about what the orchestrator may run, not a technical limit. My Round 1 sentence that creation is "an owner step" described the design's O3 and O4, not what is possible. I checked the second half read-only:

- The CLI has no "create if absent" flag. `orca automations create --help` lists no creation key. The Orca code does have a `creationKey` parameter: when a create call carries a key that an existing automation already has, the existing one is returned and nothing new is made. But that key exists only in the internal call (`shared/rpc-contract/automation-params.js:150`), and I found no CLI flag that sets it. So I cannot count on it.
- Names are not unique. The create path does not check the name, so a second `create --name orchestrator-poll` would make a second automation.
- A boot script can still be idempotent in the ordinary way: `orca automations list --json`, look for `name == "orchestrator-poll"`, and create only when it is absent. `list --json` works here today (it returns an empty `automations` array). One boot script, run once per boot, makes the check-then-create race harmless in practice. If it did create two, each tick would start two polls and the second would exit 75 on the poll's own lock (`record.py:382`), so the failure is quiet.
- What the script needs that cron does not: the Orca server must be up when it runs (it talks to the Orca runtime), and `--workspace path:<orchestrator-repo>` must name a worktree that already exists in Orca. Cron needs neither. So a boot script is possible but has an ordering condition in `startup.sh` that nobody has written or tested.
- What it saves: if the automation survives an image update (see (c)), the script is a safety net that normally finds the automation already there. Cron's entry has to be recreated at every boot.

Net for X-003: the design's "owner step" is a design choice, not a wall. But no such script exists, and the opponent is right that "zero setup" is proven today for neither route. I move X-003 from 60% Variant 1 to a draw, 50%.

### (c) Where the automation is stored, and does it survive an Orca restart or an image update

Read-only findings:

- Storage. Automations are part of the profile state: `/home/coder/.config/orca/profiles/local-default/profile-state.db` (an SQLite database with a write-ahead log; the older `orca-data.json` in the same folder still has `automations` and `automationRuns` keys, both empty arrays, and a `sqlite-export` from 2026-10-27 shows the move). The Orca code writes each created automation into the state and flushes it at once (`state.automations=[...]` then `flush()`), and each run row the same way.
- That folder is on the persisted home volume. `/home/coder` is its own device (`/dev/sdb`, ext4, 1.3 TB), and Orca's program is on the image side at `/opt/Orca`. The proof that this folder outlives image updates is in its own dates: files in `~/.config/orca` date from 2026-10-24 and 2026-10-27, while the installed `app.asar` is from 2026-11-08 and the running server started 2026-11-18 15:02:30 (version `1.4.245-aidev02`). The profile and its repo list survived at least one program update and several restarts. Automations live in the same store, so they should do the same. I did not create one to test it, so this stays an inference. It is stronger than Round 1, because it rests on the folder's own history, not on the text of issue 515 alone.
- Restart behaviour. On start, the scheduler recomputes from the stored `nextRunAt`. A run that was due while the server was down is run once if it is inside the missed-run grace window, otherwise recorded as `skipped_missed`. The create path defaults that window to 720 minutes (`missedRunGraceMinutes ?? 720`), and `--missed-run-grace-minutes` sets it. So after a restart there is catch-up. Cron has none.
- Also noted: the build has code that carries "dormant" automations across an Orca-managed upgrade (`orcad-migration-dormant-automation-validation.js`). I read it only to see that upgrades are expected to keep automations. I did not test one.

So (c) goes to Variant 2 at about 65%: stored on the persisted volume, with no observed loss, and not tested by me.

### (d) The 288 `skipped_precheck` rows a day, retention unknown

Retention is now known, from the installed code. The function that prunes run history keeps the newest 100 runs in a finished state per automation, and it is called with that default at load and every time a run row is created (`Uoe(e, t=100)`; I found three call sites and none passes another number). Pending and running rows are kept besides. Consequences:

- The history cannot grow without bound. At 12 ticks an hour, 100 rows cover about 8 hours and 20 minutes. Storage is a non-issue.
- It also means the Orca history is a short heartbeat, not a record. Over a weekend it keeps nothing of Friday. So my Round 1 line "Orca keeps run history" must not be read as an audit trail. The record of what the poll did stays in `audit.jsonl`, `poll.log` and `issue-watch status`, exactly as the design says, and the opponent is right that under both routes a person must read those.
- The 2 writes per tick (create the row, then mark it skipped) are small. The profile database's write-ahead log is already 4 MB and busy with terminal state.
- What I did not check: how the Orca desktop table shows 100 identical `skipped_precheck` rows (noise in the UI). The waker automation fires twice a day, so "VERIFIED 2026-11-03" does not cover this cadence, as the opponent said. Retention is bounded, but "works at 288 a day" is still unobserved.

### (e) Does the Orca schedule fire with no GUI window?

Evidence, none of it a firing:

- The official page does not say. I fetched https://orca.dev/docs/cli/automations: it says schedules "reside on the local computer or supported connected Orca hosts", gives a 30-minute missed-run grace example, and states no retention. It does not say whether a schedule runs after the window is closed or Orca is quit, and it does not describe headless operation. So the documentation is silent, as I said in Round 1.
- The installed code is more informative. The scheduler is a class in the main process that runs `setInterval(evaluateDueRuns, 60000)` (`tickMs` defaults to 60 000 ms). It is started with `start()` and does not wait for a window. The precheck runs in that same main-process path (`runPrecheck`, then the run is marked `skipped_precheck` before any dispatch). The part that needs a renderer is the dispatch of an agent: `canDispatch` is true when a renderer is ready or when the build has a `headlessDispatcher`, and the build has one, switched on by a `headless` option, with a separate keep-alive routine for headless mode. So the program is written to run automations without a window, including the dispatch.
- This host: `ps` shows the server `orca-ide --serve --serve-json --serve-port 6768` (pid 476, since 2026-11-18 15:02:30), a virtual display `Xvfb :99` that Orca itself started, and zero `--type=renderer` processes. So there is no window and no page rendering at all. That is the setting the code's headless path is built for.
- What I could not confirm: which switch turns the `headless` option on for `--serve`. I searched for it and found only an end-to-end test variable (`ORCA_E2E_HEADLESS`) near it, so the link between `--serve` and the headless dispatcher is by inference. If it is off, then with no renderer `canDispatch` is false for every tick, and the scheduler may record `skipped_unavailable` instead of running the precheck. That would stop the poll silently. This is the one real unknown that decides whether the automation works here at all. Round 1 called it "UNVERIFIED"; it is now "supported by the code, not run".

Position on (e): likely yes, untested. This is the point where I am most exposed, and I say so.

## New evidence

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

## Concessions

1. The opponent's narrowed safety claim is true as written. Cron has no scheduler-layer path to an unguarded model run. I only dispute its size.
2. "Run now" bypasses the precheck in the code, not just in the help text. The design's prompt gives that session no instruction. My two improvements (a fixed always-exit-1 command, and a "do nothing" prompt) are not in the design.
3. The 288-rows-a-day concern is answered on storage but not on usefulness: Orca keeps only about 8 hours. It is a heartbeat, not an audit trail. The poll's own outcome is in `audit.jsonl` and `poll.log` under both routes.
4. N5 is a design rule, not a technical limit; a boot script could create the automation. But no boot script exists, it needs the Orca server up and the orchestrator worktree to exist, and it is not idempotent by flag, only by a list-then-create check. "Nothing outside this repo changes" in my Round 1 paper remains an overstatement for set-up effort.
5. No automation exists on this host and I observed no firing. The headless claim rests on reading code. The waker evidence is from Clay's host and is twice a day.
6. The image has no cron today (the opponent's `apt install` finding). That strengthens C-003 for Variant 2, but only a little: both routes need a new `superclaude` build, and the automation needs a creation step.
7. The owner decided R6 and R16 on 2026-11-18. Nothing here proves the owner wrong; it shows the stated reason was incomplete.

## Updated per-point positions

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

## What would change my mind

One fact: a `*/5 * * * *` automation with a `; exit 1` precheck, created `--disabled` and then enabled on this host under the present headless server, fires on schedule for at least one hour with only `skipped_precheck` rows, starts no session, and is still listed after an Orca server restart.

- If that holds, I move to Variant 2 at about 70%, and I would ask for the always-exit-1 command and the "do nothing" prompt as part of the design.
- If the scheduler records `skipped_unavailable` or nothing at all with no window open, or the automation is gone after a restart, I concede to Variant 1 outright (about 75%), because the whole case for the automation depends on it firing without a window.

A second, smaller fact would also move me: a template boot script that runs `list --json` then `create` and is shown to leave exactly one automation after two boots in a row. If that holds, X-003 goes to Variant 2.
