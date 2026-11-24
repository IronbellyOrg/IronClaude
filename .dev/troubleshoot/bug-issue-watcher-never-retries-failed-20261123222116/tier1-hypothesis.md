# Hypothesis: run_sweep calls first_run only on the sweep that generates a config, so a config left `enabled: false` after a failed first run is skipped as `not_enabled` forever

**Agent**: root-cause-analyst (inline orchestrator formation; Wave 1.7 analyst not spawned, see Grounding gaps)
**Tier**: 1
**Timestamp**: 2026-11-23T22:21:16Z
**Cause class**: Control-flow gap / missing retry path
**Claim class**: `static_defect`
**Evidence class**: `source_static`
**Verdict direction**: `AFFIRM`
**Consistency with docs**: conflicts
runs-in=run_sweep in one cron-started `superclaude issue-watch run-all` process (local, same env)

## Claim

In `run_sweep` the only call to `first_run` sits inside the branch `if not config_path.exists()` and only when `ensure_config` returned `generated`. On every later sweep the config exists, so `_enabled(config_path)` is read; a config whose first run failed (for example `worktree_invalid`, because the Coordinator worktree did not exist yet) still says `enabled: false`, so the repo is skipped with `not_enabled` and `first_run` is never called again. Nothing else in the package calls `first_run`, so the label, state directory, lock and `enabled: true` stay manual. The code cannot tell this unfinished case from a deliberately disabled project, which is why a naive "call first_run for every disabled config" is not a safe fix.

## Evidence

- `src/superclaude/cli/issue_watch/dispatch.py:415` `if not config_path.exists():` and `:425-427` `if outcome.status == "generated": generated.append(repo.name); first_run(config_path, defaults, runner, deps_factory)` (the only call site; grep of the package finds no other `first_run(` caller).
- `src/superclaude/cli/issue_watch/dispatch.py:428-436` `enabled = _enabled(config_path)` / `if enabled is not True: skipped.append(Skipped(repo.name, "not_enabled" ...)); continue`.
- `src/superclaude/cli/issue_watch/generate.py:252` `"enabled": False,` and `:256` `"worktree": str(base.worktrees_dir / name / "Coordinator"),` (the worktree may not exist at generation time).
- `src/superclaude/cli/issue_watch/cycle.py:398-401` `validate_setup` raises `ConfigError("worktree_invalid", ...)` when the worktree is not a directory.
- `src/superclaude/cli/issue_watch/first_run.py:176-183` the `config` step turns that into a failed step and `done(step)` leaves `enabled` false; `:138` and `:170` write `first-run.txt` ("first-run: failed config: worktree_invalid") into the config's `state_dir`.
- `src/superclaude/cli/issue_watch/first_run.py:136-137` an already-enabled config returns `already_enabled` (retry is safe for enabled repos) and `:208-216` an existing store is kept (`state_exists`), so a retry does not reset history.
- `tests/issue_watch/test_first_run.py:179-180` pins the failed-report text; `tests/issue_watch/test_dispatch.py:421-426` pins `not_enabled` for a disabled config with no report file.

## Proposed Fix

In `run_sweep`, when the config exists, `enabled is False`, not a dry run, and the config's own `first-run.txt` report in its `state_dir` starts with `first-run: failed`, call `first_run(config_path, defaults, runner, deps_factory)` once, then re-read `_enabled`. A disabled config with no failed report (owner-written, or hand-disabled after a passed run) stays `not_enabled`. A dry run never calls it.

- `src/superclaude/cli/issue_watch/dispatch.py` — add the retry branch before the `enabled is not True` skip (around line 428), plus a small read-only helper that reads the first line of the report.
- `tests/issue_watch/test_dispatch.py` — add: failed first run then valid worktree then next sweep enables and starts the child; repeated failure stays `not_enabled`; no report means no retry; dry run makes no call.

## Confidence

Self-reported confidence: 0.9

- Evidence grounding: 1.0 — every step cited from the live source lines above
- Runtime check: 1.0 — inherits Evidence grounding (static_defect)
- Symptom coverage: 1.0 — explains the issue's label, state, lock and enabled flag all staying manual
- Reproducibility fit: 0.5 — no live run or new test executed
- Fix directness: 0.5 — the retry-eligibility marker (failed report) is a design choice the owner may prefer to make explicit
- Domain coherence: 1.0 — single module (dispatch.py)

## Risks

Retrying every sweep after a non-worktree failure (`label_failed`, `dry_run`) makes GitHub label and field calls and dry-run cycles each sweep; a back-off or a restriction to `config` step failures may be wanted. A report written by an old run of a config the owner then disabled on purpose would be retried; the owner can delete the report or the config.

## If I'm wrong it's probably because...

An unseen code path outside `issue_watch/` (the runner, cron wrapper or Coder template) calls `first_run` or enables configs another way.

## Falsification standard

`rg -n "first_run\(" src/ tests/` showing a second production call site, or a test that creates a failed first run, makes the worktree valid, runs a second `run_sweep` and observes the child start without manual commands (the new test is the fix's check; today it would fail with `not_enabled`).

## Evidence classification

- **Claim class**: `static_defect` — control flow readable from source
- **Evidence class**: `source_static` — Read of dispatch.py, first_run.py, generate.py, cycle.py
- **Runtime check performed?**: no — no live Orca/GitHub in this worktree; static diagnosis only
- **If REFUTE verdict, coverage statement**: not a REFUTE

## Alternatives considered

- Make `ensure_config` return `exists` and call `first_run` for every non-enabled existing config: rejected, it would re-enable repos the owner switched off.
- Generate configs with `enabled: true`: rejected, R18 (requirements.md:44) wants the check to gate enabling.

## Grounding gaps

No tests run; Wave 1.5 branch fan-out and Wave 1.6 audit not run as parallel agents (done inline); codegraph reported 107407 pending references so caller edges were not used (grep and Read used). Diagnosability verdict: unknown.
