"""Guards for /sc:workflow v3: thin command + skill refs (SPEC §8)."""

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
