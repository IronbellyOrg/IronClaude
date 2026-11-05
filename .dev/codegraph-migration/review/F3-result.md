# F3 result: Phase 3 spec review resolution and tasklist (issue #323)

Status: COMPLETE (finalizer F3, 2026-10-29). Planning only: no source, test or doc edited; nothing staged or committed.

## 1. Review findings applied to the Phase 3 spec

Spec: `.dev/codegraph-migration/specs/phase-3-codegraph-adoption-spec.md` (366 → 405 lines). Its new `## Review resolution` section (end of file) has one row per finding. Every finding was checked against the cited source first (Phase 1 and Phase 2 final specs, `tests/recommend/test_routing_refresh.py:638-640`, an `rg -c` exit-code run, `CHANGELOG.md`, `decisions/P2-indexing-sync/probe-results.md`).

| Finding | Result |
|---|---|
| X-1 (shared) | applied, Phase 3 hunk: G3 is a plain `jq -e` against Phase 2's `install_codegraph.MCP_TOOLS`; E-5 removed from T0; both tool-list branches (seven tools or `status` only) supported by new standing rule 6 |
| X-2 (Phase 3 hunk) | applied: T2 owns wording inside Phase 2's `SUPERCLAUDE_CODEGRAPH_BEGIN/END` block; acceptance adds `! rg -q codegraph_explore` |
| X-3 | applied: Phase 3 adopts Phase 2's session-start-hook indexing model; mutating-verb check narrowed to `Bash(codegraph <verb>` invocation forms in commands, skills and agents; guide prose confined to its "Never" section |
| X-6 | applied (modified): case B dropped; P1 column is `deleted`/`floor`; new T0 step E-7 maps every Phase 1 slots-ledger row to a §1.2 row with a count check (verbatim anchor matching would fail because the ledger is written later by another executor) |
| X-7 | applied: rows 11, 20, 31 keep Phase 1's Grep floor below the codegraph tier; standing rule 9; tests assert both names |
| X-8 | applied: T6/T7 add a `_POST_REFRESH_ADDITIONS` set to `tests/recommend/test_routing_refresh.py` and run it |
| X-9 | applied: row 1 edits Phase 2's single `\| codegraph` row in place; T2 asserts exactly one |
| X-10 | applied: guide path goes inside the marked block (reaches Coder via marker re-sync) and T12 posts a Coder addendum on #323 |
| X-13 | applied: `! git worktree list \| rg -q cg-sandbox` |
| X-14 | applied: switch renamed `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off`; guide and user doc name both switches |
| X-18, X-19, X-20, X-22, X-23 | applied (X-19 modified: primitives call bare `codegraph` because their exact allowlists match only that form) |
| X-25 | applied (updated): cites F2's observed hide-and-block run instead of UNVERIFIED |
| X-4, X-5, X-11, X-12, X-15, X-16, X-17, X-21, X-24 | not applicable (Phase 1 or Phase 2 only; resolved by F1/F2) |
| F3-1 (new) | CLI `codegraph status` during an init empties the index (probe row 6); every CLI `status` is now `pgrep`-guarded |
| F3-2 (new) | row 21 step 7 invented a token outside the closed list; now keeps Phase 1's `[INFERRED]` text; rows 21/23 no longer redo Phase 1's Bash diagnostics rewrite |
| F3-3 (new) | the design doc `DES` (not owned by F3) still has the old switch name and unguarded status; spec §3 lists overrides (a)-(e) where the spec wins |

Handoff files under `.dev/codegraph-migration/handoff/` were not edited: this task is N=3 and the brief gives them to N=2 (F2).

A second pass (spec section "Second pass: advisory reflect on the generated plan") fixed the 12 reflect findings that came from the spec itself, for example `/sc:pr-submit` has no `--body-file` flag and `tests/core/test_how_we_work_routing_table.py:294` pins the routing-table members. The spec is now 424 lines.

## 2. Tasklist package

- Package: `.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/`
  - Plan: `TASK-WF-phase3CodegraphA-20261029-204913.md` (schema `workflow-plan/1.2`, 8 phases = spec groups 0 and A-G, 14 tasks: Task 1 = section 0 gate and baselines, Tasks 2-14 = spec T0-T12).
  - `source.md`: byte-exact snapshot of the final spec (`cmp` clean after the second pass).
  - `return-contract.yaml`: contract 1.1, `status: success`, `reflect_status: partial`.
  - `progress.md`: `/sc:implement` ledger header plus the `PLAN:` hash pin of the final plan and source (no task lines, so `/sc:implement` starts at Task 1).
- Execute with `/sc:implement` on that plan, started from the Phase 3 worktree root after the setup in the plan's Constraints (worktree from `origin/master`, package and `.dev/codegraph-migration/` inputs present there).
- Workflow gate (re-run on the final plan): 14 contiguous tasks, each with acceptance criteria; 8 phases (standard cap 4-8); no numbered or checkbox lines; no `.dev/tasks/to-do/` operational prefix.

## 3. Reflect status

