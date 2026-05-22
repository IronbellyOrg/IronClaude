# cliEval Post-Sprint Remediation — Architecture Spec

**Source review:** `.dev/reviews/snapshot-src-superclaude-cli-eval-20260522142818/REVIEW.md`
**Target module:** `src/superclaude/cli/eval/`
**Generated:** 2026-05-22
**Type:** architecture (component-level remediation)
**Scope:** 5 High + 6 Medium findings + 3 cross-cutting concerns + 7 test-coverage gaps

## 1. Design Intent

Restore the **FR-G4 artifact-layout invariant**, **FR-G5 coverage-gate fail-closed semantics**, and **complete failure-taxonomy observability** in the eval_run lifecycle without altering the public CLI surface or the AC12 allowlist closure. Tighten three architectural seams (cwd-binding, executor silence, SoT drift) where the Phase 4/5 work landed correct *behavior* but fragile *contracts*.

Out of scope: changes to the orchestrator, runner, pty_driver, expect, hook_adapter, or claude_process. No new dependencies. No public-API surface changes.

## 2. Component Boundaries

| Component | File | Role in remediation |
|---|---|---|
| `commands.py` | eval/commands.py | Owns `eval_run` Click entry + 11 helpers; H1/H3/H5/M1/M2/M3/M6 anchor here |
| `coverage.py` | eval/coverage.py | Owns `coverage_gate`; H2 anchor |
| `config.py` | eval/config.py | Owns `resolve_scratch_root`; H4 anchor |
| `artifact_layout.py` | eval/artifact_layout.py | Owns `compose_run_dir` and `_EVAL_ID_RE`; H1 reach + CC1 anchor |
| `reporter.py` / `run_report.py` | eval/{reporter,run_report}.py | M4 anchor (artifact-set divergence) |
| `exit_codes.py` | **NEW** eval/exit_codes.py | CC2 consolidation target |
| `loader.py` | eval/loader.py | CC1 reach (FR-SCH2 regex SoT) |

## 3. Per-Finding Specifications

### H1 — Anchor `--output-dir` through `compose_run_dir`

**Invariant violated:** FR-G4 — every run anchors at `<root>/<YYYY-MM-DD>/<run-id>/`.

**Current behavior:** `commands.py:1710-1714` resolves `output_dir` as-is; `:1853` and `:1918` pass that path to Reporter / per-eval writers. Operator-supplied `--output-dir /tmp/foo` produces a flat layout, and subsequent runs alias on `per-eval/<eval_id>`.

**Target contract:**

```
resolved_output = compose_run_dir(
    root        = operator_output_dir or _default_output_dir(),
    started_iso = started_at,
    suite_name  = suite.name,
)
```

The composer is the **single** path-shape authority. `commands.py` MUST call it on both branches.

**Acceptance:**

1. `eval run --output-dir /tmp/x --suite SUITE` produces `/tmp/x/<YYYY-MM-DD>/<run-id>/` — verified by integration test.
2. The `run_dir=resolved_output` flat-path branch is deleted; static grep for `run_dir=resolved_output` returns 0 hits.
3. `compose_run_dir` is called in exactly one place in `commands.py`.

### H2 — Fail-closed coverage gate on corrupt settings.json

**Invariant violated:** FR-G5 — absent ≠ corrupt.

**Current behavior:** `coverage.py:294-302` returns `CoverageResult(passed=True, ...)` on JSON parse error or OSError.

**Target contract:** Distinguish three states:

| Source state | Result |
|---|---|
| settings.json absent | `passed=True, status="absent"` (existing behavior preserved) |
| settings.json present + parseable + gate met | `passed=True, status="passed"` |
| settings.json present + parseable + gate failed | `passed=False, status="failed"` |
| settings.json present + unparseable (JSONDecodeError / OSError / KeyError on required keys) | `passed=False, status="corrupt", reason="<exception type + message>"` |

**Acceptance:**

1. New test `test_coverage_gate_fails_on_corrupt_settings_json` writes malformed JSON, asserts `passed=False`.
2. New test `test_coverage_gate_absent_passes_with_status_absent` regression-pins the absent-passes path.
3. The verbose stdout line surfaces `status="corrupt"` distinctly from `status="absent"`.

