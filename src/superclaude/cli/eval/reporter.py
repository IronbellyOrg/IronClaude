"""COMP-008 Reporter / AggregatedRunReport class (D-0055 / T03.13).

The :class:`Reporter` (aliased as :class:`AggregatedRunReport`) is the
class-shaped surface that COMP-008 of the design-spec carries. It wraps
a :class:`~superclaude.cli.eval.models.RunSummary` (T03.09 / DM-004) and
exposes the four canonical emitter methods declared by the roadmap row::

    Reporter(summary).to_markdown()  # human-readable summary.md body
    Reporter(summary).to_yaml()      # YAML rendering of the DM-004 dict
    Reporter(summary).to_json()      # canonical summary.json payload
    Reporter(summary).to_junit()     # JUnit XML payload (feature-gated)

Each emitter delegates to the file-emitting layer in
:mod:`~superclaude.cli.eval.run_report` (the module-level renderers
landed in T03.11 / FR-RPT1 / D-0054). That layer already enforces the
FR-RPT1 N'-vs-K dimensional invariant (``len(summary.evals) ==
summary.counts.expanded_n_prime``) before doing any work, so the
assertion guard fires inside *every* emitter — calling ``to_markdown()``
on a mismatched summary raises :class:`ReporterContractViolation` just
the same as calling ``to_junit()`` does, and no caller can sneak a
partial render past the guard.

The class itself does not perform the contract check directly; it
relies on the underlying renderers so that a single
``_check_invariant`` implementation is the source of truth. The
acceptance criteria require the guard to fire "before any emitter
writes output" — which is exactly what the module-level renderers do.

Pattern reference: ``src/superclaude/cli/sprint/executor.py:190-335``
(``AggregatedPhaseReport``). The cliEval reporter mirrors that
class's shape (frozen dataclass-like wrapper, ``to_yaml``/``to_markdown``
methods) but operates on a :class:`RunSummary` instead of a list of
``TaskResult`` rows. The probe test in T03.14 pins the upstream shape
read-only so refactors there fail loudly.

Feature gating of JUnit XML
---------------------------

The roadmap row requires ``to_junit`` to be feature-gated and only
emitted when explicitly requested. Two layers achieve that:

* The :meth:`Reporter.to_junit` method is opt-in: callers must invoke
  it explicitly (it is not part of :meth:`Reporter.write`'s default
  output set).
* :meth:`Reporter.write` accepts ``emit_junit=False`` by default and
  only writes ``junit.xml`` when the caller flips it to ``True`` — the
  same convention :func:`write_aggregated_report` follows so the two
  surfaces stay aligned.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from .models import RunSummary
from .run_report import (
    REPORTER_CONTRACT_VIOLATION_EXIT_CODE,
    ReporterContractViolation,
    _check_invariant,
    _write_artifact_set,
    render_junit_xml,
    render_summary_json,
    render_summary_markdown,
    render_summary_yaml,
)

__all__ = [
    "AggregatedRunReport",
    "REPORTER_CONTRACT_VIOLATION_EXIT_CODE",
    "Reporter",
    "ReporterContractViolation",
    "render_summary_yaml",
]


# ---------------------------------------------------------------------------
# YAML renderer
# ---------------------------------------------------------------------------
# M4: ``render_summary_yaml`` was promoted to ``run_report.py`` so it sits
# alongside its Markdown / JSON / JUnit siblings and the consolidated
# ``_write_artifact_set`` helper. It is re-exported above from ``reporter``
# for backward-compatibility (any external caller importing
# ``from .reporter import render_summary_yaml`` keeps working).


# ---------------------------------------------------------------------------
# Reporter / AggregatedRunReport
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Reporter:
    """Class-shaped Reporter surface (COMP-008 / D-0055).

    Wraps a :class:`RunSummary` and exposes the four canonical emitter
    methods. The class is a frozen dataclass so once a caller hands the
    Reporter a summary, the rendered output is reproducible across the
    Reporter's lifetime — a property the byte-stability tests rely on.

    Construction is intentionally minimal::

        Reporter(summary)                        # write() skips junit.xml
        Reporter(summary, emit_junit=True)       # write() includes junit.xml

    The four ``to_*`` methods are always callable regardless of
    ``emit_junit``; the flag only governs :meth:`write`'s default output
    set. Direct ``to_junit()`` callers signal explicit intent and the
    XML is emitted.

    Attributes
    ----------
    summary:
        The :class:`RunSummary` to render. Stored by reference;
        ``RunSummary`` is itself frozen so a Reporter consumer cannot
        mutate the source mid-render.
    emit_junit:
        Whether :meth:`write` should emit ``junit.xml`` alongside the
        markdown / JSON / YAML artefacts. Defaults to ``False``.
    """

    summary: RunSummary
    emit_junit: bool = False

    # -- single-format emitters ---------------------------------------------

    def to_markdown(self) -> str:
        """Return the ``summary.md`` body for :attr:`summary`.

        Delegates to :func:`render_summary_markdown` so the contract
        guard fires before any rendering work happens.
        """

        return render_summary_markdown(self.summary)

    def to_yaml(self) -> str:
        """Return the YAML rendering of :attr:`summary`.

        Delegates to :func:`render_summary_yaml` so the contract guard
        fires before any rendering work happens.
        """

        return render_summary_yaml(self.summary)

    def to_json(self) -> str:
        """Return the ``summary.json`` payload for :attr:`summary`.

        Delegates to :func:`render_summary_json` so the contract guard
        fires before any rendering work happens.
        """

        return render_summary_json(self.summary)

    def to_junit(self) -> str:
        """Return the JUnit XML payload for :attr:`summary`.

        Always callable: invoking this method is itself the "explicit
        request" the feature-gate language refers to. Callers that only
        want the markdown/JSON/YAML triplet should use :meth:`write`
        without ``emit_junit=True`` instead.
        """

        return render_junit_xml(self.summary)

    # -- multi-artefact writer ---------------------------------------------

    def write(self, output_dir: Path | str) -> Mapping[str, Path]:
        """Write the report artefacts under ``output_dir``.

        Always writes ``summary.md``, ``summary.json``, and ``summary.yaml``.
        Writes ``junit.xml`` only when :attr:`emit_junit` is ``True``
        (the feature gate). The N'-vs-K invariant guard fires *before*
        the output directory is created so a mismatched summary cannot
        leave a partial artefact set on disk.

        Returns a mapping of artefact-name → written path. ``junit.xml``
        is only present in the mapping when :attr:`emit_junit` is True.

        M4: delegates to :func:`run_report._write_artifact_set` so the
        Reporter and the module-level :func:`write_aggregated_report` emit
        the same artefact set from a single SoT. Renderer callables are
        threaded through so each instance method's formatting flourishes
        flow through the shared helper.
        """

        _check_invariant(self.summary)
        return _write_artifact_set(
            Path(output_dir),
            summary=self.summary,
            emit_junit=self.emit_junit,
            md_renderer=lambda _s: self.to_markdown(),
            json_renderer=lambda _s: self.to_json(),
            yaml_renderer=lambda _s: self.to_yaml(),
            junit_renderer=lambda _s: self.to_junit(),
        )


# Aliased name the roadmap row (COMP-008) and design-spec §9 use
# interchangeably with ``Reporter``. Both spellings resolve to the same
# class so callers can pick whichever reads better at their call site.
AggregatedRunReport = Reporter
