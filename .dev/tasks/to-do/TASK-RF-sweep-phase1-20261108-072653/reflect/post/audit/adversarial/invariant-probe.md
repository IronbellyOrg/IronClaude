# Invariant Probe Results

## Round 2.5 - Fault-Finder Analysis (agent a755eade9d72a3a09, opus, read-only; statuses re-checked by the orchestrator where noted)

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | guard_conditions | A worker-list row dropped for a missing, empty or non-string `dispatchId` (C-004) is a Drift because no criterion fails | UNADDRESSED | MEDIUM | `probes.py:1109` names the unscanned source row `orca worker-list {run} row {i}`; `classify.py:690` reads only `orca worker-list {run}`; a non-empty invalid string id still becomes a row and trips path-B `earlier_pane` (`probes.py:1115-1118`, `classify.py:739`); the guard fails open only when every non-ready row of the window is dropped (`classify.py:730`, `:733-739`, `:759-762`). `test_classify.py:970-973` pins the empty-list control as `person_started=True` / IDLE. Orchestrator ruling: the five list-incomplete cases are the whole of FR-010's enumerated rule (docstring `classify.py:679`), a dropped row is a gap in completeness detection outside them, so it stays Drift medium; it becomes a wrong-class bug only if real Orca emits id-less rows |
| INV-002 | sufficiency_challenge | The evidence is enough to call zero findings blocking | UNADDRESSED | MEDIUM | Falsifier: real `worker-list` replies with rows lacking `dispatchId` (queued or undispatched workers) would make every recent transcript of that Run a person-started IDLE session (INV-001 path). Orchestrator check: `tests/sweep/fixtures/captured-worker-list.json` holds 5 worker rows and every one carries `dispatchId` (10 matching key lines for dispatchId and taskId); rows in other states are UNVERIFIED |
| INV-003 | interaction_effects | The C-003 runaway-child difference (`unavailable` instead of `call_failed`) is only a mechanism and memory issue | ADDRESSED | LOW | a later timeout not cut by the budget returns `unavailable` (`probes.py:264-265`), sets `state.available=False` (`:1027-1028`, `:1172-1173`) and `_origin_unknown` adds the Orca-unavailable note (`classify.py:682-683`): fails closed for origin; later Orca sources go unscanned |
| INV-004 | interaction_effects | The first-call rule, the budget-cut rule and the timeout rule compose correctly | ADDRESSED | LOW | budget-cut conversion runs before the first-call conversion (`probes.py:349-357`); a first call with no budget left returns before `orca_calls` is incremented (`:336-339`) |
| INV-005 | guard_conditions | The first-call rule only turns a nonzero exit or invalid response into `unavailable` | UNADDRESSED | LOW | any `call_failed` on the first call becomes `unavailable` (`probes.py:355-357`), including `output over 8 MiB` (`:270-273`); noted by reviewer 1 (variant-1-original.md:103) |
| INV-006 | count_divergence | The ledger limit boundary matches the SPEC | ADDRESSED | LOW | `size > LEDGER_LIMIT` (`probes.py:560`, `:72`); SPEC "exactly 1 MiB is not a hit" |
| INV-007 | count_divergence | Over the limit only a partial first line of the tail is dropped | UNADDRESSED | LOW | `data.split(b"\n", 1)[1]` always drops the first line (`probes.py:565`); when the tail starts exactly on a line start a complete `FINAL:` line is lost; a tail with no newline searches nothing; pinned by `test_ledger_tail_drops_a_first_line_that_the_cut_split` (`test_probes_allowlist.py:1336-1346`) |
| INV-008 | count_divergence | The full-page rule `len(workers) >= 100 or hasMore` marks the list as truncated | UNADDRESSED | LOW | `len` counts dict entries after filtering (`probes.py:1042-1046`); malformed-reply edge only; an exact 100-row total is marked truncated (conservative) |
| INV-009 | collection_boundaries | The show-cap split behaves for zero Runs, one Run or more Runs than shows | ADDRESSED | LOW | `share_shows` early return (`probes.py:141-142`), leftover pass (`:148-155`), `take_show` global total (`:159-161`) |
| INV-010 | count_divergence | The window cap is 720h | ADDRESSED | LOW | `commands.py:45-49` accepts `720h` and `30d`, rejects `721h` and `31d` |
| INV-011 | sufficiency_challenge | The FR-010 tests prove the guard behaves as it will in production | ADDRESSED (orchestrator re-check) | LOW | the `test_fr010_*` cases take the `path_a` fixture (`test_classify.py:117-119` sets `JOIN_PATH = "A"`) but production uses path B (`classify.py:40`); path B is exercised by the separate `path_b` fixture tests (`test_classify.py:123-125`, `:1314-1492`: window, inclusive bounds, reused pane, conflict, note order). Original severity MEDIUM lowered after the re-check |
| INV-012 | sufficiency_challenge | Tests assert what their names say | UNADDRESSED | LOW | `test_fr010_full_page_uncaptured_continuation` passes `truncated=True` directly (`test_classify.py:947`), so it does not run the probe's full-page rule (`probes.py:1046`); adds to the misnamed `..._read_as_head_and_tail` test and the two "still publish" tests |
| INV-013 | state_variables | Rule 5 inert, the output-style exception and the sweep skill's exempt reply interact cleanly | UNADDRESSED (not probed) | LOW | UNVERIFIED by the fault-finder (tool budget spent on the code paths); reviewer 3 checked the skill/style conditions (R3-F9) |

## Summary

- **Total findings**: 13
- **ADDRESSED**: 6 (INV-003, INV-004, INV-006, INV-009, INV-010, INV-011)
- **UNADDRESSED**: 7
  - HIGH: 0
  - MEDIUM: 2 (INV-001, INV-002: warnings, do not block convergence; both are folded into finding F-04 of the merge with the conditional escalation)
  - LOW: 5 (INV-005, INV-007, INV-008, INV-012, INV-013)
- Gate result: no HIGH + UNADDRESSED invariant, so convergence is not blocked by the invariant probe.
