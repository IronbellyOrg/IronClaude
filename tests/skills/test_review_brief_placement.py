"""Placement pins for the coordinator review/revise briefs (#346 P6 experiment).

The wording is identical in all three variants; only where it lives differs. Static text assertions only.
"""

from __future__ import annotations

import re  # noqa: F401
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
LABELS = ("First-review brief", "Re-review brief", "Revise brief")


def _text(rel: str) -> str:
    return (_REPO / rel).read_text(encoding="utf-8")


RULES_FILE = _REPO / "src/superclaude/rules/prompts/document_review_loop_prompts.md"
REF = "~/.claude/rules/prompts/document_review_loop_prompts.md"


def test_c_rules_file_holds_the_briefs_roles_and_when_to_use():
    text = RULES_FILE.read_text(encoding="utf-8")
    for label in LABELS:
        assert f'- {label}: "' in text, label
    for token in (
        "Prompt R1",
        "Prompt R2",
        "Prompt V1",
        "## When to use which prompt",
        "## Roles (fixed)",
        "## Never",
    ):
        assert token in text, token
    for ph in ("{{CANDIDATE}}", "{{BASELINE}}", "{{PRIOR}}", "{{N}}", "{{IDS}}"):
        assert ph in text, ph
    assert "does not change the roles" in text
    assert "src/superclaude" not in text


def test_c_spec_panel_has_the_hard_gate_in_both_copies():
    for rel in SPEC_PANELS:
        text = _text(rel)
        assert "\n## Review-loop prompts (hard gate)\n" in text, rel
        assert f"read `{REF}` in full" in text
        assert "return `incomplete`" in text and "do not review" in text
        for token in (
            "Prompt R1",
            "Prompt R2",
            "Prompt V1",
            "{{CANDIDATE}}",
            "{{BASELINE}}",
            "{{PRIOR}}",
            "{{N}}",
        ):
            assert token in text, (rel, token)
        assert "that prompt is the brief" in text
        for label in LABELS:
            assert f'- {label}: "' not in text, (
                rel,
                label,
            )  # briefs are not duplicated in the command
        # the gate must sit outside the seven-bullet Review Loop section
        lines = text.splitlines()
        start = lines.index("## Review Loop") + 1
        end = next(i for i in range(start, len(lines)) if lines[i].startswith("## "))
        assert lines[end] == "## Review-loop prompts (hard gate)"
        assert "src/superclaude" not in "\n".join(lines[end : end + 12])


def test_c_guide_references_the_file_and_holds_no_briefs():
    for rel in GUIDES:
        text = _text(rel)
        assert f"read `{REF}` first" in text
        assert (
            "Use Prompt R1 for a first review, Prompt R2 for a re-review and Prompt V1 for a revision"
            in text
        )
        assert (
            "name that file, name the prompt, and give the values it asks for" in text
        )
        for label in LABELS:
            assert f'- {label}: "' not in text, (rel, label)


def test_c_installer_ships_the_rules_file(tmp_path):
    from superclaude.cli import install_user_setup as setup

    ok, message = setup.install_rules(home=tmp_path)
    assert ok, message
    assert (
        tmp_path / ".claude/rules/prompts/document_review_loop_prompts.md"
    ).is_file()
