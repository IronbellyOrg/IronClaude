# Section 01 analysis: How it works, end to end
Counts: COVERED 16, CONFLICT 10, NOT-COVERED 3 (29 features)

Scope: issue 655 body lines 21-29 (section 1, items 1 to 7), plus the acceptance criteria lines 215, 216 and 219 that touch it. Current plan = SPEC.md, DECISIONS.md (verdicts D01-D16, OD-*, OA-*), the debate VERDICT.md files and the tech references, all under /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/ (short paths below: SPEC.md = spec/SPEC.md, DECISIONS.md, D07 VERDICT = debates/D07/VERDICT.md). Item 4 (run the section 2 workflow) and the later items of 655 are other sections and are only named as dependencies.

Note on the word: the plan says "coordinator"; 655 says "orchestrator". Both are treated as the same role (DECISIONS.md:355, D08 item 1).

### S01-F1 Orca automation runs the poll every 5 minutes (configurable); no cron entry
- 655 says: An Orca automation runs the poll script every 5 minutes (configurable) (body line 23); acceptance criterion says "no cron entry exists" (line 215).
- Status: CONFLICT
- Current plan: D02 decided the opposite: cron with one dispatcher is the scheduler of record, one `*/5 * * * *` entry under `flock -n` (DECISIONS.md:179-182, SPEC.md:200 FR-10, SPEC.md:449 "B2 Orca automation as scheduler | REJECT"). 655's version is REJECTED. An Orca automation survives only as a tested-first fallback (DECISIONS.md:185).
- Component (NOT-COVERED only): n/a
- Feature statement (NOT-COVERED only): n/a
- Done when (NOT-COVERED only): n/a
- Depends on: none
- Evidence from our documents:
  - /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/DECISIONS.md:179 "cron with one dispatcher stays the scheduler ... Clay's precheck automation is kept as a tested-first fallback"
  - DECISIONS.md:198 "UNVERIFIED: that an automation fires headless on this host; the 100-row cap, 720-minute catch-up and survival of an image update"
  - DECISIONS.md:196 "both advocates called it a toss-up (about 50 and 55 percent)" (confidence 62 percent, status partial)
- Concerns: D02 is a partial verdict at 62 percent; its own reversal test is "a headless `*/5` automation with a `; exit 1` precheck fires for 1 to 24 hours with only skipped rows, survives an Orca restart, and a boot script creates exactly one automation" (DECISIONS.md:198). Cron is not yet in the image (Coder issue 515, DECISIONS.md:196). The plan fixes the interval at five minutes in the cron line; no configurable-interval key was found (searched SPEC.md FR-10, FR-12 and the config table row 2 at SPEC.md:172). Owner rule: the owner has not yet ruled in chat, so everything is a recommendation (SPEC.md:73).

### S01-F2 Reuse the work-report waker "precheck exits non-zero" pattern so Orca starts no agent
- 655 says: The schedule reuses the IronFlow waker pattern (`scripts/waker.py`, agent-work-report SKILL.md Input section); the automation runs the script as its precheck and the script exits non-zero so Orca starts no agent and leaves no terminal (line 23).
- Status: COVERED
- Current plan: D02 item 4 and D15 element B1: "precheck pattern" ADOPT+CHANGE as a fallback only (SPEC.md:449; DECISIONS.md:185): automation created `--disabled`, enabled after a scheduled shadow run, precheck that always returns 1 with a unit test, created by the owner. The same pattern already drives the two existing report automations (DECISIONS.md:186).
- Component (NOT-COVERED only): n/a
- Feature statement (NOT-COVERED only): n/a
- Done when (NOT-COVERED only): n/a
- Depends on: S01-F1
- Evidence from our documents: n/a (COVERED)
- Concerns: Covered as a fallback, not as the primary scheduler. The D02 verdict confirmed the precheck claim itself against the skill text ("exits non-zero so Orca starts no agent and leaves no terminal (VERIFIED 2026-11-03)", debates/D02/VERDICT.md:33). The `agent-work-report` skill, which holds `waker.py`, was removed from master by PR 700 (SPEC.md:758, Appendix B), so the pattern's code reference is gone until the owner restores it (SPEC.md:786 B.3 item 1).

### S01-F3 The poll routes new issues to the repo's orchestrator and wakes it only when something is new
- 655 says: The script routes each new issue to an orchestrator of the issue's repo (starting one if none) and wakes it only when something is new; one wake per orchestrator carries its share; each wake is addressed to one orchestrator, which refuses any other (lines 23, 216).
- Status: COVERED
- Current plan: D10 and FR-13: the poll writes an ids-only wake file (`repo`, `number`, `url`) before any nudge, three deliveries, the coordinator writes the ack (SPEC.md:203; DECISIONS.md:414-418). FR-28: the coordinator takes only wakes addressed to itself (SPEC.md:230). If no live session of the target tag exists the poll starts one (DECISIONS.md:421, D10 item 8). The routing "to a coordinator with a free place" in the plan is the in-flight cap (FR-33, SPEC.md:235).
- Component (NOT-COVERED only): n/a
- Feature statement (NOT-COVERED only): n/a
- Done when (NOT-COVERED only): n/a
- Depends on: S01-F18, S01-F20
- Evidence from our documents: n/a (COVERED)
- Concerns: The plan's wake carries ids only, no titles (DECISIONS.md:418), so 655's "information items" cannot ride in the wake as text (see S01-F7). "Starting one if none" is covered only for the single project coordinator; starting additional ones is rejected (S01-F21). D10 has two mandatory fixes (M1 ack after the state file, M2 abandoned-wake retarget; SPEC.md:205-206).

