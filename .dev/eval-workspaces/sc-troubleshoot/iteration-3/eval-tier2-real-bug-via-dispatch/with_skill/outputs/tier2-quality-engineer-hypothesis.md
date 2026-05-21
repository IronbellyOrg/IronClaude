# Tier 2 Hypothesis Card — quality-engineer

**Brief received**: Original issue + Tier 1 card. Asked to look for edge cases, test gaps, and surprising failure modes.

**Claim**: I agree on the root cause. The deeper quality issue is **a missing parity-test between doctor and eval_run** — the OPS-002 cross-module consistency requirement is documented (`scratch-roots.md:82-88`) but not enforced by a test. The bug shipped because:

1. There IS a test in `tests/cli/eval/test_scratch_root_policy.py` that catches *drift between SCRATCH_ROOT_POLICY (the text constant) and the doc table and `_default_allowed_scratch_roots()`*.
2. There IS NO test that exercises BOTH doctor and eval_run with the same non-allowlisted `--output-dir` and asserts both reject with the same exit code.

The check that should have failed in CI didn't exist. So the silent-pass bug was *un-detectable* by the existing test suite even though every individual piece was tested.

**Evidence**:

- `scratch-roots.md:82-88` — declares the cross-module guarantee:
  > "New CLI surfaces MUST funnel through that helper instead of reimplementing the message; this is the OPS-002 cross-module consistency guarantee."
  The guarantee is policy; the test enforcing it is absent.
- `scratch-roots.md:108-110` — names `tests/cli/eval/test_scratch_root_policy.py` as the drift detector, but that test detects *text drift*, not *behavioral drift between command surfaces*.
- `commands.py:815-823` vs. `commands.py:1472-1477` — visual proof the two surfaces behave differently with the same input.

**Proposed fix (quality-engineer choice)**:

- **Primary**: same as security-engineer's FIX-A (one-line removal at commands.py:1476). Necessary to fix the live security hole.
- **Required follow-up**: add a parameterized parity test `test_doctor_and_run_reject_same_paths[/etc/foo, /var/lib/foo, ~/, /]` that asserts both surfaces produce `SCRATCH_ROOT_VIOLATION_EXIT_CODE` (2) and emit the same `SCRATCH_ROOT_POLICY` text on stderr. Without this test, the bug class can recur on any future CLI surface (`eval gather`, hypothetical `eval validate`, etc.).

**Confidence (agent self-report)**: 0.91

**If I'm wrong it's probably because...**: the parity test already exists in a sibling file I haven't grepped. Even if it does, the absence of an *executed* assertion on this exact code path is evidenced by the bug shipping — so the test gap is real either way.

**Risks of fix**: None new beyond FIX-A. The parity test addition is pure additive coverage.

**Test plan** (detailed):

```python
@pytest.mark.parametrize("bad_path", ["/etc/foo", "/var/lib/test", "/", "~/"])
def test_doctor_and_run_reject_same_paths(bad_path, tmp_path, runner):
    """OPS-002 cross-module consistency: doctor and run reject identically."""
    doc = runner.invoke(cli, ["eval", "doctor", "--output-dir", bad_path])
    run = runner.invoke(cli, ["eval", "run", "default-suite", "--output-dir", bad_path])
    assert doc.exit_code == SCRATCH_ROOT_VIOLATION_EXIT_CODE
    assert run.exit_code == SCRATCH_ROOT_VIOLATION_EXIT_CODE
    assert "OPS-002" in doc.stderr or "AC12" in doc.stderr
    assert "OPS-002" in run.stderr or "AC12" in run.stderr
```
