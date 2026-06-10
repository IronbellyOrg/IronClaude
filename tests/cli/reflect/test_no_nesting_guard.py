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

# Actual agent-routing tokens (a real Agent/Task invocation). Prose tokens like
# "via Agent" are intentionally NOT included: the Mode-2 Action legitimately reads
# "NEVER via Agent/Task" as a prohibition, which must not trip the no-nesting guard.
_NESTING_TOKENS = ("Task(", "subagent_type")


def _extract_wrapper_branch(text: str) -> str:
    """Return the text of the Mode-2 wrapper block in the Phase-N template.

    The ``--reflect`` dial replaced the legacy ``Wrapper arm
    (POST_REFLECT_MODE: wrapper)`` heading with the per-mode ``Mode 2`` template;
    the Bash ``superclaude reflect run`` shell-out behaviour is unchanged.
    """
    marker = "**Mode `2` / `auto-resolved-2` (§6.3, DEFAULT) — wrapper shell-out, remediate:**"
    start = text.index(marker)
    # The Mode-2 block ends where the next mode (halt) heading begins.
    end = text.index("**Mode `halt`", start)
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
