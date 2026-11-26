"""Pin the project CLAUDE.md worktree rule: every worktree gets an agent."""

from pathlib import Path

CLAUDE_MD = Path(__file__).resolve().parents[2] / "CLAUDE.md"


def _section(text: str | None = None) -> str:
    text = CLAUDE_MD.read_text() if text is None else text
    start = text.index("### Parallel Development with Git Worktrees")
    return text[start:].split("\n## ", 1)[0]


def _example_errors(section: str) -> list[str]:
    """Reasons the worktree examples in a section are stale; empty means fine."""
    errors = [
        f"stale name {s!r}" for s in ("pm-agent", "name:integration") if s in section
    ]
    lines = section.splitlines()
    create = [ln for ln in lines if ln.startswith("orca worktree create")]
    if not create or not all(
        "--name issue-" in ln and "--agent" in ln for ln in create
    ):
        errors.append("create example needs --name issue-<N>... and --agent")
    remove = [ln for ln in lines if ln.startswith("orca worktree rm")]
    if not remove or not all("name:issue-" in ln for ln in remove):
        errors.append("rm example must name an issue- worktree")
    return errors


def test_every_worktree_gets_an_agent_and_its_creator_owns_it() -> None:
    section = _section()
    assert "--agent claude" in section
    assert "every worktree gets an agent" in section
    assert "never create a worktree for your own use" in section
    first_item = next(ln for ln in section.splitlines() if ln.startswith("- ")).lower()
    # The bullet names who owns the agent: the eligible session that creates the worktree,
    # not a coordinator and not a supervised worker (wording set by #532).
    for word in ("eligible session", "coordinator", "supervised worker", "owns"):
        assert word in first_item, word


def test_example_creates_the_worktree_with_an_agent() -> None:
    lines = [
        ln for ln in _section().splitlines() if ln.startswith("orca worktree create")
    ]
    assert lines, "the example create line is missing"
    assert all("--agent" in ln for ln in lines), lines


def test_names_follow_the_guide_pattern() -> None:
    section = _section()
    for phrase in (
        "Worktrees and branches",
        "<login>/issue-<N>[-<words>]",
        "at most 24 characters",
        "no spaces",
        "--name issue-<N>-<words>",
        # The two exceptions of the guide, so the summary never overstates the rule.
        "keep `<login>/issue-<N>`, even if that is over 24",
        "never stop on it",
        "a run of 2 to 4 digits is left out",
    ):
        assert phrase in section, phrase


def test_examples_use_issue_names() -> None:
    assert _example_errors(_section()) == []
    # The check itself fails on the old examples, so it cannot pass by accident.
    stale = _section() + "\norca worktree create --name pm-agent --agent claude\n"
    assert _example_errors(stale)
    assert _example_errors(_section().replace("name:issue-", "name:integration"))


def test_existing_worktree_rules_are_kept() -> None:
    section = _section()
    assert "every project worktree is created through Orca" in section
    assert "Never pass Orca link flags (`--issue`, `--pr`)" in section
    assert "**Exception — internal temporary checkouts:**" in section
    assert "Do **not** use the `EnterWorktree` tool" in section
