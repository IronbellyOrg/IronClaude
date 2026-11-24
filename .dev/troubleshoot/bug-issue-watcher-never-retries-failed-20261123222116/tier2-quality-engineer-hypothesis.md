# Hypothesis: a failed first run leaves `enabled: false` and `run_sweep` never retries it, so the retry needs a failed-report marker, and the marker must also look beside the config

**Agent**: quality-engineer (lens: tests and edge cases)
**Tier**: 2
**Timestamp**: 2026-11-23T22:40:00Z
**Cause class**: Control-flow gap / missing retry path (agrees with Tier 1)
**Claim class**: `static_defect`
**Evidence class**: `source_static`
**Verdict direction**: `AFFIRM`
**Consistency with docs**: conflicts (the `not_applicable` text in dispatch.py says "the first run did not pass, or the owner set it", but nothing retries the first case)
runs-in=run_sweep in one cron-started `superclaude issue-watch run-all` process (local, same env)

(Persisted by the orchestrator from the troubleshoot-analyst's returned card. NOTE: the Timestamp above was written by the analyst, not copied from a command; it is later than this run's clock (22:24Z) and is treated as invalid per C5/A3.)

## Claim

I agree with Tier 1. `run_sweep` calls `first_run` only inside `if not config_path.exists()` and only when `ensure_config` returned `generated`. After a failed first run the config is read as `enabled: false` and skipped as `not_enabled` on every later sweep. Producer P1 (`dispatch.py:429`, surviving=yes) is the skip that hides the failure. I extend Tier 1 in one way. The marker "first line of `<state_dir>/first-run.txt` starts with `first-run: failed`" misses some real failed first runs, because the report can land in two places or in none. The fix has to read both places. Some failures leave no report, and I list those as accepted limits.

## Evidence

- `src/superclaude/cli/issue_watch/dispatch.py:425-429` — `if outcome.status == "generated": ... first_run(config_path, defaults, runner, deps_factory)` then `enabled = _enabled(config_path)` / `if enabled is not True:`. Config creation and the first run happen together, once.
- `src/superclaude/cli/issue_watch/first_run.py:78-83` — `_report_dir` returns the state dir only when `os.path.isabs(state)`, otherwise `config_path.parent`.
- `first_run.py:141-145` — `report_name = REPORT_FILE if directory != config_path.parent else f"{config_path.stem}-{REPORT_FILE}"`. A config with no usable absolute `state_dir` reports to `<config dir>/<stem>-first-run.txt`.
- `first_run.py:180-185` — when `cycle.load_config` or `validate_setup` fails, the report goes to the raw `state_dir`. When they pass, `directory = config.state_dir` and `report_name = REPORT_FILE`. The `worktree_invalid` case is therefore at `<raw state_dir>/first-run.txt`.
- `first_run.py:86-95` — `_write_report` returns `None` on `OSError` and does not raise. A failed run can then leave no report at all.
- `first_run.py:136-137` — a config with `enabled is True` returns `already_enabled`, so the retry is safe for enabled repos. `first_run.py:211-212` keeps an existing store (`state_exists`).

### (1) Which existing tests break

- No existing test breaks (read by the analyst plus grep).
  - `tests/issue_watch/test_dispatch.py:141-152` `sweep()` passes `deps_factory=lambda cfg: pytest.fail("no first run expected")`; a trap that fires only if the new branch runs.
  - `test_dispatch.py:421-426` `test_a_config_that_is_not_enabled_is_skipped_with_a_reason` makes `world.config("Beta", enabled=False)`; `world` (lines 48-75) never writes `first-run.txt`, so the test still gets `not_enabled`; it becomes the "no report means no retry" case.
  - `test_dispatch.py:349-373` and `:376-401` monkeypatch `dispatch.first_run` and `ensure_config` and go through the `generated` branch, so they are unaffected.
  - `tests/issue_watch/test_first_run.py` calls `first_run` directly; unaffected, and its report-text pins stay the marker's contract.
  - `tests/issue_watch/test_security_invariants.py` has no match for `run_sweep`, `first_run` or `not_enabled`; the retry calls `first_run` (which calls `repo_init`), not the cycle, so NG-2 is not touched.
  - Unverified: `tests/sweep/test_probes_allowlist.py` (name collision only, not read).
- Changes needed: additions to `test_dispatch.py` only; `World` needs a helper to write `first-run.txt` into `state_dir(name)` with a chosen first line; retry tests override `deps_factory` and monkeypatch `dispatch.first_run` as at lines 364-369.

### (2) Edge cases the new tests must cover

