# Code Review: src/superclaude/cli/eval/ (post Phase 4 + 5 sprint)

**Target**: snapshot of `src/superclaude/cli/eval/` (23 Python files, 11,019 LOC + 3 schema/index files)
**Reviewer**: `/sc:auggie-review` (depth=deep, focus=security,architecture,quality,tests,anti-patterns)
**Generated**: 2026-05-22 14:50 UTC
**Source PR**: n/a (snapshot mode)
**Base ↔ Head**: working tree at master `5d71ae5e` (cliEval commits: 1ca25953, dce3c3cb, e6368db8, 08183738)
**Stats**: 23 files, 11,019 LOC, **47 raw findings** → **17 findings retained**, **30 dropped during grounding** (hallucinated file:line citations or unfounded claims)

---

## Summary

**Recommendation: Request changes** — 0 Critical, 5 High, 6 Medium, 6 Low, plus 3 cross-cutting observations and 7 test-coverage gaps.

Top three risks: (1) `--output-dir` operator paths bypass the FR-G4 `<date>/<run-id>/` layout invariant (`commands.py:1710-1714, 1853`); (2) the FR-G5 coverage gate silently passes when `settings.json` is unreadable/corrupt (`coverage.py:294-302`), defeating the gate's purpose on the failure path most likely to indicate a broken matcher; (3) `_format_run_summary_line` undercounts half the failure taxonomy (`errored`, `interrupted`, `timeout`) in operator stdout while the exit code still reflects them (`commands.py:1526-1539`).

The post-sprint tech-debt cleanup is solid: F401/F821 are clean, `mix_stderr` is fully removed, `shell=True` does not appear, `tempfile.mktemp` does not appear, `T04.09` only persists as historical context in test docstrings, and the AC12 scratch-root tautology fix from commit dce3c3cb is meaningful and pinned by `test_rejects_non_allowlisted_paths`. **FR-G1 ban-import rule is fully observed** across the snapshot (zero banned imports anywhere in `src/superclaude/cli/eval/`), refuting both Auggie passes that claimed a violation in `reporter.py:8`.

The 11 helpers + 3 exit-code constants from commit e6368db8 are mostly defensible but three (`_utc_iso_now`, `_new_run_id`, `_default_output_dir`) could plausibly live in `artifact_layout.py` (or a new `clock.py`) rather than `commands.py`. `_NullLifecycleExecutor` is a known M2 shim with no operator-visible warning — when M5/M6 lands the swap will be hard to verify.

---

## Findings

### 🟠 High (should fix before this batch is closed)

#### H1. `--output-dir` bypasses the FR-G4 `<date>/<run-id>/` layout

- **File**: `src/superclaude/cli/eval/commands.py:1710-1714, 1853, 1918`
- **Category**: data-integrity / api-contract
- **Source**: claude-side (Auggie passes did not surface this)
- **Evidence**:
  ```python
  requested_output = (
      output_dir
      if output_dir is not None
      else _default_output_dir(started_at=started_iso, suite_name=suite_name)
  )
  ...
  resolved_output = resolve_scratch_root(requested_output, config=base_config)
  ...
  return _run_one_spec(spec, run_dir=resolved_output, ...)
  ```
- **Why this matters**: `_default_output_dir(...)` returns the full FR-G4 layout `<cwd>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/`. When the operator passes `--output-dir /tmp/eval-runs/myrun`, `resolved_output = /tmp/eval-runs/myrun` (no `<date>/<run-id>/` segments), and `Reporter.write(resolved_output)` writes flat under the operator path. Multiple runs against the same `--output-dir` alias on `per-eval/<eval_id>` paths and silently overwrite prior `summary.{md,json,yaml}`. The FR-G4 contract declared in `artifact_layout.py:6-15, 282-296` says the layout is the *single source of truth* for the on-disk shape of every `superclaude eval run` invocation — this path violates it.
- **Recommendation**: Always anchor via `run_dir = compose_run_dir(resolved_output, started_iso, suite_name)`, then pass `run_dir` to `_run_one_spec(run_dir=...)` and `Reporter.write(...)`. Operator's `--output-dir` becomes the `output_root` argument to `compose_run_dir`, not the run dir itself.

