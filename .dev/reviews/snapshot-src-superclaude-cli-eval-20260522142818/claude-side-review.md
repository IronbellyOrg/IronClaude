# Claude-side independent cross-check pass (Wave 2)

Total LOC inspected: ~3,800 of ~11,000 across `commands.py`, `isolation.py`, `reporter.py`, `run_report.py`, `coverage.py`, `artifact_layout.py`, `config.py`, plus targeted reads of `runner.py` and the relevant tests.

## Critical findings

### C1. `--output-dir` bypasses the FR-G4 `<date>/<run-id>/` layout
**File:** `src/superclaude/cli/eval/commands.py:1710-1714, 1853, 1918`

Operator-supplied `--output-dir` skips `_default_output_dir`'s `<cwd>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/` layout, so artifacts land flat under the operator path. Subsequent runs alias on `per-eval/<eval_id>` and the FR-G4 invariant declared in `artifact_layout.py:6-15, 282-296` is violated.

**Recommendation:** Always anchor via `compose_run_dir(resolved_output, started_iso, suite_name)`.

### C2. `home_root.mkdir` happens BEFORE `home_root` is added to AC12 allowlist
**File:** `commands.py:1735-1746`

Side-effect-before-validation reversal of the OPS-002 doctrine. Future refactors will silently break the invariant.

**Recommendation:** Route through `resolve_scratch_root(home_root, ...)` post-allowlist-extension, OR add a regression test pinning order.

## High findings

### H1. `_format_run_summary_line` undercounts non-pass/fail/skip outcomes
**File:** `commands.py:1526-1539` — elides `errored`, `interrupted`, `timeout` counts from the verbose stdout line while `RunCounts` taxonomy tracks six totals.

### H2. `_default_output_dir` uses `Path.cwd()` — silent CWD-binding
**File:** `commands.py:1335-1343` + `artifact_layout.py:76` — `cd src && eval run` places artifacts under `<src>/.dev/eval-runs/...`. Document or anchor to repo root.

### H3. `resolve_scratch_root` accepts the bare prefix
**File:** `config.py:243-249` — `test_accepts_tmp_eval_runs_root_itself` encodes the foot-gun. Operator can pass `--output-dir /tmp/eval-runs` directly, polluting the allowlist root.

### H4. `coverage_gate` silently passes when settings.json is unreadable
**File:** `coverage.py:294-302` — Parse errors / OSError return trivially-green `CoverageResult`. Distinguish absent (green) from corrupt (red).

## Medium findings

### M1. `_NullLifecycleExecutor` makes non-PTY-tagged eval appear to PASS
**File:** `commands.py:1361-1402`

### M2. `session_id` derived from `spec.id` while `isolation.py:42-44` claims orchestrator owns it
**File:** `commands.py:1442-1446` vs `isolation.py:42-44` — two source-of-truth docstrings disagree.

### M3. `_compute_run_stats` uses hardcoded status sets for `RunTotals` while `RunCounts` derives from `EVAL_STATUSES`
**File:** `commands.py:1496-1522` — adding a new status silently drops it from totals.

### M4. `Reporter.write` vs `write_aggregated_report` produce divergent artifact sets
**File:** `reporter.py:190-227` vs `run_report.py:335-379` — Reporter writes `summary.yaml`, write_aggregated_report doesn't. Foot-gun.

### M5. `--output-dir` Click `Path` options inconsistent between `eval run` and `eval doctor`
**File:** `commands.py:1587` vs `:784`

## Low / nit findings

- `commands.py:1297` — stale header comment ("eight" helpers; actually 11+3).
- `commands.py:1815` — `del _gates` no-op signaling.
- `isolation.py:530-533` — `home_root.mkdir` before `containment_guard`.
- `coverage.py:185` — `re.sub` filename sanitiser doesn't bound output length.
- `run_report.py:283` — possible double-count of XPASS in `failures` field.
- `artifact_layout.py:99` — `_EVAL_ID_RE` duplicates `loader.validate_eval_id` regex.

## Cross-cutting observations

### CC1. FR-SCH2 regex duplicated between `artifact_layout.py:99` and `loader.validate_eval_id`

### CC2. Seven copies of exit code `2` across the eval module — centralise into `exit_codes.py`

### CC3. `_NullLifecycleExecutor` is silent — no warning, no observable runtime signal — when M5/M6 swap happens, no signal that the old shim was active

## Test coverage gaps

1. `commands.py:1853` — `run_dir=resolved_output` flat-layout case (no test).
2. `commands.py:1526` — `_format_run_summary_line` with errored/timeout counts (no test).
3. `coverage.py:297-300` — corrupt-settings.json parse failure (no test).
4. `commands.py:1735-1737` — `home_root.mkdir` ordering relationship (no test).
5. `config.py:246` — bare-prefix-as-output-dir case (`test_accepts_tmp_eval_runs_root_itself` pins the foot-gun).
6. `commands.py:1361-1402` — `_NullLifecycleExecutor` returning canned pass for un-tagged spec (no test).
7. `commands.py:1442-1446` — `session_id` ownership contract (no test).

## Validation results (per the user's 7 axes)

1. **FR-G1 ban-import rule** — PASS. `reporter.py:51-67` imports only `dataclasses`, `pathlib`, `typing`, `yaml`, `.models`, `.run_report`. No banned `superclaude.{core,agents,skills,commands}` imports.

2. **FR-G4 artifact layout** — PARTIAL. Pure path-composition; no duplicated magic strings between `artifact_layout.py` and `run_report.py`. **C1 above** breaks the contract for operator-supplied `--output-dir`.

3. **FR-G5 coverage gate** — PARTIAL. Happy path correct; **H4 above** silently passes on corrupt settings.json.

4. **FR-ISO2 path containment** — PASS (with one minor). `containment_guard` correctly uses `resolve(strict=True)` + `is_relative_to`. Symlink traversal rejected. Minor: `home_root.mkdir` precedes the guard but the guard still catches escapes.

5. **AC12 scratch-root allowlist closure (dce3c3cb)** — PASS. Tautology fix is meaningful; default-deny preserved; regression testable.

6. **eval_run lifecycle helpers (e6368db8)** — PARTIAL. 11 helpers + 3 constants present and mostly defensible, but several issues documented above (M1, M2, M3, H1, C1). Three helpers (`_utc_iso_now`, `_new_run_id`, `_default_output_dir`) could be moved out of `commands.py` (clock.py, artifact_layout.py).

7. **Residual tech debt (08183738)** — PASS. `ruff check --select F401,F821` clean. Zero `mix_stderr` remnants. `T04.09` only appears in test docstrings as historical context.
