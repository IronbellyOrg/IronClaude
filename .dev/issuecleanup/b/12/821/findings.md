# Round 2 findings: issue 821 (W13, size bound for the dispatch store, FU-11)

Checked 2026-11-24 against master f2894fc44 in `/home/coder/workspaces/worktrees/IronClaude/Realign`. Sources: issue 821, its round 1 findings (`/home/coder/workspaces/worktrees/IronClaude/Analyze717/.dev/issuecleanup/a717/5/821/findings.md`), umbrella #717 and its closing review (comment 1), `/sc:analyze` report `.dev/issuecleanup/b/12/analyze/analyze-report.md`.

Item defect found in the issue text itself: the body of #821 also carries the full text of W14 and W15 (two unchecked boxes after its own W13 block). The same leak is in #822 (W15 after W14). A reader can take W14 or W15 for part of this item. Fix is a text edit of the issue; the coordinator does it after the owner's go.

## Alignment with architectural decisions

- **R38** (`.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:64`, owner 2026-11-21): the merged zero-setup watcher is the design; Clay's in-flight cap, wake file, ack states and registry are not adopted. Partly aligned. W13 itself is neutral (it builds on the merged store), but its Watch-out cites FR-33 (`/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md:235`, the in-flight cap with states woken and acked). FR-33 comes from D07 "Adopt Clay's in-flight cap" (`DECISIONS.md:326`), which R38(C) lists as not adopted and says supersedes the plan's "Clay strengths adopted" rows. So the Watch-out names a rule that no longer governs. The states a prune rule meets are the six on master (`src/superclaude/cli/issue_watch/record.py:34`: pending, launched, unknown, failed, abandoned, claimed). Round 1 said a prune rule "should wait for FR-33's definition"; that was wrong after R38.
- **Technical reference rows** (`techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md:944, 1965, 1990`): D-14 "Bound or pruning rule for finished entries (FU-11)", NOT BUILT, deferred "when the store is above 1 MiB". Aligned: W13 is exactly the deferred row. Design text agrees (`docs/designs/issue-watcher.md:870`, `docs/designs/issue-watcher-setup.md:678`).
- **At-most-once guarantee** (design risk R5 as quoted in `docs/designs/issue-watcher-setup.md:248-250`: "the at-most-once guarantee lives in the state directory"; `cycle.py:981-996`: a `claimed` or `pending` entry makes the cycle skip with `already_dispatched`). Aligned only if the rule keeps those entries. W13's own Done-when says so.
- **WORKER-CONTRACT.md** (`~/.claude/WORKER-CONTRACT.md:296` and `:302`): the coordinator adopts from "the `claimed` entry in `dispatch.json`", and `issue-pipeline complete` takes `--run` "from the issue's `dispatch.json` entry". New constraint round 1 did not name: pruning a `claimed` entry before the coordinator has run `complete` for that run would remove the run id the verb needs. In conflict with the item's wording "finished tombstone entries" unless "finished" is defined as after `complete`. Not a conflict with the item's intent.
- **Day cap** (`record.py:699-703`, `reset_entry` at `record.py:706-720`): `consumed_at` must move to `consumed_log` before an entry is deleted, or the 24-hour count drops. Aligned if the build copies `reset_entry`'s step; the item does not say so.
- **SPEC.md:45 and R18** (`requirements.md:44`): no bearing. No decision in DECISIONS.md, SPEC.md, FOLLOW-UPS.md or the `debates/*/VERDICT.md` files mentions FU-11 or tombstone pruning (grep returned no hit). R5 (`requirements.md:31`): each repo has its own store, so the bound is per repo.

## Complementary issues

- **#717** (umbrella): parent; its review lists "W7/W13 at their triggers" and "W13 a measured size trigger". W13 is built only when the trigger is seen.
- **#816 (W8, alert after three bad cycles) and #820 (W12, seven-day service-level review)**: both add readers to `issue-watch status` (audit log, `slo_numbers`). W13's measurement step (report the store size in `status`) is a third reader of the same command. Interface: one `status` JSON field each; no shared code path to merge, but they should add fields in one reviewed shape.
- **#770** (watcher hands each claim to the coordinator): treats `claimed` entries in `dispatch.json` as the adoption list (option c). Interface: W13 must keep every `claimed` entry the coordinator has not completed. #770 completes first or W13 keeps `claimed` forever.
- **#819 (W11, one retry of an unknown launch)**: changes what `unknown` entries become (`claimed` or `failed`). Interface: W13's finished-entry rule is written over the states after W11, so W13 should not be built before W11 settles its transitions.
- **#716**: the coordinator items do not change store entries on master; the closing-by-the-poll idea (FR-33) is not adopted (R38). No dependency.

## Closest overlap

