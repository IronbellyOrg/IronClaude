"""Click commands for the cliEval real-eval harness.

FR-CLI4 / Task T01.13 (roadmap R-011, deliverable D-0011): the ``eval
doctor`` subcommand renders a green checklist verifying every HARD
capability (``claude>=0.5.0``, ``jq``, ``make``, ``git``, ``~/.claude/``
extant) and reports SOFT-SKIP MCP server availability + the ptytest
vendoring marker. ``--json`` emits a deterministic, machine-readable
payload that extends the :class:`CapabilityReport` contract documented in
``artifacts/D-0010/spec.md`` with three doctor-specific rows:

* ``claude.min_version``      — HARD; parses ``claude --version`` output.
* ``filesystem.claude_home``  — HARD; checks ``~/.claude/`` exists.
* ``vendored.ptytest``        — SOFT-SKIP; checks
  ``src/superclaude/cli/eval/pty/__init__.py``. The full vendoring
  lands at M2; until then this row stays in ``soft_skips`` so doctor
  still exits 0 on a clean dev machine (per T01.13 AC).

``--no-mcp`` forwards into :class:`CapabilityGates` so SOFT-SKIP MCP
rows are flagged with ``skipped_by_flag=True``. ``--check-coverage`` is
accepted now and wired through the JSON payload + human checklist as a
deferred marker; the actual FR-G5 coverage gate lands in M4 T04.14.

Doctor fails closed with ``HARD_FAIL_EXIT_CODE`` when any HARD row is missing and
prints a HARD-failure artifact identifying every offending capability to
``stderr`` so CI logs capture a stable diagnostic line per failure.
"""

from __future__ import annotations

import json
import platform
import re
import subprocess
import sys
import time
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Optional, Sequence

import click
import yaml

from . import exit_codes as _exit_codes
from .artifact_layout import (
    allocate_per_eval_paths,
    compose_run_dir,
    compose_run_id,
)
from .capabilities import (
    CapabilityGates,
    CapabilityReport,
    CapabilityStatus,
)
from .config import (
    SCRATCH_ROOT_VIOLATION_EXIT_CODE,
    EvalConfig,
    ScratchRootViolation,
    format_scratch_root_violation,
    resolve_scratch_root,
)
from .coverage import (
    COVERAGE_GATE_FAILED_EXIT_CODE,
    CoverageResult,
    coverage_gate,
)
from .disk_budget import (
    DEFAULT_DISK_BUDGET_MB,
    DISK_BUDGET_EXCEEDED_ARTIFACT_NAME,
    DISK_BUDGET_EXCEEDED_EXIT_CODE,
    DISK_BUDGET_RETENTION_ADVICE,
    DiskBudgetPoller,
)
from .isolation import HomeIsolation
from .loader import (
    SUITE_LOADER_ERROR_EXIT_CODE,
    ParsedSuite,
    SuiteLoader,
    SuiteLoaderError,
)
from .models import (
    EVAL_STATUSES,
    FAILED_STATUSES,
    PASSED_STATUSES,
    SKIPPED_STATUSES,
    EvalOutcome,
    EvalSpec,
    RunCounts,
    RunSummary,
    RunTotals,
)
from .orchestrator import RunOrchestrator, allocate_session_id
from .reporter import Reporter
from .runner import EvalRunner, ExecutorContext, LifecycleExecutor, ObservedRun
from .signal_handler import (
    EXIT_INTERRUPTED,
    CancellationToken,
    SignalHandlerInstaller,
)
from .suites import SCHEMA_PATH

_VersionTuple = tuple[int, ...]

_VERSION_RE = re.compile(r"(\d+)\.(\d+)\.(\d+)")


def _format_version(parts: Iterable[int]) -> str:
    return ".".join(str(p) for p in parts)


def _parse_version(text: str) -> Optional[_VersionTuple]:
    """Return the first ``X.Y.Z`` triple in ``text`` or ``None``."""
    match = _VERSION_RE.search(text or "")
    if match is None:
        return None
    return tuple(int(g) for g in match.groups())


