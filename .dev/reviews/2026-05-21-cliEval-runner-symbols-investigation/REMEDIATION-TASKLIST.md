# REMEDIATION TASKLIST — cliEval Runner Symbols (D1-final)

**Source design:** `.dev/reviews/2026-05-21-cliEval-runner-symbols-investigation/phase2B-final-design.md`
**Verdict:** HYBRID T1+T3 @ 0.86 (C1 minimum in-place, post-Phase-2B refactors)
**Date:** 2026-05-21
**Scope:** 14 atomic tasks in dependency order. All land in a single feature-branch PR; the F401+F821 ruff gate clears only when all 14 land together.

---

## T01: Add `RUN_*_EXIT_CODE` module-level constants

- **File:** `src/superclaude/cli/eval/commands.py`
- **Location:** between `commands.py:1289` (end of `RUN_BODY_DEFERRED_EXIT_CODE` block) and `commands.py:1291` (start of `RUN_BODY_DEFERRED_MESSAGE`). Group as a single block with a comment citing `design-spec.md:202-209`.
- **Diff sketch:**
    ```python
    # Design-spec §4 (lines 202-209): the three terminal eval-run exit codes.
    # Pinned values 0/1/3 per design-spec. Convention mirrors the eight
    # existing *_EXIT_CODE constants. HARD_FAIL_EXIT_CODE = 2 (line 550)
    # remains the harness-error code; the three constants below own the
    # 0 / 1 / 3 surface.
    RUN_CLEAN_EXIT_CODE: int = 0
    RUN_FAILURES_EXIT_CODE: int = 1
    RUN_INTERRUPTED_EXIT_CODE: int = 3
    ```
- **AC:** `python -c "from superclaude.cli.eval import commands; assert commands.RUN_CLEAN_EXIT_CODE == 0 and commands.RUN_FAILURES_EXIT_CODE == 1 and commands.RUN_INTERRUPTED_EXIT_CODE == 3"`
- **Verification:** `uv run ruff check src/superclaude/cli/eval/commands.py --select F821 2>&1 | grep -E "RUN_(CLEAN|FAILURES|INTERRUPTED)_EXIT_CODE" | wc -l` returns 0 (those three F821s cleared).
- **Estimated LOC:** +9 (3 constants × 3 lines incl. comment).
- **Dependencies:** none (first task).

---

## T02: Add `_utc_iso_now` helper

- **File:** `src/superclaude/cli/eval/commands.py`
- **Location:** after the T01 constants block.
- **Diff sketch:**
    ```python
    def _utc_iso_now() -> str:
        """Return the current UTC instant as ISO-8601 with Z suffix.

        Format matches the shape `artifact_layout._parse_iso` (line 107)
        accepts, so a generated timestamp round-trips through
        `compose_run_id` / `compose_run_dir` without loss.
        """
        return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    ```
- **AC:** `python -c "from superclaude.cli.eval import commands; s = commands._utc_iso_now(); assert s.endswith('Z') and 'T' in s"`
- **Verification:** ruff `_utc_iso_now` F821 cleared at lines 1612, 1636 (will still fire until T13 lands import unused-import cleanup).
- **Estimated LOC:** +5 (signature + docstring + body).
- **Dependencies:** none.

---

## T03: Add `_can_install_signal_handler` helper

- **File:** `src/superclaude/cli/eval/commands.py`
- **Location:** after T02.
- **Diff sketch:**
    ```python
    def _can_install_signal_handler() -> bool:
        """Return True iff SignalHandlerInstaller.install() will not raise.

        Mirrors the invariant at `signal_handler.py:203-206`: install()
        raises ValueError unless current_thread() is main_thread().
        """
        return threading.current_thread() is threading.main_thread()
    ```
- **AC:** `python -c "from superclaude.cli.eval import commands; assert commands._can_install_signal_handler() is True"` (true in the main interpreter thread).
- **Verification:** ruff `_can_install_signal_handler` F821 cleared at line 1624.
- **Estimated LOC:** +5.
- **Dependencies:** T13 must add `import threading` to the import block.

