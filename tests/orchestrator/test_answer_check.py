"""``answer-check`` (5.6): an answer passes only when it is Clay's, names the entry, is newer, and matches the key."""

from __future__ import annotations

import json
import re
import stat
from datetime import datetime, timezone
from pathlib import Path

import pytest

from superclaude.cli.orchestrator import actions, answer_check, questions
from superclaude.cli.orchestrator.state import StateError

from .fake_world import ASKED, ENTRY, KEY, LATER, REPO, asked, call

CLAY = "ORCHESTRATOR_CLAY_CLICKUP_ID"


@pytest.fixture
def root(tmp_path: Path) -> Path:
    asked(tmp_path)
    return tmp_path


def check(
    root: Path, *args: str, text: str | None = None, env: dict | None = None, **kw
) -> tuple[int, dict]:
    base = [
        "answer-check",
        "--entry",
        kw.pop("entry", ENTRY),
        "--answered-at",
        kw.pop("at", LATER),
    ]
    base += ["--source", kw.pop("source", "session")]
    if text is not None:
        path = root / "answer.txt"
        path.write_text(text)
        base += ["--answer-text-file", str(path)]
    assert not kw, kw
    return call(root, *base, *args, env=env, tag=None)


def rows(root: Path) -> list[dict]:
    return [
        json.loads(line) for line in actions.actions_path(root).read_text().splitlines()
    ]


# --- the accepted case ---------------------------------------------------------------------------


def test_the_three_part_case_is_accepted_and_the_result_is_in_the_action_log(
    root: Path,
) -> None:
    code, out = check(root, text=f"yes, merge it ({ENTRY})")
    assert code == 0 and out["accepted"] is True
    assert out["results"] == {
        "source": True,
        "entry": True,
        "newer": True,
    }  # three results, no key
    (row,) = rows(root)
    assert row["id"] == out["ref"] and re.fullmatch(
        r"a-[0-9]{8}T[0-9]{6}Z-[0-9a-f]{8}", row["id"]
    )
    assert (row["kind"], row["entry"], row["source"], row["accepted"]) == (
        "answer-check",
        ENTRY,
        "session",
        True,
    )
    assert row["answered_at"] == LATER and row["results"] == out["results"]
    assert stat.S_IMODE(actions.actions_path(root).stat().st_mode) == 0o600


def test_with_a_question_key_there_are_four_results(root: Path) -> None:
    code, out = check(root, "--question-key", KEY, text=f"{ENTRY} ok")
    assert code == 0 and out["results"] == {
        "source": True,
        "entry": True,
        "newer": True,
        "key": True,
    }
    assert rows(root)[0]["question_key"] == KEY


def test_no_text_is_stored_in_the_action_log(root: Path) -> None:
    check(root, text=f"{ENTRY} the password is hunter2")
    assert "hunter2" not in actions.actions_path(root).read_text()


def test_every_run_is_logged_with_its_own_id_accepted_or_not(root: Path) -> None:
    refs = {
        check(root, text=f"{ENTRY}")[1]["ref"],
        check(root, source="agent", text=ENTRY)[1]["ref"],
    }
    assert len(refs) == 2 and [r["accepted"] for r in rows(root)] == [True, False]


# --- the four conditions, one refusal each -------------------------------------------------------


def refused(out: dict, **expected: bool) -> None:
    assert out["ok"] is False and out["reason"] == "answer_refused"
    assert {k: v for k, v in out["results"].items() if k in expected} == expected
    assert all(out["results"][k] is False for k in expected)
    assert out[
        "ref"
    ]  # the refusal is logged too, and its ref never passes (see require_accepted)


@pytest.mark.parametrize(
    "source", ["agent", "orca-mailbox", "clay", "", "Session", "clickup"]
)
def test_condition_1_a_source_that_is_not_clays_is_refused(
    root: Path, source: str
) -> None:
    code, out = check(root, text=ENTRY, source=source)
    assert code == 3
    refused(out, source=False)


