# QA Report — PG-2 (layout + ordering correctness)

**Task:** TASK-RF-20260522-153212 (cliEval remediation)
**Phase:** task-integrity / PG-2 gate
**Date:** 2026-05-22
**Fix authorization:** false (report-only)
**Mode:** Zero-trust adversarial — independent verification

---

## Overall Verdict: **PASS**

All 8 findings (H1, M4, H5a, H5b, T1, T2, T4a, T4b) verified against source. Pytest regression: 1368 passed, 0 failed, 4 skipped — matches the expected ≥1368 baseline (1359 Phase 1 baseline + 9 new tests: T3 + T5b + T6 + T1 + T2 ×3 params + T4a + T4b). The H1 grep gate returns 0 hits. H5a and H5b ordering invariants hold by absolute line number. No issues found.

---

## Per-Finding Evaluation

### H1 — FR-G4 layout restoration via compose_run_dir → **PASS**

**Spec contract:** `--output-dir` is the OUTPUT ROOT; run-dir composed via `compose_run_dir(resolved_output_root, started_iso, suite_name)`. Artifacts land at `<output_root>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/`. Grep gate `run_dir=resolved_output` must return 0 hits.

**Evidence (independent reads):**
- `src/superclaude/cli/eval/commands.py:1730-1736` — `resolved_output_root = resolve_scratch_root(output_dir, config=base_config)` followed by `resolved_run_dir = compose_run_dir(resolved_output_root, started_iso, suite_name)`.
- `src/superclaude/cli/eval/commands.py:1737-1749` — default flow: `_default_output_dir(...)` returns the FR-G4 run-dir anchored at `Path.cwd()` via `compose_run_dir`; resolved via `resolve_scratch_root` and then `resolved_output_root = resolved_run_dir`.
- `src/superclaude/cli/eval/commands.py:1338-1346` — `_default_output_dir` confirmed to delegate to `compose_run_dir(Path.cwd(), ...)`.
- `src/superclaude/cli/eval/commands.py:1826` — `coverage_gate(..., output_dir=resolved_run_dir)`.
- `src/superclaude/cli/eval/commands.py:1900-1909` — `_run_one_spec(spec, run_dir=resolved_run_dir, home_root=home_root, config=runtime_config, ...)`.
- `src/superclaude/cli/eval/commands.py:1967` — `Reporter(summary=summary, emit_junit=junit).write(resolved_run_dir)`.
- **Grep gate:** `grep -rn "run_dir=resolved_output" src/superclaude/cli/eval/` → **0 hits**. Also confirmed no bare `resolved_output` variable exists (only `resolved_output_root` and `resolved_run_dir`).

**Verdict:** PASS. Flat-layout branch deleted, all downstream consumers anchored to `resolved_run_dir`.

---

### M4 — Reporter / write_aggregated_report consolidation → **PASS**

**Spec contract:** Both `Reporter.write` and `write_aggregated_report` delegate to `_write_artifact_set`. Always writes summary.{md,json,yaml}; conditionally writes junit.xml. `render_summary_yaml` lives in run_report.py (not reporter.py); reporter.py re-exports it.

**Evidence (independent reads):**
- `src/superclaude/cli/eval/run_report.py:337-361` — `render_summary_yaml` defined here (with M4 docstring noting promotion from reporter.py).
- `src/superclaude/cli/eval/run_report.py:364-408` — `_write_artifact_set` exists with injected renderer callables (`md_renderer`, `json_renderer`, `yaml_renderer`, `junit_renderer`); unconditionally writes summary.md / summary.json / summary.yaml; conditionally writes junit.xml on `emit_junit=True`.
- `src/superclaude/cli/eval/run_report.py:411-439` — `write_aggregated_report` delegates to `_write_artifact_set(Path(output_dir), summary=summary, emit_junit=emit_junit)`.
- `src/superclaude/cli/eval/reporter.py:58-67` — imports `_write_artifact_set` and `render_summary_yaml` from `.run_report`.
- `src/superclaude/cli/eval/reporter.py:74` — re-exports `render_summary_yaml` for backward-compatibility (in `__all__`).
- `src/superclaude/cli/eval/reporter.py:81-85` — comment confirming the SoT move.
- `src/superclaude/cli/eval/reporter.py:144` — `Reporter.to_yaml` delegates to `render_summary_yaml`.
- `src/superclaude/cli/eval/reporter.py:187-196` — `Reporter.write` calls `_check_invariant(self.summary)` then `_write_artifact_set(...)` with lambda renderers wrapping the instance methods (`md_renderer=lambda _s: self.to_markdown()`, etc.).

