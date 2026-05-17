"""Remediation functions -- pure functions for Phase 3 remediation pipeline.

All functions in this module are pure (no I/O, no subprocess calls, no side
effects) per NFR-004, except where explicitly noted.

Provides:
- format_validation_summary(findings) -> str  (T03.01)
- RemediationScope enum  (T03.01/T03.02)
- filter_findings(findings, scope) -> tuple  (T03.02)
- generate_remediation_tasklist(findings, source_report_path, source_report_content) -> str  (T03.04)

Status vocabulary note
----------------------
This module is consumed by two callers with different status vocabularies:

- The registry path (``_run_remediate_step`` -> ``deviations_to_findings``)
  produces findings with ``status in {"ACTIVE", "FIXED"}`` -- never
  ``"PENDING"``.  ``generate_remediation_tasklist`` therefore treats
  ``status == "ACTIVE"`` as the actionable condition.  Records whose status
  is missing from the upstream JSON default to ``"ACTIVE"`` in
  ``deviations_to_findings`` so they survive the actionable filter.
- The parser path (``remediate_parser.py``) constructs findings with
  ``status == "PENDING"`` directly.  Callers feeding that vocabulary into
  this module must translate to ``"ACTIVE"`` before calling
  ``generate_remediation_tasklist``.

``deviation_class`` is currently always ``UNCLASSIFIED``; the
``SLIP``/``INTENTIONAL``/``PRE_APPROVED``/``AMBIGUOUS`` branches in this
module remain wired for forward compatibility but are dead until a real
classifier ships (see backlog item ``pipeline-classifier-implementation``).

See ``.dev/releases/backlog/finding-status-vocabulary-audit.md`` (filed
separately) for the broader follow-up audit.
"""

from __future__ import annotations

import enum
import hashlib
from datetime import datetime, timezone

from .models import Finding


class RemediationScope(enum.Enum):
    """User-selected scope for remediation filtering.

    Maps to prompt options:
    [1] BLOCKING_ONLY  -- only BLOCKING findings
    [2] BLOCKING_WARNING -- BLOCKING + WARNING
    [3] ALL -- all findings with fix_guidance
    """

    BLOCKING_ONLY = "blocking_only"
    BLOCKING_WARNING = "blocking_warning"
    ALL = "all"


# Agreement categories that trigger auto-SKIP regardless of scope selection
_AUTO_SKIP_CATEGORIES = frozenset({"NO_ACTION_REQUIRED", "OUT_OF_SCOPE"})


def format_validation_summary(findings: list[Finding]) -> str:
    """Format findings into a severity-grouped terminal summary.

    Groups findings by severity (BLOCKING, WARNING, INFO) with counts
    and lists each finding's ID and description. Returns a formatted
    string suitable for terminal output per spec section 2.2 box layout.

    Pure function: no I/O or side effects.
    """
    blocking = [f for f in findings if f.severity == "BLOCKING"]
    warning = [f for f in findings if f.severity == "WARNING"]
    info = [f for f in findings if f.severity == "INFO"]

    lines: list[str] = []
    lines.append("=" * 60)
    lines.append("  VALIDATION SUMMARY")
    lines.append("=" * 60)
    lines.append("")

    total = len(findings)
    lines.append(f"  Total findings: {total}")
    lines.append(
        f"  BLOCKING: {len(blocking)}  |  WARNING: {len(warning)}  |  INFO: {len(info)}"
    )
    lines.append("")

    if blocking:
        lines.append("  --- BLOCKING ---")
        for f in blocking:
            lines.append(f"  {f.id} | {f.description}")
        lines.append("")

    if warning:
        lines.append("  --- WARNING ---")
        for f in warning:
            lines.append(f"  {f.id} | {f.description}")
        lines.append("")

    if info:
        lines.append("  --- INFO ---")
        for f in info:
            lines.append(f"  {f.id} | {f.description}")
        lines.append("")

    lines.append("=" * 60)
    return "\n".join(lines)


def should_skip_prompt(findings: list[Finding]) -> bool:
    """Return True when prompt should be skipped (zero BLOCKING + zero WARNING).

    Per spec section 2.2: when there are no BLOCKING and no WARNING findings,
    the prompt is auto-skipped.

    Pure function: no I/O or side effects.
    """
    blocking = sum(1 for f in findings if f.severity == "BLOCKING")
    warning = sum(1 for f in findings if f.severity == "WARNING")
    return blocking == 0 and warning == 0