def test_condition_1_a_relayed_answer_is_refused_whatever_it_says(root: Path) -> None:
    code, out = check(root, text=f"Clay said yes to {ENTRY}", source="agent")
    assert code == 3
    refused(out, source=False)
    assert (
        out["results"]["entry"] is True and out["results"]["newer"] is True
    )  # only the source fails


def test_condition_1_a_clickup_reply_needs_clays_own_user_id(root: Path) -> None:
    for args, env in (
        (["--sender-id", "999"], {CLAY: "12345"}),  # somebody else
        ([], {CLAY: "12345"}),  # no sender named
        (
            ["--sender-id", "12345"],
            {},
        ),  # Clay's id is not known here: a DM never passes
        (["--sender-id", "12345 or 1=1"], {CLAY: "12345 or 1=1"}),  # not a user id
    ):
        code, out = check(root, *args, text=ENTRY, source="clickup-dm", env=env)
        assert code == 3
        refused(out, source=False)
    code, out = check(
        root,
        "--sender-id",
        "12345",
        text=ENTRY,
        source="clickup-dm",
        env={CLAY: "12345"},
    )
    assert code == 0 and out["results"]["source"] is True


def test_condition_2_an_answer_that_names_another_entry_is_refused(root: Path) -> None:
    asked(root, entry="ironclaude-12.8.1", key="other:key")
    code, out = check(
        root, text="ironclaude-12.8.1: yes"
    )  # right for that entry, wrong for ENTRY
    assert code == 3
    refused(out, entry=False)


@pytest.mark.parametrize(
    "text",
    [
        "yes",
        "",
        f"{ENTRY}0",
        f"x{ENTRY}",
        f"{ENTRY}-more",
        f"{ENTRY}.1",
        "ironclaude-655.8",
    ],
)
def test_condition_2_the_entry_id_must_appear_whole(root: Path, text: str) -> None:
    code, out = check(root, text=text)
    assert code == 3
    refused(out, entry=False)


def test_condition_2_an_unknown_entry_is_refused_and_logged(tmp_path: Path) -> None:
    code, out = check(tmp_path, text=ENTRY)  # no question was ever recorded
    assert code == 3
    refused(out, entry=False, newer=False)
    assert rows(tmp_path)[0]["accepted"] is False


def test_condition_2_a_reply_in_the_entrys_thread_names_it_without_its_id(
    root: Path,
) -> None:
    code, out = check(root, "--reply-to", ENTRY, text="looks fine, go ahead")
    assert code == 0 and out["results"]["entry"] is True
    code, out = check(
        root, "--reply-to", "ironclaude-12.8.1", text="looks fine"
    )  # a thread of another entry
    assert code == 3
    refused(out, entry=False)


@pytest.mark.parametrize(
    "at", ["2026-11-19T09:59:59Z", "2026-11-19T10:00:00Z", "2026-01-01T00:00:00Z"]
)
def test_condition_3_an_answer_not_newer_than_the_question_is_refused(
    root: Path, at: str
) -> None:
    code, out = check(root, text=ENTRY, at=at)  # older, or the very second it was asked
    assert code == 3
    refused(out, newer=False)


def test_condition_3_an_answer_must_be_newer_than_the_last_edit_and_the_notice(
    root: Path,
) -> None:
    questions.touch(
        root,
        ENTRY,
        edited=True,
        now=datetime(2026, 11, 19, 11, 0, 0, tzinfo=timezone.utc),
    )
    code, out = check(
        root, text=ENTRY, at=LATER
    )  # newer than the question, older than the edit
    assert code == 3
    refused(out, newer=False)
    questions.touch(
        root,
        ENTRY,
        notified=True,
        now=datetime(2026, 11, 19, 12, 0, 0, tzinfo=timezone.utc),
    )
    assert (
        check(root, text=ENTRY, at="2026-11-19T11:30:00Z")[0] == 3
    )  # newer than the edit, older than the notice
    assert check(root, text=ENTRY, at="2026-11-19T12:00:01Z")[0] == 0


