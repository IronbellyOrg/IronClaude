"""Output-contract integration tests (Steps 7.10 / 7.11 / 7.12).

Content-assertion tests over the source-of-truth markdown:
- SKILL.md Output Contract (backward-compat / additive fields, NFR-6 / FR-13 AC1)
- hardening-output-contract.md backtest-status table (NFR-1)
- report-template.md Pipeline Hardening Closure section (FR-13 AC3)
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "src" / "superclaude" / "skills" / "sc-troubleshoot-protocol"
REFS = SKILL_DIR / "refs"
SKILL = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
OC = (REFS / "hardening-output-contract.md").read_text(encoding="utf-8")
RT = (REFS / "report-template.md").read_text(encoding="utf-8")

# The 19 pre-existing Output Contract result fields (skill-anchors.md §(c)).
LEGACY_FIELDS = (
    "status",
    "tier_reached",
    "report_path",
    "audit_log_path",
    "confidence",
    "escalation_reason",
    "test_is_wrong",
    "test_file_path",
    "behavior_is_documented",
    "doc_context_card_path",
    "hypothesis_cards",
    "adversarial_artifacts_dir",
    "task_file_path",
    "remediation_offered",
    "remediation_accepted",
    "diagnosability_verdict",
    "diagnosability_context_card_path",
    "diagnosability_tasklist_path",
    "diagnosability_hard_stop",
)

# The 11 additive Pipeline Hardening Closure fields (§5.5).
HARDENING_FIELDS = (
    "contract_version",
    "pipeline_hardening_applicable",
    "pipeline_hardening_verdict",
    "waiver_status",
    "backtest_status",
    "off_path_review_decision",
    "runtime_entrypoint_card_path",
    "contract_ledger_path",
    "unmask_sweep_path",
    "effective_input_card_path",
    "known_escapes_caught",
)


def test_output_contract_backward_compat() -> None:
    """FR-13 AC1 + NFR-6: the SKILL.md Output Contract still contains ALL pre-existing
    result fields (none renamed/removed) AND the new hardening fields are present as
    ADDITIVE additions."""
    for field in LEGACY_FIELDS:
        assert f"`{field}`" in SKILL, (
            f"legacy Output Contract field removed/renamed: {field}"
        )
    for field in HARDENING_FIELDS:
        assert f"`{field}`" in SKILL, f"additive hardening field missing: {field}"


def test_backtest_status_keeps_pipeline_health_advisory_until_complete() -> None:
    """NFR-1: the 3-row backtest-status table documents that not_run and partial keep the
    production-facing pipeline-health signoff advisory even when pipeline_hardening_verdict=pass,
    and only complete may mirror the verdict."""
    for state in ("`not_run`", "`partial`", "`complete`"):
        assert state in OC, f"backtest-status row missing: {state}"
    # not_run -> advisory even if the run-level verdict is pass
    assert "advisory` even if `pipeline_hardening_verdict=pass`" in OC
    # partial -> advisory with missing escape IDs listed
    assert "with missing escape IDs listed" in OC
    # only complete may mirror the verdict
    assert "May mirror `pipeline_hardening_verdict`" in OC


def test_report_closure_section_not_proven_blockers() -> None:
    """FR-13 AC3: report-template.md contains the Pipeline Hardening Closure section, renders
    the FOUR-token pipeline_hardening_verdict (incl. advisory), and uses the NOT PROVEN token
    verbatim for absent required proof."""
    assert "## Pipeline Hardening Closure" in RT
    # FOUR-token verdict, advisory-inclusive (no-space form in the rendered template,
    # spaced form in the rule section — accept either)
    assert (
        "pass|blocked|advisory|not_applicable" in RT
        or "pass | blocked | advisory | not_applicable" in RT
    ), "report-template Closure verdict must be the 4-token advisory-inclusive enum"
    assert "advisory" in RT.lower()
    # NOT PROVEN blocker token verbatim
    assert "NOT PROVEN" in RT
