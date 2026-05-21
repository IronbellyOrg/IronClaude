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

import yaml

from .models import RunSummary
from .run_report import (
    REPORTER_CONTRACT_VIOLATION_EXIT_CODE,
    ReporterContractViolation,
    _check_invariant,
    render_junit_xml,
    render_summary_json,
    render_summary_markdown,
)

__all__ = [
    "AggregatedRunReport",
    "REPORTER_CONTRACT_VIOLATION_EXIT_CODE",
    "Reporter",
    "ReporterContractViolation",
    "render_summary_yaml",
]


# ---------------------------------------------------------------------------
# YAML renderer (the only emitter not already provided by run_report.py)
# ---------------------------------------------------------------------------


def render_summary_yaml(summary: RunSummary) -> str:
    """Return the YAML rendering of ``summary.to_dict()``.

    Uses ``yaml.safe_dump`` with ``sort_keys=False`` so the output
    preserves the DM-004 field declaration order :meth:`RunSummary.to_dict`
    yields. ``default_flow_style=False`` keeps the result in canonical
    block style (one key per line) which is what a human reviewer
    expects when diffing summary YAMLs side-by-side.

    The N'-vs-K invariant guard is checked *before* any serialisation so
    a mismatched summary cannot leave a partial YAML behind.

    Byte-stable for a given input: ``RunSummary`` is a frozen dataclass,
    ``to_dict()`` returns a deterministic mapping, and PyYAML emits a
    stable block-style serialisation for the same Python value.
    """

    _check_invariant(summary)
    payload = summary.to_dict()
    return yaml.safe_dump(
        payload,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
    )


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
        """

        _check_invariant(self.summary)

        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)

        md_path = out / "summary.md"
        json_path = out / "summary.json"
        yaml_path = out / "summary.yaml"

        md_path.write_text(self.to_markdown(), encoding="utf-8")
        json_path.write_text(self.to_json(), encoding="utf-8")
        yaml_path.write_text(self.to_yaml(), encoding="utf-8")

        written: dict[str, Path] = {
            "summary.md": md_path,
            "summary.json": json_path,
            "summary.yaml": yaml_path,
        }

        if self.emit_junit:
            junit_path = out / "junit.xml"
            junit_path.write_text(self.to_junit(), encoding="utf-8")
            written["junit.xml"] = junit_path

        return written


# Aliased name the roadmap row (COMP-008) and design-spec §9 use
# interchangeably with ``Reporter``. Both spellings resolve to the same
# class so callers can pick whichever reads better at their call site.
AggregatedRunReport = Reporter
