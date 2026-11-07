"""Pure tests for ``superclaude.pr_submit.ci`` (spec PR-SUBMIT-CI §13)."""

from __future__ import annotations

import pytest

from superclaude.pr_submit.ci import (
    ci_wait_autofix,
    classify_checks,
    expect_checks_after_push,
    findings_from_logs,
    is_human_gate,
    should_arm_ci_wait,
)
from superclaude.pr_submit.classifier import STATE_CLEAN, STATE_FINDINGS, STATE_POLLING
from superclaude.pr_submit.models import MonitorState


def _link(run: str) -> str:
    return f"https://example.test/o/r/actions/runs/{run}"


def test_classify_pending(load_fixture):
    assert classify_checks(load_fixture("checks-pending.json")) == STATE_POLLING


def test_wave8_arm_after_silence_wait_only_not_clean(load_fixture):
    assert should_arm_ci_wait(MonitorState.TERMINAL_AUGMENT_NO_RESPONSE) is True
    assert ci_wait_autofix(MonitorState.TERMINAL_AUGMENT_NO_RESPONSE) is False
    assert should_arm_ci_wait(MonitorState.TERMINAL_TIMEOUT) is False
    assert ci_wait_autofix(MonitorState.TERMINAL_TIMEOUT) is False
    assert classify_checks(load_fixture("checks-pending.json")) == STATE_POLLING


def test_classify_all_pass(load_fixture):
    assert classify_checks(load_fixture("checks-pass.json")) == STATE_CLEAN


def test_classify_empty():
    assert classify_checks({"checks": []}) == STATE_CLEAN
    assert classify_checks({}) == STATE_CLEAN


def test_classify_empty_polling_is_not_clean():
    assert classify_checks({"state": "polling", "checks": []}) == STATE_POLLING


def test_classify_mixed_pass_and_pending():
    assert (
        classify_checks({"checks": [{"bucket": "pass"}, {"bucket": "pending"}]})
        == STATE_POLLING
    )


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


# issue #305 (source section 6.2): ``expect_checks`` and its setter.

_HEAD = "a" * 40


def test_expect_checks_empty_matching_head_is_polling():
    payload = {"head_sha": _HEAD, "checks": []}
    assert classify_checks(payload, wait_sha=_HEAD, expect_checks=True) == STATE_POLLING
    assert classify_checks({"head_sha": _HEAD}, expect_checks=True) == STATE_POLLING
    assert classify_checks({}, expect_checks=True) == STATE_POLLING


def test_expect_checks_nonempty_all_pass_is_clean(load_fixture):
    payload = {
        "head_sha": _HEAD,
        "checks": [{"name": "t", "bucket": "pass", "state": "COMPLETED"}],
    }
    assert classify_checks(payload, wait_sha=_HEAD, expect_checks=True) == STATE_CLEAN
    fixture = load_fixture("checks-pass.json")
    assert classify_checks(fixture, expect_checks=True) == STATE_CLEAN
    fail = load_fixture("checks-fail.json")
    assert classify_checks(fail, expect_checks=True) == STATE_FINDINGS


def test_expect_checks_false_keeps_empty_clean():
    assert classify_checks({"checks": []}, expect_checks=False) == STATE_CLEAN
    assert classify_checks({}, expect_checks=False) == STATE_CLEAN
    assert (
        classify_checks(
            {"head_sha": _HEAD, "checks": []}, wait_sha=_HEAD, expect_checks=False
        )
        == STATE_CLEAN
    )
    assert classify_checks("not a dict", expect_checks=False) == STATE_CLEAN


def test_expect_checks_head_mismatch_is_polling():
    payload = {
        "head_sha": "b" * 40,
        "checks": [{"name": "t", "bucket": "pass", "state": "COMPLETED"}],
    }
    assert classify_checks(payload, wait_sha=_HEAD, expect_checks=True) == STATE_POLLING
    assert (
        classify_checks(payload, wait_sha=_HEAD, expect_checks=False) == STATE_POLLING
    )


def test_expect_checks_non_dict_payload_is_polling():
    for payload in (None, [], "x", 0):
        assert classify_checks(payload, expect_checks=True) == STATE_POLLING
        assert classify_checks(payload) == STATE_CLEAN


def test_expect_checks_after_push_pre_push_evidence_one_is_true():
    assert (
        expect_checks_after_push(
            checks_seen_this_run=False, pre_push_evidence=1, base_evidence=0
        )
        is True
    )


def test_expect_checks_after_push_all_zero_is_false():
    assert (
        expect_checks_after_push(
            checks_seen_this_run=False, pre_push_evidence=0, base_evidence=0
        )
        is False
    )


