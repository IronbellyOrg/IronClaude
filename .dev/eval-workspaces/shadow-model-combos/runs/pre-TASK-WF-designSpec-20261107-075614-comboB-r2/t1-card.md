---
card: t1-reflection
mode: pre
spec: source.md (378 lines, sha256 a865f397...)
tasklist: TASK-WF-designSpec-20261107-075614.md (200 lines, 13 tasks, sha256 044809e3...)
author: orchestrator (T1, single agent; grounded with git show e8db2fe6, repo Read/Grep, codegraph status fresh)
codegraph: index_state=fresh (3322 files); the audited code is pr_submit Python plus shell and tests, found by Grep and Read
---

# T1 reflection card: plan vs design spec

## Summary

The plan covers the spec well: every file of source.md section 6, every test named in section 7 and every plan note of section 10 maps to a task (see coverage). The defects I found are contradictions or gaps inside acceptance criteria and signatures, not missing work. None of them makes the plan unbuildable. Three are MAJOR, four MINOR.

## Coverage (UC-1)

Pass 1 found 0 parsed ids (the spec labels requirements FR-n, F-n, G-n, which `ID_REGEX` does not match). Pass 2 produced 66 quote-pinned inferred rows (all 66 quotes verified verbatim in source.md), 60 matched by the containment rule, 6 left unmapped by the rule (INF-006, 023, 025, 038, 042, 065). Reading the six by hand, all six are present in the plan (Task 8 held-guard report; Task 3 BRANCH equality test; Task 4 classify_toggles; Task 6 "Leave RunConfig and run_skill unchanged"; Task 7 idempotent `--to`; Task 3 `held_cycle_published`), so the lexical rule under-matches; no real coverage gap. `coverage_pct` (parsed-only) is null; `coverage_pct_union` 0.9091; `S_dev_density` 0.0909; `coverage_degraded: parsed-sparse`. Artifacts: artifacts/coverage-matrix.json.

## Findings

F1 MAJOR, contradiction (Task 7). The acceptance criterion asks that a static scan assert "every `gh` line carries `--repo` or a `repos/` path" (plan line 113) and also that the new script join `_RESOLUTION_SCRIPTS` and pass its tests (plan line 108, 113). Those tests require a line containing `gh repo view --json nameWithOwner` (tests/pr_submit/test_static_grep.py:549, inside the tests that use `_RESOLUTION_SCRIPTS` at :481), which carries neither `--repo` nor `repos/`; the model script has exactly that line (scripts/retrigger-review.sh:50). Both cannot hold unless the new scan reuses the existing `_repo_scoped` predicate, which accepts the resolution idiom (test_static_grep.py:35, :107). The plan names the stricter wording instead.

F2 MAJOR, under-specified signature (Task 4, spec 4.1). `resume_decision` row 4 is "re-enter `release_decision` with `push_completed=True`" (source.md:166), but `resume_decision`'s documented parameters (source.md:109, plan line 70) omit `cycle_id`, `applied_edits` and `target_sha`, which `release_decision` needs (source.md:107). No `GuardAction` value stands for "re-enter" (source.md:82-85). The acceptance criterion (plan line 77) cannot be written as stated. An implementer who omits the head proof would release without confirming the head, breaking the rule that release needs a confirmed push.

F3 MAJOR, report gap (Task 3, Task 8). The spec says a halt with reason `draft_guard_unavailable` reports `unavailable` (source.md:112, :68), but `guard_status(guard, mode, ordinal)` has no halt input, and plan line 61 pins "no record at ordinal 3 gives `released`". An engage that halts because the read or the timeline failed writes no guard event, so the run reports `released` for a halt. No task (Task 8 Exit report, plan line 124; Task 11) assigns the halt-reason override or tests it.

F4 MINOR, untested fold field (Task 3). `guard_status` maps `DISABLED` + `user_override` to `user_override` (source.md:112), but the fold table row for `settled(any, skipped, user_override)` (source.md:206) does not say `disabled_cause` is set, and Task 3's fold criterion (plan line 60) tests `already_draft` only. A fold that leaves the cause empty passes Task 3 and mis-reports.

F5 MINOR, weak baseline (Task 1, Task 13). Task 1 records the base failures before any `make sync-dev` (plan line 33). The repo notes that fresh worktrees fail about 43 mirror/ruff tests until `make install` and `make sync-dev` run and to record the baseline after both (docs/memory/reflect/deviation-patterns-post-release-v5.0.0.md:7). Task 13 passes when no failing id is "absent from the base-commit record" (plan line 199), so a feature-caused mirror failure that is also in the stale baseline is hidden; only two files are re-run separately.

F6 MINOR, unowned mapping (spec 4.1/4.4). `GuardRead` fields (`is_draft`, `head_sha`, `auto_merge_armed`; source.md:88-91) differ from the script's JSON keys (`isDraft`, `headRefOid`, `autoMergeRequest`; source.md:230). No task or function does the conversion, and the SKILL has no python fence to do it.

F7 MINOR, test wording (Task 9). The Wave 0 bullet must name the `--merge-guard off` L3 case (plan line 137) yet its test must fail on "L3 or `draft` gate wording" (plan line 140); a sentence "no draft call is made" contains the word `draft`.

## Risks not findings

- Unverified outside the build: gates G1, G2, G4, G5, G6 stay OPEN by owner decision (source.md:326); the plan handles this correctly.
- Task 1 runs the full suite before editing; runtime is long but bounded.

## Recommendations

R1 Task 7: reuse `_repo_scoped` from test_static_grep.py for the new scan instead of the literal wording.
R2 Task 4/spec 4.1: add `cycle_id`, `applied_edits`, `target_sha` to `resume_decision` (or return a `RELEASE_CHECK` action) and say what row 4 returns.
R3 Task 3/8: add a status override for the `draft_guard_unavailable` halt, with a test.
R4 Task 3: add a `disabled_cause == user_override` fold assertion.
R5 Task 1: run `make install` and `make sync-dev` before recording the baseline.
R6 Add a one-line read-JSON-to-`GuardRead` mapping to the Resume/Exit section of the ref, with a test.
R7 Task 9: state that the test checks gate wording of the print rule, not the word `draft` in general.

## Self-grade (uncalibrated, for the record only)

Citation grounding high; coverage union 0.91; risk surface moderate (no blocking defect found); recommendations actionable.