**Verdict:** PASS. The +1 yaml divergence between `Reporter.write` and `write_aggregated_report` is closed via the shared helper. Both paths produce the same artifact set from a single SoT.

---

### H5a — OPS-002 ordering site 1 (commands.py) → **PASS**

**Spec contract:** `runtime_allowed = tuple(...) + (resolved_output_root, resolved_run_dir, home_root)` precedes `runtime_config = EvalConfig(...)` precedes `home_root.mkdir(...)` by absolute line number.

**Evidence (grep + independent read):**
- `grep -n "home_root.mkdir\|runtime_allowed\|runtime_config" src/superclaude/cli/eval/commands.py` (first 10 hits):
  - L1766: `runtime_allowed = tuple(base_config.allowed_scratch_roots) + (`
  - L1771: `runtime_config = EvalConfig(`
  - L1774: `allowed_scratch_roots=runtime_allowed,`
  - L1781: `home_root.mkdir(parents=True, exist_ok=True)`
- Line numbers strictly increasing: **1766 < 1771 < 1781**. Allowlist extension → EvalConfig construction → home_root.mkdir is the correct OPS-002 order.
- `src/superclaude/cli/eval/commands.py:1762-1765` carries the H5a anchor comment explaining the ordering invariant.

**Verdict:** PASS. Absolute line ordering confirmed.

---

### H5b — OPS-002 ordering site 2 (isolation.py) → **PASS**

**Spec contract:** `HomeIsolation.setup` performs an allowlist pre-check on `self.home_root` BEFORE `self.home_root.mkdir(...)`. Non-allowlisted paths raise `HomeContainmentViolation(check="scratch_root_allowlist")` with no on-disk side effect.

**Evidence (independent read of isolation.py:550-590):**
- `src/superclaude/cli/eval/isolation.py:561` — `_resolved_root = self.home_root.expanduser().resolve(strict=False)` (resolves home_root).
- `src/superclaude/cli/eval/isolation.py:562-564` — `_config_prefixes = [_resolve_prefix(p) for p in config.allowed_scratch_roots]` (mirrors Check 2 of `containment_guard`).
- `src/superclaude/cli/eval/isolation.py:565-568` — membership check via `_resolved_root == prefix or _resolved_root.is_relative_to(prefix)`.
- `src/superclaude/cli/eval/isolation.py:569-581` — on non-membership, constructs `ScratchRootViolation(...)`, raises it via try/except, then re-raises as `HomeContainmentViolation(check="scratch_root_allowlist", home_path=self.home_root, scratch_root=self.home_root, eval_id=self.eval_id, detail=str(exc)) from exc`.
- `src/superclaude/cli/eval/isolation.py:586` — `self.home_root.mkdir(parents=True, exist_ok=True)` runs AFTER the pre-check.
- Absolute line ordering: pre-check (L561-581) **<** mkdir (L586).

**Verdict:** PASS. Pre-check refusal occurs before any filesystem write; exception type matches the post-mkdtemp guard so callers branch on a single `HomeContainmentViolation`.

---

### T1 — `test_run_anchors_output_via_compose_run_dir` → **PASS**

**Location:** `tests/cli/eval/test_eval_run.py:488-551`

**Spec contract:** Pin H1/FR-G4 layout invariant — `--output-dir` is the OUTPUT ROOT; artifacts land at `<output_dir>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/`; summary.{md,json,yaml} all co-exist; flat-layout regression guard.