def test_expect_checks_after_push_failed_read_is_true():
    assert (
        expect_checks_after_push(
            checks_seen_this_run=False, pre_push_evidence=-1, base_evidence=0
        )
        is True
    )
    assert (
        expect_checks_after_push(
            checks_seen_this_run=False, pre_push_evidence=0, base_evidence=-1
        )
        is True
    )


def test_expect_checks_after_push_none_is_true():
    assert (
        expect_checks_after_push(
            checks_seen_this_run=False, pre_push_evidence=None, base_evidence=0
        )
        is True
    )
    assert (
        expect_checks_after_push(
            checks_seen_this_run=False, pre_push_evidence=0, base_evidence=None
        )
        is True
    )


def test_expect_checks_after_push_base_evidence_two_is_true():
    assert (
        expect_checks_after_push(
            checks_seen_this_run=False, pre_push_evidence=0, base_evidence=2
        )
        is True
    )


def test_expect_checks_after_push_checks_seen_this_run_is_true():
    assert (
        expect_checks_after_push(
            checks_seen_this_run=True, pre_push_evidence=0, base_evidence=0
        )
        is True
    )


def test_expect_checks_after_push_non_int_evidence_fails_closed():
    for bad in ("0", 0.0, False, True):
        assert (
            expect_checks_after_push(
                checks_seen_this_run=False, pre_push_evidence=bad, base_evidence=0
            )
            is True
        )


# issue #361 (FR-25): the CI poll payload also carries ``merge_state``. These tests
# are regression guards: they pass on today's code because ``classify_checks`` never
# reads that key, and they fail if a later change makes it read it.

_CONFLICTING_STATE = {"mergeable": "CONFLICTING", "status": "DIRTY"}
_PASS_CHECK = {"name": "t", "bucket": "pass", "state": "COMPLETED"}
_PENDING_CHECK = {"name": "t", "bucket": "pending", "state": "PENDING"}
_FAIL_CHECK = {"name": "t", "bucket": "fail", "state": "COMPLETED"}

_PAYLOAD_SHAPES = {
    "pending": {"head_sha": _HEAD, "checks": [_PENDING_CHECK]},
    "all-pass": {"head_sha": _HEAD, "checks": [_PASS_CHECK]},
    "fail": {"head_sha": _HEAD, "checks": [_FAIL_CHECK]},
    "empty": {"head_sha": _HEAD, "checks": []},
    "empty-polling": {"head_sha": _HEAD, "state": "polling", "checks": []},
}
_CLASSIFY_KWARGS = {
    "default": {},
    "expect-checks-true": {"expect_checks": True},
    "expect-checks-false": {"expect_checks": False},
    "matching-wait-sha": {"wait_sha": _HEAD},
    "stale-head": {"wait_sha": "b" * 40},
}
_MERGE_STATES = [
    _CONFLICTING_STATE,
    {"mergeable": "MERGEABLE", "status": "CLEAN"},
    {"mergeable": "", "status": ""},
    "junk",
    None,
]


@pytest.mark.parametrize("merge_state", _MERGE_STATES)
@pytest.mark.parametrize("kwargs", _CLASSIFY_KWARGS.values(), ids=_CLASSIFY_KWARGS)
@pytest.mark.parametrize("payload", _PAYLOAD_SHAPES.values(), ids=_PAYLOAD_SHAPES)
def test_classify_ignores_the_merge_state_key(payload, kwargs, merge_state):
    """Regression guard (passes on today's code): ``merge_state`` never changes the
    classification of a payload."""
    assert classify_checks(
        {**payload, "merge_state": merge_state}, **kwargs
    ) == classify_checks(payload, **kwargs)


def test_classify_polling_with_no_checks_stays_polling_when_conflicting():
    """Regression guard (passes on today's code): the late trigger is not the
    classifier's job, so a conflicting wait with no checks stays ``polling``."""
    payload = {"state": "polling", "checks": [], "merge_state": _CONFLICTING_STATE}
    assert classify_checks(payload) == STATE_POLLING
    assert classify_checks(payload, expect_checks=True) == STATE_POLLING


def test_classify_merge_state_conflicting_does_not_turn_clean_checks_into_findings():
    """Regression guard (passes on today's code): clean checks stay clean."""
    payload = {
        "head_sha": _HEAD,
        "checks": [_PASS_CHECK],
        "merge_state": _CONFLICTING_STATE,
    }
    assert classify_checks(payload, wait_sha=_HEAD) == STATE_CLEAN