### S01-F4 With nothing new, no agent starts and no tokens are spent
- 655 says: With nothing new no agent starts and no tokens are spent (lines 3, 24, 215).
- Status: COVERED
- Current plan: The poll is a script run by cron (no model); it starts a session only to claim or wake (SPEC.md:125 section 3.1; FR-10 SPEC.md:200; FR-13 SPEC.md:203). The poll "writes nothing to GitHub" and reads with seven read-only `gh` calls (SPEC.md:133 diagram).
- Component (NOT-COVERED only): n/a
- Feature statement (NOT-COVERED only): n/a
- Done when (NOT-COVERED only): n/a
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: The plan has no explicit acceptance test named "a cycle with no new items starts no agent and spends no tokens"; searched SPEC.md section 13.2 live firing tests (line 698) and FR-10/FR-13 checks by reading their rows only, so UNVERIFIED whether a test row covers it.

### S01-F5 Find new issues assigned to the user; only the user's own login counts
- 655 says: The script finds, since the last poll, new issues assigned to the user; only the user's own GitHub login counts (line 24).
- Status: COVERED
- Current plan: FR-01: start only if the issue is open and "assigned only to the watcher login" (SPEC.md:191; D01 item 1, DECISIONS.md:152). The store (`dispatch.json`) keeps per-issue state so the poll does not redo an issue (SPEC.md:173). FR-03 keeps `marker_in_window` so a hand claim and a poll start never run two workers (SPEC.md:193).
- Component (NOT-COVERED only): n/a
- Feature statement (NOT-COVERED only): n/a
- Done when (NOT-COVERED only): n/a
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: The plan reads "assigned only to" the login (sole assignee), which is stricter than 655's wording; 655 does not say what happens to an issue with two assignees. Whether a read-only user can self-assign is UNVERIFIED (DECISIONS.md:169). The "since the last poll" window is not stated in the plan as a time window; the plan decides from stored per-issue state instead. A start also needs the approval (see S01-F6).

### S01-F6 Assignment is the only trigger; the hold is a precondition, not an approval
- 655 says: "Only assignment triggers a claim" (line 24) and "Assignment stays the only trigger: the hold is a precondition, not an approval" (line 25).
- Status: CONFLICT
- Current plan: D01 decided the opposite: "Assignment alone never starts work"; a worker starts only with the person's approval (`Approved` field, unedited since), an allowed Status, no `hold:backlog` and a passing plan check (DECISIONS.md:152; SPEC.md:191 FR-01; SPEC.md:447 "A12 assignment alone as trigger | REJECT"; D15 A12, debates/D15/VERDICT.md:52). 655's version is REJECTED. Clay's "conditions to revisit" are kept as a documented path (DECISIONS.md:157).
- Component (NOT-COVERED only): n/a
- Feature statement (NOT-COVERED only): n/a
- Done when (NOT-COVERED only): n/a
- Depends on: none
- Evidence from our documents:
  - DECISIONS.md:152 "Assignment alone never starts work. A worker starts only when: ... an allowed approver's approval ... is present and unedited since"
  - DECISIONS.md:157 "Assignment alone may be reconsidered only when all four hold: the launch guard refuses to start when not effective; workers cannot push or merge; ... the owner records the reversal in chat."
  - DECISIONS.md:169 "Partial convergence ... Confidence 78 percent."
- Concerns: D01 is HYBRID, partial, 78 percent; OA-1 (both gates or only the start gate) is still an owner question (SPEC.md:779). Owner rule: no worker starts on assignment alone.

### S01-F7 The poll also reports comments that mention the user, issues that could be assigned, and issues and pull requests that affect the user's work (information items)
- 655 says: The script also finds comments mentioning the user, issues that could be assigned to the user, and issues and PRs that affect the user's work; these are passed on as information, with only assignment triggering a claim (line 24).
- Status: CONFLICT
- Current plan: FR-09: the three info streams (`mentions`, `could_assign`, `affects`) go behind an off switch, default off; if enabled, only `could_assign`, after capturing the reply shapes (SPEC.md:199). OD-9: "No list of newly assignable issues; info streams off with a switch" (SPEC.md:105; DECISIONS.md:893). 655's always-on version is REJECTED; an opt-in switch exists. The org-wide search is also off in the first build (DECISIONS.md:329, D07 item 6).
- Component (NOT-COVERED only): n/a
- Feature statement (NOT-COVERED only): n/a
- Done when (NOT-COVERED only): n/a
- Depends on: none
- Evidence from our documents:
  - DECISIONS.md:893 "Keep the info streams off ... Reason: the replies of the three searches were never captured (U8), and two of the three are subsets of what the report skill already collects"
  - DECISIONS.md:893 "in PR 686 the streams are not behind any switch today and a failed search stops the whole discovery cycle"
  - DECISIONS.md:895 "Cost if enabled: about 8 of 35 calls per cycle."
