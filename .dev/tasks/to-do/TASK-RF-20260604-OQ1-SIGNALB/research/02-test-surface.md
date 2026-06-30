# OQ-1 Opt-2a Test Surface Research

Status: Complete
Date: 2026-06-04

## 1. Existing recovered-seam test surface

Source read: `origin/master:tests/sprint/test_resume.py` materialized as `/tmp/oq1_test_resume_origin_master.py` for line-numbered reading.

`TestResumePlanner.test_resume_pass_recovered_counts_as_completed` is the right positive Opt-2a surface. It already builds a recovered seam with a declared deliverable present, a `pass_recovered` persisted result, and a `PASS_TRANSCRIPT` for `T03.01` (`/tmp/oq1_test_resume_origin_master.py:142-215`). The fixture shape is:

```python
        deliv = base / "recovered_deliverable.txt"
        deliv.write_text("done\n")
...
            + _task_block("T03.01", deliverable=deliv)
...
                        {"task": {"task_id": "T03.01"}, "status": "pass_recovered"},
...
        (results / "phase-3-task-T03.01-output.txt").write_text(PASS_TRANSCRIPT)
```

The deferred note to un-defer is verbatim (`/tmp/oq1_test_resume_origin_master.py:210-214`):

```python
        # report.validated_last is the COMPOSITE (signal_a AND signal_b AND
        # artifacts). signal_b re-derives via _classify_transcript, which scores
        # PASS_TRANSCRIPT as PASS even though a genuine recovered seam would fail
        # it — so validated_last here is OQ-1/Opt-2-dependent — NOT a guard.
        # (Intentionally not asserted: see F1 GUARD in TASK-RF-20260604-035221.)
```

Recommendation: edit the existing test, but do two things together: (1) replace the synthetic `PASS_TRANSCRIPT` for `T03.01` with a transcript that `_classify_transcript` derives as `FAIL_RECOVERABLE` (the genuine recovered-seam Signal-B mismatch), and (2) replace the deferred note plus `assert report is not None` with `assert report.validated_last is True`. Rationale: this test was explicitly designed as the PR #124 recovered-task guard and already names the Opt-2 dependency; converting its transcript from synthetic PASS to recovered/non-PASS makes the un-deferred assertion a real RED→GREEN guard instead of adding another overlapping positive fixture.

## 2. Negative Opt-2a fixture pattern: recovered seam must still require artifacts

The reusable integrity-gate fixture is `_build_gate_fixture` (`/tmp/oq1_test_resume_origin_master.py:686-725`). It builds a TASK-interrupted release where `T03.01` is the last-completed task and `T03.02` is next-unfinished. The deliverable-present vs deliverable-absent control is exactly this code (`/tmp/oq1_test_resume_origin_master.py:686-701`):

```python
def _build_gate_fixture(
    tmp_path: Path, *, lc_deliverable_exists: bool, nu_partial: bool
) -> Path:
    """TASK-interrupted fixture: T03.01 last-completed (PASS transcript +
    optional deliverable), T03.02 next-unfinished (optional partial transcript)."""
    results = tmp_path / "results"
    results.mkdir()
    lc_deliv = tmp_path / "lc_deliverable.txt"
    if lc_deliverable_exists:
        lc_deliv.write_text("done\n")
...
        "# Phase 3\n"
        + _task_block("T03.01", deliverable=lc_deliv)
        + _task_block("T03.02")
```

The current fixture persists `T03.01` as ordinary `pass` and writes a PASS transcript (`/tmp/oq1_test_resume_origin_master.py:705-720`):

```python
    (results / "phase-3-result.json").write_text(
        json.dumps(
            {
                "phase": 3,
                "status": "incomplete",
                "task_results": [
                    {"task": {"task_id": "T03.01"}, "status": "pass"},
                    {"task": {"task_id": "T03.02"}, "status": "incomplete"},
                ],
            }
        )
    )
...
    (results / "phase-3-task-T03.01-output.txt").write_text(PASS_TRANSCRIPT)
```

The existing hard-stop negative pattern is `TestInvariants.test_gate_hard_stops_on_last_completed_overclaim` (`/tmp/oq1_test_resume_origin_master.py:729-751`): it calls `_build_gate_fixture(tmp_path, lc_deliverable_exists=False, nu_partial=False)`, runs `BoundaryIntegrityGate().run(plan)`, and asserts `report.validated_last is False`, `report.passed is False`, `report.blocking_reasons`, and a last-completed suspect.

For Opt-2a, add a recovered-specific negative companion rather than changing this existing ordinary-PASS overclaim test. The companion should use the same shape but persist `T03.01` as `pass_recovered` and leave `lc_deliverable_exists=False`. This proves the new Signal-B exemption only handles the recovered transcript seam; it does not over-trust the persisted recovered status when `artifacts_ok` is false. Expected assertions:

```python
report = BoundaryIntegrityGate().run(plan)
assert report.validated_last is False
assert report.passed is False
assert report.blocking_reasons
assert any(s.role == "last_completed" for s in report.suspects)
```

## 3. RED→GREEN framing and non-overbroad Signal B assertions

Current master computes Signal B as ordinary PASS only: `_classify_transcript(transcript)` is assigned to `derived`, then `signal_b_pass = derived is TaskStatus.PASS` (`/tmp/oq1_integrity_origin_master.py:127-132`). `validated_last` is the conjunction of Signal A, Signal B, and `artifacts_ok` (`/tmp/oq1_integrity_origin_master.py:144-153`):

```python
        derived = _classify_transcript(transcript)
        lc.derived_status = derived
        signal_b_pass = derived is TaskStatus.PASS
...
        validated = signal_a_pass and signal_b_pass and artifacts_ok
        if not validated:
            lc.suspect = True
            return False, [lc], lc
```

