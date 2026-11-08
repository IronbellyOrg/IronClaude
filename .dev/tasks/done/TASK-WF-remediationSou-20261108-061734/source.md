# Remediation Source: #440 T-SPD-5 looser asserted limit

Derived from REPORT.md at /home/coder/workspaces/worktrees/IronClaude/issue-440/.dev/troubleshoot/test-slow-launch-level-guard-runs-20261108045517/REPORT.md (status partial, tier 2, confidence 0.67, test_is_wrong=true).

## Summary

T-SPD-5 (`test_speed_large_commands` in tests/hooks/test_launch_level_guard.py) never asserts its 1 s limit in CI: the assert is gated on `PYTEST_XDIST_WORKER` being unset (:1269, :1279-1280) and CI always runs `-n auto` (.github/workflows/test.yml:47). The 1 s limit also sits inside shared-CPU timing noise (CI medians 716-849 ms, maxima 1083-1166 ms). The fix is test-only: one measured `LARGE_LIMIT_S` asserted unconditionally on every run, the 1 s design target kept as a reported figure. The owner's rule for the value: "Set up a much looser limit that will bring the risk down as close to zero until the diminishing returns are too much to warrant loosening it any more." The numeric value is chosen by preregistered measurements (D1-D5 in the diagnosability tasklist), run in full before the test is edited.

## Files

- `tests/hooks/test_launch_level_guard.py` — the only file changed in the main path:
  1. Add `LARGE_LIMIT_S` next to `LARGE_RUNS` (:1004), one-line comment: measured per #440, capped at half the 5 s hook timeout (design :219), design target 1 s reported not asserted.
  2. In `test_speed_large_commands` (:1265-1280): delete the shortcut comment and `shared_cpus` (:1266-1269); verdict `"PASS" if worst < LARGE_LIMIT_S else "FAIL"`; assert `worst < LARGE_LIMIT_S` unconditionally with the case name and limit in the message; note "over 1 s design target" when `worst >= 1.0`; target text states the new limit and "(asserted; design target 1 s (reported))".
  3. Update the 1 s wording at :995-996, :1107-1108, :1258 (and :1267's unverified "1.07 to 1.34 s" figure must not survive; carry only verified numbers).
  4. Add the 10x-slower-guard check: a test-local bash wrapper in tmp_path that reads stdin into a file once, then runs `launch-level-guard.sh` 10 times on it, timed with `_spd_once` with the subprocess timeout raised (default 10 s at :1039 is too low for ~9 s of work under load). It must exceed `LARGE_LIMIT_S`. If it does not (per case), record that fact and fall back to the CI route.
- `.github/workflows/test.yml` — fallback only, if no single limit both clears the noise in every condition and fails the 10x wrapper: add a serial step on the :137-142 pattern asserting T-SPD-5 (no `-n`), and `--deselect tests/hooks/test_launch_level_guard.py::test_speed_large_commands` at :47.
- Files that MUST NOT change: `src/superclaude/hooks/scripts/launch-level-guard.sh`, `src/superclaude/hooks/scripts/launch-job-identity.sh` (owner constraint; the diagnosis is that the test, not the guard, is wrong).

## Measurements (preregistered; run all before editing the test)

Each T-SPD-5 case is measured at least 30 times per condition; record the slowest time per case per condition. nproc=28, so the busy load is 56 loops (2 x nproc).

- D1 serial idle: `uv run pytest tests/hooks/test_launch_level_guard.py -k test_speed_large_commands -p no:xdist` with LL_SPEED_RESULTS to a file, >=30 runs/case.
- D2 serial loaded: D1 while 56 busy loops run (`timeout 900 yes > /dev/null &` x 56).
- D3 CI-shaped: the full suite `uv run pytest -n auto --maxfail=1000 --ignore=tests/cli/test_verify_sync_hooks.py` with the T-SPD-5 rows read from its output (single-run rows are 100-run aggregates; this is the CI-shaped condition).
- D4 xdist idle no contention: the D1 command with `-n 1` (variable set, no CPU sharing).
- D5 10x wrapper: per case, time the tmp_path wrapper via `_spd_once`; record the seconds.

Selection rule (owner's guidance): the limit is the smallest value that (a) is >= 2x the worst 64 KB max across D1-D3, (b) is exceeded by every 64 KB case's D5 wrapper time (the `1MB-big` case exits at the guard's size check and is exempt: it does not exercise the timed classification path, so its wrapper time only bounds the limit informationally), and (c) stays <= 2.5 s (half the 5 s hook timeout). Stop loosening at the cap or when the margin is already >= 2x, whichever comes first: a further doubling past that point lowers false-failure risk only negligibly while halving sensitivity. If no value <= 2.5 s satisfies (a) and (b), use the CI fallback route instead of a looser limit.

Amendment 2026-11-08 (pre-execution, from the advisory pre-reflect calibration): condition (b) originally read "every case's"; the `1MB-big` case exits 2 at the guard's size check (test :1263-1264) and can be fast enough that its 10-run wrapper never exceeds a sensible limit, which would dead-end the selection at no-viable-limit on a case the limit does not protect. The 64 KB cases are the ones the limit guards.

## Acceptance

1. `uv run pytest tests/hooks/test_launch_level_guard.py -k test_speed_large_commands -n auto -rP` passes: 4 cases, assert active, no "NOT ASSERTED" row; the 10x check (test name containing `speed_large_limit`, e.g. `test_speed_large_limit_catches_10x_slower_guard`, so `-k "speed_large"` selects it) fails the limit.
2. `PYTEST_XDIST_WORKER=gw0 uv run pytest tests/hooks/test_launch_level_guard.py -k test_speed_large_commands -p no:xdist` still asserts (the env var no longer matters).
3. Grep `PYTEST_XDIST_WORKER|NOT ASSERTED|shared_cpus` in tests/hooks/test_launch_level_guard.py returns no hits.
4. The test-file comment states the chosen limit, the three measured conditions with their worst maxima, the 2x-margin rule, and why one more doubling was rejected.
5. The chosen limit, all measurements and the reasoning are recorded in the handoff.
6. The guard scripts are untouched (`git diff --exit-code src/superclaude/hooks/scripts/`).
7. No `.claude/` path is staged; `.dev/tasks` is staged (`git add .dev/tasks`); nothing is pushed; no PR is opened.

## References

- REPORT.md: .dev/troubleshoot/test-slow-launch-level-guard-runs-20261108045517/REPORT.md
- Diagnosability tasklist (D1-D5): .dev/troubleshoot/test-slow-launch-level-guard-runs-20261108045517/diagnosability-tasklist.md
- Impact report (both symbols test-only, 0 prod dependents): .dev/troubleshoot/test-slow-launch-level-guard-runs-20261108045517/impact/impact.md
- Issue brief: .dev/issues/440/issue-summary.md
- CI log evidence: .dev/troubleshoot/test-slow-launch-level-guard-runs-20261108045517/job-128512582247.log (:44115, :44123, :44225)

## Pipeline Hardening

Applicable: false; verdict not_applicable (HC0 boundary scan in REPORT.md: the defect is a test's assert gating, not a pipeline boundary). No closure blockers; no hardening gates bind this remediation.