- Concerns: The wake carries ids only, no free GitHub text (DECISIONS.md:418), so passing information as text is blocked by D10 item 5. The report's `involves` search (which covers mentions) is gone from master with the skill (SPEC.md:758). UNVERIFIED: reply shapes of the three searches (U8).

### S01-F8 At switch-on, the issues already assigned count as seen (baseline)
- 655 says: At switch-on the issues already assigned count as seen; an older one is handed over with `/sc:orchestrator --take <repo>#<N>` (line 24).
- Status: NOT-COVERED
- Current plan: none found as a requirement; searched SPEC.md for "baseline", "seen", "switch-on", "already assigned" (only unrelated hits at lines 10, 52, 141), DECISIONS.md, FOLLOW-UPS.md, and the D01, D09, Q03, OAG3 verdicts. The plan only records the behaviour as a fact about PR 686 ("Issues assigned before switch-on are marked seen in PR 686 and never woken; an approved one needs `--take`", DECISIONS.md:162). Under the plan's approval gate an old approved issue would simply start on the first enabled poll. Mitigation in the plan is process-only: every repo off and at most one throwaway repo with cap 1 first (DECISIONS.md:1267 OA-19).
- Component (NOT-COVERED only): WATCHER. Reason: it is a first-poll rule of the discovery poll and its state store.
- Feature statement (NOT-COVERED only): On a repo's first enabled poll, the watcher records every issue that is already assigned and approved as seen so it is never woken or started, and a person can hand one over with `/sc:coordinator --take`.
- Done when (NOT-COVERED only): A dry run on a repo with an already assigned approved issue shows `would_baseline` for it, the real first poll starts no claim for it, and `--take <owner/repo#N>` on that issue is accepted.
- Depends on: S01-F9, S01-F5
- Evidence from our documents:
  - debates/D01/VERDICT.md:59 "Issues assigned before switch-on are baselined as 'seen' in PR 686 and never woken, so an approved one needs `--take` (INV-009)."
  - debates/D09/VERDICT.md:34 "a baseline that never touches the 17 already-assigned issues (`:492`)"
  - debates/D09/VERDICT.md:41 "`--dry-run` that shows the holds before any write, plus the switch-on baseline ... they become the gate in recommendation item 4."
  - DECISIONS.md:1267 "Every repo off (`enabled: false`, `auto_enable` false); at most one throwaway repo after the `--dry-run` shadow run, cap 1"
- Concerns: The baseline is code in PR 686 that the plan adapts; whether the adapted PR keeps it is not stated (UNVERIFIED, PR 686 code not read). The D09 reference to the baseline as the switch-on gate was tied to the label write that was rejected, so the baseline may be dropped by accident unless a requirement names it.

### S01-F9 Hand over an older issue by hand with `--take`
- 655 says: An older already assigned issue is handed over with `/sc:orchestrator --take <repo>#<N>` (line 24).
- Status: COVERED
- Current plan: FR-24 lists the flag `--take <owner/repo#N>` on `/sc:coordinator` (SPEC.md:226; D08 item 2, DECISIONS.md:356); FR-25 says grants have one door, `--wake` or `--take`, on a recorded authorization (SPEC.md:227).
- Component (NOT-COVERED only): n/a
- Feature statement (NOT-COVERED only): n/a
- Done when (NOT-COVERED only): n/a
- Depends on: S01-F8
- Evidence from our documents: n/a (COVERED)
- Concerns: Name differs (`/sc:coordinator`, key form `owner/repo#N`); the command name `/sc:orchestrator` is rejected (D08). What `--take` does step by step is in another section of 655 (flags); not classified here.

### S01-F10 An unacknowledged wake is tried up to 3 times
- 655 says: An unacknowledged wake is tried up to 3 times (line 24).
- Status: COVERED
- Current plan: FR-13: "three deliveries 10 minutes apart, then mark the Orca workspace unread and exit 7; the poll never writes the ack" (SPEC.md:203; DECISIONS.md:414).
- Component (NOT-COVERED only): n/a
- Feature statement (NOT-COVERED only): n/a
- Done when (NOT-COVERED only): n/a
- Depends on: S01-F3
- Evidence from our documents: n/a (COVERED)
- Concerns: none

