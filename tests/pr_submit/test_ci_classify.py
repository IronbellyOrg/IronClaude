"""Pure tests for ``superclaude.pr_submit.ci`` (spec PR-SUBMIT-CI §13)."""

from __future__ import annotations

from superclaude.pr_submit.ci import (
    classify_checks,
    findings_from_logs,
    is_human_gate,
)
from superclaude.pr_submit.classifier import STATE_CLEAN, STATE_FINDINGS, STATE_POLLING


def test_classify_pending(load_fixture):
    assert classify_checks(load_fixture("checks-pending.json")) == STATE_POLLING


def test_classify_all_pass(load_fixture):
    assert classify_checks(load_fixture("checks-pass.json")) == STATE_CLEAN


def test_classify_empty():
    assert classify_checks({"checks": []}) == STATE_CLEAN
    assert classify_checks({}) == STATE_CLEAN


def test_classify_fail(load_fixture):
    assert classify_checks(load_fixture("checks-fail.json")) == STATE_FINDINGS


def test_classify_cancel():
    payload = {
        "head_sha": "abc",
        "checks": [{"name": "x", "bucket": "cancel", "state": "COMPLETED"}],
    }
    assert classify_checks(payload) == STATE_FINDINGS


def test_classify_required_fallback():
    """Classify operates on the list it is given (script already chose required-or-all)."""
    payload = {
        "checks": [
            {"name": "required", "bucket": "pass", "state": "COMPLETED"},
            {"name": "optional", "bucket": "fail", "state": "COMPLETED"},
        ]
    }
    assert classify_checks(payload) == STATE_FINDINGS


def test_classify_stale_head_is_polling(load_fixture):
    payload = load_fixture("checks-fail.json")
    assert classify_checks(payload, wait_sha="other") == STATE_POLLING
    assert classify_checks(payload, wait_sha="abc123") == STATE_FINDINGS


def test_is_human_gate():
    assert is_human_gate({"name": "Mechanical-merge boundary touched", "bucket": "fail"})
    assert is_human_gate({"name": "x", "state": "ACTION_REQUIRED", "bucket": "fail"})
    assert is_human_gate({"name": "x", "bucket": "cancel"})
    assert not is_human_gate({"name": "Quick Test", "bucket": "fail"})


def test_parse_pytest_line():
    log = "tests/foo.py:12: in test_x\n    assert 1 == 2\n"
    findings = findings_from_logs(
        [{"name": "t", "bucket": "fail", "link": "runs/1"}],
        {"1": log},
    )
    assert len(findings) == 1
    assert findings[0].path == "tests/foo.py"
    assert findings[0].line == 12


def test_parse_ruff_line():
    log = "src/a.py:3:1: F401 unused import\n"
    findings = findings_from_logs(
        [{"name": "lint", "bucket": "fail", "link": "runs/1"}],
        {"1": log},
    )
    assert len(findings) == 1
    assert findings[0].path == "src/a.py"
    assert findings[0].line == 3


def test_unparseable_empty():
    assert (
        findings_from_logs(
            [{"name": "t", "bucket": "fail", "link": "runs/1"}],
            {"1": "job failed, no file locus\n"},
        )
        == []
    )


def test_no_severity_hint():
    log = "tests/foo.py:12: in test_x\n"
    findings = findings_from_logs(
        [{"name": "t", "bucket": "fail", "link": "runs/1"}],
        {"1": log},
    )
    assert findings[0].severity_hint is None


def test_human_gate_skipped_in_logs():
    log = "tests/foo.py:12: in test_x\n"
    findings = findings_from_logs(
        [
            {
                "name": "Mechanical-merge boundary touched",
                "bucket": "fail",
                "link": "runs/1",
            }
        ],
        {"1": log},
    )
    assert findings == []