`_classify_transcript` returns `TaskStatus.FAIL_RECOVERABLE` for an errored transcript with a transient signal such as `api_retry`, and `TaskStatus.INCOMPLETE` when no terminal result event exists (`/tmp/oq1_rerun_tasks_origin_master.py:547-593`). Therefore the positive Opt-2a RED fixture should not keep using `PASS_TRANSCRIPT`; it should use a recovered transcript that derives as `FAIL_RECOVERABLE`, for example:

```python
RECOVERED_TRANSCRIPT = (
    '{"type":"assistant","message":{"usage":{"output_tokens":42}}}\n'
    '{"type":"result","subtype":"error_during_execution","is_error":true}\n'
    'api_retry\n'
)
```

RED/GREEN outcomes:

- Positive recovered seam with declared artifact present: persisted status `pass_recovered` means Signal A is true; `RECOVERED_TRANSCRIPT` derives `FAIL_RECOVERABLE`, so current master Signal B is false and `assert report.validated_last is True` is RED. After Opt-2a, Signal B should pass via the recovered-seam exemption and the same assertion is GREEN.
- Recovered seam with missing declared artifact: Signal A true and Opt-2a Signal B exempt/passing, but `artifacts_ok` remains false, so `assert report.validated_last is False` and `assert report.passed is False` are GREEN both before and after the source fix; they guard against over-trusting recovered status.
- Ordinary non-PASS transcript must still fail Signal B: build a normal last-completed fixture with persisted `pass`, artifact present, then overwrite `results/phase-3-task-T03.01-output.txt` with a transcript lacking a terminal result event (for example `"partial work, killed mid-task\n"`). `_classify_transcript` returns `INCOMPLETE` when no result event exists (`/tmp/oq1_rerun_tasks_origin_master.py:576-577`), so `assert report.validated_last is False` should remain GREEN before and after Opt-2a. This proves the exemption is not “any non-PASS transcript is okay.”

## 4. Test conventions and concrete recommended plan

Conventions observed in `tests/sprint/test_resume.py`:

- Use pytest classes: planner tests live under `class TestResumePlanner` (`/tmp/oq1_test_resume_origin_master.py:87`) and gate invariant tests under `class TestInvariants` (`/tmp/oq1_test_resume_origin_master.py:728`).
- Test methods use `tmp_path` fixtures throughout (`/tmp/oq1_test_resume_origin_master.py:142`, `/tmp/oq1_test_resume_origin_master.py:729`).
- `PASS_TRANSCRIPT` is the shared clean-pass transcript constant (`/tmp/oq1_test_resume_origin_master.py:33-37`). For Opt-2a, add a sibling recovered transcript constant or inline local `RECOVERED_TRANSCRIPT` so the positive recovered assertion is actually RED on current master.
- The autouse `_stub_invoke_sonnet` fixture patches advisory LLM reads to `""`, keeping these tests no-LLM/CI-safe (`/tmp/oq1_test_resume_origin_master.py:40-43`).
- Run command: `uv run pytest tests/sprint/ -q`.

Concrete plan:

1. Edit `TestResumePlanner.test_resume_pass_recovered_counts_as_completed`:
   - Change the `T03.01` transcript write from `PASS_TRANSCRIPT` to a recovered transcript that derives `FAIL_RECOVERABLE`.
   - Replace the deferred Opt-2 note and `assert report is not None` with:

   ```python
   assert report.validated_last is True
   ```

   RED now: current master has `signal_b_pass = derived is TaskStatus.PASS`, so recovered-derived `FAIL_RECOVERABLE` makes `validated_last` false. GREEN after Opt-2a: Signal B accepts the recovered seam and artifacts are present.

2. Add a recovered-specific negative test near `TestInvariants.test_gate_hard_stops_on_last_completed_overclaim`, e.g. `test_gate_recovered_last_completed_missing_artifact_stops`:
   - Build the same TASK-interrupted shape as `_build_gate_fixture` but with persisted `status: "pass_recovered"` for `T03.01` and the declared `lc_deliverable.txt` intentionally absent.
   - Write the recovered transcript for `T03.01`.
   - Assert:

   ```python
   assert report.validated_last is False
   assert report.passed is False
   assert report.blocking_reasons
   assert any(s.role == "last_completed" for s in report.suspects)
   ```

   RED/GREEN: this is expected GREEN on both current master and after Opt-2a for `validated_last is False` because missing artifacts stop the seam either way. Its value is regression coverage that the new exemption does not bypass artifacts.

3. Add or keep a narrow ordinary-non-PASS Signal-B test, e.g. `test_gate_last_completed_non_pass_transcript_still_stops`:
   - Use `_build_gate_fixture(tmp_path, lc_deliverable_exists=True, nu_partial=False)` so persisted status is ordinary `pass` and artifact exists.
   - Overwrite `results/phase-3-task-T03.01-output.txt` with `"partial work, killed mid-task\n"`.
   - Assert:

   ```python
   assert report.validated_last is False
   assert report.passed is False
   assert report.blocking_reasons
   assert any(s.role == "last_completed" for s in report.suspects)
   ```

   RED/GREEN: this should be GREEN before and after Opt-2a. It proves the exemption is scoped to persisted `PASS_RECOVERED`, not all non-PASS derived transcripts.

Summary: edit the existing recovered planner/integrity test for the positive RED→GREEN assertion, and add two small gate-level companions for missing artifacts and ordinary non-PASS Signal-B failure. Do not replace the existing ordinary-PASS overclaim test; it is still valuable coverage for the original FR-2.4 invariant.
