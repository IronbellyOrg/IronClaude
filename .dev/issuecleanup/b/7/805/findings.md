# Round 2 findings: #805 (C24) Home of the coordinator spec, the requirement ids the skill cites and the mapping of Clay's open owner questions

Checked 2026-11-24 against master f2894fc44 (worktree Realign). Parent: #716 (coordinator). Round 1: `/home/coder/workspaces/worktrees/IronClaude/Analyze716/.dev/issuecleanup/a716/8/805/findings.md`. Static run: `/sc:analyze src/superclaude/cli/issue_pipeline --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/b/7/analyze` (finding 5: no coordinator spec on master; the coordinator rules sit in `~/.claude/WORKER-CONTRACT.md` and its repo source). Plan paths are under `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/` (SPEC = `spec/SPEC.md`, DEC = `DECISIONS.md`).

## Alignment with architectural decisions

- **R38** (owner 2026-11-21, `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:64`): "no element of Clay's orchestrator design for issue 655 ... is adopted"; the merged watcher is the design; names stay coordinator and `/sc:coordinator`; and the "Clay strengths adopted" rows of SPEC (section 7, HYBRID rows of section 2) are superseded. C24 asks to reconcile "Clay's IronFlow coordinator spec" (FR-1, FR-2, FR-13, FR-19, FR-23 to FR-25 and others) with the unified spec, to cite its requirement ids in the skill refs (S06-F14) and to map Clay's OD1 to OD15 (S10-F62). The IronFlow spec is the spec of the #655 design (closed #665 lines 31 and 41 and closed #675 line 60 quote `SPEC-AGENT-WORK-COORDINATOR-20261027.md` as the coordinator spec of that plan). **In conflict** with R38 as far as the item treats that spec as a source of requirements; **UNVERIFIED** that R38's "orchestrator design" document and the IronFlow spec are one text, because the IronFlow file was never read (D04 VERDICT:87, D05 VERDICT:85, D11 VERDICT:108, D15 VERDICT:264 each say "not read").
- **FOLLOW-UPS.md:50 and SPEC.md header**: the unified spec "is not a plan of record until the owner confirms the owner actions"; R38 then superseded part of it. The item treats `SPEC.md` as the unified coordinator spec to compare against. **Partly aligned / stale**: that half of the comparison has no confirmed standard.
- **DEC:371** ("the name `/sc:orchestrator` was never an owner decision"; none of OD1 to OD15 covers it): R38 settled the name as `/sc:coordinator`. The OD1 to OD15 mapping is therefore partly answered by R38 for names. **Aligned** with a mapping of the two lists in the plan (OD-1 to OD-13, OA-13a to OA-28b: `SPEC.md:73`, `:97`), **moot** for the Clay-only questions.
- **SEC-14, D2 amendment** (`SPEC.md:303`; `~/.claude/WORKER-CONTRACT.md:57`): the home of a spec is an owner choice given in chat and recorded by an agent. **Aligned**: the item's first step is exactly that choice.
- **WORKER-CONTRACT.md:69-71 and `:296-303`** (coordinator rules and issue pipeline duties): today the coordinator's rules live here, in `HOW-WE-WORK.md`, the Coder launch prompt, and `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` (PR #532). That is the working de facto home and it is where #735, #736, #752 and #754 edited coordinator wording. **Aligned** as the candidate home; the item does not name it.
- **#716 review 2026-11-24** (item 1): "retained engineering requirements distinct from rejected architecture", not authorized merely by appearing in #716. **Partly aligned**: C24 mixes the two.
- **Report-dependent parts** (FR-2, FR-19 daily run; #718 D3, D4): the owner parked the work report on 2026-11-22 and said #718 D3 and D4 are not pursued (#716 and #718 comments). **In conflict** while parked.

## Complementary issues

- #774 (docs refresh for watcher and coordinator): can carry the "short note naming the home copy". Interface: C24's note is one line in the docs #774 already edits.
- #782 C1 and #787 C6 (skill layout, verbs per step): the skill-refs id table (S06-F14) would live in C6's refs; it cites a spec that R38 does not adopt, so C6's own test (verbs checked against the refusal list) is the better check.
- #777 (map of the whole watcher and coordinator chain) and #761 (potential gaps, including that the coordinator has no skill): show where the rules live; #777's map would answer "which copy is the home".
- #718 D1 (named as related) and D4 (IronFlow copy of the report skill): same sync work, same hold (#720).

## Closest overlap

**#774, Docs refresh for the issue watcher and coordinator.** Shared: the short note in the repo that says where the coordinator rules live, and fixing statements that contradict the worker contract. About 15 percent of C24's done-when (the note). Next two: **#777** (about 10 percent: its map names the home of the topic) and **#718** (about 10 percent: D4 is the same IronFlow-sync question, on hold). The diff list of FR ids (the main done-when) and the OD mapping are covered by none.

## Standalone or merge

**Neither stand-alone nor merge as filed: close, with one residual line moved.** Against #774: owner same (docs owner), acceptance test differs (a diff list of FR ids versus a docs check), files differ (an external IronFlow file versus repo docs), build phase same (docs, any time), risk if merged: #774 would inherit an unread external file and an owner-gated external edit. What the owner needs is one chat decision, "the coordinator rules live in WORKER-CONTRACT.md, `HOW-WE-WORK.md` and the coordinator skill once built; the IronFlow spec is not a source", recorded on #716; if the owner wants it written down, one line in #774. Merging into #774 would be right if the owner wants the note and not the diff list. The item stands alone only if the owner reverses R38 for the IronFlow spec.

## Closed issues and merged PRs checked

- #655 (closed as not planned), #681 (merged design, rolled back by #700), #700 (merged revert), #729 (merged R38): the spec's design lineage; R38 and #700 remove it as a source.
- #665 (closed, 21 Medium findings of the #655 plan) and #675 (closed, 54 findings): quote the IronFlow spec's text and line numbers; they show the spec disagreed with itself (M1 at #665 line 41) and that its cross-repo claim was unproven (M8 at line 31). They deliver reading evidence for part of what C24 wants to diff, but never a diff list.
- #735, #736, #752, #754 (merged): coordinator wording moved to one coordinator per project and not person-opened, in the worker contract and docs; this is where the home already is.
- #532 (merged): supervised orchestration technical reference, the written home of the watcher side.
- #587 (merged): alignment decision records for orchestrator, observer and watcher.
- #701 and #724 (merged): worker-contract rule fixes after #700 (no `--to`, owner records given in chat).

## Updated recommendation

**Close** (superseded by R38; the home question is one owner chat decision recorded on #716, optionally one line in #774). If the owner keeps it: **keep open with changes**, as round 1 said: one decision first, one FR list taken from the IronFlow file once read and including FR-10 (the interrupt exception), no FR-2 or FR-19 while the report is parked, say which OD list is mapped, move the skill id table to C6, edits to the IronFlow repo wait for the owner's go. Priority **P3**, complexity **medium**, size **S** (unchanged if kept). Changed from round 1: R38 applied (round 1 cited no R38), closest overlap named (#774), and the recommendation moves from keep open to close.

## Scan record

Read in full: open-issues.tsv (134 lines), closed-issues.tsv (157), merged-prs.tsv (508). Search terms: spec, IronFlow, coordinator, docs, architecture, home, reconcile, OD, FR, report skill, runbook, glossary, contract. Opened (body read with `gh`): open #716, #717, #718, #720, #761, #774, #777, #782, #787, #823, #725, #731, #770; closed or merged #655, #665, #675, #532, #735, #587, #681, #700, #701, #729. Plan and repo files: requirements.md:64, SPEC.md header and `:303`, FOLLOW-UPS.md:50, DEC:371, D04/D05/D11/D15 VERDICT lines above, WORKER-CONTRACT.md:57, :69-71, :296-303. UNVERIFIED: the IronFlow spec itself (another repository; not read); whether R38's design document and the IronFlow spec are the same text; the OD1 to OD15 text (only the #655 line 157 reference was read).
