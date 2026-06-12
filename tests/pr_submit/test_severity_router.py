"""Severity-router tests (spec FR-3.1/FR-3.2).

T-301 `severity_hint=low`+category=security → Critical (floor); T-302
`severity_hint=critical`+`confidence=low` → High (confidence drop); T-310 Medium →
route `--fix` only; T-311 High → `--depth deep --fix`; T-312 Low → troubleshoot NOT
called (report-only); T-N30 router remap coverage over the finding-medium/high
fixtures. No test asserts `--depth quick --fix`. Asserts against the rubric's own
calibration shapes (severity-rubric.md:104-152) so the reuse is provably faithful.
"""

from __future__ import annotations

from superclaude.pr_submit import Finding, Severity, remap_severity, route


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
