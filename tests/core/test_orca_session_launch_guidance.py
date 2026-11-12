"""Pin shell/agent distinctions in the installed Claude session guidance."""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2] / "src" / "superclaude"
COPIES = ["core/CLAUDE.md", "skills/ccsession-tag/README.md"]
EXISTING_END = "commands' internal Agent-tool subagents.\n\n"


@pytest.mark.parametrize("relative", COPIES)
def test_orca_session_launch_guidance(relative: str) -> None:
    text = (ROOT / relative).read_text()
    start = text.index("### Orca session launches")
    section = text[start:].split("\n## ", 1)[0]
    for required in (
        "Claude (CLI)",
        "never **New Terminal**",
        "`terminal create` is for shells",
        "version-matched `orca-cli` guide",
        "`agent launch`",
        "`worktree create --agent`",
        "`--surface terminal`",
        "ccsession-orca",
        "supervised workers",
        "`worker-start`",
        "dispatch preamble",
        "internal Agent-tool subagents",
        "Every Orca worktree gets an agent",
        "never create a worktree for your own use",
        "owns its agent",
        "coordinator is person-opened",
        "authorize a supervised worker to create worktrees or dispatch workers",
    ):
        assert "coordinator under another orchestrator" not in section
        assert required in section, (relative, required)


def _appended_paragraph(relative: str) -> str:
    text = (ROOT / relative).read_text()
    start = text.index("### Orca session launches")
    after = text[start:].split(EXISTING_END, 1)[1]
    return after.split("\n\n", 1)[0]


@pytest.mark.parametrize("relative", COPIES)
def test_appended_paragraph_names_the_owner_roles_and_no_source_path(
    relative: str,
) -> None:
    paragraph = _appended_paragraph(relative)
    assert paragraph.startswith("Every Orca worktree gets an agent")
    assert "orchestrator" in paragraph and "coordinator" in paragraph
    assert "A hook blocks `orca worktree create` without `--agent`" in " ".join(
        paragraph.split()
    )
    assert "src/superclaude/" not in paragraph


def test_appended_paragraph_is_identical_in_both_copies() -> None:
    first, second = (_appended_paragraph(relative) for relative in COPIES)
    assert first == second