1. Failed first run, then valid worktree, then next sweep: retry enables, child starts.
2. Repeated failure: sweep reports `not_enabled`, fake called exactly once in that sweep (no loop).
3. No report file: no call, `not_enabled` (existing test at :421).
4. Report first line `first-run: passed` with `enabled: false` (owner disabled afterwards): no call.
5. Dry run: no call and no file written; the marker read writes nothing.
6. Retry that fails again: report rewritten by `first_run`, store untouched (`state_exists`, first_run.py:211).
7. NG-2: `dispatch.py` adds no write verb of its own.
8. Relative or unreadable `state_dir`: report is `<stem>-first-run.txt` beside the config (`first_run.py:141-145`; `test_first_run.py:347-356` pins `Broken-first-run.txt`); the retry must find it there too.
9. Failed report in `<raw state_dir>` while `config.state_dir` differs in loaded form: read the same raw path `_report_dir` uses.
10. Non-regular or symlinked report: read without following symlinks; read error = no marker.
11. Non-UTF-8 or huge first line: read only a bounded first line; any error = no retry.

### (3) Ways the proposed marker misses a real failed first run

- A report beside the config (relative, missing or non-string `state_dir`, unreadable config): marker must check both locations.
- No report written: `_write_report` swallows `OSError` (`first_run.py:93-94`).
- A crash before the report: a sweep that dies between `ensure_config` and `first_run` (`dispatch.py:421-427`), or `first_run` raising, leaves no report and a stuck disabled config.
- `enable_failed` writes `first-run: failed config: enable_failed` (`first_run.py:154-161`), covered, but a permanent write failure would retry every sweep.
- Stale reports: a `failed` report left by an old run on a config the owner then disabled on purpose would be retried; a later passed report replaces the failed one.

## Proposed Fix

Keep Tier 1's fix, with one change to how the marker is read. In `run_sweep`, before the `enabled is not True` skip (`dispatch.py:428-429`), when the config exists, `enabled is False` and `dry_run` is false:

1. Read the first line of `<raw state_dir>/first-run.txt` if `state_dir` is an absolute string, else of `<config dir>/<stem>-first-run.txt`.
2. Read with `O_NOFOLLOW`, a bounded size and a catch-all for `OSError` and `ValueError`.
3. If the line starts with `first-run: failed`, call `first_run(config_path, defaults, runner, deps_factory)` once and re-read `_enabled`.

Files: `src/superclaude/cli/issue_watch/dispatch.py` (branch plus helper `_first_run_failed(config_path)`); `tests/issue_watch/test_dispatch.py` (cases above plus a `World.report(name, first_line, *, beside_config=False)` helper). Existing tests keep passing.

## Confidence

Self-reported confidence: 0.85

- Evidence grounding: 1.0 — every cited line was read in this session.
- Runtime check: 1.0 — inherits Evidence grounding (`static_defect`).
- Symptom coverage: 0.5 — covers failures that leave a report; crashes and unwritable report directories remain uncovered.
- Reproducibility fit: 0.5 — no test was run.
- Fix directness: 0.5 — the marker choice is a design decision for the owner; a separate explicit "needs first run" marker would cover report-less failures.
- Domain coherence: 1.0 — one module plus its test file.

## Risks

- The retry runs every sweep for a repo that keeps failing; `label_failed` or `dry_run` failures cost label and dry-run work each sweep, so a back-off may be wanted. A `config` step failure costs only local checks.
- A stale `failed` report on a deliberately disabled config would be retried; the owner deletes the report or the config to stop it.
- The first-line read must not follow a symlink or raise; a raise would break the whole sweep.

## If I'm wrong, it's probably because...

An explicit marker written by `ensure_config` (a "needs first run" state, not the report) is the better design; it would also cover the crash and unwritable-report cases.

## Falsification standard

A new test in `tests/issue_watch/test_dispatch.py` that writes a failed report in `state_dir(name)`, makes the worktree valid, runs two sweeps and fails on current code with `not_enabled` and no child start. A second production call site found by `rg -n "first_run\(" src/` would also refute the claim.

## Evidence classification

- **Claim class**: `static_defect`
- **Evidence class**: `source_static` — Read of `dispatch.py` (380-459), `first_run.py` (30-239) and the test files named above.
- **Runtime check performed?**: no — the worker cannot execute anything.
- **If REFUTE verdict, coverage statement**: not a REFUTE.

## Alternatives considered

- An explicit "needs first run" marker file or config key written by `ensure_config`: more robust against crashes and unwritable report directories, but changes the config schema or adds a file. Offered as the owner's alternative.
- Retry every disabled config: rejected, it would re-enable repos the owner switched off.

## Grounding gaps

- Not read: `tests/sweep/test_probes_allowlist.py`; the full `test_first_run.py` and `test_security_invariants.py` (grep only).
- Producer row P1 cited as given by the parent.
- Codegraph not used, per the brief. No tests run. Diagnosability verdict: unknown.
