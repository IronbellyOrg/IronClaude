# Tier 1 reflection card (UC-1, pre): merge-guard design spec vs. its 13-task plan

Spec: `source.md` (378 lines, sha256 a865f397...). Plan: `TASK-WF-designSpec-20261107-075614.md` (200 lines, sha256 044809e3...).
Code facts are checked against base commit e8db2fe6 (the commit the spec says it was read from); excerpts are in `artifacts/base-grounding.md`. HEAD has evolved (the feature has since landed), so HEAD files are not evidence for what the plan could know.

## Coverage (Step 1B.0, two passes)

- Pass 1 (regex): 0 parsed IDs in spec and plan (labels are F1..F13, G1..G6, O1..O4, FR-n; none match `R-/REQ-/SPEC-/T-`). 
- Pass 2 (inference): 75 quote-pinned rows (`artifacts/inf-rows.tsv`, `artifacts/coverage-matrix.json`). 61 matched by the 0.6 containment rule, 14 unmatched. Union coverage 0.8133; `coverage_pct` is null (no parsed rows); `coverage_degraded: parsed-sparse` (75 inferred > 0 parsed), so the Tier-1 stop is forbidden.
- Manual read of the 14 unmatched rows: INF-012, 021, 023, 033, 034, 036, 037, 040, 055, 061, 062, 064, 068 and INF-003 are covered by a task whose wording differs from the quote (for example INF-021 by Task 3 AC5, INF-023 by Task 4, INF-033 by Task 3 AC2 "not_applied", INF-055 by Task 13 AC3). Two have no acceptance criterion: INF-036 (flag "accepted and inert below ordinal 3", plan 98-102 has no inertness check) and INF-037 (`RunConfig`/`run_skill` unchanged, plan 98 states it, no AC). Both MINOR.

## Findings (Tier 1)

- T1-F1 (MAJOR, contradiction): `resume_decision` cannot do what its row 4 says. Spec 109 gives the signature `resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)`; row 4 (spec 166) says "re-enter `release_decision` with `push_completed=True`", and `release_decision` (spec 107) needs `cycle_id`, `applied_edits` and `target_sha`, none of which `resume_decision` receives. Without `target_sha`, release row 8 (spec 156) can never match, so a crash after a normal push would always end in `HOLD`, contradicting the sequences at spec 279-280. Task 4 copies the signature (plan 70) and its acceptance criterion (plan 77) only says "re-enter `release_decision`", never what action or reason comes back.
- T1-F2 (MINOR, unpassable-check): Task 12's grep criterion (plan 185) looks for `merge-guard` on "the section heading", but the plan names the section "Merge guard" with a space (plan 182); the literal grep cannot match that heading.
- T1-F3 (MINOR, missing-requirement): nothing assigns the mapping from the script's `--read` JSON keys (`isDraft`, `headRefOid`, `autoMergeRequest`, spec 230) to the `GuardRead` fields (`is_draft`, `head_sha`, `auto_merge_armed`, spec 88-89). Task 7's AC (plan 111) checks that the keys are printed, not that `autoMergeRequest` is a boolean; `gh` returns an object or null for that field, and `GuardRead.auto_merge_armed` is a bool.
- T1-F4 (MINOR, other): Task 7's `_RESOLUTION_SCRIPTS` criterion (plan 113) is vacuous when the executor decides, per plan 108, not to add the script to that list.
- T1-F5 (MINOR, other): Task 5 asserts `state["draft_guard"]["phase"] == "held"` and phase `engage_pending` (plan 90) and Task 3 asserts `disabled_cause == "already_draft"` (plan 60), but the spec never states the string values of `Phase` (spec 80); only Task 5 would force the convention.

## Verified non-issues (checked, no finding)

- Event-count pins: every "43" at base is in the Task 2 edit list (`artifacts/base-grounding.md` 80-89).
- No import cycle: `merge_guard` -> `conflicts` -> `fsm` -> `loop_guard/models/severity_router`; `run_log` imports only `models` (`artifacts/base-grounding.md` 9-32). Task 5's fresh-interpreter import check covers it anyway.
- `allowed-tools` already grants `Bash(gh|git|uv|make|jq *)` and scripts are checked only for existence (`artifacts/base-grounding.md` 4-7, 52-77), so no front-matter edit is missing.
- Real crash-window API exists: `resolve_crash_window(run_log, dangling, *, remote_reachable, observed_remote_sha)` returns `(branch, state)` (`artifacts/base-grounding.md` 43-49), so Task 11's "real branch" tests are feasible.

## Recommendation

Plan is largely faithful (union coverage 0.81, all 12 named tests and all section 4.1 tables carried). Fix T1-F1 before execution by giving `resume_decision` the `cycle_id`, `applied_edits` and `target_sha` inputs (or stating that row 4 returns a release request the caller completes). Escalation is forced regardless (tier pin 2, `coverage_degraded`).

self-reported confidence: 0.70
