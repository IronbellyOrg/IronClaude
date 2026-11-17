"""Safety scan module: vocabulary, row handling and the raise-only outcome rule."""

from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest

from superclaude.cli.review import safety_route as route

SOURCE = Path(route.__file__)


@pytest.mark.parametrize("word", route.VOCABULARY)
def test_each_vocabulary_word_hits(word):
    result = route.scan_text(f"the recipe will {word} the target\n")
    assert [h.word.lower() for h in result.hits] == [word]
    assert result.rows_read == 1


@pytest.mark.parametrize(
    "row,hit",
    [
        ("Files were DELETED by the step", True),
        ("two tokens leak", True),
        ("a Secret value", True),
        ("we reinforce the wall", False),  # "force" inside a word does not hit
        ("untokenized input", False),
        ("nothing risky here", False),
    ],
)
def test_case_and_word_start_rule(row, hit):
    assert bool(route.scan_text(row).hits) is hit


def test_vocabulary_is_one_list_with_the_gr1_words():
    for word in (
        "delete",
        "overwrite",
        "force",
        "token",
        "secret",
        "password",
        "chmod",
    ):
        assert word in route.VOCABULARY
    assert len(set(route.VOCABULARY)) == len(route.VOCABULARY)


def test_superseded_row_is_skipped_and_counted_never_scanned():
    text = "superseded this row says delete everything\nlive row says delete\n\n"
    result = route.scan_text(text)
    assert result.rows_skipped == 1
    assert result.rows_read == 1
    assert [h.line for h in result.hits] == [2]


def test_blank_lines_are_not_rows_and_hits_carry_line_numbers():
    result = route.scan_text("\n\nfirst\n\nsecond has a password\n")
    assert result.rows_read == 2
    assert result.hits[0].line == 5
    assert result.hits[0].row == "second has a password"


def test_empty_input_is_flagged_empty():
    assert route.scan_text("").empty
    assert route.scan_text("  \n\n").empty
    assert not route.scan_text("x\n").empty


@pytest.mark.parametrize("graded", route.OUTCOMES)
def test_outcome_is_never_lowered(graded):
    for has_hit in (True, False):
        out = route.raise_outcome(graded, has_hit)
        assert route.OUTCOMES.index(out) >= route.OUTCOMES.index(graded)


def test_hit_promotes_note_and_medium_to_blocking_and_no_hit_keeps_outcome():
    assert route.raise_outcome("Note", True) == "Blocking"
    assert route.raise_outcome("Medium", True) == "Blocking"
    assert route.raise_outcome("Blocking", True) == "Blocking"
    for graded in route.OUTCOMES:
        assert route.raise_outcome(graded, False) == graded


def test_outcome_order_is_defined_once_and_unknown_outcome_is_rejected():
    assert route.OUTCOMES == ("Note", "Medium", "Blocking")
    with pytest.raises(ValueError):
        route.raise_outcome("Minor", True)


def test_unreadable_input_is_its_own_result_not_zero_hits(tmp_path):
    missing = route.scan_file(tmp_path / "nope.md")
    folder = route.scan_file(tmp_path)
    bad = tmp_path / "bad.md"
    bad.write_bytes(b"\xff\xfe\x00 not utf-8 \x80")
    binary = route.scan_file(bad)
    for result, reason in (
        (missing, "no such file"),
        (folder, "is a directory"),
        (binary, "not valid UTF-8"),
    ):
        assert isinstance(result, route.Unreadable)
        assert result.reason == reason
    ok = tmp_path / "ok.md"
    ok.write_text("clean row\n", encoding="utf-8")
    result = route.scan_file(ok)
    assert isinstance(result, route.ScanResult)
    assert result.hits == ()


def test_module_imports_no_unrelated_reader_and_makes_no_call_out():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    imported = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            imported.append(node.module or "")
    banned = re.compile(
        r"classif|codec|ledger|follow_up|subprocess|requests|httpx|socket", re.I
    )
    assert not [name for name in imported if banned.search(name)], imported
