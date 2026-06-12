"""Catch-rate report writer -- pure renderer (invariant-guarded) + single to_dict SoT + emitter.

Mirrors the ``src/superclaude/cli/eval/run_report.py`` triad (run_report.py:67-108, 233-246,
366-439): a ``ReporterContractViolation`` analogue, a ``_check`` invariant guard called BEFORE any
serialization, a pure ``render_*`` that goes through ``to_dict()`` as the single serialization SoT,
and a filesystem writer that guards-then-writes so a partial/contradictory artifact is never left on
disk. The renderers also record, in plain sight, that NEW=CATCH is a documentation-presence PROXY so
the report is not oversold.

Proxy honesty (wire text MUST match code): the catch-rate model is a bookkeeping contract of
PRODUCER-ASSERTED claims, not a record of executed-gate observations. All three ``is_fully_caught``
conjuncts (CATCH / negative_witness / card_path) are producer-asserted. ``card_path`` NON-NULLNESS is
the data invariant the model enforces; card EXISTENCE (the impl ref having landed) is enforced
UPSTREAM by the Phase 4 ``requires_impl_ref`` skip-guard and the aggregation (which only sets
``card_path`` from a verified-existing ref). A real on-disk existence gate lives in
``catch_rate.unresolved_card_paths`` (pure, model-external).
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path

from tests.troubleshoot.backtest.catch_rate import (
    STATUS_PARTIAL,
    CatchRateReport,
)

# The CLI dispatcher maps a contract violation to exit code 2 (mirrors run_report.py:56).
# Pinned to ``superclaude.cli.eval.exit_codes.USAGE_ERROR`` (= 2). NOT imported here on purpose: this
# test-tree module stays self-contained (no dependency on the eval package); the comment is the pin.
CATCH_RATE_CONTRACT_VIOLATION_EXIT_CODE: int = 2

_PROXY_NOTE = (
    "NEW=CATCH is a documentation-presence PROXY: card_path records a PRODUCER-ASSERTED impl-ref, and "
    "the model enforces card_path NON-NULLNESS only (it is NOT an executed gate and does not stat the "
    "path). All three is_fully_caught conjuncts (CATCH / negative_witness / card_path) are "
    "producer-asserted. Card EXISTENCE (the impl ref having landed) is enforced UPSTREAM by the "
    "Phase 4 requires_impl_ref skip-guard and the aggregation (which sets card_path only from a "
    "verified-existing ref); catch_rate.unresolved_card_paths is the real on-disk existence gate."
)


class CatchRateContractViolation(RuntimeError):
    """Raised when a report's count accounting is internally inconsistent.

    Analogous to ``ReporterContractViolation`` (run_report.py:67-93): raised BEFORE any write so the
    writer never leaves a partial artifact on disk that contradicts its own accounting. The CLI
    dispatcher maps this to :data:`CATCH_RATE_CONTRACT_VIOLATION_EXIT_CODE` (= 2).

    Reachability: this guard protects inputs that BYPASS the frozen model -- duck-typed or mutated
    reports whose accounting was never validated (the fidelity test exercises exactly this via a
    ``types.SimpleNamespace`` passed straight into the renderer). For any normally-constructible
    :class:`~tests.troubleshoot.backtest.catch_rate.CatchRateReport`, this path is intentionally
    REDUNDANT: the model's ``__post_init__`` already enforces the same count checks at construction,
    so a constructible report can never reach the writer in a violating state. The guard is kept as a
    boundary check for the bypass case, not as a claim that constructible reports can trip it.
    """

    def __init__(self, *, message: str, run_id: str | None = None) -> None:
        self.run_id = run_id
        run_clause = f" (run_id={run_id!r})" if run_id else ""
        super().__init__(f"Catch-rate contract violation: {message}{run_clause}.")


def _check(report: CatchRateReport) -> None:
    """Re-validate count accounting before any serialization, for inputs that BYPASS the frozen model.

    Guards duck-typed / mutated reports whose ``__post_init__`` never ran (the fidelity test passes a
    ``types.SimpleNamespace`` directly into the renderer). For a constructible ``CatchRateReport`` this
    is intentionally redundant -- the model's ``__post_init__`` already enforces these same count
    checks at construction. Kept as the writer-boundary check for the bypass case.
    """
    if report.caught + report.missed != report.total_escapes:
        raise CatchRateContractViolation(
            message=(
                f"caught({report.caught}) + missed({report.missed}) != "
                f"total_escapes({report.total_escapes})"
            ),
            run_id=report.run_id,
        )
    if report.escapes and len(report.escapes) != report.total_escapes:
        raise CatchRateContractViolation(
            message=(
                f"len(escapes)({len(report.escapes)}) != total_escapes({report.total_escapes})"
            ),
            run_id=report.run_id,
        )


def render_catch_rate_json(report: CatchRateReport) -> str:
    """Return the ``catch-rate.json`` payload as a string (invariant-checked, ``to_dict`` SoT)."""
    _check(report)
    return (
        json.dumps(report.to_dict(), indent=2, ensure_ascii=False, sort_keys=False)
        + "\n"
    )


def render_catch_rate_markdown(report: CatchRateReport) -> str:
    """Return a human-readable ``catch-rate.md`` with a per-escape table + proxy-limitation note."""
    _check(report)
    lines: list[str] = []
    # Headline carries the proxy qualifier INLINE so a skimmer cannot read the bare number as
    # executed-gate coverage; the limitation note sits directly under it (not only at the tail).
    lines.append(
        f"## Catch rate (documentation-presence proxy): "
        f"{report.caught}/{report.total_escapes} ({report.backtest_status})"
    )
    lines.append("")
    lines.append(f"> Proxy limitation: {report.proxy_limitation or _PROXY_NOTE}")
    lines.append("")
    lines.append("| Escape | Wave | Verdict | Witness | Card |")
    lines.append("|--------|------|---------|---------|------|")
    for e in report.escapes:
        witness = "yes" if e.negative_witness else "no"
        card = e.card_path if e.card_path is not None else "—"
        lines.append(f"| {e.escape_id} | {e.wave} | {e.verdict} | {witness} | {card} |")
    lines.append("")
    if report.backtest_status == STATUS_PARTIAL:
        missing = ", ".join(report.missing_escape_ids()) or "(none)"
        lines.append(
            f"**Partial** — escape ids missing CATCH / negative_witness / card_path: {missing}."
        )
        lines.append("")
    # NEW=CATCH proxy honesty: record the limitation so the report is not oversold.
    lines.append(f"> Proxy limitation: {report.proxy_limitation or _PROXY_NOTE}")
    lines.append("")
    return "\n".join(lines)


def write_catch_rate_report(
    report: CatchRateReport,
    output_dir: Path | str,
    *,
    emit_md: bool = True,
) -> Mapping[str, Path]:
    """Guard-then-write ``catch-rate.json`` (+ optional ``catch-rate.md``) under ``output_dir``.

    The invariant is checked at the TOP (before the directory is created), mirroring
    ``write_aggregated_report`` (run_report.py:438), so a broken invariant never even creates the
    output dir. Both payloads are then rendered to local strings BEFORE either file is written, so a
    render failure leaves NO file on disk (atomicity). ``output_dir`` MUST be a tmp/test dir -- NEVER
    under ``docs/`` (the root ``_pollution_snapshot`` autouse guard fails the session on ``docs/``
    writes). Returns the artifact-name -> written-path mapping.
    """
    # Guard BEFORE any filesystem effect (no dir created on a broken invariant); run_report.py:438.
    _check(report)

    # Render every payload to a local string BEFORE writing either file: a render failure must leave
    # nothing on disk (atomicity).
    json_payload = render_catch_rate_json(report)
    md_payload = render_catch_rate_markdown(report) if emit_md else None

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    written: dict[str, Path] = {}

    json_path = out / "catch-rate.json"
    json_path.write_text(json_payload, encoding="utf-8")
    written["catch-rate.json"] = json_path

    if md_payload is not None:
        md_path = out / "catch-rate.md"
        md_path.write_text(md_payload, encoding="utf-8")
        written["catch-rate.md"] = md_path

    return written
