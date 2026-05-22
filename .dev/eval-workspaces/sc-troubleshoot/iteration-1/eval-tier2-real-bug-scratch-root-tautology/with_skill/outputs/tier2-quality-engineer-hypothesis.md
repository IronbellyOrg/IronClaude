# Hypothesis: same root cause; mechanism preference is Fix-1 PLUS a regression test that pins the policy at the `eval_run` boundary

**Agent**: quality-engineer
**Tier**: 2
**Timestamp**: 2026-05-21T05:03:00Z
**Cause class**: Security gate bypass via parameter aliasing — masked by missing regression test

## Claim

Agreed on the root cause. The deeper quality issue is that the existing test suite (per `scratch-roots.md:108-110`) pins the doctor + policy text + helper allowlist, but does NOT pin the `eval_run` CLI boundary. The fix must include a regression test at the `eval_run` boundary; otherwise the next refactor of `eval_run` can silently reintroduce the same bug. Mechanism: Fix-1 (drop kwarg) + a CliRunner regression test.

## Evidence

- Snapshot `scratch-roots.md:108-110` —
  > `tests/cli/eval/test_scratch_root_policy.py` reads all three locations and refuses to pass if they disagree, so a drift-introducing PR fails fast in CI.
  Confirms tests pin the policy *text* and the *helper*, not the *eval_run call site*.
- Snapshot `commands.py:1473-1477` — the tautology.
- Snapshot `commands.py:815-823` — the doctor's correct gate; pinned by `--output-dir` doctor tests but not mirrored at `eval_run`.

## Proposed Fix

1. (Same as Fix-1) Drop `output_dir=output_dir` from the `eval_run` call at snapshot `commands.py:1473-1477`.
2. Add `tests/cli/eval/test_eval_run_scratch_root.py` (or extend an existing eval_run test) — at minimum:
   - `test_eval_run_rejects_forbidden_scratch_root`: `CliRunner().invoke(eval_group, ["run", "--suite", ..., "--output-dir", "/etc/foo"])` returns exit code 2 and writes `AC12` / `OPS-002` to stderr.
   - `test_eval_run_accepts_default_output_dir`: with no `--output-dir`, exit succeeds and uses `.dev/eval-runs/<run-id>`.
   - `test_eval_run_accepts_tmp_eval_runs_root`: with `--output-dir /tmp/eval-runs/...`, exit succeeds.
3. Optional follow-up (not blocking): add a generic test that walks every `@click.option('--output-dir', ...)` in `commands.py` and verifies the corresponding command rejects `/etc/foo` — so future eval-CLI commands can't slip past the gate.

## Confidence

Self-reported: 0.93

Per-dimension:

- Evidence grounding: 1.0
- Symptom coverage: 1.0
- Reproducibility fit: 1.0
- Fix directness: 1.0
- Domain coherence: 0.5 (security)

## Risks

- The test (#3) is a soft generic gate and may flake if a future `--output-dir` option is genuinely meant to be unrestricted. Mitigate with an allowlist exception list in the test.
- Otherwise risk is the same as Fix-1: none meaningful.

## If I'm wrong, it's probably because

The fix needs to be more defensive (Fix-2 territory) — but Fix-2's helper-level guard fights `containment_guard`'s legitimate use of the kwarg.

## Alternatives considered

- Skip the test, just fix the call site — rejected: leaves the gap that masked the bug.
- Add the helper-level guard from Fix-2 — rejected for `containment_guard` compatibility reasons.

## Grounding gaps

- None — the test plan is self-contained and the policy boundary is well-defined.