- **#819 (W11): "Issue watcher W11: One retry of an unknown launch outcome through Orca's operation id (FU-8, owner question Q2)"**. Shared: the same functions in `record.py` (entry transitions, `_RESETTABLE`, `mark_unknown`) and the same invariant, that an entry which can block a second launch must survive. W13's done-when is covered by #819 for about 0-5 percent: W11 decides what an `unknown` entry turns into, and W13 needs that answer, but W11 builds no pruning, no size trigger and no trim test.
- Next two: **#770** (shares the `claimed` list in `dispatch.json`; about 0 percent of W13's done-when) and **#820 (W12)** (shares the `status` reader surface; about 0 percent).
- No open issue delivers any part of "a store above 1 MiB is trimmed without losing a blocking entry". A search of the open list for prune, trim, tombstone, size, dispatch.json found only the issues above.

## Standalone or merge

Verdict: **stand alone**. Tested against the closest issue, #819:
- Owner: same owner; no difference.
- Acceptance test: W13 is a pure fixture test (a store seeded above 1 MiB, trimmed, no blocking entry lost). W11 is a live test with a lost reply and one session. They cannot share a test.
- Files touched: both use `record.py`; W13 adds one pure function, W11 changes `launch.py`/`cycle.py` and needs the live Orca argv.
- Build phase: W11 waits on a live test; W13 waits on a size trigger that is far away (below).
- Risk if merged: a deferred rule with no date would hold W11 open, or W11's live-test gate would hold the prune rule; one wrong change to the store breaks the at-most-once guarantee for both.
Merging would be right only if the owner drops W13 for good and records that in chat; then the finished-entry rule becomes a line in W11. Today the trigger is a documented follow-up (FU-11), so keeping the item is correct.

Trigger evidence (new in round 2, local read-only): one sample entry serializes to about 619 bytes (17 fields, indent 2, sorted keys, `record.py:374`; sample built with jq, values typical, so an estimate), so 1 MiB is about 1,700 entries. The live IronClaude store is 1,631 bytes after 284 cycles (`stat` on `~/.local/state/superclaude/issue-watch/IronClaude/dispatch.json`, 2026-11-24). At the runbook's top rate (6 launches a day, about 2,200 a year) the trigger is more than 9 months away; at today's rate it is far later. The audit log, which already rotates at 5 MiB (`audit.py:108`), is the file that grows (1,976,719 bytes for IronClaude).

## Closed issues and merged PRs checked

- **#450** (closed, rollout tracker): live since 2026-11-23, 284 cycles; says nothing about store size. No store above 1 MiB is reported.
- **#331** (closed, the watcher request) and **PR 447** (merged 2026-11-08, the poller): built the store; no pruning. **PR 448** (merged, approvers-file race): not related.
- **PR 707** (merged 2026-11-20, zero-setup watcher): keeps the six states; adds no pruning.
- **PR 759** (merged 2026-11-24, first-run retry): reads and rewrites config only; no store change.
- **PR 485 and PR 548** (merged, runbook): record FU-11 as not built (`issue-watcher-setup.md:678`).
- **#813 (W5) and #809 (W1)**: closed not planned on 2026-11-24; neither touches the store size. **PR 729** (merged): records R38.
- **#655** (closed not planned): source design; its in-flight cap is not adopted (R38).
None delivers, supersedes or contradicts W13 other than R38 removing FR-33 as a constraint.

## Updated recommendation

Keep open with changes, **P3**, **medium**, size **S**. Unchanged from round 1 on action, priority, complexity and size. Changes to the changes:
1. Define "finished" in the item: an entry is dropped only after its issue is closed and, for a `claimed` entry, after `issue-pipeline complete` ran for that run (`WORKER-CONTRACT.md:302`); never on age alone.
2. Require the `consumed_at` move to `consumed_log` as `reset_entry` does (`record.py:717-720`).
3. Drop round 1's change "mark as waiting on #716's definition of closing a store entry" and the FR-33 Watch-out: FR-33 is not adopted (R38). Replace with "build after W11 (#819) settles the `unknown` transitions and after #770 settles who completes a claim".
4. Add the measurement step (store size in `status`), coordinated with #816 and #820, and state the trigger as about 1,700 entries.
5. Remove the W14 and W15 text that leaked into the issue body.
The owner decides.

## Scan record

Lists read in full (number and title columns): open-issues.tsv 134 of 134, closed-issues.tsv 157 of 157, merged-prs.tsv 508 of 508. Search terms: store, dispatch, prune, trim, tombstone, size, bound, watcher, watch, claim, state, ledger, retention, audit, W-numbers. Opened in full or in the relevant part with gh: open #717 (closing review), #716 (review head), #770, #774, #775, #777, #761, #810, #811, #812, #814, #815, #816, #818, #819, #820 (16 open, counting #717 and #716 once each); closed #450, #751, #809, #813 (4) and merged PRs #447, #485, #548, #707, #729, #754, #759 (7). Plan files read by search: DECISIONS.md, SPEC.md, FOLLOW-UPS.md, `debates/D02/VERDICT.md`, techref rows, requirements.md rows R5, R6, R12, R18, R28, R38. Command run: `/sc:analyze src/superclaude/cli/issue_watch --focus architecture --depth quick` (report `.dev/issuecleanup/b/12/analyze/analyze-report.md`). UNVERIFIED: the real rate of entries per year on a live host (only one host read, 2 entries); whether issue 761 (list of gaps) names pruning (read as a head only).
