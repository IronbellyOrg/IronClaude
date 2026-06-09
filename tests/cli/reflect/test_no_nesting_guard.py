"""NFR-7 no-nesting guard (two layers).

Layer A: the ``POST_REFLECT_MODE: wrapper`` branch in the task-builder SKILL
SOURCE (not the ``.claude/`` mirror) shells out via Bash (``superclaude reflect
run`` + ``--depth``) and contains NO Agent/Task nesting tokens.

Layer B: the wrapper module ``runner.py`` launches reflect ONLY via the
``ClaudeProcess`` subprocess primitive -- no agent-surface imports.
"""

from __future__ import annotations

from pathlib import Path

# Repo root = four parents up from this file (tests/cli/reflect/<file>).
_REPO_ROOT = Path(__file__).resolve().parents[3]
_SKILL_SRC = _REPO_ROOT / "src/superclaude/skills/task-builder/SKILL.md"
_RUNNER_SRC = _REPO_ROOT / "src/superclaude/cli/reflect/runner.py"

_NESTING_TOKENS = ("Task(", "subagent_type", "Agent tool", "via Agent", "Task tool")


def _extract_wrapper_branch(text: str) -> str:
    """Return the text of the ``Wrapper arm`` block in the Phase-N template."""
    marker = "**Wrapper arm (`POST_REFLECT_MODE: wrapper`):**"
    start = text.index(marker)
    # The wrapper arm ends at the next Update-status-to-Done item.
    end = text.index("**N.X — Update task status to Done**", start)
    return text[start:end]


def test_layer_a_wrapper_branch_is_bash_shellout() -> None:
    """The wrapper arm is a Bash CLI shell-out with the TCS depth baked (G3)."""
    text = _SKILL_SRC.read_text(encoding="utf-8")
    branch = _extract_wrapper_branch(text)
    # POSITIVE: invokes the CLI as a shell command with the depth passthrough.
    assert "superclaude reflect run" in branch
    assert "--depth" in branch
    # NEGATIVE: must NOT route through the Agent/Task tool surface (NFR-7).
    for token in _NESTING_TOKENS:
        assert token not in branch, f"NFR-7 violation: nesting token {token!r}"


def test_layer_b_wrapper_module_has_no_agent_imports() -> None:
    """runner.py launches reflect ONLY via ClaudeProcess (no agent surface)."""
    src = _RUNNER_SRC.read_text(encoding="utf-8")
    assert "ClaudeProcess" in src
    for banned in ("import anthropic", "from anthropic", "subagent", "Task("):
        assert banned not in src, (
            f"agent-surface token leaked into runner.py: {banned!r}"
        )