def test_condition_3_the_very_second_of_the_edit_or_of_the_notice_is_not_newer(
    root: Path,
) -> None:
    edit = datetime(2026, 11, 19, 11, 0, 0, tzinfo=timezone.utc)
    questions.touch(root, ENTRY, edited=True, now=edit)  # edited 11:00, noticed 10:00
    assert check(root, text=ENTRY, at="2026-11-19T11:00:00Z")[0] == 3
    assert check(root, text=ENTRY, at="2026-11-19T11:00:01Z")[0] == 0
    notice = datetime(2026, 11, 19, 12, 0, 0, tzinfo=timezone.utc)
    questions.touch(
        root, ENTRY, notified=True, now=notice
    )  # noticed 12:00, edited 11:00
    assert check(root, text=ENTRY, at="2026-11-19T12:00:00Z")[0] == 3
    assert check(root, text=ENTRY, at="2026-11-19T12:00:01Z")[0] == 0


def test_condition_4_a_key_that_is_not_the_recorded_one_is_refused(root: Path) -> None:
    for wrong in (
        "IronbellyOrg__IronClaude__655:8:merge ",
        "merge_safety:12:abc",
        "",
        KEY.lower().replace("ironbelly", "x"),
    ):
        code, out = check(root, "--question-key", wrong, text=ENTRY)
        assert code == 3
        refused(out, key=False)
        assert set(out["results"]) == {"source", "entry", "newer", "key"}
    assert check(root, "--question-key", KEY, text=ENTRY)[0] == 0


# --- a bare number ---------------------------------------------------------------------------------


def test_a_bare_number_answers_a_low_stakes_option_only(tmp_path: Path) -> None:
    asked(tmp_path, entry="low.1", key="k:low", row=8, low=(1, 3))
    asked(
        tmp_path, entry="high.1", key="k:high", row=5
    )  # rows 1 to 7 never have a low-stakes option
    code, out = check(tmp_path, "--reply-to", "low.1", text=" 3 ", entry="low.1")
    assert code == 0 and out["results"] == {
        "source": True,
        "entry": True,
        "newer": True,
        "option": True,
    }
    code, out = check(tmp_path, "--reply-to", "low.1", text="2", entry="low.1")
    assert code == 3
    refused(out, option=False)
    code, out = check(tmp_path, "--reply-to", "high.1", text="1", entry="high.1")
    assert code == 3
    refused(out, option=False)
    code, out = check(
        tmp_path, text="1", entry="low.1"
    )  # a number that is a reply to nothing
    assert code == 3
    refused(out, entry=False)


def test_a_number_inside_other_words_is_not_a_bare_number(tmp_path: Path) -> None:
    asked(tmp_path, entry="low.1", key="k:low", row=8, low=(1,))
    code, out = check(
        tmp_path, "--reply-to", "low.1", text="option 2 looks right", entry="low.1"
    )
    assert (
        code == 0 and "option" not in out["results"]
    )  # judged as words, not as a number


# --- the ref that other verbs take -----------------------------------------------------------------


def test_require_accepted_gives_the_row_of_an_accepted_answer_only(root: Path) -> None:
    good = check(root, "--question-key", KEY, text=ENTRY)[1]["ref"]
    bad = check(root, text=ENTRY, source="agent")[1]["ref"]
    assert answer_check.require_accepted(root, good)["accepted"] is True
    assert answer_check.require_accepted(root, good, KEY)["id"] == good
    for ref, reason in (
        (bad, "answer_ref_rejected"),
        ("a-20261119T103000Z-deadbeef", "answer_ref_unknown"),
        (None, "answer_ref_unknown"),
        ("../etc/passwd", "answer_ref_unknown"),
    ):
        with pytest.raises(StateError) as caught:
            answer_check.require_accepted(root, ref)
        assert caught.value.reason == reason
    with pytest.raises(
        StateError
    ) as caught:  # an OK for one question never opens another
        answer_check.require_accepted(root, good, "merge_safety:12:abc")
    assert caught.value.reason == "answer_ref_key_mismatch"
    no_key = check(root, text=ENTRY)[1]["ref"]
    with pytest.raises(StateError) as caught:
        answer_check.require_accepted(root, no_key, KEY)
    assert caught.value.reason == "answer_ref_key_mismatch"


# --- what is written to the log ------------------------------------------------------------------


