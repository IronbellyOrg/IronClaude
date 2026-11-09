"""Placement pins for the coordinator review/revise prompts (#346, P7 refactor 1: single home plus mechanical evidence).

All prompt text lives only in the rules file. The command carries a one-sentence hard gate that restates no role,
procedure or prompt text, and the routing guide points at that gate, not at the file. Static text assertions only.
"""

from __future__ import annotations

import re
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
SPEC_PANELS = (
    "src/superclaude/commands/spec-panel.md",
    "plugins/superclaude/commands/spec-panel.md",
)
GUIDES = (
    "src/superclaude/core/HOW-WE-WORK.md",
    "plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md",
)
RULES_FILE = _REPO / "src/superclaude/rules/prompts/document_review_loop_prompts.md"
REF = "~/.claude/rules/prompts/document_review_loop_prompts.md"
LABELS = ("First-review brief", "Re-review brief", "Revise brief")


def _text(rel: str) -> str:
    return (_REPO / rel).read_text(encoding="utf-8")


def _gate_paragraph(rel: str) -> str:
    text = _text(rel)
    head = "\n## Review-loop prompts (hard gate)\n\n"
    assert head in text, rel
    after = text.split(head, 1)[1]
    return after.split("\n\n", 1)[0]


def test_rules_file_holds_all_prompt_text():
    text = RULES_FILE.read_text(encoding="utf-8")
    for label in LABELS:
        assert f'- {label}: "' in text, label
    for token in (
        "FIRST-REVIEW prompt",
        "RE-REVIEW prompt",
        "REVISE prompt",
        "## When to use which prompt",
        "## Values to fill",
        "## Never",
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
        assert token in text, token
    for ph in ("{{CANDIDATE}}", "{{BASELINE}}", "{{PRIOR}}", "{{N}}", "{{IDS}}"):
        assert ph in text, ph
    assert "src/superclaude" not in text
    assert not re.search(r"Prompt (R\d|V\d)", text), "old prompt names must be gone"
    assert "<!-- core:" not in text, "refactor 1 has no mirrored core block"


def test_spec_panel_gate_is_one_sentence_that_restates_nothing():
    for rel in SPEC_PANELS:
        para = _gate_paragraph(rel)
        assert para.count("\n") == 0, rel
        assert (
            f"read `{REF}` in full and follow its prompt for your task step by step"
            in para
        )
        assert "return `incomplete` and review nothing" in para
        assert para.count(". ") == 0 and para.endswith("."), "one sentence"
        for forbidden in (
            "CANDIDATE",
            "BASELINE",
            "PRIOR",
            "{{",
            "Step 1",
            "diff -w",
            "FIRST-REVIEW",
            "RE-REVIEW",
            "REVISE",
            "evidence",
        ):
            assert forbidden not in para, (rel, forbidden)
        text = _text(rel)
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
