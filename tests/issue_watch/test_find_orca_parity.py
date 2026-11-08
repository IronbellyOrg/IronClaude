"""Parity of ``launch.find_orca`` with ``install_user_setup._find_orca`` (C2, C19).

The original is driven by monkeypatching ``shutil.which`` and ``subprocess.run``
inside ``install_user_setup``; ``launch.find_orca`` is driven through a
``FakeRunner`` and a dict-based ``which``. Both see the same probe replies.

Where the original returns, both must return the same candidate. Where the
original raises (with exit 0, a probe reply whose ``topics`` is null, an int, a
bool, a non-empty str, a non-empty dict, or a list with a non-dict element before
any ``orca-cli`` dict), ``launch.find_orca`` is only required to reject without
raising (DF-36, C19). An empty str or dict has no elements, so the original
returns there and the two functions agree (``_SAME_RESULT``). The difference is
on purpose: the original reads ``topics`` outside its ``try`` at
``install_user_setup.py:219``, so it raises ``AttributeError`` or ``TypeError``
there, while ``launch.find_orca`` is meant to give None. A top-level JSON list (or any non-object top level) is not a
difference: the original's ``AttributeError`` from ``.get`` is caught inside its
``try`` at ``install_user_setup.py:216-217``, so it skips the candidate, and both
functions return the same result.
"""

from __future__ import annotations

import json
import types

import pytest

from superclaude.cli import install_user_setup as setup
from superclaude.cli.issue_watch import launch

from .conftest import FakeRunner, result

FIRST, SECOND = "orca-ide", "orca"
ORCA_TOPICS = json.dumps({"topics": [{"name": "orca-cli"}]})

# (reply stdout, exit code); the same reply goes to both implementations.
_SAME_RESULT: dict[str, tuple[str, int]] = {
    "orca_cli_topic": (ORCA_TOPICS, 0),
    "orca_cli_topic_after_others": (
        json.dumps({"topics": [{"name": "x"}, {"other": 1}, {"name": "orca-cli"}]}),
        0,
    ),
    "orca_cli_topic_extra_keys": (
        json.dumps({"version": 3, "topics": [{"name": "orca-cli", "n": 1}]}),
        0,
    ),
    "other_topic_only": (json.dumps({"topics": [{"name": "git"}]}), 0),
    "topics_without_name": (json.dumps({"topics": [{"title": "orca-cli"}]}), 0),
    "empty_topics_list": (json.dumps({"topics": []}), 0),
    "topics_absent": (json.dumps({}), 0),
    "topics_absent_other_keys": (json.dumps({"version": 1}), 0),
    "empty_topics_str": (json.dumps({"topics": ""}), 0),
    "empty_topics_dict": (json.dumps({"topics": {}}), 0),
    "orca_cli_topic_exit_1": (ORCA_TOPICS, 1),
    "null_topics_exit_1": (json.dumps({"topics": None}), 1),
    "non_dict_element_exit_2": (json.dumps({"topics": [1]}), 2),
    "top_level_list_empty": ("[]", 0),
    "top_level_list_of_orca_cli": (json.dumps([{"name": "orca-cli"}]), 0),
    "top_level_list_of_topics": (json.dumps([{"topics": [{"name": "orca-cli"}]}]), 0),
    "top_level_int": ("7", 0),
    "top_level_str": (json.dumps("orca-cli"), 0),
    "top_level_null": ("null", 0),
    "screen_reader_text": ("screen reader\n", 0),
    "empty_stdout": ("", 0),
    "truncated_json": ('{"topics": [{"name": "orca-', 0),
}

_FOUND = {"orca_cli_topic", "orca_cli_topic_after_others", "orca_cli_topic_extra_keys"}

# The original raises on each of these (exit 0 so that it reads ``topics``).
_ORIGINAL_RAISES: dict[str, str] = {
    "topics_null": json.dumps({"topics": None}),
    "topics_int": json.dumps({"topics": 5}),
    "topics_bool": json.dumps({"topics": True}),
    "topics_str": json.dumps({"topics": "orca-cli"}),
    "topics_dict": json.dumps({"topics": {"name": "orca-cli"}}),
    "element_int": json.dumps({"topics": [1]}),
    "element_str": json.dumps({"topics": ["orca-cli"]}),
    "element_null": json.dumps({"topics": [None]}),
    "element_list": json.dumps({"topics": [[{"name": "orca-cli"}]]}),
    "non_dict_before_orca_cli": json.dumps(
        {"topics": [1, {"name": "orca-cli"}]},
    ),
}