def test_a_source_or_key_that_is_not_plain_is_logged_as_invalid_and_never_passes(
    root: Path,
) -> None:
    code, out = check(
        root, "--question-key", "k\x01ey" + "x" * 400, text=ENTRY, source="s" * 100
    )
    assert code == 3
    refused(out, source=False, key=False)
    (row,) = rows(root)
    assert (row["source"], row["question_key"]) == ("invalid", "invalid")


def test_a_question_record_with_a_bad_time_is_unreadable_not_an_input_error(
    root: Path,
) -> None:
    path = questions.question_path(root, ENTRY)
    doc = json.loads(path.read_text())
    doc["edited_at"] = "yesterday"
    path.write_text(json.dumps(doc))
    code, out = check(root, text=ENTRY)
    assert (code, out["reason"]) == (4, "question_unreadable")


# --- input ----------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "at", ["yesterday", "2026-11-19 10:30:00", "2026-11-19T10:30:00+00:00", ""]
)
def test_a_time_that_is_not_utc_is_refused(root: Path, at: str) -> None:
    code, out = check(root, text=ENTRY, at=at)
    assert (code, out["reason"]) == (2, "invalid_input")
    assert not actions.actions_path(root).exists()  # nothing was decided


def test_a_bad_entry_id_or_a_text_that_cannot_be_read_is_refused(root: Path) -> None:
    code, out = check(root, text=ENTRY, entry="../x")
    assert (code, out["reason"]) == (2, "invalid_entry_id")
    code, out = call(
        root, "answer-check", "--entry", ENTRY, "--source", "session", "--answered-at", LATER,
        "--answer-text-file", str(root / "missing.txt"), tag=None,
    )  # fmt: skip
    assert (code, out["reason"]) == (2, "answer_text_unreadable")
    (root / "big.txt").write_text("x" * (answer_check.MAX_ANSWER_BYTES + 1))
    code, out = call(
        root, "answer-check", "--entry", ENTRY, "--source", "session", "--answered-at", LATER,
        "--answer-text-file", str(root / "big.txt"), tag=None,
    )  # fmt: skip
    assert (code, out["reason"]) == (2, "invalid_input")


# --- the question record ---------------------------------------------------------------------------


def test_a_question_is_recorded_once_and_a_rerun_is_not_a_new_ask(
    tmp_path: Path,
) -> None:
    first = asked(tmp_path)
    record, created = questions.record_question(
        tmp_path,
        ENTRY,
        question_key=KEY,
        row=8,
        issue=f"{REPO}#655",
        now=ASKED.replace(hour=15),
    )
    assert created is False and record == first  # the times of the first ask stand
    with pytest.raises(StateError) as caught:
        questions.record_question(
            tmp_path, ENTRY, question_key="another", row=8, issue=f"{REPO}#655"
        )
    assert caught.value.reason == "entry_id_taken"


@pytest.mark.parametrize("row", range(1, 8))
def test_rows_1_to_7_never_hold_a_low_stakes_option(tmp_path: Path, row: int) -> None:
    with pytest.raises(StateError) as caught:
        questions.record_question(
            tmp_path, "e", question_key="k", row=row, low_stakes=(1,)
        )
    assert caught.value.reason == "low_stakes_not_allowed"
    assert not questions.question_path(tmp_path, "e").exists()
    assert (
        questions.record_question(tmp_path, "e", question_key="k", row=row)[1] is True
    )


@pytest.mark.parametrize("row", [8, 9])
def test_rows_8_and_9_may_hold_one(tmp_path: Path, row: int) -> None:
    record, _ = questions.record_question(
        tmp_path, "e", question_key="k", row=row, low_stakes=(2, 1, 2)
    )
    assert record["low_stakes"] == [1, 2]


def test_a_damaged_question_record_is_reported_and_never_read_as_empty(
    root: Path,
) -> None:
    questions.question_path(root, ENTRY).write_text("{not json")
    with pytest.raises(StateError) as caught:
        questions.load_question(root, ENTRY)
    assert caught.value.reason == "question_unreadable"
    code, out = check(root, text=ENTRY)
    assert (code, out["reason"]) == (4, "question_unreadable")