### S01-F11 Plan check by script: Priority, Fix approach and Test plan each present once and filled in
- 655 says: Before an assigned issue is sent on, the poll checks its body with a script: `## Priority`, `## Fix approach`, `## Test plan` must each be present once and filled in (line 25).
- Status: COVERED
- Current plan: FR-05 (read-only plan check on the body before the approval read; skip as `held_incomplete`; a `<...>`-only section counts as empty; SPEC.md:195), FR-54 (one reference check `plan_body.py check`, a package copy with a parity test; SPEC.md:275), D09 item 1 (DECISIONS.md:386), D15 A1 and A2 (debates/D15/VERDICT.md:41-42).
- Component (NOT-COVERED only): n/a
- Feature statement (NOT-COVERED only): n/a
- Done when (NOT-COVERED only): n/a
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: The check runs in memory only; the body never enters the audit log, store, argv or a typed line (DECISIONS.md:391). Presence is not quality (SPEC.md:275). `plan_body.py` lives in PR 690, still a draft (SPEC.md:274 FR-53).

### S01-F12 A failing issue gets the label `hold:plan` (a label only, never a comment)
- 655 says: An issue that fails gets the label `hold:plan` (label only, never a comment) and is not sent to an orchestrator (line 25).
- Status: CONFLICT
- Current plan: The "not sent on" part is covered (skip `held_incomplete`, FR-05). The label write is rejected: "Write nothing to GitHub in a poll cycle (NG-2)"; strip the label writer of PR 686 (SPEC.md:196 FR-06); D15 A5 "REJECT now; deferred PR" (SPEC.md:443; debates/D15/VERDICT.md:45); D09 and Q03. A leftover `hold:plan` is ignored (SPEC.md:197 FR-07). The hold exists only as a local `holds` entry with no write. 655's label write is REJECTED for now.
- Component (NOT-COVERED only): n/a
- Feature statement (NOT-COVERED only): n/a
- Done when (NOT-COVERED only): n/a
- Depends on: S01-F11
- Evidence from our documents:
  - DECISIONS.md:388 "The label write is deferred, not rejected. If the owner later wants a visible mark, the only poll write allowed is add or remove of the existing `hold:plan` label, only in a repo holding the `issue.hold` grant, and NG-2 is amended at that time"
  - DECISIONS.md:389 "Switch-on gate for item 3: a 24-hour `--dry-run` shadow run showed the holds, and a test showed `gh` can add and remove a label under cron's minimal environment."
  - DECISIONS.md:396 "With no label, a held issue shows only in `issue-watch status` and the audit log ... or a plan-less issue is invisible"
  - debates/D09/VERDICT.md:30 "the label write is the costly part of Clay's hold and its dormant form is unclean"
- Concerns: Owner rule NG-2: the poll never writes to GitHub (DECISIONS.md:84; SPEC.md:218 FR-82). D09 is partial at 78 percent; it would fall "if the owner decides GitHub visibility of a hold is required now" (debates/D09/VERDICT.md:77). UNVERIFIED: whether anyone reads `hold:plan`.

### S01-F13 The poll removes `hold:plan` when the check passes
- 655 says: When the check passes, the poll removes the label (line 25).
- Status: CONFLICT
- Current plan: Same decision as S01-F12: the poll writes no label, so it never removes one (SPEC.md:196 FR-06; SPEC.md:443 A5; `hold_released` has no producer and leaves the reason table, debates/D15/VERDICT.md:45). 655's version is REJECTED for now.
- Component (NOT-COVERED only): n/a
- Feature statement (NOT-COVERED only): n/a
- Done when (NOT-COVERED only): n/a
- Depends on: S01-F12
- Evidence from our documents:
  - SPEC.md:197 "ignore a leftover `hold:plan`"
  - debates/D15/VERDICT.md:45 "The reasons `hold_applied`, `hold_released`, `hold_removed_by_hand`, `hold_write_failed` then have no producer and leave the table"
- Concerns: With no removal, a label a person or an older run placed stays on GitHub forever; the plan accepts this by ignoring it.

### S01-F14 A person's `hold:backlog` label makes the system do nothing with the issue
- 655 says: A person's label `hold:backlog` makes the system do nothing with the issue until it is removed (line 25).
- Status: COVERED
- Current plan: FR-01 and FR-05: skip `hold:backlog` as `held_backlog`; the poll only reads it; only a person places it (SPEC.md:191, 195; D09 item 2, DECISIONS.md:387; D15 A3, debates/D15/VERDICT.md:43). The start-time and wake-time re-check also tests it (FR-02, FR-08).
- Component (NOT-COVERED only): n/a
- Feature statement (NOT-COVERED only): n/a
- Done when (NOT-COVERED only): n/a
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: "Do nothing" in 655 also covers the coordinator side (wave 1 re-reads the issue for `hold:backlog`); the coordinator side belongs to 655 section 2.

