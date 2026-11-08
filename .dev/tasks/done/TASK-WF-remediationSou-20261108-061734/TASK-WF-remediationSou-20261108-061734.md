---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-remediationSou-20261108-061734
version: "1"
priority: Medium
created_date: "2026-11-08"
---

# Loosen and re-assert the T-SPD-5 speed limit so it runs in CI (#440)

Source: ./source.md
Goal: `test_speed_large_commands` asserts one measured, much looser wall-clock limit on every run (xdist workers included), with the value chosen from preregistered measurements and a 10x-slower-guard experiment proving the limit is live; CI's `-n auto` job can then fail T-SPD-5.

## Constraints

- `src/superclaude/hooks/scripts/launch-level-guard.sh` and `src/superclaude/hooks/scripts/launch-job-identity.sh` must not change (owner constraint; the diagnosis is that the test, not the guard, is wrong).
- Test and CI-config changes only. If no limit up to 2.5 s both clears the measured noise and fails the 10x wrapper, do not pick a looser value: record the outcome in `artifacts/limit-selection.md` and stop; the serial CI step is proposed to the coordinator in the handoff, not implemented here.
- The documented 1 s figure (design section 8, NFR-L-01) stays as a reported design target in the test output; the docs update is an open item outside this plan.
- Python operations through UV only. Stage `.dev/tasks` (`git add .dev/tasks`); never stage `.claude/` (except `.claude/settings.json`) or `.dev/issues/`. No push, no PR, no merge.
- The numeric limit is not invented: it comes from the measurements recorded under `artifacts/` in this package.

## Phase 1: Idle measurement arms

## Task 1: Measure the serial idle baseline (D1)

Run, on the current HEAD with no other load: `LL_SPEED_RESULTS=<package>/artifacts/d1-serial-idle.md uv run pytest tests/hooks/test_launch_level_guard.py -k test_speed_large_commands -p no:xdist -rP`. The test itself samples each of the 4 cases 100 times (well above the 30-run floor); the report file records per-case median/p95/max, and `-rP` also prints the rows as the fallback source. If the LL_SPEED_RESULTS file is not written or is empty, fall back to parsing the `-rP` row output into the artifact by hand.

Acceptance criteria:
- `artifacts/d1-serial-idle.md` exists and holds, for each of the 4 cases (`heredoc-git-words-64KB`, `backslash-lines-64KB`, `git-status-lines-64KB`, `1MB-big`), the runs count, median and max in seconds (or ms as printed), plus the command used.
- The slowest 64 KB max and the slowest overall max are stated in a one-line summary at the top of the artifact.

## Task 2: Measure the xdist-idle arm (D4)

Run the same test with one xdist worker and no load: `LL_SPEED_RESULTS=<package>/artifacts/d4-xdist1-idle.md uv run pytest tests/hooks/test_launch_level_guard.py -k test_speed_large_commands -n 1`. On current HEAD the rows may print `NOT ASSERTED` verdicts; the timing values are still recorded. This arm isolates the `PYTEST_XDIST_WORKER` plumbing from CPU contention.

Acceptance criteria:
- `artifacts/d4-xdist1-idle.md` exists with per-case runs/median/max and the command used.
- A one-line comparison against Task 1's artifact states whether the xdist medians/maxima are within noise of the serial arm (delta under about 10 percent) or clearly above.

## Phase 2: Loaded measurement arms

## Task 3: Measure the serial loaded arm (D2)

Start 56 CPU busy loops (`for i in $(seq 56); do timeout 900 yes > /dev/null & done`, nproc is 28 so this is 2x oversubscription), then re-run the Task 1 command with `LL_SPEED_RESULTS=<package>/artifacts/d2-serial-loaded.md`. The loops self-terminate after 900 s; verify they are gone afterwards and kill any survivors.

Acceptance criteria:
- `artifacts/d2-serial-loaded.md` exists with per-case runs/median/max and the command used, and notes the load generator.
- A one-line comparison against Task 1 states whether the loaded max rises clearly above the idle max.
- No `yes` loop from this task remains running afterwards (`pgrep -f 'timeout 900 yes'` prints nothing).

## Task 4: Measure the CI-shaped arm (D3)

Run the full suite the way CI does, so T-SPD-5 executes amid real sibling-worker contention: `uv run pytest -n auto --maxfail=1000 --ignore=tests/cli/test_verify_sync_hooks.py -rP` and capture the four T-SPD-5 rows from the reported captured output (under xdist the LL_SPEED_RESULTS file is last-writer-wins, so parse the rows instead). Save them to `artifacts/d3-suite-auto.md` with the full-suite runtime and worker count.

