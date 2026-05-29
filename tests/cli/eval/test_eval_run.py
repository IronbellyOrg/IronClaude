"""FR-CLI1 ``eval run`` Click command acceptance tests (T04.10 / D-0072).

T04.10 wires the twelve FR-CLI1 flags
(``--suite, --parallel, --eval, --no-mcp, --no-pty, --output-dir,
``--keep-home, --timeout-mult, --max-disk-mb, --json, --verbose, --junit``)
into the :class:`RunOrchestrator` + :class:`CapabilityGates` +
:class:`Reporter` + :class:`DiskBudgetPoller` stack. These tests pin
the four acceptance bullets from the phase-4 tasklist:

1. ``superclaude eval run --help`` lists all 12 flags named in FR-CLI1.
2. Per-flag validation:
   * ``--parallel 0`` clamps to 1; ``--parallel 16`` clamps to 15
     (design-spec §11 / RunOrchestrator.{MIN,MAX}_PARALLEL).
   * ``--timeout-mult <= 0`` → exit 2 (HARD_FAIL).
   * ``--max-disk-mb < 0`` → exit 2 (HARD_FAIL).
   * ``--output-dir`` outside the AC12 / OPS-002 scratch-root allowlist
     → exit 2 (SCRATCH_ROOT_VIOLATION).
   * ``--suite`` that does not resolve → exit 2 (SuiteNotFound).
   * ``--eval`` id missing from the suite → exit 2 (EvalNotFound).
3. A one-eval run completes end-to-end with ``--suite real --eval E1``;
   under ``--no-pty`` the DOC-OQ3 ``no_pty: skip`` tag short-circuits the
   spec to SKIPPED + skip_reason ``--no-pty`` and the run exits 0 with
   ``summary.{md,json}`` on disk.
4. ``D-0072/spec.md`` documents flag wiring — pinned by the artifact-
   existence guard in :func:`test_d0072_spec_documents_flag_wiring`.

Parallel clamping is observed by monkeypatching :class:`RunOrchestrator`
so the worker concurrency the command passes through is captured
verbatim without running a real orchestrator. The end-to-end test uses
the real orchestrator + the ``real`` suite + ``--no-pty`` so every
worker dispatch goes through the documented short-circuit path; no
PTY harness is required.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from click.testing import CliRunner

from superclaude.cli.eval import commands as commands_module
from superclaude.cli.eval.commands import (
    EVAL_NOT_FOUND_EXIT_CODE,
    HARD_FAIL_EXIT_CODE,
    RUN_CLEAN_EXIT_CODE,
    SCRATCH_ROOT_VIOLATION_EXIT_CODE,
    SUITE_NOT_FOUND_EXIT_CODE,
    eval_group,
)
from superclaude.cli.eval.orchestrator import RunOrchestrator
from superclaude.cli.eval.suites import SCHEMA_PATH

REAL_SUITE_PATH: Path = SCHEMA_PATH.parent / "real.yaml"
"""On-disk location of the ``real`` suite manifest (T04.16 / DOC-OQ3)."""


def _find_run_dir(output_root: Path) -> Path:
    """Return the FR-G4 run-dir composed under ``output_root``.

    Post-H1 ``--output-dir`` is the OUTPUT ROOT — artifacts land at
    ``<output_root>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/`` via
    ``compose_run_dir``. The exact run-id is timestamp-derived so the
    test resolves it by globbing rather than hard-coding.
    """
    eval_runs_root = output_root / ".dev" / "eval-runs"
    assert eval_runs_root.is_dir(), (
        f"FR-G4 layout root missing: {eval_runs_root} (post-H1, "
        f"--output-dir is the OUTPUT ROOT, not the run-dir)"
    )
    date_dirs = sorted(p for p in eval_runs_root.iterdir() if p.is_dir())
    assert len(date_dirs) == 1, (
        f"Expected exactly one date-stamped dir under {eval_runs_root}, "
        f"found {[p.name for p in date_dirs]}"
    )
    run_dirs = sorted(p for p in date_dirs[0].iterdir() if p.is_dir())
    assert len(run_dirs) == 1, (
        f"Expected exactly one run-id dir under {date_dirs[0]}, "
        f"found {[p.name for p in run_dirs]}"
    )
    return run_dirs[0]


EXPECTED_FLAGS: tuple[str, ...] = (
    "--suite",
    "--parallel",
    "--eval",
    "--no-mcp",
    "--no-pty",
    "--output-dir",
    "--keep-home",
    "--timeout-mult",
    "--max-disk-mb",
    "--json",
    "--verbose",
    "--junit",
)
"""The twelve FR-CLI1 flags T04.10 MUST register on the ``run`` command."""


D0072_SPEC_PATH: Path = (
    Path(__file__).resolve().parents[3]
    / ".dev"
    / "releases"
    / "current"
    / "cliEval"
    / "artifacts"
    / "D-0072"
    / "spec.md"
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@pytest.fixture
def clean_claude_home(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    """Redirect ``Path.home()`` to ``tmp_path`` so the coverage gate is empty.

    The FR-G5 coverage gate inside :func:`eval_run` reads
    ``~/.claude/settings.json`` BEFORE worker dispatch. On a dev host with
    matchers like ``mcp__auggie__.*`` the gate would fail because the
    ``real`` suite's E1 has no inputs yet (T05.02 is deferred), so no
    eval covers any matcher. Pointing ``$HOME`` at an empty directory
    makes the gate treat the matcher set as empty, which always passes.
    """
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    return tmp_path


# ---------------------------------------------------------------------------
# AC bullet 1 — `superclaude eval run --help` lists all 12 flags
# ---------------------------------------------------------------------------


def test_eval_run_help_lists_all_twelve_flags() -> None:
    """Every FR-CLI1 flag appears in ``eval run --help`` output."""

    runner = CliRunner()
    result = runner.invoke(eval_group, ["run", "--help"])
    assert result.exit_code == 0, result.output
    missing = [flag for flag in EXPECTED_FLAGS if flag not in result.output]
    assert not missing, f"FR-CLI1: --help missing {missing!r}; got:\n{result.output}"


def test_eval_run_help_documents_clamping_band() -> None:
    """``--help`` quotes the design-spec §11 clamping band so operators
    learn the policy without spelunking source."""
    runner = CliRunner()
    result = runner.invoke(eval_group, ["run", "--help"])
    assert result.exit_code == 0
    assert "clamp to 1" in result.output
    assert "clamp to 15" in result.output


# ---------------------------------------------------------------------------
# AC bullet 2 — per-flag validation
# ---------------------------------------------------------------------------


class _RecordingOrchestrator:
    """Capture the ``parallel`` kwarg without invoking a real workpool.

    The Click command instantiates a real :class:`RunOrchestrator`
    *before* the worker closure fires; by monkeypatching the class on
    the commands module we intercept the ``parallel=`` value at the call
    site documented in design-spec §11 (the clamp lives in
    :func:`eval_run` just above the orchestrator construction). The
    clamp reads ``RunOrchestrator.MIN_PARALLEL`` / ``MAX_PARALLEL`` from
    the same patched symbol, so the recording class MUST re-export the
    canonical band — mirroring it from the real class keeps the test
    insulated from a future design-spec re-tune.
    """

    MIN_PARALLEL: int = RunOrchestrator.MIN_PARALLEL
    MAX_PARALLEL: int = RunOrchestrator.MAX_PARALLEL
    DEFAULT_PARALLEL: int = RunOrchestrator.DEFAULT_PARALLEL

    last_parallel: int | None = None

    def __init__(self, *_args: Any, **_kwargs: Any) -> None:
        return None

    def run(self, specs: Any, *, parallel: int) -> tuple:
        _RecordingOrchestrator.last_parallel = parallel
        # Return an empty outcomes tuple so the command can still write
        # a summary and exit cleanly. The spec list is filtered to a
        # single eval upstream, but the orchestrator contract permits
        # returning fewer outcomes than specs when every worker is
        # short-circuited (e.g. cancellation). The summary writer
        # tolerates the empty tuple — RunCounts treats N'=0 as valid.
        return tuple()


@pytest.fixture
def recording_orchestrator(
    monkeypatch: pytest.MonkeyPatch,
) -> type[_RecordingOrchestrator]:
    """Patch ``commands.RunOrchestrator`` with the recording stand-in.

    Resets ``last_parallel`` per test so prior invocations cannot leak
    state. Module-level attribute is patched (not the import path) so
    the substitution is reverted automatically at test teardown.
    """
    _RecordingOrchestrator.last_parallel = None
    monkeypatch.setattr(commands_module, "RunOrchestrator", _RecordingOrchestrator)
    return _RecordingOrchestrator


def _invoke_run_with_real_suite(args: list[str], *, output_dir: Path) -> Any:
    """Run ``eval run`` against the ``real`` suite with ``--no-pty``.

    Every eval in ``real.yaml`` carries the DOC-OQ3 ``no_pty: skip`` tag,
    so the worker closure short-circuits each spec BEFORE the recording
    orchestrator is asked to dispatch it. The orchestrator therefore
    only sees the ``parallel`` kwarg — exactly the surface this fixture
    pins.
    """
    runner = CliRunner()
    return runner.invoke(
        eval_group,
        [
            "run",
            "--suite",
            str(REAL_SUITE_PATH),
            "--eval",
            "E1",
            "--no-pty",
            "--output-dir",
            str(output_dir),
            *args,
        ],
        catch_exceptions=False,
    )


def test_parallel_zero_clamps_to_one(
    clean_claude_home: Path,
    recording_orchestrator: type[_RecordingOrchestrator],
    allowlisted_output_dir: Path,
) -> None:
    """``--parallel 0`` clamps to ``MIN_PARALLEL`` (= 1)."""

    output_dir = allowlisted_output_dir / "p0"
    result = _invoke_run_with_real_suite(["--parallel", "0"], output_dir=output_dir)
    assert result.exit_code == RUN_CLEAN_EXIT_CODE, result.stdout + (
        result.stderr or ""
    )
    assert recording_orchestrator.last_parallel == RunOrchestrator.MIN_PARALLEL == 1


def test_parallel_sixteen_clamps_to_fifteen(
    clean_claude_home: Path,
    recording_orchestrator: type[_RecordingOrchestrator],
    allowlisted_output_dir: Path,
) -> None:
    """``--parallel 16`` clamps to ``MAX_PARALLEL`` (= 15)."""

    output_dir = allowlisted_output_dir / "p16"
    result = _invoke_run_with_real_suite(["--parallel", "16"], output_dir=output_dir)
    assert result.exit_code == RUN_CLEAN_EXIT_CODE, result.stdout + (
        result.stderr or ""
    )
    assert recording_orchestrator.last_parallel == RunOrchestrator.MAX_PARALLEL == 15


def test_timeout_mult_zero_exits_hard_fail(
    clean_claude_home: Path,
    allowlisted_output_dir: Path,
) -> None:
    """``--timeout-mult 0`` rejected with HARD_FAIL (exit 2)."""

    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "run",
            "--suite",
            str(REAL_SUITE_PATH),
            "--eval",
            "E1",
            "--no-pty",
            "--output-dir",
            str(allowlisted_output_dir / "tm0"),
            "--timeout-mult",
            "0",
        ],
    )
    assert result.exit_code == HARD_FAIL_EXIT_CODE
    assert "--timeout-mult must be > 0" in result.stderr


def test_timeout_mult_negative_exits_hard_fail(
    clean_claude_home: Path,
    allowlisted_output_dir: Path,
) -> None:
    """Negative ``--timeout-mult`` is rejected the same as zero."""

    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "run",
            "--suite",
            str(REAL_SUITE_PATH),
            "--eval",
            "E1",
            "--no-pty",
            "--output-dir",
            str(allowlisted_output_dir / "tm-neg"),
            "--timeout-mult",
            "-1.5",
        ],
    )
    assert result.exit_code == HARD_FAIL_EXIT_CODE
    assert "--timeout-mult must be > 0" in result.stderr


def test_max_disk_mb_negative_exits_hard_fail(
    clean_claude_home: Path,
    allowlisted_output_dir: Path,
) -> None:
    """``--max-disk-mb -1`` rejected; the error message points operators
    at ``0`` as the documented poller-disable value."""

    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "run",
            "--suite",
            str(REAL_SUITE_PATH),
            "--eval",
            "E1",
            "--no-pty",
            "--output-dir",
            str(allowlisted_output_dir / "md-neg"),
            "--max-disk-mb",
            "-1",
        ],
    )
    assert result.exit_code == HARD_FAIL_EXIT_CODE
    assert "--max-disk-mb must be >= 0" in result.stderr
    assert "use 0 to disable" in result.stderr


def test_output_dir_outside_allowlist_exits_scratch_root_violation(
    clean_claude_home: Path, tmp_path: Path
) -> None:
    """A ``--output-dir`` outside the AC12 / OPS-002 allowlist exits 2.

    The default allowlist is ``[/tmp/eval-runs, <repo>/.dev/eval-runs]``;
    pytest's ``tmp_path`` lands under ``/tmp/pytest-of-<user>/``, which
    is OUTSIDE the allowlist. Pre-PR-66 the runtime extended the
    allowlist with the operator's input (the tautology bug); after the
    fix the policy is strict and a path under ``/tmp/pytest-of-...`` is
    rejected with :data:`SCRATCH_ROOT_VIOLATION_EXIT_CODE`.
    """
    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "run",
            "--suite",
            str(REAL_SUITE_PATH),
            "--eval",
            "E1",
            "--no-pty",
            "--output-dir",
            str(tmp_path / "rogue"),
        ],
    )
    assert result.exit_code == SCRATCH_ROOT_VIOLATION_EXIT_CODE
    # The renderer pins the OPS-002 banner; we assert the banner stem
    # rather than the full message so a wording polish elsewhere does
    # not crater the test.
    assert "scratch-root" in result.stderr.lower()


def test_suite_not_found_exits_2(
    clean_claude_home: Path, allowlisted_output_dir: Path
) -> None:
    """An unresolvable ``--suite`` argument exits 2 with ``SuiteNotFound``."""

    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "run",
            "--suite",
            "this-suite-does-not-exist",
            "--no-pty",
            "--output-dir",
            str(allowlisted_output_dir / "sn"),
        ],
    )
    assert result.exit_code == SUITE_NOT_FOUND_EXIT_CODE
    assert "SuiteNotFound" in result.stderr


def test_unknown_eval_id_exits_2(
    clean_claude_home: Path, allowlisted_output_dir: Path
) -> None:
    """A ``--eval`` id not present in the suite exits 2 with ``EvalNotFound``."""

    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "run",
            "--suite",
            str(REAL_SUITE_PATH),
            "--eval",
            "E9999",
            "--no-pty",
            "--output-dir",
            str(allowlisted_output_dir / "en"),
        ],
    )
    assert result.exit_code == EVAL_NOT_FOUND_EXIT_CODE
    assert "EvalNotFound" in result.stderr


# ---------------------------------------------------------------------------
# AC bullet 3 — one-eval end-to-end run
# ---------------------------------------------------------------------------


def test_run_real_suite_no_pty_skips_e1_and_exits_clean(
    clean_claude_home: Path, allowlisted_output_dir: Path
) -> None:
    """``--suite real --eval E1 --no-pty`` exits 0 with summary on disk.

    Pins the AC bullet: "A one-eval run completes end-to-end with
    ``--suite real --eval E1``". The ``--no-pty`` short-circuit is the
    only currently-supported green path (the production lifecycle
    executor lands in M5/M6); every eval in ``real.yaml`` carries the
    DOC-OQ3 ``no_pty: skip`` tag so E1 returns ``SKIPPED`` with
    ``skip_reason='--no-pty'`` and the run exits cleanly.
    """
    output_dir = allowlisted_output_dir / "e2e"
    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "run",
            "--suite",
            str(REAL_SUITE_PATH),
            "--eval",
            "E1",
            "--no-pty",
            "--output-dir",
            str(output_dir),
            "--parallel",
            "1",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == RUN_CLEAN_EXIT_CODE, result.stdout + (
        result.stderr or ""
    )
    # FR-G4 / T04.13 / H1: summary.md + summary.json land in the compose_run_dir-
    # derived run-dir under output_dir (the OUTPUT ROOT, post-H1).
    run_dir = _find_run_dir(output_dir)
    assert (run_dir / "summary.md").is_file()
    summary_json = run_dir / "summary.json"
    assert summary_json.is_file()
    payload = json.loads(summary_json.read_text(encoding="utf-8"))
    assert payload["counts"]["expanded_n_prime"] == 1
    assert payload["totals"]["skipped"] == 1
    assert payload["evals"][0]["eval_id"] == "E1"
    assert payload["evals"][0]["status"] == "SKIPPED"
    assert payload["evals"][0]["skip_reason"] == "--no-pty"


def test_run_anchors_output_via_compose_run_dir(
    clean_claude_home: Path, allowlisted_output_dir: Path
) -> None:
    """T1 / H1 / FR-G4: ``--output-dir`` is the OUTPUT ROOT, the run-dir is
    composed via ``compose_run_dir`` into the canonical layout
    ``<output_dir>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/``.

    Pre-H1 a flat layout placed ``summary.{md,json,yaml}`` directly under
    ``--output-dir``, breaking the FR-G4 layout invariant. This test pins
    the post-H1 contract: artifacts land under the compose_run_dir-derived
    run-dir, and ``summary.md``, ``summary.json``, and ``summary.yaml`` all
    co-exist there (the M4 unconditional-yaml guarantee). Any regression
    that anchors ``--output-dir`` as the run-dir directly fails this test.
    """
    output_dir = allowlisted_output_dir / "h1-anchor"
    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "run",
            "--suite",
            str(REAL_SUITE_PATH),
            "--eval",
            "E1",
            "--no-pty",
            "--output-dir",
            str(output_dir),
            "--parallel",
            "1",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == RUN_CLEAN_EXIT_CODE, result.stdout + (
        result.stderr or ""
    )

    # FR-G4 layout: <output_dir>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/
    eval_runs_root = output_dir / ".dev" / "eval-runs"
    assert eval_runs_root.is_dir(), (
        f"FR-G4 layout root missing under --output-dir: {eval_runs_root}"
    )
    date_dirs = sorted(p for p in eval_runs_root.iterdir() if p.is_dir())
    assert len(date_dirs) == 1, (
        f"Expected exactly one date-stamped dir under {eval_runs_root}, "
        f"found {[p.name for p in date_dirs]}"
    )
    run_dirs = sorted(p for p in date_dirs[0].iterdir() if p.is_dir())
    assert len(run_dirs) == 1, (
        f"Expected exactly one run-id dir under {date_dirs[0]}, "
        f"found {[p.name for p in run_dirs]}"
    )
    run_dir = run_dirs[0]

    # M4 unconditional yaml — all three summary files co-exist.
    assert (run_dir / "summary.md").is_file()
    assert (run_dir / "summary.json").is_file()
    assert (run_dir / "summary.yaml").is_file()

    # Flat-layout regression guard: summary.* MUST NOT live directly
    # under --output-dir (only the .dev/ subtree is permitted there).
    assert not (output_dir / "summary.md").exists(), (
        "FR-G4 regression: summary.md found at flat layout — "
        "H1 anchoring via compose_run_dir is not active."
    )


def test_run_json_emits_summary_to_stdout(
    clean_claude_home: Path, allowlisted_output_dir: Path
) -> None:
    """``--json`` mirrors the on-disk summary onto stdout."""

    output_dir = allowlisted_output_dir / "json"
    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "run",
            "--suite",
            str(REAL_SUITE_PATH),
            "--eval",
            "E1",
            "--no-pty",
            "--output-dir",
            str(output_dir),
            "--parallel",
            "1",
            "--json",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == RUN_CLEAN_EXIT_CODE
    payload = json.loads(result.stdout)
    assert payload["counts"]["expanded_n_prime"] == 1
    assert payload["totals"]["skipped"] == 1


def test_run_verbose_emits_summary_line(
    clean_claude_home: Path, allowlisted_output_dir: Path
) -> None:
    """``--verbose`` prints a human-readable summary line on success."""

    output_dir = allowlisted_output_dir / "verbose"
    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "run",
            "--suite",
            str(REAL_SUITE_PATH),
            "--eval",
            "E1",
            "--no-pty",
            "--output-dir",
            str(output_dir),
            "--parallel",
            "1",
            "--verbose",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == RUN_CLEAN_EXIT_CODE
    # The summary-line formatter (commands._format_run_summary_line) renders
    # ``run <id>: <P>P/<F>F/<S>S/<E>E/<I>I/<T>T in <duration>s -> <output_dir>``
    # per H3 — the full DM-012 status taxonomy (6 buckets covering 8 statuses).
    out = result.stdout
    assert out.startswith("run ")
    assert (
        "0P/0F/1S/0E/0I/0T" in out
    )  # 1 SKIPPED, 0 PASS, 0 FAIL, 0 ERRORED, 0 INTERRUPTED, 0 TIMEOUT
    assert str(output_dir) in out


def test_run_junit_writes_xml_artifact(
    clean_claude_home: Path, allowlisted_output_dir: Path
) -> None:
    """``--junit`` causes the Reporter to also emit ``junit.xml``."""

    output_dir = allowlisted_output_dir / "junit"
    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "run",
            "--suite",
            str(REAL_SUITE_PATH),
            "--eval",
            "E1",
            "--no-pty",
            "--output-dir",
            str(output_dir),
            "--parallel",
            "1",
            "--junit",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == RUN_CLEAN_EXIT_CODE
    # H1: artifacts land under the compose_run_dir-derived run-dir.
    run_dir = _find_run_dir(output_dir)
    assert (run_dir / "junit.xml").is_file()


def test_run_no_pty_full_suite_skips_every_eval(
    clean_claude_home: Path, allowlisted_output_dir: Path
) -> None:
    """``--no-pty`` against the full ``real`` suite skips every entry.

    DOC-OQ3 / R-077 tags every E1-E15 row in ``real.yaml`` with
    ``no_pty: skip`` so the whole suite short-circuits to ``SKIPPED``
    with no per-eval HOME allocations. The total post-expansion row
    count matches the manifest n (E2 is parameterized 3× → 17 expanded
    rows).
    """
    output_dir = allowlisted_output_dir / "no-pty-all"
    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "run",
            "--suite",
            str(REAL_SUITE_PATH),
            "--no-pty",
            "--output-dir",
            str(output_dir),
            "--parallel",
            "4",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == RUN_CLEAN_EXIT_CODE, result.stdout + (
        result.stderr or ""
    )
    # H1: summary.json lands under the compose_run_dir-derived run-dir.
    run_dir = _find_run_dir(output_dir)
    payload = json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
    n_prime = payload["counts"]["expanded_n_prime"]
    assert n_prime == payload["totals"]["skipped"]
    assert n_prime >= 15  # at least one expanded row per E1-E15
    # Every outcome carries the documented --no-pty skip reason.
    for outcome in payload["evals"]:
        assert outcome["status"] == "SKIPPED"
        assert outcome["skip_reason"] == "--no-pty"


# ---------------------------------------------------------------------------
# AC bullet 4 — spec.md documents the flag wiring
# ---------------------------------------------------------------------------


def test_d0072_spec_documents_flag_wiring() -> None:
    """``D-0072/spec.md`` exists and references each FR-CLI1 flag.

    The phase-4 AC bullet "TASKLIST_ROOT/artifacts/D-0072/spec.md
    documents flag wiring" is a deliverable, not a code surface. Pinning
    the file's existence + that every flag name appears at least once
    keeps the AC from drifting under future doc edits without affecting
    the runtime tests above.
    """
    assert D0072_SPEC_PATH.is_file(), (
        f"D-0072 spec missing at {D0072_SPEC_PATH}; T04.10 AC requires "
        "spec.md to be authored alongside the test file."
    )
    body = D0072_SPEC_PATH.read_text(encoding="utf-8")
    missing = [flag for flag in EXPECTED_FLAGS if flag not in body]
    assert not missing, (
        f"D-0072/spec.md does not mention every FR-CLI1 flag; missing: {missing!r}"
    )


# ---------------------------------------------------------------------------
# AC bullet 5 — _NullLifecycleExecutor observability (M2)
# ---------------------------------------------------------------------------


def test_run_emits_warning_when_null_lifecycle_executor_active(
    clean_claude_home: Path, allowlisted_output_dir: Path
) -> None:
    """Spec M2 — `_NullLifecycleExecutor` MUST emit a stderr WARNING when active.

    Today's production code at `commands.py:1361-1402` unconditionally
    returns `_NullLifecycleExecutor` from `_resolve_executor_factory()`
    (no production branch exists yet — the M5/M6 lifecycle integration
    hasn't landed). Operators running `eval run` therefore get a canned
    PASS shape from a non-production shim with NO observable runtime
    signal. M2 fixes this by emitting a `click.echo(..., err=True)`
    WARNING tagged "NullLifecycleExecutor" at the executor-factory call
    site.

    Until Phase 3 Step 3.5 lands, this test is EXPECTED to be RED — the
    warning string is not emitted today.
    """
    output_dir = allowlisted_output_dir / "m2-warning"
    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "run",
            "--suite",
            str(REAL_SUITE_PATH),
            "--eval",
            "E1",
            "--no-pty",
            "--output-dir",
            str(output_dir),
            "--parallel",
            "1",
        ],
        catch_exceptions=False,
    )
    assert "NullLifecycleExecutor" in (result.stderr or "")