**Evidence:**
- Test name and docstring (L491-501) explicitly target H1 / FR-G4.
- Invokes `eval_group` via `CliRunner` with `--output-dir output_dir/h1-anchor`.
- Asserts `output_dir / ".dev" / "eval-runs"` is a directory (L525-528).
- Asserts exactly one date-stamped dir (L529-533) and one run-id dir (L534-538).
- Asserts `summary.md`, `summary.json`, `summary.yaml` all exist in run_dir (L542-544) — M4 unconditional yaml guarantee.
- Regression guard at L548-551: asserts `summary.md` does NOT live at flat layout (directly under `--output-dir`).
- Would fail on a pre-H1 regression that flattens the layout.

**Verdict:** PASS. Test pins the H1 invariant correctly and would catch regressions.

---

### T2 — `test_format_run_summary_line_renders_errored_interrupted_timeout` (3× parametrized) → **PASS**

**Location:** `tests/cli/eval/test_run_summary.py:370-403`

**Spec contract:** Pin H3 — `_format_run_summary_line` renders all six DM-012 buckets (P/F/S/E/I/T).

**Evidence:**
- `@pytest.mark.parametrize("bucket,abbreviation", [("errored","E"),("interrupted","I"),("timeout","T")])` (L370-377).
- Test docstring (L381-389) explicitly cites the pre-H3 elision and the post-H3 contract.
- For each bucket, sets count to 3 and asserts `f"3{abbreviation}"` appears in the line (L403).
- Would fail on a regression that omits any of E/I/T from the rendered format.

**Verdict:** PASS. Pins the H3 invariant across all three new buckets.

---

### T4a — `test_eval_run_extends_allowlist_before_mkdir` → **PASS**

**Location:** `tests/cli/eval/test_home_isolation_extend.py:601-707`

**Spec contract:** Pin H5a/OPS-002 — runtime EvalConfig with extended allowlist constructed BEFORE home_root.mkdir.

**Evidence:**
- Test docstring (L605-620) explicitly cites H5a/OPS-002 and the pre/post-fix ordering.
- Monkeypatches `commands_module.EvalConfig.__init__` (L632-645) to log each `EvalConfig` build (filters by `len(allowed_scratch_roots) > 2` to skip the base_config build).
- Monkeypatches `Path.mkdir` (L647-656) to log mkdirs where `self.name == "homes"` (the home_root mkdir per `commands.py:home_root = resolved_run_dir / "homes"`).
- Asserts `config_idx < mkdir_idx` (L695-699) — EvalConfig construction precedes home_root.mkdir in event_log.
- Defense-in-depth assertion at L704-707: extended allowlist contains a path ending in "homes" (home_root is in allowlist at moment of mkdir).
- Would fail on H5a regression where mkdir runs before allowlist extension.

**Verdict:** PASS. Test pins H5a ordering with spy-based event log + index comparison.

---

### T4b — `test_home_isolation_setup_rejects_non_allowlisted_home_root_before_mkdir` → **PASS**

**Location:** `tests/cli/eval/test_containment.py:592-646`

**Spec contract:** Pin H5b — `HomeIsolation.setup` raises `HomeContainmentViolation(check="scratch_root_allowlist")` with no on-disk side effect when home_root is non-allowlisted.

**Evidence:**
- Test docstring (L595-611) cites H5b/OPS-002 and pre/post-fix behavior.
- Constructs a narrow EvalConfig with `allowed_scratch_roots=(allowed,)` not containing `non_allowlisted_root` (L618-620).
- Snapshots parent directory contents BEFORE the refused setup (L628).
- Asserts `HomeContainmentViolation` is raised (L630-631).
- Asserts `exc_info.value.check == "scratch_root_allowlist"` (L633) — pins exception attribute.
- Asserts `not non_allowlisted_root.exists()` (L636-639) — no on-disk side effect.
- Asserts parent contents unchanged after refusal (L640-645).
- Asserts `not iso.is_set_up` (L646).
- Would fail on H5b regression where mkdir runs before the allowlist pre-check.

