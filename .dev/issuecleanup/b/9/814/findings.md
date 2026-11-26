# Round 2 findings for issue 814 (W6: Shadow-run acceptance check, every cycle ends with exit 0 or a named reason)

Checked 2026-11-24 on master f2894fc44 (worktree Realign). Issue 814 is OPEN, sub-issue of umbrella #717 (watcher). Read-only. Round 1 file: `/home/coder/workspaces/worktrees/IronClaude/Analyze717/.dev/issuecleanup/a717/2/814/findings.md`. Plan files: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/` (SPEC = `spec/SPEC.md`, DEC = `DECISIONS.md`). Owner records (REQ): `/home/coder/workspaces/worktrees/IronClaude/Realign/.dev/releases/backlog/issue-watcher-zero-setup/requirements.md`.

Defect in the issue text: the body of 814 is W6 followed by a copy of W7 to W15 (108 lines). "Done when ... the item below" is ambiguous. Trim it to W6 whatever is decided.

## Alignment with architectural decisions

- **R18 (REQ:44) and R28 (REQ:54): CONFLICT with the item's premise.** The owner replaced "the shadow run, lock test and restart test of the runbook" with one automatic first-run check per repo; R28 puts the lock and restart tests inside it. REQ:106-107: switch-on "is no longer a manual gate"; only the live-test record stays an owner check. W6's "after the 24-hour shadow run" and "any other exit blocks switch-on" contradict this. Code: `first_run.py` (6 checks, built; REQ:93 Task 21).
- **R7 (REQ:38): CONFLICT.** "check-config, init-state, the shadow run run automatically when the watcher is initialised": the shadow run is already automatic, not a person's gate.
- **R38 (REQ:64): CONFLICT in origin.** W6 comes from issue 655 section 12 (Clay's design, which carried the cron shadow run). R38 adopts no Clay element. PR 729 still lets uncovered features be tracked in #717.
- **D02 (DEC:175-198; `debates/D02/VERDICT.md`) and FR-10 (SPEC:200): partly aligned; the item's "Watch out" cites the losing side.** The item says "Cron hides exit 75 under the detach (D02 position, position-CLAY.md:19)". D02's winner is HYBRID with cron kept; under the dispatcher the cron log prints each child as `<repo>: ran <reason> exit=<n>` (`cli.py:392`) and the sweep treats exits 0, 5 and 75 as fine (`cli.py:380`). So the exit code is readable from the cron log. The conclusion "read the audit log and the cron log" still holds.
- **SPEC:705 (13.2 "Cron shadow run, 24 hours"), SPEC:45 ("not switched on before S17") and DEC:1119 (the S17 pass list "is a proposal, not an owner rule (UNVERIFIED)"): CONFLICT with what happened.** The watcher has been live since 2026-11-23 (#450 closing comment; 4689 cycle lines on this host). The plan's gate did not govern; how much of SPEC.md still stands after R38 is UNVERIFIED.
- **FR-20 (SPEC:210) and `REASON_TABLE` (`audit.py:26-104`, 59 names; `cycle.py:508-509`): aligned, with one gap.** The table equals the code for cycle lines. The cron log also holds names outside it: `list_failed`, `list_timeout`, `unreadable_list` (`repos.py:85-124`) and the sweep lines `sweep: error ...` and `sweep: unhealthy (a child failed)` (`cli.py:418-423`). A literal "named reason from the reasons table" check flags these, so "named" must be defined.
- **NFR-04 (SPEC:217): partly aligned.** Asks for status fields (last sweep, recent skips). A reader of the audit log is the missing piece for it too. `status_report` does not read the audit log (`cycle.py:1416-1418`).
- **NFR-05 (SPEC:343): partly aligned.** "Prove the live unknowns before the poll is enabled"; the poll is already enabled, so the evidence now comes after.
- **FR-23 (SPEC:213) versus R18: conflict between plan and owner rule, resolved by R18** (owner 2026-11-18, built); FR-23's "owner turns it on once after S17" is not what runs.
- **NG-2 / FR-06 / FR-82 (SPEC:196, :218): aligned.** A reader writes nothing to GitHub.
- **WORKER-CONTRACT.md and HOW-WE-WORK.md: none apply** (grepped: audit, exit codes, shadow; nothing on watcher exits).
- **Verdict files:** D02 and D09 (`debates/D09/VERDICT.md`, the shadow run as switch-on gate tied to the rejected label write) are the only ones that mention the shadow run; D09's gate was for the label write that the plan rejected.

## Complementary issues

- **#816 (W8, alert after three bad cycles):** both need one reader of `audit.jsonl` that classifies cycles by exit. Interface: the reader's output (cycle, exit, reason, named or not). W8 adds "consecutive" and an alert place.
- **#820 (W12, seven-day SLO review):** `slo_numbers` (`cycle.py:1497`) is the only code reading audit lines and has no production caller (5 callers, all tests, per codegraph_callers). W12 would read the same lines.
- **#823 (W15, runbook rewrite) and #774 (docs refresh):** runbook section 8.1 (`docs/designs/issue-watcher-setup.md:223-233`) holds the manual `grep` of non-zero cycles; it would point at the script.
- **#777 (map the manual pieces):** a script that replaces a manual check fits its goal.
- **#775 (a comment cancels an approval silently):** shows the same gap: exit-0 skips are invisible; W6 does not cover them.
- **#813 (W5, closed today):** the same premise; closed.

## Closest overlap

1. **#816 (W8)**, "Alert after three bad cycles". Shared: a reader that walks `audit.jsonl`, takes each cycle's exit and reason, and decides whether it is bad; both would be built on `audit.py` names. It covers about 35% of W6's done-when (the reader and the exit classification; not the cron log, not "named", not a one-shot run).
2. **#820 (W12)**: about 15% (reads the same lines for different numbers).
3. **#823 (W15)**: about 10% (the runbook text that would call the script).

## Standalone or merge

Test against #816:

| Test | W6 | W8 | If merged |
|---|---|---|---|
| Owner | watcher owner | watcher owner | same |
| Acceptance test | a script over the audit logs and the cron log lists zero unexplained non-zero cycles | three scripted failing cycles in a row make `status` exit non-zero; a good cycle clears it | one reader, two tests |
| Files touched | a new read-only script (reads both logs plus the `.1` rotation) | `cycle.py` `status_report`, `cli.py` | W6 becomes the first step of W8 |
| Build phase | any time; no gate left | after the alert place is chosen (SETUP section 12: never chosen) | W6's easy part waits on W8's open decision unless split in two steps |
| Risk if merged | a simple scan gets held by the alert-sink question | none | real, but fixable by ordering inside one issue |

Verdict: **merge into #816** (my recommendation; the owner decides). Reasons: after the premise is removed, what is left is "a reader that classifies cycles against named reasons", and W8 needs the same reader; two issues would produce two readers. The owner merged W1 into #716 on the same day for a similar reason. Keep W6's own acceptance line inside #816 as step 1 ("a one-shot scan of every audit log and the cron log and its `.1` file, failing on any non-zero cycle whose reason is not named, where named = `REASON_TABLE` plus `list_failed`, `list_timeout`, `unreadable_list`, `unhealthy`"), built before the alert-sink question is settled. Standing alone would be right only if the owner wants W6 as a runbook script with no `status` change and wants W8 dropped or deferred indefinitely; then keep W6 alone, P3, simple.

Host evidence (read-only, 2026-11-24 22:2xZ; this host only): 4689 cycle lines in `~/.local/state/superclaude/issue-watch/*/audit.jsonl`; 10 are non-zero, all with table names: `lock_held` 75 (3), `gh_timeout` 3 (3), `lock_missing` 6 (2), `launch_unknown` 7 (2). Cron log `~/.aidev/logs/issue-watch.log`: 4382 `exit=` lines (4375 exit 0, exit 3 x3, exit 6 x2, exit 7 x2), `sweep: error list_failed` x3, `list_timeout` x2, `sweep: unhealthy` x7, and no `exit=75` line, so the three `lock_held` audit lines did not come through the cron sweep (cause UNVERIFIED). A crash (`cycle_crashed`, exit 1, `audit.py:57`) is printed to stderr only (`cli.py:131-135`), so only the cron log can show it. So the scan on today's data finds no unexplained exit except the sweep-level names above.

## Closed issues and merged PRs checked

- **#813 (W5, closed 2026-11-24, not planned):** owner decision that R18 and R28 replaced the manual lock and restart tests; the persistence need moved to #822. Same premise as W6's "before switch-on".
- **#809 (W1, closed 2026-11-24, merged into #716):** precedent for merging.
- **#450 (closed, completed):** rollout done, shadow run and lock/restart replaced by the automatic check; live with 284 cycles at the time (280 exit 0, 2 `lock_missing`, 2 `launch_unknown`).
- **#331 (closed):** original watcher; shadow run left to #450.
- **#751 and PR 759 (merged):** retry of a failed first run; adds first-run robustness, no acceptance scan.
- **PR 707 (merged):** built `first_run.py` (R7, R18, R28) and `run-all`.
- **PR 485 (merged):** wrote runbook section 8.1 and the capture sheet; says the shadow run, lock and restart tests were owner-run and "still open" at that time.
- **PR 729 (merged):** records R38.
- **PR 447 (merged):** original poller with the reasons table.
- **#655 and #665 (closed, not planned):** origin of the item; nothing delivered.

## Updated recommendation

**Merge into #816** (W8), as its first step, after trimming W6 to: drop "after the 24-hour shadow run" and "blocks switch-on"; define "named"; read both the audit logs and the cron log with its `.1` rotation; delete the stale D02 sentence. If the owner keeps it separate: keep open with those changes, simple, S. Priority P3. Complexity simple, size S for the scan itself; the merged #816 stays medium. Changed from round 1 (keep open with changes, standalone): after #813 and #809 were handled on 2026-11-24 the owner's pattern is to fold premise-less items into the item that owns the remaining work, and W6's remaining work is #816's reader. The same fixes as round 1 stay, and R38 and the cron-log numbers are added.

## Scan record

- Lists read in full: open-issues.tsv 134 of 134; closed-issues.tsv 157 of 157; merged-prs.tsv 508 of 508.
- Search terms: shadow, audit, exit, reason, status, alert, SLO, first-run, lock, restart, runbook, switch-on, watcher, issue-watch, live test, acceptance.
- Opened in full (open): 717, 716, 774, 761, 777, 775, 770, 811, 812, 815, 816, 817, 819, 820, 821, 822, 823, 442 (18). Closed: 450, 331, 655, 665, 751, 809, 813 (7). Merged PRs: 447, 485, 707, 729, 759 (5).
- Master check: `/sc:analyze src/superclaude/cli/issue_watch --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/b/9/analyze`; report `/home/coder/workspaces/worktrees/IronClaude/Realign/.dev/issuecleanup/b/9/analyze/analyze-report.md` (findings 3, 4, 5).
- UNVERIFIED: why the three `lock_held` audit lines have no cron-log twin; other hosts; plan-file stage state after PR 700; whether the owner wants W8 at all.
