"""Aggregated run report writer (FR-RPT1 / DM-012 / Deliverable D-0054).

This module implements the cliEval Reporter's writer half: given a
:class:`~superclaude.cli.eval.models.RunSummary` (T03.09 / DM-004) it
emits the three canonical artefacts under a caller-chosen output
directory:

* ``summary.md``  — human-readable run report (design-spec §9).
* ``summary.json`` — machine-readable run report matching
  ``summary.schema.json`` (T03.10 / DM-012).
* ``junit.xml``   — optional JUnit XML export (feature-gated; only
  emitted when ``emit_junit=True``).

The writer also enforces the FR-RPT1 N'-vs-K dimensional invariant:
``len(summary.evals) == summary.counts.expanded_n_prime``. When the
invariant is violated the writer raises
:class:`ReporterContractViolation` *before* any artefact is written;
callers map the exception to exit code 2 (design-spec §4: harness
contract error before any eval ran is exit 2, and a reporter contract
mismatch is the same class of bug — the orchestrator's accounting and
the evals list disagree).

The Reporter class (COMP-008 / T03.13) wraps this writer with the four
emitter methods (``to_markdown`` / ``to_yaml`` / ``to_json`` /
``to_junit``); this module is the file-emitting layer the class sits on
top of.
"""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Callable, Mapping

import yaml

from . import exit_codes as _exit_codes
from .models import EvalOutcome, RunSummary

__all__ = [
    "REPORTER_CONTRACT_VIOLATION_EXIT_CODE",
    "ReporterContractViolation",
    "render_summary_markdown",
    "render_summary_json",
    "render_junit_xml",
    "write_aggregated_report",
]


# Per design-spec §4: harness contract errors that surface *before* a
# meaningful run-result classification map to exit code 2. The reporter
# contract violation is in that class — the orchestrator and the
# reporter disagree on the row count, so the run itself is suspect.
# Canonical value: ``exit_codes.USAGE_ERROR`` (CC2 / OQ-2).
REPORTER_CONTRACT_VIOLATION_EXIT_CODE: int = _exit_codes.USAGE_ERROR


# Statuses that count as failure for the markdown headline. Mirrors the
# design-spec §9 "Status taxonomy" table: XPASS is a surprise success
# treated as a major signal.
_FAILURE_STATUSES: frozenset[str] = frozenset(
    {"FAIL", "ERRORED", "TIMEOUT", "INTERRUPTED", "XPASS"}
)


class ReporterContractViolation(RuntimeError):
    """Raised when the Reporter detects an N'-vs-K dimensional mismatch.

    FR-RPT1 declares ``len(evals[]) == counts.expanded_n_prime`` as the
    Reporter's load-bearing invariant. When the orchestrator emits a
    summary where the two disagree, the run's accounting is suspect and
    the writer refuses to emit any artefact — partial output that
    contradicts the manifest accounting would be more misleading than no
    output at all.

    The CLI dispatcher catches this exception and exits with
    :data:`REPORTER_CONTRACT_VIOLATION_EXIT_CODE` (= 2).
    """

    def __init__(
        self, *, expected: int, actual: int, run_id: str | None = None
    ) -> None:
        self.expected = expected
        self.actual = actual
        self.run_id = run_id
        run_clause = f" (run_id={run_id!r})" if run_id else ""
        super().__init__(
            "Reporter contract violation: "
            f"len(evals)={actual} != counts.expanded_n_prime={expected}"
            f"{run_clause}. FR-RPT1 requires every expanded EvalSpec to be "
            "present in evals[] (SKIPPED rows stay in the list)."
        )


def _check_invariant(summary: RunSummary) -> None:
    """Enforce FR-RPT1 ``len(evals) == counts.expanded_n_prime``.

    Raised *before* any file is written so the writer never leaves a
    partial summary on disk that contradicts the manifest accounting.
    """

    expected = summary.counts.expanded_n_prime
    actual = len(summary.evals)
    if expected != actual:
        raise ReporterContractViolation(
            expected=expected, actual=actual, run_id=summary.run_id
        )


# ---------------------------------------------------------------------------
# Markdown renderer
# ---------------------------------------------------------------------------


def _format_duration(seconds: float) -> str:
    """Render a duration in a human-readable form (Xm Ys or Y.Ys).

    Stable across Python versions; sub-second values keep one decimal so
    the markdown table does not flatten 0.05s vs 0.5s into "0s".
    """

    if seconds >= 60:
        minutes, rem = divmod(seconds, 60)
        return f"{int(minutes)}m {rem:.1f}s"
    return f"{seconds:.1f}s"


def _row_note(outcome: EvalOutcome) -> str:
    """Pick a short note for the per-eval markdown row."""

    if outcome.status == "SKIPPED":
        if outcome.skip_reason:
            return outcome.skip_reason
        return "—"
    if outcome.status == "ERRORED" and outcome.error_class:
        return outcome.error_class
    return "—"


