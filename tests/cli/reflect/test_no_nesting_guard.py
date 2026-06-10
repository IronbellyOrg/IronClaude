"""NFR-7 no-nesting guard (two layers).

Layer A: the ``POST_REFLECT_MODE: wrapper`` branch in the task-builder SKILL
SOURCE (not the ``.claude/`` mirror) shells out via Bash (``superclaude reflect
run`` + ``--depth``) and contains NO Agent/Task nesting tokens.

Layer B: the wrapper module ``runner.py`` launches reflect ONLY via the
``ClaudeProcess`` subprocess primitive -- no agent-surface imports.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

# Repo root = four parents up from this file (tests/cli/reflect/<file>).
_REPO_ROOT = Path(__file__).resolve().parents[3]
_SKILL_SRC = _REPO_ROOT / "src/superclaude/skills/task-builder/SKILL.md"
_REFLECT_PKG = _REPO_ROOT / "src/superclaude/cli/reflect"
_RUNNER_SRC = _REFLECT_PKG / "runner.py"
# Every reflect-wrapper source module (thinness guards apply package-wide).
_REFLECT_PY = sorted(p for p in _REFLECT_PKG.glob("*.py") if p.name != "__init__.py")

# Import statements pulling in the heavy sibling subcommand packages (NFR-1).
# Anchored on `from`/`import` so the guardrail DOCSTRING prose
# ("No imports from ``superclaude.cli.sprint``") never false-positives.
_SPRINT_ROADMAP_IMPORT_RE = re.compile(
    r"^\s*(?:from|import)\s+\S*(?:sprint|roadmap)", re.MULTILINE
)
# Real async/await CODE (anchored), not the docstring word "async def".
_ASYNC_DEF_RE = re.compile(r"^\s*async\s+def\b", re.MULTILINE)
_AWAIT_RE = re.compile(r"^\s*await\s", re.MULTILINE)
# Real raw-subprocess CALLS (identifier.method followed by `(`) + import lines.
# Anchored so the _apply_remediation docstring prose ("never a raw
# ``subprocess.run`` / ``Popen``") does NOT false-positive (it has no `(`).
_RAW_SUBPROCESS_CALL_RE = re.compile(r"\b(?:subprocess\.(?:run|Popen)|Popen)\s*\(")
_IMPORT_SUBPROCESS_RE = re.compile(
    r"^\s*(?:import\s+subprocess|from\s+subprocess\b)", re.MULTILINE
)

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


@pytest.mark.xfail(
    reason=(
        "Cross-component: this Layer-A guard asserts the task-builder SKILL Mode-2 "
        "wrapper shell-out block (marker `auto-resolved-2`), which is GENERATOR-side "
        "content emitted by the companion worktree (reflect/f3-hygiene-stage105-e2e). "
        "It is absent on this wrapper-only canonical base (and on origin/master). "
        "Adding it here would couple the wrapper to unmerged generator work, which "
        "NFR-5 forbids. XPASSes (auto-recovers) once the generator's task-builder "
        "Mode-2 block lands. Out of scope for TASK-RF-reflect-wrapper-autofix."
    ),
    strict=False,
)
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


def test_no_sprint_or_roadmap_import_anywhere_in_reflect_pkg() -> None:
    """AC-8: NO cli.sprint / cli.roadmap import in any cli/reflect/*.py (NFR-1)."""
    assert _REFLECT_PY, "expected to find reflect package source files"
    for path in _REFLECT_PY:
        src = path.read_text(encoding="utf-8")
        m = _SPRINT_ROADMAP_IMPORT_RE.search(src)
        assert m is None, (
            f"sprint/roadmap import leaked into {path.name}: {m.group(0)!r}"
        )


def test_no_async_await_anywhere_in_reflect_pkg() -> None:
    """AC-8: zero `async def` / `await` CODE in any cli/reflect/*.py (anchored, NFR-1).

    Anchored regexes avoid the docstring prose ("Zero ``async def`` / ``await``")
    in runner.py:10 / config.py:9 / models.py:10 false-positiving.
    """
    for path in _REFLECT_PY:
        src = path.read_text(encoding="utf-8")
        assert _ASYNC_DEF_RE.search(src) is None, f"`async def` in {path.name}"
        assert _AWAIT_RE.search(src) is None, f"`await ` in {path.name}"


def test_apply_remediation_launches_only_via_claudeprocess() -> None:
    """AC-8: the /task apply (and audit) launch ONLY via ClaudeProcess in runner.py.

    Scoped to runner.py (NOT a package-wide subprocess grep -- commands.py:267-274
    legitimately uses subprocess.run for --tmux). runner.py must NOT import or call
    raw subprocess.run / Popen; the apply is a ClaudeProcess `/task` launch.
    """
    src = _RUNNER_SRC.read_text(encoding="utf-8")
    assert "ClaudeProcess" in src
    assert "_apply_remediation" in src
    assert "/task " in src  # the apply prompt is a /task launch
    # Anchored on real CALLS / imports so the docstring prose does not false-positive.
    m = _RAW_SUBPROCESS_CALL_RE.search(src)
    assert m is None, f"raw subprocess call leaked into runner.py: {m.group(0)!r}"
    assert _IMPORT_SUBPROCESS_RE.search(src) is None, "runner.py imports subprocess"
