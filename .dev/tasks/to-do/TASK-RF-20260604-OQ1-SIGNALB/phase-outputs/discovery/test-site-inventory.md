# Test Site Inventory (Step 2.2)

**Date:** 2026-06-04
**Test file (worktree):** `/config/workspace/IronClaude/.dev/worktrees/fix-sprint-integrity-signalb-pass-recovered/tests/sprint/test_resume.py`
**Research basis:** `research/02-test-surface.md`, `research/04-gate-resolutions.md`

## Exact worktree line ranges

| Element | Lines |
|---|---|
| `PASS_TRANSCRIPT` constant | 33–37 |
| `TestResumePlanner.test_resume_pass_recovered_counts_as_completed` | 142–257 |
| — `T03.01` transcript write (`PASS_TRANSCRIPT`) | 189 |
| — deferred `validated_last` comment block | 210–214 |
| — `assert report is not None` (current weak assertion) | 215 |
| `_build_gate_fixture` | 686–725 |
| `class TestInvariants` | 728 |
| `TestInvariants.test_gate_hard_stops_on_last_completed_overclaim` | 729–751 |

## Current fixture snippets (verified in worktree)

`PASS_TRANSCRIPT` (lines 33–37):

```python
PASS_TRANSCRIPT = (
    '{"type":"assistant","message":{"usage":{"output_tokens":42}}}\n'
    '{"type":"result","subtype":"success","is_error":false}\n'
)
```

`T03.01` transcript write in the recovered planner test (line 189):

```python
        (results / "phase-3-task-T03.01-output.txt").write_text(PASS_TRANSCRIPT)
```

Current deferred note + weak assertion (lines 210–215):

```python
        # report.validated_last is the COMPOSITE (signal_a AND signal_b AND
        # artifacts). signal_b re-derives via _classify_transcript, which scores
        # PASS_TRANSCRIPT as PASS even though a genuine recovered seam would fail
        # it — so validated_last here is OQ-1/Opt-2-dependent — NOT a guard.
        # (Intentionally not asserted: see F1 GUARD in TASK-RF-20260604-035221.)
        assert report is not None
```

`_build_gate_fixture` persists `T03.01` as ordinary `pass` (line 711) and writes `PASS_TRANSCRIPT` (line 719); `lc_deliverable_exists` controls whether `lc_deliverable.txt` is written (lines 693–695).

## Required `RECOVERED_TRANSCRIPT` content

A transcript `_classify_transcript` derives as `FAIL_RECOVERABLE` (errored terminal result + transient `api_retry` token), per research/02 §3 and research/04 R1:

```python
RECOVERED_TRANSCRIPT = (
    '{"type":"assistant","message":{"usage":{"output_tokens":42}}}\n'
    '{"type":"result","subtype":"error_during_execution","is_error":true}\n'
    'api_retry\n'
)
```

Add this as a module-level sibling constant near `PASS_TRANSCRIPT` (lines 33–37) so both Step 4.1 (positive guard) and Step 4.2 (missing-artifact negative) can reuse it.

## Why retaining `PASS_TRANSCRIPT` would be vacuous

`_classify_transcript(PASS_TRANSCRIPT)` returns `TaskStatus.PASS` (clean result event + output tokens). Under the **pre-Opt-2a** Signal B rule `signal_b_pass = derived is TaskStatus.PASS`, a `PASS_TRANSCRIPT` already makes `signal_b_pass = True`, so `assert report.validated_last is True` would pass **without the source fix** — a vacuous (always-green) assertion that provides no RED→GREEN signal. Switching `T03.01`'s transcript to `RECOVERED_TRANSCRIPT` (derives `FAIL_RECOVERABLE`) makes the pre-fix Signal B `False` → `validated_last False` → genuine RED; the Opt-2a exemption flips it GREEN.

## Insertion plan