Acceptance criteria:
- `artifacts/d3-suite-auto.md` exists with the four T-SPD-5 rows (median/p95/max per case), the worker count, and the suite wall time.
- The slowest 64 KB max across this arm is stated in a one-line summary.

## Phase 3: Limit selection and 10x proof

## Task 5: Run the 10x wrapper experiment and select the limit

Depends on: Task 1, Task 2, Task 3, Task 4

For each of the 4 cases, build a throwaway bash wrapper (under this package's `artifacts/`, or a pytest tmp_path via a small probe that imports the helpers from `tests/hooks/test_launch_level_guard.py`: `_spd_env`, `_bind`, `_bash`, `LARGE_COMMANDS`, `HOOK`, `BASH`, `_spd_once` with its timeout raised above the 10 s default) that reads the case's stdin payload into a file once and then runs `launch-level-guard.sh` ten times in a row on it. Time each wrapper with `_spd_once` and record the seconds per case.

Then apply the selection rule from `./source.md` and write `artifacts/limit-selection.md`: the smallest value that is at least 2x the worst 64 KB max across D1/D2/D3, is exceeded by every 64 KB case's wrapper time (the `1MB-big` case is exempt from condition (b): it exits at the guard's size check and its wrapper time only bounds the limit informationally), and is at most 2.5 s (half the 5 s hook timeout). Record every 1MB-big wrapper time in the artifact anyway. Include every measured number, the margin arithmetic, and the diminishing-returns reasoning (why one more doubling was not taken: the margin is already at least 2x or the 2.5 s cap is reached). If no value satisfies all three conditions, record `outcome: no-viable-limit` with the numbers that block it and stop this plan here (the Constraints section governs the fallback).

Acceptance criteria:
- `artifacts/limit-selection.md` exists and names either a concrete `LARGE_LIMIT_S` value (one decimal, at most 2.5) or `outcome: no-viable-limit`.
- The artifact lists the per-case wrapper times, the worst 64 KB max per condition (D1, D2, D3, D4 informational), the 2x-margin arithmetic, and the stop-loosening rationale.
- The chosen value is at least 2x the worst 64 KB max, is below every wrapper time, and does not exceed 2.5 s (or the no-viable-limit outcome is recorded with the blocking numbers).

## Phase 4: Test implementation

## Task 6: Apply the measured limit to `tests/hooks/test_launch_level_guard.py`

Depends on: Task 5

Using the value from `artifacts/limit-selection.md` (skip this task if it recorded `no-viable-limit`): add `LARGE_LIMIT_S` beside `LARGE_RUNS` with a comment stating the chosen value, the three measured conditions with their worst maxima, the 2x-margin rule, the 2.5 s cap rationale (half the 5 s hook timeout, design section 8), and that the 1 s design target is now reported, not asserted; in `test_speed_large_commands` delete the `shared_cpus` shortcut comment and variable, make the verdict `"PASS" if worst < LARGE_LIMIT_S else "FAIL"`, make the assert unconditional with the case name and limit in the message, add the `over 1 s design target` note when `worst >= 1.0`, and reword the target string to state the new limit with the reported design target; update the 1 s wording at the module header, `_spd_markdown` and the test comment (the unverified `1.07 to 1.34 s` figure at the current comment must not survive; carry only numbers from the artifacts); add the 10x check as a new test named `test_speed_large_limit_catches_10x_slower_guard` in the same file that builds the tmp_path wrapper (stdin to file once, guard ten times), times it with `_spd_once` with the timeout raised, and asserts it exceeds `LARGE_LIMIT_S`.

Acceptance criteria:
- `uv run pytest tests/hooks/test_launch_level_guard.py -k "speed_large" -n auto -rP` passes: the 4 T-SPD-5 cases with the assert active (no `NOT ASSERTED` row) and the new 10x check failing the limit.
- `PYTEST_XDIST_WORKER=gw0 uv run pytest tests/hooks/test_launch_level_guard.py -k "speed_large" -p no:xdist` passes with the assert active (the environment variable no longer gates anything).
- `grep -n "PYTEST_XDIST_WORKER\|NOT ASSERTED\|shared_cpus" tests/hooks/test_launch_level_guard.py` prints nothing.
- `git diff --exit-code src/superclaude/hooks/scripts/` passes (the guard scripts are untouched).
- The test comment carries the chosen limit, the measured numbers and the selection reasoning, matching `artifacts/limit-selection.md`.
