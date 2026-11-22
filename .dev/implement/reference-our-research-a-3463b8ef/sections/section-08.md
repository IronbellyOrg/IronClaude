# Section 08 analysis: Every check, defined
Counts: COVERED 8, CONFLICT 2, NOT-COVERED 5 (15 features)

Source: issue 655 body lines 106-116 (table of checks), plus acceptance criteria at body lines 215 and 222. Context lines 1-30 read. Plan files searched: SPEC.md (FR, SEC, section 2, section 7, Appendix B), DECISIONS.md, D02, D08, D13, D15, QG4 verdicts, FOLLOW-UPS.md, both tech references, and the installed src/superclaude/core/WORKER-CONTRACT.md. Paths below are relative to /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/ unless they start with src/ or .dev/implement/.

### S08-F1 New-issue poll is a no-model script on a 5-minute clock
- 655 says: Row "New issues" (body line 110): the poll script finds new issues with no model unless something is new, on the clock every 5 minutes. AC line 215: a cycle with nothing new starts no agent and spends no model tokens.
- Status: COVERED
- Current plan: SPEC.md FR-10 (line 200: one cron entry `*/5 * * * *`), FR-11 (line 201: `run-all` runs one read-only poll per project), section 3.1 (line 125: the poll starts a claim session only when an issue passes the start gate), FR-06 (line 196: the poll cycle writes nothing to GitHub). The poll is code, not a model; a model session starts only for a claim or a wake.
- Depends on: none
- Evidence from our documents: not needed for COVERED.
- Concerns: the plan cannot yet show "zero model tokens on an empty cycle" as a tested number. SPEC.md line 705 plans a 24-hour cron shadow run ("no agent, no config generated, no GitHub write"); that run has not happened (UNVERIFIED).

### S08-F2 The scheduler is an Orca automation, and no cron entry exists
- 655 says: The poll is "run by the Orca automation" (body line 110, and section 1 line 23, reusing the work-report waker precheck pattern). AC line 215: "An Orca automation runs the poll script every 5 minutes ... and no cron entry exists."
- Status: CONFLICT
- Current plan: D02 verdict (debates/D02/VERDICT.md line 15): "Scheduler of record is cron", one `*/5 * * * *` entry under `flock -n`. SPEC.md FR-10 (line 200), FR-11 (line 201), and section 7 row B2 (line 449): "B2 Orca automation as scheduler: REJECT; cron stays". 655's version is REJECTED as the primary scheduler. Only the precheck pattern survives as a tested-first fallback (D02 recommendation 4, line 18; SPEC.md line 704 "Precheck test"), created `--disabled` by the owner.
- Depends on: none
- Evidence from our documents: debates/D02/VERDICT.md:9 "Cron with one dispatcher stays the scheduler (the owner's line wins the tie)". debates/D02/VERDICT.md:28 "an automation has two [paths to a model run] (Run now bypass, a dropped `exit 1`)".
- Concerns: D02 is HYBRID at 62% confidence (SPEC.md line 78) and both advocates called it a toss-up (D02 line 72). Cron is not yet in the Coder image (Coder 515; SPEC.md RK-5 line 649). 655's claim that a precheck-exit automation starts no agent is correct (D02 line 17), so only the owner's old reason was wrong, not the fallback. The test that would reverse D02 is optional and not run (D02 line 23). Owner rule applies: the current plan wins.