def _default_claude_version_probe() -> Optional[str]:
    """Invoke ``claude --version`` and return its stdout+stderr or ``None``."""
    try:
        result = subprocess.run(
            ["claude", "--version"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (FileNotFoundError, OSError, subprocess.SubprocessError):
        return None
    raw = (result.stdout or "") + (result.stderr or "")
    return raw.strip() or None


def _check_claude_version(
    probe: Optional[Callable[[], Optional[str]]] = None,
    min_version: Optional[_VersionTuple] = None,
    *,
    config: Optional[EvalConfig] = None,
) -> CapabilityStatus:
    """HARD check: ``claude --version`` parses and meets the minimum.

    The version floor (R1-mit / T02.20) is sourced from ``EvalConfig`` —
    there is no in-doctor hard-coded copy. Callers may pass ``min_version``
    directly (kept for test ergonomics); otherwise the helper reads
    ``config.min_claude_version``, falling back to a default-constructed
    :class:`EvalConfig` whose default tracks
    :data:`DEFAULT_MIN_CLAUDE_VERSION`.
    """
    probe = probe or _default_claude_version_probe
    if min_version is None:
        active_config = config if config is not None else EvalConfig()
        min_version = active_config.min_claude_version
    description = f"Claude CLI >= {_format_version(min_version)}"
    try:
        raw = probe()
    except Exception as exc:  # noqa: BLE001 - probe is a user-supplied callable
        return CapabilityStatus(
            name="claude.min_version",
            passed=False,
            failure_mode="hard",
            description=description,
            detail=f"version probe raised {type(exc).__name__}: {exc}",
        )
    if not raw:
        return CapabilityStatus(
            name="claude.min_version",
            passed=False,
            failure_mode="hard",
            description=description,
            detail="claude --version not callable",
        )
    parsed = _parse_version(raw)
    if parsed is None:
        return CapabilityStatus(
            name="claude.min_version",
            passed=False,
            failure_mode="hard",
            description=description,
            detail=f"could not parse version from {raw!r}",
        )
    passed = parsed >= min_version
    detail = f"claude {_format_version(parsed)}"
    if not passed:
        detail += f" < required {_format_version(min_version)}"
    return CapabilityStatus(
        name="claude.min_version",
        passed=passed,
        failure_mode="hard",
        description=description,
        detail=detail,
    )


def _check_claude_home(home: Optional[Path] = None) -> CapabilityStatus:
    """HARD check: ``~/.claude/`` (or override) exists and is a directory."""
    target = home if home is not None else Path.home() / ".claude"
    exists = target.is_dir()
    return CapabilityStatus(
        name="filesystem.claude_home",
        passed=exists,
        failure_mode="hard",
        description="~/.claude/ directory exists",
        detail=str(target) if exists else f"{target} not found",
    )


# ---------------------------------------------------------------------------
# NFR-PERF2 free-RAM precheck (T03.17 / D-0059)
# ---------------------------------------------------------------------------
#
# Design-spec §11 (NFR-PERF2) pins peak resident-set-size at 2.25 GB for
# ``--parallel 15``. When an operator requests the maximum concurrency on a
# host that cannot afford that ceiling, the doctor MUST emit a warning
# string containing the literal ``"2.25 GB"`` token so the operator can
# tell at a glance which budget was insufficient. Hosts with less than
# 4 GB free RAM are out-of-scope per ``CLAUDE.md`` infrastructure notes —
# the warning is the documented stop-gap, not an exit-2 hard failure
# (which would block legitimate ``--parallel 8`` runs on tight hosts).

RAM_CEILING_GB: float = 2.25
"""Design-spec §11 NFR-PERF2 peak-RSS ceiling at ``--parallel 15``.

The literal value ``2.25`` (not the bytes) is the one operators see in
the warning text, so changing it requires a roadmap edit. The bytes
constant below is derived from it so the two views cannot drift.
"""

RAM_CEILING_BYTES: int = int(RAM_CEILING_GB * (1024**3))
"""Byte-equivalent of :data:`RAM_CEILING_GB` for free-RAM comparisons.

``int(2.25 * 1024**3) == 2_415_919_104``. Computed once at import time so
the helper does not re-derive it on every call.
"""

RAM_CEILING_TEXT: str = f"{RAM_CEILING_GB} GB"
"""Canonical rendering of the ceiling used in operator-facing strings.

The T03.17 AC asserts that the warning contains this literal token. Pin
it here so any downstream string formatting picks up changes uniformly.
"""

PARALLEL_RAM_GATE_THRESHOLD: int = 15
"""``--parallel`` value at-or-above which the RAM precheck fires.

Matches :attr:`RunOrchestrator.MAX_PARALLEL`. Below this threshold the
benchmark does not document a ceiling, so the doctor stays silent rather
than emit a misleading number.
"""


def _default_free_ram_probe() -> Optional[int]:
    """Return free RAM in bytes via Linux ``/proc/meminfo``.

    Prefers ``MemAvailable`` (kernel ≥3.14) because it accounts for
    reclaimable cache the way an oncoming allocation would; falls back to
    ``MemFree`` on ancient kernels. Returns ``None`` on any failure (eg
    non-Linux host, locked-down container) so the doctor records a
    ``probe unavailable`` SOFT-SKIP rather than crashing — a doctor that
    crashes on tight hosts is worse than one that warns.
    """

    meminfo = Path("/proc/meminfo")
    if not meminfo.is_file():
        return None
    try:
        text = meminfo.read_text(encoding="utf-8")
    except OSError:
        return None
    available: Optional[int] = None
    free: Optional[int] = None
    for line in text.splitlines():
        key, _, rest = line.partition(":")
        key = key.strip()
        if key not in ("MemAvailable", "MemFree"):
            continue
        tokens = rest.strip().split()
        if not tokens:
            continue
        try:
            kb = int(tokens[0])
        except ValueError:
            continue
        unit = tokens[1].lower() if len(tokens) > 1 else "kb"
        # /proc/meminfo always reports in kB on Linux; the unit check is
        # defensive in case a future kernel changes the format.
        multiplier = 1024 if unit == "kb" else 1
        value = kb * multiplier
        if key == "MemAvailable":
            available = value
        elif key == "MemFree":
            free = value
    if available is not None:
        return available
    return free


def _check_free_ram_for_parallel(
    *,
    requested_parallel: Optional[int],
    probe: Optional[Callable[[], Optional[int]]] = None,
    ceiling_bytes: int = RAM_CEILING_BYTES,
    threshold_parallel: int = PARALLEL_RAM_GATE_THRESHOLD,
) -> Optional[CapabilityStatus]:
    """SOFT-SKIP check: free RAM is sufficient for the requested concurrency.

    Returns ``None`` (gate inactive) when ``requested_parallel`` is below
    :data:`PARALLEL_RAM_GATE_THRESHOLD` — the design-spec only pins the
    RSS ceiling for the upper-bound run, so warning operators about
    insufficient RAM at ``--parallel 8`` would be noise.

    When the gate is active the helper returns a :class:`CapabilityStatus`
    whose ``failure_mode`` is ``"skip"`` regardless of outcome:

    * Passed when the probe returns a value at or above
      :data:`RAM_CEILING_BYTES`.
    * Failed (SOFT-SKIP) when free RAM is below the ceiling, with the
      detail string containing the literal :data:`RAM_CEILING_TEXT` token
      so a grep against the operator-facing artifact pins the failure
      mode without parsing structure.
    * Failed (SOFT-SKIP) when the probe returned ``None`` — the host
      cannot self-report free RAM so we cannot certify the budget either.
    """

    if requested_parallel is None or requested_parallel < threshold_parallel:
        return None

    probe = probe or _default_free_ram_probe
    description = f"free RAM >= {RAM_CEILING_TEXT} for --parallel {threshold_parallel}"
    try:
        free_ram = probe()
    except Exception as exc:  # noqa: BLE001 — probe is caller-supplied
        return CapabilityStatus(
            name="host.free_ram_for_max_parallel",
            passed=False,
            failure_mode="skip",
            description=description,
            detail=(
                f"free-RAM probe raised {type(exc).__name__}: {exc}; "
                f"{RAM_CEILING_TEXT} budget unverified"
            ),
        )
    if free_ram is None:
        return CapabilityStatus(
            name="host.free_ram_for_max_parallel",
            passed=False,
            failure_mode="skip",
            description=description,
            detail=(
                f"free-RAM probe unavailable on this host; cannot verify "
                f"{RAM_CEILING_TEXT} budget"
            ),
        )
    free_gb = free_ram / (1024**3)
    if free_ram < ceiling_bytes:
        return CapabilityStatus(
            name="host.free_ram_for_max_parallel",
            passed=False,
            failure_mode="skip",
            description=description,
            detail=(
                f"free RAM {free_gb:.2f} GB < {RAM_CEILING_TEXT} ceiling "
                f"for --parallel {threshold_parallel}"
            ),
        )
    return CapabilityStatus(
        name="host.free_ram_for_max_parallel",
        passed=True,
        failure_mode="skip",
        description=description,
        detail=f"free RAM {free_gb:.2f} GB >= {RAM_CEILING_TEXT}",
    )


def _check_ptytest_vendored(pty_dir: Optional[Path] = None) -> CapabilityStatus:
    """SOFT-SKIP check: ptytest vendored under ``cli/eval/pty/``.

    The actual ptytest vendoring lands at M2; the row stays SOFT-SKIP so
    doctor still exits 0 on a clean dev machine until the upstream task
    materialises ``cli/eval/pty/__init__.py``.
    """
    target = pty_dir if pty_dir is not None else Path(__file__).resolve().parent / "pty"
    init_file = target / "__init__.py"
    passed = init_file.is_file()
    return CapabilityStatus(
        name="vendored.ptytest",
        passed=passed,
        failure_mode="skip",
        description="ptytest vendored under cli/eval/pty/",
        detail=str(target) if passed else f"{init_file} not found (vendored at M2)",
    )


def _extend_report(
    base: CapabilityReport,
    extras: tuple[CapabilityStatus, ...],
) -> CapabilityReport:
    """Return a new ``CapabilityReport`` with ``extras`` appended and
    failure-bucket tallies updated.

    The base report's ``blocked_evals`` and ``skip_flags`` are preserved
    verbatim — supplementary doctor rows only contribute to the three
    failure buckets (``hard_failures``, ``soft_skips``, ``soft_xfails``).
    """
    rows = base.report + extras
    hard_failures = list(base.hard_failures)
    soft_skips = list(base.soft_skips)
    soft_xfails = list(base.soft_xfails)
    for status in extras:
        if status.passed:
            continue
        if status.failure_mode == "hard":
            hard_failures.append(status.name)
        elif status.failure_mode == "skip":
            soft_skips.append(status.name)
        else:  # "xfail"
            soft_xfails.append(status.name)
    return replace(
        base,
        report=rows,
        hard_failures=tuple(hard_failures),
        soft_skips=tuple(soft_skips),
        soft_xfails=tuple(soft_xfails),
    )


def build_doctor_report(
    skip_flags: Optional[Iterable[str]] = None,
    *,
    gates: Optional[CapabilityGates] = None,
    claude_version_probe: Optional[Callable[[], Optional[str]]] = None,
    claude_home: Optional[Path] = None,
    pty_dir: Optional[Path] = None,
    config: Optional[EvalConfig] = None,
    requested_parallel: Optional[int] = None,
    free_ram_probe: Optional[Callable[[], Optional[int]]] = None,
) -> CapabilityReport:
    """Aggregate :class:`CapabilityGates` + doctor-specific checks.

    Args:
        skip_flags: Active CLI skip flags (e.g. ``{"--no-mcp"}``).
            Forwarded to :class:`CapabilityGates` when ``gates`` is not
            supplied.
        gates: Optional pre-built :class:`CapabilityGates` (test hook).
        claude_version_probe: Override for ``claude --version`` invocation.
        claude_home: Override for ``~/.claude/`` path.
        pty_dir: Override for the ptytest vendored directory.
        config: Optional :class:`EvalConfig` providing the
            ``min_claude_version`` floor (R1-mit / T02.20). Falls back to a
            default-constructed instance whose floor matches
            :data:`DEFAULT_MIN_CLAUDE_VERSION`.
        requested_parallel: Optional concurrency the operator declared via
            ``--parallel``. When at-or-above
            :data:`PARALLEL_RAM_GATE_THRESHOLD` the NFR-PERF2 free-RAM
            check (T03.17) is appended to the report.
        free_ram_probe: Override for the ``/proc/meminfo`` probe; tests
            inject a deterministic value.

    Returns:
        A :class:`CapabilityReport` whose ``report`` tuple contains the
        seven default capability rows followed by the three core doctor
        rows in this fixed order: ``claude.min_version``,
        ``filesystem.claude_home``, ``vendored.ptytest``. The NFR-PERF2
        ``host.free_ram_for_max_parallel`` row is appended last when the
        parallel gate fires.
    """
    if gates is None:
        gates = CapabilityGates(skip_flags=skip_flags or ())
    base = gates.check_all()
    extras: list[CapabilityStatus] = [
        _check_claude_version(probe=claude_version_probe, config=config),
        _check_claude_home(home=claude_home),
        _check_ptytest_vendored(pty_dir=pty_dir),
    ]
    ram_status = _check_free_ram_for_parallel(
        requested_parallel=requested_parallel,
        probe=free_ram_probe,
    )
    if ram_status is not None:
        extras.append(ram_status)
    return _extend_report(base, tuple(extras))


def _row_marker(row: CapabilityStatus) -> tuple[str, str]:
    """Return ``(glyph, tag)`` for the human checklist line."""
    if row.passed:
        return "[ok]", ""
    if row.skipped_by_flag:
        return "[--]", " (skipped by flag)"
    if row.failure_mode == "hard":
        return "[XX]", " (HARD)"
    if row.failure_mode == "skip":
        return "[--]", " (SOFT-SKIP)"
    return "[??]", " (xfail)"


def render_checklist(report: CapabilityReport) -> str:
    """Render the doctor green-checklist text (FR-CLI4 human output)."""
    lines = ["superclaude eval doctor:"]
    for row in report.report:
        marker, tag = _row_marker(row)
        detail = f" -- {row.detail}" if row.detail else ""
        lines.append(f"  {marker} {row.description}{tag}{detail}")
    if report.skip_flags:
        lines.append(f"skip flags: {', '.join(report.skip_flags)}")
    if report.hard_failures:
        lines.append(f"HARD failures: {', '.join(report.hard_failures)}")
    else:
        lines.append("all HARD capabilities satisfied")
        if report.soft_skips:
            lines.append(f"soft skips: {', '.join(report.soft_skips)}")
    return "\n".join(lines)


def render_hard_failure_artifact(report: CapabilityReport) -> str:
    """Render the stderr HARD-failure artifact per FR-CLI4 AC."""
    by_name = {row.name: row for row in report.report}
    lines = ["eval doctor: HARD failures"]
    for name in report.hard_failures:
        row = by_name.get(name)
        if row is None:
            lines.append(f"  - {name}")
            continue
        lines.append(f"  - {name} ({row.description}): {row.detail}")
    return "\n".join(lines)


def doctor_payload(
    report: CapabilityReport,
    *,
    check_coverage: bool,
    coverage_result: Optional[CoverageResult] = None,
) -> dict:
    """Build the ``--json`` payload.

    Extends :meth:`CapabilityReport.to_json` with a ``coverage_gate``
    marker so callers can detect whether ``--check-coverage`` was passed.
    The base ``CapabilityReport`` keys are preserved verbatim so the
    payload remains compatible with the D-0010 contract.

    When ``check_coverage`` is on and ``coverage_result`` is supplied
    (T04.14 wiring), the marker carries the full :meth:`CoverageResult.to_dict`
    payload under ``result``; ``status`` is ``"passed"`` / ``"failed"``
    based on ``coverage_result.passed``. When ``check_coverage`` is on
    but no suite was supplied the gate runs in "matchers-only" mode
    (no covering evals to resolve), so ``coverage_result`` is still
    populated but ``coverage_map`` will be empty.
    """
    payload = report.to_json()
    marker: dict[str, object] = {"requested": bool(check_coverage)}
    if check_coverage and coverage_result is not None:
        marker["status"] = "passed" if coverage_result.passed else "failed"
        marker["result"] = coverage_result.to_dict()
    else:
        marker["status"] = "skipped"
    payload["coverage_gate"] = marker
    return payload


HARD_FAIL_EXIT_CODE: int = _exit_codes.USAGE_ERROR
"""Process exit code for harness contract failures reaching the ``eval`` CLI.
Canonical value: ``exit_codes.USAGE_ERROR`` (CC2 / OQ-2).
"""


# ---------------------------------------------------------------------------
# Design-spec §4 exit-code constants for ``eval run``
# ---------------------------------------------------------------------------
#
# Pinned by tests/cli/eval/test_exit_codes.py (TEST-008 / T04.19 / D-0079).
# Per CC2 / OQ-2 — every cliEval exit code re-exports from ``exit_codes.py``.
# RUN_INTERRUPTED_EXIT_CODE preserves its existing alias to
# ``signal_handler.EXIT_INTERRUPTED`` because that constant predates this
# consolidation; both point at the same integer (3) so no drift is possible.

RUN_CLEAN_EXIT_CODE: int = _exit_codes.SUCCESS
"""Clean run: every expanded eval reached PASS / SKIPPED / XFAIL and no breach."""

RUN_FAILURES_EXIT_CODE: int = _exit_codes.FAILURES
"""Failing run: at least one eval ended FAIL / ERRORED / TIMEOUT / XPASS but
the harness ran to completion."""

RUN_INTERRUPTED_EXIT_CODE: int = EXIT_INTERRUPTED
"""SIGINT / SIGTERM mid-run; cooperative cancellation drained. Re-exports
:data:`signal_handler.EXIT_INTERRUPTED` (= 3) so the two surfaces cannot
drift. Mirrors ``exit_codes.INTERRUPTED`` (= 3) by construction."""


# ---------------------------------------------------------------------------
# AC1 / R-109 / T06.07 — Linux-only v1 platform precheck
# ---------------------------------------------------------------------------
#
# Roadmap row 353 (AC1 / R-109) pins v1 to Linux. The doctor refuses any
# other ``platform.system()`` value with a friendly stderr message before
# any capability gates run, so a macOS or Windows operator gets a single
# actionable line instead of a cascade of HARD failures triggered by
# absent ``/proc/meminfo``, missing ``jq``, etc. Re-uses
# :data:`HARD_FAIL_EXIT_CODE` (2) because a non-Linux host is a precondition
# failure of the same class as a missing ``claude`` binary.

NON_LINUX_REFUSAL_TEMPLATE: str = (
    "eval doctor: unsupported platform: {system!r}. "
    "The cliEval harness ships Linux-only for v1 (AC1, roadmap R-109). "
    "macOS support is deferred to v2 — see DOC-OQ9 closure in "
    ".dev/releases/current/cliEval/decisions.md."
)
"""Friendly non-Linux refusal message rendered to stderr by ``eval doctor``.

The template cites AC1 and DOC-OQ9 so an operator landing here can trace
the v1 platform commitment back to the ADR log without a documentation
hunt. Pin as a module-level constant so tests can match on it without
duplicating the string.
"""


def _default_platform_probe() -> str:
    """Return :func:`platform.system` output.

    Wrapped so tests can monkey-patch the doctor's platform view
    independently of the host they run on (the cliEval suite is
    Linux-only at v1 ship, but unit tests must still exercise the
    macOS/Windows refusal branch on a Linux CI box).
    """
    return platform.system()


def _format_coverage_summary(result: CoverageResult) -> str:
    """One-line human summary for ``doctor --check-coverage`` stdout."""
    if not result.matchers:
        return "coverage gate: no in-scope matchers (passed)"
    if result.passed:
        return (
            f"coverage gate: {len(result.covered)}/{len(result.matchers)} "
            f"matcher(s) covered (passed)"
        )
    return (
        f"coverage gate: {len(result.missing)} of {len(result.matchers)} "
        f"matcher(s) uncovered (FAILED)"
    )


def _format_coverage_missing_roster(result: CoverageResult) -> str:
    """Render the stderr artifact when the coverage gate fails."""
    lines = ["eval doctor: coverage gate FAILED — uncovered matcher patterns:"]
    for m in result.missing:
        lines.append(f"  - {m.event}: {m.pattern}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# FR-CLI2 ``eval list`` (T01.21 / D-0018)
# ---------------------------------------------------------------------------


_DEFAULT_SUITES_DIR: Path = SCHEMA_PATH.parent
"""Default location for built-in suite manifests.

Resolves to ``src/superclaude/cli/eval/suites/``. The directory currently
only ships ``suite.schema.json`` and an ``__init__.py``; built-in
``*.yaml`` manifests will land in subsequent milestones. The glob in
:func:`discover_suite_manifests` filters to ``*.yaml`` so the schema and
package marker never appear in the listing.
"""


def discover_suite_manifests(suites_dir: Path) -> list[Path]:
    """Return ``suites_dir/*.yaml`` sorted by filename for determinism.

    ``eval list`` MUST produce identical output for a given suite
    directory across invocations (FR-CLI2 AC), so the sort is part of the
    contract — not an implementation detail.

    A missing or non-directory ``suites_dir`` is treated as the
    empty-directory case (no suites found) rather than an error: a fresh
    checkout that has not yet populated built-in suites must not break
    ``eval list``.
    """

    if not suites_dir.is_dir():
        return []
    return sorted(suites_dir.glob("*.yaml"))


@dataclass(frozen=True)
class SuiteSummary:
    """One row in the ``eval list`` output.

    Attributes:
        name: Manifest ``name`` field (verbatim).
        version: Manifest ``version`` field (verbatim, string).
        eval_count: Number of evals after parameterize expansion. This
            reflects "how many evals would run" rather than the raw
            ``evals[]`` length, which matches operator intent.
        source: Filesystem path of the manifest (used for human output
            and stable JSON ordering).
    """

    name: str
    version: str
    eval_count: int
    source: Path

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "version": self.version,
            "eval_count": self.eval_count,
        }


def summarize_suites(
    suites_dir: Path,
    *,
    loader: Optional[SuiteLoader] = None,
) -> list[SuiteSummary]:
    """Load every ``*.yaml`` in ``suites_dir`` and project to summaries.

    Any :class:`SuiteLoaderError` raised by :class:`SuiteLoader` propagates
    so the CLI boundary can map it to
    :data:`SUITE_LOADER_ERROR_EXIT_CODE` (= 2). The loader is injectable
    for tests that want to stub schema/regex/capability gates without
    touching the file system.
    """

    loader = loader if loader is not None else SuiteLoader()
    summaries: list[SuiteSummary] = []
    for manifest in discover_suite_manifests(suites_dir):
        parsed: ParsedSuite = loader.load(manifest)
        summaries.append(
            SuiteSummary(
                name=parsed.name,
                version=parsed.version,
                eval_count=len(parsed.evals),
                source=manifest,
            )
        )
    return summaries


def render_list_text(summaries: Iterable[SuiteSummary]) -> str:
    """Render the human-readable ``eval list`` output."""

    rows = list(summaries)
    lines = ["superclaude eval list:"]
    if not rows:
        lines.append("  (no suites found)")
        return "\n".join(lines)
    for row in rows:
        lines.append(
            f"  - {row.name} (version {row.version}, {row.eval_count} eval"
            f"{'s' if row.eval_count != 1 else ''})"
        )
    return "\n".join(lines)


def list_payload(summaries: Iterable[SuiteSummary]) -> list[dict]:
    """Build the ``--json`` payload: a list of ``{name,version,eval_count}``."""

    return [row.to_dict() for row in summaries]


@click.group("eval")
def eval_group() -> None:
    """Run and inspect the cliEval real-eval harness."""


@eval_group.command("doctor")
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    help="Emit a deterministic JSON payload extending CapabilityReport.",
)
@click.option(
    "--no-mcp",
    is_flag=True,
    help="Skip MCP-server capability gates (forwarded to CapabilityGates).",
)
@click.option(
    "--check-coverage",
    is_flag=True,
    help=(
        "Wire the FR-G5 coverage gate marker into the payload "
        "(full gate lands in M4 T04.14)."
    ),
)
@click.option(
    "--output-dir",
    "output_dir",
    type=click.Path(file_okay=False, path_type=Path),
    default=None,
    help=(
        "Validate <path> against the OPS-002 / AC12 scratch-root policy. "
        "A non-allowlisted root exits 2 and the stderr artifact quotes "
        "the policy verbatim (see docs/eval/scratch-roots.md)."
    ),
)
@click.option(
    "--parallel",
    "parallel",
    type=int,
    default=None,
    help=(
        "Declared concurrency for the next ``eval run``. When >= 15 the "
        "doctor runs the NFR-PERF2 free-RAM precheck and warns on hosts "
        f"with less than {RAM_CEILING_TEXT} free."
    ),
)
@click.option(
    "--suite",
    "suite",
    type=str,
    default=None,
    help=(
        "Suite name or manifest path used to resolve matcher coverage "
        "when --check-coverage is set (FR-G5 / T04.14). Without --suite "
        "the gate runs in matchers-only mode and reports every matcher "
        "as uncovered."
    ),
)
def doctor(
    as_json: bool,
    no_mcp: bool,
    check_coverage: bool,
    output_dir: Optional[Path],
    parallel: Optional[int],
    suite: Optional[str],
) -> None:
    """Verify host preconditions for ``superclaude eval run``.

    Exit codes:

    * ``0`` — every HARD capability satisfied.
    * ``2`` — at least one HARD capability failed, ``--output-dir``
      was supplied and escaped the OPS-002 / AC12 scratch-root policy,
      OR the host is not Linux (AC1 / R-109 — v1 is Linux-only;
      :data:`NON_LINUX_REFUSAL_TEMPLATE` is rendered to stderr citing
      DOC-OQ9 for the macOS follow-up). In every case the stderr
      artifact identifies the cause; for a scratch-root violation it
      quotes :data:`SCRATCH_ROOT_POLICY` verbatim so operators can
      correct the invocation without consulting the docs.
    """
    system = _default_platform_probe()
    if system != "Linux":
        click.echo(
            NON_LINUX_REFUSAL_TEMPLATE.format(system=system),
            err=True,
        )
        sys.exit(HARD_FAIL_EXIT_CODE)

    if output_dir is not None:
        try:
            resolve_scratch_root(output_dir)
        except ScratchRootViolation as exc:
            click.echo(
                f"eval doctor: {format_scratch_root_violation(exc)}",
                err=True,
            )
            sys.exit(SCRATCH_ROOT_VIOLATION_EXIT_CODE)

    skip_flags: tuple[str, ...] = ("--no-mcp",) if no_mcp else ()
    report = build_doctor_report(
        skip_flags=skip_flags,
        requested_parallel=parallel,
    )

    coverage_result: Optional[CoverageResult] = None
    if check_coverage:
        suite_specs: tuple[EvalSpec, ...] = ()
        if suite is not None:
            try:
                manifest_path = resolve_suite_manifest(suite, _DEFAULT_SUITES_DIR)
                parsed = SuiteLoader().load(manifest_path)
                suite_specs = parsed.evals
            except SuiteNotFound as exc:
                click.echo(f"eval doctor: {type(exc).__name__}: {exc}", err=True)
                sys.exit(SUITE_NOT_FOUND_EXIT_CODE)
            except SuiteLoaderError as exc:
                click.echo(f"eval doctor: {type(exc).__name__}: {exc}", err=True)
                sys.exit(SUITE_LOADER_ERROR_EXIT_CODE)
        coverage_result = coverage_gate(
            settings_path=Path.home() / ".claude" / "settings.json",
            suite=suite_specs,
            output_dir=None,
        )

    if as_json:
        payload = doctor_payload(
            report,
            check_coverage=check_coverage,
            coverage_result=coverage_result,
        )
        click.echo(json.dumps(payload, indent=2, sort_keys=True))
    else:
        click.echo(render_checklist(report))
        if check_coverage and coverage_result is not None:
            click.echo(_format_coverage_summary(coverage_result))

    # NFR-PERF2 SOFT-SKIP warning: when ``--parallel >= 15`` was requested
    # and the host could not certify the free-RAM budget, emit a stderr
    # warning containing the literal :data:`RAM_CEILING_TEXT` token. The
    # warning fires regardless of ``--json`` so CI logs and machine
    # consumers see the same signal — the JSON payload still carries the
    # row under ``soft_skips`` for structured parsing.
    ram_row = next(
        (r for r in report.report if r.name == "host.free_ram_for_max_parallel"),
        None,
    )
    if ram_row is not None and not ram_row.passed:
        click.echo(
            f"eval doctor: NFR-PERF2 warning: {ram_row.detail}",
            err=True,
        )

    if report.hard_failures:
        click.echo(render_hard_failure_artifact(report), err=True)
        sys.exit(HARD_FAIL_EXIT_CODE)

    if coverage_result is not None and not coverage_result.passed:
        click.echo(_format_coverage_missing_roster(coverage_result), err=True)
        sys.exit(COVERAGE_GATE_FAILED_EXIT_CODE)


@eval_group.command("list")
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    help="Emit a JSON array of {name, version, eval_count} entries.",
)
@click.option(
    "--suites-dir",
    "suites_dir",
    type=click.Path(file_okay=False, path_type=Path),
    default=None,
    help=(
        "Override the suite manifest directory. Defaults to "
        "src/superclaude/cli/eval/suites/."
    ),
)
def eval_list(as_json: bool, suites_dir: Optional[Path]) -> None:
    """Enumerate suite manifests under ``cli/eval/suites/``.

    Each row reports the manifest ``name``, ``version`` field, and the
    post-parameterize-expansion eval count. An empty or missing suites
    directory prints ``(no suites found)`` and still exits ``0``.

    Exit codes:

    * ``0`` — every discovered manifest loaded green (or no manifests
      found).
    * ``2`` (``SUITE_LOADER_ERROR_EXIT_CODE``) — at least one manifest
      failed schema validation, eval-id regex, or capability resolution;
      the stderr line names the offending manifest and the typed error
      class so operators can locate the failure.
    """

    target = suites_dir if suites_dir is not None else _DEFAULT_SUITES_DIR
    try:
        summaries = summarize_suites(target)
    except SuiteLoaderError as exc:  # type: ignore[misc]
        click.echo(
            f"eval list: {type(exc).__name__}: {exc}",
            err=True,
        )
        sys.exit(SUITE_LOADER_ERROR_EXIT_CODE)

    if as_json:
        click.echo(json.dumps(list_payload(summaries), indent=2, sort_keys=True))
    else:
        click.echo(render_list_text(summaries))


