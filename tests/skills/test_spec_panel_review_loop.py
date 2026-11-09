"""Static pins for the /sc:spec-panel ``## Review Loop`` section (document-review remediation).

Enforcement type: STATIC - assertions over the text of the two spec-panel
copies, the two routing-guide copies and the two release guides. They prove the
text is present and in the right order, not that a reviewer obeys it.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from tests.skills.test_review_severity_rule import AT_CAP_CLAUSES, CANONICAL_CAP_TEXT

_REPO = Path(__file__).resolve().parents[2]

SPEC_PANELS = (
    "src/superclaude/commands/spec-panel.md",
    "plugins/superclaude/commands/spec-panel.md",
)
HOW_WE_WORK = (
    "src/superclaude/core/HOW-WE-WORK.md",
    "plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md",
)
RELEASE_GUIDES = (
    "docs/guides/prd-skill-release-guide.md",
    "docs/guides/tdd-skill-release-guide.md",
)
HEADING = "## Review Loop"
BULLET_NAMES = (
    "Mode",
    "Grading",
    "Verdict",
    "Cap",
    "Re-review output",
    "Reviser contract",
    "Precedence",
)
OLD_SENTENCE = "until no critical findings remain"


def _flat(text: str) -> str:
    return " ".join(text.split())


def _lines(rel: str) -> list[str]:
    return (_REPO / rel).read_text(encoding="utf-8").splitlines()


def _section_lines(rel: str) -> list[str]:
    """Raw lines between the Review Loop heading and the next ``## `` heading."""
    lines = _lines(rel)
    start = lines.index(HEADING) + 1
    end = next(
        (i for i in range(start, len(lines)) if lines[i].startswith("## ")), len(lines)
    )
    return lines[start:end]


def _section(rel: str) -> str:
    return _flat("\n".join(_section_lines(rel)))


spec_panel = pytest.mark.parametrize("rel", SPEC_PANELS)


@spec_panel
def test_t1_usage_line_names_the_re_review_flags(rel):
    usage = next(line for line in _lines(rel) if line.startswith("/sc:spec-panel "))
    assert "[--re-review <prior-findings-file> --baseline <saved-copy>]" in _flat(usage)


@spec_panel
def test_t2_section_exists_once_before_output_formats(rel):
    lines = _lines(rel)
    assert lines.count(HEADING) == 1
    assert lines.index(HEADING) < lines.index("## Output Formats")


@spec_panel
def test_t3_seven_single_line_bullets_in_order(rel):
    body = [line for line in _section_lines(rel) if line.strip()]
    bullets = [line for line in body if re.match(r"^[1-7]\. \*\*", line)]
    assert body == bullets, (
        "every non-blank line of the section must be one of the seven bullets"
    )
    assert [re.match(r"^(\d)\. \*\*([^*]+)\*\*", b).groups() for b in bullets] == [
        (str(i), name) for i, name in enumerate(BULLET_NAMES, start=1)
    ]


CAP_LITERALS = (CANONICAL_CAP_TEXT, AT_CAP_CLAUSES[1])
VOCABULARY = (
    "resolved|open|regressed",
    "origin=changed|unchanged",
    "verdict: PASS",
    "verdict: FAIL",
    "review: N of 3",
    "Reviser brief",
    "byte size before and after",
)
LOOKUP_ORDER = (
    "the project `.claude/agents/rf-qa.md` first, else `~/.claude/agents/rf-qa.md`"
)
SPEC_REVIEW_FIXES = (
    "ignores `--iterations`",
    "`regressed` = a finding the prior report marked resolved that fails again",
    "never fall back to a first review",
)
PRECEDENCE = "A brief may narrow the checked scope but must retain applicable required assurance, prior findings and necessary dependencies"


@spec_panel
@pytest.mark.parametrize("literal", CAP_LITERALS, ids=["t4-cap-text", "t4-at-cap-halt"])
def test_t4_cap(rel, literal):
    assert literal in _section(rel)


@spec_panel
@pytest.mark.parametrize(
    "literal", VOCABULARY, ids=[f"t5-{i}" for i in range(len(VOCABULARY))]
)
def test_t5_vocabulary(rel, literal):
    assert literal in _section(rel)


@spec_panel
def test_t6_project_rf_qa_lookup_comes_first(rel):
    section = _section(rel)
    assert LOOKUP_ORDER in section
    assert section.index(".claude/agents/rf-qa.md") < section.index(
        "~/.claude/agents/rf-qa.md"
    )


@spec_panel
@pytest.mark.parametrize(
    "literal",
    SPEC_REVIEW_FIXES,
    ids=["t7-iterations", "t7-regressed", "t7-no-first-review"],
)
def test_t7_spec_review_fixes(rel, literal):
    assert literal in _section(rel)


@spec_panel
def test_t8_precedence_sentence(rel):
    assert PRECEDENCE in _section(rel)


@spec_panel
def test_t9_section_names_no_source_path(rel):
    # Scoped to the section: the whole file names one such path elsewhere and must not be asserted.
    assert "src/superclaude" not in _section(rel)


@pytest.mark.parametrize("rel", HOW_WE_WORK)
@pytest.mark.parametrize(
    "literal", ("--re-review", "--baseline", "save a copy of the PRD")
)
def test_t10_routing_guide_sentence_carries_the_new_flags(rel, literal):
    reporting = [line for line in _lines(rel) if "It only reports." in line]
    assert reporting, "routing guide lost the 'It only reports.' sentence"
    assert all(literal in _flat(line) for line in reporting)


@pytest.mark.parametrize("rel", HOW_WE_WORK + RELEASE_GUIDES)
def test_t10_old_sentence_is_gone(rel):
    assert OLD_SENTENCE not in _flat("\n".join(_lines(rel)))
