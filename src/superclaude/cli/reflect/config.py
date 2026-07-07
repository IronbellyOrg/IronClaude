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
        raise ValueError(
            "base-unresolved: 'master' did not resolve; pass --base <ref> or set frontmatter start_commit"
        ) from exc


def _audit_tree_dirty(git_cwd: Path, base: str) -> bool:
    """COR-5 (L2): True if tracked, repo-scope (vs ``<base>``) paths are dirty.

    The audit's file set is ``git diff --name-only <base> -- .`` from the repo
    root. The tree is "dirty for the audit" if any of those repo-relative paths
    also appears in ``git status --porcelain=v1`` as a TRACKED modification.
    Untracked (``??``) entries do NOT count (they are not part of the
    committed-ref diff a snapshot captures).

    Fail-closed: any git error -> ``True`` (treat as dirty so the L2 gate STOPs
    rather than snapshotting a tree that may omit the audit target). Reuses the
    ``_git`` primitive (``config.py``). Only called when ``--isolate-reviewers``
    is set; the default (flag-off) path never probes.
    """
    try:
        repo_root = Path(_git(git_cwd, "rev-parse", "--show-toplevel"))
        scope = {
            line.strip()
            for line in _git(
                repo_root, "diff", "--name-only", base, "--", "."
            ).splitlines()
            if line.strip()
        }
        if not scope:
            return False
        for line in _git(repo_root, "status", "--porcelain=v1").splitlines():
            if not line.strip():
                continue
            status_code = line[:2]
            path = line[3:].strip()
            # Untracked entries (??) do not make the audit tree dirty.
            if status_code == "??":
                continue
            # Rename entries "R  old -> new": the new path is the dirty one.
            if " -> " in path:
                path = path.split(" -> ", 1)[1].strip()
            if path in scope:
                return True
        return False
    except (OSError, subprocess.SubprocessError):
        return True


def create_review_snapshot(config) -> tuple[Path | None, str | None]:
    """L2 (COR-2/A-2/A-3): create an isolated ``git worktree`` snapshot of the audit ref.

    Lives in ``config.py`` (the subprocess-owning module) so ``runner.py`` stays
    free of any raw ``subprocess`` import (NFR-1 thinness guard). Returns
    ``(snapshot_path, None)`` on success, or ``(None, stop_reason)`` on a
    precondition STOP. NEVER falls back to the live tree. Uses a REAL worktree
    checkout (NOT an archive) so serena/auggie stay indexed (A-2).

    Lifecycle:
      1. PRE-CLEAN a leftover ``<output>/_review-snapshot`` via ``git worktree
         remove --force`` (crash recovery); failure -> STOP ``snapshot-precleanup-failed``.
      2. RE-RESOLVE HEAD immediately before ``worktree add`` and compare to the
         config-time ``config.head``; drift -> STOP ``head-moved-precondition``
         (the parallel-session HEAD-moved hazard, memory
         ``feedback_parallel_sessions_share_index``).
      3. ``git worktree add --detach <snapshot> <ref>``; any non-zero exit -> STOP
         with the captured stderr in the reason (memory
         ``reference_worktree_merge_head_path``: teardown uses ``git worktree
         remove``, never ``rm -rf`` / ``git stash``).
    """
    git_cwd = config.tasklist_path.parent
    snapshot = config.output_dir / "_review-snapshot"
    # (1) Pre-clean a leftover snapshot from a crashed prior run.
    if snapshot.exists():
        try:
            _git(git_cwd, "worktree", "remove", "--force", str(snapshot))
        except (OSError, subprocess.SubprocessError):
            return (None, "snapshot-precleanup-failed")
    # (2a) COR-1 base-resolves check: the committability predicate requires
    # `<base>` to resolve to a commit. If `<base>` does not name a commit, STOP
    # `no-committable-ref` BEFORE the worktree add rather than snapshot against an
    # unresolvable ref.
    try:
        _git(git_cwd, "rev-parse", "--verify", f"{config.base}^{{commit}}")
    except (OSError, subprocess.SubprocessError):
        return (None, "no-committable-ref")
    # (2b) Re-resolve HEAD and compare to the config-time value (parallel-session race).
    try:
        current_head = _git(git_cwd, "rev-parse", "HEAD")
    except (OSError, subprocess.SubprocessError):
        return (None, "no-committable-ref")
    if current_head != config.head:
        return (None, "head-moved-precondition")
    # (3) Real worktree checkout (NOT archive) so serena/auggie stay indexed.
    config.output_dir.mkdir(parents=True, exist_ok=True)
    try:
        _git(git_cwd, "worktree", "add", "--detach", str(snapshot), current_head)
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or "").strip().replace("\n", " ")[:200]
        return (None, f"worktree-add-failed: {stderr}")
    except (OSError, subprocess.SubprocessError) as exc:
        return (None, f"worktree-add-failed: {exc}")
    return (snapshot, None)


def teardown_review_snapshot(config, snapshot: Path) -> None:
    """L2 teardown (A-3): remove the snapshot via ``git worktree remove --force``.

    NEVER ``rm -rf`` / ``git stash`` (memory ``reference_worktree_merge_head_path``:
    the snapshot's ``.git`` is a linked-worktree FILE; a filesystem delete orphans
    the ``.git/worktrees/<name>`` admin entry). Best-effort: a teardown failure is
    swallowed so the always-write sidecar still runs; the next run's pre-clean
    handles any leftover.
    """
    git_cwd = config.tasklist_path.parent
    try:
        _git(git_cwd, "worktree", "remove", "--force", str(snapshot))
    except (OSError, subprocess.SubprocessError):
        pass


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
    isolate_reviewers: bool = False,
    reachability: bool = True,
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

    # -- L2 (COR-5): probe the audit tree's cleanliness ONLY when reviewer
    # isolation is opted in (`--isolate-reviewers`). The default (flag-off) path
    # never probes, preserving today's #153 dirty-tree-audit behavior byte-for-byte.
    resolved_audit_tree_dirty = (
        _audit_tree_dirty(git_cwd, base) if isolate_reviewers else False
    )

    # -- Tier-2 ensemble transport/reviewer plumbing (§5.1) --
    resolved_transport = (transport or "openai_compat").strip().lower()
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
        isolate_reviewers=isolate_reviewers,
        audit_tree_dirty=resolved_audit_tree_dirty,
        reachability=reachability,
    )
