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


def test_b_briefs_live_in_both_guide_copies():
    for rel in GUIDES:
        text = _text(rel)
        for label in LABELS:
            assert f'- {label}: "' in text, (rel, label)
        assert "the baseline is the spec as it was before the revision" in text
        assert "apply all findings" in text  # the prohibition is stated


def test_b_spec_panel_is_unchanged_by_the_placement():
    for rel in SPEC_PANELS:
        text = _text(rel)
        assert "## Coordinator briefs" not in text
        assert "Review-loop prompts (hard gate)" not in text
        for label in LABELS:
            assert f'- {label}: "' not in text, (rel, label)