def _original(monkeypatch, replies: dict[str, tuple[str, int]]):
    """Run ``install_user_setup._find_orca`` with ``which`` and ``run`` faked.

    ``replies`` maps a candidate name to its ``(stdout, returncode)``; a name not
    in it is not found by ``which``. Returns ``(answer, which_names, run_calls)``
    and lets any exception of the original propagate.
    """
    which_names: list[str] = []
    run_calls: list[tuple[list[str], dict]] = []

    def fake_which(name: str) -> str | None:
        which_names.append(name)
        return f"/bin/{name}" if name in replies else None

    def fake_run(argv, *, capture_output, text, timeout, stdin):
        run_calls.append(
            (
                list(argv),
                {
                    "capture_output": capture_output,
                    "text": text,
                    "timeout": timeout,
                    "stdin": stdin,
                },
            )
        )
        stdout, code = replies[argv[0].rsplit("/", 1)[1]]
        return types.SimpleNamespace(stdout=stdout, returncode=code)

    monkeypatch.setattr(setup.shutil, "which", fake_which)
    monkeypatch.setattr(setup.subprocess, "run", fake_run)
    return setup._find_orca(), which_names, run_calls


def _launched(fake_runner, replies: dict[str, tuple[str, int]]):
    """Run ``launch.find_orca`` through a ``FakeRunner`` and a dict-based ``which``.

    Returns ``(answer, runner, which_names)``; the ``fake_runner`` fixture fails
    the test when an argv outside ``replies`` reaches the runner.
    """
    script = {
        (f"/bin/{name}", "skills", "list", "--json"): result(
            stdout=stdout, returncode=code
        )
        for name, (stdout, code) in replies.items()
    }
    runner: FakeRunner = fake_runner(script)
    which_names: list[str] = []
    paths = {name: f"/bin/{name}" for name in replies}

    def which(name: str) -> str | None:
        which_names.append(name)
        return paths.get(name)

    return launch.find_orca(runner, which=which), runner, which_names


@pytest.mark.parametrize("case", sorted(_SAME_RESULT))
def test_ac25_find_orca_same_answer_as_the_original__fr013_nfr014(
    case, monkeypatch, fake_runner
) -> None:
    """AC-25 FR-013 NFR-014: both give the same candidate where the original returns."""
    replies = {FIRST: _SAME_RESULT[case]}
    original, _, run_calls = _original(monkeypatch, replies)
    answer, runner, _ = _launched(fake_runner, replies)
    assert answer == original
    assert answer == (f"/bin/{FIRST}" if case in _FOUND else None)
    # One probe each, with the same argv and the same 10 s limit.
    assert [call[0] for call in run_calls] == [list(k) for k, _ in runner.calls]
    assert run_calls[0][1]["timeout"] == 10 == runner.timeouts[0]


@pytest.mark.parametrize("case", sorted(_SAME_RESULT))
def test_ac25_find_orca_same_answer_for_the_second_candidate__fr013_nfr014(
    case, monkeypatch, fake_runner
) -> None:
    """AC-25 FR-013 NFR-014: the second candidate is tried after a rejected first."""
    # The first candidate is a screen reader; the second gives the table reply.
    replies = {FIRST: ("screen reader\n", 0), SECOND: _SAME_RESULT[case]}
    original, which_names, _ = _original(monkeypatch, replies)
    answer, runner, launch_which = _launched(fake_runner, replies)
    assert answer == original
    assert launch_which == which_names
    assert len(runner.calls) == 2


@pytest.mark.parametrize("case", sorted(_ORIGINAL_RAISES))
def test_ac25_find_orca_rejects_where_the_original_raises__fr013_nfr014(
    case, monkeypatch, fake_runner
) -> None:
    """AC-25 FR-013 NFR-014 C19: the original raises; launch.find_orca returns None.

    This is the one pinned difference. The original reads ``topics`` outside its
    ``try`` (``install_user_setup.py:219``), so the two functions are compared only
    on "launch.find_orca rejects without raising", not on equal behaviour.
    """
    replies = {FIRST: (_ORIGINAL_RAISES[case], 0)}
    with pytest.raises((AttributeError, TypeError)):
        _original(monkeypatch, replies)
    answer, runner, _ = _launched(fake_runner, replies)
    assert answer is None
    assert len(runner.calls) == 1


@pytest.mark.parametrize("case", sorted(_ORIGINAL_RAISES))
def test_ac25_find_orca_moves_on_after_a_malformed_reply__fr013_nfr014(
    case, fake_runner
) -> None:
    """AC-25 FR-013 NFR-014 C19: a malformed first reply does not hide a good second."""
    replies = {FIRST: (_ORIGINAL_RAISES[case], 0), SECOND: (ORCA_TOPICS, 0)}
    answer, _, _ = _launched(fake_runner, replies)
    assert answer == f"/bin/{SECOND}"


