"""Pin the project CLAUDE.md worktree rule: every worktree gets an agent."""

from pathlib import Path

CLAUDE_MD = Path(__file__).resolve().parents[2] / "CLAUDE.md"


def _section() -> str:
    text = CLAUDE_MD.read_text()
    start = text.index("### Parallel Development with Git Worktrees")
    return text[start:].split("\n## ", 1)[0]


def test_every_worktree_gets_an_agent_and_its_creator_owns_it() -> None:
    section = _section()
    assert "--agent claude" in section
    assert "every worktree gets an agent" in section
    assert "never create a worktree for your own use" in section
    first_item = next(ln for ln in section.splitlines() if ln.startswith("- ")).lower()
    for word in ("orchestrator", "coordinator", "owns"):
        assert word in first_item, word


def test_example_creates_the_worktree_with_an_agent() -> None:
    lines = [
        ln for ln in _section().splitlines() if ln.startswith("orca worktree create")
    ]
    assert lines, "the example create line is missing"
    assert all("--agent" in ln for ln in lines), lines


def test_existing_worktree_rules_are_kept() -> None:
    section = _section()
    assert "every project worktree is created through Orca" in section
    assert "Never pass Orca link flags (`--issue`, `--pr`)" in section
    assert "**Exception — internal temporary checkouts:**" in section
    assert "Do **not** use the `EnterWorktree` tool" in section
