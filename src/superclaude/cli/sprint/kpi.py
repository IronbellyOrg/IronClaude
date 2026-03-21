"""KPI report for gate and remediation metrics.

Generated after sprint completion to provide observability into:
- Trailing gate latency (p50, p95)
- Remediation frequency
- Conflict review rate
- Gate pass/fail distribution
"""

from __future__ import annotations

from dataclasses import dataclass, field

from typing import TYPE_CHECKING

from ..pipeline.trailing_gate import DeferredRemediationLog, TrailingGateResult

if TYPE_CHECKING:
    from ..audit.wiring_gate import WiringReport
    from .models import TurnLedger


@dataclass
class GateKPIReport:
    """Aggregated KPI metrics for trailing gate performance.

    Built from gate results, remediation log, and conflict review data
    after sprint completion.
    """

    # Gate evaluation metrics
    total_gates_evaluated: int = 0
    gates_passed: int = 0
    gates_failed: int = 0
    gate_latency_ms: list[float] = field(default_factory=list)

    # Remediation metrics
    total_remediations: int = 0
    remediations_resolved: int = 0
    remediations_pending: int = 0

    # Conflict review metrics
    total_conflict_reviews: int = 0
    conflicts_detected: int = 0

    # Wiring gate KPI metrics (FR: T07c)
    wiring_findings_total: int = 0
    wiring_findings_by_type: dict[str, int] = field(default_factory=dict)
    wiring_turns_used: int = 0
    wiring_turns_credited: int = 0
    whitelist_entries_applied: int = 0
    files_skipped: int = 0

    @property
    def gate_pass_rate(self) -> float:
        """Fraction of gates that passed (0.0–1.0)."""
        if self.total_gates_evaluated == 0:
            return 0.0
        return self.gates_passed / self.total_gates_evaluated

    @property
    def gate_fail_rate(self) -> float:
        """Fraction of gates that failed (0.0–1.0)."""
        if self.total_gates_evaluated == 0:
            return 0.0
        return self.gates_failed / self.total_gates_evaluated

    @property
    def remediation_frequency(self) -> float:
        """Fraction of gates requiring remediation (0.0–1.0)."""
        if self.total_gates_evaluated == 0:
            return 0.0
        return self.total_remediations / self.total_gates_evaluated

    @property
    def conflict_review_rate(self) -> float:
        """Fraction of conflict reviews that found conflicts (0.0–1.0)."""
        if self.total_conflict_reviews == 0:
            return 0.0
        return self.conflicts_detected / self.total_conflict_reviews

    @property
    def p50_latency_ms(self) -> float:
        """Median gate evaluation latency in milliseconds."""
        if not self.gate_latency_ms:
            return 0.0
        s = sorted(self.gate_latency_ms)
        mid = len(s) // 2
        if len(s) % 2 == 0:
            return (s[mid - 1] + s[mid]) / 2
        return s[mid]

    @property
    def p95_latency_ms(self) -> float:
        """95th percentile gate evaluation latency in milliseconds."""
        if not self.gate_latency_ms:
            return 0.0
        s = sorted(self.gate_latency_ms)
        idx = int(len(s) * 0.95)
        return s[min(idx, len(s) - 1)]

    def format_report(self) -> str:
        """Format KPI report as human-readable text."""
        lines = [
            "## Gate & Remediation KPI Report",
            "",
            "### Gate Evaluation",
            f"  Total evaluated:  {self.total_gates_evaluated}",
            f"  Passed:           {self.gates_passed}",
            f"  Failed:           {self.gates_failed}",
            f"  Pass rate:        {self.gate_pass_rate:.1%}",
            f"  Latency (p50):    {self.p50_latency_ms:.1f}ms",
            f"  Latency (p95):    {self.p95_latency_ms:.1f}ms",
            "",
            "### Remediation",
            f"  Total:            {self.total_remediations}",
            f"  Resolved:         {self.remediations_resolved}",
            f"  Pending:          {self.remediations_pending}",
            f"  Frequency:        {self.remediation_frequency:.1%}",
            "",
            "### Conflict Review",
            f"  Reviews:          {self.total_conflict_reviews}",
            f"  Conflicts found:  {self.conflicts_detected}",
            f"  Conflict rate:    {self.conflict_review_rate:.1%}",
            "",
            "### Wiring Gate",
            f"  Findings total:   {self.wiring_findings_total}",
            f"  Findings by type: {self.wiring_findings_by_type}",
            f"  Turns used:       {self.wiring_turns_used}",
            f"  Turns credited:   {self.wiring_turns_credited}",
            f"  Whitelist applied:{self.whitelist_entries_applied}",
            f"  Files skipped:    {self.files_skipped}",
        ]
        return "\n".join(lines)


def build_kpi_report(
    gate_results: list[TrailingGateResult],
    remediation_log: DeferredRemediationLog | None = None,
    conflict_reviews_total: int = 0,
    conflicts_detected: int = 0,
    turn_ledger: TurnLedger | None = None,
    wiring_report: WiringReport | None = None,
) -> GateKPIReport:
    """Build a KPI report from gate results and remediation data.

    Called after sprint completion. Aggregates metrics from:
    - TrailingGateResult objects (latency, pass/fail)
    - DeferredRemediationLog (remediation counts)
    - Conflict review counts
    - TurnLedger (wiring turn budget data)
    - WiringReport (wiring finding data)
    """
    report = GateKPIReport()

    # Gate metrics
    for result in gate_results:
        report.total_gates_evaluated += 1
        if result.passed:
            report.gates_passed += 1
        else:
            report.gates_failed += 1
        report.gate_latency_ms.append(result.evaluation_ms)

    # Remediation metrics
    if remediation_log is not None:
        report.total_remediations = remediation_log.entry_count
        report.remediations_pending = len(remediation_log.pending_remediations())
        report.remediations_resolved = (
            report.total_remediations - report.remediations_pending
        )

    # Conflict review metrics
    report.total_conflict_reviews = conflict_reviews_total
    report.conflicts_detected = conflicts_detected

    # Wiring gate metrics (FR: T07c)
    if turn_ledger is not None:
        report.wiring_turns_used = turn_ledger.wiring_turns_used
        # Floor-to-zero: credited turns never go negative (R7)
        report.wiring_turns_credited = max(0, turn_ledger.wiring_turns_credited)

    if wiring_report is not None:
        report.wiring_findings_total = wiring_report.total_findings
        report.files_skipped = wiring_report.files_skipped
        # Build findings-by-type breakdown
        by_type: dict[str, int] = {}
        for finding in wiring_report.all_findings:
            by_type[finding.finding_type] = by_type.get(finding.finding_type, 0) + 1
        report.wiring_findings_by_type = by_type
        # Count suppressed findings as whitelist entries applied
        report.whitelist_entries_applied = sum(
            1 for f in wiring_report.all_findings if f.suppressed
        )

    return report