# ---------------------------------------------------------------------------
# FR-CLI3 ``eval describe`` (T01.22 / D-0019)
# ---------------------------------------------------------------------------


SUITE_NOT_FOUND_EXIT_CODE: int = _exit_codes.USAGE_ERROR
"""Process exit code emitted when :class:`SuiteNotFound` reaches the CLI.
Canonical value: ``exit_codes.USAGE_ERROR`` (CC2 / OQ-2). Mirrors
:data:`SUITE_LOADER_ERROR_EXIT_CODE` for operator-visible parity.
"""


EVAL_NOT_FOUND_EXIT_CODE: int = _exit_codes.USAGE_ERROR
"""Process exit code emitted when :class:`EvalNotFound` reaches the CLI.
Canonical value: ``exit_codes.USAGE_ERROR`` (CC2 / OQ-2).
"""


class SuiteNotFound(Exception):
    """Raised when ``--suite <name>`` resolves to no manifest on disk.

    Carries the requested ``suite`` token and the ``suites_dir`` that was
    searched so the stderr line names both. CLI callers MUST map this to
    :data:`SUITE_NOT_FOUND_EXIT_CODE` (= 2).
    """

    def __init__(self, suite: str, suites_dir: Path) -> None:
        self.suite = suite
        self.suites_dir = suites_dir
        super().__init__(f"no manifest matched --suite {suite!r} in {suites_dir}")


