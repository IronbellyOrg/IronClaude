"""Guards for /sc:workflow v3: thin command + skill refs (SPEC §8)."""

import filecmp
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_CMD = _REPO / "src" / "superclaude" / "commands" / "workflow.md"
_SKILL = _REPO / "src" / "superclaude" / "skills" / "sc-workflow-protocol"
_REFS = (
    "input-parse.md",
    "phase-templates.md",
    "overlap-routing.md",
    "quality-gates.md",
    "return-contract.md",
)


def test_activation_handoff():
    text = _CMD.read_text(encoding="utf-8")
    assert "## Activation" in text
    assert "Skill sc:workflow-protocol" in text


def test_command_has_no_execute_step():
    text = _CMD.read_text(encoding="utf-8")
    assert "**Execute**" not in text
    assert "Analyze→Plan" not in text


def test_skill_and_five_refs_exist():
    assert (_SKILL / "SKILL.md").is_file()
    for name in _REFS:
        assert (_SKILL / "refs" / name).is_file(), name


def test_mcp_servers_empty():
    text = _CMD.read_text(encoding="utf-8")
    assert "mcp-servers: []" in text
    assert "morphllm" not in text


def test_plan_uses_template_00():
    skill = (_SKILL / "SKILL.md").read_text(encoding="utf-8")
    gates = (_SKILL / "refs" / "quality-gates.md").read_text(encoding="utf-8")
    assert "00_mdtm_template_simple_task.md" in skill
    assert "03_project_plan_template" not in skill + gates
    for key in ("schema: workflow-plan/1.1", "version:", "priority:", "created_date:"):
        assert key in gates, key


def test_plugin_mirror_matches_src():
    plugin = _REPO / "plugins" / "superclaude" / "skills" / "sc-workflow-protocol"
    src_rels = {str(p.relative_to(_SKILL)) for p in _SKILL.rglob("*.md")}
    plugin_rels = {str(p.relative_to(plugin)) for p in plugin.rglob("*.md")}
    assert src_rels == plugin_rels, src_rels ^ plugin_rels
    _, mismatch, errors = filecmp.cmpfiles(
        _SKILL, plugin, sorted(src_rels), shallow=False
    )
    assert not mismatch and not errors, mismatch + errors
