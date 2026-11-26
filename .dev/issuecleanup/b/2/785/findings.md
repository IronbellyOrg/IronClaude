# Round 2 findings: issue #785 (C4) Load Orca's own orchestration skill at run time

Checked against master `f2894fc44`, 2026-11-24. Read-only. Plan files: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/` (SPEC.md, DECISIONS.md, debates/*/VERDICT.md). Owner decision R38 is in `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:64` of this worktree (round 1 could not find it). Round 1: `/home/coder/workspaces/worktrees/IronClaude/Analyze716/.dev/issuecleanup/a716/2/785/findings.md`. Umbrella #716 and its backlog review (2026-11-24) and closing review (end of body) were read.

## Alignment with architectural decisions

- **R38 (owner, 2026-11-21, requirements.md:64): aligned on the name, and it changes the stage order.** R38 says "Names stay coordinator and `/sc:coordinator`", so the skill that holds this step keeps its name. R38 also says it "supersedes the 'Clay strengths adopted' rows of the unification spec (section 7 and the HYBRID rows of section 2)". SPEC.md section 7 (line 435 on) holds the rows that S13 (SPEC.md:497, verb group and `refuse(argv)`) and the merge-path part of S14 (SPEC.md:498) were built from. So round 1's blocker "C4 cannot start before S13 lands" no longer holds as written: S13 is mostly void. Whether the owner has re-staged the plan: UNVERIFIED. What still blocks C4 is only the existence of the skill (#782).
- **D08 / FR-62 (name `coordinator`; debates/D08/VERDICT.md:33; SPEC.md:319): aligned.** D08's own evidence is that Orca's `orchestration` skill has "Coordinator" and "Handoff owner" roles and no Orchestrator role. I re-checked that on 2026-11-24: `orca skills get orchestration` line 34 "Classify the role" and line 40 "Handoff owner". C4 loads exactly that guide, so it supports the naming decision.
- **WORKER-CONTRACT.md:7 (the contract never copies Orca verb syntax; the preamble of the running Orca is the authority): aligned.** This is the same principle as C4's "no copy of Orca's text in IronClaude" (the test under `src/superclaude/skills/sc-coordinator-protocol/`). C4 extends it from the worker preamble to the coordinator's guide.
- **FR-40 (SPEC.md:242: never interrupt a worker, never approve a prompt) and FR-26 (SPEC.md:228: closed `refuse(argv)` list): partly aligned.** C4's watch-out says the contract and the plan win over a loaded guide. That is consistent with both. But FR-26 and `refuse(argv)` are rows of the voided section 7 (row D8, SPEC.md:459, carrier "PB" = Clay's unbuilt verb group). So the safety net C4 leans on ("`refuse(argv)` must not be widened by a loaded text") has no owner-approved form today. The rule survives as a plain precedence line in the skill, not as code.
- **WC-8 / WC-13 (WORKER-CONTRACT.md:40, :63: commands and workers never call `worker-start`, `dispatch`, `task-create`): aligned.** The load step runs `orca skills get`, a read of a guide, in the coordinator's own session. It is not one of the barred verbs.
- **Launch-level guard (`src/superclaude/hooks/scripts/launch-level-guard.sh:495-506`): UNVERIFIED, possible conflict.** The allowed-orca list has no `skills get`; a level-limited launched session would hit the `*)` branch and be classed ESCAPE. The standing coordinator is not a claim-launched session as far as I can show (PR #735, #736: one coordinator per project, script-started allowed), so no conflict is shown. One live check settles it.
- **D2 (owner records in chat) and WC-17:** none apply to this step.
- Searched: DECISIONS.md and SPEC.md for `orca skills get`, `orchestration skill`, `Handoff owner`; the only plan hits are D08 VERDICT.md:33 and SPEC.md section U-8 (location of the Orca skill). No decision rejects or requires the load; the plan is silent on it.

## Complementary issues

- **#782 (C1, skill layout):** C4's start step lives in the skill and its ref files that C1 creates. C1's own text (row S04-F5) already says the skill "loads Orca's own `orchestration` skill first". Interface: C1 names the wave 0 ref and the file-table test; C4 fills the ref with the command, the fail-closed rule and the no-copy test. Since 2026-11-24 #806 (C25, template tests) was merged into #782 by the owner, so #782 is now the one skill-skeleton issue.
- **#783 (C2, STOP codes):** the fail-closed escalation ("command returns nothing") needs a named STOP code. Interface: C4 adds one row to C2's table, and C2's two-way test then covers it.
- **#786 (C5, Run lifecycle):** the guide's Run text (lines 103-131 of the live guide: `run-create`, then "After a restart, resume your own Run with `run-use --id <run_id>`") is what C5's rule must agree with. C4's load runs before C5's `run-current`.
- **#787 (C6, verbs per step):** the loaded guide can name verbs the plan does not allow. C6 is the check on that. Interface: C6's per-step lists beat the guide.
- **#755 (one Run or many):** the guide says "bind one Run" without saying per project or per task. #755 sets the rule that the loaded text must not override.
- **#716 (umbrella):** parent. Its backlog review (2026-11-24) lists C4 in the first start group with C1, C2, C6.

## Closest overlap

**#782 (C1) "Skill layout: Activation section, numbered waves with lazy refs, stub-first files, file-table test".** Shared: C1's row S04-F5 says the skill "describes its runtime workflow as numbered waves... and loads Orca's own `orchestration` skill first", which is the same sentence C4 builds; both live in the same `SKILL.md` and wave 0 ref. Estimate: #782 covers about 25 percent of #785's done-when (it names the load as the first wave step, but has no run-time command check, no no-copy test, no fail-closed escalation, no precedence rule and no "loaded before first `worker-start`" test).
Next two: **#783 (C2)**, about 15 percent (the STOP code for the empty-guide case); **#786 (C5)**, about 10 percent (both are start-of-run steps, and C4's load must come first).

## Standalone or merge

**Verdict: stand alone, sequenced after #782 inside the same first build group.** Tested against #782:
- Owner: same (the person building the coordinator skill). That favours merging.
- Acceptance test: different. #782 tests file layout (sections, table, refs exist). #785 tests behaviour of one start step (guide loaded before the first `worker-start`, nothing copied, fail closed on empty output). Different failure modes.
- Files touched: #782 touches `SKILL.md`, the wave table and test. #785 touches one ref file, a second test, and one STOP row in C2's table.
- Build phase: both Phase 1 of #716.
- Risk if merged: #782 grows (it already took in #806 and has 6 source rows) and its pass/fail then waits on the live Orca call and on the C2 table. The one outside dependency in the whole skeleton (the Orca CLI) would sit inside the layout issue.
Deciding reasons: separate acceptance test, separate outside dependency, and the item is size S so it adds little tracking. Merging into #782 would be right if the owner wants one pull request for C1+C4 and the same builder does both; the owner merged #806 and #798 on exactly that "same first step" reason on 2026-11-24. Then the done-when lines of #785 carry over as three bullets. I recommend standalone because the two done-when sets can be checked separately and only #782 must land first.
One fix either way: remove the duplicate sentence (S04-F5 "loads Orca's own orchestration skill first") from #782, or point it to #785, so the same requirement is not in two issues.

## Closed issues and merged PRs checked

- **#806 (closed, merged into #782, 2026-11-24):** moves the template tests into C1. Changes C4 only in that the skill's file-table test now also names template files; no change to C4's scope.
- **#796 (C15 plan request, closed not planned), #804 (C23 overview, closed), #798 (C17 merge-safety files, merged into #797), #809 (W1, merged into #716):** all closed on R38 grounds. None touches C4. They confirm that R38 is being applied item by item, so C4 and C6's `refuse(argv)` dependency should be judged the same way.
- **#444 (closed, sub-orchestrator evaluation):** asked to analyze the orchestration skill; no skill-loading rule came from it.
- **PR #735, #736 (merged 2026-11-23):** one coordinator per project and script-started coordinators allowed. They mean the coordinator that loads the guide may be started by a script, which supports putting the load in a skill start step rather than a person's habit.
- **PR #539 (merged, `/sc:sweep` and WC-16 loop), #514 and #503 (observer):** no code loads the guide; the sweep and observer never need it.
- **PR #591 (merged, Plan B: coordinator handoff duties in WORKER-CONTRACT.md):** the contract text the coordinator runs on today; it holds no instruction to load Orca's guide, which confirms the gap.
- **PR #700, #701:** rolled back the 655 build and restored contract text; nothing of C4 was in them.

## Updated recommendation

- **Action:** keep open with changes. (1) Say "wave 0 of the coordinator skill" is the start step but name stage dependencies as "after #782", not "after S13/S14" (R38 voids most of S13). (2) Make the precedence rule (WORKER-CONTRACT and the plan win over the loaded guide) a test in done-when, with a fixture where the guide and the contract disagree. (3) Add a STOP-code row request to #783. (4) Record the open check: is `orca skills get` allowed in the coordinator's own guard context (UNVERIFIED). (5) Remove the duplicate S04-F5 sentence between #782 and #785.
- **Priority:** P2. **Complexity:** simple, size S.
- **Change from round 1:** priority, complexity and size unchanged. Changed: the blocker is now only #782 (and #783 for the STOP row), not S13/S14, because R38 supersedes the rows those stages came from; "R38 not found" is resolved; overlap with #782 is named and its duplicate sentence flagged.

## Scan record

- Lists read in full (titles): open-issues.tsv 134 of 134 rows, closed-issues.tsv 157 of 157, merged-prs.tsv 508 of 508.
- Search terms: orchestration, orca skills, Run, coordinator, skill layout, STOP code, refuse, verbs, guide, sweep, observer, closeout.
- Opened in full with `gh issue view`: open #716, #782, #783, #788, #755, #761, #770, #800, #793, #757, #725, #771, #807, #805, #794; closed #806, #796, #798, #804, #809, #444, #507. Merged PRs opened with `gh pr view`: #591, #514, #539, #735, #736, #683.
- Command run: `/sc:analyze src/superclaude/cli/sweep --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/b/2/analyze` (report: `.dev/issuecleanup/b/2/analyze/analyze-report.md`). Chosen path: the only code that calls Orca verbs under a closed list; no code on master loads `orca skills get`.
- UNVERIFIED: whether the owner re-staged S13/S14 after R38; whether `orca skills get` passes the launch guard for the coordinator; the Coder launch prompt (other repository).
