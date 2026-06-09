"""Isolated contract -> verdict map (spec Section 6) + FR-11 degradation routing.

This is the SINGLE place the verdict map, the FR-11 degradation routing, and
``contract_version`` gating live (Risk Section 10). It is a PURE module:

- Depends ONLY on ``.models`` + stdlib + PyYAML.
- No Click, no subprocess, no reflect-logic strings beyond contract field names.
- Imports NOTHING from ``commands.py`` / ``runner.py`` / ``config.py``.

A wrong verdict map silently leaks a degraded audit as a pass (the load-bearing
defense per the Section 11 invariant probe), so the ordering is exact:
**blocked -> degraded -> halted -> pass**, first-match-wins.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from .models import ReflectResult, Verdict

# ---------------------------------------------------------------------------
# Routing constants
# ---------------------------------------------------------------------------

# FR-11 chain-critical subset: EXACT membership (NOT substring) so benign
# fail-open tokens (search_deps:lsp_unindexed, serena:onboarding-parse,
# serena:pre-v1.5-no-rename-propagation, get_current_config,
# neighbour-search:auggie_unavailable) do NOT over-HALT.
_DEGRADED_COMPONENTS_HALT_SET = frozenset(
    {"serena", "auggie", "env-aliases", "evidence-validator", "serena:context-excluded"}
)

# verification_ran == False is exempt (NOT degradation) for these skip reasons.
_VERIFICATION_SKIP_EXEMPTIONS = frozenset(
    {"read-only-project", "tool-unavailable", "--no-verify"}
)

_DEVIATION_KEYS = ("authorized", "necessary", "drift", "regression")


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


def parse_contract(path: Path) -> dict | None:
    """Parse ``return-contract.yaml``; return ``None`` when unusable.

    Returns ``None`` when the file is missing or YAML-unparseable (so the
    caller routes ``blocked``). Tolerates unknown top-level fields
    (NFR-8 read-and-ignore). A non-mapping document is treated as unusable.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError:
        return None
    if not isinstance(data, dict):
        return None
    return data


# ---------------------------------------------------------------------------
# Verdict derivation
# ---------------------------------------------------------------------------


def _extract_deviations(contract: dict | None) -> dict[str, int]:
    """Pull ``deviation_count_by_class`` as a 4-key int dict (absent -> 0)."""
    raw = (contract or {}).get("deviation_count_by_class") or {}
    if not isinstance(raw, dict):
        raw = {}
    out: dict[str, int] = {}
    for key in _DEVIATION_KEYS:
        try:
            out[key] = int(raw.get(key, 0) or 0)
        except (TypeError, ValueError):
            out[key] = 0
    return out


def _make_result(
    verdict: Verdict,
    *,
    reason: str,
    contract: dict | None,
    child_rc: int,
) -> ReflectResult:
    """Build a ``ReflectResult`` reading contract fields defensively."""
    c = contract or {}
    tier = c.get("tier_reached")
    return ReflectResult(
        verdict=verdict,
        status=c.get("status"),
        tier_reached=tier if isinstance(tier, int) else None,
        reason=reason,
        report_path=c.get("report_path"),
        contract_path=None,  # runner fills the pinned path it parsed
        deviations=_extract_deviations(contract),
        child_exit_code=child_rc,
        write_status="",
    )


