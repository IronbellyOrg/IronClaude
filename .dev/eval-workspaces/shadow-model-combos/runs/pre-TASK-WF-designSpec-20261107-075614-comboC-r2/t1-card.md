# Tier 1 reflection card (UC-1, pre-execution)

Spec: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md` (378 lines, design spec v3 for the pr-submit merge guard).
Plan: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md` (200 lines, 13 tasks, 5 phases).
Orchestrator: the session model (inline T1 card, hypothesis_source: inline). Plan line numbers below are from a fresh Read of both files this turn.

## Coverage (Step 1B)

Pass 1 (ID regex) found 0 parsed ids in either file (the spec labels requirements FR-n, F-n, G-n, O-n, which the regex does not match). Pass 2 inferred 86 quote-pinned rows, 2 dropped at emission for a non-verbatim quote, 84 kept. Deterministic containment match: 70 of 84 mapped (`coverage_pct_union` 0.8333), 14 unmapped. `coverage_degraded: parsed-sparse` (inferred 84 > parsed 0), so no Tier 1 stop is allowed. Most of the 14 unmapped rows are lexical misses (the plan carries the idea in other words), see the matrix `artifacts/coverage-matrix.json`. `S_dev_density` = 14/84 = 0.1667.

## Findings

- **T1-F1 (MAJOR, contradiction).** Task 9 requires the Wave 0 bullet to say that "at L3 with `--merge-guard off`" the line is printed once (plan line 137), yet the same bullet must "carry no L3 or `draft` condition" and its criterion says the test "fails ... when it names an L3 or `draft` condition" (plan line 140). A bullet that satisfies the first sentence names L3. Source: spec line 59 and line 241 hold the same tension, so the plan copies it.
- **T1-F2 (MAJOR, missing-requirement).** The FR-16 retry (spec line 315: "one retry, `already_in_state` counts as confirmed, `release_pending`") has no decision-table row, no fold rule and no acceptance criterion. Task 8 puts "one retry" into the ref prose (plan line 124), and Task 11 only names `test_guard_release_failure_retries_once_and_reports` (plan line 169).
- **T1-F3 (MAJOR, missing-requirement).** No criterion checks that the guard, the push triad and `rereview_requested` share one `cycle_id` (spec line 251). Task 11's trace asserts event order only (plan line 170) and Task 8 only requires the ref to name the minting place (plan line 127).
- **T1-F4 (MAJOR, unpassable-check).** Task 7's criteria check that `--read` prints the keys, not their values (plan line 111). Spec line 230 shows `"autoMergeRequest":false` and a `transitions` count made with `wc -l`, while `gh pr view --json autoMergeRequest` returns an object or null, so the boolean needs a conversion that no criterion tests.
- **T1-F5 (MAJOR, other).** `engage_decision` row 6 returns `HOLD(ownership_unproven)` and `settled(draft, failed)` leaves the phase at `RELEASE_PENDING` with `owned_draft` false (spec lines 138, 199). After a failed engage every later engage returns HOLD. Neither spec nor plan says whether edits continue on a HOLD at engage, so a non-draft PR could be edited. Task 4 and Task 8 test rows, not this consequence.
- **T1-F6 (MINOR, other).** Plan line 25 says the scope limits are "non-goals of ./source.md". source.md has no non-goals section; "no labels, commit statuses or rulesets" and "a second concurrent run ... is unsupported" appear nowhere in it (grep of the spec found only the word "label" in the owner-decision line 6).
- **T1-F7 (MINOR, other).** Task 11's first criterion passes once the 12 test names exist (plan line 169). The case list has no moved-head scenario although the test name says "moved_head" (spec line 319).
- **T1-F8 (MINOR, other).** Task 13 says `git status --short` lists "gitignored `.claude/` mirrors" (plan line 200); git status never lists ignored files.
- **T1-F9 (MINOR, other).** `Phase` string values are never defined in Task 3 (spec line 80 lists names only); Task 5 pins lowercase strings (`held`, `engage_pending`) in its criteria (plan line 90).

## Grounding notes

- The feature is already present in this working tree (`src/superclaude/pr_submit/merge_guard.py`, `scripts/set-draft-state.sh`, `refs/merge-guard.md`, `EventType` has 45 members). Grounding therefore reads post-implementation code; every combo of the experiment sees the same tree.
- Held: all 12 test names of spec section 7 appear in Task 11; every file of spec section 6 has a task; Task 2 names the test in the repo (`test_eventtype_is_45_members_...` now).

## Rubric inputs

S_scope = 13 tasks; S_domains = 3 (code, tests, docs/protocol); S_dev_density = 0.1667; coverage_pct null (parsed 0), coverage_pct_union 0.8333; coverage_degraded parsed-sparse.