@pytest.mark.parametrize(
    "shape", ["[]", json.dumps([{"name": "orca-cli"}]), "7", "null", '"x"']
)
def test_ac25_non_object_top_level_is_skipped_by_both__fr013_nfr014(
    shape, monkeypatch, fake_runner
) -> None:
    """AC-25 FR-013 NFR-014: a non-object top level is caught in the original's try.

    ``.get`` raises ``AttributeError`` inside ``install_user_setup.py:216-217``, so
    the original skips the candidate and goes on; both give the second candidate.
    """
    replies = {FIRST: (shape, 0), SECOND: (ORCA_TOPICS, 0)}
    original, _, run_calls = _original(monkeypatch, replies)
    answer, runner, _ = _launched(fake_runner, replies)
    assert original == answer == f"/bin/{SECOND}"
    assert len(run_calls) == len(runner.calls) == 2


def test_ac25_candidates_are_shared_and_ordered__fr013_nfr014(
    monkeypatch, fake_runner
) -> None:
    """AC-25 FR-013 NFR-014: one ``_ORCA_CLIS`` tuple, probed in the same order."""
    assert launch._ORCA_CLIS is setup._ORCA_CLIS
    assert tuple(launch._ORCA_CLIS) == (FIRST, SECOND)
    replies = {FIRST: ("[]", 0), SECOND: ("[]", 0)}
    original, which_names, run_calls = _original(monkeypatch, replies)
    answer, runner, launch_which = _launched(fake_runner, replies)
    assert original is answer is None
    assert which_names == launch_which == list(setup._ORCA_CLIS)
    probed = [f"/bin/{name}" for name in setup._ORCA_CLIS]
    assert [call[0][0] for call in run_calls] == probed
    assert [argv[0] for argv, _ in runner.calls] == probed
    assert all(cwd is None for _, cwd in runner.calls)


def test_ac25_first_candidate_wins_when_both_answer__fr013_nfr014(
    monkeypatch, fake_runner
) -> None:
    """AC-25 FR-013 NFR-014: the first candidate that answers is returned."""
    replies = {FIRST: (ORCA_TOPICS, 0), SECOND: (ORCA_TOPICS, 0)}
    original, _, run_calls = _original(monkeypatch, replies)
    answer, runner, _ = _launched(fake_runner, replies)
    assert original == answer == f"/bin/{FIRST}"
    assert len(run_calls) == len(runner.calls) == 1


def test_ac25_nothing_on_the_path_starts_no_process__fr013_nfr014(
    monkeypatch, fake_runner
) -> None:
    """AC-25 FR-013 NFR-014: no candidate found by ``which`` means no probe."""
    original, which_names, run_calls = _original(monkeypatch, {})
    answer, runner, launch_which = _launched(fake_runner, {})
    assert original is answer is None
    assert which_names == launch_which == list(setup._ORCA_CLIS)
    assert run_calls == [] and runner.calls == []


@pytest.mark.parametrize("stdout", ["screen reader\n", "Orca screen reader 46.0", ""])
def test_t17_screen_reader_stub_is_rejected_by_both__fr013_nfr014(
    stdout, monkeypatch, fake_runner
) -> None:
    """T17 FR-013 NFR-014: a stub answering non-JSON is not taken for Orca."""
    replies = {FIRST: (stdout, 0), SECOND: (stdout, 0)}
    original, _, run_calls = _original(monkeypatch, replies)
    answer, runner, _ = _launched(fake_runner, replies)
    assert original is None and answer is None
    assert len(run_calls) == len(runner.calls) == 2


def test_ac25_no_real_process_or_which_call_survives__nfr014(
    monkeypatch, fake_runner
) -> None:
    """AC-25 NFR-014: the patched seams, not ``shutil.which`` or ``subprocess.run``."""
    real_which, real_run = setup.shutil.which, setup.subprocess.run
    replies = {FIRST: (ORCA_TOPICS, 0)}
    _original(monkeypatch, replies)
    # Inside the monkeypatch both seams are the fakes, never the real functions.
    assert setup.shutil.which is not real_which
    assert setup.subprocess.run is not real_run
    # A path with no scripted reply makes the original fail loudly (KeyError).
    with pytest.raises(KeyError):
        monkeypatch.setattr(setup.shutil, "which", lambda name: "/bin/unscripted")
        setup._find_orca()
    # launch.find_orca with an empty script and a fake ``which`` that finds
    # nothing never reaches a runner or the real ``shutil.which``.
    runner = fake_runner({})
    assert launch.find_orca(runner, which=lambda _name: None) is None
    assert runner.calls == []