- Advisory `/sc:reflect --mode pre` (workflow Wave 4). Report: `.dev/reflect/pre-phase3CodegraphA-20261029205359/REPORT.md`; contract: `.dev/reflect/pre-phase3CodegraphA-20261029205359/return-contract.yaml`. **Status: partial.**
- Path: Tier 1 card calibrated blind at C = 0.60; `coverage_degraded: parsed-sparse` (0 labelled ids, 119 inferred rows) forced Tier 2; two reviewers, sonnet (analyzer, calibrated 0.73) and glm-5.3 via the haiku alias (qa, calibrated 0.67), with the executor class (opus) excluded; `/sc:adversarial` merge at convergence 1.00, verdict refactor, 19 findings (0 critical, 9 important, 10 minor; one Regression, M-03).
- Coverage: 72 of 119 rows matched by word containment (`coverage_pct_union` 0.605); the other 47 are covered by an explicit section or row reference in the plan (`artifacts/unmapped-triage.yaml`); 0 real gaps.
- Why partial: the evidence-validator dropped 2 of 107 citations (a wrong line number, `task.md:6` should be `:7`; and `DES:456`, which governs `/sc:impact`'s report rather than the guide). Both findings still stand. No input drift.
- Fixes applied after reflect, by editing the generated plan (brief step 2): all 19 merged findings (M-01 to M-19). The most important:
  - M-01: `/sc:pr-submit` has no `--body-file`; Task 14 passes a plain placeholder `--body` and then sets the real body with `gh pr edit --body-file`.
  - M-03: Task 12 now updates `_OTHER_COMMANDS` in the routing-table test, which would otherwise fail.
  - M-04/M-19: one test-path set for baseline and final check, and every "pytest passes" criterion tolerates only baseline failures.
  - M-06: the worktree, package and inputs are set up before `/sc:implement` starts, because the ledger must sit in the checkout it changes.
  - M-08: Task 14 posts comment G and records URLs before its single commit, then re-runs the PR monitor on that push.

## 4. Required tasklist properties (brief item 3)

| Property | Where in the plan |
|---|---|
| Test command and commit point after every task group | Every task's acceptance names its test command and a commit; the last task of each phase (Tasks 2, 4, 5, 7, 9, 11, 12, 14) closes its group |
| Issue #323 progress-comment step at each commit point | Group comments 0 and A-G at the same eight group-closing tasks; the procedure (`gh repo view` check, `gh issue comment 323 --repo IronbellyOrg/IronClaude --body-file …`, URL into the decision log) is in Constraints |
| Decision rules | Constraints: simple = self; mid = option files plus an agent running `/sc:adversarial --compare <option files> --depth quick`; complex = `/sc:adversarial --compare <option files>`; each logged in `.dev/codegraph-migration/decisions/P3X-execution-log.md` |
| Final full verification task | Task 13: sync and `make verify-sync`, installed-path count, old-tool-name, mutating-verb, wildcard and explore searches, pin parity, the full test-path set against the baseline, and the live smoke in a fresh session |

## Open item for the coordinator

`.dev/codegraph-migration/` (spec, design doc, ledger inputs) is untracked on this branch; the plan requires it, and the package, to be present in the Phase 3 worktree created from `origin/master`. Commit or copy-in is the coordinator's call (the brief says the coordinator stages `.dev/tasks`); the plan escalates rather than reconstructs if they are missing.

## Decisions

| Decision | Options considered | Method | Rationale |
|---|---|---|---|
| Phase 3 adopts Phase 2's session-start-hook indexing model (X-3) | keep "init only in `/sc:graph init`"; spawn `/sc:adversarial` | self | Evidence settles it: Phase 2 merges first and its hook came from an adversarial run plus sandbox probes; the review reached the same conclusion |
| Status-only tool-list branch: same primitive text, CLI lookup verbs in orchestrators, floor elsewhere | Grep floor only; separate text per branch | self | Follows the access decision's adversarial failure branch (P3-D1, §9.1) and `orchestration/README.md:41`; a later Phase 2 flip needs no Phase 3 edit |
| Guard every CLI `codegraph status` with `pgrep` (new finding F3-1) | no guard; MCP only | self | `decisions/P2-indexing-sync/probe-results.md` row 6: `status` during an init empties the index, and Phase 2's hook starts one in every new checkout |
| Kill switch named `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` (X-14) | keep `IRONCLAUDE_CODEGRAPH`; one combined switch | self | Phase 2 fixes the `SUPERCLAUDE_CODEGRAPH_` prefix and leaves the primitive switch to Phase 3; a combined switch would change Phase 2's hook contract |
| X-6 slots map by count check, not verbatim anchor match | review's anchor-text script | self | The ledger is written later by another executor; its anchors need not match this spec's Anchor column verbatim |
| Spec wins over the design doc for overrides (a)-(e) (F3-3) | edit the design doc | self | The design doc is outside F3's ownership; the spec lists each override explicitly |
| Group comments at the eight group-closing tasks, every task commits | a comment after every task commit | self | Spec §6 posts per group; "each commit point" in the brief is read as each task-group commit point, as F1 and F2 did |
| `source.md` written by `cp` plus `cmp`, refreshed after the second spec pass | Write tool | self (necessary deviation from the workflow protocol) | Byte-exactness is the requirement; the protocol's Write path cannot guarantee it for a 424-line spec |
| Edited the generated plan after reflect | leave reflect advisory only (workflow protocol rule) | self (forced by the brief, step 2) | The brief says to fix plan defects in the plan; the edit came after the workflow run finished |
| Fixed the 12 inherited findings in the spec too | plan only | self | The spec is F3-owned and the plan cites it as source of truth; leaving the spec wrong would re-introduce the defects |
| Accepted reflect `partial` without a rerun | rerun reflect | self | The two dropped citations do not change any finding; no input drift |
| Two reviewers instead of three | three | protocol-forced | The executor class (opus) is excluded from the reviewer pool and no backfill class exists |
| `progress.md` seeded with the ledger header and `PLAN:` pin | leave it to `/sc:implement` | self (brief's observable acceptance) | Same format `/sc:implement` writes; it re-pins a changed hash before its first task |
| No adversarial run for applying review findings | one run per finding | self | Each finding was settled by its cited source; none had two viable options. No `decisions/F3-*` folder was needed |
