"""EvalConfig — frozen configuration dataclass for the cliEval harness.

Roadmap COMP-005 / Deliverable D-0001 (Task T01.01).

Holds the three configuration domains every eval-CLI component needs:

* ``paths``        — resolved filesystem locations (suites dir, output dir, etc.).
* ``defaults``     — per-eval default knobs (timeout, isolation mode, parallelism).
* ``allowed_scratch_roots`` — the AC12 allowlist of directories where scratch
  HOMEs and per-eval working trees may be created. Any path resolution that
  lands outside this allowlist must be rejected before any FS write.

The default ``allowed_scratch_roots`` includes ``/tmp/eval-runs`` and the
in-repo ``.dev/eval-runs`` directory, matching AC12 in the cliEval roadmap.

AC12 enforcement (T01.19 / Deliverable D-0016) lives in
:func:`resolve_scratch_root`, the single helper every caller MUST funnel
through before writing under a scratch root. The helper consumes
``EvalConfig.allowed_scratch_roots`` so the allowlist has exactly one
source of truth — no other module embeds a hard-coded copy.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Mapping

__all__ = [
    "DEFAULT_MIN_CLAUDE_VERSION",
    "EvalConfig",
    "SCRATCH_ROOT_POLICY",
    "SCRATCH_ROOT_VIOLATION_EXIT_CODE",
    "ScratchRootViolation",
    "format_scratch_root_violation",
    "resolve_scratch_root",
]


SCRATCH_ROOT_POLICY: str = (
    "cliEval scratch root policy (AC12 / OPS-002):\n"
    "  Scratch HOMEs, per-eval working trees, and --output-dir targets MUST\n"
    "  resolve under one of these allowed roots:\n"
    "    1. /tmp/eval-runs/        -- canonical M1 scratch root\n"
    "    2. <repo>/.dev/eval-runs/ -- repo-relative scratch root\n"
    "    3. --output-dir <path>    -- extends the allowlist for the current\n"
    "                                  invocation only (call-scoped, never\n"
    "                                  mutates EvalConfig.allowed_scratch_roots)\n"
    "  Anything else is rejected before any filesystem write.\n"
    "  Authoritative reference: docs/eval/scratch-roots.md."
)
"""Canonical OPS-002 / AC12 scratch-root policy text.

Single source of truth for the human-readable policy paragraph that
``superclaude eval doctor`` and other CLI commands quote verbatim when a
non-allowlisted root is supplied. The three allowed roots listed here
match :func:`_default_allowed_scratch_roots` plus the optional CLI-supplied
``--output-dir`` honored by :func:`resolve_scratch_root`; ``docs/eval/scratch-roots.md``
re-uses this constant so the docs cannot drift from the runtime check.
"""


def _default_allowed_scratch_roots() -> tuple[Path, ...]:
    """Default AC12 scratch-root allowlist."""
    return (
        Path("/tmp/eval-runs"),
        Path(".dev/eval-runs"),
    )


DEFAULT_MIN_CLAUDE_VERSION: tuple[int, int, int] = (0, 5, 0)
"""R1-mit minimum supported ``claude`` CLI version (T02.20 / D-0039).

The cliEval harness pins this floor as the single source of truth for the
``eval doctor`` ``claude.min_version`` HARD check. ``EvalConfig`` exposes
it as a mutable-by-construction field so tests (and future operator
overrides) can lower or raise the bar without monkeypatching the doctor
module, while the default keeps the policy declared verbatim in the
roadmap (R-039) at one location.
"""


@dataclass(frozen=True)
class EvalConfig:
    """Frozen configuration for the cliEval harness.

    Attributes:
        paths: Mapping of named filesystem locations (e.g. ``suites_dir``,
            ``output_dir``). An empty mapping is valid; callers fill it in.
        defaults: Mapping of default per-eval knobs (e.g. ``timeout_sec``,
            ``isolation``). An empty mapping is valid.
        allowed_scratch_roots: Ordered tuple of directories where the harness
            may create per-eval scratch HOMEs / working trees. Resolution that
            escapes this allowlist must be rejected (AC12).
        min_claude_version: ``(major, minor, patch)`` triple enforced by the
            ``eval doctor`` ``claude.min_version`` HARD check (R1-mit /
            T02.20). Defaults to :data:`DEFAULT_MIN_CLAUDE_VERSION`.
    """

    paths: Mapping[str, Path] = field(default_factory=dict)
    defaults: Mapping[str, object] = field(default_factory=dict)
    allowed_scratch_roots: tuple[Path, ...] = field(
        default_factory=_default_allowed_scratch_roots
    )
    min_claude_version: tuple[int, int, int] = DEFAULT_MIN_CLAUDE_VERSION


# ---------------------------------------------------------------------------
# AC12 enforcement (T01.19 / D-0016)
# ---------------------------------------------------------------------------


SCRATCH_ROOT_VIOLATION_EXIT_CODE: int = 2
"""Exit code mapped to :class:`ScratchRootViolation` at the CLI boundary.

