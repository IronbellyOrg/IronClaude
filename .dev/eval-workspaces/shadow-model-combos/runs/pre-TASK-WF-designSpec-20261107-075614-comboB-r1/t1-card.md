# T1 reflection card (UC-1 pre, orchestrator pass)

Spec: source.md (378 lines). Plan: TASK-WF-designSpec-20261107-075614.md (13 tasks, 5 phases, 200 lines).
Mode pre, tier pinned 2 (`--tier 2`), engine shadow. This card is the Tier 1 work product; it feeds the reviewer briefs and is calibrated blind.

## Coverage (mechanical, artifacts/coverage-matrix.json)

- Pass 1 (regex IDs R-/REQ-/SPEC-/T-): 0 parsed rows. The spec labels its requirements FR-1..FR-23, F1..F13, G1..G6, O1..O4; none match the ID regex. `coverage_pct` = null, `coverage_degraded: parsed-sparse` (inferred 73 > parsed 0).
- Pass 2 (quote-pinned, 73 INF rows, every quote verified verbatim at its cited spec line by script): 63 matched to a task by containment (>= 0.6), 10 unmatched. `coverage_pct_union` = 0.863, `S_dev_density` = 0.137.
- Unmatched INF rows (mechanical, may be false misses where the plan states the same rule in different words): INF-004 (source.md:51 core decides, SKILL performs), INF-006 (:57 held guard reported with clear command at ordinals 0-2), INF-015 (:66 user_override settle), INF-019 (:75 no gh/git word in merge_guard.py; Task 3 does carry it), INF-043 (:216 flag effective only at monitor 3), INF-044 (:217 RunConfig unchanged; Task 6 says so), INF-046 (:234 --to idempotent), INF-062 (:301 never stage .claude; Constraints carry it), INF-067 (:364 Wave 0 hook wiring; Task 9 carries it), INF-069 (:369 no file:NNN pointers; Constraints carry it).

## Structural signals

S_scope 13 tasks; S_domains >= 3 (python code, tests, shell script, protocol markdown, user docs); S_dev_density 0.137. All signals point to escalation; the tier is pinned to 2 anyway.

## Grounding at the spec base commit e8db2fe6 (git show / git grep, not the working tree)

- Every symbol the plan cites exists at e8db2fe6: EventType (43 members, models.py), RunLog.rebuild_state and the `open_conflict_cycle` idiom, BRANCH_A_LANDED / BRANCH_B_NOT_LANDED / BRANCH_C_AMBIGUOUS, detect_crash_window, resolve_crash_window, CONFLICT_CYCLE_PREFIXES, is_conflict_cycle, `--conflict-max-tier`, SkillArgs / parse_args / build_arg_parser, CORE_PURE_FILES, test_tn50_core_pure_no_gh_git_tokens, _NEW_KEY_DEFAULTS, test_eventtype_is_43_members_with_silence_reviewer_and_conflict_events, test_conflict_max_tier_default_and_bounds, test_intent_and_validator_lines_say_tier_2, retrigger-review.sh (set -euo pipefail, exit 127), loop-guard.md heading "The 43 event types".
- No import cycle: conflicts.py imports only .fsm and .models; fsm.py imports loop_guard, models, severity_router; none imports run_log. recovery.py imports conflicts, models, run_log.
- The working tree is HEAD, which already holds the merged feature (merge_guard.py, commit 0b8a5801d). Any claim about what exists must be checked at e8db2fe6, not at HEAD.

## Candidate findings (reviewers must verify or refute)

1. Missing adapter: source.md:89-95 defines `GuardRead` as the "parsed output of `--read`", and the script prints camelCase JSON (`isDraft`, `headRefOid`, `autoMergeRequest`, source.md:230). No task in the plan writes the JSON-to-`GuardRead` conversion; Task 3 creates only the dataclass. Task 11's "small test driver" must invent it, and the SKILL prose never states the mapping. Candidate MAJOR, non-blocking.
2. Scenario tests exercise a test driver, not the protocol: the engage, release and resume sequences are SKILL prose (Tasks 8-10); Task 11 tests only a Python driver written in the same task, so a SKILL prose that disagrees with the driver would pass. Candidate MINOR.
3. Task 7 acceptance criterion 3 requires the script to "pass the `_RESOLUTION_SCRIPTS` origin-URL resolution tests", but the same task adds it to that list "only after reading the purpose of that list" (Task 1 O2). If O2 says do not add it, the criterion cannot be met. Candidate MINOR (internally conditional acceptance criterion).
4. Nothing assigns the PR-body gate statement or the `--merge-guard off` rule for the run that opens the PR (source.md:326); Task 1 only records it. Candidate MINOR.
5. Task 4 acceptance criteria test `engage_decision` rows with a guard present; the `guard is None` path of rows 2 and 5-7 (source.md:131-143) is not named. Candidate MINOR.
6. source.md:75 says the module imports only enum, dataclasses, re and is_conflict_cycle; the plan's Task 3 repeats it. A `from __future__ import annotations` line (used by run_log.py and recovery.py) is also an import. Candidate MINOR wording.

## Confidence and gaps

Grounded: base-commit symbol existence, import-cycle absence, coverage numbers. [INFERRED]: findings 2-6 rest on reading, not on a run. Not verified: live GitHub behaviour (gates G1, G2, G4, G5, G6 are explicitly open in the plan), and whether the 10 unmatched INF rows are real gaps.

## Recommendations (pre-execution)

- Add a task step or acceptance criterion for the `--read` JSON to `GuardRead` mapping (Task 3 or Task 4), with a test that feeds the exact script JSON line.
- State in Task 7 what happens when Task 1 O2 says the script must not join `_RESOLUTION_SCRIPTS`.
