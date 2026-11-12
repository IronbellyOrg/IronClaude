"""Contract lint for panel-run reflect output directories (the reflect Tier 2 panel, Stages 0-2).

lint_panel_contract(out_dir, legacy_contract) returns the failure lines of a panel run's return-contract.yaml
against the frozen 1.8.0 contract; an empty list is a pass. It is a read-only checker: it reads
out_dir/return-contract.yaml, out_dir/panel/manifest.json, out_dir/adversarial/merged-verdict.yaml,
out_dir/reviewer-cards/ and out_dir/audit.log, and writes nothing. The assertion ids (L0 to L7, B) and their exact
messages are those of the plan's lint design (artifacts/lint-test-design.md of the managed package).

Limit: the EV-1 check reads the interactive layout out_dir/adversarial/ that recorded pre runs and the Stage 2
shadow mode use. The --unattended layout (nested/adversarial-<n>/, SKILL.md section 8) is not covered; on such a
run L6 reports `merged-verdict: absent`. The lint is meant for panel-run contracts and the matched legacy fixture,
not as a retro-check of every recorded run.

STABLE_FIELDS_1_8_0 and TELEMETRY_FIELDS are copies of the top-level keys of the YAML blocks of SKILL.md sections
9.1 and 9.2. Those blocks do not parse as YAML (they hold `a | b` value forms), so the keys are taken line by line:
every line of the block matching ^([a-z_0-9]+): (no indent). extract_field_list applies that rule, and a test fails
when the constants and the SKILL.md sections differ.
"""

from __future__ import annotations

import json
import math
import os
import re
from pathlib import Path
from typing import Any

import yaml

from .contract import _LOAD_BEARING_BOOL_FIELDS

STABLE_FIELDS_1_8_0 = (
    "contract_version",
    "status",
    "mode",
    "tier_reached",
    "report_path",
    "audit_log_path",
    "confidence_calibrated",
    "escalation_rule_matched",
    "onboarding_ran",
    "coverage_pct",
    "coverage_pct_union",
    "coverage_undefined",
    "coverage_degraded",
    "unmapped_requirements",
    "unmapped_requirements_union",
    "best_practice_grade",
    "implementation_coverage_pct",
    "missing_implementations",
    "hierarchy_slice_path",
    "hierarchy_coverage_pct",
    "tasklist_completion_pct",
    "deviation_count_by_class",
    "deviation_register_path",
    "grounding_gaps_path",
    "hunk_to_declaration_map_path",
    "third_party_api_grounding",
    "third_party_api_verified",
    "verification_ran",
    "verification_invocations",
    "verification_failures",
    "verification_regressions_detected",
    "verification_skip_reason",
    "runtime_surface_requirements",
    "runtime_surface_sweep_ran",
    "runtime_surface_ledger_path",
    "runtime_surface_unreached",
    "runtime_surface_degraded",
    "unreached_surfaces",
    "reachability_gate_ran",
    "reachability_ledger_path",
    "reachability_requirements_scanned",
    "reachability_unreachable",
    "reachability_unproven",
    "reachability_real_boot_ran",
    "reachability_skip_reason",
    "reuse_sweep_ran",
    "reuse_audit_path",
    "reuse_miss_blocking",
    "reuse_miss_advisory",
    "reuse_verdict_count_by_type",
    "reuse_grounding_gap_count",
    "neighbour_search_sampled",
    "neighbour_search_degraded",
    "max_overlap_score",
    "input_sha256",
    "input_tree_sha256",
    "input_tree_file_count",
    "input_tree_snapshot_path",
    "input_drift_detected",
    "input_drift_diff",
    "citations_total",
    "citations_revalidated",
    "citations_dropped",
    "citations_dropped_extrapolated",
    "citations_inferred",
    "citation_budget_policy",
    "evidence_validator_ran",
    "citation_revalidation_at_promotion",
    "reviewer_cards",
    "adversarial_artifacts_dir",
    "adversarial_convergence_score",
    "adversarial_unavailable",
    "merge_method",
    "t2_model_class_diversity",
    "t2_vendor_diversity",
    "t2_effective_diversity",
    "calibrator_diversity",
    "remediation_offered",
    "remediation_accepted",
    "task_file_path",
    "remediation_task_path",
    "remediation_plan_path",
    "handoff_memory_key",
    "cannot_validate_without_user_input",
    "regression_present",
    "unauthorized_deviation_present",
    "blocked_by_low_confidence",
    "spec_is_wrong",
    "user_decision_required",
    "needs_human_decision",
    "per_task_verdicts",
    "interaction_effects_scanned",
    "interaction_effects_findings",
    "budget_forced_tier_downgrade",
    "budget_forced_stop",
    "budget_check_skipped",
    "forced_tier",
    "promotion_action",
    "promotion_adapter",
    "promotion_source",
    "promotion_destination",
    "promotion_log_path",
    "promotion_gate_passed",
    "promotion_skip_reason",
    "promotion_fail_reason",
    "promotion_override_used",
    "promotion_rollback_command",
    "promotion_checkpoint_path",
    "promotion_cross_fs",
    "promotion_pending",
)