### S01-F15 A hold removed by hand stays removed
- 655 says: A hold removed by hand stays removed (line 25).
- Status: CONFLICT
- Current plan: The plan deletes the code for this: the `hand_removed` state and the label rows of `_hold_step` are stripped (SPEC.md:196 FR-06; debates/D15/VERDICT.md:45). With no `hold:plan` label, there is nothing to remove by hand; the check simply runs on every poll, so a person cannot override a failing plan check except by filling in the plan. 655's version is REJECTED (moot).
- Component (NOT-COVERED only): n/a
- Feature statement (NOT-COVERED only): n/a
- Done when (NOT-COVERED only): n/a
- Depends on: S01-F12
- Evidence from our documents:
  - SPEC.md:196 "strip the label writer of PR 686 ... label rows 3-5 of `_hold_step` ... `hand_removed`"
  - debates/D09/VERDICT.md:30 "the label drags in rows 3 to 6, a `hand_removed` state and a live read"
- Concerns: A person who wants to push a thin issue through anyway has no override in the plan except to write the three sections; the plan does not discuss this (searched DECISIONS.md D09 and Q03 entries; no evidence found of an override decision).

### S01-F16 After one hour with no plan work, send ONE plan request to the repo's orchestrator (plan through `/sc:issue --plan`)
- 655 says: After one hour with no plan work elsewhere the poll sends ONE plan request to the repo's orchestrator, which makes the plan through `/sc:issue --plan` (line 25). An open plan request takes a place in the in-flight count (line 27); acceptance criterion line 219 repeats the one-hour rule.
- Status: NOT-COVERED
- Current plan: none found as a requirement; D15 A4 decided "Defer": "Not built now; if built, ids only and after D07 settles who plans" (debates/D15/VERDICT.md:44; SPEC.md:442). D09 item 5 and Q03 item 3 call it "a wake-file item, not a GitHub write" and keep the local `holds` entry and quiet-hour clock for it (DECISIONS.md:390, 714). The pieces that exist: `/sc:issue --plan` and `--remaining` (PR 690, a draft; FR-53, FR-59), the local `holds` entry (FR-07). Searched: "plan request", "one hour", "plan_requests", "quiet" in SPEC.md, DECISIONS.md, FOLLOW-UPS.md, D09, D15, Q03 verdicts.
- Component (NOT-COVERED only): WATCHER. Reason: the one-hour clock, the single request and the wake item belong to the poll and its store; the plan creation itself is the coordinator's (655 section 5).
- Feature statement (NOT-COVERED only): The watcher sends one ids-only plan-request wake item to the repo's coordinator when an assigned issue has failed the plan check for one hour with no change, and counts that open request as in flight.
- Done when (NOT-COVERED only): With a fixture issue that fails the plan check for 60 minutes, the poll writes exactly one wake item of kind plan request (ids only, no title), writes nothing to GitHub, sends no second request on later polls, and the in-flight count includes it.
- Depends on: S01-F11, S01-F18, 655 section 5 plan mode (`/sc:issue --plan`)
- Evidence from our documents:
  - debates/D15/VERDICT.md:44 "A4 | Plan request after one hour, wake `plan_requests[]` with the issue title | Defer | A wake-file item, not a GitHub write (D09 item 5); a title is free GitHub text (D10 item 5)"
  - debates/Q03/VERDICT.md:71 "the one-hour plan request remains a wake-file item for D07. Because the wake-time re-check today needs the label ... leaving it unchanged would stop plan requests from ever firing in a read-only variant."
  - DECISIONS.md:714 "The local `holds` entry ... is created when a failing issue is first seen, so the one-hour quiet clock starts."
  - debates/D01/VERDICT.md:16 "the plan request is an agent edit of the issue body, and any body edit after the approval voids it"
- Concerns: Two traps for the builder. (1) Order: a plan written after approval voids the approval (D01 item 5, SPEC.md:194 FR-04), so a plan request must complete before the person approves. (2) 655's wake carries the issue title; the plan forbids titles in wakes (ids only, DECISIONS.md:418). The "who plans" question (D07) is settled for the coordinator but the plan-request consumer is not built. The plan's `plan_depth` default is `quick` (FR-59, SPEC.md:280) while 655 says the `plan_tier` default is `tier1b`; that is another section.

### S01-F17 One orchestrator per repo
- 655 says: One orchestrator per repo (line 27).
- Status: COVERED
- Current plan: D07: "Coordinator session, branch, worktree and records live in each project" (DECISIONS.md:324); name `COORD-<RepoName>` in the `Coordinator` worktree (SPEC.md:125; D08 item 7, DECISIONS.md:361). Until Coder issue 516 lands, `ORCH-IronClaude` holds the duties (DECISIONS.md:327).
- Component (NOT-COVERED only): n/a
- Feature statement (NOT-COVERED only): n/a
- Done when (NOT-COVERED only): n/a
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: Coder issues 515 and 516 are in another repo and unverified (DECISIONS.md:342). The plan's "one" is one standing coordinator; 655 allows more than one (see S01-F21).

