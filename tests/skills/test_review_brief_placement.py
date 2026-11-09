"""Placement pins for the coordinator review/revise briefs (#346 P6 experiment).

The wording is identical in all three variants; only where it lives differs. Static text assertions only.
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
LABELS = ("First-review brief", "Re-review brief", "Revise brief")


def _text(rel: str) -> str:
    return (_REPO / rel).read_text(encoding="utf-8")


def test_a_briefs_live_in_both_spec_panel_copies():
    for rel in SPEC_PANELS:
        text = _text(rel)
        assert "\n## Coordinator briefs\n" in text, rel
        assert "**Inputs and roles.**" in text
        assert (
            "`--baseline` is the saved copy of the spec as it was before the revision"
            in text
        )
        assert "does not change the roles" in text
        for label in LABELS:
            assert f'- {label}: "' in text, (rel, label)
        assert "apply all findings" in text  # the prohibition is stated


def test_a_review_loop_section_is_untouched_by_the_placement():
    # the seven single-line bullets stay the only content of the Review Loop section
    for rel in SPEC_PANELS:
        lines = _text(rel).splitlines()
        start = lines.index("## Review Loop") + 1
        end = next(i for i in range(start, len(lines)) if lines[i].startswith("## "))
        body = [ln for ln in lines[start:end] if ln.strip()]
        assert len(body) == 7 and all(re.match(r"^[1-7]\. \*\*", ln) for ln in body)
        assert lines[end] == "## Coordinator briefs"


def test_a_guide_points_to_the_command_and_holds_no_briefs():
    for rel in GUIDES:
        text = _text(rel)
        assert (
            'copy the briefs from the "Coordinator briefs" section of `~/.claude/commands/sc/spec-panel.md`'
            in text
        )
        for label in LABELS:
            assert f'- {label}: "' not in text, (rel, label)
