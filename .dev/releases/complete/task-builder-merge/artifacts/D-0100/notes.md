# D-0100 -- T05.17 Slow-cycle correction halt-safety regression sweep

**Task:** T05.17 -- Verify slow-cycle correction halt-safety regression sweep
**Roadmap items:** R-099 (X-003 rejection enforcement)
**Mitigation target:** K-005 false-halt-rate baseline for M7 audit prep
**Tier:** STANDARD  |  **Verification:** Direct test execution
**Date:** 2026-05-18

## 1. Goal

Final K-005 mitigation check: confirm `|F|=5,4`, `|F|=5,3`, `|F|=5,2`
and other legitimate slow-cycle fixtures continue to halt **only** on
the documented regression+monotonicity conditions, never on a
rate-of-shrink heuristic. Capture a false-halt-rate baseline that the
M7 K-005 audit can consume.

## 2. Method

The shared 4-step iterator at `tests/audit/_halt_emitter.py`
(`run_fix_cycle`) is the same helper exercised by TEST-015 / TEST-016 /
TEST-017 / TEST-022, so the sweep is load-bearing against the wire
contract emitter, not a parallel re-implementation.

Three trajectories were replayed via the sweep driver at
`sweep_runner.py`:

| Label     | Cycle 1 | Cycle 2     | Cycle 3 | Strict shrink? |
|-----------|---------|-------------|---------|----------------|
| `|F|=5,4` | 5 FAILs | 4 FAILs     | 0       | Yes (delta=1)  |
| `|F|=5,3` | 5 FAILs | 3 FAILs     | 0       | Yes (delta=2)  |
| `|F|=5,2` | 5 FAILs | 2 FAILs     | 0       | Yes (delta=3)  |

Each trajectory fixes the first `delta = |F_1| - |F_2|` cycle-1 FAIL
items into PASS at cycle 2 (no new FAILs introduced; no PASS@1 →
FAIL@2 flip) and converges to `|F_3|=0`. This is the legitimate
slow-correction shape the K-005 hazard warns about: a rate-of-shrink
threshold would falsely halt cycles 1→2 when shrink is "too slow".

## 3. Pre-conditions

- `make verify-sync` reported PASS at MIG-005 landing
  (commit `db6166e` -- M5 FR-CONV.5 wrapper, evidence in `D-0067`).
- T05.14 `test_slow_shrink_continues.py` (TEST-017) merged at
  commit `c9e2b12`.
- The binary monotonicity predicate `|F_{n+1}| >= |F_n|` is encoded
  in SKILL.md §A.9 (TEST-017 `test_monotonicity_predicate_is_binary`
  enforces this verbatim).

## 4. Sweep results

`uv run pytest tests/audit/test_slow_shrink_continues.py -v` -- 20/20 PASS
(0.03s). Full log: `pytest-slow-shrink-F-5-4.log`.

`uv run python sweep_runner.py` -- exit 0. Full log:
`sweep-results.log`. Inline:

```
T05.17 slow-cycle correction false-halt-rate sweep (X-003 rejection enforcement)
==============================================================================
trajectory      halt_message                              cycle_3_started   verdict
------------------------------------------------------------------------------
|F|=5,4         <none>                                    True              PASS
|F|=5,3         <none>                                    True              PASS
|F|=5,2         <none>                                    True              PASS
------------------------------------------------------------------------------
false_halts=0/3  false_halt_rate=0.000
```

### Per-trajectory verdict detail

For each row, the 4-step iterator records:

1. Step 1 (regression): PASS -- no PASS@1 item appears in FAIL@2.
2. Step 2 (monotonicity): PROCEED -- `|F_2| < |F_1|` (binary
   non-shrink predicate FALSE).
3. Step 3 (hard-cap): PROCEED -- counter 2/3.
4. Step 4 (proceed): re-spawn cycle 3.

Cycle 3 starts in all three trajectories with `counter=3/3` (at the
boundary, but not halting -- the existing rf-team-lead.md:417 3-cycle
hard cap continues to govern, byte-identical per D-0060 / D-0067).

## 5. False-halt-rate baseline (K-005 audit input)

```
false_halt_rate = false_halts / legitimate_slow_shrink_trajectories
                = 0 / 3
                = 0.000
```

**Baseline statement for M7 K-005 audit:** the M5 retry monotonicity +
regression halt wrapper, as landed by MIG-005, exhibits a 0.000
false-halt-rate across the three canonical slow-shrink trajectories
defined in R-099 (`|F|=5,4`, `|F|=5,3`, `|F|=5,2`). The result is
deterministic across runs because the iterator is pure and depends
only on set membership, not on timing or non-determinism.

If a future change introduces a rate-of-shrink threshold (X-003
re-emergence), the sweep MUST regress -- `|F|=5,4` at minimum would
emit a `[HALT-MONOTONICITY]` line. The counterfactual `|F|=5,5`
trajectory in TEST-017 `TestCounterfactualNonShrinkHalts` provides
the load-bearing proof that the guard fires on genuine non-shrink,
confirming the 0.000 baseline is not a tautology of a no-op emitter.

## 6. Cross-references

- **MIG-005 landing commit:** `db6166e feat(task-builder): MIG-005
  land FR-CONV.5 Retry Monotonicity + Regression Halts (M5)`
- **MIG-005 evidence commit:** `edd3ddd docs(task-builder): D-0067
  T05.16 MIG-005 evidence + FF governance entry`
- **Slow-shrink fixture (TEST-017) commit:** `c9e2b12
  test(task-builder): D-0065 T05.14 TEST-017 + TEST-022 slow-shrink
  + cross-cycle dedup fixtures`
- **Canonical D-0060 log:** `.dev/releases/current/task-builder-merge/
  artifacts/D-0060/fixture-slow-shrink-F-5-4.log`
- **SKILL.md §A.9 binary predicate:** `|F_{n+1}| >= |F_n|` (X-003
  REJECTED -- no rate threshold introduced).

## 7. Acceptance Criteria (phase-5-tasklist.md L815-819)

- [x] All slow-shrink fixtures continue without halts
      (`|F|=5,4` / `|F|=5,3` / `|F|=5,2` -- see Section 4).
- [x] False-halt-rate metric documented at
      `TASKLIST_ROOT/artifacts/D-0100/notes.md` for M7 K-005 audit
      input (this file, Section 5).
- [x] Cross-reference to MIG-005 commit recorded (Section 6).
- [ ] Reviewer confirms baseline metric captured (pending review).

## 8. Artefacts (relative to repo root)

- `.dev/releases/current/task-builder-merge/artifacts/D-0100/notes.md`
  (this file)
- `.dev/releases/current/task-builder-merge/artifacts/D-0100/sweep_runner.py`
  -- driver replaying the 4-step iterator across the 3 trajectories
- `.dev/releases/current/task-builder-merge/artifacts/D-0100/sweep-results.log`
  -- captured stdout of `sweep_runner.py`
- `.dev/releases/current/task-builder-merge/artifacts/D-0100/pytest-slow-shrink-F-5-4.log`
  -- captured pytest output for `test_slow_shrink_continues.py`