### S01-F18 At most 3 issues in flight per orchestrator (`max_in_flight`)
- 655 says: At most 3 issues in flight each; `max_in_flight` in `repos.yaml` (line 27).
- Status: COVERED
- Current plan: FR-33: `max_in_flight` checked in the child cycle after the sweep, per coordinator id, default 3 (SPEC.md:235; D07 item 3, DECISIONS.md:326). A full repo records `coordinator_full` (SPEC.md:210 FR-20).
- Component (NOT-COVERED only): n/a
- Feature statement (NOT-COVERED only): n/a
- Done when (NOT-COVERED only): n/a
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: The key lives in the per-repo JSON, not `repos.yaml` (the hand-kept `repos.yaml` allow list is removed, DECISIONS.md:325; SPEC.md:201 FR-11). "First build enforces 1 until claim agents have their own worktree" (SPEC.md:235; DECISIONS.md:331 defect). A hand-back waiting for re-approval does not count (OD-13, SPEC.md:109).

### S01-F19 What "in flight" means: from routing until closed, dropped or escalated
- 655 says: In flight runs from the moment the poll routes the issue until it is closed, dropped or escalated (line 27).
- Status: COVERED
- Current plan: FR-33 counts store entries `pending`, `launched`, `claimed`, `woken`, `acked`, `unknown` and open claim files, once per issue; "The poll closes a store entry from the per-issue phase" (SPEC.md:235). The window start (pending is written before anything is sent) is in D07 item 3 (DECISIONS.md:326).
- Component (NOT-COVERED only): n/a
- Feature statement (NOT-COVERED only): n/a
- Done when (NOT-COVERED only): n/a
- Depends on: S01-F16 (plan request counted as a place)
- Evidence from our documents: n/a (COVERED)
- Concerns: D07 admits "'In flight' needs a named closing writer and an expiry (not yet designed)" (DECISIONS.md:326); FR-33 gives the poll as closing writer but "escalated" and "dropped" as end states are not named in the plan (searched FR-33, FR-35). The plan-request place is carried by S01-F16.

### S01-F20 The poll alone routes each issue, under its lock
- 655 says: The poll alone routes each issue, under its lock, to an orchestrator of the repo with a free place (line 27; also line 216).
- Status: COVERED
- Current plan: D07 item 1: one child cycle per project "with its own lock, state directory, kill switch and day cap" (DECISIONS.md:324); NFR-02 one writer per file (SPEC.md:215); FR-33 cap check inside the child cycle (SPEC.md:235). The poll writes the store and wakes; the coordinator writes acks and per-issue files (SPEC.md:215).
- Component (NOT-COVERED only): n/a
- Feature statement (NOT-COVERED only): n/a
- Done when (NOT-COVERED only): n/a
- Depends on: S01-F18
- Evidence from our documents: n/a (COVERED)
- Concerns: "to an orchestrator with a free place or starts another" is rejected (S01-F21).

### S01-F21 When the repo's orchestrator is full, the poll starts another orchestrator for the same repo
- 655 says: The poll routes each issue to an orchestrator of the repo with a free place, "or starts another" (line 27; line 216 "or starts another").
- Status: CONFLICT
- Current plan: D07 item 2 removes "extra poll-started orchestrators per repo"; a full repo records `coordinator_full` and the issue waits (DECISIONS.md:325-326; SPEC.md:210 FR-20, SPEC.md:235 FR-33; D15 C5 REJECT, SPEC.md:454). 655's version is REJECTED.
- Component (NOT-COVERED only): n/a
- Feature statement (NOT-COVERED only): n/a
- Done when (NOT-COVERED only): n/a
- Depends on: S01-F17
- Evidence from our documents:
  - debates/D07/VERDICT.md:16 "removes ... the 30-minute idle end, the poll starting extra orchestrators for one repo, the `wrong_target` refusal"
  - debates/D07/VERDICT.md:78 "The 'one orchestrator per repo' wording is replaced."
  - debates/D09/VERDICT.md:77 "It would fall ... if D07 keeps several orchestrators per repo so the lease comment and plan request must be written by the poll side."
- Concerns: D07 found that claim agents launch into the same `Coordinator` worktree as the standing coordinator, against "one live agent per worktree" (DECISIONS.md:331), so more than one agent per project is a known defect the plan avoids by cap 1.

### S01-F22 An idle orchestrator ends
- 655 says: "An idle one ends" (line 27; line 216).
- Status: CONFLICT
- Current plan: D07 item 2 removes the 30-minute idle end (DECISIONS.md:325); the coordinator is a standing project session (SPEC.md:125). The restart rule is "no idle end" (debates/D07/VERDICT.md:41, "Override: no idle end"). 655's version is REJECTED.
- Component (NOT-COVERED only): n/a
- Feature statement (NOT-COVERED only): n/a
- Done when (NOT-COVERED only): n/a
- Depends on: S01-F17
- Evidence from our documents:
  - DECISIONS.md:325 "Remove ... the 30-minute idle end, extra poll-started orchestrators per repo, the `wrong_target` refusal"
  - debates/D07/VERDICT.md:41 "Guarded restart with resume ... Override: no idle end."
- Concerns: Without an idle end a coordinator session keeps its context and cost open; the plan accepts this because the coordinator is a person-visible standing session. UNVERIFIED: idle cost of a standing coordinator; not measured in the documents read.