### S08-F3 Poll interval is configurable
- 655 says: "Every 5 minutes (configurable)" (body line 110; AC line 215).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC.md, DECISIONS.md and D02 for "configurable", "interval", "poll_interval", "schedule". FR-10 fixes the literal `*/5 * * * *`; the only edit path is changing the cron line. SPEC.md line 558 mentions "interval" only for a push-notice number.
- Component: WATCHER (scheduling belongs to the poll and its cron line or config).
- Feature statement: Let the owner change the poll interval in one named setting instead of hand-editing the cron line.
- Done when: after changing the setting to a new value, `crontab -l` (or the dispatcher's own status) shows the new interval and `issue-watch status --json` reports it.
- Depends on: S08-F1
- Evidence from our documents: debates/D02/VERDICT.md:67 "A sweep can last up to about 525 seconds ... against a 300-second tick, so lost ticks can be routine; not measured." A shorter interval makes overlap worse.
- Concerns: low value. The 270 s cap (SPEC.md line 171) and `flock -n` (FR-10) assume a 5-minute tick; any interval below the sweep time causes skipped ticks, so a floor is needed.

### S08-F4 The poll also applies the hold (plan check, `hold:*`)
- 655 says: The poll script "also applies the hold of section 1" (body line 110; hold rules at section 1 line 25).
- Status: COVERED (read-only part only)
- Current plan: SPEC.md section 2 D01 (line 77: plan check and `hold:backlog` added as read-only skips), FR-54 (line 275: `plan_body.py check` is the reference), FR-08 (line 198: re-check plan check and `hold:backlog` at wake time). The part where the poll WRITES the `hold:plan` label is a CONFLICT: FR-06 (line 196), FR-07 (line 197), D09/Q03 and section 7 row A5 (line 443) reject it. That write belongs to the section 1 analysis and is only a dependency here.
- Depends on: 655 section 1 (hold and `hold:plan` label), S08-F1
- Evidence from our documents: not needed for COVERED.
- Concerns: the plan keeps the owner's approval as the start trigger (D01; section 7 row A12 line 447 "assignment alone as trigger: REJECT"). 655's "assignment is the only trigger" conflicts with D01; that is handled in section 1.

### S08-F5 Worker messages are read from the Orca mailbox as they arrive
- 655 says: Row "Worker messages" (body line 111): the orchestrator reads the Orca mailbox (`worker_done`, `ask`, escalation, heartbeats) as they arrive, using `orca orchestration check --wait`.
- Status: COVERED
- Current plan: SPEC.md section 3.2 steps 1 and 6 (lines 145 and 151-153: the coordinator pulls at each `check --wait` and handles `worker_done`), FR-28 (line 230: pull the wake folder at every `check --wait` return, at most every 5 minutes), FR-83 (line 243: coordinator reads a succeeded `worker_done`). Worker side: src/superclaude/core/WORKER-CONTRACT.md (WC-5, WC-7, WC-10; line 61 heartbeats, "sends none while blocked in `ask` or `check --wait`"). The tech reference lists the Run mailbox read as designed with no PR (techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md:366).
- Depends on: none
- Evidence from our documents: not needed for COVERED.
- Concerns: handling of `ask` and escalation messages has no requirement in SPEC.md (searched "ask", "heartbeat", "worker_done"); only `worker_done` has a step. It sits in the coordinator verbs (FR-26), which are NOT BUILT (SPEC.md line 62). Whether Orca mailbox reads are non-acknowledging is UNVERIFIED (techref OBSERVER...:210).

### S08-F6 Every open worker gets a status check (state from Orca, stall proofs)
- 655 says: Row "Worker status" (body line 112): "A status check of every open worker: state read from Orca".
- Status: COVERED
- Current plan: SPEC.md FR-38 (line 240: each cycle run `/sc:sweep`), FR-42 (line 253: "WC-16 (one coordinator sweep per 5 minutes) unchanged"). The sweep reads `worker-list` and `worker-show` and applies Orca stall proofs (techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md:704-706, WC-10 and WC-16 rows). The plan checks at every wake or wait timeout, at most every 5 minutes, which is more often than 655's hour.
- Depends on: S08-F5
- Evidence from our documents: not needed for COVERED.
- Concerns: the tech reference cites WC-16 at WORKER-CONTRACT.md:287-289, but I found no "WC-16" or "sweep" text in the current src/superclaude/core/WORKER-CONTRACT.md (grep returned nothing), so its source branch is UNVERIFIED. The sweep is read-only and recommends nothing (D13 verdict line 51).

### S08-F7 Worker check runs hourly, Monday to Friday, 24 hours, interval configurable, stops at `worker_done`
- 655 says: Same row (body line 112) and AC line 222: hourly by default, only the interval is configurable, for each running worker, Monday to Friday, 24 hours a day; it stops for a worker at its `worker_done`.
- Status: NOT-COVERED
- Current plan: none found; searched SPEC.md, DECISIONS.md and all D*, QG* verdicts for "hourly", "--hourly", "Monday", "weekday", "24 hours a day", "status check". The only hit is the flag `--hourly` on `/sc:coordinator` (D08 verdict line 18; SPEC.md FR-24 line 226), adopted "unchanged" from Clay, but no document defines what it does (UNVERIFIED). The plan's cadence is the 5-minute sweep (S08-F6), with no weekday window.
- Component: COORDINATOR (the `--hourly` flag and the coordinator's own check cadence).
- Feature statement: Define the `/sc:coordinator --hourly` pass as a once-an-hour check of each running worker, Monday to Friday, with a configurable interval, that ends for a worker when its `worker_done` arrives.
- Done when: a test with a fake clock shows one check per running worker per hour on weekdays, none on Saturday and Sunday (or the plan states why weekends are included), and none for a worker after `worker_done`.
- Depends on: S08-F6, S08-F8
- Evidence from our documents: techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md:1251 "Leftover, unreferenced: no hourly automation exists" (about the report's own hourly waker mode, a recorded skip per line 811). debates/D13/VERDICT.md:50 keeps "the owner's duty text in issue 339 (hourly sweep ...)" as the governing definition, so an hourly duty exists for issue 339 but is not tied to 655's table.
- Concerns: who starts an hourly pass is unspecified. A coordinator waiting on `check --wait` has no clock, so an hourly pass needs a scheduler; FR-10 allows only the one poll cron entry and SPEC.md section 8 says no stage adds cron before S17. Do not add a second cron entry without the owner.

### S08-F8 The status check also reads the issue (closed, assigned elsewhere, edited by someone else)
- 655 says: The status check "also reads the issue (closed, assigned elsewhere, edited by someone else)" (body line 112).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC.md for "reassign", "assigned elsewhere", "unassigned", "edited since", "body hash", "re-check". The plan checks these conditions only at START: SPEC.md section 3.1 (line 125: assigned only to the watcher login, Approved "unedited since"), D01 "start-time re-check repeats every gate (MR-1)" (line 77). `/sc:closeout` checks the merged PR at the end (FR-38). No mid-flight re-read of the issue is stated.
- Component: COORDINATOR (per-issue state and watching are the coordinator's; the poll only reads for new work).
- Feature statement: While a worker runs, have the coordinator re-read its issue on each status pass and record a stop or an escalation when the issue is closed, assigned to someone else, or edited by another person.
- Done when: with a fake `gh` returning a reassigned, a closed and an edited issue in turn, the coordinator marks each case in the per-issue file and takes the escalation path instead of continuing.
- Depends on: S08-F7, 655 section 9 (escalation rules)
- Evidence from our documents: SPEC.md:125 and :77 (start-time only, quoted above). SPEC.md:218 (FR-82, NG-2): the poll cycle writes nothing to GitHub, so this must be a read.
- Concerns: an owner edit after approval may void the approval; SPEC.md FR-35 (line 237) says a re-plan voids approval and the whole start gate repeats. A mid-flight edit needs a stated rule (UNVERIFIED, not in the plan).

### S08-F9 Check-ins by typing, done by the coordinator itself, no session manager
- 655 says: Row "Worker status" (body line 112): "a check-in by the orchestrator itself where needed". AC line 222: no session-manager skill; the orchestrator does every check-in itself, typing included, refused on unsent typing or fresh output.
- Status: COVERED
- Current plan: FR-40 (SPEC.md line 242): "Type into worker terminals only under the four typing rules". Section 7 row D14 (line 462): typing "ADOPT+CHANGE". The techref shows the same guard in code: `typing_or_fresh` marks a terminal unsafe if it holds draft text or output under 60 s old (techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md:812). No document states "no session manager" as a rule (searched "session manager", "session-manager"); the plan has none in effect.
- Depends on: S08-F6
- Evidence from our documents: not needed for COVERED.
- Concerns: the four typing rules are text only; the typing helper is a shared helper with a parity test planned (FR-18, line 208), NOT BUILT.

### S08-F10 Approving permission prompts and one interrupt during a check-in
- 655 says: AC line 222: the check-in includes "approvals"; "refused on unsent typing or fresh output, except the one interrupt"; "always allow" never sent (FR-23, FR-24 of Clay's spec).
- Status: CONFLICT
- Current plan: FR-40 (SPEC.md line 242): "never approve a permission prompt; never interrupt a worker". Section 7 row D14 (line 462): "reject approving permission prompts". Row D9/N7 (line 458): interrupt REJECT. OD-7 (line 103): "No interrupt of a running worker" (QG4, 85%). 655's version is REJECTED.
- Depends on: S08-F9
- Evidence from our documents: debates/D15/VERDICT.md:98 "Reject approving permission prompts (WC:122, WC:137); drop approval rules and test cases". debates/QG4/VERDICT.md:20 "The N7 interrupt would be undone by the contract's own nudge and cannot be confirmed to land, and no incident is cited." debates/D15/VERDICT.md:238 "never answers a permission prompt, never interrupts a worker".
- Concerns: SECURITY. Approving a worker's prompt from the coordinator widens what a worker may do without the owner; the plan refuses it on purpose. A builder must not implement approvals or the interrupt from 655.

### S08-F11 The worker entry is updated only at milestones
- 655 says: "the entry is updated only at a milestone" (body line 112); AC line 221: added at claim, updated at milestones only, removed at close.
- Status: NOT-COVERED
- Current plan: none found; searched SPEC.md, DECISIONS.md, D11, D15 verdicts, both tech references and clay-prs.md for "milestone", "updated only at", "on each worker message". The plan says who writes an entry (FR-48: `report-entry` is the only writer; FR-49: AU4a, AU4c, AU5 shown as lines of the entry; NFR-02) but not WHEN it is updated. FR-45, FR-46 and FR-48 are blocked until the report skill is restored (SPEC.md Appendix B line 778; owner action B.3 item 1, line 786).
- Component: COORDINATOR (work-report entries and the `report-entry` verb).
- Feature statement: Have `report-entry` write an issue entry at claim, update it only at a named list of milestones (plan done, blocked or asking, PR opened, review rounds, PR ready, merged) and remove it at close.
- Done when: a run with a fake worker sending ten heartbeats and two CI changes produces no entry update, and each listed milestone produces one.
- Depends on: 655 section 7 (living report), S08-F5, owner decision B.3-1
- Evidence from our documents: SPEC.md:778 "FR-45, FR-46, FR-48 ... blocked until the skill is restored (they stay requirements)". SPEC.md:786 "Decide whether to restore the PR 684 skill (`agent-work-report`) from the archive branch".
- Concerns: the milestone list is in 655 comment 6 (comments file lines 59-63), not in the section 8 table. It cannot be built until the owner rules on B.3-1.

### S08-F12 Daily report run: Monday to Friday, 07:00 local, configurable
- 655 says: Row "Daily report" (body line 113): a daily run of the work report, Monday to Friday, default 07:00 local, configurable.
- Status: COVERED
- Current plan: D02 verdict recommendation 5 (debates/D02/VERDICT.md line 19): "The two existing report automations stay as they are. `coordinator-morning-wake` and `coordinator-missed-check` ... a daily wake at fixed hours." debates/OAG1/VERDICT.md:63 names the 07:00 wake as an existing surface "for Clay's own setup only". The plan does not change that schedule.
- Depends on: none
- Evidence from our documents: not needed for COVERED.
- Concerns: the report skill (`agent-work-report`) was removed from master by PR 700 (SPEC.md Appendix B line 758 and row line 771), so on current master nothing runs this schedule. Whether the waker automations were re-pointed after PR 684 was not checked (debates/D11/VERDICT.md:107, UNVERIFIED). "Configurable" and "from FR-2" refer to Clay's report spec, which is not in our files.

### S08-F13 Daily run covers only what the orchestrator does not, never touches issue entries, is being phased out
- 655 says: The daily run covers "only what the orchestrator does not (section 7); it no longer touches issue entries and is being phased out" (body line 113; AC line 221 adds a test that it no longer touches issue entries).
- Status: NOT-COVERED
- Current plan: none found for the split of work; searched SPEC.md, DECISIONS.md, D11, OAG1, OAG2 for "daily run", "phased out", "issue entries", "rebuild". The plan adopts the living report (section 7 row E2, line 464; FR-45 to FR-48) and says the sweep and observer are the owner's surfaces (OAG1 line 63), but does not say the daily run stops rebuilding issue entries.
- Component: TUI-DASHBOARD (report views, what the owner sees). It depends on the report skill that PR 700 removed.
- Feature statement: Change the report so the daily run skips issue entries that `report-entry` owns and adds only ClickUp, direct messages, mentions and items with no issue.
- Done when: a test of the daily run over a folder holding coordinator-written entry files leaves those files byte-identical and still produces the non-issue sections.
- Depends on: S08-F11, S08-F12, owner decision B.3-1
- Evidence from our documents: techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md:823 "Daily report phased out for the living report (owner ruling 1) | designed; code still runs the daily pipeline". Line 810: `run.py refresh` "without `--run` it does nothing while a daily run holds the lock".
- Concerns: the report is configured for one person (`"person": "clayphi"`, FR-46 line 257), so this is Clay's setup. Not buildable until the owner decides B.3-1.

### S08-F14 Two runs never overlap (run lock)
- 655 says: "Two runs never overlap (the run lock of FR-2)" (body line 115). FR-2 is Clay's report spec, so the lock is the work-report run lock; section 1 line 27 adds a routing lock for the poll.
- Status: COVERED
- Current plan: SPEC.md FR-10 (line 200: `flock -n` around the cron entry); D02 verdict line 46 ("the per-repo lock (master `record.py:382`) on top: two lock layers that do not collide"); NFR-02 (line 215: one writer per file); SPEC.md line 125 (a wake may arrive twice; handling a round twice has no second effect). The report run lock is built in the report skill (techref OBSERVER...:1062: open run younger than budget gives a skip record and `sys.exit(3)`).
- Depends on: S08-F1, S08-F12
- Evidence from our documents: not needed for COVERED.
- Concerns: the report run lock lives in the skill removed by PR 700, so it is covered only once B.3-1 restores the skill. The poll-lock risk (525 s sweep against a 300 s tick) is unmeasured (D02 line 67).

### S08-F15 How the poll and the waker fit together
- 655 says: "How the poll and the spec's waker (FR-25) fit together: see the spec." (body line 115). A pointer only; 655 gives no rule here.
- Status: COVERED
- Current plan: D10 (SPEC.md section 2 row D10, line 86): wake file plus ack, mailbox and typed line as id-only nudges, the coordinator also pulls. FR-13 to FR-19 (lines 203-209) and FR-28 (line 230).
- Depends on: 655 wake format (another section)
- Evidence from our documents: not needed for COVERED.
- Concerns: "FR-25" in 655 is Clay's spec numbering. In our SPEC.md FR-25 is a different requirement (line 227, flag-less coordinator is person-opened); do not map one to the other.

## Section summary
- Clay's check table is mostly covered in effect: a read-only no-model poll (FR-10, FR-11), mailbox reading at `check --wait` (FR-28), a 5-minute coordinator sweep of every worker (FR-38, WC-16), the 07:00 report wakers (D02) and run locks.
- Two conflicts: the scheduler (655 wants an Orca automation and no cron; D02, FR-10 and section 7 row B2 keep cron, automation only as a tested fallback), and approving permission prompts plus the one interrupt (FR-40, OD-7, D15 D14).
- Five remaining features: configurable poll interval (WATCHER); the hourly Monday to Friday worker check and the meaning of `--hourly` (COORDINATOR); the mid-flight issue re-read (COORDINATOR); milestone-only entry updates (COORDINATOR); the daily-run split (TUI-DASHBOARD). The last two wait on the owner's B.3-1 decision about restoring the report skill.
- Builder caution: do not add a second cron entry for an hourly pass, and never implement permission-prompt approvals or interrupts from 655.