#### H2. FR-G5 coverage gate silently passes when `settings.json` is unreadable

- **File**: `src/superclaude/cli/eval/coverage.py:294-302`
- **Category**: correctness / data-integrity
- **Source**: claude-side (Auggie's `coverage.py:210` TOCTOU finding hallucinated; this is the real issue)
- **Evidence**:
  ```python
  matcher_filter = matcher_filter or default_matcher_filter
  if not settings_path.is_file():
      return CoverageResult()
  try:
      data = json.loads(settings_path.read_text(encoding="utf-8"))
  except (OSError, json.JSONDecodeError):
      return CoverageResult()
  if not isinstance(data, Mapping):
      return CoverageResult()
  ```
- **Why this matters**: An empty `CoverageResult` has `missing=()`, so `.passed` is `True`. The docstring at lines 271-276 justifies "missing file → green" so dev hosts without `settings.json` stay clean. But the SAME silent-pass behavior fires when the file is present but corrupt (JSON parse error) or unreadable (OSError). The bug class FR-G5 exists to catch is "a matcher pattern broke and no eval noticed" — a corrupt `settings.json` is a strong signal that matchers may have broken silently, and that should NOT result in a green gate.
- **Recommendation**: Distinguish "file absent" (green) from "file present but unparseable/unreadable" (red). Return a `CoverageResult` with a synthetic `missing=("settings.json unparseable",)` entry, or raise a typed error mapped to `COVERAGE_GATE_FAILED_EXIT_CODE` (= 2). Add a regression test in `test_coverage_gate.py` pinning the corrupt-settings.json path.

#### H3. `_format_run_summary_line` undercounts errored / interrupted / timeout

- **File**: `src/superclaude/cli/eval/commands.py:1526-1539`
- **Category**: correctness / api-contract
- **Source**: claude-side (Auggie qa pass flagged "missing Unicode edge case test" — wrong axis)
- **Evidence**:
  ```python
  def _format_run_summary_line(summary: RunSummary, output_dir: Path) -> str:
      return (
          f"run {summary.run_id}: "
          f"{summary.totals.passed}P/"
          f"{summary.totals.failed}F/"
          f"{summary.totals.skipped}S "
          f"in {summary.duration_sec:.2f}s "
          f"-> {output_dir}"
      )
  ```
- **Why this matters**: The status taxonomy from `_compute_run_stats` (`commands.py:1515-1522`) tracks six totals: `passed`, `failed`, `skipped`, `errored`, `interrupted`, `timeout`. The verbose stdout line elides three of them. An operator running `eval run --verbose` whose three evals all timed out sees `0P/0F/3S` and assumes a clean skip, when the exit code is `RUN_FAILURES_EXIT_CODE (=1)` and the markdown rendering at `run_report.py:170-174` *does* surface all six. The verbose stdout is the only place where this projection drops half the failure taxonomy. Operators routinely tail stdout in CI before they look at the markdown — this misleads them.
- **Recommendation**: Either spell out all six counts (`{P}P/{F}F/{S}S/{E}E/{I}I/{T}T`) or document the aggregation in the docstring and fold `errored/interrupted/timeout` into `F`.

#### H4. `resolve_scratch_root` accepts the bare allowlist prefix as a scratch root

- **File**: `src/superclaude/cli/eval/config.py:243-249` + `tests/cli/eval/test_scratch_root_allowlist.py:52-56`
- **Category**: security (latent)
- **Source**: claude-side
- **Evidence**:
  ```python
  for prefix in allowed:
      # ``is_relative_to`` catches strict sub-paths; the equality branch
      # accepts the prefix itself (``/tmp/eval-runs`` is a valid root).
      if resolved == prefix or resolved.is_relative_to(prefix):
          return resolved
  ```
- **Why this matters**: `test_accepts_tmp_eval_runs_root_itself` pins this as deliberate behavior — `resolve_scratch_root("/tmp/eval-runs")` returns the bare prefix. Combined with **H1**: an operator who passes `--output-dir /tmp/eval-runs` (or `--output-dir .dev/eval-runs`) gets `resolved_output = <prefix>`, then `_run_one_spec` writes `per-eval/<eval_id>/` directly under the allowlist root with no run-id segregation. Reporter writes `summary.{md,json,yaml}` at that root. `rm -rf <root>/per-eval` no longer catches all the artifacts. This is more "footgun" than "exploit" — but it weakens the AC12 closure that commit dce3c3cb just landed.
- **Recommendation**: Reject the bare prefix when used as `--output-dir` (require operator paths to be *strict* sub-paths of an allowlisted root). The general `resolve_scratch_root` can keep accepting the prefix for internal allowlist checks; the policy belongs in the `--output-dir` boundary at `commands.py:1727-1730`.

#### H5. `home_root.mkdir` happens BEFORE `home_root` is in the AC12 allowlist

- **File**: `src/superclaude/cli/eval/commands.py:1735-1746`
- **Category**: security (defensive-doctrine violation)
- **Source**: claude-side
- **Evidence**:
  ```python
  resolved_output.mkdir(parents=True, exist_ok=True)
  home_root = resolved_output / "homes"
  home_root.mkdir(parents=True, exist_ok=True)        # ← FS write happens HERE

  runtime_allowed = tuple(base_config.allowed_scratch_roots) + (
      resolved_output,
      home_root,
  )
  runtime_config = EvalConfig(..., allowed_scratch_roots=runtime_allowed, ...)
  ```
- **Why this matters**: `home_root` is by construction a child of `resolved_output` (already validated), so the path is fine *today*. But the `mkdir` is a filesystem write that precedes adding `home_root` to the allowlist. The OPS-002 doctrine repeated through this file (e.g. `isolation.py:165-179`, `config.py:179-185`) is "hard refusal before side effects". This reverses the order: side-effect first, then add to allowlist. A future refactor that swaps `resolved_output / "homes"` for an operator-derived path (or moves the block above the `resolved_output.mkdir`) silently breaks the invariant with no test catching the order swap.
- **Recommendation**: Either (a) route `home_root` through `resolve_scratch_root(home_root, config=runtime_config)` *after* extending `runtime_allowed` but *before* the mkdir, or (b) keep current order but add a pinned regression test asserting "mkdir is not called before allowlist extension" and a load-bearing code comment explaining why current order is safe.

### 🟡 Medium (fix in this PR if cheap, otherwise file followup)

#### M1. `_default_output_dir` uses `Path.cwd()` — CWD-binding is invisible

- **File**: `src/superclaude/cli/eval/commands.py:1335-1343`
- **Category**: correctness / docs
- **Evidence**:
  ```python
  def _default_output_dir(*, started_at: str, suite_name: str) -> Path:
      """Return the default per-run output directory under the AC12 prefix.

      Anchored on :func:`artifact_layout.compose_run_dir` so the layout
      matches FR-G4 / D-0074 exactly: ``<cwd>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/``.
      ...
      """
      return compose_run_dir(Path.cwd(), started_at, suite_name)
  ```
- **Why**: `RUN_DIR_PREFIX = Path(".dev/eval-runs")` is the AC12-allowlisted prefix *relative to CWD*. If the operator is `cd`'d into a subdirectory (`cd src && superclaude eval run --suite real`), artifacts land at `<src>/.dev/eval-runs/...` and `resolve_scratch_root` agrees (also CWD-bound). Operator's mental model is "artifacts go under repo `.dev/eval-runs`". The two sides "agree" because both use CWD, but the user gets surprised.
- **Recommendation**: Either document the CWD-binding in `_default_output_dir`'s docstring AND in `--output-dir`'s Click help text, or anchor to the repo root via a `_resolve_repo_root()` helper (or `Path(__file__).resolve().parents[3]` for the package install case).

#### M2. `_NullLifecycleExecutor` returns canned PASS without operator-visible warning

- **File**: `src/superclaude/cli/eval/commands.py:1361-1402`
- **Category**: correctness / code-quality
- **Evidence**: `_NullLifecycleExecutor.observe()` returns `ObservedRun(exit_code=0, ...)`. The docstring at L1364-1372 acknowledges this is a M2/M3 shim and only safe because `real.yaml` tags every spec `no_pty: skip`. But the `--no-pty` flag is operator-supplied; operator can omit `--no-pty` against a suite whose specs lack the tag and see fake passes.
- **Why**: Exactly the class of silent-success bug the FR-G5 coverage gate was built to prevent. When M5/M6 wires the real `ClaudeProcessAdapter + PtyDriver`, anyone who relied on the null executor for tests will see green→red transitions with no clear root cause.
- **Recommendation**: Make `_resolve_executor_factory()` raise `NotImplementedError("M5/M6 PTY executor not yet wired")` when the operator omits `--no-pty` against a suite whose specs are not all `no_pty: skip`. Or have the runner surface a hard ERRORED outcome for any spec that reaches the null executor. At minimum, `logger.warning("null executor in use — this is a M2/M3 shim, not production wiring")` once per process.

#### M3. `session_id` ownership: two source-of-truth docstrings disagree

- **File**: `src/superclaude/cli/eval/commands.py:1442-1446` vs `src/superclaude/cli/eval/isolation.py:42-44`
- **Category**: docs / api-contract
- **Evidence**:
  ```python
  # commands.py:1442-1446
  home = HomeIsolation(
      eval_id=spec.id,
      home_root=home_root,
      session_id=f"sess-{spec.id}",
  )
  ```
  `commands.py:1424-1426` docstring says: "`session_id` is derived from `spec.id` so re-runs of the same eval against the same run-dir are observably the same run to `claude`'s session telemetry (FR-G2)."
  `isolation.py:42-44` docstring says: "Allocation lives in the orchestrator (FR-G2 / T03.16); this record only holds the assigned value."
- **Why**: Two files declare contradictory ownership of session-id allocation. If FR-G2 actually demands per-run uniqueness, `f"sess-{spec.id}"` collides across runs (intentionally, per commands.py) — which is the opposite of what `isolation.py` claims the orchestrator owns.
- **Recommendation**: Pick one model and reconcile both docstrings. If commands.py is correct, delete the "orchestrator allocates" claim in `isolation.py:42-44`. If isolation.py is correct, fix `_run_one_spec` to ask the orchestrator for the session id.

#### M4. `_compute_run_stats` derives `kept`/`skipped` from `EVAL_STATUSES` but hardcodes per-status literals for `RunTotals`

- **File**: `src/superclaude/cli/eval/commands.py:1496-1522`
- **Category**: correctness / maintenance
- **Evidence**:
  ```python
  # RunCounts: SoT-derived
  skipped_statuses = frozenset({"SKIPPED", "INTERRUPTED"})
  kept_statuses = frozenset(EVAL_STATUSES) - skipped_statuses
  ...
  # RunTotals: hardcoded literals
  totals = RunTotals(
      passed=sum(1 for o in outcomes if o.status in {"PASS", "XFAIL"}),
      failed=sum(1 for o in outcomes if o.status in {"FAIL", "XPASS"}),
      ...
  )
  ```
- **Why**: Asymmetric: `RunCounts` is SoT-derived, `RunTotals` is not. Adding a new `EvalStatus` value (`ABORTED`, `FLAKY`) silently drops it from `RunTotals` totals while flowing correctly into `RunCounts`. The reason for the asymmetric handling is not explained.
- **Recommendation**: Drop SoT-derivation in `RunCounts` (matching `RunTotals`) OR extend it to `RunTotals` via a status→bucket mapping that fails closed on unknown statuses.

#### M5. `Reporter.write` writes `summary.yaml`; `write_aggregated_report` does not

- **File**: `src/superclaude/cli/eval/reporter.py:190-227` vs `src/superclaude/cli/eval/run_report.py:335-379`
- **Category**: api-contract / coupling
- **Evidence**:
  - `Reporter.write` (`reporter.py:190-227`): writes `summary.md`, `summary.json`, `summary.yaml`; optional `junit.xml`.
  - `write_aggregated_report` (`run_report.py:335-379`): writes `summary.md`, `summary.json`; optional `junit.xml`. **No `summary.yaml`.**
- **Why**: Both methods claim to "write the FR-RPT1 aggregated run report under `output_dir`" in their docstrings. They produce different artifact sets. `write_aggregated_report` is exposed in `__all__` (line 26-37 of `run_report.py`); any caller using the older API silently produces an incomplete artifact set per FR-G4 (which `artifact_layout.py:8` lists `summary.yaml` as part of the layout). Asymmetric helpers like this are a high-signal "one is right, one is wrong" pattern.
- **Recommendation**: Either delete `write_aggregated_report` from the public API (the parallel surface is a foot-gun) or have it write `summary.yaml` via `render_summary_yaml` (already exported from `reporter.py`).

#### M6. `--output-dir` Click `Path` options inconsistent between `eval run` and `eval doctor`

- **File**: `src/superclaude/cli/eval/commands.py:1587` vs `:784`
- **Category**: api-contract / style
- **Evidence**:
  ```python
  # commands.py:1587 (eval run)
  type=click.Path(file_okay=False, path_type=Path),
  # commands.py:784   (eval doctor)
  type=click.Path(path_type=Path),
  ```
- **Why**: `eval run`'s `--output-dir` rejects existing files; `eval doctor`'s does not. Operator behavior diverges silently across the two subcommands. The doctor's help text also references AC12 allowlist resolution — should match the run path semantics.
- **Recommendation**: Pin the doctor's `--output-dir` to the same `click.Path(file_okay=False, path_type=Path)` shape.

### 🟢 Low (nice-to-have)

- **L1**. `commands.py:1297` — header comment says "Eight module-private helpers" but the file defines 11+ (plus 3 exit-code constants). Stale comment.
- **L2**. `commands.py:1815` — `_gates = CapabilityGates(...)` immediately followed by `del _gates` — construction-for-side-effects is fine but obscure. Consider just `CapabilityGates(skip_flags=tuple(skip_flags))` with no assignment, or a brief comment "construction is the wiring; instance unused at M2" (already present at 1815 — actually clear enough — leave as-is). Nit.
- **L3**. `isolation.py:530-533` — `self.home_root.mkdir(parents=True, exist_ok=True)` runs *before* `containment_guard`. If `home_root` is a hostile path, this mkdir is a no-op for absolute paths but still touches the FS before the guard fires. The guard then catches the escape. Document why "mkdir before guard" is safe (it is — `containment_guard` uses `resolve(strict=True)` post-mkdir to catch symlink races).
- **L4**. `coverage.py:185` — `re.sub(r"[^A-Za-z0-9_:.-]", "_", pattern)` does not bound output length. An attacker-controlled `pattern` could produce a >255-char filename that fails at `path.write_text`. Truncate to a fixed cap (e.g. `[:120]`).
- **L5**. `run_report.py:283` — `failures=str(totals.failed + totals.timeout)`; `_compute_run_stats` rolls XPASS into `totals.failed`, so XPASS double-counts into JUnit `failures`. Verify against `tests/cli/eval/test_reporter.py` expected output.
- **L6**. `artifact_layout.py:99` — `_EVAL_ID_RE = re.compile(r"^[A-Za-z0-9_.-]{1,64}$")` duplicates the FR-SCH2 pattern from `loader.py:EVAL_ID_REGEX` / `validate_eval_id`. Two sources of truth for the same regex. (See CC1.)

### 💬 Nits

- `commands.py:1322-1332` — `_new_run_id` is a thin wrapper over `compose_run_id`; the docstring is longer than the body. Acceptable per the test-importability justification, but consider whether the test can import `compose_run_id` directly.
- `claude_process.py:84` imports `ClaudeProcess` from `superclaude.cli.pipeline.process` — *not* a FR-G1 violation (pipeline is a peer module, not core/agents/skills/commands), but verify with the FR-G1 owner that `pipeline` is on the allowed list.

---

## Architectural / Cross-Cutting Observations

### CC1. FR-SCH2 regex duplicated between `artifact_layout.py:99` and `loader.py`

`compose_per_eval_dir` re-implements the FR-SCH2 regex inline instead of calling `loader.validate_eval_id` / `loader.EVAL_ID_REGEX`. The two regex strings are currently identical; a future schema bump that updates one will silently desync. Either delete the layout-side regex and call `validate_eval_id`, or document the duplication with a load-bearing comment.

**Affected files**: `src/superclaude/cli/eval/artifact_layout.py:99`, `src/superclaude/cli/eval/loader.py` (validate_eval_id).

### CC2. Three identical exit-code-2 constants live in three modules (plus four more in commands.py)

- `COVERAGE_GATE_FAILED_EXIT_CODE` (`coverage.py:77`)
- `SCRATCH_ROOT_VIOLATION_EXIT_CODE` (`config.py:113`)
- `REPORTER_CONTRACT_VIOLATION_EXIT_CODE` (`run_report.py:52`)
- Plus `HARD_FAIL_EXIT_CODE`, `SUITE_LOADER_ERROR_EXIT_CODE`, `SUITE_NOT_FOUND_EXIT_CODE`, `EVAL_NOT_FOUND_EXIT_CODE` (`commands.py`)

All seven equal `2`. The design-spec §4 mapping is "every harness-rejection outcome → 2", and each module documents the rationale, but seven copies of the literal `2` makes it easy for a future tweak to change one without the others. Consider a `superclaude.cli.eval.exit_codes` module that centralises all of them. (Note: `RUN_CLEAN_EXIT_CODE`, `RUN_FAILURES_EXIT_CODE`, `RUN_INTERRUPTED_EXIT_CODE` in `commands.py:570-577` are already centralised — extend that pattern.)

**Affected files**: `src/superclaude/cli/eval/{coverage,config,run_report,commands}.py`.

### CC3. `_NullLifecycleExecutor` is silent — no operator-visible signal when M5/M6 wiring is missing

The `_NullLifecycleExecutor + _resolve_executor_factory + _run_one_spec` trio (commands.py:1361-1476) is a shim with M5/M6 production wiring still TBD. Today it relies on every reachable suite tagging `no_pty: skip`, which is correct for `real.yaml` but not enforceable. When M5/M6 lands, swapping `_resolve_executor_factory` to return the real executor requires confidence that no test still relies on the null fall-through. Add `warnings.warn` or a runtime "null executor invoked N times" counter so the eventual swap is observable.

**Affected files**: `src/superclaude/cli/eval/commands.py:1361-1476`.

---

## Test Coverage Gaps

For each gap, the file:line of the untested behavior is given alongside the closest existing test (if any) and what a missing test would assert.

1. **`commands.py:1853` — operator-supplied `--output-dir` flat-layout case (H1)**.
   - Closest existing: `tests/cli/eval/test_eval_run.py:test_output_dir_outside_allowlist_exits_scratch_root_violation` (only tests rejection).
   - Missing: assert `--output-dir <root>` results in artifacts under `<root>/.dev/eval-runs/<date>/<run-id>/per-eval/<eval_id>/`, NOT directly under `<root>/per-eval/<eval_id>/`.

2. **`commands.py:1526` — `_format_run_summary_line` only renders 3 of 6 totals (H3)**.
   - Closest existing: `tests/cli/eval/test_eval_run.py:test_run_verbose_emits_summary_line` (only asserts run-id presence).
   - Missing: assert a summary with `errored=2, timeout=1` surfaces those counts in the verbose line.

3. **`coverage.py:297-300` — parse-failure / OSError trivially-green path (H2)**.
   - Closest existing: `tests/cli/eval/test_coverage_gate.py` (covers happy + missing-file paths).
   - Missing: assert a corrupt `settings.json` (`{` only) yields a non-green `CoverageResult` with a synthetic "unparseable" missing entry, not a green pass.

4. **`commands.py:1735-1737` — `home_root.mkdir` before allowlist extension (H5)**.
   - Closest existing: no test pins the ordering relationship.
   - Missing: patch `Path.mkdir` to fail and assert the failure surfaces *after* `runtime_config` is built, OR refactor to make order explicit and test it.

5. **`config.py:246` — `resolved == prefix` accepts the bare allowlist root (H4)**.
   - Closest existing: `test_accepts_tmp_eval_runs_root_itself` *encodes* the current behavior.
   - Missing: when used as `--output-dir`, this should be rejected (or Reporter should refuse to write directly under the prefix). The current test pins the foot-gun.

6. **`commands.py:1361-1402` — `_NullLifecycleExecutor` returns canned pass (M2)**.
   - Closest existing: no test asserts that a non-`no_pty: skip` spec running through the null executor produces an observable artifact or warning.
   - Missing: load a synthetic suite with no `no_pty:` tags, run end-to-end, assert that stderr carries a "null executor in use" warning or that the outcome is ERRORED rather than PASS.

7. **`commands.py:1442-1446` — `session_id` allocation ownership (M3)**.
   - Closest existing: `tests/cli/eval/test_eval_lifecycle.py` uses fixture-built `HomeIsolation` instances.
   - Missing: pin the contract one way or the other (orchestrator-allocates per `isolation.py:42-44`, OR `f"sess-{spec.id}"` per `commands.py:1424-1426`).

---

## Validation Results (Post-Sprint Validation Axes)

| Axis | Verdict | Evidence |
|---|---|---|
| **FR-G1 ban-import in reporter.py** | ✅ PASS | `reporter.py:51-67` imports only `dataclasses`, `pathlib`, `typing`, `yaml`, `.models`, `.run_report`. Grep across the entire snapshot for `from superclaude\.(core\|agents\|skills\|commands)` returns **zero matches**. Auggie's claim that `reporter.py:8` violates FR-G1 was a hallucination (line 8 is inside a docstring). |
| **FR-G4 artifact layout** | 🟡 PARTIAL | `artifact_layout.py` and `run_report.py` have a clean boundary (no duplicated magic strings). However, **H1** (`--output-dir` bypasses the `<date>/<run-id>/` layout) and **M5** (`write_aggregated_report` omits `summary.yaml`) both violate the FR-G4 contract on specific code paths. |
| **FR-G5 coverage gate** | 🟡 PARTIAL | Happy path is correct: `coverage_gate` rejects under-threshold runs, returns a typed `CoverageResult`, handles `settings.json` absent. **H2** documents the silent-pass-on-corrupt-settings failure path. |
| **FR-ISO2 path containment** | ✅ PASS | `containment_guard` correctly chains `resolve(strict=True)` (catches symlinks) with `resolve_scratch_root` (allowlist) and `is_relative_to` (sub-path). Symlink traversal IS rejected. **L3** documents the `home_root.mkdir-before-guard` order as defense-in-depth-safe (guard catches escapes anyway). |
| **AC12 scratch-root allowlist (commit dce3c3cb)** | ✅ PASS | Tautology fix at `commands.py:1727-1730` removed the `output_dir=requested_output` kwarg from the first-gate call. Default-deny preserved. `test_rejects_non_allowlisted_paths` would fail under regression. **H4** flags that the bare-prefix acceptance pattern (`config.py:246`) is a separate footgun not introduced by dce3c3cb. |
| **eval_run lifecycle (commit e6368db8)** | 🟡 PARTIAL | All 11 helpers present (`_utc_iso_now` L1308, `_new_run_id` L1322, `_default_output_dir` L1335, `_can_install_signal_handler` L1346, `_NullLifecycleExecutor` L1361, `_resolve_executor_factory` L1390, `_run_one_spec` L1405, `_compute_run_stats` L1477, `_format_run_summary_line` L1526, plus `_format_coverage_summary` L621, `_format_coverage_missing_roster` L636) and 3 exit-code constants (`RUN_CLEAN_EXIT_CODE` L570, `RUN_FAILURES_EXIT_CODE` L573, `RUN_INTERRUPTED_EXIT_CODE` L577). Mostly defensible, but several have documented issues (**H1, H3, M1, M2, M3, M4**). |
| **Residual tech debt (commits 08183738, e6368db8, dce3c3cb)** | ✅ PASS | Verified live: `uv run ruff check src/superclaude/cli/eval/ --select F401,F821` → **all checks passed**. Grep for `mix_stderr` across src/ + tests/ → **zero matches**. Grep for `T04.09` → only test docstrings as historical context (`tests/cli/eval/test_eval_group.py:1,3,30,40`). Grep for `shell=True` → none. Grep for `tempfile.mktemp` → none. Grep for `yaml.load\|unsafe_load\|full_load` → none. |

---

## Audit

- **Auggie chunks**: 4 (succeeded: 4, retried: 0, skipped: 0)
  - `auggie-raw-main.json` — 20 findings + 6 cross-cutting
  - `auggie-raw-security.json` — 15 findings
  - `auggie-raw-architect.json` — 4 meta-findings (mostly clean verdicts) + 10 cross-cutting
  - `auggie-raw-qa.json` — 12 missing-test findings + 8 cross-cutting
- **Claude-side cross-check**: 1 pass (`auggie-reviewer` agent → `claude-side-review.md`)
- **Findings dropped during grounding**: 30
  - 20 Auggie findings cited non-existent functions or docstring lines (e.g., `isolation.py:156 _resolve_workspace_path` — function doesn't exist; `reporter.py:8 imports superclaude.core` — line is inside a docstring; `hook_adapter.py:80,89 shell injection` — lines are enum docstrings; `claude_process.py:120 verify no shell=True` — `shell=True` not present anywhere; `tempfile.mktemp` — not used).
  - 6 architect "meta-findings" rephrased as positive verdicts (FR-G1 CLEAN, layering CLEAN, etc.) — folded into Validation Results, not retained as findings.
  - 4 low-signal "missing X" findings on hypothetical concerns (memory limits, exponential backoff) where the design intentionally doesn't enforce that policy.
- **Persona cross-check**: Enabled (deep depth). 5 of 17 retained findings (H1, H2, H3, H4, H5) were claude-only; 0 were auggie-only with high signal; the rest were cross-cutting observations and test-coverage gaps surfaced primarily by claude-side.
- **Hallucination rate**: ~64% of raw Auggie findings (30/47) failed file:line grounding. The `auggie-reviewer` cross-check was essential.
- **Token cost (estimated)**: Auggie ≈ 80k tokens (4 calls × 24-turn deep mode); Claude ≈ 18k tokens (orchestration + grounding + synthesis).
- **Duration**: ~12 minutes wall clock.

<!-- SC:AUGGIE-REVIEW:SUMMARY
status: success
critical: 0 high: 5 medium: 6 low: 6 nit: 2
dropped: 30
auggie_chunks: 4
duration_sec: 720
-->
