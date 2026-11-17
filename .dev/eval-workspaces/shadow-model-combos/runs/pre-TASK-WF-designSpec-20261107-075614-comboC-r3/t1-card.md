# Tier 1 reflection card (UC-1, pre-execution)

hypothesis_source: orchestrator-inline (UC-1 has no deviation candidates for root-cause-analyst)

## Scope

Spec: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md` (378 lines, design spec v3 for the `/sc:pr-submit` merge guard, issue #375).
Plan: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md` (200 lines: a Constraints block and 13 tasks in 5 phases).

Temporal anchor: the spec says it read the repository at master `e8db2fe66` (spec line 13). The plan was executed later; HEAD now contains the implementation (commit `0b8a5801d`). Every repository fact below was read from a `git archive` of `e8db2fe66` extracted to `artifacts/base-e8db2fe6/` in this run's output directory, never from HEAD. A claim that holds only at HEAD is post-execution evolution, not a plan defect.

## Coverage (Step 1B.0, deterministic)

- Pass 1 (labeled IDs): 0 hits in spec and plan. The spec labels its content `F1..F13`, `FR-n`, `G1..G6`, `O1..O4`, none of which match `ID_REGEX`.
- Pass 2 (quote-pinned inference): 34 valid rows (2 dropped at emission because the quote was not in the cited line).
- `coverage_pct` = null (parsed total 0); `coverage_pct_union` = 0.8824 (30 of 34 matched by the containment rule); `S_dev_density` = 0.1176.
- Parse-density guard: `inferred_count` (34) > `parsed_count` (0) so `coverage_degraded: parsed-sparse`, and Tier 1 may not stop.
- The four unmatched rows are lexical misses of the 0.6 containment rule, not necessarily plan gaps: INF-008 (`HALT_UNAVAILABLE(timeline_unreadable)`, a symbol the plan covers as "all 11 rows"), INF-016 (inert below monitor 3, stated in Task 12 prose), INF-019 (script exit codes, covered by Task 7 acceptance wording), INF-032 (the `Depends on:` rule, which the plan itself follows). INF-035 matched Task 4 at 0.6667 although the docs rows belong to Task 13: a false positive of the same rule.

## Facts verified at the base commit (all hold)

- F1 enum has exactly 43 members: `models.py:3` and `models.py:24` say "43", `run_log.py:117` says "43 closed".
- F2 `_NEW_KEY_DEFAULTS` at `tests/pr_submit/test_run_log.py:312`, exact key-set asserts at lines 403-404.
- F3/F13 `recovery.py:40-42` holds `BRANCH_A_LANDED = "landed"`, `BRANCH_B_NOT_LANDED = "not_landed"`, `BRANCH_C_AMBIGUOUS = "ambiguous"`; `recovery.py:37` imports `RunLog`.
- F4 `conflicts.py:46` `CONFLICT_CYCLE_PREFIXES = ("sync-", "conflict-")`, `conflicts.py:1242` `is_conflict_cycle`.
- F5 `fsm.py:104` is the one enum flag; `SkillArgs` at `fsm.py:54`.
- F6/F7/F12 pins: `CORE_PURE_FILES` (`test_static_grep.py:37`), `_RESOLUTION_SCRIPTS` (`test_static_grep.py:479`), `WRITE_VERB_RE` and `WRITE_VERB_CLASSIFICATION` (`tests/skills/test_worker_contract.py:1098`, `:1166`).
- No import cycle: `run_log` would import `merge_guard`, which imports only `conflicts`; `conflicts` imports `fsm` and `models`; `fsm` imports `loop_guard`, `models`, `severity_router`. None of them imports `run_log` or `recovery`.
- `tests/pr_submit/__init__.py` exists, so Task 11 importing a helper from another test module resolves.

## Hypotheses (candidate findings)

H1 (analyzer, MAJOR, non-blocking): `resume_decision` row 4 cannot be implemented from its own signature. Spec line 166 says row 4 "re-enter[s] `release_decision` with `push_completed=True`", but `release_decision` (spec line 107) needs `cycle_id`, `applied_edits` and `target_sha`, and `resume_decision` (spec line 109) receives none of them. Task 4 (plan lines 70 and 77) repeats the row and its acceptance only asserts the returned action, so an implementation that passes `target_sha=read.head_sha` (making the head check vacuous) would pass every listed test.

H2 (analyzer, MAJOR, non-blocking): the Wave 0 bullet is specified two incompatible ways. Spec line 241 says it applies at every ordinal and "contains no L3 or `draft` condition", and in the same cell says "at L3 with `--merge-guard off` it prints the unprotected line once". Task 9 (plan lines 137 and 140) copies both, and its acceptance test must fail when the bullet "names an L3 or `draft` condition". A bullet that satisfies the print rule names L3; the test as worded cannot be both written and passed.

H3 (qa, MINOR): Task 2 acceptance (plan line 49) greps `43` and wants "no remaining claim that the enum has 43 members". `models.py:93` carries the comment "the 42nd-43rd" and `models.py:3` carries a breakdown sentence; the grep will still print hits, so the check is a judgment call, not a mechanical one.

H4 (qa, MINOR): Tasks 7, 8 and 12 restrict the classification-entry step to lines that match `gh pr` or `gh api` (plan lines 108, 124, 182), while the Constraints block (plan line 22) and spec 4.7 (spec line 255) also name git write verbs, and `WRITE_VERB_RE` (`test_worker_contract.py:1098`) matches `git add|commit|push|merge|stash|update-ref|worktree`. A new ref line that mentions `git push` is unclassified and fails `test_every_write_verb_hit_is_classified`; the per-task wording would not prompt an entry for it.

## Risk surface

- Tests outside `tests/pr_submit` and `tests/skills/test_worker_contract.py` run only in Task 13 (spec line 301 says a repo-wide pin escaped two earlier reviews). A late failure there would force an edit to a file whose classification entries are already written, and a later edit of a classified line makes the entry stale.
- Release-gate items G1 (live part), G2 (live part), G4, G5, G6 are explicitly recorded OPEN (plan line 24, spec lines 326-335); the plan does not claim them verified.
- Dependency lines: Task 6 depends only on Task 1 though Task 9 (flag row) needs it, which is satisfied transitively through Task 9.

## Recommendations

1. Add to Task 4 the inputs `release_decision` needs when `resume_decision` row 4 re-enters it (state where `cycle_id`, `applied_edits` and `target_sha` come from) and an acceptance case that fails when `target_sha` is taken from the live read.
2. Rewrite the Wave 0 acceptance in Task 9 so the test checks position and the literal `off` line, and separates "applies at every ordinal" from the `off` print condition.
3. Make Task 2's `grep` criterion name the files and the exact strings that must be gone (`exactly 43`, `43 closed`, `The 43 event types`).
4. In Tasks 7, 8 and 12 say "every line that `WRITE_VERB_RE` matches", not only `gh pr` and `gh api`.
