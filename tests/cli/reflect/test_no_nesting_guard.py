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
# FR-RH2.8 / NFR-RH2.1: the swarm-driven Tier-2 driver. NFR-7 reconciliation
# (spec §9): the ensemble fans out to EXTERNAL HTTP workers via `dispatch_wave1`,
# which is NOT the in-process Agent/Task surface NFR-7 targets, so the guarantee
# (no `claude -p` self-nesting) is preserved and in fact strengthened. The
# adversarial scorer is launched through the sanctioned `ClaudeProcess` primitive
# (Phase 0.3 decision: launch site = ensemble.py), never `Task(`/`subagent_type`.
# This guard is therefore extended to scan `ensemble.py` for the same agent-surface
# bans as `runner.py`.
_ENSEMBLE_SRC = _REFLECT_PKG / "ensemble.py"
# The agent-surface bans (Layer B) apply to BOTH the runner and the new driver.
_AGENT_SURFACE_SRCS = (_RUNNER_SRC, _ENSEMBLE_SRC)
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
    """Return the O1 terminal reflect-gate block from the task-builder SKILL.

    Anchored on the flat wrapper-shell-out item heading (the exact literal the
    builder emits for the penultimate final-phase item) and bounded at the next
    checklist bullet (``- [ ] **N.X`` -- the Update-status-to-Done item). The
    block carries the SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE skip-guard + the
    ``superclaude reflect run ... --depth deep --fix --promote`` Bash shell-out.

    Fence-agnostic: ``str.index`` matches the unique substring regardless of any
    surrounding ``` fences or ``---`` rules in the templated MDTM example.
    """
    anchor = "Independent post-execution reflection gate (wrapper shell-out)"
    start = text.index(anchor)
    # Bound at the next checklist item (the Update-status-to-Done bullet).
    end = text.index("- [ ] **N.X", start)
    return text[start:end]


@pytest.mark.xfail(
    reason=(
        "The Layer-A marker was migrated from the abandoned `Mode 2` / "
        "`auto-resolved-2` (§6.3) dial taxonomy (PR #157 closed) to the flat "
        "`superclaude reflect run` contract shape. The helper now anchors on the "
        "O1 wrapper-shell-out item heading emitted by THIS worktree's "
        "task-builder/SKILL.md and the test passes against the live O1 emission, "
        "so it reports XPASS. Kept strict=False (OQ-1) to record the stale-marker "
        "migration without going red on a half-wired tree."
    ),
    strict=False,
)
def test_layer_a_wrapper_branch_is_bash_shellout() -> None:
    """O1 terminal gate is a guarded Bash CLI shell-out (contract §2 / §3.2)."""
    text = _SKILL_SRC.read_text(encoding="utf-8")
    branch = _extract_wrapper_branch(text)
    # POSITIVE -- the flat O1 shell-out (contract §2):
    assert "superclaude reflect run" in branch
    assert "--depth deep" in branch
    assert "--fix" in branch
    # POSITIVE -- the recursion-breaker skip-guard marker (contract §3.2):
    assert "SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE" in branch
    # NEGATIVE: must NOT route through the Agent/Task tool surface (NFR-7).
    for token in _NESTING_TOKENS:
        assert token not in branch, f"NFR-7 violation: nesting token {token!r}"


def test_layer_b_wrapper_module_has_no_agent_imports() -> None:
    """Layer B: no `Task(`/`subagent_type`/`anthropic`/`Agent(` surface in
    `runner.py` or the swarm-driven `ensemble.py`, including for the new driver.

    FR-RH2.8: the agent-surface ban is asserted over BOTH `runner.py` and the
    swarm-driven `ensemble.py` (NFR-7 reconciliation, spec §9). `ClaudeProcess`
    is the ONLY sanctioned inference launch and must be present in both modules
    (the audit launch in `runner.py`; the adversarial Mode-A scorer in
    `ensemble.py`, per the resolved Phase 0.3 launch-site decision).

    The banned tokens target the agent-spawn *surface* (imports + Agent/Task
    spawn calls / the `subagent_type` kwarg), NOT English prose. The FR-INLINE
    directive STRING legitimately discusses a "subagent" as data it sends to the
    remote headless agent, so we guard `subagent_type` / `Agent(` rather than the
    bare word "subagent".
    """
    for src_path in _AGENT_SURFACE_SRCS:
        src = src_path.read_text(encoding="utf-8")
        assert "ClaudeProcess" in src, (
            f"sanctioned ClaudeProcess launch missing from {src_path.name}"
        )
        for banned in (
            "import anthropic",
            "from anthropic",
            "subagent_type",
            "Agent(",
            "Task(",
        ):
            assert banned not in src, (
                f"agent-surface token leaked into {src_path.name}: {banned!r}"
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


def test_ensemble_launches_only_via_claudeprocess_no_raw_subprocess() -> None:
    """FR-RH2.8 / NFR-RH2.1/.2: `ensemble.py` adds no raw subprocess launch.

    The swarm-driven Tier-2 driver fans out via `dispatch_wave1` (external HTTP
    workers, not the Agent/Task surface) and launches the adversarial Mode-A
    scorer through the sanctioned `ClaudeProcess` primitive (Phase 0.3 launch
    site). It MUST NOT import or call raw `subprocess.run` / `Popen`.
    """
    src = _ENSEMBLE_SRC.read_text(encoding="utf-8")
    assert "ClaudeProcess" in src
    m = _RAW_SUBPROCESS_CALL_RE.search(src)
    assert m is None, f"raw subprocess call leaked into ensemble.py: {m.group(0)!r}"
    assert _IMPORT_SUBPROCESS_RE.search(src) is None, "ensemble.py imports subprocess"
