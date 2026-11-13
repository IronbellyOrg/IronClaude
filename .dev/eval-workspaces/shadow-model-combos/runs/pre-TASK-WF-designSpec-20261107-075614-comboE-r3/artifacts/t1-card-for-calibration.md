# T1 reflection card (UC-1 pre): TASK-WF-designSpec-20261107-075614 vs its design spec

Run: pre-TASK-WF-designSpec-20261107-075614-comboE-r3. Plan = `TASK-WF-designSpec-20261107-075614.md` (13 tasks). Spec = `source.md` (design of the pr-submit merge guard, issue #375).
Paths below are repo-relative under `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/` (P = the plan file, S = source.md).

## Attribution note (read before judging any HEAD text)
This package already executed. The implementation landed in commit 0b8a5801d (#428, 2026-11-07), parent 0e486ab8d. Checked with `git show 0e486ab8d:<path>`: at the parent `models.py` says "exactly 43 members" (docstring line 3, class docstring line 24) and has the comment "the 42nd-43rd" at line 93; `recovery.py` defines `BRANCH_A_LANDED`, `BRANCH_B_NOT_LANDED`, `BRANCH_C_AMBIGUOUS` (lines 40-42); `merge_guard.py` does not exist at the parent and exists at HEAD. The spec facts F1-F13 therefore hold at the parent. HEAD now carries the implementation, so a plan defect or gap claimed from HEAD text must be re-checked at 0e486ab8d. This is a plan-text audit: judge the plan and spec, not the shipped code.

## Coverage (Step 1B.0, two passes)
- Pass 1 (ID regex `R-|REQ-|SPEC-|T-`, fences skipped): 0 parsed IDs in the spec and 0 in the plan (the spec uses FR-n, F-n, G-n, O-n labels, none of which the regex matches).
- Pass 2: 61 inferred rows INF-001..INF-061, every quote verified verbatim against its cited spec line by script (artifacts/coverage-matrix.json).
- Containment matching (>= 0.6 content-word ratio against one task section): 54 of 61 matched, `coverage_pct_union` 0.8852, `coverage_pct` null (no parsed rows), `S_dev_density` 0.1148.
- `inferred_count` 61 > `parsed_count` 0: `coverage_degraded: parsed-sparse`, no Tier-1 stop; the run is also pinned to Tier 2 by `--tier 2`.
- The 7 `none` rows (INF-004, 013, 018, 023, 042, 056, 057) are mostly matcher noise: held-guard reporting is in Task 8 prose, the user-override scenario in Task 11 prose, the `ValueError` rule in Task 3 AC, the BRANCH equality test in Task 3 AC, RunConfig-unchanged in Task 6 prose, `Depends on:` per dependency in the plan's own structure. INF-057 (no `file:NNN` pointers) is a real constraint without an AC (H6).

## Candidate gaps (hypotheses; none is final)
H1. Task 11 gates three of its twelve named tests by name only. AC1 (P:169) requires that the twelve names exist; behaviour ACs cover the crash tests, the acceptance trace and the forbidden-call checks. The prose (P:166) lists no release-failure retry (spec test S:315), no unreadable-timeline-never-readies case (S:317) and no moved-head case (S:319). A test with such a name that asserts nothing passes.
H2. Cycle-id continuity is asserted by prose only. The spec says the SKILL mints one id at the end of Wave 3 and the push triad and `rereview_requested` reuse it (S:251), and `held_cycle_published` (S:108) matches on that id. Task 8 prose says so (P:124) but its AC (P:127) only requires the ref to name the single place where the id is minted; no AC says the push triad reuses it.
H3. `resume_decision` row 4 re-enters `release_decision` (S:166), which needs `target_sha`, `applied_edits` and `cycle_id` (S:107), but the `resume_decision` signature (S:109, repeated at P:70) carries none of them, so a pure function cannot honour the row without inventing inputs. Task 4 AC (P:77) tests the row-4 result without saying where those values come from.
H4. `settled(ready, skipped, not_applied)` returns to `HELD` "or `RELEASE_PENDING` when a failed release preceded it" (S:201). Task 3 AC (P:60) tests only the `HELD` outcome, so an implementation that always returns `HELD` passes.
H5. Task 7 AC (P:111) lists the `autoMergeRequest` key but not its type; the spec prints a boolean (S:230) while `gh pr view --json autoMergeRequest` returns an object or null, so a pass-through script satisfies the AC and breaks `GuardRead.auto_merge_armed`.
H6. Constraint without AC: "protocol prose carries no `file:NNN` pointers" (P:23, S:369) is repeated in Task 8 prose (P:124) but its AC list (P:128) tests only `src/superclaude`, fences and `gh` scope.
H7. Task 2 AC3 (P:49) greps "43" and expects no claim that the enum has 43 members; the parent `models.py` keeps the true comment "the 42nd-43rd" (line 93), so the grep keeps matching and the result is a judgment, not an exit code.
H8. Task 7 prose makes adding the script to `_RESOLUTION_SCRIPTS` conditional on a purpose check (P:108) while its AC (P:113) states the script "passes the `_RESOLUTION_SCRIPTS` origin-URL resolution tests": if the purpose check says no, the AC has nothing to run.
H9. The request key `guard:<run_id>:<cycle_id>:<to>:a<k>` (S:184) and the `--read` JSON to `GuardRead` mapping (S:88-90, S:230) have no named owner among the pure functions (S:99-110); both end up in SKILL prose or test code. Dependency order is otherwise acyclic and every file of spec section 6 has an owning task.

## Reflection
No blocking defect found at plan scope: the engage, release and resume tables are covered by Tasks 3 and 4 row by row, the fold table by Task 3, the flag by Task 6, the script by Task 7, the protocol text by Tasks 8-10, the docs by Tasks 12-13. The weak spots are mechanical-gate quality (H1, H2, H4, H6) and one spec-level interface hole (H3). Severity of every candidate is MINOR or low MAJOR; H3 is the only one that could make a literal implementer ship a wrong resume path.

## Findings block
(Tier 1 carries no findings-v2 block; the reviewers write one.)

confidence (self-reported): 0.68