def filter_findings(
    findings: list[Finding],
    scope: RemediationScope,
) -> tuple[list[Finding], list[Finding]]:
    """Filter findings by user-selected scope with auto-SKIP logic.

    Auto-SKIP is applied first: findings with agreement_category of
    NO_ACTION_REQUIRED or OUT_OF_SCOPE are always moved to skipped,
    regardless of scope selection.

    Then scope filtering is applied:
    - BLOCKING_ONLY: keeps only BLOCKING severity
    - BLOCKING_WARNING: keeps BLOCKING + WARNING
    - ALL: keeps all findings that have fix_guidance

    Returns (actionable, skipped) tuple.

    Pure function: no I/O or side effects.
    """
    actionable: list[Finding] = []
    skipped: list[Finding] = []

    for f in findings:
        # Auto-SKIP: NO_ACTION_REQUIRED and OUT_OF_SCOPE always skipped
        if f.agreement_category in _AUTO_SKIP_CATEGORIES:
            skipped.append(f)
            continue

        # Already terminal status (FIXED, SKIPPED) -> skip
        if f.status in ("FIXED", "SKIPPED"):
            skipped.append(f)
            continue

        # Scope filtering
        if scope == RemediationScope.BLOCKING_ONLY:
            if f.severity == "BLOCKING":
                actionable.append(f)
            else:
                skipped.append(f)
        elif scope == RemediationScope.BLOCKING_WARNING:
            if f.severity in ("BLOCKING", "WARNING"):
                actionable.append(f)
            else:
                skipped.append(f)
        else:  # ALL
            if f.fix_guidance:
                actionable.append(f)
            else:
                skipped.append(f)

    return actionable, skipped


def generate_remediation_tasklist(
    findings: list[Finding],
    source_report_path: str,
    source_report_content: str,
) -> str:
    """Generate remediation-tasklist.md with YAML frontmatter.

    Produces markdown with:
    - YAML frontmatter: type, source_report, source_report_hash, generated,
      total_findings, actionable, skipped
    - Severity-grouped entries (BLOCKING/WARNING/INFO) for **actionable**
      findings only (``status == "ACTIVE"``).
    - A distinct ``## ALREADY FIXED`` section for ``status == "FIXED"``
      records, rendered as ``- [x]`` checkboxes so the actionable counter
      stays internally consistent with the body.
    - A ``## SKIPPED`` section for ``status == "SKIPPED"`` records.

    T2b: When ``len(findings) == 0`` the function defers to
    ``generate_stub_tasklist``; an empty ``actionable`` list with
    non-actionable records present still renders the full body so FIXED
    records are not silently dropped.

    The source_report_hash is SHA-256 of the source report content.

    Pure function: no I/O or side effects (datetime injected via UTC now).
    """
    # T2b: empty registry -> stub format; non-empty with zero actionable
    # still renders so non-actionable records survive.
    if not findings:
        return generate_stub_tasklist(source_report_path, source_report_content)

    source_hash = hashlib.sha256(source_report_content.encode("utf-8")).hexdigest()
    generated = datetime.now(timezone.utc).isoformat()

    # T2: registry-aligned actionable filter. Registry findings carry
    # status ACTIVE; FIXED/SKIPPED are non-actionable and rendered under
    # their own sections.
    actionable_findings = [f for f in findings if f.status == "ACTIVE"]
    skipped_findings = [f for f in findings if f.status != "ACTIVE"]
    total = len(findings)

    # YAML frontmatter
    lines: list[str] = [
        "---",
        "type: remediation-tasklist",
        f"source_report: {source_report_path}",
        f"source_report_hash: {source_hash}",
        f"generated: {generated}",
        f"total_findings: {total}",
        f"actionable: {len(actionable_findings)}",
        f"skipped: {len(skipped_findings)}",
        "---",
        "",
        "# Remediation Tasklist",
        "",
    ]

    # T2c: restrict BLOCKING/WARNING/INFO to actionable findings so the
    # body item count matches the frontmatter ``actionable`` value.
    blocking = [f for f in actionable_findings if f.severity == "BLOCKING"]
    warning = [f for f in actionable_findings if f.severity == "WARNING"]
    info = [f for f in actionable_findings if f.severity == "INFO"]
    fixed = [f for f in findings if f.status == "FIXED"]
    skipped_sev = [f for f in findings if f.status == "SKIPPED"]

    if blocking:
        lines.append("## BLOCKING")
        lines.append("")
        for f in blocking:
            status = f.status
            files = ", ".join(f.files_affected) if f.files_affected else "unknown"
            lines.append(f"- [ ] {f.id} | {files} | {status} -- {f.description}")
        lines.append("")

    if warning:
        lines.append("## WARNING")
        lines.append("")
        for f in warning:
            status = f.status
            files = ", ".join(f.files_affected) if f.files_affected else "unknown"
            lines.append(f"- [ ] {f.id} | {files} | {status} -- {f.description}")
        lines.append("")

    if info:
        lines.append("## INFO")
        lines.append("")
        for f in info:
            status = f.status
            files = ", ".join(f.files_affected) if f.files_affected else "unknown"
            lines.append(f"- [ ] {f.id} | {files} | {status} -- {f.description}")
        lines.append("")

    # T2c: distinct ALREADY FIXED section. Operators still see FIXED
    # records but they do not contribute to ``actionable``.
    if fixed:
        lines.append("## ALREADY FIXED")
        lines.append("")
        for f in fixed:
            files = ", ".join(f.files_affected) if f.files_affected else "unknown"
            lines.append(f"- [x] {f.id} | {files} | FIXED -- {f.description}")
        lines.append("")

    # Skipped section (findings that were already SKIPPED before tasklist generation)
    if skipped_sev:
        lines.append("## SKIPPED")
        lines.append("")
        for f in skipped_sev:
            files = ", ".join(f.files_affected) if f.files_affected else "unknown"
            lines.append(f"- [x] {f.id} | {files} | SKIPPED -- {f.description}")
        lines.append("")

    return "\n".join(lines)


