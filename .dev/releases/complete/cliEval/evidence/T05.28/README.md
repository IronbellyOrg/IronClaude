# T05.28 Evidence — Phase 5 / M5 exit gate

## Files

- `eval-list.txt` — live `uv run superclaude eval list` capture
  (2026-05-21T22:46Z). Output: `real (version 1.0, 17 evals)`,
  exit 0. Confirms Verification 1 (15 conceptual / 17 expanded eval
  ids enumerate: E1, E2.{1,2,3}, E3..E15).
- `eval-doctor-check-coverage.txt` — live `uv run superclaude eval
  doctor --suite real --check-coverage` capture
  (2026-05-21T22:46Z). Output: `all HARD capabilities satisfied`,
  `coverage gate: 3/3 matcher(s) covered (passed)`. Confirms
  Verification 2.
- `eval-doctor-exit.txt` — `0`.
- `eval-run-parallel-8.log` — annotated full-suite run capture
  (2026-05-21T22:46:08Z, run_id `224608Z-fd761175`). Exit 0,
  duration 0.11s (well under the 600s NFR-PERF3 budget). All 17
  evals report status `PASS`. Confirms Verification 3 + Exit
  Criterion 1.
- `run-summary.json` / `run-summary.md` — copies of the canonical
  `summary.{json,md}` from `.dev/eval-runs/2026-05-21/224608Z-fd761175/`.

## AC mapping

See `CP-P05-END.md` § Verification (3/3 confirmed), § Exit Criteria
(3/3 met), § Acceptance Criteria (4/4 met).

## Status

`CP-P05-END.md` records `status: PASS`. The earlier `_new_run_id`
NameError that blocked an initial T05.28 evaluation has been
remediated upstream (commands.py:1322 defines `_new_run_id`,
called at commands.py:1709); the fresh 2026-05-21T22:46Z capture
runs clean end-to-end.

## Note on per-eval duration

Each eval reports `duration_sec: 0.0` because the body assertions
in `real.yaml` carry empty `expects: []` lists — the strict-form
scaffolding for the inherited fixtures / failing-fixture scripts /
multi-HOME orchestration is deferred to follow-up tasks per the
per-eval-task `spec.md §8.1` notes (see CP-P05-T19-T23 §Notes
"Scaffolding-gap inheritance"). M5 acceptance is the harness
contract holding under full-suite invocation, not real assertion
firings; the latter lands in M6 / post-M5 follow-ups.
