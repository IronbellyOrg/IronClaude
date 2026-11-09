"""Placement pins for the coordinator review/revise prompts (#346, P7 refactor 2: in-context mirror guarded by a drift test).

The rules file is the source of truth. Its CORE block (roles table, evidence block, review-number rule, self-check) is
mirrored byte for byte into both copies of spec-panel.md between the same markers, and a drift test fails when they differ.
Static text assertions only.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
SPEC_PANELS = (
    "src/superclaude/commands/spec-panel.md",
    "plugins/superclaude/commands/spec-panel.md",
)
GUIDES = (
    "src/superclaude/core/HOW-WE-WORK.md",
    "plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md",
)
RULES_REL = "src/superclaude/rules/prompts/document_review_loop_prompts.md"
REF = "~/.claude/rules/prompts/document_review_loop_prompts.md"
START, END = "<!-- core:start -->", "<!-- core:end -->"
LABELS = ("First-review brief", "Re-review brief", "Revise brief")
spec_panel = pytest.mark.parametrize("rel", SPEC_PANELS)


def _text(rel: str) -> str:
    return (_REPO / rel).read_text(encoding="utf-8")


def _core(rel: str) -> str:
    text = _text(rel)
    assert text.count(START) == 1 and text.count(END) == 1, rel
    a, b = text.index(START), text.index(END) + len(END)
    assert a < b, rel
    return text[a:b]


def test_rules_file_has_one_core_block_with_all_four_parts():
    core = _core(RULES_REL)
    for token in (
        "| ROLE | FILE VALUE | MEANING |",
        "| CANDIDATE | the `@file` of the command | the revised text under review |",
        "| BASELINE | the `--baseline` file | the text as it was before the revision |",
        "| PRIOR | the `--re-review` file | the previous review report |",
        "never infer a role from reading order or from memory",
        "Step 1, the evidence block",
        "`diff -w BASELINE CANDIDATE`",
        "`BEFORE (baseline)`",
        "`AFTER (candidate)`",
        "If the diff is empty, every prior blocking finding stays open",
        "N is the number in PRIOR's `review: N of 3` header plus 1",
        "Example: a prior `review: 2 of 3` gives `review: 3 of 3`",
        "Use no other header variant",
        "`grep -nF`",
        "you swapped roles: redo Step 1",
    ):
        assert token in core, token


def test_rules_file_holds_the_prompts_with_descriptive_names():
    text = _text(RULES_REL)
    for label in LABELS:
        assert f'- {label}: "' in text, label
    for token in (
        "FIRST-REVIEW prompt",
        "RE-REVIEW prompt",
        "REVISE prompt",
        "## Never",
    ):
        assert token in text, token
    for ph in ("{{CANDIDATE}}", "{{BASELINE}}", "{{PRIOR}}", "{{N}}", "{{IDS}}"):
        assert ph in text, ph
    assert "src/superclaude" not in text
    assert not re.search(r"Prompt (R\d|V\d)", text), "old prompt names must be gone"


@spec_panel
def test_command_mirror_is_byte_identical_to_the_rules_file_core(rel):
    """Drift test: editing either side without the other fails here."""
    assert _core(rel) == _core(RULES_REL), rel


@spec_panel
def test_markers_occur_exactly_once_in_each_file(rel):
    for path in (rel, RULES_REL):
        text = _text(path)
        assert text.count(START) == 1, (path, START)
        assert text.count(END) == 1, (path, END)


@spec_panel
def test_hard_gate_sends_the_reviewer_to_the_file_and_makes_the_core_win(rel):
    text = _text(rel)
    head = "\n## Review-loop prompts (hard gate)\n\n"
    assert head in text, rel
    gate = text.split(head, 1)[1].split(START, 1)[0]
    assert f"read `{REF}` in full" in gate
    assert "return `incomplete` and review nothing" in gate
    for name in ("FIRST-REVIEW prompt", "RE-REVIEW prompt", "REVISE prompt"):
        assert name in gate, (rel, name)
    assert (
        "may add detail to the core below but may never change the roles or the core steps"
        in gate
    )
    assert "if they disagree, this core wins" in gate
    for label in LABELS:
        assert f'- {label}: "' not in text, (rel, label)
    lines = text.splitlines()
    start = lines.index("## Review Loop") + 1
    end = next(i for i in range(start, len(lines)) if lines[i].startswith("## "))
    assert lines[end] == "## Review-loop prompts (hard gate)"
    assert "src/superclaude" not in "\n".join(lines[end : end + 8])


def test_guide_points_at_the_gate_not_the_file_and_holds_no_prompt_text():
    for rel in GUIDES:
        text = _text(rel)
        assert (
            'follow the "Review-loop prompts (hard gate)" section of `/sc:spec-panel`'
            in text
        )
        assert "do not write the brief yourself" in text
        assert "document_review_loop_prompts" not in text, rel
        for label in LABELS:
            assert f'- {label}: "' not in text, (rel, label)


def test_installer_ships_the_rules_file(tmp_path):
    from superclaude.cli import install_user_setup as setup

    ok, message = setup.install_rules(home=tmp_path)
    assert ok, message
    assert (
        tmp_path / ".claude/rules/prompts/document_review_loop_prompts.md"
    ).is_file()