---

## T04: Add `_new_run_id` wrapper

- **File:** `src/superclaude/cli/eval/commands.py`
- **Location:** after T03.
- **Diff sketch:**
    ```python
    def _new_run_id(started_iso: str, suite_name: str) -> str:
        """Wrapper around `artifact_layout.compose_run_id` (line 139).

        Two-arg signature matches `compose_run_id(started_at, suite_name)`
        byte-for-byte; the wrapper exists so tests can mock-patch
        `commands._new_run_id` without affecting `compose_run_id`'s other
        consumers (e.g., `test_artifact_reproducibility.py:67`).
        """
        return compose_run_id(started_iso, suite_name)
    ```
- **AC:** `python -c "from superclaude.cli.eval import commands; assert commands._new_run_id('2026-05-21T10:00:00Z', 'real') == commands._new_run_id('2026-05-21T10:00:00Z', 'real')"` (determinism).
- **Verification:** ruff `_new_run_id` F821 cleared at line 1467 (after T13 updates the call site signature).
- **Estimated LOC:** +6.
- **Dependencies:** T13 must add `compose_run_id` to the `.artifact_layout` import.

---

## T05: Add `_default_output_dir` wrapper

- **File:** `src/superclaude/cli/eval/commands.py`
- **Location:** after T04.
- **Diff sketch:**
    ```python
    def _default_output_dir(started_iso: str, suite_name: str) -> Path:
        """Return the canonical AC12-aligned default run directory.

        Composes `<cwd>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/` via
        `artifact_layout.compose_run_dir` (line 162). The AC12 allowlist
        check at commands.py:1473 is the single enforcement gate; this
        wrapper only constructs a candidate path.
        """
        return compose_run_dir(Path.cwd(), started_iso, suite_name)
    ```
- **AC:** `python -c "from superclaude.cli.eval import commands; from pathlib import Path; p = commands._default_output_dir('2026-05-21T10:00:00Z', 'real'); assert '.dev/eval-runs' in str(p)"`
- **Verification:** ruff `_default_output_dir` F821 cleared at line 1469.
- **Estimated LOC:** +6.
- **Dependencies:** T13 must add `compose_run_dir` to the `.artifact_layout` import.

---

## T06: Add `ExecutorFactory` type alias + `_resolve_executor_factory`