TELEMETRY_FIELDS = (
    "wave_durations_ms",
    "token_usage",
    "reviewer_models",
    "reviewer_personas",
    "reviewer_vendors",
    "degraded_components",
    "fallback_path",
    "executor_class_source",
    "executor_class_resolved",
    "executor_exclusion_degraded",
    "citations_dropped_extrapolated",
    "memory_hits",
    "memory_misses",
    "memory_retention_actions",
    "verify_blocked",
    "verify_blocked_reason",
    "verify_timeout_hit",
    "verify_flaky_suspected",
    "verify_timeout_default",
    "verify_invocations_path",
    "handoff_memory_written",
    "handoff_payload_size_bytes",
    "handoff_persist_failed",
    "type_hierarchy_invoked",
    "summarize_changes_invoked",
    "references_extended_info_used",
    "telemetry",
)

LOAD_BEARING_BOOLS = _LOAD_BEARING_BOOL_FIELDS
PARITY_FIELDS = (
    "t2_model_class_diversity",
    "t2_vendor_diversity",
    "t2_effective_diversity",
    "calibrator_diversity",
    "reviewer_cards",
)
LEGAL_MERGE_METHODS = ("adversarial", "single-reviewer-fallback")
CONTRACT_VERSION = "1.8.0"

_KEY_LINE = re.compile(r"(?m)^([a-z_0-9]+):")
_CARD_FILE = re.compile(r"^reviewer-(\d+)-card\.(?:yaml|yml|md)$")
_FALLBACK_ROW = re.compile(r"\bF[23]\b")


def extract_field_list(skill_text: str, heading: str) -> list[str]:
    """Top-level keys of the first ```yaml block after `heading` in SKILL.md text (see the module docstring)."""
    start = skill_text.index(heading)
    first = skill_text.index("```yaml\n", start) + len("```yaml\n")
    last = skill_text.index("\n```", first)
    return _KEY_LINE.findall(skill_text[first:last])


def _read_yaml_mapping(path: Path) -> tuple[str, dict | None]:
    """('absent' | 'unparseable' | 'ok', mapping)."""
    if not path.is_file():
        return "absent", None
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (
        OSError,
        ValueError,
        yaml.YAMLError,
    ):  # ValueError covers UnicodeDecodeError
        return "unparseable", None
    return ("ok", data) if isinstance(data, dict) else ("unparseable", None)


def _positive_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 1


def _card_count(cards_dir: Path) -> int:
    if not cards_dir.is_dir():
        return 0
    found = set()
    for p in cards_dir.iterdir():
        m = _CARD_FILE.match(p.name)
        if m and p.is_file():
            found.add(m.group(1))
    return len(found)


def _basenames(value: Any) -> Any:
    if isinstance(value, list):
        return sorted(os.path.basename(str(v)) for v in value)
    return value


def ev1_failures(
    out_dir: str | Path, contract: dict, *, use_manifest: bool = True
) -> list[str]:
    """The EV-1 failure lines (L6) of a run directory; use_manifest=False takes the count from len(reviewer_cards).

    The Stage 2 aggregator compares shadow runs with the legacy baseline under the same rule, so it passes False.
    """
    return _ev1(Path(out_dir), contract, use_manifest=use_manifest)


