# Focused OQ-1 Tests Summary (Step 5.1)

**Date:** 2026-06-04
**Command:**
```
uv run pytest \
  tests/sprint/test_resume.py::TestResumePlanner::test_resume_pass_recovered_counts_as_completed \
  tests/sprint/test_resume.py::TestInvariants::test_gate_recovered_last_completed_missing_artifact_stops \
  tests/sprint/test_resume.py::TestInvariants::test_gate_last_completed_non_pass_transcript_still_stops \
  -q
```
**Raw output:** `phase-outputs/test-results/focused-oq1-tests-output.txt`

| Check | Result |
|---|---|
| Command uses UV / no `python -m` | YES — compliant |
| Tests collected | 3 |
| Passed | 3 |
| Failed | 0 |
| Exit code | 0 |

## Coverage

1. `test_resume_pass_recovered_counts_as_completed` — positive guard (recovered seam + present artifact ⇒ `validated_last True`). Genuine RED→GREEN (Step 4.4).
2. `test_gate_recovered_last_completed_missing_artifact_stops` — negative: PASS_RECOVERED seam with missing declared artifact still STOPs (`validated_last False`).
3. `test_gate_last_completed_non_pass_transcript_still_stops` — scoping guard: ordinary persisted `pass` with INCOMPLETE transcript still STOPs (exemption not over-broad).

**Verdict:** All three targeted tests pass together with the Opt-2a fix restored. No failures to fix. Ready for the full sprint suite.