class EvalNotFound(Exception):
    """Raised when ``--eval <id>`` does not match a post-expansion eval id.

    Carries the requested ``eval_id`` plus the suite ``name`` and the
    sorted tuple of known ids so the stderr line is forensic. CLI callers
    MUST map this to :data:`EVAL_NOT_FOUND_EXIT_CODE` (= 2).
    """

    def __init__(
        self,
        eval_id: str,
        suite_name: str,
        known_ids: Iterable[str],
    ) -> None:
        self.eval_id = eval_id
        self.suite_name = suite_name
        self.known_ids: tuple[str, ...] = tuple(known_ids)
        known = ", ".join(self.known_ids) if self.known_ids else "<none>"
        super().__init__(
            f"eval {eval_id!r} not in suite {suite_name!r} (known: {known})"
        )


def _evalspec_to_dict(spec: EvalSpec) -> dict:
    """Project an ``EvalSpec`` into a manifest-shaped dict.

    Field ordering matches ``suite.schema.json`` so YAML/JSON output is
    deterministic and round-trips visually against the source manifest.
    Optional fields are omitted when they hold their dataclass default
    (e.g. ``category=""``, empty tuples, ``timeout_sec=None``) so the
    "no editorial transformation" guarantee from T01.22 Notes holds: an
    eval that did not declare ``category:`` in YAML does not gain one
    here.
    """

    payload: dict[str, Any] = {
        "id": spec.id,
        "title": spec.title,
    }
    if spec.category:
        payload["category"] = spec.category
    if spec.requires:
        payload["requires"] = list(spec.requires)
    if spec.timeout_sec is not None:
        payload["timeout_sec"] = spec.timeout_sec
    if spec.isolation is not None:
        payload["isolation"] = dict(spec.isolation)
    if spec.inputs:
        payload["inputs"] = [dict(row) for row in spec.inputs]
    if spec.expects:
        payload["expects"] = [dict(row) for row in spec.expects]
    if spec.parameterize:
        payload["parameterize"] = [dict(row) for row in spec.parameterize]
    if spec.no_pty is not None:
        payload["no_pty"] = spec.no_pty
    return payload


