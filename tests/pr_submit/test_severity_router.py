"""Severity-router tests (spec FR-3.1/FR-3.2).

T-301 `severity_hint=low`+category=security → Critical (floor); T-302
`severity_hint=critical`+`confidence=low` → High (confidence drop); T-310 Medium →
route `--fix` only; T-311 High → `--depth deep --fix`; T-312 Low → troubleshoot NOT
called (report-only); T-N30 router remap coverage over the finding-medium/high
fixtures. No test asserts `--depth quick --fix`. Asserts against the rubric's own
calibration shapes (severity-rubric.md:104-152) so the reuse is provably faithful.
"""

from __future__ import annotations

import pytest

from superclaude.pr_submit import (
    DetectionContract,
    Finding,
    Severity,
    actionable_finding_comments,
    classify,
    finding_from_comment,
    remap_severity,
    route,
)
from superclaude.pr_submit.fsm import is_groundable


def _f(**kw) -> Finding:
    base = dict(path="src/x.py", line=1, body="b", in_diff=True)
    base.update(kw)
    return Finding(**base)


def test_t301_security_floor_overrides_low_hint():
    """T-301: `severity_hint=low` but category=security → remapped Critical (floor)."""
    f = _f(severity_hint="low", category="security", confidence="high")
    assert remap_severity(f).remapped_severity is Severity.CRITICAL


def test_t302_confidence_low_drops_critical_to_high():
    """T-302: `severity_hint=critical` but `confidence=low` → remapped High (drop one tier)."""
    f = _f(severity_hint="critical", category="correctness", confidence="low")
    assert remap_severity(f).remapped_severity is Severity.HIGH


def test_t310_medium_routes_fix_only():
    """T-310: a Medium finding routes to `--fix` ONLY (never `--depth deep`/`--depth quick`)."""
    f = _f(severity_hint="medium", category="correctness", confidence="medium")
    assert remap_severity(f).remapped_severity is Severity.MEDIUM
    decision = route(f)
    assert decision == "--fix"
    assert "--depth deep" not in decision
    assert "--depth quick" not in decision


def test_t311_high_routes_depth_deep_fix():
    """T-311: a High finding routes to `--depth deep --fix`."""
    f = _f(severity_hint="high", category="resource-leak", confidence="high")
    assert remap_severity(f).remapped_severity is Severity.HIGH
    assert route(f) == "--depth deep --fix"


def test_t312_low_is_report_only_not_dispatched():
    """T-312: a Low finding is report-only — troubleshoot is NOT called."""
    f = _f(severity_hint="low", category="dead-code", confidence="high")
    assert remap_severity(f).remapped_severity is Severity.LOW
    assert route(f) == "report-only"


def test_tn30_router_remap_coverage(load_fixture):
    """T-N30: router remap coverage over the finding-medium / finding-high fixtures."""
    for name, expected_route in (
        ("finding-medium.json", "--fix"),
        ("finding-high.json", "--depth deep --fix"),
    ):
        raw = load_fixture(name)
        for fd in raw["findings"]:
            f = Finding(
                path=fd["path"],
                line=fd["line"],
                body=fd["body"],
                severity_hint=fd.get("severity_hint"),
                category=fd.get("category"),
                confidence=fd.get("confidence"),
                in_diff=fd.get("in_diff", True),
            )
            decision = route(f)
            assert decision == expected_route
            assert decision != "--depth quick --fix"


@pytest.mark.parametrize(
    ("body", "hint", "expected"),
    [
        ("Defect.\n\n**Severity:** low", None, Severity.LOW),
        ("Defect.\r\n\r\n**Severity:** low\r\n", None, Severity.LOW),
        ("Defect.\r\n\r\n**Severity:** low\r\n", "low", Severity.LOW),
        ("**sEvErItY:** HIGH", None, Severity.HIGH),
        ("plain finding", "low", Severity.LOW),
        ("**Severity:** low", "HIGH", Severity.HIGH),
        ("plain finding", None, Severity.MEDIUM),
        ("**Severity:** unfamiliar", None, Severity.MEDIUM),
        ("**Severity:** low", "unfamiliar", Severity.MEDIUM),
        ("Example **Severity:** low in prose", None, Severity.MEDIUM),
        ("**Severity:** low\n**Severity:** high", None, Severity.MEDIUM),
    ],
)
def test_raw_severity_normalization(body, hint, expected):
    finding = finding_from_comment(
        {"path": "src/x.py", "line": 1, "body": body, "severity_hint": hint}
    )
    assert finding.body == body
    assert remap_severity(finding).remapped_severity is expected


def test_raw_low_hint_still_obeys_category_floor_and_verification():
    finding = finding_from_comment(
        {
            "path": "src/x.py",
            "line": 1,
            "body": "**Severity:** low",
            "category": "security",
            "verification_status": "verified",
            "remapped_severity": "Low",
        }
    )
    assert finding.verification_status == "unverified"
    assert remap_severity(finding).remapped_severity is Severity.CRITICAL
    assert route(finding) == "--depth deep --fix"


def test_selected_cosmos_root_normalizes_same_identity_and_nullable_locus(load_fixture):
    payload = load_fixture("cosmos-pr266.json")
    payload["threads"][0]["isResolved"] = False
    contract = DetectionContract.for_arming()
    context = {"watermark": "2026-10-16T19:30:00Z"}
    assert classify(payload, contract, **context) == "findings"
    selected = actionable_finding_comments(payload, contract, **context)
    findings = [finding_from_comment(root) for root in selected]
    assert len(findings) == 1
    finding = findings[0]
    assert finding.comment_id == 4296483537
    assert finding.thread_id == "PRRT_pr266_example"
    assert finding.review_id == 5550158176
    assert finding.line is None
    assert finding.original_line == 172
    assert finding.is_outdated is True
    assert finding.verification_status == "unverified"
    assert not is_groundable(finding)
    assert route(finding) == "report-only"
    payload["threads"][0]["isResolved"] = True
    assert classify(payload, contract, **context) == "clean"
    assert actionable_finding_comments(payload, contract, **context) == []


@pytest.mark.parametrize(
    "override",
    [
        {"path": ""},
        {"body": None},
        {"line": True},
        {"original_line": -1},
        {"severity_hint": []},
        {"in_diff": "false"},
        {"comment_id": True},
        {"thread_id": ""},
        {"review_id": False},
    ],
)
def test_raw_finding_rejects_malformed_boundary_values(override):
    raw = {"path": "src/x.py", "line": 1, "body": "Defect.", **override}
    with pytest.raises(ValueError):
        finding_from_comment(raw)