Matches the loader-error trio (``SCHEMA_ERROR_EXIT_CODE``,
``INVALID_EVAL_ID_EXIT_CODE``, ``UNRESOLVED_CAPABILITY_EXIT_CODE``) so every
"harness refused to operate before any filesystem write" outcome surfaces
as a single ``2`` from the operator's point of view.
"""


class ScratchRootViolation(Exception):
    """Raised when a path escapes the AC12 scratch-root allowlist.

    Surfaces from :func:`resolve_scratch_root` whenever the candidate path,
    after symlink-free resolution, does not live inside any entry in
    ``EvalConfig.allowed_scratch_roots`` (plus the optional CLI-supplied
    ``output_dir`` for that invocation).

    Attributes:
        path: The original, un-resolved candidate path (rendered verbatim in
            messages so forensics keep the offending input).
        resolved: The fully-resolved absolute form that failed the check.
        allowed: Tuple of resolved allowlisted prefixes that were checked.
            Useful for human-readable doctor failures.
    """

    def __init__(
        self,
        path: Path,
        resolved: Path,
        allowed: Iterable[Path],
    ) -> None:
        self.path = path
        self.resolved = resolved
        self.allowed: tuple[Path, ...] = tuple(allowed)
        allowed_render = ", ".join(str(p) for p in self.allowed) or "<empty>"
        super().__init__(
            "scratch path escapes AC12 allowlist: "
            f"path={path!s} resolved={resolved!s} allowed=[{allowed_render}]"
        )


def _resolve_prefix(prefix: Path) -> Path:
    """Resolve an allowlist entry to its absolute, symlink-free form.

    ``EvalConfig`` ships relative defaults (``.dev/eval-runs``) so the
    repo-local prefix anchors against the process CWD. ``strict=False``
    keeps the helper usable in tests / fresh checkouts where the scratch
    directory may not yet exist.
    """

    return Path(prefix).expanduser().resolve(strict=False)


def resolve_scratch_root(
    path: Path | str,
    *,
    config: EvalConfig | None = None,
    output_dir: Path | str | None = None,
) -> Path:
    """Resolve ``path`` and verify it lives under an AC12 allowed root.

    The helper is the single ingress point for the AC12 allowlist policy
    (see roadmap R-016 / FR-ISO2). Callers that mint scratch directories,
    per-eval HOMEs, or output dirs MUST route the target through this
    function *before* any filesystem write so a malformed path cannot
    leak side effects onto disk.

    Args:
        path: Candidate scratch path. ``str`` accepted for ergonomics;
            normalised to ``Path``. The value is expanded (``~``) and
            resolved (``strict=False``) so symlinks and relative segments
            do not escape the allowlist.
        config: Optional :class:`EvalConfig` whose
            ``allowed_scratch_roots`` provides the policy allowlist. Falls
            back to a default-constructed instance, which yields the
            canonical pair ``(/tmp/eval-runs, .dev/eval-runs)``.
            Passing the project's live ``EvalConfig`` guarantees there is
            exactly one source of truth — no other module embeds a copy.
        output_dir: Optional CLI-supplied ``--output-dir`` to extend the
            allowlist for this call only. The value is resolved the same
            way as the rest of the allowlist; passing it does NOT mutate
            ``config``.

    Returns:
        The resolved absolute :class:`~pathlib.Path` for ``path``. Callers
        SHOULD use this returned value rather than the original input when
        composing further sub-paths so subsequent comparisons stay stable.

    Raises:
        ScratchRootViolation: ``path`` (after resolution) is not equal to
            and not relative to any entry in the resolved allowlist. The
            exception carries the original input, the resolved form, and
            the resolved allowlist so reporters can render verbatim
            forensics. CLI callers MUST map it to
            :data:`SCRATCH_ROOT_VIOLATION_EXIT_CODE` (= 2).
    """

    config = config if config is not None else EvalConfig()

    # Build the allowlist from EvalConfig (sole source of truth) plus the
    # optional per-call --output-dir. Resolving each prefix once here keeps
    # the comparison loop below allocation-free.
    allowed: list[Path] = [
        _resolve_prefix(prefix) for prefix in config.allowed_scratch_roots
    ]
    if output_dir is not None:
        allowed.append(_resolve_prefix(Path(output_dir)))

    candidate = Path(path)
    resolved = candidate.expanduser().resolve(strict=False)

    for prefix in allowed:
        # ``is_relative_to`` catches strict sub-paths; the equality branch
        # accepts the prefix itself (``/tmp/eval-runs`` is a valid root).
        if resolved == prefix or resolved.is_relative_to(prefix):
            return resolved

    raise ScratchRootViolation(candidate, resolved, allowed)


def format_scratch_root_violation(exc: ScratchRootViolation) -> str:
    """Render a :class:`ScratchRootViolation` with the canonical policy text.

    Every CLI boundary that catches :class:`ScratchRootViolation` (the
    doctor command, future ``eval run``, the loader fallback, etc.) MUST
    funnel the exception through this helper so the operator-facing message
    quotes :data:`SCRATCH_ROOT_POLICY` verbatim. Embedding the policy in
    one renderer guarantees the doctor / CLI / hook adapters cannot drift
    from each other or from ``docs/eval/scratch-roots.md`` -- per the
    OPS-002 cross-module consistency requirement (T02.25 / D-0043).

    Args:
        exc: The violation raised by :func:`resolve_scratch_root`. Its
            ``path``, ``resolved``, and ``allowed`` attributes survive
            verbatim into the rendered output so forensic detail (the
            offending input and the allowlist actually used for the
            check) is never lost.

    Returns:
        A multi-line ``str`` whose first block is the per-violation
        forensic detail (matching ``str(exc)``) and whose trailing block
        is :data:`SCRATCH_ROOT_POLICY`. Callers SHOULD emit the result to
        stderr in CLI contexts so CI log scrapers can grep the policy
        identifier (``OPS-002`` / ``AC12``) without parsing JSON.
    """

    return f"{exc}\n\n{SCRATCH_ROOT_POLICY}"