def _parsed_suite_to_dict(parsed: ParsedSuite) -> dict:
    """Project a :class:`ParsedSuite` into the manifest envelope shape.

    ``evals`` is the post-parameterize-expansion list (the canonical
    "what would run if you invoked ``eval run``" view per FR-CLI3 AC).
    Suite-level fields are verbatim from the manifest so the output
    mirrors the validated source byte-for-byte modulo the ``evals``
    expansion.
    """

    return {
        "name": parsed.name,
        "version": parsed.version,
        "description": parsed.description,
        "defaults": dict(parsed.defaults),
        "required_binaries": [dict(row) for row in parsed.required_binaries],
        "optional_capabilities": [dict(row) for row in parsed.optional_capabilities],
        "evals": [_evalspec_to_dict(spec) for spec in parsed.evals],
    }


def resolve_suite_manifest(suite: str, suites_dir: Path) -> Path:
    """Resolve ``--suite <token>`` to a manifest path on disk.

    Resolution precedence (first match wins):

    1. ``token`` is itself a file path that exists → return it.
    2. ``suites_dir / f"{token}.yaml"`` exists → return it (filename stem
       convention used by the built-in suites).
    3. Otherwise scan ``suites_dir`` and return the first manifest whose
       schema-validated ``name`` field equals ``token``. Broken manifests
       in the same directory are skipped silently — we only fail on the
       *requested* suite, not on the neighbours.

    Raises:
        SuiteNotFound: No manifest matched the token under any rule. CLI
            callers map this to :data:`SUITE_NOT_FOUND_EXIT_CODE` (= 2).
    """

    candidate = Path(suite)
    if candidate.is_file():
        return candidate

    by_filename = suites_dir / f"{suite}.yaml"
    if by_filename.is_file():
        return by_filename

    loader = SuiteLoader()
    for manifest_path in discover_suite_manifests(suites_dir):
        try:
            parsed = loader.load(manifest_path)
        except SuiteLoaderError:
            # Neighbour manifest is broken; don't let it mask the lookup.
            continue
        if parsed.name == suite:
            return manifest_path

    raise SuiteNotFound(suite, suites_dir)


def describe_suite(
    suite: str,
    *,
    suites_dir: Path,
    eval_id: Optional[str] = None,
    loader: Optional[SuiteLoader] = None,
) -> dict:
    """Resolve, load, and project a suite (optionally a single eval).

    Validation runs via :class:`SuiteLoader` BEFORE any rendering, so
    schema / id-regex / capability rejections raise before the caller
    can produce stdout (FR-CLI3 AC: validate before print).

    Args:
        suite: Suite name, filename stem, or direct manifest path. See
            :func:`resolve_suite_manifest` for resolution precedence.
        suites_dir: Directory to search when ``suite`` is not a direct
            path. Tests inject a tmp dir via ``--suites-dir``.
        eval_id: Optional post-expansion eval id (``E1``, ``E2.1``) to
            filter the output to a single eval. Missing → ``EvalNotFound``.
        loader: Injectable :class:`SuiteLoader` for tests that need to
            stub capability resolution.

    Returns:
        A dict suitable for ``yaml.safe_dump`` / ``json.dumps``. When
        ``eval_id`` is ``None``, the dict is the full manifest envelope;
        when ``eval_id`` is set, the dict is a single ``evalEntry`` shape
        (the same projection :func:`_evalspec_to_dict` produces).

    Raises:
        SuiteNotFound: Resolution rule chain produced no manifest.
        EvalNotFound: ``eval_id`` did not match any post-expansion id.
        SchemaError / InvalidEvalId / UnresolvedCapability: Propagated
            from :class:`SuiteLoader` so the CLI exit-code map still
            applies (all → 2).
    """

    manifest_path = resolve_suite_manifest(suite, suites_dir)
    active_loader = loader if loader is not None else SuiteLoader()
    parsed: ParsedSuite = active_loader.load(manifest_path)

    if eval_id is None:
        return _parsed_suite_to_dict(parsed)

    for spec in parsed.evals:
        if spec.id == eval_id:
            return _evalspec_to_dict(spec)
    raise EvalNotFound(
        eval_id=eval_id,
        suite_name=parsed.name,
        known_ids=sorted(spec.id for spec in parsed.evals),
    )


def render_describe_yaml(payload: dict) -> str:
    """Render a describe payload as a deterministic YAML document.

    ``sort_keys=False`` preserves the manifest field ordering produced by
    :func:`_parsed_suite_to_dict` / :func:`_evalspec_to_dict` so the
    YAML output reads like the source manifest. ``default_flow_style=False``
    keeps block-style for human review.
    """

    return yaml.safe_dump(
        payload,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
    )


def render_describe_json(payload: dict) -> str:
    """Render a describe payload as a deterministic JSON document.

    ``sort_keys=True`` guarantees byte-level stability across hosts and
    Python versions (matching the ``eval list --json`` contract).
    """

    return json.dumps(payload, indent=2, sort_keys=True)


@eval_group.command("describe")
@click.option(
    "--suite",
    "suite",
    required=True,
    help=(
        "Suite name, filename stem, or path to a manifest. Name lookup "
        "matches the manifest 'name:' field; stem lookup matches "
        "'<suites-dir>/<token>.yaml'."
    ),
)
@click.option(
    "--eval",
    "eval_id",
    default=None,
    help=(
        "Filter output to a single post-expansion eval id "
        "(e.g. 'E1' or 'E2.1'). Missing id exits 2 with EvalNotFound."
    ),
)
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    help="Emit JSON instead of YAML (default is YAML).",
)
@click.option(
    "--suites-dir",
    "suites_dir",
    type=click.Path(file_okay=False, path_type=Path),
    default=None,
    help=(
        "Override the suite manifest directory used for name/stem "
        "lookups. Defaults to src/superclaude/cli/eval/suites/."
    ),
)
def eval_describe(
    suite: str,
    eval_id: Optional[str],
    as_json: bool,
    suites_dir: Optional[Path],
) -> None:
    """Print a validated, post-parameterize-expansion manifest.

    Output mirrors the validated manifest with no editorial
    transformation. ``evals[]`` is the post-expansion list so a
    parameterized row produces one entry per row in the output.

    Exit codes:

    * ``0`` — manifest validated and printed.
    * ``2`` — schema / id-regex / capability rejection, missing suite
      (``SuiteNotFound``), or missing eval id (``EvalNotFound``). The
      stderr line names the typed error class so operators can locate
      the failure without parsing tracebacks.
    """

    target = suites_dir if suites_dir is not None else _DEFAULT_SUITES_DIR

    try:
        payload = describe_suite(
            suite,
            suites_dir=target,
            eval_id=eval_id,
        )
    except SuiteNotFound as exc:
        click.echo(f"eval describe: {type(exc).__name__}: {exc}", err=True)
        sys.exit(SUITE_NOT_FOUND_EXIT_CODE)
    except EvalNotFound as exc:
        click.echo(f"eval describe: {type(exc).__name__}: {exc}", err=True)
        sys.exit(EVAL_NOT_FOUND_EXIT_CODE)
    except SuiteLoaderError as exc:  # type: ignore[misc]
        click.echo(
            f"eval describe: {type(exc).__name__}: {exc}",
            err=True,
        )
        sys.exit(SUITE_LOADER_ERROR_EXIT_CODE)

    if as_json:
        click.echo(render_describe_json(payload))
    else:
        # safe_dump terminates with a trailing newline; click.echo adds
        # another, so strip to keep output tidy and snapshot-stable.
        click.echo(render_describe_yaml(payload).rstrip("\n"))


# ---------------------------------------------------------------------------
# T04.10 FR-CLI1 ``eval run`` body helpers (D-0072)
# ---------------------------------------------------------------------------
#
# Eight module-private helpers consumed by :func:`eval_run`. They are
# module-level (not nested in the command) so :mod:`tests.cli.eval` can
# import + monkeypatch them, and so the closure inside ``eval_run`` keeps
# a small, readable signature.
#
# Three of the eight are run-id / output-dir / executor wiring (anchored
# on the FR-G4 ``artifact_layout`` module); two are stats + summary-line
# rendering; one is a UTC ISO clock helper; one is a signal-handler
# install guard; one is the per-spec runner driver.


