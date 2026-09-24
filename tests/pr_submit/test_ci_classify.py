"""Pure tests for ``superclaude.pr_submit.ci`` (spec PR-SUBMIT-CI §13)."""

from __future__ import annotations

from superclaude.pr_submit.ci import (
    classify_checks,
    findings_from_logs,
    is_human_gate,
)
from superclaude.pr_submit.classifier import STATE_CLEAN, STATE_FINDINGS, STATE_POLLING


def _link(run: str) -> str:
    return f"https://example.test/o/r/actions/runs/{run}"


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
    assert is_human_gate(
        {"name": "Mechanical-merge boundary touched", "bucket": "fail"}
    )
    assert is_human_gate({"name": "x", "state": "ACTION_REQUIRED", "bucket": "fail"})
    assert is_human_gate({"name": "x", "bucket": "cancel"})
    assert not is_human_gate({"name": "Quick Test", "bucket": "fail"})


def test_parse_pytest_line():
    log = "tests/foo.py:12: in test_x\n    assert 1 == 2\n"
    findings = findings_from_logs(
        [{"name": "t", "bucket": "fail", "link": _link("1")}],
        {"1": log},
    )
    assert len(findings) == 1
    assert findings[0].path == "tests/foo.py"
    assert findings[0].line == 12


def test_parse_ruff_line():
    log = "src/a.py:3:1: F401 unused import\n"
    findings = findings_from_logs(
        [{"name": "lint", "bucket": "fail", "link": _link("1")}],
        {"1": log},
    )
    assert len(findings) == 1
    assert findings[0].path == "src/a.py"
    assert findings[0].line == 3


def test_unparseable_empty():
    assert (
        findings_from_logs(
            [{"name": "t", "bucket": "fail", "link": _link("1")}],
            {"1": "job failed, no file locus\n"},
        )
        == []
    )


def test_no_severity_hint():
    log = "tests/foo.py:12: in test_x\n"
    findings = findings_from_logs(
        [{"name": "t", "bucket": "fail", "link": _link("1")}],
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
                "link": "https://github.com/o/r/actions/runs/1",
            }
        ],
        {"1": log},
    )
    assert findings == []


def test_log_for_does_not_match_run_id_prefix():
    findings = findings_from_logs(
        [
            {
                "name": "t",
                "bucket": "fail",
                "link": "https://github.com/o/r/actions/runs/12345",
            }
        ],
        {
            "1234": "tests/a.py:1: in test_a\n",
            "12345": "tests/b.py:2: in test_b\n",
        },
    )
    assert [f.path for f in findings] == ["tests/b.py"]
    assert findings[0].line == 2


def test_cap_is_per_run_not_global():
    first = "".join(f"tests/a.py:{i}: in t\n" for i in range(1, 16))
    findings = findings_from_logs(
        [
            {
                "name": "one",
                "bucket": "fail",
                "link": "https://github.com/o/r/actions/runs/1",
            },
            {
                "name": "two",
                "bucket": "fail",
                "link": "https://github.com/o/r/actions/runs/2",
            },
        ],
        {"1": first, "2": "tests/b.py:1: in t\n"},
    )
    assert sum(1 for f in findings if f.path == "tests/a.py") == 10
    assert any(f.path == "tests/b.py" and f.line == 1 for f in findings)


def test_parse_prefixed_job_log_line():
    log = "Quick Test\tRun tests\ttests/foo.py:12: in test_x\n"
    findings = findings_from_logs(
        [{"name": "t", "bucket": "fail", "link": _link("1")}],
        {"1": log},
    )
    assert len(findings) == 1
    assert findings[0].path == "tests/foo.py"
    assert findings[0].line == 12


def test_missing_run_link_does_not_borrow_other_log():
    findings = findings_from_logs(
        [{"name": "t", "bucket": "fail", "link": "https://example.test/no-run"}],
        {"1": "tests/foo.py:12: in test_x\n"},
    )
    assert findings == []