def render_summary_markdown(summary: RunSummary) -> str:
    """Return the ``summary.md`` body as a single string.

    Output shape follows design-spec §9 (human-readable summary):

    * Header line: ``# Eval Run: <started_at> / <run_id>``.
    * Meta line:   ``**Suite:** ... | **Parallel:** N | **Duration:** ...``
    * Result line: ``## Result: passed/failed/skipped tally``.
    * Per-eval table with ``ID | Title | Status | Duration | Notes``.
    * Failures block: per-failure detail block with title, expects, and
      artifacts when present.
    * Counts block: rendered last so reviewers can sanity-check the
      N'-vs-K accounting against the table above.

    Trailing newline so concatenation with downstream content stays
    clean. Byte-stable for a given ``RunSummary`` (the input dataclass
    is frozen; iteration follows the tuple ordering the orchestrator
    constructed).
    """

    _check_invariant(summary)

    totals = summary.totals
    counts = summary.counts

    lines: list[str] = []
    lines.append(f"# Eval Run: {summary.started_at} / {summary.run_id}")
    lines.append(
        f"**Suite:** {summary.suite} | **Parallel:** {summary.parallel} | "
        f"**Duration:** {_format_duration(summary.duration_sec)}"
    )
    lines.append("")
    lines.append(
        "## Result: "
        f"{totals.passed} passed, {totals.failed} failed, "
        f"{totals.skipped} skipped, {totals.errored} errored, "
        f"{totals.interrupted} interrupted, {totals.timeout} timeout"
    )
    lines.append("")

    lines.append("| ID | Title | Status | Duration | Notes |")
    lines.append("|---|---|---|---|---|")
    for outcome in summary.evals:
        lines.append(
            f"| {outcome.eval_id} | {outcome.title} | {outcome.status} | "
            f"{_format_duration(outcome.duration_sec)} | {_row_note(outcome)} |"
        )

    failures = [o for o in summary.evals if o.status in _FAILURE_STATUSES]
    if failures:
        lines.append("")
        lines.append(f"## Failures ({len(failures)})")
        for outcome in failures:
            lines.append("")
            lines.append(f"### {outcome.eval_id}: {outcome.title}")
            lines.append(f"**Status:** {outcome.status}")
            if outcome.error_class:
                lines.append(f"**Error class:** {outcome.error_class}")
            if outcome.expects:
                for expect in outcome.expects:
                    bullet = "✅" if expect.passed else "❌"
                    msg = expect.message or ""
                    lines.append(f"- {bullet} `{expect.name}` — {msg}".rstrip())
            if outcome.artifacts:
                lines.append("**Artifacts:**")
                for name in sorted(outcome.artifacts):
                    lines.append(f"- `{name}` → `{outcome.artifacts[name]}`")

    lines.append("")
    lines.append("## Counts")
    lines.append(f"- manifest_n: {counts.manifest_n}")
    lines.append(f"- expanded_n_prime: {counts.expanded_n_prime}")
    lines.append(f"- kept_k: {counts.kept_k}")
    lines.append(f"- skipped_s: {counts.skipped_s}")
    lines.append(
        "- kept_plus_skipped_equals_n_prime: "
        f"{str(counts.kept_plus_skipped_equals_n_prime).lower()}"
    )

    if summary.finished_at:
        lines.append("")
        lines.append(f"_Finished at {summary.finished_at}._")

    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# JSON renderer
# ---------------------------------------------------------------------------


def render_summary_json(summary: RunSummary) -> str:
    """Return the ``summary.json`` payload as a string.

    Wraps :meth:`RunSummary.to_dict` (the canonical DM-004 producer) so
    every consumer that needs JSON bytes goes through the same single
    serialisation path. ``sort_keys=False`` preserves the DM-004 /
    DM-012 declaration order; the trailing newline is added explicitly
    so the file content terminates with ``\\n`` (POSIX text-file
    convention).
    """

    _check_invariant(summary)
    payload = summary.to_dict()
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


# ---------------------------------------------------------------------------
# JUnit XML renderer
# ---------------------------------------------------------------------------


_JUNIT_FAILURE_STATUSES: frozenset[str] = frozenset(
    {"FAIL", "ERRORED", "TIMEOUT", "INTERRUPTED", "XPASS"}
)


