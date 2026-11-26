# Round 2 findings for issue 811 (W3: Configurable poll interval)

Checked 2026-11-24 on master f2894fc44 (worktree Realign). Issue 811 is OPEN, sub-issue of umbrella #717 (watcher). Read-only: nothing on GitHub or in the code was changed. Round 1 file: `/home/coder/workspaces/worktrees/IronClaude/Analyze717/.dev/issuecleanup/a717/1/811/findings.md`. Plan files: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/` (SPEC = `spec/SPEC.md`, DEC = `DECISIONS.md`). Owner records: `/home/coder/workspaces/worktrees/IronClaude/Realign/.dev/releases/backlog/issue-watcher-zero-setup/requirements.md` (REQ).

Defect in the issue text itself: the body of 811 is W3 followed by a copy of W4 to W15 (lines 21 to 137 of the body, 142 lines in all). "Done when: the item below is built" can therefore be read as the whole tail. Issue 823 (W15) already has a trimmed body. Fix the body whatever else is decided.

## Alignment with architectural decisions

The item asks for one named setting for the poll interval, "instead of hand-editing the cron line".

- **R38 (REQ:64, owner 2026-11-21): CONFLICT in origin, partly aligned in substance.** The owner discarded Clay's design; "configurable every 5 minutes" is Clay's wording (issue 655 body, "Every 5 minutes (configurable)", from his Orca-automation design). Part (B) of R38 keeps cron plus one dispatcher installed by the Coder image and rejects his automation. PR 729 and the closure comment of PR 686 say uncovered 655 features stay tracked in #716 to #718, so tracking is allowed, but no build is authorised by R38.
- **R6 (REQ:36) and R16 (REQ:37): aligned for who owns the line, in conflict with the item's wording.** Cron is the scheduler, installed by the Coder image (Coder issue 515), one entry, one dispatcher. Nothing in IronClaude installs or edits it.
- **FR-10 (SPEC:200) and D02 (DEC:175-198): CONFLICT on the value.** FR-10 fixes `*/5 * * * *` under `flock -n`, "installed once per boot by the image; no stage installs it before S17". D02 (`debates/D02/VERDICT.md`) says the sweep can last about 525 s against a 300 s tick and lost ticks "can be routine; not measured".
- **FR-11 and the 270 s cap (SPEC:171, SPEC:201): aligned with the item's "floor" warning.** Code: `LOOP_CAP_S = 270`, `CHILD_TIMEOUT_S = 255` (`src/superclaude/cli/issue_watch/dispatch.py:54-55`), and a comment that a sweep can last 270 + 255 s so `flock -n` skips a tick (`dispatch.py:468-470`).
- **NFR-04 (SPEC:217): partly aligned.** It asks `status --json` to gain `last_sweep_at` and more fields; the item's "status reports the interval" is the same kind of field. Not built: `status_report` returns eight keys and no interval (`cycle.py:1464-1473`). I found no open issue that tracks NFR-04 (UNVERIFIED beyond the scan lists).
- **NG-2 / FR-06 / FR-82 (SPEC:196, SPEC:218): aligned.** A setting needs no GitHub write.
- **Zero-setup rule R17/R18 (REQ:43-44): partly aligned.** Nothing manual, which is the reason nobody hand-edits the line any more.
- **Reality check, host: UNVERIFIED for other hosts, verified here.** `crontab -l` on this host shows `* * * * * /usr/bin/flock -n ... issue-watch run-all ...` under the header `# aidev02-issue-watch (managed: rewritten on every boot)`. So the live cadence is 1 minute, not the 5 minutes of FR-10 and D02; issue 774 item 8 and the closing comment of #450 say the same (Coder PR 526, not readable by me). Hand-editing is useless because the image rewrites the line at every boot.
- **WORKER-CONTRACT.md and HOW-WE-WORK.md: none apply** (grepped for interval, cron, cadence, poll; the only hit is the coordinator's own 5-minute sweep clock, `WC-16`, a different clock).
- **Verdict files:** only D02 touches the interval. D15 (`debates/D15/VERDICT.md`) has no row for a configurable interval (checked its A to G lists in DEC:561-593).

## Complementary issues

- **#774 (docs refresh):** its item 8 asks to settle the real cadence with `crontab -l`. W3's floor and default depend on that answer. Interface: #774 decides the number; W3 would only add a way to change it.
- **#812 (W4 backoff):** a shorter interval raises throttle risk, a longer one lowers it. Interface: both change how fast the watcher spends GitHub calls. Independent to build.
- **#817 (W9 conditional reads):** same budget, same evidence need.
- **#814 (W6) and #820 (W12):** the shadow-run sizing and the SLO numbers assume a tick length (`docs/designs/issue-watcher-setup.md:191`).
- **#757 (coordinator sweep outside the session):** a second cron clock (every 5 minutes) that could share a setting convention. Related, not dependent.
- **#777 (map the manual pieces):** W3 would add a manual piece, the opposite of its goal.

## Closest overlap

1. **#774**, "Docs refresh for the issue watcher and coordinator". Shared: the cadence statement (items 8 and the `*/5` and `0 */5 * * * *` text in `docs/designs/issue-watcher*.md`) and the question whether the live tick is 1 or 5 minutes. It covers about 15% of W3's done-when (it settles what the interval is; it builds no setting and no status field).
2. **#812 (W4)**: about 10% (the same "how fast do we spend calls" question; no shared acceptance test).
3. **#757**: about 10% (cron pattern and tick length; different program).

## Standalone or merge

Test against the closest issue, #774:

| Test | W3 | #774 | Effect of merging |
|---|---|---|---|
| Owner | the owner; the image (Coder repo) holds the line | the docs owner | no change |
| Acceptance test | `crontab -l` and `status --json` show the new interval | text matches `crontab -l`, "no behaviour change" | a behaviour change inside a docs-only issue breaks #774's own scope line |
| Files touched | `dispatch.py`/`cli.py`/`cycle.py` plus the Coder template | docs only | mixed review |
| Build phase | a code change plus a second repository | one docs PR | #774 would wait on Coder |
| Risk if merged | #774 stalls on a cross-repo item | none | real |

Verdict: **do not merge into #774; and W3 should not stand as a build item either: close it as not planned, and carry its one live question in #774.** Reasons: (1) the premise is gone, the line is managed and rewritten on every boot, so "instead of hand-editing" has nothing to replace; (2) the change belongs to the Coder image, which this repository cannot build or test; (3) FR-10 and D02 fix the cadence as a design value, not a setting; (4) it is a Clay-origin feature that R38 did not adopt; (5) nothing depends on it, and the issue calls itself low value. The owner closed W5 (#813) and merged W1 (#809) on 2026-11-24 for the same kind of reason (premise replaced, owned elsewhere). The residual need, "what is the real interval and what is the lowest safe one", is a single question for #774 item 8 and for the owner: if the tick stays at 1 minute, sweeps that run longer than 60 s skip ticks (`dispatch.py:468-470`). Merging would be right only if the owner wants a status field `interval_seconds` and `last_sweep_at`: then that is NFR-04 and belongs with the watcher status work, not with a setting.

## Closed issues and merged PRs checked

- **#450 (closed, completed):** closing comment says the watcher is live, "polling every minute", cron "managed, rewritten on every boot". Contradicts the item's premise.
- **#331 (closed):** its text says "checks GitHub every 5 minutes"; no setting was asked.
- **#655 (closed, not planned):** source of "every 5 minutes (configurable)" (its body, poll section); owner closed it.
- **#665 (closed, not planned):** review findings on the 655 plan; nothing on the interval (grep).
- **#813 (W5, closed 2026-11-24, not planned):** precedent: manual premise replaced by the automatic first-run check, so the item was closed.
- **#809 (W1, closed 2026-11-24, merged into #716):** second precedent from the same day.
- **PR 707 (merged):** the zero-setup watcher; installs no cron itself, ships `run-all`, the caps above.
- **PR 729 (merged):** records R38; the merged watcher is the design.
- **PR 485 (merged):** says cron entry `0 */5 * * * *` is owner-run; that text is the stale six-field line #774 wants fixed.
- **PR 759 (merged):** failed-first-run retry; not about the interval.
- **PR 447 (merged):** original poller, no interval setting.

## Updated recommendation

**Close (not planned), carry the cadence question in #774 item 8; if the owner prefers to keep it, keep open with changes: trim the body to W3 only, drop the "instead of hand-editing the cron line" wording, and ask for `interval_seconds` plus `last_sweep_at` in `status --json` (NFR-04) with a floor taken from the measured sweep time.** Priority P3. Complexity medium, size S in this repository (a status field) and M overall if the Coder template must change. Changed from round 1 (keep open with changes): the host now shows a managed every-minute line (round 1 left this UNVERIFIED), R38 was weighed (round 1 did not cite it), and the precedent of #813 and #809 closed today. The owner decides.

## Scan record

- Lists read in full: open-issues.tsv 134 of 134 lines; closed-issues.tsv 157 of 157; merged-prs.tsv 508 of 508.
- Search terms (titles): watcher, issue-watch, cron, poll, interval, rate, throttle, shadow, sweep, coordinator, dashboard, observer, review, alert, SLO, runbook, first-run, approval, Run.
- Opened in full with `gh issue view` (open): 717, 716, 774, 757, 761, 777, 770, 772, 775, 753, 810, 812, 814, 815, 816, 817, 818, 819, 820, 821, 822, 823, 442 (23). Closed: 450, 331, 655, 665, 751, 796, 809, 813 (8). Merged PRs with `gh pr view`: 707, 759, 729, 584, 591, 447, 485, 700, 701, 548, 448 (11).
- Master check: `/sc:analyze src/superclaude/cli/issue_watch --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/b/9/analyze` ran; report `/home/coder/workspaces/worktrees/IronClaude/Realign/.dev/issuecleanup/b/9/analyze/analyze-report.md` (finding 2 and 3).
- UNVERIFIED: Coder PR 526 and the Coder template (repository not readable); any host other than this one; whether any open issue tracks NFR-04; the plan file stage completion after PR 700.
