# T1 reflection card (UC-1, pre-execution)

Spec: input/TASK-WF-designSpec-20261107-075614/source.md (378 lines)
Tasklist: input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md (200 lines, 13 tasks, 5 phases)
Attribution note: this package already executed (landed in commit 0b8a5801d, parent 0e486ab8d). The spec's facts F1-F13 were
re-read at the parent commit 0e486ab8d and hold there (EventType 43 members, `_NEW_KEY_DEFAULTS`, `_RESOLUTION_SCRIPTS`,
`CORE_PURE_FILES`, `WRITE_VERB_CLASSIFICATION`, `BRANCH_*` constants, fsm.py has 1246 lines so the 900-943 cite is valid). HEAD
now carries the implementation, so a citation of HEAD text as a plan defect or as a gap must be checked against 0e486ab8d.

## Coverage (Step 1B.0 two passes)

- Pass 1 (ID regex, fences skipped): 0 parsed IDs in the spec, 0 in the tasklist (the spec uses FR-n, F-n, G-n, O-n labels,
  none of which match `R-|REQ-|SPEC-|T-`).
- Pass 2: 32 inferred rows, every quote verified verbatim against its cited spec line (artifacts/coverage-matrix.json).
- Containment matching: 24 of 32 matched (`coverage_pct_union` 0.75); `coverage_pct` is null (no parsed rows).
- `inferred_count` (32) > `parsed_count` (0), so `coverage_degraded: parsed-sparse`: no Tier-1 stop; routed to Tier 2
  (also pinned by `--tier 2`).
- The 8 `none` rows are partly matcher noise (word overlap below 0.6 although a task covers the item): INF-004 (Task 3
  states the gh/git ban), INF-014 (Task 6 "Leave RunConfig and run_skill unchanged"), INF-015 (Task 7 "is idempotent"),
  INF-011 (Task 3 fold AC). Truly weak: INF-026 (no `file:NNN` pointers in protocol prose: stated in Constraints and Task 8
  prose, no AC), INF-019 (single source for the cycle id: Task 1 O1 records it, Task 8 AC only states the place).

## Candidate gaps (hypotheses for the reviewers; none is final)

1. Task 11 acceptance criteria assert that twelve test NAMES exist, a trace order, and forbidden calls, but not the behaviour
   of most listed scenarios (foreign toggle continues the run, engage failure halts before any edit; the merged-PR case does carry a behaviour AC about push events). A test
   with the right name and an empty body would satisfy the name AC.
2. Spec 4.6 says the guard, the push triad and `rereview_requested` of one cycle share one `cycle_id`. No AC asserts the
   shared id; Task 8 AC says only that the ref names the minting place.
3. Task 8 text says "no `file:NNN` pointer" and spec section 10 requires it; no AC checks it (constraint without AC).
4. Task 2 AC3 says `grep 43 ...` "shows no remaining claim that the enum has 43 members"; models.py keeps the comment "the
   42nd-43rd", so the grep output is never empty and the AC is a judgment call.
5. Task 7 prose requires `gh api --paginate`; no AC feeds a multi-page timeline to the fake `gh` (spec F9, gate G2).

## Confidence

Self-reported confidence 0.72: structure and dependencies were traced, the pinned symbols exist at the parent commit, but the
reviewers have not yet read the ACs against each spec clause.
