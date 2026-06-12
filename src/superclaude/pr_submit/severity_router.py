"""Severity re-grading + troubleshoot routing for the ``sc:pr-submit`` core (C3).

``remap_severity(finding)`` applies the 5-step remap pipeline DEFINED BY the
auggie-review rubric (``sc-auggie-review-protocol/refs/severity-rubric.md``
§Severity-remap algorithm, lines 63-101) — it encodes the rubric's category
floor/ceiling table by reference, it does NOT fork the tier scheme. ``route(finding)``
maps the remapped tier to a troubleshoot route (FR-3.2) and NEVER emits the
``--depth quick --fix`` conflict.

NFR-6 / AC-9 core purity (T-N50): this module contains ZERO shell or
version-control command tokens. Grading and routing are pure functions of the
finding's fields.
"""

from __future__ import annotations

from .models import Finding, Severity

# Severity rank — higher is more severe. Used to clamp to category floor/ceiling
# and to apply the one-tier drops (confidence / diff-locality / cross-source).
_RANK: dict[Severity, int] = {
    Severity.NIT: 0,
    Severity.LOW: 1,
    Severity.MEDIUM: 2,
    Severity.HIGH: 3,
    Severity.CRITICAL: 4,
}
_BY_RANK: dict[int, Severity] = {v: k for k, v in _RANK.items()}

# Category floor/ceiling table — encoded by reference from severity-rubric.md:70-87.
# Each entry is (floor, ceiling); ``None`` means unbounded on that side.
_CATEGORY_TABLE: dict[str, tuple[Severity | None, Severity | None]] = {
    "security": (Severity.CRITICAL, None),  # exploitable today (rubric default)
    "security-latent": (Severity.HIGH, None),
    "data-integrity": (Severity.HIGH, Severity.CRITICAL),
    "correctness": (Severity.MEDIUM, Severity.CRITICAL),
    "concurrency": (Severity.MEDIUM, Severity.HIGH),
    "resource-leak": (Severity.MEDIUM, Severity.HIGH),
    "api-contract": (Severity.MEDIUM, Severity.HIGH),
    "performance": (Severity.LOW, Severity.HIGH),
    "architecture": (Severity.MEDIUM, Severity.HIGH),
    "layering": (Severity.MEDIUM, Severity.HIGH),
    "coupling": (Severity.MEDIUM, Severity.HIGH),
    "anti-pattern": (Severity.LOW, Severity.MEDIUM),
    "dead-code": (Severity.LOW, Severity.LOW),
    "tests": (Severity.MEDIUM, Severity.HIGH),
    "docs": (Severity.LOW, Severity.MEDIUM),
    "logging": (Severity.LOW, Severity.HIGH),
    "naming": (Severity.NIT, Severity.LOW),
    "style": (Severity.NIT, Severity.LOW),
}

# Troubleshoot routes (the NEW C3 logic; NOT in the rubric). NEVER --depth quick --fix.
ROUTE_FIX = "--fix"  # Medium — defaults to --depth standard
ROUTE_DEEP_FIX = "--depth deep --fix"  # High / Critical
ROUTE_REPORT_ONLY = "report-only"  # Low / Nit — not dispatched


def _hint_to_severity(hint: str | None) -> Severity:
    """Map Augment's ``severity_hint`` string to a :class:`Severity` (fail-safe Medium).

    Unknown / absent hints map to Medium (NFR-4 fail-safe default).
    """
    if not hint:
        return Severity.MEDIUM
    normalized = hint.strip().lower()
    for sev in Severity:
        if sev.value.lower() == normalized:
            return sev
    return Severity.MEDIUM


def _clamp(sev: Severity, floor: Severity | None, ceiling: Severity | None) -> Severity:
    """Clamp ``sev`` to the category floor (minimum) and ceiling (maximum)."""
    rank = _RANK[sev]
    if floor is not None:
        rank = max(rank, _RANK[floor])
    if ceiling is not None:
        rank = min(rank, _RANK[ceiling])
    return _BY_RANK[rank]


def _drop_one(sev: Severity) -> Severity:
    """Drop one tier (Critical → High → Medium → Low → Nit; never below Nit)."""
    return _BY_RANK[max(0, _RANK[sev] - 1)]


def remap_severity(finding: Finding, *, deep: bool = False) -> Finding:
    """Apply the rubric's 5-step remap pipeline; set and return ``finding.remapped_severity``.

    Steps (by reference to severity-rubric.md:63-101):
    (1) start from ``severity_hint``; (2) clamp to the category floor/ceiling;
    (3) ``confidence == "low"`` → drop one tier; (4) ``in_diff is False`` (pre-existing,
    untouched) → drop one tier; (5) ``deep`` single-source → drop one tier unless the
    category floor blocks it. The category floor is re-applied after the drops so a
    floor (e.g. exploitable security = Critical) is never violated by a drop.
    """
    sev = _hint_to_severity(finding.severity_hint)

    floor: Severity | None = None
    ceiling: Severity | None = None
    if finding.category:
        floor, ceiling = _CATEGORY_TABLE.get(
            finding.category.strip().lower(), (None, None)
        )

    # Step 2: category floor/ceiling override.
    sev = _clamp(sev, floor, ceiling)

    # Step 3: confidence adjustment.
    if (finding.confidence or "").strip().lower() == "low":
        sev = _drop_one(sev)

    # Step 4: diff-locality adjustment (pre-existing + untouched).
    if finding.in_diff is False:
        category = (finding.category or "").strip().lower()
        if category in ("architecture", "layering", "coupling"):
            # The rubric's architecture/layering note (severity-rubric.md:80-81):
            # "downgrade to Low if pre-existing". A pre-existing, untouched layering
            # violation lands at Low directly (the PR-scope principle), overriding the
            # Medium floor for this category — so the floor is cleared for the
            # re-clamp below.
            sev = Severity.LOW
            floor = None
        else:
            sev = _drop_one(sev)

    # Step 5: cross-source agreement bonus (--depth deep only) — single-source drop.
    if deep:
        sev = _drop_one(sev)

    # Re-apply the category floor so the one-tier drops never breach an exploitable
    # floor (e.g. security stays Critical). Ceiling stays applied too.
    sev = _clamp(sev, floor, ceiling)

    finding.remapped_severity = sev
    return finding


def route(finding: Finding) -> str:
    """Map the remapped severity to a troubleshoot route (FR-3.2).

    Critical/High → ``--depth deep --fix``; Medium → ``--fix`` (defaults to
    ``--depth standard``); Low/Nit → ``report-only`` (not dispatched). NEVER emits
    ``--depth quick --fix``.
    """
    sev = finding.remapped_severity or remap_severity(finding).remapped_severity
    if sev in (Severity.CRITICAL, Severity.HIGH):
        decision = ROUTE_DEEP_FIX
    elif sev is Severity.MEDIUM:
        decision = ROUTE_FIX
    else:
        decision = ROUTE_REPORT_ONLY
    # Invariant guard: the conflicting form is never produced. Use an explicit
    # raise (not ``assert``) so the guard survives ``python -O``.
    if decision == "--depth quick --fix":
        raise RuntimeError(
            "invariant violated: severity router must never emit '--depth quick --fix'"
        )
    return decision
