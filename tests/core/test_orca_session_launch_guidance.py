"""Pin shell/agent distinctions in the installed Claude session guidance."""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2] / "src" / "superclaude"


@pytest.mark.parametrize("relative", ["core/CLAUDE.md", "skills/ccsession-tag/README.md"])
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
    ):
        assert required in section, (relative, required)
