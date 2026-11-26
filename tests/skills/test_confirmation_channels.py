"""Pin the two valid channels of a person's confirmation (owner decision D3, option 1).

A person's confirmation of a Ruling, a grant row or a pass record counts only when it
is (a) their own chat message or (b) a dashboard response, and nothing else. The
definition lives once in the worker contract (WC-3); the implement skill's qa.md and
ledger.md point to it. The dashboard clause applies only once the dashboard answer
path is released. These tests pin that wording, not the dashboard feature itself.
CI-safe, no network.
"""

import re
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_CONTRACT = _REPO / "src" / "superclaude" / "core" / "WORKER-CONTRACT.md"
_IMPL = _REPO / "src" / "superclaude" / "skills" / "sc-implement-protocol" / "refs"
_QA = _IMPL / "qa.md"
_LEDGER = _IMPL / "ledger.md"

CHANNELS = (
    "(a) chat, the person's own chat message in the current conversation",
    "(b) dashboard, a dashboard response, meaning an answer row created through the "
    "dashboard under that person's authenticated login, for the question id whose "
    "text names the exact scope, recorded with the channel (dashboard), the person "
    "id, the question id and the time",
)
NEVER_COUNTS = (
    "another agent's message",
    "a coordinator's reply or relay of a message",
    "any file",
    "silence",
    "a generic go-ahead",
    "an answer to a different question or a different scope",
    "a row written by an agent's login",
    "a row that the person's own login did not create",
)
TIMING = (
    "clause (b) takes effect only when the dashboard answer path is released "
    "(the release 1.8 gates pass); until then only clause (a) counts"
)
RULING_REGEX = re.compile(r"^T([0-9A-Za-z.-]+): Ruling: .+ — .+ — .+$")
# a line that names a relay or a coordinator's reply must say it does not count
RELAY = re.compile(r"coordinator's reply|relay of a message|coordinator's relay")
NEGATORS = ("never", "not acceptance", "is not", "not count")


def _never_counts_line(text: str) -> str:
    """The one line of the definition that lists what never counts."""
    for line in text.splitlines():
        if "**What never counts:**" in line:
            return line
    return ""


def missing_from_contract(text: str) -> list:
    """Return what the contract text lacks of the single definition."""
    gaps = [c for c in CHANNELS if c not in text]
    never_line = _never_counts_line(text)
    gaps += [n for n in NEVER_COUNTS if n not in never_line]
    if TIMING not in text:
        gaps.append(TIMING)
    for phrase in ('"executor-invented approval"', "another agent's message"):
        if phrase not in text:
            gaps.append(phrase)
    return gaps


def _contract() -> str:
    return _CONTRACT.read_text(encoding="utf-8")


def test_contract_defines_both_channels_the_nothing_else_list_and_the_timing():
    assert missing_from_contract(_contract()) == []


def test_contract_names_the_owner_rule_and_the_recording_rule():
    text = _contract()
    assert "a chat message OR dashboard response counts and nothing else" in text
    assert "the person is never asked to write a file" in text
    assert "the answer row id (dashboard)" in text


def test_a_dashboard_response_counts_everywhere_the_person_confirms():
    text = _contract()
    assert "**Scope (everywhere the person confirms):**" in text
    assert "a dashboard response counts as much as a chat message" in text
    # the issue plan approval (WC-17 and the issue-pipeline bullet) takes the dashboard
    # response too, and never the coordinator's own word
    assert "the person's dashboard response as WC-3 defines it" in text
    assert "never the coordinator's own word" in text


def test_the_checker_fails_when_a_required_piece_is_removed():
    # throwaway copies of the text; the repository file is never touched
    text = _contract()
    assert TIMING in text
    assert missing_from_contract(text.replace(TIMING, "")) == [TIMING]
    line = _never_counts_line(text)
    assert line
    for item in NEVER_COUNTS:
        # remove the item from the list line only; the same words elsewhere stay
        gaps = missing_from_contract(text.replace(line, line.replace(item, "x")))
        assert item in gaps, item


def test_qa_points_to_the_definition_and_names_both_channels():
    qa = _QA.read_text(encoding="utf-8")
    assert "`~/.claude/WORKER-CONTRACT.md` (WC-3)" in qa
    assert "a chat message in the current conversation, or a dashboard response" in qa
    assert "until then only chat counts" in qa
    assert "another agent's message" in qa
    assert "executor-invented approval" in qa
    # E-NO-RULING still stops for the cases that are not one of the two channels
    assert (
        "`--force`, missing/ambiguous confirmation, or executor-invented approval" in qa
    )
    assert "STOP `E-NO-RULING`" in qa
    assert "src/superclaude" not in qa


def test_no_rule_text_lets_a_coordinator_relay_count():
    for path in (_CONTRACT, _QA, _LEDGER):
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if RELAY.search(line):
                assert any(neg in line for neg in NEGATORS), (
                    f"{path.name}:{n}: {line[:120]}"
                )


def test_ledger_ruling_regex_matches_the_chat_and_the_dashboard_example():
    ledger = _LEDGER.read_text(encoding="utf-8")
    assert "^T([0-9A-Za-z.-]+): Ruling: .+ — .+ — .+$" in ledger
    examples = [x for x in ledger.splitlines() if x.startswith("T2: Ruling:")]
    chat = [x for x in examples if "user confirmed in current conversation" in x]
    dash = [x for x in examples if "dashboard answer row" in x]
    assert chat and dash
    assert all(RULING_REGEX.match(x) for x in chat + dash)