- **File:** `src/superclaude/cli/eval/commands.py`
- **Location:** after T05. The type alias goes immediately after the T01 constants block (so it is in scope for use in T07's `_run_one_spec` signature). The function goes after T05.
- **Diff sketch (type alias, near T01):**
    ```python
    ExecutorFactory = type[LifecycleExecutor]
    ```
- **Diff sketch (function, after T05):**
    ```python
    def _resolve_executor_factory() -> ExecutorFactory:
        """Return the executor constructor used per-spec.

        Production path returns `ClaudeProcessAdapter` (the type itself,
        not an instance). `_run_one_spec` invokes the returned type with
        full per-eval kwargs (home, prompt, output_file, error_file).
        Tests can monkeypatch this to substitute a stub LifecycleExecutor.
        """
        return ClaudeProcessAdapter
    ```
- **AC:** `python -c "from superclaude.cli.eval import commands; from superclaude.cli.eval.claude_process import ClaudeProcessAdapter; assert commands._resolve_executor_factory() is ClaudeProcessAdapter"`
- **Verification:** ruff `_resolve_executor_factory` F821 cleared at line 1577.
- **Estimated LOC:** +9 (alias + signature + docstring + body).
- **Dependencies:** T13 must add `ClaudeProcessAdapter` to imports.

---

## T07: Add `_run_one_spec` orchestration helper

- **File:** `src/superclaude/cli/eval/commands.py`
- **Location:** after T06.
- **Diff sketch (~30 LOC):**
    ```python
    def _run_one_spec(
        spec: EvalSpec,
        *,
        run_dir: Path,
        home_root: Path,
        config: EvalConfig,
        timeout_mult: float,
        keep_home: bool,
        cancellation_token: CancellationToken,
        executor_factory: ExecutorFactory,
    ) -> EvalOutcome:
        """Orchestrate one spec end-to-end: HOME setup → runner → outcome.

        Maps HomeContainmentViolation to an ERRORED EvalOutcome per
        D-0048 status-mapping rules; every other exception propagates so
        RunOrchestrator's _errored_outcome catches it.
        """
        paths = allocate_per_eval_paths(run_dir, spec.id)
        home = HomeIsolation(
            eval_id=spec.id,
            home_root=home_root / spec.id,
            session_id=secrets.token_hex(8),
        )
        try:
            home.setup(config=config)
            executor = executor_factory(
                home=home,
                prompt=spec.prompt,
                output_file=paths.eval_dir / "stdout.log",
                error_file=paths.eval_dir / "stderr.log",
            )
            runner = EvalRunner(
                home=home,
                config=config,
                executor=executor,
                run_dir=paths.eval_dir,
                artifacts_dir=paths.artifacts_dir,
                stdout_path=paths.eval_dir / "stdout.log",
                stderr_path=paths.eval_dir / "stderr.log",
                transcript_path=paths.tty_transcript,
                expect_callables=spec.compiled_expects,
                keep_home_on_pass=keep_home,
                default_timeout_sec=(spec.timeout_sec or 0) * timeout_mult,
                cancellation_token=cancellation_token,
            )
            return runner.run(spec)
        except HomeContainmentViolation as exc:
            return EvalOutcome(
                eval_id=spec.id,
                title=spec.title,
                status="ERRORED",
                duration_sec=0.0,
                expects=(),
                error_class="HomeContainmentViolation",
            )
    ```
- **AC:** `python -c "from superclaude.cli.eval import commands; assert callable(commands._run_one_spec)"`. Test contract: the patch path `superclaude.cli.eval.commands._run_one_spec` resolves to a module attribute (verified by 5 existing test files via `hasattr`).
- **Verification:** ruff `_run_one_spec` F821 cleared at line 1598.
- **Estimated LOC:** +30.
- **Dependencies:** T13 must add `allocate_per_eval_paths`, `HomeContainmentViolation`, `HomeIsolation`, `EvalRunner` to imports. `secrets` stays in imports (consumed here).

---

## T08: Add `_compute_run_stats` aggregator

- **File:** `src/superclaude/cli/eval/commands.py`
- **Location:** after T07.
- **Diff sketch:**
    ```python
    def _compute_run_stats(
        outcomes: Sequence[EvalOutcome],
        *,
        manifest_n: int,
    ) -> tuple[RunCounts, RunTotals]:
        """Aggregate outcomes into DM-012 RunCounts + RunTotals.

        kept_plus_skipped_equals_n_prime is DERIVED, not hardcoded — the
        boolean tracks the arithmetic so RunSummary.__post_init__ at
        models.py:896-912 never raises on internally-consistent counts.
        """
        from collections import Counter
        counter = Counter(o.status for o in outcomes)
        kept_k = sum(counter[s] for s in ("PASS", "FAIL", "ERRORED", "TIMEOUT", "XFAIL", "XPASS"))
        skipped_s = sum(counter[s] for s in ("SKIPPED", "INTERRUPTED"))
        expanded_n_prime = len(outcomes)
        counts = RunCounts(
            manifest_n=manifest_n,
            expanded_n_prime=expanded_n_prime,
            kept_k=kept_k,
            skipped_s=skipped_s,
            kept_plus_skipped_equals_n_prime=(kept_k + skipped_s == expanded_n_prime),
        )
        totals = RunTotals(
            passed=counter["PASS"] + counter["XFAIL"],
            failed=counter["FAIL"] + counter["XPASS"],
            skipped=counter["SKIPPED"],
            errored=counter["ERRORED"],
            interrupted=counter["INTERRUPTED"],
            timeout=counter["TIMEOUT"],
        )
        return counts, totals
    ```
- **AC:** `python -c "from superclaude.cli.eval import commands; c, t = commands._compute_run_stats((), manifest_n=0); assert c.expanded_n_prime == 0 and c.kept_plus_skipped_equals_n_prime is True"`
- **Verification:** ruff `_compute_run_stats` F821 cleared at line 1642. `Sequence`, `RunCounts`, `RunTotals` consumed.
- **Estimated LOC:** +25.
- **Dependencies:** T13 must keep `Sequence` in `typing` import; `RunCounts` + `RunTotals` already imported.

---

## T09: Add `_format_run_summary_line` helper

- **File:** `src/superclaude/cli/eval/commands.py`
- **Location:** after T08.
- **Diff sketch:**
    ```python
    def _format_run_summary_line(summary: RunSummary, output_dir: Path) -> str:
        """One-line operator-stdout banner for --verbose mode."""
        t = summary.totals
        return (
            f"eval run {summary.run_id}: "
            f"passed={t.passed} failed={t.failed} skipped={t.skipped} "
            f"errored={t.errored} timeout={t.timeout} "
            f"duration={summary.duration_sec:.2f}s → {output_dir}"
        )
    ```
- **AC:** `python -c "from superclaude.cli.eval import commands; assert callable(commands._format_run_summary_line)"`
- **Verification:** ruff `_format_run_summary_line` F821 cleared at line 1671.
- **Estimated LOC:** +8.
- **Dependencies:** none beyond `RunSummary` already imported.

---

## T10: Hoist `started_iso` computation + update call sites for `_new_run_id` and `_default_output_dir`

- **File:** `src/superclaude/cli/eval/commands.py`
- **Location:** in `eval_run` body around lines 1466-1612.
- **Diff sketch:**
    ```python
    # At line 1466 (immediately after `base_config = EvalConfig()`):
    + started_iso = _utc_iso_now()
    # At line 1467, change:
    -    run_id = _new_run_id()
    +    run_id = _new_run_id(started_iso, suite)
    # At line 1469, change:
    -        output_dir if output_dir is not None else _default_output_dir(run_id)
    +        output_dir if output_dir is not None else _default_output_dir(started_iso, suite)
    # At line 1612, delete:
    -    started_iso = _utc_iso_now()
    ```
- **AC:** `started_iso` is in scope at line 1651 (its only downstream consumer in `RunSummary(...started_at=started_iso, ...)`).
- **Verification:** `grep -n "started_iso" src/superclaude/cli/eval/commands.py` shows one definition (line 1466) and one consumer (line 1651). `_utc_iso_now()` still called at line 1636 for `finished_iso`.
- **Estimated LOC:** +1 / -1 / 2 edits = net 0 LOC change.
- **Dependencies:** T02 (`_utc_iso_now`), T04 (`_new_run_id`), T05 (`_default_output_dir`).

---

## T11: Update Click 8.3.2 `mix_stderr` regression

- **File:** `tests/cli/eval/test_eval_group.py`
- **Location:** line 114.
- **Diff sketch:**
    ```python
    -    runner = CliRunner(mix_stderr=False)
    +    runner = CliRunner()
    ```
- **AC:** `result.stderr` access at line 117 still works (Click 8.3.2 retains the attribute; only the `mix_stderr` kwarg was removed — confirmed via `uv run python -c "from click.testing import CliRunner; help(CliRunner.__init__)"`).
- **Verification:** `uv run pytest tests/cli/eval/test_eval_group.py::test_run_skeleton_emits_deferral_notice_on_stderr -v` exits 0.
- **Estimated LOC:** 1 line edited.
- **Dependencies:** none.

---

## T12: Author `tests/cli/eval/test_eval_run.py`

- **File:** `tests/cli/eval/test_eval_run.py` (NEW)
- **Diff sketch (~45 LOC):**
    ```python
    """E2E tests for `superclaude eval run` body (T04.10 deliverable)."""
    from pathlib import Path
    from unittest.mock import patch
    import pytest
    from click.testing import CliRunner
    from superclaude.cli.eval.commands import eval_group
    from superclaude.cli.eval.models import EvalOutcome

    REAL_SUITE = Path("src/superclaude/cli/eval/suites/real.yaml")

    def _stub_pass(spec, **_): return EvalOutcome(eval_id=spec.id, title=spec.title, status="PASS", duration_sec=0.0, expects=())
    def _stub_fail(spec, **_): return EvalOutcome(eval_id=spec.id, title=spec.title, status="FAIL", duration_sec=0.0, expects=())

    def test_eval_run_help_renders_all_flags():
        result = CliRunner().invoke(eval_group, ["run", "--help"])
        assert result.exit_code == 0
        for flag in ("--suite", "--parallel", "--eval", "--no-mcp", "--no-pty", "--output-dir", "--keep-home", "--timeout-mult", "--max-disk-mb", "--json", "--verbose", "--junit"):
            assert flag in result.output

    def test_eval_run_clamp_parallel_low(tmp_path):
        with patch("superclaude.cli.eval.commands._run_one_spec", side_effect=_stub_pass):
            r = CliRunner().invoke(eval_group, ["run", "--suite", "real", "--parallel", "0", "--output-dir", str(tmp_path / "out")])
            assert r.exit_code in (0, 1)  # clamped to 1, runs normally

    def test_eval_run_exit_0_on_all_pass(tmp_path):
        with patch("superclaude.cli.eval.commands._run_one_spec", side_effect=_stub_pass):
            r = CliRunner().invoke(eval_group, ["run", "--suite", "real", "--output-dir", str(tmp_path / "out")])
            assert r.exit_code == 0

    def test_eval_run_exit_1_on_failures(tmp_path):
        with patch("superclaude.cli.eval.commands._run_one_spec", side_effect=_stub_fail):
            r = CliRunner().invoke(eval_group, ["run", "--suite", "real", "--output-dir", str(tmp_path / "out")])
            assert r.exit_code == 1

    def test_eval_run_exit_3_on_cancellation(tmp_path):
        from superclaude.cli.eval import commands as cmds
        with patch.object(cmds.CancellationToken, "is_cancelled", lambda self: True), \
             patch("superclaude.cli.eval.commands._run_one_spec", side_effect=_stub_pass):
            r = CliRunner().invoke(eval_group, ["run", "--suite", "real", "--output-dir", str(tmp_path / "out")])
            assert r.exit_code == 3

    def test_eval_run_timeout_mult_invalid_exits_2():
        r = CliRunner().invoke(eval_group, ["run", "--suite", "real", "--timeout-mult", "0"])
        assert r.exit_code == 2
    ```
- **AC:** `uv run pytest tests/cli/eval/test_eval_run.py -v` exits 0 with 6 passing tests.
- **Verification:** All 6 test functions PASS.
- **Estimated LOC:** ~45.
- **Dependencies:** T01-T10 (the helpers all need to resolve).

---

## T13: Update import block + clear F401 cluster

- **File:** `src/superclaude/cli/eval/commands.py`
- **Location:** lines 30-88 (the import block).
- **Diff sketch:**
    ```python
    # Drop line 31:
    - import os

    # Add after line 36 (import sys):
    + import threading

    # Add new import line, alphabetically placed before .capabilities:
    + from .artifact_layout import (
    +     allocate_per_eval_paths,
    +     compose_run_dir,
    +     compose_run_id,
    + )

    # Add new import line, after .capabilities:
    + from .claude_process import ClaudeProcessAdapter
    ```
- **KEEP UNCHANGED:**
  - `import secrets` (consumed by T07's `secrets.token_hex(8)`)
  - `from datetime import datetime, timezone` (consumed by T02)
  - `from typing import ..., Sequence` (consumed by T08's `Sequence[EvalOutcome]`)
  - `from .isolation import HomeContainmentViolation, HomeIsolation` (consumed by T07)
  - `from .models import EvalOutcome, EvalSpec, RunCounts, RunSummary, RunTotals` (consumed)
  - `from .runner import EvalRunner, LifecycleExecutor` (consumed by T07 + T06)
- **AC:** `uv run ruff check src/superclaude/cli/eval/commands.py --select F401,F821 2>&1 | grep -E "error|warning" | wc -l` returns 0.
- **Verification:** ruff exit 0 on commands.py.
- **Estimated LOC:** -1 line (`import os`), +1 line (`import threading`), +5 lines (artifact_layout block), +1 line (claude_process). Net +6.
- **Dependencies:** T01-T09 must all be on disk (the imports they consume).

---

## T13a: Triage un-skipped failures

- **File:** (verification only — no source-tree edits)
- **Action:** After T13 lands, run `uv run pytest tests/cli/eval/ -v --tb=short > .dev/reviews/2026-05-21-cliEval-runner-symbols-investigation/artifacts/pytest-post-D1final.log 2>&1`. Triage the output:
  - **Blockers** (must fix before sprint exit): any test that exercises code touched by T01-T13 and FAILs.
  - **Carry-forward** (Phase 5 follow-up): any test that was previously SKIPPED via `hasattr` gate and now FAILs due to pre-existing logic bugs unrelated to D1-final.
- **AC:** Triage document written to `.dev/reviews/2026-05-21-cliEval-runner-symbols-investigation/artifacts/triage-post-D1final.md` listing each FAIL with classification (blocker vs. carry-forward).
- **Verification:** Document exists; blockers = 0 (or each blocker has an open follow-up task).
- **Estimated LOC:** 0 source; ~20 lines of triage doc.
- **Dependencies:** T13 complete.

---

## T14-2: Ruff gate

- **Action:** `uv run ruff check src/superclaude/cli/eval/`
- **AC:** Exit 0.
- **Verification:** Same as AC.
- **Dependencies:** T01-T13.

## T14-1: Pytest gate

- **Action:** `uv run pytest tests/cli/eval/ -v`
- **AC:** 0 unexpected failures (skips are allowed if classified in T13a as carry-forward).
- **Verification:** Compare against baseline (`evidence/T04.22/pytest-baseline.log` or equivalent). New PASSES = currently-SKIP tests un-skipping; no new FAILs in D1-final-touched code.
- **Dependencies:** T01-T13a.

## T14: Capture per-eval determinism evidence (Phase 5 carry-forward precondition)

- **Action:** `for eval in E1 E2.1 E2.2 E2.3 E3 E4 E5 E6 E7 E8 E9 E10 E11 E12 E13 E14 E15; do for i in 1 2 3; do uv run superclaude eval run --suite real --eval $eval --output-dir /tmp/det-$eval-$i > evidence/T05.02/run-${eval}-green-${i}.log 2>&1; done; done`
- **AC:** All 45 invocations exit cleanly; `EvalOutcome.status` is identical across each per-eval triple.
- **Verification:** Save logs under `evidence/T05.02/`; write a summary comparing the per-eval status triples.
- **Estimated LOC:** 0 source; evidence-only.
- **Dependencies:** T14-1, T14-2.
- **Scope note:** This is the Phase 5 carry-forward measurement; C1 unblocks it but does not perform it. The remediation tasklist owns the precondition (T01-T13a) and prescribes the measurement; the actual capture is operator work after the PR lands.

---

## Carry-forward (out of scope for THIS tasklist)

The following items are explicitly NOT blockers for the D1-final sprint exit; they should be filed as follow-up tasks:

| Item | Source | Why deferred |
|---|---|---|
| **D-0070 / D-0071 / D-0072 / D-0077 artifact-triplet authoring** | `CP-P04-END.md` doc-gap rows | Spec-artifact gaps unrelated to runtime symbols; can be authored after D1-final lands. |
| **OQ-2 sign-off in decisions.md** | `CP-P05-END.md:438-441` step 4 | Requires RyanW; not a code change. File as `TASK-RF-...-oq2-signoff.md`. |
| **C2/C6 sibling-promotion refactor** | D2 §10 final recommendation; D1 §2 Q-RESV-1 trade-off | Lifting `_compute_run_stats` to `RunCounts.from_outcomes` classmethods is a cohesion improvement worth doing at v2; not under deadline pressure for the current sprint exit. File as `TASK-RF-...-aggregator-promotion-v2.md`. |
| **Per-eval determinism captures (E1..E15 × 3 runs)** | `CP-P05-END.md` step 2 | T14 prescribes; the captures themselves are Phase 5 operator work after D1-final lands. |
| **NFR-PERF3 parallel-8 < 600s measurement** | `CP-P05-END.md` step 3 | Same — Phase 5 measurement after D1-final unblocks the runner. |
| **`tests/cli/eval/test_run_helper_surface.py` smoke** | D1 §8 R1 mitigation | Optional 12th-task hardening (`hasattr` smoke for all 11 names). C1 deferred as out-of-scope refinement; can be added as a follow-up if the mock-patch resolution drift becomes a concern. |
| **`OQ-B1.1` resolution** (exact F401 count discrepancy in Phase 1) | B1 §5 | Already resolved by the live ruff probe — see ATK-5 verdict (only `os` is dropped; `secrets` + `Sequence` stay). No follow-up needed beyond updating the open question's status in the verdict doc. |

---

## Dependency graph (ASCII)

```
T01 (constants) ─────────┐
T02 (_utc_iso_now) ──┐   │
T03 (_can_install) ──┤   │
T04 (_new_run_id) ───┤   │   ← deps on T02 in spirit (signature uses started_iso str)
T05 (_default_outdir)┤   │
T06 (factory + alias)┤   │   ← alias placed near T01 constants
T07 (_run_one_spec) ─┤   │   ← deps on T06 (uses ExecutorFactory + executor_factory)
T08 (compute_stats) ─┤   │
T09 (format_line) ───┤   │
                     ▼   ▼
T10 (call-site edits + started_iso hoist)   ← deps on T02, T04, T05
                     │
                     ▼
T13 (import block update + F401 clear)      ← deps on T01-T09 (consumers must exist first)
                     │
                     ▼
T11 (test_eval_group.py mix_stderr fix)     ← independent of T01-T13 but must land in same PR
                     │
                     ▼
T12 (new test_eval_run.py)                  ← deps on T01-T10 (imports/probes the helpers)
                     │
                     ▼
T13a (triage un-skipped failures)
                     │
                     ▼
T14-2 (ruff gate) → T14-1 (pytest gate) → T14 (determinism captures)
```

**Wall-clock estimate:** ~3-4 hours focused implementation + ~1 hour verification = ~5 hours total. Fits inside a single sprint slot.

---

## Final sprint-exit verification command sequence

```bash
# 1. Ruff
uv run ruff check src/superclaude/cli/eval/   # expect exit 0

# 2. Eval test suite
uv run pytest tests/cli/eval/ -v               # expect 0 unexpected failures

# 3. Triage doc exists
test -f .dev/reviews/2026-05-21-cliEval-runner-symbols-investigation/artifacts/triage-post-D1final.md

# 4. Determinism captures (Phase 5)
ls evidence/T05.02/run-E*-green-*.log | wc -l  # expect 45 (15 evals × 3 runs)
```

When all 4 commands pass, sprint exit gates for cliEval P4/P5 (CP-P04-END + CP-P05-END) are SATISFIED for the C1/D1-final scope.