### S01-F23 A dead orchestrator is restarted
- 655 says: "a dead one is restarted" (line 27; line 216).
- Status: COVERED
- Current plan: FR-34: restart a dead coordinator with a resume wake, at most 3 times (stored counter); an unreadable terminal list restarts nothing; key `coordinator_session` (SPEC.md:236; D07 item 4, DECISIONS.md:327).
- Component (NOT-COVERED only): n/a
- Feature statement (NOT-COVERED only): n/a
- Done when (NOT-COVERED only): n/a
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: Until Coder 516 creates `COORD-<RepoName>`, nothing restarts and `ORCH-IronClaude` holds the duties (SPEC.md:236).

### S01-F24 The report coordinator stays a separate session
- 655 says: "the report coordinator stays separate (spec 5.7)" (line 27).
- Status: COVERED
- Current plan: D08 item 3 names "report coordinator" as its own kind; item 6 says "The report session keeps its names (tag `coordinator`, prefix `coordinator-`, state `.dev/coordinator/`)" (DECISIONS.md:357, 360).
- Component (NOT-COVERED only): n/a
- Feature statement (NOT-COVERED only): n/a
- Done when (NOT-COVERED only): n/a
- Depends on: none
- Evidence from our documents: n/a (COVERED)
- Concerns: The report skill and its waker automations are gone from master (PR 700), so the report coordinator has no skill behind it until restored (SPEC.md:786).

### S01-F25 Repo list and repo-to-checkout map come from the private repo `IronbellyOrg/IronOrchestrator`, where the sessions run
- 655 says: The orchestrator reads the repo list and the repo-to-checkout map from the private orchestrator repo `IronbellyOrg/IronOrchestrator`, where the orchestrator sessions run, not from IronClaude configuration (line 28). Acceptance line 228 repeats it ("coordinator spec and work report state live in the orchestrator repo").
- Status: CONFLICT
- Current plan: D07 decided the opposite: "Remove the separate registry repo `IronbellyOrg/IronOrchestrator`, `.orchestrator/orchestrators.json`, the hand-kept `repos.yaml` allow list" (DECISIONS.md:325); repos come from `orca repo list` with one JSON config per project in `~/.config/superclaude/issue-watch.d/` (SPEC.md:201 FR-11; SPEC.md:172 config row); sessions run in each project's `Coordinator` worktree (SPEC.md:125). D15 C5 REJECT (SPEC.md:454). 655's version is REJECTED.
- Component (NOT-COVERED only): n/a
- Feature statement (NOT-COVERED only): n/a
- Done when (NOT-COVERED only): n/a
- Depends on: none
- Evidence from our documents:
  - SPEC.md:201 "a failed list is an error, never 'zero repos' ... no registry repository, no `repos.yaml`"
  - debates/D07/VERDICT.md:16 "Test: a grep of the unified spec for `orchestrators.json` and `repos.yaml` finds only the 'rejected' table."
  - DECISIONS.md:340 "Clay's rulings 8 and 9 are Clay's, not the repository owner's."
- Concerns: A cited read-only `gh` call against `IronbellyOrg/IronOrchestrator` returned `private: true` during D07 (DECISIONS.md:342); the repo exists but is not used. Owner rule: the plan's direction (project-local coordinators) was decided by the owner, but layout and names were not (DECISIONS.md:333).

### S01-F26 Workers start in the issue's own repo and a worktree there
- 655 says: Workers start in the issue's own repo and a worktree there (line 28).
- Status: COVERED
- Current plan: FR-29 (adopt a claim, copy `.dev/issues/<N>/` into the worker worktree, read `launch_cwd` through `state`; SPEC.md:231); FR-30 (every worker started bound to the guard through `orca_worktree.py pending --level worktree` and the marker; SPEC.md:232). The coordinator lives in the same project, so the worker's repo is the coordinator's repo (D07 item 1).
- Component (NOT-COVERED only): n/a
- Feature statement (NOT-COVERED only): n/a
- Done when (NOT-COVERED only): n/a
- Depends on: S01-F17
- Evidence from our documents: n/a (COVERED)
- Concerns: A repo with no checkout is a skip reason `no_checkout` (SPEC.md:210; SPEC.md:454 C7). FR-30's launch-timeout of 60 s is UNVERIFIED (SPEC.md:232).

### S01-F27 The report is a living document
- 655 says: "The report is a living document (Clay, 2026-11-19)" (line 29).
- Status: COVERED
- Current plan: D11 and D15 E2: living report adopted with change (per-user state path, entries store only `session_id`; SPEC.md:464; DECISIONS.md:450); FR-45, FR-46, FR-48 (SPEC.md:256-259).
- Component (NOT-COVERED only): n/a
- Feature statement (NOT-COVERED only): n/a
- Done when (NOT-COVERED only): n/a
- Depends on: 655 section 7
- Evidence from our documents: n/a (COVERED)
- Concerns: The carrier is gone: PR 700 removed the `agent-work-report` skill from master; adoption "means restoring it from the archive branch in a later owner-approved PR" and FR-45, FR-46, FR-48 are "blocked until the skill is restored" (SPEC.md:464, 778; DECISIONS.md:462). Owner decision B.3 item 1 is open (SPEC.md:786).

