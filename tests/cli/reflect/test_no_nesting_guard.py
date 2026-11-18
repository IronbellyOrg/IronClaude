"""NFR-7 no-nesting guard.

The wrapper module ``runner.py`` launches reflect ONLY via the ``ClaudeProcess``
subprocess primitive -- no agent-surface imports. (Layer A, which read the
task-builder skill's terminal gate, went with that skill in 6.1.0.)
"""

from __future__ import annotations

import re
from pathlib import Path

# Repo root = four parents up from this file (tests/cli/reflect/<file>).
_REPO_ROOT = Path(__file__).resolve().parents[3]
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
# Anchored on `from`/`import` so guardrail DOCSTRING prose never
# false-positives.
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


def test_layer_b_wrapper_module_has_no_agent_imports() -> None:
    """No `Task(`/`subagent`/`anthropic` imports in `runner.py`, passes,
    including for the new driver module.

    FR-RH2.8: the agent-surface ban is asserted over BOTH `runner.py` and the
    swarm-driven `ensemble.py` (NFR-7 reconciliation, spec §9). `ClaudeProcess`
    is the ONLY sanctioned inference launch and must be present in both modules
    (the audit launch in `runner.py`; the adversarial Mode-A scorer in
    `ensemble.py`, per the resolved Phase 0.3 launch-site decision).
    """
    for src_path in _AGENT_SURFACE_SRCS:
        src = src_path.read_text(encoding="utf-8")
        assert "ClaudeProcess" in src, (
            f"sanctioned ClaudeProcess launch missing from {src_path.name}"
        )
        for banned in ("import anthropic", "from anthropic", "subagent", "Task("):
            assert banned not in src, (
                f"agent-surface token leaked into {src_path.name}: {banned!r}"
            )


def test_no_sprint_or_roadmap_import_anywhere_in_reflect_pkg() -> None:
    """AC-8: NO sprint/roadmap-named import in any cli/reflect/*.py (NFR-1)."""
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
    """AC-8: the /sc:implement apply (and audit) launch ONLY via ClaudeProcess in runner.py.

    Scoped to runner.py (NOT a package-wide subprocess grep -- commands.py:267-274
    legitimately uses subprocess.run for --tmux). runner.py must NOT import or call
    raw subprocess.run / Popen; the apply is a ClaudeProcess `/sc:implement` launch.
    """
    src = _RUNNER_SRC.read_text(encoding="utf-8")
    assert "ClaudeProcess" in src
    assert "_apply_remediation" in src
    assert "/sc:implement " in src  # the apply prompt is a /sc:implement launch
    assert "/task " not in src
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