### H3 — `_format_run_summary_line` renders full failure taxonomy

**Invariant violated:** Observability — the verbose line must reflect `RunCounts` taxonomy (six totals: `passed, failed, skipped, errored, interrupted, timeout`).

**Current behavior:** `commands.py:1526-1539` renders only `P/F/S`.

**Target contract:** Render `passed, failed, skipped, errored, interrupted, timeout` whenever any non-zero. Omit zero buckets to keep the happy path concise. Status set is derived from `EVAL_STATUSES`, not hardcoded — adding a new status MUST extend the line automatically.

**Acceptance:**

1. New test `test_format_run_summary_line_renders_errored_interrupted_timeout` — three specs of those outcomes appear on the line.
2. New test `test_format_run_summary_line_omits_zero_buckets` — happy path keeps current format.
3. `_compute_run_stats` (`commands.py:1496-1522`) derives `RunTotals` keys from `EVAL_STATUSES` rather than a hardcoded set (fixes M3 simultaneously).

### H4 — `resolve_scratch_root` rejects bare allowlist prefix

**Invariant violated:** Defense-in-depth — operators MUST NOT be able to point eval artifacts at the allowlist root itself.

**Current behavior:** `config.py:243-249` returns `prefix` unchanged when `resolved == prefix`. `test_accepts_tmp_eval_runs_root_itself` encodes the foot-gun.

**Target contract:** When the resolved path equals any allowlist prefix exactly, raise `ScratchRootError("--output-dir must be a subdirectory of the allowlist root, not the root itself")`.

**Acceptance:**

1. The pinning test is **inverted**: now asserts `ScratchRootError` raised.
2. New positive test `test_accepts_immediate_subdir_of_allowlist_root` — `/tmp/eval-runs/x` passes.
3. Error message names both the offending path and the allowlist root.

### H5 — Allowlist extension precedes `home_root.mkdir`

**Invariant violated:** OPS-002 doctrine — validate-before-side-effect.

**Current behavior:** `commands.py:1735-1746` calls `home_root.mkdir(parents=True, exist_ok=True)` *before* extending the AC12 allowlist with `home_root`.

**Target contract:** Route through `resolve_scratch_root(home_root, allowlist=allowlist + [home_root])` first; mkdir only on the resolved path returned by that call. If extension fails, `home_root` is never created.

**Acceptance:**

1. New regression test `test_home_root_extension_precedes_mkdir` — patches `resolve_scratch_root` to raise; asserts `home_root` does not exist on disk after the failed call.
2. Static grep for `home_root.mkdir` returns 0 hits prior to the allowlist extension call.

## 4. Medium-Severity Bundle (in-PR if cheap)

| ID | File:Line | Change |
|---|---|---|
| M1 | `commands.py:1335-1343` | Add docstring noting `_default_output_dir` is CWD-relative; do NOT anchor to repo root (existing tests depend on the relative behavior — flag for follow-up not bundled) |
| M2 | `commands.py:1361-1402` | `_NullLifecycleExecutor` emits a `WARNING`-level log line "null lifecycle executor active — no PTY tagging" the first time it runs |
| M3 | `commands.py:1496-1522` | Folded into H3 (single-source-of-truth `EVAL_STATUSES`) |
| M4 | `reporter.py:190-227` vs `run_report.py:335-379` | Extract `_write_artifact_set(run_dir, ...)` helper; both call paths invoke it; `summary.yaml` written unconditionally |
| M5 | `commands.py:1442-1446` | Replace inline `session_id = spec.id` with `session_id = orchestrator.allocate_session_id(spec)`; reconcile with `isolation.py:42-44` docstring |
| M6 | `commands.py:1587` vs `:784` | Align Click `Path` option definitions for `eval run` and `eval doctor` (same `path_type=Path`, same `resolve_path` setting) |

## 5. Cross-Cutting Refactors

