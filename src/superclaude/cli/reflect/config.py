"""Reflect-wrapper input resolution -- ``resolve_config`` + FR-3/FR-4 derivation.

Turns CLI args + tasklist frontmatter + git state into a validated
``ReflectConfig``. Raises ``ValueError`` (caught by the command body, routed
to a ``blocked`` exit) on any unresolvable input or a preflight STOP.

Isolation guardrails:
- No imports from ``superclaude.cli.sprint`` or ``superclaude.cli.roadmap``.
- Zero ``async def`` / ``await``.
- Imports nothing from ``commands.py`` / ``runner.py`` / ``contract.py``.

FR-3 input derivation, FR-4 pinned output dir + ``.claude`` STOP, G1 max_turns
default (Open Question OQ6), OQ1 base-branch default ``master``.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from superclaude.cli.pipeline.frontmatter import extract_frontmatter

from .models import ReflectConfig

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# NFR-5: default subprocess timeout (ClaudeProcess default is 6300 -- override).
_DEFAULT_TIMEOUT_SECONDS = 3600

# G1 / OQ6: per-process turn ceiling sized for a Tier-2 reflect run
# (heterogeneous reviewers + adversarial merge + evidence-validator +
# promotion gate plausibly exceed the ClaudeProcess default of 100 top-level
# turns; 100 would truncate the common-path T2 audit into a fail-closed HALT,
# defeating "zero human intervention in the common path"). No user-facing
# ``--max-turns`` flag in v1 (keeps the spec Section 9 option set exact).
_DEFAULT_MAX_TURNS = 250

# OQ1 (LOAD-BEARING): the project trunk is ``master`` (origin/HEAD -> master);
# an ``integration`` branch also exists but hardcoding it would compute the
# WRONG base. Make it a parameter defaulting to ``master``, never hardcode.
_DEFAULT_BASE_BRANCH = "master"

# FR-4 STOP: an ``--output`` resolving under any of these ``.claude`` subtrees
# is a reflect STOP condition -- reject before launch.
_CLAUDE_PROTECTED_SUBDIRS = frozenset({"skills", "agents", "commands"})

# Frontmatter key the builder/executor records the task-start commit under.
_FRONTMATTER_START_COMMIT_KEY = "start_commit"
_FRONTMATTER_SPEC_PATH_KEY = "spec_path"
_FRONTMATTER_EXECUTOR_MODEL_KEY = "executor_model_class"

# OQ2: env var consulted first for the anti-self-confirmation executor class.
_EXECUTOR_MODEL_ENV = "EXECUTOR_MODEL_CLASS"


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _git(cwd: Path, *args: str) -> str:
    """Run ``git -C <cwd> <args>`` and return stripped stdout.

    Models the ``drift.py`` ``_git`` subprocess shape. Raises
    ``subprocess.SubprocessError`` (via ``check=True``) or ``OSError`` on
    failure so callers can route to a fail-closed fallback.
    """
    result = subprocess.run(
        ["git", "-C", str(cwd), *args],
        capture_output=True,
        check=True,
        text=True,
        timeout=10,
    )
    return result.stdout.strip()


def _resolve_base(
    cwd: Path,
    frontmatter: dict[str, str],
    base_branch: str,
    base_override: str | None = None,
) -> str:
    """Derive ``<BASE>`` per the FR-6 precedence chain.

    ``--base`` override -> frontmatter ``start_commit`` ->
    ``git merge-base HEAD <base_branch>`` -> else raise
    ``ValueError("base-unresolved")``.

    The ``base_override`` value is stored VERBATIM as a SINGLE ref: no ``..``
    range parsing/splitting is performed (F3 de-range invariant, FR-6). The
    diff against this ref is the working-tree diff reflect computes downstream.
    """
    if base_override is not None and base_override.strip():
        return base_override.strip()
    start_commit = frontmatter.get(_FRONTMATTER_START_COMMIT_KEY, "").strip()
    if start_commit:
        return start_commit
    try:
        return _git(cwd, "merge-base", "HEAD", base_branch)
    except (OSError, subprocess.SubprocessError) as exc:
        raise ValueError("base-unresolved") from exc


def _is_under_claude_protected(path: Path) -> bool:
    """True if ``path`` is under ``.claude/{skills,agents,commands}`` (FR-4 STOP)."""
    parts = path.parts
    for i, part in enumerate(parts):
        if part == ".claude" and i + 1 < len(parts):
            if parts[i + 1] in _CLAUDE_PROTECTED_SUBDIRS:
                return True
    return False


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def resolve_config(
    tasklist_path: str | Path,
    *,
    depth: str,
    spec_path: str | Path | None = None,
    output_dir: str | Path | None = None,
    model: str,
    timeout: int | None = None,
    max_turns: int | None = None,
    promote: bool = False,
    allow_single_vendor: bool = False,
    tmux: bool = False,
    dry_run: bool = False,
    print_command: bool = False,
    resume: bool = False,
    base_branch: str = _DEFAULT_BASE_BRANCH,
    base_override: str | None = None,
    fix: bool = False,
    max_fix_iterations: int = 2,
    transport: str = "openai_compat",
    reviewers: int = 3,
) -> ReflectConfig:
    """Resolve CLI args + frontmatter + git state into a ``ReflectConfig``.

    Args:
        tasklist_path: Explicit path to the MDTM tasklist (no cwd guessing).
        depth: ``standard`` | ``deep`` (``quick`` is floored to ``standard``).
        spec_path: Explicit ``--spec`` override; else frontmatter ``spec_path``.
        output_dir: Explicit ``--output``; else ``<task-dir>/reflect/post/<short-sha>/`` (``HEAD[:12]``).
        model: Non-empty Claude model (empty would omit ``--model``).
        timeout: Subprocess timeout seconds (default 3600).
        max_turns: Per-process turn ceiling (G1; default 250, never None).
        promote / allow_single_vendor / tmux / dry_run / print_command /
        resume: wrapper-side flags threaded through to the runner.
        base_branch: base for ``git merge-base`` fallback (default ``master``).
        transport: Tier-2 worker transport (``openai_compat`` or ``stub``).
        reviewers: Tier-2 reviewer slots; ``1`` is preserved as the negative
            witness, otherwise values are clamped to ``[2,4]``.

    Returns:
        A fully-populated ``ReflectConfig``.

    Raises:
        ValueError: tasklist missing, base unresolved, ``--output`` under
            ``.claude/{skills,agents,commands}``, or empty model.
    """
    # -- Tasklist path --
    resolved_tasklist = Path(tasklist_path).resolve()
    if not resolved_tasklist.is_file():
        raise ValueError(f"tasklist not found: {resolved_tasklist}")

    # -- Model (non-empty required -- empty omits --model in ClaudeProcess) --
    resolved_model = (model or "").strip()
    if not resolved_model:
        raise ValueError("model must be non-empty (empty model omits --model)")

    # -- Frontmatter (scalar keys only) --
    frontmatter = (
        extract_frontmatter(resolved_tasklist.read_text(encoding="utf-8")) or {}
    )

    # -- git cwd: the tasklist's own directory (git -C discovers the repo root) --
    git_cwd = resolved_tasklist.parent

    # -- <BASE> via FR-6 precedence chain (--base override first); <HEAD> via rev-parse --
    base = _resolve_base(git_cwd, frontmatter, base_branch, base_override=base_override)
    try:
        head = _git(git_cwd, "rev-parse", "HEAD")
    except (OSError, subprocess.SubprocessError) as exc:
        raise ValueError("head-unresolved") from exc

    # -- Depth floor (O4/FR-3 -- POST never runs quick) --
    resolved_depth = "standard" if depth == "quick" else depth

    # -- Tier-2 ensemble transport/reviewer plumbing (§5.1) --
    resolved_transport = (transport or "openai_compat").strip()
    if resolved_transport not in {"openai_compat", "stub"}:
        raise ValueError(
            f"transport must be openai_compat or stub: {resolved_transport}"
        )
    raw_reviewers = int(reviewers)
    resolved_reviewers = 1 if raw_reviewers == 1 else max(2, min(4, raw_reviewers))

    # -- Spec path: explicit arg, else frontmatter, only when one existing file --
    resolved_spec: Path | None = None
    spec_candidate = spec_path or frontmatter.get(_FRONTMATTER_SPEC_PATH_KEY) or None
    if spec_candidate:
        candidate = Path(spec_candidate).resolve()
        if candidate.is_file():
            resolved_spec = candidate

    # -- Executor model: env first (OQ2), then frontmatter, else None --
    executor_model = (
        os.environ.get(_EXECUTOR_MODEL_ENV, "").strip()
        or frontmatter.get(_FRONTMATTER_EXECUTOR_MODEL_KEY, "").strip()
    )
    resolved_executor_model: str | None = executor_model or None

    # -- Output dir: default <task-dir>/reflect/post/<short-sha>/ (FR-4) --
    if output_dir:
        resolved_output = Path(output_dir).resolve()
    else:
        resolved_output = (
            resolved_tasklist.parent / "reflect" / "post" / head[:12]
        ).resolve()
    if _is_under_claude_protected(resolved_output):
        raise ValueError(
            f"--output must not be under .claude/{{skills,agents,commands}}: "
            f"{resolved_output}"
        )

    return ReflectConfig(
        tasklist_path=resolved_tasklist,
        base=base,
        head=head,
        spec_path=resolved_spec,
        depth=resolved_depth,
        executor_model=resolved_executor_model,
        output_dir=resolved_output,
        model=resolved_model,
        timeout_seconds=timeout or _DEFAULT_TIMEOUT_SECONDS,
        max_turns=max_turns or _DEFAULT_MAX_TURNS,
        promote=promote,
        allow_single_vendor=allow_single_vendor,
        tmux=tmux,
        dry_run=dry_run,
        print_command=print_command,
        resume=resume,
        base_override=base_override,
        fix=fix,
        max_fix_iterations=max_fix_iterations,
        transport=resolved_transport,
        reviewers=resolved_reviewers,
    )