def _utc_iso_now() -> str:
    """Return the current UTC instant as an ISO 8601 ``...Z`` string.

    Used both for the ``RunSummary.started_at`` / ``finished_at`` stamps
    AND as the seed for :func:`compose_run_id` so the run-id and the
    summary timestamps share one clock read.
    """
    return (
        datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    )


def _new_run_id(*, started_at: str, suite_name: str) -> str:
    """Return the FR-G4 deterministic run-id for ``(started_at, suite_name)``.

    Thin wrapper over :func:`artifact_layout.compose_run_id` so callers in
    this module can invoke it without re-importing the layout module at
    every call site. The wrapper exists for symbol-contract reasons:
    ``tests/cli/eval/test_single_command.py`` asserts ``_new_run_id`` is
    importable from this module; delegating keeps the FR-G4
    single-source-of-truth invariant.
    """
    return compose_run_id(started_at, suite_name)


def _default_output_dir(*, started_at: str, suite_name: str) -> Path:
    """Return the default per-run output directory under the AC12 prefix.

    Anchored on :func:`artifact_layout.compose_run_dir` so the layout
    matches FR-G4 / D-0074 exactly: ``<cwd>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/``.
    The path is **constructed**, not created — :func:`eval_run` funnels
    it through :func:`resolve_scratch_root` before any ``mkdir``.
    """
    return compose_run_dir(Path.cwd(), started_at, suite_name)


def _can_install_signal_handler() -> bool:
    """Return ``True`` when this thread can install POSIX signal handlers.

    :class:`SignalHandlerInstaller` is main-thread-only. Click's
    :class:`CliRunner` invokes commands on the main thread by default;
    pytest's threaded runners may not. The check guards the install so a
    non-main-thread invocation degrades gracefully (cancellation still
    works via the orchestrator's own token wiring) instead of raising
    ``ValueError: signal only works in main thread``.
    """
    import threading

    return threading.current_thread() is threading.main_thread()


class _NullLifecycleExecutor:
    """Zero-side-effect :class:`LifecycleExecutor` for the M2/M3 surface.

    Production wiring (``ClaudeProcessAdapter`` + ``PtyDriver``) lands in
    M5 / M6 when the vendored PTY harness is on disk. Until then the
    only operator-reachable green path is ``--no-pty``, which
    short-circuits every spec in ``real.yaml`` (DOC-OQ3 / R-077 tags
    every E1-E15 ``no_pty: skip``) **before** ``run_one`` calls
    :func:`_run_one_spec`. The null executor's three methods therefore
    only fire on synthetic tests or future suites whose specs are NOT
    PTY-tagged; they return canned values so ``run_eval`` flows
    end-to-end without spawning a subprocess.
    """

    def spawn(self, ctx: ExecutorContext) -> None:
        return None

    def inject(self, ctx: ExecutorContext) -> None:
        return None

    def observe(self, ctx: ExecutorContext) -> ObservedRun:
        return ObservedRun(
            exit_code=0,
            stdout="",
            stderr="",
            duration_sec=0.0,
        )


def _resolve_executor_factory() -> Callable[..., LifecycleExecutor]:
    """Return the factory that constructs a per-eval :class:`LifecycleExecutor`.

    Production wiring (``ClaudeProcessAdapter`` + ``PtyDriver``) lands
    with the vendored PTY harness (M5 / M6). Until then this factory
    returns the :class:`_NullLifecycleExecutor` documented above. Tests
    monkeypatch this function to inject canned executors.

    The returned factory is tagged with ``produces_null_executor = True``
    so the one-shot WARNING probe in ``run_eval`` can classify it
    without instantiating an executor. Constructor side-effects in
    future real executors (PTY descriptors, helper threads, scratch
    dirs) would otherwise leak resources before orchestration starts.
    """

    def factory(**_kwargs: Any) -> LifecycleExecutor:
        return _NullLifecycleExecutor()  # type: ignore[return-value]

    factory.produces_null_executor = True  # type: ignore[attr-defined]
    return factory


def _run_one_spec(
    spec: EvalSpec,
    *,
    run_id: str,
    run_dir: Path,
    home_root: Path,
    config: EvalConfig,
    timeout_mult: float,
    keep_home: bool,
    cancellation_token: CancellationToken,
    executor_factory: Callable[..., LifecycleExecutor],
) -> EvalOutcome:
    """Build a :class:`HomeIsolation` + :class:`EvalRunner` for one spec and run it.

    This is the per-spec worker the ``run_one`` closure delegates to
    after the ``--no-pty`` short-circuit. Each call:

    1. Allocates the per-eval subtree under ``run_dir`` via
       :func:`allocate_per_eval_paths` (FR-G4 layout invariants).
    2. Constructs a fresh :class:`HomeIsolation` rooted at ``home_root``.
       ``session_id`` is allocated by :func:`orchestrator.allocate_session_id`
       per M5 — identifier policy lives in the orchestrator so the value is
       (run_id, eval_id)-deterministic and orthogonal across runs.
    3. Wires the executor + an empty ``expect_callables`` tuple. The
       expects resolver (manifest ``expects:`` row → callable) lands in
       a follow-up; for now every spec that survives the ``--no-pty``
       short-circuit returns PASS via the null executor.
    4. Folds ``timeout_mult`` into the runner's ``default_timeout_sec``
       so the operator's ``--timeout-mult`` scales every spec uniformly.

    The function deliberately raises no business exceptions — any
    :class:`HomeContainmentViolation` or constructor error bubbles up
    to :meth:`RunOrchestrator._invoke_worker`, which folds it into an
    ``ERRORED`` outcome.
    """

    paths = allocate_per_eval_paths(run_dir, spec.id, create=True)

    home = HomeIsolation(
        eval_id=spec.id,
        home_root=home_root,
        session_id=allocate_session_id(run_id=run_id, eval_id=spec.id),
    )

    executor = executor_factory()

    # ``timeout_sec`` on the spec is authoritative when set; the
    # multiplier scales the suite-wide fallback the orchestrator wires.
    # Spec-level timeouts ignore the multiplier per FR-CLI1 — operators
    # who want per-spec scaling edit the manifest.
    spec_timeout = spec.timeout_sec
    default_timeout: Optional[float] = None
    if spec_timeout is not None and spec_timeout > 0:
        default_timeout = float(spec_timeout) * float(timeout_mult)

    runner = EvalRunner(
        home=home,
        config=config,
        executor=executor,
        run_dir=run_dir,
        artifacts_dir=paths.artifacts_dir,
        stdout_path=paths.artifacts_dir / "stdout.log",
        stderr_path=paths.artifacts_dir / "stderr.log",
        transcript_path=paths.tty_transcript,
        expect_callables=(),
        keep_home_on_pass=keep_home,
        default_timeout_sec=default_timeout,
        cancellation_token=cancellation_token,
    )

    return runner.run(spec)


def _compute_run_stats(
    outcomes: Sequence[EvalOutcome],
    *,
    manifest_n: int,
) -> tuple[RunCounts, RunTotals]:
    """Tally outcomes into ``(RunCounts, RunTotals)`` for :class:`RunSummary`.

    ``manifest_n`` is the pre-expansion row count the loader returned;
    ``expanded_n_prime`` is ``len(outcomes)`` because the orchestrator
    guarantees one outcome per expanded spec (D-0057 / RunOrchestrator
    contract). ``kept_k`` counts outcomes with a terminal lifecycle
    status; ``skipped_s`` counts SKIPPED + INTERRUPTED per DM-012.

    The XFAIL / XPASS rollup follows DM-012 verbatim:

    * ``XFAIL`` → ``passed`` (expected failure is a pass at the suite level).
    * ``XPASS`` → ``failed`` (unexpected pass signals stale ``xfail`` markers).
    """
    expanded = len(outcomes)
    # M3: DM-012 partitions derived from the EVAL_STATUSES SoT (models.py:62)
    # via the SKIPPED_STATUSES / PASSED_STATUSES / FAILED_STATUSES constants.
    # Deriving rather than hardcoding ensures that adding a new EvalStatus
    # value cannot silently drift this tally out of sync with the canonical
    # set. ``kept_statuses`` is everything in EVAL_STATUSES minus the
    # non-terminal SKIPPED + INTERRUPTED buckets.
    kept_statuses = frozenset(EVAL_STATUSES) - SKIPPED_STATUSES

    kept = sum(1 for o in outcomes if o.status in kept_statuses)
    skipped = sum(1 for o in outcomes if o.status in SKIPPED_STATUSES)

    counts = RunCounts(
        manifest_n=manifest_n,
        expanded_n_prime=expanded,
        kept_k=kept,
        skipped_s=skipped,
        kept_plus_skipped_equals_n_prime=(kept + skipped == expanded),
    )

    totals = RunTotals(
        passed=sum(1 for o in outcomes if o.status in PASSED_STATUSES),
        failed=sum(1 for o in outcomes if o.status in FAILED_STATUSES),
        skipped=sum(1 for o in outcomes if o.status == "SKIPPED"),
        errored=sum(1 for o in outcomes if o.status == "ERRORED"),
        interrupted=sum(1 for o in outcomes if o.status == "INTERRUPTED"),
        timeout=sum(1 for o in outcomes if o.status == "TIMEOUT"),
    )
    return counts, totals