### CC1 — Centralize FR-SCH2 regex
- Move `_EVAL_ID_RE` from `artifact_layout.py:99` and the duplicate in `loader.validate_eval_id` to a new module-level constant `EVAL_ID_PATTERN` in `artifact_layout.py`.
- Both consumers import from there.
- Add `test_eval_id_pattern_single_source` — greps `re.compile.*eval` across `cli/eval/` and asserts only one match.

### CC2 — Consolidate exit codes
- Create `src/superclaude/cli/eval/exit_codes.py` with named constants:
  - `RUN_CLEAN_EXIT_CODE = 0` (existing at `commands.py:570`)
  - `RUN_FAILURES_EXIT_CODE = 1` (existing at `:573`)
  - `RUN_INTERRUPTED_EXIT_CODE = 130` (existing at `:577`)
  - `RUN_USAGE_ERROR_EXIT_CODE = 2` (consolidates the seven scattered copies)
- All eval module files import from `exit_codes`. No magic `2` literals remain.
- Test: `test_no_magic_exit_codes` — greps `sys.exit(2)|raise click.exceptions.Exit(2)` and asserts 0 matches.

### CC3 — NullLifecycleExecutor observability
- Folded into M2.

## 6. Test-Coverage Gap Closure

Add the following tests under `tests/cli/eval/`:

| # | Test | Pins |
|---|---|---|
| T1 | `test_eval_run_output_dir_anchors_compose_run_dir` | H1 |
| T2 | `test_format_run_summary_line_errored_interrupted_timeout` | H3 |
| T3 | `test_coverage_gate_fails_on_corrupt_settings_json` | H2 |
| T4 | `test_home_root_mkdir_after_allowlist_extension` | H5 |
| T5 | `test_resolve_scratch_root_rejects_bare_prefix` (invert existing) | H4 |
| T6 | `test_null_lifecycle_executor_logs_warning_when_active` | M2 |
| T7 | `test_session_id_owned_by_orchestrator_not_command` | M5 |
| T8 | `test_eval_id_pattern_single_source` | CC1 |
| T9 | `test_no_magic_exit_codes_in_eval_module` | CC2 |

## 7. Non-Goals (Deferred / Filed)

- L1-L6 nits: track separately; do not bundle (avoids PR sprawl).
- `_default_output_dir` repo-root anchoring (H2 variant from cross-check): defer pending an explicit operator-experience decision.
- Schema-vs-model drift audit (architect-pass clean verdict): no action.

## 8. Implementation Order (Dependency-Aware)

```
Phase 1 (test scaffolding):    T3, T5, T6  ← red baseline before any source change
Phase 2 (correctness):          H4, H2     ← failures fail closed, foot-gun closed
Phase 3 (observability):        H3, M3, M2 ← single-source EVAL_STATUSES + null-exec warning
Phase 4 (layout):               H1, M4     ← compose_run_dir authority + artifact-set parity
Phase 5 (ordering):             H5         ← allowlist before mkdir
Phase 6 (cross-cutting):        CC1, CC2   ← regex SoT + exit_codes module
Phase 7 (Click symmetry):       M5, M6     ← session_id ownership + Path option parity
Phase 8 (final regression):     run all T# tests + full pytest + ruff F401,F821
```

Each phase is independently revertable. Phase 1 (test scaffolding) is the contract — if Phase 2-7 changes pass Phase 1 tests, the remediation is done.

## 9. Validation Hooks

- `make verify-sync` after each phase (no `.claude/` drift)
- `uv run pytest tests/cli/eval/ -v` after each phase
- `uv run ruff check --select F401,F821 src/superclaude/cli/eval/` after each phase
- Final: `superclaude doctor` smoke test (no install-time regressions)

## 10. Exit Criteria

1. All 9 new tests (T1-T9) pass.
2. Full `pytest tests/cli/eval/` green.
3. `ruff` F401/F821 clean.
4. `make verify-sync` clean.
5. Static grep gates from §3 acceptance criteria all return 0 hits.
6. No new dependencies in `pyproject.toml`.
7. Public CLI surface unchanged: `eval run --help` output diff is empty.