### S01-F28 The daily run no longer touches issue entries; the daily report is being phased out
- 655 says: "the daily run no longer touches issue entries; the daily report is being phased out (section 7)" (line 29); acceptance line 221 adds a test for it.
- Status: NOT-COVERED
- Current plan: none found as a requirement. The plan adopts the living report (S01-F27) but states no rule that the daily run skips orchestrated issue entries and no phase-out of the daily report. Searched: "daily", "phased out", "phase out", "exclude" in SPEC.md, DECISIONS.md, FOLLOW-UPS.md, D11 and D15 verdicts, merged-requirements.md, and the observer/sweep tech reference. FR-50 keeps the report's silent-loss rules and `run.py gate` as they are (SPEC.md:261).
- Component (NOT-COVERED only): TUI-DASHBOARD. Reason: it decides what the owner sees in the report views and which report shows an issue.
- Feature statement (NOT-COVERED only): The daily report run leaves out every issue that has a living-report entry, so each issue appears in one report only, and the daily run is retired once the living report covers its content.
- Done when (NOT-COVERED only): A test with one entry file and a matching issue shows the daily run's output has no block for that issue (the entry's url, `pr_url` and session links are excluded) and the entry file is byte-identical after the daily run.
- Depends on: S01-F27, 655 section 7
- Evidence from our documents:
  - techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md:809 "`exclude.py`: ... removes the issue url, the entry's `pr_url` and each `orca://session/<id>`; ... With no entry files it excludes nothing."
  - techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md:823 "Daily report phased out for the living report (owner ruling 1) | designed; code still runs the daily pipeline"
  - DECISIONS.md:462 "Every action that builds on PR 684's report skill ... is SUPERSEDED: the skill was removed from master."
  - debates/D11/VERDICT.md:107 "Whether Clay uses the daily report and whether its Orca waker automations were re-pointed after PR 684 ... not checked."
- Concerns: Moot on master today: the daily pipeline and `exclude.py` live in the removed skill (SPEC.md:758). The label "owner ruling 1" in the tech reference is UNVERIFIED as to who ruled (DECISIONS.md:456 says Clay's ruling 39 is "Clay's, not the owner's"); do not treat the phase-out as an owner decision. Builder should only build this after the owner decides whether to restore the skill (SPEC.md:786 B.3 item 1).

### S01-F29 Acceptance number: the closed reason table has exactly 62 names
- 655 says: "The closed reason table has exactly 62 names" (line 215).
- Status: CONFLICT
- Current plan: FR-20: the reasons table must equal the code: restore 14 approval reasons, add `coordinator_full`, `name_collision`, `no_checkout`, `coordinator_absent`, remove `registry_invalid`, `repo_not_listed` and four label-write reasons (SPEC.md:210; D15 E6, DECISIONS.md:585 "E6 62-reason audit table: adopt with change (bring back 14 approval reasons, add three, drop label-write reasons)"). The final count therefore differs from 62; the new total is not stated (UNVERIFIED; I did not compute it from code). 655's "exactly 62" is REJECTED as a fixed number.
- Component (NOT-COVERED only): n/a
- Feature statement (NOT-COVERED only): n/a
- Done when (NOT-COVERED only): n/a
- Depends on: 655 reason-table section (not classified here)
- Evidence from our documents:
  - SPEC.md:210 "Hold a reasons table equal to the code ... remove ... four label-write reasons"
  - debates/D15/VERDICT.md:45 "recompute the pin" (the reasons `hold_applied` ... "leave the table (my inference from Q03; recompute the pin)")
  - DECISIONS.md:585 "E6 62-reason audit table: adopt with change"
- Concerns: A builder must not pin 62 in a test; MC-10 (the mechanical check for the table) is the controlling test (SPEC.md:210).

## Section summary
- 29 features split out of section 1. 16 are covered by the current plan (poll mechanics, wake transport and retries, plan check, `hold:backlog`, one coordinator per repo, cap of 3, restart, report coordinator, worker location, living report), 10 conflict and are rejected, 3 are not covered.
- The biggest rejected parts: an Orca automation as scheduler (D02, cron wins), assignment as the only trigger (D01), the `hold:plan` label writes and hand-removal rule (D09, Q03, NG-2), always-on info streams (OD-9), extra poll-started and idle-ending orchestrators and the `IronOrchestrator` registry repo (D07).
- Not covered: the switch-on baseline of already assigned issues (WATCHER), the one-hour plan request with its in-flight place (WATCHER, deferred as D15 A4), and the daily-run exclusion and daily-report phase-out (TUI-DASHBOARD, moot until the report skill removed by PR 700 is restored).
- Builder cautions: the plan's wake carries ids only, so 655's titles in plan requests and information items need a different carrier; the report-side rows depend on the owner's open decision to restore the PR 684 skill (SPEC.md:786).