### Step 4.1 — convert existing positive test (lines 142–257)
- Add `RECOVERED_TRANSCRIPT` module constant near line 37.
- Line 189: change `write_text(PASS_TRANSCRIPT)` → `write_text(RECOVERED_TRANSCRIPT)` for `T03.01`.
- Lines 210–215: replace the deferred comment block + `assert report is not None` with `assert report.validated_last is True`.
- Persisted status for `T03.01` stays `pass_recovered` (line 178, unchanged); declared deliverable `recovered_deliverable.txt` still written (lines 161–162, unchanged) so `artifacts_ok` is True.

### Step 4.2 — `test_gate_recovered_last_completed_missing_artifact_stops` (new, in `TestInvariants`, near line 751)
- Call `index = _build_gate_fixture(tmp_path, lc_deliverable_exists=False, nu_partial=False)` (deliverable absent). The helper RETURNS the index path; resolve `results = tmp_path / "results"` exactly as the existing gate tests do (e.g. line 763).
- **ORDERING (load-bearing):** the two overwrites below MUST happen BEFORE `ResumePlanner().plan(index)` is called, because the plan reads `phase-3-result.json` and the transcript at plan/run time. Sequence: (1) `_build_gate_fixture`, (2) overwrite result.json, (3) overwrite transcript, (4) `plan = ResumePlanner().plan(index)`, (5) `report = BoundaryIntegrityGate().run(plan)`.
- Overwrite `results/phase-3-result.json` so `T03.01` status is `pass_recovered` (the helper writes ordinary `pass`). The planner's `_coerce_task_status("pass_recovered")` → `TaskStatus("pass_recovered")` → `TaskStatus.PASS_RECOVERED`, so `lc.persisted_status is TaskStatus.PASS_RECOVERED` (the exact exemption-guard predicate). Keep `T03.02` as `incomplete`.
- Overwrite `results/phase-3-task-T03.01-output.txt` with `RECOVERED_TRANSCRIPT`.
- Build the plan, then run `report = BoundaryIntegrityGate().run(plan)`; assert `validated_last is False`, `passed is False`, `blocking_reasons`, `any(s.role == "last_completed" for s in report.suspects)`.
- Proves the PASS_RECOVERED exemption does NOT over-trust persisted status when `artifacts_ok` is False.

### Step 4.3 — `test_gate_last_completed_non_pass_transcript_still_stops` (new, in `TestInvariants`)
- Call `index = _build_gate_fixture(tmp_path, lc_deliverable_exists=True, nu_partial=False)` (ordinary persisted `pass`, deliverable present). Resolve `results = tmp_path / "results"`.
- **ORDERING (load-bearing):** overwrite the transcript BEFORE building the plan. Sequence: (1) `_build_gate_fixture`, (2) overwrite transcript, (3) `plan = ResumePlanner().plan(index)`, (4) `report = BoundaryIntegrityGate().run(plan)`.
- Overwrite `results/phase-3-task-T03.01-output.txt` with `"partial work, killed mid-task\n"` (no `{`-prefixed terminal result event ⇒ `_classify_transcript` returns `INCOMPLETE`). No result.json overwrite is needed — the persisted `pass` is what routes this case through the `else` (non-recovered) branch under Opt-2a, where `INCOMPLETE.is_success` is False.
- Build the plan, then run the gate; assert `validated_last is False`, `passed is False`, `blocking_reasons`, last_completed suspect.
- Proves the exemption is scoped to persisted `PASS_RECOVERED`, not "any non-PASS transcript is fine".

## Constraints / verification

- Both companion tests belong in `tests/sprint/test_resume.py` under `class TestInvariants` (alongside `test_gate_hard_stops_on_last_completed_overclaim`).
- No new test helper or fixture is invented beyond the existing `_build_gate_fixture`, `_task_block`, `_write_index`, `_complete_phase`, `_write_log`, and the new `RECOVERED_TRANSCRIPT` constant.
- The existing ordinary-PASS overclaim test (`test_gate_hard_stops_on_last_completed_overclaim`) is NOT replaced or weakened — it remains as FR-2.4 coverage.
- The autouse `_stub_invoke_sonnet` fixture (lines 40–43) keeps all gate tests no-LLM / CI-safe.