def render_junit_xml(summary: RunSummary) -> str:
    """Return the ``junit.xml`` payload as a string.

    Maps each :class:`EvalOutcome` to a ``<testcase>`` element. Status
    is encoded via the standard JUnit child tags:

    * ``FAIL`` / ``XPASS``               → ``<failure>``
    * ``ERRORED`` / ``TIMEOUT`` /
      ``INTERRUPTED``                    → ``<error>``
    * ``SKIPPED``                        → ``<skipped>``
    * ``PASS`` / ``XFAIL``               → no child element

    Output is byte-stable: element attributes are inserted in a fixed
    order (matching JUnit conventions) and child elements follow the
    tuple ordering of ``summary.evals``.
    """

    _check_invariant(summary)

    totals = summary.totals
    suite = ET.Element(
        "testsuite",
        attrib={
            "name": summary.suite,
            "tests": str(summary.counts.expanded_n_prime),
            "failures": str(totals.failed + totals.timeout),
            "errors": str(totals.errored + totals.interrupted),
            "skipped": str(totals.skipped),
            "time": f"{summary.duration_sec:.3f}",
            "timestamp": summary.started_at,
        },
    )

    for outcome in summary.evals:
        case = ET.SubElement(
            suite,
            "testcase",
            attrib={
                "classname": summary.suite,
                "name": outcome.eval_id,
                "time": f"{outcome.duration_sec:.3f}",
            },
        )
        if outcome.status == "SKIPPED":
            ET.SubElement(
                case,
                "skipped",
                attrib={
                    "message": outcome.skip_reason or "skipped",
                    "type": outcome.skip_flag_triggered or "",
                },
            )
        elif outcome.status in {"FAIL", "XPASS"}:
            ET.SubElement(
                case,
                "failure",
                attrib={
                    "message": outcome.title,
                    "type": outcome.status,
                },
            )
        elif outcome.status in {"ERRORED", "TIMEOUT", "INTERRUPTED"}:
            ET.SubElement(
                case,
                "error",
                attrib={
                    "message": outcome.error_class or outcome.title,
                    "type": outcome.status,
                },
            )

    body = ET.tostring(suite, encoding="unicode")
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + body + "\n"


# ---------------------------------------------------------------------------
# Writer entry-point
# ---------------------------------------------------------------------------


def render_summary_yaml(summary: RunSummary) -> str:
    """Return the YAML rendering of ``summary.to_dict()``.

    M4: promoted from ``reporter.py`` so the YAML renderer sits alongside
    its Markdown / JSON / JUnit siblings and the consolidated
    :func:`_write_artifact_set` helper can emit ``summary.yaml`` from a
    single SoT without a circular import. ``Reporter.to_yaml`` re-exports
    from here for backward-compatibility.

    Uses ``yaml.safe_dump`` with ``sort_keys=False`` so the output
    preserves the DM-004 field declaration order :meth:`RunSummary.to_dict`
    yields. ``default_flow_style=False`` keeps the result in canonical
    block style (one key per line). The N'-vs-K invariant guard fires
    before serialisation so a mismatched summary cannot leave a partial
    YAML behind.
    """

    _check_invariant(summary)
    payload = summary.to_dict()
    return yaml.safe_dump(
        payload,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
    )


def _write_artifact_set(
    out: Path,
    *,
    summary: RunSummary,
    emit_junit: bool,
    md_renderer: Callable[[RunSummary], str] = render_summary_markdown,
    json_renderer: Callable[[RunSummary], str] = render_summary_json,
    yaml_renderer: Callable[[RunSummary], str] = render_summary_yaml,
    junit_renderer: Callable[[RunSummary], str] = render_junit_xml,
) -> dict[str, Path]:
    """M4: consolidated artifact-set writer used by both ``Reporter.write``
    and :func:`write_aggregated_report`.

    Always writes ``summary.md``, ``summary.json``, ``summary.yaml``.
    Writes ``junit.xml`` only when ``emit_junit`` is True. Returns the
    artefact-name → written-path mapping. The N'-vs-K invariant must
    have already been checked by the caller — this helper is the
    file-emit layer only.

    Renderer callables are injected so :class:`Reporter` can plug in its
    instance methods (which add formatting flourishes on top of the
    module-level renderers) without going through a second class shape.
    """
    out.mkdir(parents=True, exist_ok=True)

    md_path = out / "summary.md"
    json_path = out / "summary.json"
    yaml_path = out / "summary.yaml"

    md_path.write_text(md_renderer(summary), encoding="utf-8")
    json_path.write_text(json_renderer(summary), encoding="utf-8")
    yaml_path.write_text(yaml_renderer(summary), encoding="utf-8")

    written: dict[str, Path] = {
        "summary.md": md_path,
        "summary.json": json_path,
        "summary.yaml": yaml_path,
    }

    if emit_junit:
        junit_path = out / "junit.xml"
        junit_path.write_text(junit_renderer(summary), encoding="utf-8")
        written["junit.xml"] = junit_path

    return written


def write_aggregated_report(
    summary: RunSummary,
    output_dir: Path | str,
    *,
    emit_junit: bool = False,
) -> Mapping[str, Path]:
    """Write the FR-RPT1 aggregated run report under ``output_dir``.

    Emits:

    * ``<output_dir>/summary.md``
    * ``<output_dir>/summary.json``
    * ``<output_dir>/summary.yaml`` (M4: now unconditional, closing the
      +1 yaml divergence with :meth:`Reporter.write`)
    * ``<output_dir>/junit.xml`` (only when ``emit_junit=True``)

    The N'-vs-K invariant is checked *before* any file is written; a
    mismatch raises :class:`ReporterContractViolation` (callers map to
    exit 2). The output directory is created when missing.

    Returns a mapping of artefact-name → written path for the artifacts
    actually emitted. ``junit.xml`` is only present in the mapping when
    ``emit_junit=True``.
    """

    _check_invariant(summary)
    return _write_artifact_set(Path(output_dir), summary=summary, emit_junit=emit_junit)