def derive_verdict(
    contract: dict | None,
    *,
    expected_tier: int,
    allow_single_vendor: bool,
    child_rc: int,
) -> ReflectResult:
    """Derive the 4-state verdict per spec Section 6 (first-match-wins).

    Ordering: blocked -> degraded -> halted -> pass.

    Args:
        contract: parsed ``return-contract.yaml`` mapping, or ``None``.
        expected_tier: the tier the wrapper expected (2 for a T2 post gate).
        allow_single_vendor: suppress the single-vendor degradation (FR-11).
        child_rc: the child ``claude`` exit code (124 == timeout).
    """
    # -- 1. BLOCKED (fail-loud) ------------------------------------------------
    if child_rc == 124:
        return _make_result(
            Verdict.BLOCKED, reason="timeout", contract=contract, child_rc=child_rc
        )
    if contract is None:
        reason = "child-crash" if child_rc != 0 else "contract-missing"
        return _make_result(
            Verdict.BLOCKED, reason=reason, contract=None, child_rc=child_rc
        )

    version = contract.get("contract_version")
    if version is None or not str(version).strip():
        return _make_result(
            Verdict.BLOCKED,
            reason="contract-version-missing",
            contract=contract,
            child_rc=child_rc,
        )
    major = str(version).strip().split(".")[0].strip()
    if major != "1":
        return _make_result(
            Verdict.BLOCKED,
            reason="unknown-major-version",
            contract=contract,
            child_rc=child_rc,
        )

    # degraded_components is telemetry: absent -> [], malformed -> blocked.
    degraded_components = contract.get("degraded_components", [])
    if degraded_components is None:
        degraded_components = []
    if not isinstance(degraded_components, list):
        return _make_result(
            Verdict.BLOCKED,
            reason="malformed-degraded-components",
            contract=contract,
            child_rc=child_rc,
        )

    tier_reached = contract.get("tier_reached")

    # -- 2. DEGRADED (chain-critical loss -> audit untrustworthy) -------------
    degraded_reason = _degraded_reason(
        contract,
        degraded_components=degraded_components,
        tier_reached=tier_reached,
        expected_tier=expected_tier,
        allow_single_vendor=allow_single_vendor,
    )
    if degraded_reason is not None:
        return _make_result(
            Verdict.DEGRADED,
            reason=degraded_reason,
            contract=contract,
            child_rc=child_rc,
        )

    # -- 3. HALTED (trustworthy audit FOUND deviations/partial) ---------------
    halted_reason = _halted_reason(contract)
    if halted_reason is not None:
        return _make_result(
            Verdict.HALTED, reason=halted_reason, contract=contract, child_rc=child_rc
        )

    # -- 4. PASS (only when status success AND expected tier reached) ---------
    if contract.get("status") == "success" and tier_reached == expected_tier:
        return _make_result(
            Verdict.PASS, reason="pass", contract=contract, child_rc=child_rc
        )

    # Did not satisfy pass (e.g. status success but tier mismatch) -> halted.
    return _make_result(
        Verdict.HALTED,
        reason="tier-mismatch",
        contract=contract,
        child_rc=child_rc,
    )


def _degraded_reason(
    contract: dict,
    *,
    degraded_components: list,
    tier_reached: object,
    expected_tier: int,
    allow_single_vendor: bool,
) -> str | None:
    """Return a degraded reason slug for the first FR-11 trigger, else None."""
    # Triggers 1-5: chain-critical degraded_components (exact membership).
    if any(token in _DEGRADED_COMPONENTS_HALT_SET for token in degraded_components):
        return "degraded-components"

    # Trigger 6: expected-T2 but ran T1.
    if expected_tier >= 2 and tier_reached == 1:
        return "degraded-tier1"

    # Trigger 7: model-class diversity not full (guard T1-null: only when set).
    mcd = contract.get("t2_model_class_diversity")
    if mcd is not None and mcd != "full":
        return "degraded-model-diversity"

    # Trigger 8: vendor diversity single, unless --allow-single-vendor.
    if contract.get("t2_vendor_diversity") == "single" and not allow_single_vendor:
        return "single-vendor"

    # Trigger 9: adversarial merge unavailable.
    if contract.get("adversarial_unavailable") is True:
        return "adversarial-unavailable"

    # Trigger 10: single-reviewer fallback.
    if contract.get("merge_method") == "single-reviewer-fallback":
        return "single-reviewer-fallback"

    # Trigger 11: null convergence at T2 (guard: only when tier_reached == 2).
    if tier_reached == 2 and contract.get("adversarial_convergence_score") is None:
        return "null-convergence"

    # Trigger 12: verification didn't run, unless exempted.
    if contract.get("verification_ran") is False:
        skip_reason = contract.get("verification_skip_reason")
        if skip_reason not in _VERIFICATION_SKIP_EXEMPTIONS:
            return "verification-skipped"

    # Trigger 13: citations dropped (sample-count, NOT extrapolated).
    try:
        if int(contract.get("citations_dropped", 0) or 0) > 0:
            return "citations-dropped"
    except (TypeError, ValueError):
        pass

    # Trigger 14: input drift.
    if contract.get("input_drift_detected") is True:
        return "input-drift"

    return None


def _halted_reason(contract: dict) -> str | None:
    """Return a halted reason slug for the first audit-found problem, else None."""
    if contract.get("status") == "partial":
        return "status-partial"
    if contract.get("regression_present") is True:
        return "regression"
    if contract.get("unauthorized_deviation_present") is True:
        return "unauthorized-deviation"
    if contract.get("needs_human_decision") is True:
        return "needs-human-decision"
    if contract.get("user_decision_required") is True:
        return "user-decision-required"
    deviations = _extract_deviations(contract)
    if deviations["regression"] > 0:
        return "regression"
    if deviations["drift"] > 0:
        return "drift"
    return None
