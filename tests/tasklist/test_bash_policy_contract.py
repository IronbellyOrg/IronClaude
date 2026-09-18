"""Pins the tasklist-local Bash inspection policy contract."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = REPO_ROOT / "src/superclaude/skills/sc-tasklist-protocol"


def test_skill_emission_template_and_self_check_require_policy_block():
    skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")

    assert "the required `## Bash Inspection Policy` framework-guidance block" in skill
    assert "After the phase goal and before the first task" in skill
    assert "do not flag, weaken, remove, or patch it as invented content" in skill


def test_phase_template_places_policy_before_tasks():
    template = (SKILL_ROOT / "templates/phase-template.md").read_text(encoding="utf-8")

    assert template.index("## Bash Inspection Policy") < template.index(
        "## Task Format"
    )
    assert "Follow the globally installed `BASH_INSPECTION_POLICY.md`." in template