def _ev1(out: Path, c: dict, *, use_manifest: bool = True) -> list[str]:
    """L6m, L6a and L6b: the EV-1 merge gate as it stands on disk."""
    lines: list[str] = []
    cards = c.get("reviewer_cards")
    resolved = len(cards) if isinstance(cards, list) else 0
    source = "len(reviewer_cards)"
    manifest = out / "panel" / "manifest.json"
    if use_manifest and manifest.is_file():
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            data = None
        if not isinstance(data, dict) or (
            "reviewers_resolved" in data
            and not _positive_int(data["reviewers_resolved"])
        ):
            lines.append(
                "L6 EV-1: panel/manifest.json is not a JSON object with a positive integer reviewers_resolved"
            )
        elif "reviewers_resolved" in data:
            resolved = data["reviewers_resolved"]
            source = "reviewers_resolved from panel/manifest.json"
    required = max(2, resolved)
    if resolved < 2:
        source = "minimum 2"
    state, verdict = _read_yaml_mapping(out / "adversarial" / "merged-verdict.yaml")
    if state == "ok" and verdict.get("merge_method") == "adversarial":
        held = _card_count(out / "reviewer-cards")
        if held < required:
            lines.append(
                f"L6 EV-1: reviewer-cards/ holds {held} card(s), fewer than the required {required} ({source})"
            )
        return lines
    mv_state = (
        state if state != "ok" else f"merge_method {verdict.get('merge_method')!r}"
    )
    audit = out / "audit.log"
    try:
        rows = audit.read_text(encoding="utf-8").splitlines() if audit.is_file() else []
    except (OSError, ValueError):
        rows = []
    missing = []
    if c.get("adversarial_unavailable") is not True:
        missing.append("adversarial_unavailable: true")
    if c.get("merge_method") != "single-reviewer-fallback":
        missing.append("merge_method: single-reviewer-fallback")
    if not any(_FALLBACK_ROW.search(r) for r in rows):
        missing.append("audit.log F2/F3 row")
    if missing:
        lines.append(
            "L6 EV-1: neither a merged adversarial verdict nor a loud fallback is on disk "
            f"(merged-verdict: {mv_state}; fallback missing: {', '.join(missing)})"
        )
    return lines


def lint_panel_contract(out_dir: str | Path, legacy_contract: dict) -> list[str]:
    """Failure lines of the panel run in out_dir against the 1.8.0 contract and the matched legacy contract."""
    out = Path(out_dir)
    state, c = _read_yaml_mapping(out / "return-contract.yaml")
    if state != "ok":
        return [
            "L0 contract: return-contract.yaml is missing, unparseable or not a mapping"
        ]
    lines: list[str] = []
    version = c.get("contract_version")
    if version != CONTRACT_VERSION:
        lines.append(
            f"L1 contract_version: expected {CONTRACT_VERSION!r}, got {version!r}"
        )
    known = set(STABLE_FIELDS_1_8_0) | set(TELEMETRY_FIELDS) | {"telemetry"}
    key_lines = [
        f"L2 stable keys: top-level key {k!r} is not in the 1.8.0 stable field list or the telemetry block"
        for k in sorted((k for k in c if k not in known), key=str)
    ]
    lines += key_lines
    if "telemetry" in c and not isinstance(c["telemetry"], dict):
        lines.append(
            f"L2 stable keys: 'telemetry' must be a mapping, got {type(c['telemetry']).__name__}"
        )
    tier = c.get("tier_reached")
    wave4 = not (isinstance(tier, int) and not isinstance(tier, bool) and tier == 1)
    merge = c.get("merge_method")
    legal = merge in LEGAL_MERGE_METHODS if isinstance(merge, str) else False
    l3_failed = not legal if wave4 else not (merge is None or legal)
    if l3_failed:
        lines.append(
            f"L3 merge_method: {merge!r} is not a legal 1.8.0 value (EV-2: 'adversarial' or 'single-reviewer-fallback')"
        )
    score = c.get("adversarial_convergence_score")
    if score is not None and not (type(score) is float and math.isfinite(score)):
        lines.append(
            f"L4 adversarial_convergence_score: expected a float or null, got {score!r}"
        )
    required_when_wave4 = {"adversarial_unavailable", "regression_present"}
    for field in sorted(LOAD_BEARING_BOOLS):
        value = c.get(field)
        if (value is None and wave4 and field in required_when_wave4) or (
            value is not None and not isinstance(value, bool)
        ):
            lines.append(f"L5 {field}: expected a real boolean, got {value!r}")
    if wave4:
        lines += _ev1(out, c)
    for field in PARITY_FIELDS:
        panel_value, legacy_value = c.get(field), legacy_contract.get(field)
        if field == "reviewer_cards":
            panel_value, legacy_value = (
                _basenames(panel_value),
                _basenames(legacy_value),
            )
        if panel_value != legacy_value:
            lines.append(
                f"L7 parity {field}: panel {panel_value!r} differs from matched legacy {legacy_value!r}"
            )
    if key_lines or l3_failed:
        lines.append(
            f"B bump rule: the contract leaves 1.8.0 ({len(key_lines)} stable-key violation(s), "
            f"{1 if l3_failed else 0} EV-2 value violation(s)); a new stable key or merge_method value needs a "
            "contract version bump, which this plan does not make"
        )
    return lines
