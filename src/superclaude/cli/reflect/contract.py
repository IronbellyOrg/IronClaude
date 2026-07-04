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

import math
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
    {"read-only-project", "tool-unavailable", "--no-verify", "no-verification-stage"}
)

_DEVIATION_KEYS = ("authorized", "necessary", "drift", "regression")

# F2 (fail-closed): load-bearing booleans whose halt/degrade triggers use strict
# identity (`is True` / `is False`). A malformed-but-truthy value (e.g. the string
# "true" or the int 1) is NOT `is True`, so the trigger would silently not fire and
# a contract could leak to PASS. When any of these is PRESENT and non-None but not
# an actual bool, route BLOCKED (mirrors the malformed-degraded-components guard).
_LOAD_BEARING_BOOL_FIELDS = frozenset(
    {
        "regression_present",
        "unauthorized_deviation_present",
        "needs_human_decision",
        "user_decision_required",
        "adversarial_unavailable",
        "input_drift_detected",
        "verification_ran",
    }
)


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
        # FR-8: the wrapper only READS the path reflect emits; it never guesses
        # a "newest TASK-RF-* dir". Defaults to None when reflect did not author one.
        remediation_task_path=c.get("remediation_task_path"),
    )


def derive_verdict(
    contract: dict | None,
    *,
    expected_tier: int,
    allow_single_vendor: bool,
    child_rc: int,
    promoting: bool = False,
) -> ReflectResult:
    """Derive the 4-state verdict per spec Section 6 (first-match-wins).

    Ordering: blocked -> degraded -> halted -> pass.

    Args:
        contract: parsed ``return-contract.yaml`` mapping, or ``None``.
        expected_tier: the tier the wrapper expected (2 for a T2 post gate).
        allow_single_vendor: suppress the single-vendor degradation (FR-11).
        child_rc: the child ``claude`` exit code (124 == timeout).
        promoting: True when the run may mutate the tree (``--promote``); drops the
            ``tool-unavailable``/``read-only-project`` verification-skip exemptions so
            an unverified promoting audit degrades. Default ``False`` keeps advisory/
            stub/legacy callers unchanged.
    """
    # -- 1. BLOCKED (fail-loud) ------------------------------------------------
    if child_rc == 124:
        return _make_result(
            Verdict.BLOCKED, reason="timeout", contract=contract, child_rc=child_rc
        )
    # F0 (fail-closed): ANY non-zero exit vetoes a present contract before its
    # success fields are trusted. The 124 timeout above is now a labelled subset;
    # every other non-zero rc routes BLOCKED/child-crash (spec Section 6 row 1,
    # FR-8). contract is passed through (it may be present) for telemetry.
    if child_rc != 0:
        return _make_result(
            Verdict.BLOCKED, reason="child-crash", contract=contract, child_rc=child_rc
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

    # F2 (fail-closed): a PRESENT load-bearing boolean that is not an actual bool
    # is malformed -> BLOCKED before any degraded/halted/pass decision. Absent or
    # None fields flow normally; only present non-bool values block.
    for _field in _LOAD_BEARING_BOOL_FIELDS:
        if _field in contract:
            _value = contract[_field]
            if _value is not None and not isinstance(_value, bool):
                return _make_result(
                    Verdict.BLOCKED,
                    reason="malformed-contract-boolean",
                    contract=contract,
                    child_rc=child_rc,
                )

    # -- 2. DEGRADED (chain-critical loss -> audit untrustworthy) -------------
    degraded_reason = _degraded_reason(
        contract,
        degraded_components=degraded_components,
        tier_reached=tier_reached,
        expected_tier=expected_tier,
        allow_single_vendor=allow_single_vendor,
        promoting=promoting,
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
    promoting: bool = False,
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

    # Trigger 11a (R-002 D-C2 #5): adversarial sub-status partial/failed -> DEGRADE.
    # Keyed on the ADVERSARIAL child's status verbatim (NOT the worst-of telemetry
    # ``subrun_status``/``subrun_status_partial``), so a benign 2-of-3 swarm quorum
    # loss with a healthy adversarial run does NOT degrade (test_i3 stays green).
    if contract.get("adversarial_subrun_status") in ("partial", "failed"):
        return "degraded-subrun-partial"

    # Trigger 11b (R-002 D-C2 #6): present-but-low adversarial convergence at T2.
    # A present score below 0.80 (the incident 0.75) degrades where the null-
    # convergence trigger above missed it. The more-specific null case precedes this.
    # A non-finite score (NaN/Inf) is an untrustworthy adversarial merge and MUST
    # degrade too -- ``float("nan")`` does not raise and ``nan < 0.80`` is False, so
    # without the ``isfinite`` guard a NaN/Inf convergence would bypass both this and
    # the ``is None`` null-convergence trigger and wrongly stay PASS-eligible.
    _score = contract.get("adversarial_convergence_score")
    if tier_reached == 2 and _score is not None:
        try:
            _score_f = float(_score)
        except (TypeError, ValueError):
            _score_f = None
        if _score_f is not None and (not math.isfinite(_score_f) or _score_f < 0.80):
            return "low-convergence"

    # Trigger 12: verification didn't run, unless exempted.
    if contract.get("verification_ran") is False:
        skip_reason = contract.get("verification_skip_reason")
        # Promote-tightening (R-002 D-C1, CORRECTED): a --promote run that skipped
        # verification for ``tool-unavailable``/``read-only-project`` must NOT be
        # exempt -> DEGRADED, so an unverified audit can never mutate the tree. The
        # honest ``no-verification-stage`` slug STAYS exempt even under promote (the
        # ensemble has no verification stage; dropping it would brick every
        # ``--promote --depth deep`` run) as does the explicit ``--no-verify`` opt-out.
        # Subtract into a per-call local -- never mutate the frozenset constant.
        effective_exemptions = _VERIFICATION_SKIP_EXEMPTIONS
        if promoting:
            effective_exemptions = effective_exemptions - {
                "tool-unavailable",
                "read-only-project",
            }
        if skip_reason not in effective_exemptions:
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
    # F5: a `status: failed` contract halts (exit 10, already correct) with the
    # accurate `status-failed` slug instead of falling through to `tier-mismatch`.
    if contract.get("status") == "failed":
        return "status-failed"
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


def classify_fix(contract: dict, deviations: dict[str, int]) -> str:
    """Pure AUTO-FIXABLE vs HUMAN-REQUIRED carve-out (D4 / contract Section 4).

    Returns one of ``"human-required"`` / ``"auto-fixable"`` / ``"none"``.

    HUMAN-REQUIRED on ANY hard signal: ``regression_present``,
    ``needs_human_decision``, ``user_decision_required``,
    ``unauthorized_deviation_present`` (each ``is True``), or
    ``deviation_count_by_class.regression > 0``. AUTO-FIXABLE only when, with NO
    hard signal, the register is solely drift/necessary
    (``drift > 0 or necessary > 0``). Otherwise ``"none"`` (clean).

    PURE: no Click, no subprocess, no I/O -- keys off the SAME existing contract
    fields ``_halted_reason`` reads (no new parse).

    LOAD-BEARING INVARIANT: the grounding-gaps -> HUMAN-REQUIRED carve-out
    (merged-requirements Section 3 / contract Section 4) rests ENTIRELY on
    reflect's contract guarantee that ``needs_human_decision is True`` IFF
    ``grounding-gaps.yaml`` is non-empty (SKILL.md:754). This wrapper does NOT
    re-parse grounding-gaps; a grounding-gaps-only audit surfaces as
    ``needs_human_decision`` and therefore classifies ``human-required`` ->
    terminal HALT, never auto-promoted. Consulted ONLY on a trustworthy HALTED
    result (DEGRADED/BLOCKED are terminal upstream in ``derive_verdict`` and
    re-guarded in the runner loop).
    """
    if (
        contract.get("regression_present") is True
        or contract.get("needs_human_decision") is True
        or contract.get("user_decision_required") is True
        or contract.get("unauthorized_deviation_present") is True
        or deviations.get("regression", 0) > 0
    ):
        return "human-required"
    if deviations.get("drift", 0) > 0 or deviations.get("necessary", 0) > 0:
        return "auto-fixable"
    return "none"