def generate_stub_tasklist(
    source_report_path: str,
    source_report_content: str,
) -> str:
    """Generate a stub remediation-tasklist.md when no actionable findings exist.

    Produces minimal tasklist with actionable: 0 in frontmatter.

    Pure function: no I/O or side effects.
    """
    source_hash = hashlib.sha256(source_report_content.encode("utf-8")).hexdigest()
    generated = datetime.now(timezone.utc).isoformat()

    return "\n".join(
        [
            "---",
            "type: remediation-tasklist",
            f"source_report: {source_report_path}",
            f"source_report_hash: {source_hash}",
            f"generated: {generated}",
            "total_findings: 0",
            "actionable: 0",
            "skipped: 0",
            "---",
            "",
            "# Remediation Tasklist",
            "",
            "No actionable findings. All entries SKIPPED or no findings detected.",
            "",
        ]
    )


def _parse_routing_list(routing_value: str) -> list[str]:
    """Parse a whitespace/comma-separated routing value into a list of IDs.

    Valid IDs match DEV-\\d+. Invalid tokens are silently dropped.
    Empty string or whitespace-only input returns empty list.

    Pure function: no I/O or side effects.
    """
    import logging
    import re

    _log = logging.getLogger("superclaude.roadmap.remediate")

    if not routing_value or not routing_value.strip():
        return []

    result: list[str] = []
    id_pattern = re.compile(r"^DEV-\d+$")
    for token in re.split(r"[\s,]+", routing_value):
        token = token.strip()
        if not token:
            continue
        if id_pattern.match(token):
            result.append(token)
        else:
            _log.warning("Invalid routing ID ignored: %r", token)
    return result


# Severity mapping for deviations_to_findings (v2.26)
_DEVIATION_SEVERITY_MAP: dict[str, str] = {
    "HIGH": "BLOCKING",
    "MEDIUM": "WARNING",
    "LOW": "INFO",
}


def deviations_to_findings(
    deviation_records: list[dict],
    fidelity_table: dict[str, dict] | None = None,
) -> list[Finding]:
    """Convert deviation analysis records to Finding objects.

    Severity mapping (FR-082):
    - HIGH -> BLOCKING
    - MEDIUM -> WARNING
    - LOW -> INFO

    Raises ValueError if routing is empty but slip_count > 0.
    Logs WARNING if a routing ID is not found in fidelity_table.

    Pure function aside from logging.

    Args:
        deviation_records: list of dicts with keys:
            id, severity, dimension, description, location, evidence,
            fix_guidance, files_affected, deviation_class, routing
        fidelity_table: optional dict mapping DEV-ID -> metadata dict

    Returns:
        list of Finding objects
    """
    import logging

    _log = logging.getLogger("superclaude.roadmap.remediate")

    if fidelity_table is None:
        fidelity_table = {}

    slip_records = [r for r in deviation_records if r.get("deviation_class") == "SLIP"]
    routing_ids = _parse_routing_list(
        ",".join(r.get("routing", "") for r in slip_records if r.get("routing"))
    )

    if slip_records and not routing_ids:
        raise ValueError(
            f"Empty routing_fix_roadmap with slip_count={len(slip_records)} > 0. "
            "SLIP deviations require routing IDs."
        )

    findings: list[Finding] = []
    for record in deviation_records:
        dev_id = record.get("id", "UNKNOWN")
        raw_severity = record.get("severity", "LOW")
        severity = _DEVIATION_SEVERITY_MAP.get(raw_severity, "INFO")

        if dev_id not in fidelity_table and fidelity_table:
            _log.warning("Routing ID %r not found in fidelity table", dev_id)

        finding = Finding(
            id=dev_id,
            severity=severity,
            dimension=record.get("dimension", ""),
            description=record.get("description", ""),
            location=record.get("location", ""),
            evidence=record.get("evidence", ""),
            fix_guidance=record.get("fix_guidance", ""),
            files_affected=record.get("files_affected", []),
            # T2c: registry-path findings default to ACTIVE when status is
            # missing, matching the registry's serialization vocabulary
            # (ACTIVE / FIXED). The Finding dataclass default in models.py
            # remains "PENDING" -- the parser path legitimately uses it
            # (see remediate_parser.py:168,389 and remediate_executor.py:552).
            status=record.get("status", "ACTIVE"),
            agreement_category=record.get("agreement_category", ""),
            deviation_class=record.get("deviation_class", "UNCLASSIFIED"),
        )
        findings.append(finding)

    return findings
