# #789 (C8) round 2: Record the issue body hash at handoff and re-read the issue on every status pass

Checked against master f2894fc44 (2026-11-24). Round 1: /home/coder/workspaces/worktrees/IronClaude/Analyze716/.dev/issuecleanup/a716/3/789/findings.md. Static run (Command line): /home/coder/workspaces/worktrees/IronClaude/Realign/.dev/issuecleanup/b/3/analyze/analyze-report.md. Plan files read read-only from /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/; owner records from /home/coder/workspaces/worktrees/IronClaude/Realign/.dev/releases/backlog/issue-watcher-zero-setup/requirements.md.

## Alignment with architectural decisions
Searched DECISIONS.md, SPEC.md, the VERDICT files D01, QG1, D15, the owner records R36 to R38 and WORKER-CONTRACT.md. Verdicts:

- **R38** (`.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:64`) part D (the coordinator never merges or closes on its own): ALIGNED. S08-F8 only reads the issue and escalates.
- **R38 part C** (living work report and flags "not adopted"): the report-entry line (S05-F18) is IN CONFLICT, because it needs the living work report. The owner's own note on #716 (2026-11-22) already holds it until #720's trigger, so both owner statements agree it is not built now. The status pass in S08-F8 is the other R38 point: `/sc:coordinator --hourly` (C10) is one of the flags (D15 G2, `DECISIONS.md:591`) that R38 lists as not adopted, and the #716 review (2026-11-24, next step 1) asks to reconcile "the old wake/flag/build-order assumptions". S08-F8 is ALIGNED if the status pass means the existing WC-16 sweep (`WORKER-CONTRACT.md:111`, `:290`) and PARTLY ALIGNED if it means `--hourly`.
- **SPEC NG-2 and FR-82** (SPEC.md:218, the poll writes nothing to GitHub): ALIGNED. The re-read is a read; the only GitHub writer is the coordinator-only `complete.py` (analyze report, layout).
- **No GitHub text rule** (SEC-16, SPEC.md:305; `reads.py:7-9`; `approval_record.py:20-22`): ALIGNED if a script computes the hash. A 64-hex value matches `_HASH` (`approval_record.py:40`). A model reading the body to hash it, or a stored "edited by" free text, would be IN CONFLICT. jq has no sha256 here (UNVERIFIED for the installed jq), so a small script step is needed.
- **R36 and R37** (`requirements.md:62-63`; edit rule `unchanged_since`, `predicates.py:275-296`, used at `cycle.py:1014`): ALIGNED. They govern the start; C8 detects change after handoff and never decides approval. `stage_predicates.py:7-9` says the plan stage deliberately does not reuse `unchanged_since`; a `body_sha` compare is a third test and is allowed only against its own stored hash (the item's own watch-out).
- **WC-10** (`WORKER-CONTRACT.md:46`) and **FR-40** (SPEC.md:242): "record a stop" is IN CONFLICT as worded. A closed or reassigned issue is not an Orca stall proof, and the coordinator stops a worker only on a stall proof or the person's recorded stop (WC-6, `:81`). The third check ("takes the escalation path instead of continuing") is ALIGNED; reword the build line to "write an escalation entry and ask the person".
- **D01 VERDICT item 3** (`debates/D01/VERDICT.md:29`, Clay's rule that later edits get a report line): the source of S05-F18. Clay-derived, so under R38's general sentence it is not adopted. **QG1 VERDICT** (`debates/QG1/VERDICT.md:26`, `:31`): `body_sha` there is the hand-back re-approval carrier, a different use; no conflict.
- **Record name** (`issues/<repo-key>__<N>.json`): same conflict as #788 (R38 general sentence; #716 review next step 2, "no competing state store"). The field is fine; where it lives is the owner's ruling in #788.
- **Contract `:296`** ("never trusts a Status it remembers ... rereads"): ALIGNED precedent for re-reading instead of remembering.

## Complementary issues
- **#788 (C7)** writes the record that holds `body_sha`; C8's first check asserts that file, so the record ruling comes first.
- **#791 (C10)** is the pass that re-reads the issue (its S02-F32 lists "issue re-read"); `body_sha` has no consumer without it. Interface: C8 supplies the stored hash and the closed, reassigned and edited predicates; C10 supplies the schedule.
- **#795 (C14)** writes the report entry that S05-F18 adds a line to; held by #720 (trigger) and #719 (page-server fix).
- **#775** (a comment cancels the approval): same edit predicate on the start side; a change there does not change what C8 compares.
- **#757** (sweep outside the session): where a read-only re-read could run later. **#800 (C19)** settles the worker at the end. **#816 (W8)** alerts after bad cycles and does not cover these cases.

## Closest overlap
**#791 (C10: Worker check-in template and the hourly status pass).**

Shared: S08-F8 is the "issue re-read" that C10's S02-F32 lists in each status check, and the stored hash is only useful at that re-read. Estimate: about 35% of #789's done-when (its third check, closed, reassigned and edited issues, plus the compare use of the first check). C10's own done-when tests the template text and a fake-clock cadence, not these three issue states, so the coverage is by description only.

Next two: **#795 (C14)**, about 30%: S05-F18's entry line is the second check; held, and its milestones-only list (plan done, blocked or asking, PR opened, review rounds, PR ready, merged) does not include "issue edited by another person", so the two items contradict each other. **#788 (C7)**, about 15%: carries the record that the first check asserts.

## Standalone or merge
**Verdict: stand alone, with a stated merge trigger.** Tested against #791:

- **Owner**: same. No reason either way.
- **Acceptance test**: different. C8 checks hash equality, one new entry line, and a fake `gh` returning a reassigned, a closed and an edited issue. C10 checks template text and a weekday cadence.
- **Files touched**: C8: a hash script, a `gh` read, one record field. C10: a check-in template and a schedule. No shared file.
- **Build phase**: C8's hash is written at handoff, the same step as C7. The re-read can run in the existing WC-16 sweep and does not need C10's hourly pass.
- **Risk if merged**: C10 rests on `--hourly`, a flag R38 lists as not adopted, and the #716 review asks to reconcile it. If the owner drops that pass, the closed, reassigned and edited detection would go with it. And S05-F18, held under #720, would hold the merged item.

Merging would be right if the owner keeps C10's hourly pass as written and parks S05-F18: what is left of C8 is then one hash field (belongs in C7's record) and a re-read C10 already lists. At that point merge C8 into #791 and move the hash field into #788.

## Closed issues and merged PRs checked
- **PR #707** (merged 2026-11-20): the zero-setup watcher with `unchanged_since` as the start-time edit rule (R36, R37). Delivers the start-side check; nothing after the claim.
- **PR #584 and PR #591** (merged 2026-11-17): plan-stage approval bound to the plan hash, adoption rows, and the contract duty to re-read the Project item at each gate (`WORKER-CONTRACT.md:296`). No body hash and no re-read of closed or assignee state.
- **PR #683** (merged 2026-11-20, `/sc:closeout`): reads the issue after merge and decides done. Does not detect an edit, reassign or close while a worker runs.
- **PR #724** (merged 2026-11-23): owner records are given in chat and recorded by the agent. Constrains how any hold on S05-F18 is recorded; changes no C8 behaviour.
- **PR #700** (merged 2026-11-20, read through `DECISIONS.md:5-39` and the #716 review): removed the report skill, which is why S05-F18 is blocked (#720, #719 open).
- **#796** (C15, closed not planned 2026-11-24, R38). **#806** (C25, merged into #782). **#809** (W1, merged into #716). None delivers or changes a C8 part.

## Updated recommendation
- **Action**: keep open with changes. (1) Build the re-read of S08-F8 as a read added to the existing WC-16 sweep and let #791 point to it, so it does not depend on `--hourly`. (2) Park S05-F18 with #720 and #795 (owner hold of 2026-11-22; R38 part C); note that it contradicts C14's milestones-only list. (3) Reword "record a stop" to "write an escalation entry and ask the person" (WC-10, FR-40). (4) State which text is hashed (the body at claim time, since a level-none worker never receives the body, `brief.py:1-10`; UNVERIFIED which text the owner wants) and that a script computes it. (5) Put the field in whatever record the owner picks in #788.
- **Priority**: P3, unchanged from round 1.
- **Complexity and size**: medium, S, unchanged from round 1.
- **What changed since round 1**: round 1 said to move S08-F8 into #791. This round recommends anchoring it on the WC-16 sweep instead, because C10's `--hourly` pass sits on a flag R38 lists as not adopted. New: the contradiction with C14's milestone list, and the stated trigger for merging into #791.

## Scan record
- Lists read in full: open-issues.tsv 134 of 134 rows, closed-issues.tsv 157 of 157, merged-prs.tsv 508 of 508.
- Title search terms: body, hash, status, re-read, check-in, hourly, sweep, report, entry, approval, edit, comment, reassign, closed, watcher, stop, escalation, record.
- Opened with `gh issue view` / `gh pr view` (bodies read to their first 1500 to 1900 characters, C-items from their `###` heading; text beyond that is UNVERIFIED): open 791, 795, 775, 757, 720, 719, 816, 698, 753, 788, 800, 761, 786 (13); closed 796, 806, 809 (3); merged PRs 707, 584, 591, 683, 724 (5). Also read: #789 and #716 (body, closing review, all 5 comments).
- Not opened with gh: PR #700 (read through `DECISIONS.md:5-39`).
- Master check: Command line `/sc:analyze src/superclaude/cli/issue_pipeline --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/b/3/analyze`, succeeded; Grep for `body_sha` over `src/superclaude/cli` found none. UNVERIFIED: the installed jq has no sha256; who can edit a public issue body.
