# Round 2 findings: issue #808 (C27) One capped notice after an escalation entry is written

Checked 2026-11-24 on master `f2894fc44`. Issue state: OPEN, no comments. Parent: umbrella #716. `<P>` = `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify`. `<R>` = `/home/coder/workspaces/worktrees/IronClaude/Coordinator/.dev/releases/backlog/issue-watcher-zero-setup/requirements.md`. Analyze check: `.dev/issuecleanup/b/8/analyze/808/analyze-report.md` (target `src/superclaude/cli/issue_pipeline`).

## Alignment with architectural decisions

- **R38** (`<R>:64`): no element of Clay's 655 design is adopted, including the "living work report", "wake file with acknowledgment" and "read-only merge gate". **Partly aligned, with a real risk of conflict.** The notice element is Clay's (`<P>/DECISIONS.md:827` "QG2 overall: HYBRID; the notice element is Clay's, reserved"), the entry lines it follows come from the report entry (C14, #795, parked by the owner 2026-11-22, #716 status note), and the Orca unread mark it reuses was step 3 of Clay's wake file (`<P>/spec/SPEC.md:203` FR-13, PR 686, closed). R38 voids the "Clay strengths adopted" rows (section 7 and HYBRID rows of section 2), so the QG2 reservation stands only as far as the owner re-adopts it. UNVERIFIED whether the owner counts the notice as adopted or rejected.
- **QG2 OD-5** (`<P>/spec/SPEC.md:101`, `DECISIONS.md:825-833`): entry lines first; notice reserved for AU4a, AU4c, AU5. **Aligned**: C27 is exactly the reserved item and states the three trigger conditions only partly (owner says push wanted with cap; sender built and tested; verb accepts row 8 alone, UNVERIFIED).
- **OA-25a** (`<P>/spec/SPEC.md:113`, `DECISIONS.md:1015-1025`): no push notice in the first build. **Aligned if C27 is deferred; in conflict if built now.**
- **FR-49** (`SPEC.md:260`) and **SEC-21** (`SPEC.md:310`): reserve the push notice until the owner asks with a cap number, a sender is built and tested, and the verb accepts row 8 alone. **Aligned** as a gate; none of the three holds today.
- **Cap wording, FR-12** (`SPEC.md:202`) and **OA-16** (`DECISIONS.md:1246`): "absent or 0 means no cap". C27's done-when says "no cap number recorded: no notice". **In conflict (wording)**: "no cap" can be read as unlimited. The item's reading is the safe one; the plan must say the same before a test pins it (also `SPEC.md:559`, "0 until a number").
- **SEC-14** (`SPEC.md:303`) and the owner rule on approvals in chat: "the owner must say a push is wanted" (DEC:829) is **aligned**; the owner states it in chat and an agent records it.
- **Secret and text rules**: ruling-17 secret rule (S10-F18, C21 #802). **Aligned**; the notice text must pass the same scan. C27 does not say so.
- **WORKER-CONTRACT WC-9, WC-13, WC-16** (`~/.claude/WORKER-CONTRACT.md:41,63,290`): the notice is a coordinator-side outward action to the owner, not a worker action; `/sc:sweep` "recommends nothing" and lists waiting items without a push. **Aligned**; no worker sends a notice.
- Plan stage: `escalate` is built in S15c (`SPEC.md:499`); not on master (analyze report F1; grep found no `escalate`, `unread` or sender in `issue_pipeline`, `sweep`, `observe`).
- Searched DECISIONS.md, SPEC.md, FOLLOW-UPS.md and the verdicts for: notice, OA-16, OA-25a, FR-47, FR-49, SEC-21, reach_daily_max, unread, ClickUp.

## Complementary issues

- **#795** (C14, report entry content; parked): the escalation entry that C27 follows is written by `report-entry` and `escalate`; C27 cannot run before entry lines exist. Interface: the entry line is the trigger of the notice.
- **#794** (C13, Orca decision gates as a way to reach the person, with answer-check): the same purpose by another means; completes the escalation channel. Interface: one escalation, either a gate or a notice, never both unless the owner wants both.
- **#801** (C20, limits and escalation rules): defines which rows escalate (row 5 deletions, row 8 questions); C27 is limited to "the rows the owner allows".
- **#802** (C21, text hygiene): the notice text is covered by its scan.
- **#781** (contact agents) and **#727/#726** (dashboard two-way, vote): other ways a person hears; they decide how a person is reached.
- **#757** (sweep outside the session, wake on change) and **#770** (watcher hands claims to the coordinator): a model-free wake path that could carry an unread mark.

## Closest overlap

**#794**, "Coordinator C13: Orca decision gates as a way to reach the person, with answer-check" (open). Shared: after an escalation is written the person must learn it (S06-F5 opens a gate so the pending question is visible to Orca and the sweep; C27 marks the workspace unread). I estimate it covers about 30 percent of C27's purpose, but 0 percent of its done-when (the cap of five in 24 hours, the "no number, no notice" rule, the sender). Next two closest: **#795** (C14; about 15 percent: it holds the entry line the notice follows) and **#801** (C20; about 10 percent: row selection).

## Standalone or merge

**Verdict: stand alone, parked.** Tested against #794:
- Owner: both are coordinator verb work; the owner decides push versus gate (both need the owner's chat go). Same person, different decisions.
- Acceptance test: C27 = one notice, a cap of five per 24 hours, none without a recorded cap; C13 = a gate opens and `gate-resolve` alone never satisfies `answer-check`. Different tests.
- Files touched: C27 = `escalate` plus a small sender (`orca worktree set --unread`, verified in `orca worktree set --help`) and a counter; C13 = gate open, close and `answer-check`. Different code.
- Build phase: both sit in the #716 phase 2 cluster, but C27 is gated on three triggers and C13 is not.
- Risk if merged: C27's parked, trigger-gated state would hold back C13's buildable part; C13's no-approval-by-gate rule would be mixed into a one-way notice.
Plainly: merging would be right if the owner says one reach-the-person mechanism is enough (gate or notice). Then close C27 into #794. Not decided here.

## Closed issues and merged PRs checked

- **#796 (C15), #809 (W1), #813 (W5)** closed NOT_PLANNED 2026-11-24 by the owner, citing R38 for the Clay-derived plan check and wake file: shows the owner treats Clay-derived items under R38; C27's notice is the same family (supports "may be dropped").
- **#655** (closed NOT_PLANNED): source design of the notice.
- **PR #539** (merged): `/sc:sweep` lists "waiting on a person"; C27's first-build fallback (FR-49).
- **PR #514, #577, #592** (merged): the observer's questions read; no sender or unread mark added (grep of `src/superclaude/cli/observe` found none).
- **PR #686** (CLOSED unmerged): the only code with an Orca unread mark step (FR-13); not on master.
- **PR #700, #729** (merged): rollback and R38.
- **PR #683** (merged): `/sc:closeout`; a "not done" result has no hand-back target, which #771 asks for; related, not overlapping.

## Updated recommendation

**Keep open with changes**, priority **P3**, complexity **medium**, size **S to M**. **Unchanged from round 1** in action, priority, complexity and size. Changes (as round 1): mark "deferred, three triggers"; state the cap rule as "no recorded cap number means no notice" and correct FR-12 and OA-16 wording; remove "that helper is reusable" (it is an Orca verb, `orca worktree set --unread`, not an IronClaude helper; PR 686 code is closed); take it out of the #716 phase 2 build-together cluster. New in round 2: record that R38 may void the notice element (Clay's); if the owner says no push notice is wanted, close instead.

## Scan record

Read in full: open-issues.tsv (133 rows), closed-issues.tsv (156), merged-prs.tsv (507), titles only. Search terms: escalat, notice, notif, unread, ClickUp, wake, report entry, gate, dashboard, sweep, waiting on a person, cap, ping, contact. Opened in full: open #716 (body, comments), #795, #801, #794, #802, #781, #725, #718, #757, #770; closed #796, #809, #813, #450; PRs #729, #280, #285, #707, #686. Plan files: SPEC.md, DECISIONS.md, FOLLOW-UPS.md, VERDICT.md greps; `<R>` R38. Master: grep for escalate, unread, notice, ClickUp in `issue_pipeline`, `sweep`, `observe` (none). UNVERIFIED: whether the owner counts the notice as adopted under R38; row-8-alone acceptance; #725 and #718 read as skims; PR #514, #577, #592 read by title only.
