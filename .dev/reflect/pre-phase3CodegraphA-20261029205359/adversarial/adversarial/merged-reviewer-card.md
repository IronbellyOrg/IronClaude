<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (reviewer-1 card, sonnet/analyzer) -->
<!-- Merge date: 2026-10-29T21:50:00Z -->

# Merged Reviewer Card: Phase 3 codegraph plan (UC-1, Tier 2)

- Plan: `.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/TASK-WF-phase3CodegraphA-20261029-204913.md`
- Spec: `source.md` in the same folder (`.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/source.md`)
- Merge method: adversarial
- Convergence: 1.00
- Findings: 19 (9 important, 10 minor, 0 critical)
- Verdict: refactor

Abbreviations: AE = Authorized expansion, ND = Necessary deviation, DR = Drift, RG = Regression.

## Findings

### M-01

<!-- Source: Base (original, modified) — R1-01; reclassified per Change #1; fix amended per INV-001 (Change #2) -->

- From: R1-01
- Sev: important
- Class: Necessary deviation
- Origin: inherited-from-spec
- plan_ref: plan:218, :221
- spec_ref: source.md:288
- Claim: `/sc:pr-submit` has no `--body-file`; it takes `--body` only (`src/superclaude/commands/pr-submit.md:8,26,54`). Its skill puts that value in double quotes in `gh pr create … --body "…"` (`src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:189`), so a Markdown body passed inline would shell-expand backticks and `$`.
- Exact fix: Task 14 passes a short plain placeholder, `--body "Phase 3 codegraph adoption for issue 323; full description follows."` (no backtick, `$`, `"` or `\`). After `/sc:pr-submit` returns, it runs `gh pr edit <n> --repo IronbellyOrg/IronClaude --body-file .dev/codegraph-migration/progress/P3-pr-body.md`. Acceptance adds `gh pr view <n> --repo IronbellyOrg/IronClaude --json body -q .body | diff - .dev/codegraph-migration/progress/P3-pr-body.md` printing nothing. Log the departure from source.md:288.

### M-02

<!-- Source: Base (original, modified) — R1-02; reclassified and origin added per Change #1 -->

- From: R1-02
- Sev: important
- Class: Drift
- Origin: plan-only
- plan_ref: plan:218, :223, :26
- spec_ref: source.md:288 (`<body>`); `~/.claude/CLAUDE.md` Core rule 4
- Claim: `./artifacts/pr-body.md` is the never-staged project-root `artifacts/` folder, and it is not gitignored (`git check-ignore` exits 1). It leaves a stray `??` file that breaks plan:26's "only that task's files" rule.
- Exact fix: Write the body to `.dev/codegraph-migration/progress/P3-pr-body.md` and stage it in the Task 14 commit.

### M-03

<!-- Source: Base (original, modified) — R1-03; INV-012 folded in per Change #8 -->

- From: R1-03
- Sev: important
- Class: Regression
- Origin: inherited-from-spec
- plan_ref: plan:187, :190
- spec_ref: source.md:286
- Claim: Task 12 adds `/sc:graph` and `/sc:impact` rows to the `other-commands` table. `tests/core/test_how_we_work_routing_table.py:294` asserts `members == _OTHER_COMMANDS`, a fixed 9-name set (`:27-37`), and no task edits it. The same file requires every guide line to be ASCII (`:339-344`).
- Exact fix: Task 12 adds `"sc:graph"` and `"sc:impact"` to `_OTHER_COMMANDS` in the same commit, lists that test file in its files, and writes both new rows in ASCII only (no em dash or arrow).

### M-04

<!-- Source: Base (original, modified) — R1-04 plus Variant 2 (reviewer-2 card) advisory note; reclassified per Change #1; INV-007 folded in per Change #8; "pipeline text not visible" half dropped -->

- From: R1-04; R2 advisory note
- Sev: important
- Class: Necessary deviation
- Origin: inherited-from-spec
- plan_ref: plan:37, :43, :210
- spec_ref: source.md:271, :287
- Claim: Baseline (b) runs fewer paths than the Task 13 (8) union. It omits `tests/recommend/test_routing_refresh.py`, `tests/sc-roadmap`, `tests/roadmap/test_threshold_registry.py` and `tests/cli/test_how_we_work_install.py`. So a failure that already existed in those paths reads as new, which sends the executor into the plan:202 fix loop and then H3.
- Exact fix: Constraints define one test-path set: the baseline (b) paths plus those four. Task 1 (b) and Task 13 (8) both run it through source.md:271's pipeline. Task 1 acceptance adds "baseline (b) pass count > 0". Log the departure.

### M-05

<!-- Source: Base (original, modified) — R1-05; reclassified and origin added per Change #1 -->

- From: R1-05
- Sev: important
- Class: Drift
- Origin: plan-only
- plan_ref: plan:22 vs :67
- spec_ref: source.md:237, :337
- Claim: The stop-and-escalate "Never" list forbids changing "any installer". Task 3 must edit `KNOWN_CORE_FILES` in `src/superclaude/cli/install_core.py`, and source.md:337 has no such ban.
- Exact fix: Reword plan:22 to: "never change `src/superclaude/cli/install_codegraph.py` or other Phase 2 installer modules; Task 3's `KNOWN_CORE_FILES` entry in `install_core.py` is the one exception".

### M-06

<!-- Source: Base (original, modified) — R1-06; narrowed per Change #3; reclassified per Change #1; fix amended per INV-002, INV-003 (Change #2) -->

- From: R1-06; INV-002, INV-003
- Sev: important
- Class: Necessary deviation
- Origin: inherited-from-spec
- plan_ref: plan:20, :21, :37, :44, :45
- spec_ref: source.md:319-321
- Claim: `git ls-files .dev/codegraph-migration` prints nothing, and the plan package is untracked. A worktree created from `origin/master` therefore lacks the plan, `source.md` and every reference input. Separately, creating the worktree inside Task 1 splits `/sc:implement` state: the ledger stays at `<package>/progress.md` and the Q0/Q2 snapshots stay in the starting checkout (`src/superclaude/skills/sc-implement-protocol/SKILL.md:64, :110-121`).
- Exact fix: Add a setup step before `/sc:implement` starts. Create the worktree per plan:20. Bring in the package and the `.dev/codegraph-migration/` inputs, either committed to `master` first or copied in. Start `/sc:implement <worktree>/.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/TASK-WF-phase3CodegraphA-20261029-204913.md` from the worktree root. Task 1 then: asserts `git rev-parse --show-toplevel` is that worktree and the package's realpath is inside it; checks the package, `source.md` and the inputs exist (missing → escalate, never reconstruct); and stages every copied-in path by exact path in its commit.

### M-07

<!-- Source: Base (original, modified) — R1-07; narrowed per Change #3 (guide half dropped); reclassified per Change #1; fix narrowed per Change #2 -->

- From: R1-07
- Sev: important (V2 dissent: minor)
- Class: Necessary deviation
- Origin: inherited-from-spec
- plan_ref: plan:202, :211
- spec_ref: source.md:287 (9), :349 (H5)
- Claim: Check (9) runs the new `/sc:graph` and `/sc:impact` in the executor's running session, which may not load commands that `make sync-dev` added mid-session. Spec T11 requires "all of (1)-(9) pass", so this lands in the plan:202 fix loop and then H3. The guide itself still resolves through the labelled fallback (source.md:247).
- Exact fix: Run check (9) in a fresh `claude` session started in the worktree after `make sync-dev`. Record that `~/.claude/CODEGRAPH.md` is absent and the guide resolved through the labelled fallback. If no fresh session can be started, use H5 (extend H5 to T11 (9)) and log it.

### M-08

<!-- Source: Base (original, modified) — R1-08 part 1; Variant 2 (reviewer-2 card), R2-05 — merged per Change #4; INV-008, INV-009 folded in per Change #8 -->

- From: R1-08 part 1; R2-05; INV-008, INV-009
- Sev: important
- Class: Drift
- Origin: plan-only
- plan_ref: plan:218, :221, :223, :224, :27
- spec_ref: source.md:269, :288, :296-300, :307
- Claim: Task 14 commits and requires "no tracked change afterwards" (plan:223). It then posts comment G and logs the comment's URL in the tracked decision log (plan:224, :27), so the criterion cannot pass. The push after the monitor also gets CI and review that no monitor watches. A rebase in the pre-PR checks rewrites the SHAs that comments 0-F cite and makes Task 13's results stale. The commit itself departs from source.md:288 ("no new commit") but is required by :269.
- Exact fix: Task 14 order: 1. Pre-PR checks; if a rebase happens, re-run Task 13 checks (1)-(8) and note the old→new SHA pairs for comment G. 2. `/sc:pr-submit` (M-01), then `gh pr edit` with the body file. 3. Write and post the addendum. 4. Write `P3-G.md` and post comment G with the PR and addendum links. 5. Record all URLs in the decision log. 6. One commit `docs(codegraph): record PR and Coder addendum links` holding the addendum, `P3-G.md`, `P3-pr-body.md`, the decision log and `.dev/tasks`. 7. `git push origin feat/codegraph-adoption`. 8. `/sc:pr-submit --monitor 3 --pr <n>`, applying the plan:221 checks criterion to that run. 9. `git status --short` prints nothing. Log the commit as a departure from source.md:288, justified by :269.

### M-09

<!-- Source: Base (original, modified) — R1-08 part 2 and R1-14 — merged per Change #4; reclassified per Change #1 -->

- From: R1-08 part 2; R1-14
- Sev: minor
- Class: Drift
- Origin: plan-only
- plan_ref: plan:26, :58
- spec_ref: source.md:269
- Claim: plan:26 drops the spec's `git add .dev/codegraph-migration/progress .dev/codegraph-migration/decisions`. Group-comment bodies and URL rows written after each group's commit are named in no commit list. Task 2's "only" list omits `.dev/tasks`.
- Exact fix: Constraints add `git add .dev/codegraph-migration/progress .dev/codegraph-migration/decisions` to the per-task commit rule. Task 2's commit says "plus `.dev/tasks`".

### M-10

<!-- Source: Base (original, modified) — R1-09; reclassified and origin added per Change #1 -->

- From: R1-09
- Sev: minor
- Class: Necessary deviation
- Origin: inherited-from-spec
- plan_ref: plan:122
- spec_ref: source.md:129, :281
- Claim: Task 7 lists `commands/task.md` and its twin as "(metadata only)", but row 40 adds `codegraph` to no task file. That leaves the change undefined; `mcp-servers:` at `src/superclaude/commands/task.md:6` gets only Phase 1's `serena` strip.
- Exact fix: Task 7 marks `commands/task.md` and its twin as verify-only (Phase 1 removed `serena`; nothing is added), or drops them from the list.

### M-11

<!-- Source: Base (original, modified) — R1-10; reclassified and origin added per Change #1 -->

- From: R1-10
- Sev: minor
- Class: Necessary deviation
- Origin: inherited-from-spec
- plan_ref: plan:122, :187
- spec_ref: source.md:123, :210, :286
- Claim: sc-task-protocol STRICT step 7 is edited twice: Task 7 adds an inline `codegraph_impact` (row 34) and Task 12 adds a `/sc:impact` call (T10). No rule says which wins. Task 7 also does not add the codegraph names it calls to `allowed-tools` (source.md:63).
- Exact fix: Task 12's `/sc:impact` call replaces Task 7's inline STRICT step 7 text. Task 7 adds the exact `mcp__codegraph__codegraph_*` names its STANDARD and STRICT text calls to sc-task-protocol `allowed-tools`.

### M-12

<!-- Source: Base (original, modified) — R1-11; reclassified per Change #1; INV-013 folded in per Change #8 -->

- From: R1-11; INV-013
- Sev: minor
- Class: Authorized expansion
- Origin: plan-only
- plan_ref: plan:177
- spec_ref: source.md:285
- Claim: The plan adds the check `git diff --name-only HEAD -- src/superclaude/cli/reflect/contract.py`. It sees only uncommitted edits, so a `contract.py` change committed earlier in Phase 3 passes unseen.
- Exact fix: Use `git diff --name-only "$(git merge-base HEAD origin/master)" -- src/superclaude/cli/reflect/contract.py` and require that it prints nothing.

### M-13

<!-- Source: Base (original, modified) — R1-12; reclassified per Change #1; INV-011 folded in per Change #8 -->

- From: R1-12; INV-011
- Sev: minor
- Class: Necessary deviation
- Origin: inherited-from-spec
- plan_ref: plan:67, :71
- spec_ref: source.md:255, :257, :277
- Claim: The sentinel scan covers `plugins/superclaude`, where the byte copy of the guide holds the sentinel. Guide section 2's spec text "no primitive runs `codegraph sync`" (source.md:255), and prose such as "codegraph index", put a banned verb after `codegraph ` outside "Never".
- Exact fix: The sentinel scan excludes both guide copies. Outside "Never", no `codegraph ` is followed by `index`, `sync`, `uninit`, `unlock`, `upgrade`, `install` or `uninstall`, even as a noun (write, for example, "the index"; "no primitive syncs the index, see Never").

### M-14

<!-- Source: Base (original, modified) — R1-15; reclassified and origin added per Change #1; INV-010 folded in per Change #8 -->

- From: R1-15; INV-010
- Sev: minor
- Class: Authorized expansion
- Origin: inherited-from-spec
- plan_ref: plan:207
- spec_ref: source.md:287 (2)
- Claim: `<baseline (a) from the decision log>` is not copy-runnable. `-eq` also fails on a harmless decrease. The `grep -v` filter correctly drops the labelled fallback lines.
- Exact fix: Write `N=<baseline (a) value>; test "$(…)" -le "$N"`, log any decrease, and add one note that the filter drops the labelled fallback lines.

### M-15

<!-- Source: Variant 2 (reviewer-2 card), R2-01 — appended per Change #5; fix corrected per DES:478 -->

- From: R2-01
- Sev: minor
- Class: Necessary deviation
- Origin: inherited-from-spec
- plan_ref: plan:67
- spec_ref: source.md:224, :197; DES `interface-design.md:478`, :144, :456
- Claim: No task carries source.md:224's rule for primitives' `graph:not_initialized` message. The spec and DES disagree on what it says: the spec says it names `/sc:graph init`, DES:478 says `/sc:graph status`. DES wins here (source.md:197; overrides (a)-(e) do not cover it).
- Exact fix: Task 3's degraded-token section says: "On `graph:not_initialized`, tell the user to run `/sc:graph status`; it reports `next_action: run_graph_init`." Add one assertion to `tests/core/test_codegraph_guide.py`.

### M-16

<!-- Source: Variant 2 (reviewer-2 card), R2-02 — appended per Change #5; narrowed (troubleshoot and new-commands halves dropped) -->

- From: R2-02
- Sev: minor
- Class: Drift
- Origin: inherited-from-spec
- plan_ref: plan:122, :162
- spec_ref: source.md:129, :281, :284
- Claim: Row 40 adds `codegraph` to `mcp-servers:` for reflect. Neither spec T5/T8 nor plan Tasks 7/10 assigns it to `src/superclaude/commands/reflect.md:6` or its twin `plugins/superclaude/commands/reflect.md:6`, and Task 7 names reflect without holding that file. Troubleshoot is covered by row 13 (Task 6). The new commands get it from DES (`interface-design.md:88, :110, :274, :292`).
- Exact fix: Task 10 adds `codegraph` to `mcp-servers:` in both reflect.md files (after Phase 1's `serena` strip). Task 7 limits row 40 to its own files.

### M-17

<!-- Source: Base calibration block (R1 calibrator note), U-012 — appended per Change #6; rewritten per INV-004, INV-005 -->

- From: U-012 (R1 calibrator); INV-004, INV-005
- Sev: minor
- Class: Drift
- Origin: plan-only
- plan_ref: plan:37, :41
- spec_ref: source.md:27, :30, :32
- Claim: plan:37 sends G1-G4 failures to H1 and drops, without logging it, source.md:30's rule that T1-T10 may continue while G3 fails. Stopping is the safe reading, because E-6 and the MCP part of E-1 would measure the wrong registration, and Tasks 3 and 5 consume them. A G5 failure has no route.
- Exact fix: Task 1: on a G3 failure, run E-2, E-3, E-7 and the CLI part of E-1, then stop at H1, and log the departure from source.md:30 in the decision log. On a G5 failure, restart once in a fresh session in the worktree, then H1.

### M-18

<!-- Source: Variant 2 (reviewer-2 card), R2-06, plus Variant 2 calibration block (R2 calibrator note), U-016 — appended per Change #5 -->

- From: R2-06; U-016 (R2 calibrator)
- Sev: minor
- Class: Drift
- Origin: plan-only
- plan_ref: plan:142, :212
- spec_ref: source.md:282, :287
- Claim: Commit messages differ from the spec: Task 8 says "manual init" where the spec says "user-typed init"; Task 13 says "changelog, docs, sync and Phase 3 smoke results" where the spec says "sync dev copies and record Phase 3 smoke results". The plan's wider Task 13 commit list (`CHANGELOG.md`, `docs/`) is a correct Necessary deviation, because the spec's T11 list omits files T11 edits.
- Exact fix: Use the spec messages verbatim, or log the rewording as a self decision. Keep the widened Task 13 file list and log it.

### M-19

<!-- Source: Invariant probe (Round 2.5), INV-006 (fault-finder; both advocates ACCEPT) — appended per Change #7 -->

- From: INV-006 (fault-finder; both advocates ACCEPT)
- Sev: important
- Class: Necessary deviation
- Origin: inherited-from-spec
- plan_ref: plan:82, :99, :114, :125, :165, :176, :190
- spec_ref: source.md:271, :278-286
- Claim: Existing failures are "recorded, not fixed" (source.md:271), yet per-task criteria require whole directories to pass: `tests/core`, `tests/agents`, `tests/troubleshoot`, `tests/commands`, `tests/sc-roadmap`, `tests/skills`, `tests/cli/reflect`. One existing failure there makes Tasks 4-7, 10-12 impossible to pass, and each ends at H3.
- Exact fix: Each task's pytest criterion reads: "passes, or the failing ids from the source.md:271 pipeline on the same paths give no output from `comm -13 .dev/codegraph-migration/experiments/P3-baseline-failures.txt <task failures file>`" (with the baseline taken over M-04's single path set).

## Dropped card items

<!-- Source: refactor-plan.md "Changes NOT Being Made" — applied per Change #9 -->

| Card item | Reason |
|---|---|
| R1-13 | Refuted. Task 9 writes "all tests of DES §7.1", and DES §7.1 lists `test_impact_guide_lookup_line` and `test_impact_runtime_surface_dual_surface` (`interface-design.md:535-536`); DES:44 holds the lookup line. |
| R2-03 | Not a plan finding. It concerns attribution in the coverage-matrix artifact, and the card itself says "No plan change". The calibrator marked it unverifiable. |
| R2-04 | Not a plan finding. Same reason as R2-03 ("None for the plan"); unverifiable. |
| R2-02 troubleshoot half | Refuted. Row 13 (source.md:102) anchors `troubleshoot.md:6`, and Task 6 applies row 13. |
| R2-02 new-commands half | Refuted. DES:88, :110, :274, :292 already put `mcp-servers: [codegraph]` in both new files. |
| R1-07 guide half | Refuted. source.md:247 gives the labelled in-checkout fallback. |
| R1-04 "pipeline text not visible" half | Refuted under A-002. plan:19 makes source.md the source of truth, and plan:37 cites the pipeline. |

## Calibration carried forward

- R1 calibrator (opus): C=0.73 (all 15 findings confirmed).
- R2 calibrator: C=0.67 (4 confirmed, 2 unverifiable).
- Findings taken from calibrator notes: M-17 (from R1 calibrator note U-012) and part of M-18 (from R2 calibrator note U-016).
