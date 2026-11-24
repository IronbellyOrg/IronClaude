# Hypothesis: `run_sweep` calls `first_run` only on the sweep that generates a config, so a config left `enabled: false` by a failed first run is skipped as `not_enabled` on every later sweep. The retry marker should be the config's own `first-run.txt` report, read by a helper placed next to `first_run`.

**Agent**: root-cause-analyst (lens: root-cause-analyst)
**Tier**: 2
**Timestamp**: 2026-11-23T22:24:52Z
**Cause class**: Control-flow gap / missing retry path
**Claim class**: `static_defect`
**Evidence class**: `source_static`
**Verdict direction**: `AFFIRM`
**Consistency with docs**: aligned
runs-in=dispatch.py run_sweep (SAME-ENV yes: a cron-started `issue-watch run-all` process)

(Persisted by the orchestrator from the troubleshoot-analyst's returned card; the analyst gave no clock time, the parent supplied 22:24:52Z, the time of receipt. The analyst's "aligned" differs from Tier 1's "conflicts"; both are recorded, see REPORT.)

## Claim

`first_run` is called from exactly one place, `dispatch.py:427`, inside `if not config_path.exists():` and only when `ensure_config` returned `generated`. On every later sweep the config exists, so `_enabled` returns `False` and the repo is skipped with `not_enabled` (P1, `dispatch.py:428-435`). Nothing else retries; no CLI command calls `first_run`. The code cannot tell an unfinished generated config from a deliberately disabled one. The failure report `first_run` already writes is the cheapest existing signal that tells them apart.

## Evidence

- `src/superclaude/cli/issue_watch/dispatch.py:425-427`: `if outcome.status == "generated": generated.append(repo.name)` then `first_run(config_path, defaults, runner, deps_factory)`; only call site (grep of `src/` finds `dispatch.py:45`, `dispatch.py:427` and the definition at `first_run.py:125`).
- `dispatch.py:428-435` (P1): `enabled = _enabled(config_path)`, `if enabled is not True:`, `"not_enabled" if enabled is False else "config_unreadable"`, `continue`. `_enabled` at `dispatch.py:210-215` returns `raw.get("enabled")`.
- `first_run.py:78-85, 138-145`: `_report_dir` returns the config's absolute `state_dir`, else `config_path.parent`; `report_name` is `first-run.txt` or `<stem>-first-run.txt`. Config-step failure at `:180-183` calls `done(step)`, which writes `first-run: failed config: <reason>` (`:158-170`) into the raw `state_dir` (`directory` is replaced by `config.state_dir` only at `:185`).
- `generate.py:249,258`: generated configs always carry an absolute `state_dir`.
- `cycle.py:59-71`: `_TOP_KEYS` is a closed key set including `"enabled"` and `"state_dir"`; a new config field would need a schema change.
- `cycle.py:396-402` `validate_setup`: `if not os.path.isdir(config.worktree): raise ConfigError("worktree_invalid", ...)`; the config step is local only (no GitHub call).
- `tests/issue_watch/test_dispatch.py:421-426` pins `not_enabled`; `tests/issue_watch/test_first_run.py:180` pins the failed-config report text; `:354-356` pins `Broken-first-run.txt`.

## Proposed Fix

Add a read-only helper in `first_run.py`, e.g. `failed_step(config_path) -> str | None`, that reads the raw config, applies the same `_report_dir` and `report_name` rule, and returns the step name when the first report line starts with `first-run: failed `, else `None`. In `run_sweep`, before the `enabled is not True` skip: if not `dry_run`, `_enabled(config_path) is False` and the helper returns a step, call `first_run(...)` once and re-read `_enabled`. Retry on every sweep when the step is `config`; retry other steps only when the report's mtime is older than a back-off (suggested 1 hour, using the injected `now`).

- `first_run.py`: the helper (reusing `_raw_config`, `_report_dir`, `REPORT_FILE`).
- `dispatch.py`: the retry branch (about `:428`); update the docstring at `:7-8` and the `not_enabled` text at `:66`.
- Tests (`test_dispatch.py`, `test_first_run.py`): failed `worktree_invalid` then valid worktree then next sweep enables and starts the child; repeated failure stays `not_enabled`; no report or a `passed` report means no retry; dry run makes no call; a non-config failure inside the back-off makes no call and outside it retries once.

Smaller alternative: retry only `config` failures with no back-off (covers the reported symptom, entirely local and cheap, but leaves `label_failed` and `dry_run` failures manual).

## Marker comparison

| Marker | Config-step failure | Later passing run | Owner disables after pass | Unwritable state dir |
|---|---|---|---|---|
| `first-run.txt` first line (recommended) | written to raw `state_dir`, or `<stem>-first-run.txt` beside the config | overwritten with `first-run: passed` | stays `passed`, no retry | `_write_report` returns `None` (`:93-94`): no marker, no retry (fails closed) |
| New config field | needs `_TOP_KEYS` change and rewrite at generation | needs a rewrite step | owner must know the field | not affected |
| Absence of a "passed" report | also true for any hand-written disabled config | | | rejected |

## Retry cost by step (first_run.py)

- config (`:176-183`): local only, safe every sweep.
- label (`:195-204`): label list and create plus Approved-field check; GitHub calls each sweep; a persistent `label_failed` repeats forever.
- init_state (`:208-216`): existing store kept (`state_exists`); cheap.
- dry_run, lock, restart (`:220-253`): up to three dry-run cycles (GitHub calls, each with a 240 s deadline, `cycle.py:428`); `first_run` is not time-bounded by the loop cap (`dispatch.py:408` checks only before a repo's turn), so a repeatedly failing repo could consume much of the 270 s budget. This is why non-config steps are gated by report age.

## Confidence

Self-reported confidence: 0.85
- Evidence grounding: 1.0; Runtime check: 1.0 (inherits); Symptom coverage: 1.0; Reproducibility fit: 0.5 (no run); Fix directness: 0.5 (retry gate is a design choice); Domain coherence: 1.0.

## Risks

- A stale failed report on an owner-disabled config is retried; deleting the report or the config opts out.
- `first_run` can run for minutes and eat the loop cap; the back-off or config-only restriction bounds it.
- The helper must reuse the same `_report_dir` and name rule or it misses the report (fails closed).

## If I'm wrong, it's probably because...

The owner wants a failed first run to stay manual by design, so the right change is only to make the `not_enabled` skip reason say "first run failed, see first-run.txt".

## Falsification standard

A second production call site found by `rg -n "first_run\(" src/ tests/`, or a new test (failed first run on `worktree_invalid`, worktree created, second `run_sweep`, repo enabled and child started) that today ends at `not_enabled`.

## Evidence classification

- Claim class `static_defect`; evidence class `source_static` (read dispatch.py 55-90, 205-216, 330-505; first_run.py in full; generate.py 225-290; cycle.py 52-71, 380-440; greps of repo_init.py and tests). Runtime check performed: no.

## Alternatives considered

- Call `first_run` for every disabled config: rejected (re-enables owner-disabled repos).
- Add a `first_run_pending` config field: rejected (`_TOP_KEYS` change, generation rewrite).
- Generate with `enabled: true`: rejected (R18 wants the check to gate enabling).

## Grounding gaps

No tests run; codegraph stale. Not read: `load_config` beyond `cycle.py:59-71` (unknown-key rejection inferred), `loop_lock` code (non-overlap taken from the comment at `dispatch.py:449-451`). No report mtimes supplied; the 1 hour back-off is a suggestion. Diagnosability verdict: unknown.
