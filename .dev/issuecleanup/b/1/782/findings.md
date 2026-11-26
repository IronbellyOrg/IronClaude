# Round 2 findings for issue 782 (C1): Skill layout: Activation section, numbered waves with lazy refs, stub-first files, file-table test

Checked on master f2894fc44 (branch ironbelly/Realign, clean), 2026-11-24. Round 1: `/home/coder/workspaces/worktrees/IronClaude/Analyze716/.dev/issuecleanup/a716/1/782/findings.md`. Command run: `/sc:analyze src/superclaude/skills/sc-closeout-protocol --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/b/1/analyze` (succeeded; report `.dev/issuecleanup/b/1/analyze/analyze-report.md`). Master check: `src/superclaude/skills/sc-coordinator*`, `src/superclaude/commands/coordinator.md` and `tests/coordinator/` do not exist (ls, 2026-11-24); no `SKILL.md` under `src/superclaude` has an Activation heading (grep count 0).

## Alignment with architectural decisions

- **R38** (`.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:64`): "no element of Clay's orchestrator design ... is adopted"; "Names stay coordinator and `/sc:coordinator`". PARTLY ALIGNED. The name and the standing project coordinator stand, so a coordinator skill is allowed. But C1's source rows (S02-F1, S04-F5, S04-F8) come from issue 655's design text, and the issue's own S02-F1 note says each wave row must be re-approved. The layout itself (numbered waves, lazy refs, file table) is not Clay's wave design; it is the pattern already on master in `src/superclaude/skills/sc-closeout-protocol/SKILL.md:28` (file table), `:57` (Waves), `:73` (Error handling). So the shape is aligned; any wave content copied from 681 is not, until re-approved.
- **D08** (`debates/D08/VERDICT.md:63-66`, `DECISIONS.md:352-356`): command `/sc:coordinator`, skill `sc-coordinator-protocol`; the "command's Activation text" carries the glossary line, with a pinned test, "with the first coordinator-skill PR". ALIGNED on names; CONFLICT with the issue's wording: Activation belongs to the command file (`src/superclaude/commands/closeout.md:85`, test `tests/commands/test_closeout_command.py:76,95`), not to `SKILL.md`. The "also" line "a test reads SKILL.md and finds an Activation section, as the existing protocol skills pass today" is false on master.
- **D15 G6** (`debates/D15/VERDICT.md:134`): the 681 design text is "Adopt with change", source of verb and wave detail, not shown owner-approved. ALIGNED with the issue's own Watch out.
- **SPEC.md:62, :178, :498**: command and skill are NOT BUILT; stage S14 ("`/sc:coordinator` command and skill", needs S13 verbs). PARTLY ALIGNED: the umbrella (#716 pick-up note) says no item starts before its stage lands; the 2026-11-24 backlog review on #716 says start with the skeleton (C1, C2, C4, C6, C25). The owner has not named which rule wins (UNVERIFIED in the thread). C1 has no S13 dependency (it needs no verbs), which supports starting now.
- **WORKER-CONTRACT.md** never-as-worker list (`src/superclaude/core/WORKER-CONTRACT.md:23`; test tuple `tests/skills/test_worker_contract.py:474-485`): `/sc:coordinator` is not on it. IN CONFLICT until C1 adds it (a coordinator command must never be dispatched as a worker). The issue does not say so.
- **WC-16** (`WORKER-CONTRACT.md:288-290`) "never stops watching on its own": ALIGNED; lazy refs per wave fit a long-lived session.
- **Repo rule: no `src/superclaude/` paths in installed primitives** (`CLAUDE.md`; `tests/skills/test_primitive_dual_surface_lookup.py`): ALIGNED if refs use installed paths; the new skill must be added to that test's scope.
- **Owner decision 2026-11-24, merge of #806 into #782** (comment on #782 and #806): #782's done-when now also carries "every template file is named by a wave or step, every writing step names a template" (C25 content). ALIGNED; round 1 listed #806 as open, so its C25 overlap finding is superseded.

## Complementary issues

- #785 (C4) completes C1: the wave-0 ref that loads Orca's orchestration guide. Interface: C1 provides wave 0 and its ref slot; C4 fills it. C1's S04-F5 sentence "loads Orca's own orchestration skill first" duplicates C4's whole scope and should be dropped from C1.
- #787 (C6): per-step verb lists live in the wave table column that C1 defines ("its commands"). Interface: one column, C1 owns the column, C6 owns the check that reads it.
- #783 (C2) and #784 (C3): C2's table and C3's block live inside C1's `SKILL.md`; both depend on C1's file table.
- #786, #788 to #795, #799 to #801: each puts its wave text in a ref C1 creates (blocked by C1 for placement).
- #806 (closed, merged into C1): template tests, now in C1's done-when.
- #767 (coordinator compacts too often): lazy refs help; the link is an inference.

## Closest overlap

**#785 (C4) "Load Orca's own orchestration skill at run time".** Shared: C1's S04-F5 clause ("loads Orca's own `orchestration` skill first") is C4's what-to-build. It covers about 10 percent of C1's done-when (one sentence of the wave table), none of the file-table test, Activation or stub-first parts. Next two: #787 (C6, about 10 percent: the "commands" column of the wave table) and #783 (C2, about 5 percent: same `SKILL.md` and test module family). No open issue covers the layout, Activation or file-table test.

## Standalone or merge

**Stand alone.** Tested against #785: owner, the same (coordinator skill author), no difference; acceptance test, different (C1: file table, waves, ref exists, template named; C4: wave-0 command runs, no copy of Orca's text, fails closed on empty output); files, `SKILL.md`, `refs/`, command file, `tests/skills/test_coordinator_protocol.py` vs one wave-0 ref plus one test; build phase, both phase 1, but C1 first because C4 needs the slot; risk if merged, C1 already grew by #806 and by the command file, and C4 touches Orca's runtime guide behaviour (a version drift risk) that should not block the skeleton. Merging into #785 would be right only if the owner decides the skeleton and wave 0 ship in one PR, which is a build choice, not an issue-tracking reason. No merge candidate beats stand-alone; C1 is the root other items hang on.

## Closed issues and merged PRs checked

- PR #683 (merged 2026-11-20) delivers the closeout skill: file table, Waves, stub-first templates, two-way file test (`tests/skills/test_closeout_protocol.py`); the copy source for C1.
- Claim skill `sc-issue-protocol` (PR #373, #425): same layout; confirms a copy job.
- PR #681 (design text) merged then removed by PR #700 (2026-11-20): wave detail is gone from master; C1 can have the skeleton, not the wave contents.
- PR #700, #701, #729 (R38), #735, #736, #752, #754: coordinator wording only; no coordinator skill.
- #655 (closed not planned 2026-11-23): its features live in #716 to #718; C1 is one of them.
- #806 (closed, merged into #782), #796 (C15), #798, #804 (closed): reduce C1's "related" set; C1 no longer has C25 as a separate neighbour.
- #444 (closed not planned): sub-coordinator deferred; `--sub` is not in C1's scope.
- #507, PR #411/#422 (unattended contract): a coordinator command, if it is ever run as a worker, would need an Unattended section; it should be on the never-as-worker list instead.

## Updated recommendation

Suggested action: **keep open with changes**: (1) move Activation and its test to the command file (`commands/coordinator.md`), as D08 and the closeout command do; (2) drop the "loads Orca's orchestration skill first" sentence (owned by #785); (3) add that `/sc:coordinator` joins the never-as-worker list and `NEVER_AS_WORKER` in `tests/skills/test_worker_contract.py`; (4) note which wave rows still need owner re-approval after PR #700; (5) owner to name which start rule applies (S14 first, or skeleton now). Priority **P2** (unchanged from round 1). Complexity **medium, size M**; with #806 merged in and the command file, upper end of M. Changed since round 1: #806 is now merged into this item (its template-test line carries over); alignment evidence for R38 and D08 added, and one decision conflict (never-as-worker list) found.

## Scan record

Lists read in full: open-issues.tsv 134 of 134 rows, closed-issues.tsv 157 of 157, merged-prs.tsv 508 of 508 (titles). Search terms: coordinator, skill, layout, wave, activation, template, STOP, contract, closeout, Run, worker, handoff, orchestration. Opened with gh (body, in part first 900 to 2300 characters, plus comments): open #716 (body, all comments), #761, #767, #770, #771, #774, #776, #725, #781, #339, #755, #757, #765, #777, #785, #786, #787, #788, #790, #791, #792, #797, #799, #800, #801 (16 or more); closed #444, #450, #507, #655, #668, #796, #798, #804, #806, #809, #813; PRs #411, #683, #700, #701, #729, #735. Plan files read: R38 (`requirements.md:64`), `design-comparison-655.md:3`, SPEC lines 62, 178, 228, 498, DECISIONS 352-356, D08 and D15 verdict lines cited. UNVERIFIED: whether R38 covers the non-design layout pieces (it names no skill-layout row); `.dev/implement/reference-our-research-a-3463b8ef/sections/` not opened.
