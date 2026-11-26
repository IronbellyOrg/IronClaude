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
# The login is optional: a person whose login holds a run of 2 to 4 digits leaves it
# out and uses the form `issue-<N>[-<words>]`.
_BRANCH_RE = re.compile(
    r"^([A-Za-z0-9]+(-[A-Za-z0-9]+)*/)?issue-[1-9][0-9]*(-[a-z0-9]+)*$"
)
_ISSUE_PART_RE = re.compile(r"issue-[1-9][0-9]*")
_MAX_LENGTH = 24


def branch_errors(branch: str) -> list[str]:
    """Reasons a branch name breaks the rule; an empty list means it is valid."""
    if not _BRANCH_RE.match(branch):
        return ["does not match [<login>/]issue-<N>[-<words>], no spaces"]
    login, _, rest = branch.rpartition("/")  # login is "" when the name has none
    issue_part = _ISSUE_PART_RE.match(rest).group(0)
    words = rest[len(issue_part) :]
    errors = []
    if not login:
        if len(branch) > _MAX_LENGTH:
            errors.append(f"{len(branch)} characters, at most {_MAX_LENGTH}")
    elif words and len(branch) > _MAX_LENGTH:
        errors.append(
            f"{len(branch)} characters, at most {_MAX_LENGTH}: drop the words"
        )
    # A name with a login and no words is never an error for its length: when even
    # <login>/issue-<N> is over the limit the rule keeps it and goes on.
    if _NUMBER_RUN.search(words):
        errors.append("the words hold a run of 2 to 4 digits that cleanup reads")
    if login and _NUMBER_RUN.search(login):
        errors.append(
            "the login holds a run of 2 to 4 digits that cleanup reads as an issue: "
            "leave the login out and use issue-<N>-<words>"
        )
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
        "dev1/issue-289",  # 14; a 1-digit run in the login is not read by cleanup
        "issue-289-wtrule",  # 16; no login: a login with a digit run leaves it out
        "issue-289",  # 9
        "averylonglogin/issue-289",  # 24
        "abcdefghijklmno/issue-289",  # 25; the bare form over 24 is kept
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
        "dev42/issue-289",  # a 2 digit run in the login: cleanup also reads issue 42
        "dev42/issue-289-words",  # the same, with words
        "issue-289-py312",  # a 3 digit run in the words, no login
        "issue-0289",  # leading zero, no login
        "averylonglogin1/issue-289-x",  # 27; the words do not fit
        "issue-289-more-words-here",  # 25; no login, ordinary words over the limit
    ],
)
def test_checker_rejects(branch):
    assert branch_errors(branch)


def test_bare_form_over_the_limit_is_kept():
    for branch in ("averylonglogin1/issue-289", "abcdefghijklmno/issue-289"):
        assert len(branch) > _MAX_LENGTH  # 25 characters
        assert branch_errors(branch) == []  # never stop on it
    assert not any("stop" in e for e in branch_errors("averylonglogin1/issue-289-x"))


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
    assert branch_errors(bare) == []  # the bare form is always accepted
    if expected >= 1:
        assert branch_errors(f"{bare}-{'b' * expected}") == []
        assert branch_errors(f"{bare}-{'b' * (expected + 1)}")
    else:
        assert branch_errors(f"{bare}-b")  # no room for words: drop them


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
    "Lessons comment",
    "pins the worktree",
    "checks that comment first",
    "is exempt",
    "handoff of unfinished work",
    "at its default location",
    "Supervised workers follow",
    "same repository, issue and branch",
    "no other live agent",
    "no uncommitted changes",
    "the PR that counts",
    "the watcher claims by itself",
    "after the first session has stopped",
    "Neither refuses an issue that already has a worktree",
    "iteration start check asks the owner first",
    "skips only the already-claimed check",
    "match on repository, issue and branch",
    "drop them and keep",
    "never stop on it",
    "is left out: use",
    "keeps the launcher's",
    "own `.dev/` notes",
    "issue 881",
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


def test_section_is_within_the_word_cap():
    assert len(_section().split()) <= 500


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


_S12_INTRO = (
    "<p>Both rules are settled. The worktree rule is the left card and the guide "
    'section "Worktrees and branches"; the contributing rule is the right card, '
    "with its history in issue #290. If a case is not covered, ask your lead.</p>"
)


def test_deck_card_is_replaced_and_neighbours_untouched():
    deck = _DECK.read_text(encoding="utf-8")
    assert "Contributing and worktrees" in deck
    assert "Worktree and branch protocol" in deck
    assert "clayphi/issue-289-wtrule" in deck
    for old in (
        "Contributing, and one open topic",
        "still open in its own issue",
        "issues #289 and #290",
        "how they are named is being worked out",
        "issues/289",
    ):
        assert old not in deck, old
    assert _S12_INTRO in deck
    # No call that the worktree topic is open anywhere on slide 12.
    slide_12 = deck[deck.index('id="s12"') : deck.index('id="s13"')]
    assert "still open" not in slide_12
    assert "Contributing rules" in deck
    assert re.search(r"Built from HOW-WE-WORK\.md at commit [0-9a-f]{7,40}\b", deck)