**Verdict:** PASS. Test pins H5b with explicit on-disk-side-effect-absence assertion.

---

## Pytest Regression Verification

**Command:** `cd /config/workspace/IronClaude && unset VIRTUAL_ENV; uv run pytest tests/cli/eval/ 2>&1 | tail -5`

**Result:** `1368 passed, 4 skipped, 5 warnings in 19.28s` — **0 failures**.

**Math:** Phase 1 baseline 1359 passed + 9 new tests (T3 + T5b + T6 + T1 + T2 ×3 params + T4a + T4b) = 1368. Matches expected (≥1368). PASS.

---

## H5b-Collateral Test Updates Verification

**Spec contract:** 14 collateral tests across test_atomic_setup.py, test_symlink_attacks.py, test_hard_guard_real_home.py, test_path_containment.py must reflect the new H5b invariant (no partial HOME on allowlist failure; symlink Check 3 still preserves partial HOME post-mkdtemp).

**Evidence (git diff --stat):**
- `tests/cli/eval/test_atomic_setup.py`: 123 lines changed (insertions/deletions).
- `tests/cli/eval/test_symlink_attacks.py`: 124 lines changed.
- `tests/cli/eval/test_hard_guard_real_home.py`: 42 lines changed.
- `tests/cli/eval/test_path_containment.py`: 29 lines changed.
- Total: 4 files, 194 insertions / 124 deletions.

**Grep evidence (H5b invariant references):**
- `test_path_containment.py`: 10 matches for `no_partial_home|H5b|scratch_root_allowlist`.
- `test_hard_guard_real_home.py`: 12 matches.
- `test_symlink_attacks.py`: 23 matches.
- `test_atomic_setup.py`: 19 matches.

All four files carry H5b invariant updates and pass under the new contract (per the 1368-passed result above).

**Verdict:** PASS.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | H1 (FR-G4 layout restoration) | PASS | commands.py:1730-1749 + grep gate 0 hits |
| 2 | M4 (Reporter / write_aggregated_report consolidation) | PASS | run_report.py:337-439 + reporter.py:58-67,144,187-196 |
| 3 | H5a (commands.py ordering) | PASS | L1766 < L1771 < L1781 |
| 4 | H5b (isolation.py ordering) | PASS | L561-581 < L586 |
| 5 | T1 test | PASS | test_eval_run.py:488-551 |
| 6 | T2 test (3× parametrized) | PASS | test_run_summary.py:370-403 |
| 7 | T4a test | PASS | test_home_isolation_extend.py:601-707 |
| 8 | T4b test | PASS | test_containment.py:592-646 |
| 9 | Pytest regression (>=1368 passed, 0 failed) | PASS | 1368 passed, 4 skipped, 0 failed |
| 10 | H5b collateral test updates (14 tests, 4 files) | PASS | git diff --stat + 64 grep hits across the 4 files |

---

## Summary

- Checks passed: **10 / 10**
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

---

## Issues Found

**None.** All 8 findings (H1, M4, H5a, H5b, T1, T2, T4a, T4b) verified against source with file:line evidence. Pytest regression clean. H5b-collateral test updates landed across all 4 expected files.

---

## Confidence Gate

- **Verified:** 10 / 10
- **Unverifiable:** 0
- **Unchecked:** 0
- **Confidence:** 100.0%
- **Tool engagement:** Read: 8 | Grep (Bash): 7 | Glob: 0 | Bash (pytest/git): 2

Tool calls (17 total) exceed the checklist item count (10), satisfying the engagement minimum. Every PASS verdict is backed by a specific file:line citation from an independent Read, a grep result with line numbers, or a pytest exit count. No reliance on prior agent claims — H1 grep gate, H5a/H5b line ordering, M4 SoT delegation, and all four new tests were re-verified directly from source.

---

## Recommendations

Green light to proceed. Phase 4 work is structurally correct against the PG-2 spec contract. No remediation needed.

## QA Complete