def _format_run_summary_line(summary: RunSummary, output_dir: Path) -> str:
    """Return the human one-liner ``eval run --verbose`` prints to stdout.

    H3: shape covers the full DM-012 status taxonomy — ``run <id>:
    <P>P/<F>F/<S>S/<E>E/<I>I/<T>T in <duration>s -> <output_dir>``. The
    six buckets cover all 8 EvalStatus literals (XFAIL rolls into
    ``passed``; XPASS rolls into ``failed`` per the RunTotals docstring).
    Pure formatting, no I/O.
    """
    totals = summary.totals
    return (
        f"run {summary.run_id}: "
        f"{totals.passed}P/"
        f"{totals.failed}F/"
        f"{totals.skipped}S/"
        f"{totals.errored}E/"
        f"{totals.interrupted}I/"
        f"{totals.timeout}T "
        f"in {summary.duration_sec:.2f}s "
        f"-> {output_dir}"
    )


@eval_group.command("run")
@click.option(
    "--suite",
    "suite",
    required=True,
    help=(
        "Suite name, filename stem, or path to a manifest. Same lookup "
        "rules as ``eval describe`` (filesystem path → stem → name field)."
    ),
)
@click.option(
    "--parallel",
    "parallel",
    type=int,
    default=RunOrchestrator.DEFAULT_PARALLEL,
    show_default=True,
    help=(
        "Worker concurrency. Values below 1 clamp to 1; values above 15 "
        "clamp to 15 (design-spec §11)."
    ),
)
@click.option(
    "--eval",
    "eval_ids",
    multiple=True,
    help=(
        "Filter to one or more post-expansion eval ids (e.g. 'E1' or 'E2.1'). "
        "Repeat for multiple ids. Empty selection exits 2 with EvalNotFound."
    ),
)
@click.option(
    "--no-mcp",
    "no_mcp",
    is_flag=True,
    help="Mark MCP capabilities as skipped-by-flag (FR-CLI1 / FR-G4).",
)
@click.option(
    "--no-pty",
    "no_pty",
    is_flag=True,
    help="Run without the vendored PTY harness (degrades stdout capture).",
)
@click.option(
    "--output-dir",
    "output_dir",
    type=click.Path(file_okay=False, path_type=Path),
    default=None,
    help=(
        "Destination directory for ``summary.{md,json,yaml}`` / ``junit.xml`` / "
        "per-eval artifacts. Resolved through the AC12 scratch-root allowlist. "
        "Defaults to ``.dev/eval-runs/<run-id>/``."
    ),
)
@click.option(
    "--keep-home",
    "keep_home",
    is_flag=True,
    help=(
        "Preserve per-eval HOME directories on PASS (default removes them). "
        "Forwarded to ``EvalRunner.keep_home_on_pass``."
    ),
)
@click.option(
    "--timeout-mult",
    "timeout_mult",
    type=float,
    default=1.0,
    show_default=True,
    help=(
        "Multiplier applied to each spec's ``timeout_sec`` before it reaches "
        "``EvalRunner.default_timeout_sec``. Must be > 0."
    ),
)
@click.option(
    "--max-disk-mb",
    "max_disk_mb",
    type=int,
    default=DEFAULT_DISK_BUDGET_MB,
    show_default=True,
    help=(
        "Disk-budget ceiling for ``output_dir`` in megabytes. ``0`` disables "
        "the poller entirely (NFR-PERF4)."
    ),
)
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    help="Emit the run summary as JSON to stdout in addition to writing it to disk.",
)
@click.option(
    "--verbose",
    "verbose",
    is_flag=True,
    help="Print a human-readable summary line to stdout when the run finishes.",
)
@click.option(
    "--junit",
    "junit",
    is_flag=True,
    help="Also write a JUnit XML report (``junit.xml``) into ``output_dir``.",
)
def eval_run(
    suite: str,
    parallel: int,
    eval_ids: tuple[str, ...],
    no_mcp: bool,
    no_pty: bool,
    output_dir: Optional[Path],
    keep_home: bool,
    timeout_mult: float,
    max_disk_mb: int,
    as_json: bool,
    verbose: bool,
    junit: bool,
) -> None:
    """Run a cliEval suite end-to-end (FR-CLI1 / D-0072).

    Wires the twelve FR-CLI1 flags to :class:`RunOrchestrator`,
    :class:`CapabilityGates`, the :class:`Reporter`, and the
    :class:`DiskBudgetPoller`. Each spec is executed inside its own
    per-eval HOME (``HomeIsolation``) under the resolved ``--output-dir``
    so the AC12 scratch-root allowlist remains the single source of truth
    for filesystem writes.

    Exit codes (design-spec §4):

    * ``0`` — every expanded eval reached a terminal PASS / SKIPPED /
      XFAIL outcome and no breach occurred.
    * ``1`` — at least one eval ended in FAIL, ERRORED, TIMEOUT, or XPASS.
    * ``2`` — harness-level rejection (invalid flag, scratch-root
      violation, suite not found, disk-budget exceeded, etc.).
    * ``3`` — the operator interrupted the run (SIGINT/SIGTERM cooperative
      cancellation).
    """

    # ------------------------------------------------------------------
    # Flag validation + clamping (design-spec §11)
    # ------------------------------------------------------------------
    if parallel < RunOrchestrator.MIN_PARALLEL:
        parallel = RunOrchestrator.MIN_PARALLEL
    elif parallel > RunOrchestrator.MAX_PARALLEL:
        parallel = RunOrchestrator.MAX_PARALLEL

    if timeout_mult <= 0:
        click.echo(
            f"eval run: --timeout-mult must be > 0; got {timeout_mult}",
            err=True,
        )
        sys.exit(HARD_FAIL_EXIT_CODE)

    if max_disk_mb < 0:
        click.echo(
            f"eval run: --max-disk-mb must be >= 0; got {max_disk_mb} "
            "(use 0 to disable the budget)",
            err=True,
        )
        sys.exit(HARD_FAIL_EXIT_CODE)

    # ------------------------------------------------------------------
    # Output dir + AC12 scratch-root allowlist
    # ------------------------------------------------------------------
    base_config = EvalConfig()
    # Single clock read for the run: feeds both the FR-G4 deterministic
    # run-id and the ``RunSummary.started_at`` stamp below.
    started_iso = _utc_iso_now()
    suite_name = str(suite)
    run_id = _new_run_id(started_at=started_iso, suite_name=suite_name)
    # H1: --output-dir is the OUTPUT ROOT, not the run-dir. The run-dir is
    # uniformly composed via ``compose_run_dir`` (FR-G4 layout
    # ``<root>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/``) so artifacts land at
    # the same shape whether the operator supplies a root or the default
    # cwd-anchored root is used. The flat-layout branch (--output-dir
    # treated as the run-dir directly) is deleted per the H1 spec.
    try:
        if output_dir is not None:
            # OPS-002 / AC12: validate the operator-supplied root, then
            # derive the run-dir uniformly via compose_run_dir.
            resolved_output_root = resolve_scratch_root(
                output_dir,
                config=base_config,
            )
            resolved_run_dir = compose_run_dir(
                resolved_output_root, started_iso, suite_name
            )
        else:
            # Default flow: ``_default_output_dir`` already returns the
            # FR-G4 run-dir anchored at ``Path.cwd()`` via ``compose_run_dir``
            # so a second wrap is unnecessary. The output root is the
            # canonical ``<cwd>/.dev/eval-runs`` prefix; resolve_scratch_root
            # validates the run-dir lives under the default allowlist.
            default_run_dir = _default_output_dir(
                started_at=started_iso, suite_name=suite_name
            )
            resolved_run_dir = resolve_scratch_root(default_run_dir, config=base_config)
            resolved_output_root = resolved_run_dir
    except ScratchRootViolation as exc:
        click.echo(format_scratch_root_violation(exc), err=True)
        sys.exit(SCRATCH_ROOT_VIOLATION_EXIT_CODE)

    resolved_run_dir.mkdir(parents=True, exist_ok=True)
    home_root = resolved_run_dir / "homes"

    # The runtime EvalConfig extends the canonical allowlist with the
    # per-run run-dir + home root + the operator-supplied output root so
    # downstream ``containment_guard`` calls see a stable allowlist rather
    # than re-deriving one from scratch.
    #
    # H5a (OPS-002 ordering site 1): allowlist extension happens BEFORE the
    # ``home_root.mkdir`` below so the path is in the allowlist at the
    # moment of any filesystem write. No mkdir of home_root has happened
    # yet at this line.
    runtime_allowed = tuple(base_config.allowed_scratch_roots) + (
        resolved_output_root,
        resolved_run_dir,
        home_root,
    )
    runtime_config = EvalConfig(
        paths=base_config.paths,
        defaults=base_config.defaults,
        allowed_scratch_roots=runtime_allowed,
        min_claude_version=base_config.min_claude_version,
    )

    # H5a (OPS-002 ordering site 1): mkdir home_root NOW, AFTER allowlist
    # extension. Restores OPS-002 invariant "no filesystem write before
    # allowlist validation".
    home_root.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Suite resolution + parse + post-expansion filter
    # ------------------------------------------------------------------
    try:
        manifest_path = resolve_suite_manifest(suite, _DEFAULT_SUITES_DIR)
    except SuiteNotFound as exc:
        click.echo(f"eval run: {type(exc).__name__}: {exc}", err=True)
        sys.exit(SUITE_NOT_FOUND_EXIT_CODE)

    loader = SuiteLoader()
    try:
        parsed = loader.load(manifest_path)
    except SuiteLoaderError as exc:
        click.echo(f"eval run: {type(exc).__name__}: {exc}", err=True)
        sys.exit(SUITE_LOADER_ERROR_EXIT_CODE)

    manifest_n = len(parsed.evals)
    specs: tuple[EvalSpec, ...] = parsed.evals
    if eval_ids:
        wanted = set(eval_ids)
        filtered = tuple(s for s in specs if s.id in wanted)
        missing = wanted - {s.id for s in filtered}
        if missing:
            click.echo(
                f"eval run: EvalNotFound: no specs match "
                f"{sorted(missing)} in suite={parsed.name!r}",
                err=True,
            )
            sys.exit(EVAL_NOT_FOUND_EXIT_CODE)
        specs = filtered

    # ------------------------------------------------------------------
    # FR-G5 hook-matcher coverage gate (T04.14 / D-0075)
    # ------------------------------------------------------------------
    # Runs BEFORE any worker dispatch so a missing-coverage breach
    # short-circuits the run without touching a per-eval HOME. Artifacts
    # land inside ``resolved_run_dir`` so the run directory still owns the
    # full forensic trail (FR-G4 contract). A missing or unreadable
    # ``settings.json`` is treated as the empty matcher set so dev hosts
    # without one stay green.
    coverage = coverage_gate(
        settings_path=Path.home() / ".claude" / "settings.json",
        suite=specs,
        output_dir=resolved_run_dir,
    )
    if not coverage.passed:
        click.echo(_format_coverage_missing_roster(coverage), err=True)
        sys.exit(COVERAGE_GATE_FAILED_EXIT_CODE)

    # ------------------------------------------------------------------
    # CapabilityGates (FR-G4): build the gate with the operator's
    # skip-flag selection so a future SuiteLoader resolver swap can
    # consume it; the doctor subcommand remains the dedicated HARD-row
    # checker so we deliberately do NOT call ``check_all()`` here.
    # ------------------------------------------------------------------
    skip_flags: list[str] = []
    if no_mcp:
        skip_flags.append("--no-mcp")
    if no_pty:
        skip_flags.append("--no-pty")
    _gates = CapabilityGates(skip_flags=tuple(skip_flags))
    del _gates  # construction is the wiring; instance unused at M2.

    # ------------------------------------------------------------------
    # Disk-budget poller, cancellation token, signal handler
    # ------------------------------------------------------------------
    poller = DiskBudgetPoller(
        resolved_run_dir,
        max_disk_mb=max_disk_mb,
        ensure_output_dir=True,
    )
    token = CancellationToken()

    # ------------------------------------------------------------------
    # Per-eval worker closure
    # ------------------------------------------------------------------
    executor_factory = _resolve_executor_factory()

    # M2: emit a one-shot stderr WARNING when the resolved factory returns
    # ``_NullLifecycleExecutor`` so operators cannot mistake null-runner
    # results for authoritative ones. Sampling once at orchestrator startup
    # (NOT inside ``_run_one_spec``) means the WARNING fires even when every
    # eval is SKIPPED via ``--no-pty``-and-``no_pty:skip`` short-circuit, and
    # a future test that monkeypatches ``_resolve_executor_factory`` to inject
    # a real executor will correctly NOT see the WARNING. The ``--json``
    # guard keeps machine-readable stdout clean — CliRunner mixes stderr
    # into stdout by default and downstream tools parsing the JSON payload
    # cannot tolerate the WARNING prefix.
    # We classify by inspecting the ``produces_null_executor`` attribute the
    # factory carries (set in ``_resolve_executor_factory``) rather than by
    # calling ``executor_factory()`` and discarding the result. When M5 / M6
    # lands ``ClaudeProcessAdapter + PtyDriver`` the real executor's
    # constructor will allocate PTY descriptors / helper threads / scratch
    # dirs; instantiating-and-discarding here would leak those resources
    # before per-spec orchestration even starts. Test monkeypatches that
    # inject real executors simply won't set the attribute, so the WARNING
    # correctly suppresses.
    if getattr(executor_factory, "produces_null_executor", False) and not as_json:
        click.echo(
            "eval run: WARNING: _NullLifecycleExecutor active — "
            "non-production executor selected; run results MUST NOT be "
            "treated as authoritative.",
            err=True,
        )

    def run_one(spec: EvalSpec) -> EvalOutcome:
        # DOC-OQ3 / R-077 / D-0077: honor the per-eval ``no_pty: skip``
        # tag when the operator passed ``--no-pty``. The skip happens
        # BEFORE any HomeIsolation.setup() call so PTY-required evals
        # never allocate a scratch HOME on hosts that cannot drive a
        # real TTY. Reporting matches the disk-budget skip shape so
        # ``RunCounts`` accounting and the Reporter render uniformly.
        if no_pty and spec.no_pty == "skip":
            return EvalOutcome(
                eval_id=spec.id,
                title=spec.title,
                status="SKIPPED",
                duration_sec=0.0,
                expects=(),
                skip_reason="--no-pty",
                skip_flag_triggered="--no-pty",
                artifacts={},
                error_class=None,
            )
        return _run_one_spec(
            spec,
            run_id=run_id,
            run_dir=resolved_run_dir,
            home_root=home_root,
            config=runtime_config,
            timeout_mult=timeout_mult,
            keep_home=keep_home,
            cancellation_token=token,
            executor_factory=executor_factory,
        )

    # ------------------------------------------------------------------
    # Orchestrate
    # ------------------------------------------------------------------
    # NOTE: ``started_iso`` was bound earlier (just before _new_run_id)
    # so the run-id and the RunSummary.started_at stamp share one clock
    # read. Do NOT re-read here.
    started_monotonic = time.monotonic()

    orchestrator = RunOrchestrator(
        run_one=run_one,
        cancellation_token=token,
        disk_budget_poller=poller,
    )

    try:
        # SignalHandlerInstaller is main-thread-only; the CliRunner-based
        # tests run on the main thread so this is safe by default.
        if SignalHandlerInstaller is not None and _can_install_signal_handler():
            with SignalHandlerInstaller(token):
                outcomes = orchestrator.run(specs, parallel=parallel)
        else:
            outcomes = orchestrator.run(specs, parallel=parallel)
    except ValueError as exc:
        # Parallel clamping above means this branch should not fire;
        # defend in depth anyway so a future refactor never crashes the
        # CLI with an unhandled ValueError.
        click.echo(f"eval run: orchestrator rejected request: {exc}", err=True)
        sys.exit(HARD_FAIL_EXIT_CODE)

    finished_iso = _utc_iso_now()
    duration_sec = time.monotonic() - started_monotonic

    # ------------------------------------------------------------------
    # Assemble RunSummary + write reports
    # ------------------------------------------------------------------
    counts, totals = _compute_run_stats(outcomes, manifest_n=manifest_n)

    artifacts: dict[str, str] = {}
    breach_path = poller.artifact_path() if poller.enabled else None
    if breach_path is not None:
        artifacts[DISK_BUDGET_EXCEEDED_ARTIFACT_NAME] = str(breach_path)

    summary = RunSummary(
        run_id=run_id,
        started_at=started_iso,
        finished_at=finished_iso,
        duration_sec=duration_sec,
        suite=str(manifest_path),
        manifest_version=parsed.version,
        parallel=parallel,
        counts=counts,
        totals=totals,
        evals=tuple(outcomes),
        artifacts=artifacts,
    )

    Reporter(summary=summary, emit_junit=junit).write(resolved_run_dir)

    # ------------------------------------------------------------------
    # Operator-facing stdout
    # ------------------------------------------------------------------
    if as_json:
        click.echo(
            json.dumps(summary.to_dict(), indent=2, sort_keys=False, default=str)
        )
    elif verbose:
        click.echo(_format_run_summary_line(summary, resolved_run_dir))

    # ------------------------------------------------------------------
    # Exit code (design-spec §4)
    # ------------------------------------------------------------------
    if token.is_cancelled():
        sys.exit(RUN_INTERRUPTED_EXIT_CODE)
    if poller.is_breached():
        # OPS-003 retention-policy advice: render the verbatim policy
        # string to stderr so operators reading the failing-CI log tail
        # learn (a) which run artifacts were preserved and (b) which
        # knobs (``--max-disk-mb`` / ``--keep-home``) to turn on the next
        # invocation. The string is pinned in
        # :data:`DISK_BUDGET_RETENTION_ADVICE`; ``docs/eval/retention.md``
        # quotes the same constant verbatim so the two surfaces cannot
        # drift apart.
        click.echo(DISK_BUDGET_RETENTION_ADVICE, err=True)
        sys.exit(DISK_BUDGET_EXCEEDED_EXIT_CODE)
    if totals.failed > 0 or totals.errored > 0 or totals.timeout > 0:
        sys.exit(RUN_FAILURES_EXIT_CODE)
    sys.exit(RUN_CLEAN_EXIT_CODE)
