import pathlib
import socket

import pytest
import questions as q
from jevlib.questions import build_request, request_sha256

QUESTIONS_PY = pathlib.Path(q.__file__)

# Distinctive cue phrases of the keyword table (SKILL.md lines 153 to 158). Words that are type names or ordinary English
# (build, make, deploy, production, memory, leak, auth, token, exposed, null) are exempt on purpose.
CUE_PHRASES = [
    "stack trace", "nameerror", "undefined", "tsc", "compiled", "lint", "slow", "latency", "p99", "too long to load",
    "takes forever", "hangs", "container", "env var", "service won't start", "cve", "vulnerab", "pytest", "jest", "flake",
    "intermittent", "passing locally",
]


def test_request_builds_and_is_stable():
    req = build_request({"prompt": "x"}, q.build_questions())
    again = build_request({"prompt": "x"}, q.build_questions())
    assert request_sha256(req) == request_sha256(again)
    assert req["model"] == "jev-1.14.0"


def test_choice_has_exactly_the_six_types():
    qs = q.build_questions()
    assert qs["problem_type"]["type"] == "choice"
    assert list(qs["problem_type"]["criteria"]) == list(q.TYPES)
    assert q.TYPES == ("bug", "build", "performance", "deployment", "security", "test")
    assert all(text.strip() for text in qs["problem_type"]["criteria"].values())


def test_noul_has_true_and_false_criteria():
    qs = q.build_questions()
    assert qs["any_type_fits"]["type"] == "noul"
    assert set(qs["any_type_fits"]["criteria"]) == {"true", "false"}
    assert all(qs["any_type_fits"]["criteria"].values())


def test_only_two_questions_in_a_fixed_order():
    assert list(q.build_questions()) == ["problem_type", "any_type_fits"]


def test_questions_file_copies_none_of_the_tables_cue_phrases():
    text = QUESTIONS_PY.read_text(encoding="utf-8").lower()
    found = [c for c in CUE_PHRASES if c in text]
    assert found == []


def test_socket_guard_fails_a_connection_attempt():
    with pytest.raises(AssertionError):
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("127.0.0.1", 9))


def test_real_state_snapshot_reports_an_edit_of_an_existing_nested_file(tmp_path, snapshot_fn):
    run = tmp_path / "runs" / "r1"
    run.mkdir(parents=True)
    (run / "jev-rows.jsonl").write_text("a\n")
    before = snapshot_fn(tmp_path)
    (run / "jev-rows.jsonl").write_text("ab\n")          # edit an existing nested file
    assert snapshot_fn(tmp_path) != before
    before = snapshot_fn(tmp_path)
    (tmp_path / "events.jsonl").write_text("{}\n")        # create a top-level state file
    assert snapshot_fn(tmp_path) != before
