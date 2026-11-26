"""Policy checks for the "Worktrees and branches" section of the how-we-work guide.

The name checker lives only in this file. It is the machine-readable form of the
naming rule in the guide, and no production code uses it.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
_GUIDE = _REPO / "src/superclaude/core/HOW-WE-WORK.md"
_TWIN = _REPO / "plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md"
_DECK = _REPO / "docs/onboarding/ironclaude-onboarding.html"

# Same bound as `_NAME_NUMBER_RE` in scripts/worktree_cleanup.py: cleanup reads a
# standalone run of 2 to 4 digits in a branch name as an issue number.
_NUMBER_RUN = re.compile(r"(?<!\d)\d{2,4}(?!\d)")
_BRANCH_RE = re.compile(
    r"^[A-Za-z0-9]+(-[A-Za-z0-9]+)*/issue-[1-9][0-9]*(-[a-z0-9]+)*$"
)
_ISSUE_PART_RE = re.compile(r"issue-[1-9][0-9]*")
_MAX_LENGTH = 24


def branch_errors(branch: str) -> list[str]:
    """Reasons a branch name breaks the rule; an empty list means it is valid."""
    if not _BRANCH_RE.match(branch):
        return ["does not match <login>/issue-<N>[-<words>], no spaces"]
    login, rest = branch.split("/", 1)
    issue_part = _ISSUE_PART_RE.match(rest).group(0)
    words = rest[len(issue_part) :]
    errors = []
    bare = f"{login}/{issue_part}"
    if len(bare) > _MAX_LENGTH:
        errors.append(
            f"stop: even {bare} is over {_MAX_LENGTH} characters; "
            "create nothing and ask the owner"
        )
    elif len(branch) > _MAX_LENGTH:
        errors.append(f"{len(branch)} characters, at most {_MAX_LENGTH}")
    if _NUMBER_RUN.search(words):
        errors.append("the words hold a run of 2 to 4 digits that cleanup reads")
    return errors


def max_words_length(login: str, digits: int) -> int:
    """Characters left for the words once the login and the issue number are in."""
    return _MAX_LENGTH - len(login) - len("/issue-") - digits - len("-")


@pytest.mark.parametrize(
    "branch",
    [
        "clayphi/issue-289-wtrule",  # 24
        "clayphi/issue-834-clean",  # 23
        "ironbelly/issue-517-orca",  # 24
        "clayphi/issue-1234-docs",  # 23
        "clayphi/issue-289",  # 17
        "longloginname/issue-289",  # 23
        "Ab-c/issue-5",  # 12
        "a/issue-1-v12345",  # 16; a 5-digit run is not a 2 to 4 digit run
    ],
)
def test_checker_accepts(branch):
    assert branch_errors(branch) == []


@pytest.mark.parametrize(
    "branch",
    [
        "clayphi/issue-289-wtrules",  # 25 characters
        "clayphi/issue-289 wtrule",  # a space
        "clayphi/issue-0289",  # leading zero
        "clayphi/issue-",  # no issue number
        "clayphi/issue-289-",  # empty words
        "clayphi/issue-289-py312",  # a 3 digit run in the words
        "clayphi/issue-289-v2024",  # a 4 digit run in the words
        "a--b/issue-1",  # a double hyphen in the login
        "-a/issue-1",  # a login that starts with a hyphen
        "a/issue-1-x/y",  # a second slash
    ],
)
def test_checker_rejects(branch):
    assert branch_errors(branch)


def test_bare_form_over_the_limit_is_a_stop():
    errors = branch_errors("averylonglogin1/issue-289")  # 25 characters
    assert errors
    assert "stop" in " ".join(errors)


@pytest.mark.parametrize(
    ("login", "digits", "expected"),
    [
        ("clayphi", 3, 6),
        ("clayphi", 4, 5),
        ("longloginname", 3, 0),
        ("abcdefghijklmn", 3, -1),  # the bare form is exactly 24 characters
        ("abcdefghijklmno", 3, -2),  # the bare form is 25 characters
    ],
)
def test_budget_formula(login, digits, expected):
    assert max_words_length(login, digits) == expected
    assert expected == 16 - len(login) - digits
    bare = f"{login}/issue-{'1' * digits}"
    # The bare form overflows exactly when the login and the digits make 18.
    assert (len(bare) > _MAX_LENGTH) == (len(login) + digits >= 18)
    assert any("stop" in e for e in branch_errors(bare)) == (len(bare) > _MAX_LENGTH)
    if expected >= 1:
        assert branch_errors(f"{bare}-{'b' * expected}") == []
        assert branch_errors(f"{bare}-{'b' * (expected + 1)}")


_SECTION_HEADING = "## Worktrees and branches"
_ORCA_HEADING = "## Orca coordination"
_BANNED_PHRASES = [
    "Every verb is a dry run",
    "every verb is a dry run",
    "Verbs (a dry run unless --apply is given)",
]
# One exact phrase per rule of the section; each occurs once in it.
_KEY_PHRASES = [
    "new worktree and branch",
    "One writer per worktree",
    "original worktree while it still exists",
    "--ff-only",
    "stop and ask",
    "/sc:issue --claim",
    "at most 24 characters",
    "no spaces",
    "no run of 2 to 4 digits",
    "create nothing and ask the owner",
    "Lessons comment",
    "pins the worktree",
    "checks that comment first",
    "is exempt",
    "handoff of unfinished work",
]


def _section() -> str:
    """The guide from the section heading up to the next line that starts with `## `."""
    lines = _GUIDE.read_text(encoding="utf-8").splitlines()
    starts = [i for i, line in enumerate(lines) if line == _SECTION_HEADING]
    assert len(starts) == 1, (
        f"the guide needs exactly one {_SECTION_HEADING!r} line, found {len(starts)}"
    )
    end = next(
        (i for i in range(starts[0] + 1, len(lines)) if lines[i].startswith("## ")),
        len(lines),
    )
    return "\n".join(lines[starts[0] : end])


def _missing_phrases(section: str) -> list[str]:
    """The key phrases that a section text does not contain."""
    return [phrase for phrase in _KEY_PHRASES if phrase not in section]


def test_section_exists_once_before_orca_coordination():
    section = _section()  # fails unless the heading occurs exactly once
    lines = _GUIDE.read_text(encoding="utf-8").splitlines()
    assert lines.index(_SECTION_HEADING) < lines.index(_ORCA_HEADING)
    assert "<!--" not in section


def test_section_is_at_most_400_words():
    assert len(_section().split()) <= 400


def test_section_is_pure_ascii_and_has_no_banned_phrase():
    section = _section()
    assert section.isascii()
    assert [phrase for phrase in _BANNED_PHRASES if phrase in section] == []


@pytest.mark.parametrize("phrase", _KEY_PHRASES)
def test_section_states_each_rule(phrase):
    section = _section()
    assert phrase not in _missing_phrases(section)
    assert section.count(phrase) == 1


def test_every_backticked_branch_example_in_the_section_passes():
    examples = re.findall(r"`([^`<>]*/issue-[^`<>]*)`", _section())
    assert examples, "the section needs at least one backticked branch example"
    for example in examples:
        assert branch_errors(example) == [], example


@pytest.mark.parametrize("phrase", _KEY_PHRASES)
def test_deletion_is_detected(phrase):
    section = _section()
    assert _missing_phrases(section) == []
    assert _missing_phrases(section.replace(phrase, "")) == [phrase]


def test_mirror_is_byte_identical():
    assert _GUIDE.read_bytes() == _TWIN.read_bytes()


def test_pointer_names_the_section():
    rows = [
        line
        for line in _GUIDE.read_text(encoding="utf-8").splitlines()
        if line.startswith("| `/sc:worktrees` |")
    ]
    assert len(rows) == 1
    assert "Worktrees and branches" in rows[0]
    assert "item 4 of issue 289" not in rows[0]


def test_deck_card_is_replaced_and_neighbours_untouched():
    deck = _DECK.read_text(encoding="utf-8")
    assert "Worktree and branch protocol" in deck
    assert "clayphi/issue-289-wtrule" in deck
    assert "how they are named is being worked out" not in deck
    assert "issues/289" not in deck
    assert "Contributing rules" in deck
    assert re.search(r"Built from HOW-WE-WORK\.md at commit [0-9a-f]{7,40}\b", deck)
