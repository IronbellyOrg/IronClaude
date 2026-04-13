"""PRD pipeline configuration -- CLI argument resolution and PrdConfig construction.

Resolves CLI arguments into a fully-populated ``PrdConfig`` instance with
sensible defaults, path resolution, and tier validation.

NFR-PRD.1: Zero ``async def`` or ``await`` in this module.
NFR-PRD.7: No imports from superclaude.cli.sprint or superclaude.cli.roadmap.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional, Sequence

from superclaude.cli.prd.models import PrdConfig


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_VALID_TIERS = frozenset({"lightweight", "standard", "heavyweight"})

# Known step ID patterns for resume validation.
# Step IDs follow the pattern: word-word or word-word-word (kebab-case).
_STEP_ID_PATTERN = re.compile(
    r"^(check-existing|parse-request|scope-discovery|research-notes"
    r"|sufficiency-review|template-triage|build-task-file|verify-task-file"
    r"|preparation|investigation-\d+|web-research-\d+"
    r"|analyst-completeness|qa-research-gate"
    r"|synthesis-\d+|analyst-synthesis|qa-synthesis-gate"
    r"|assembly|structural-qa|qualitative-qa|completion)$"
)

_DEFAULT_SKILL_REFS_DIRS = [
    Path("src/superclaude/skills/prd/refs"),
    Path(".claude/skills/prd/refs"),
]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def resolve_config(
    request: str,
    *,
    product: Optional[str] = None,
    where: Optional[Sequence[str]] = None,
    output: Optional[str] = None,
    tier: Optional[str] = None,
    max_turns: Optional[int] = None,
    model: Optional[str] = None,
    dry_run: bool = False,
    debug: bool = False,
    resume_from: Optional[str] = None,
) -> PrdConfig:
    """Resolve CLI arguments into a fully-populated ``PrdConfig``.

    Args:
        request: Natural-language product request (positional CLI arg).
        product: Product name or scope override.
        where: Source directories to focus on.
        output: Output path for final PRD (defaults to ".").
        tier: Pipeline tier -- must be one of "lightweight", "standard",
              "heavyweight". Defaults to "standard".
        max_turns: Turn budget for subprocesses. Defaults to 300.
        model: Claude model to use.
        dry_run: Validate config without executing.
        debug: Enable debug logging.
        resume_from: Step ID to resume from (validates format).

    Returns:
        A validated ``PrdConfig`` ready for pipeline execution.

    Raises:
        ValueError: If *tier* is invalid or *resume_from* has an
            unrecognised format.
    """
    # -- Tier validation --
    resolved_tier = (tier or "standard").lower().strip()
    if resolved_tier not in _VALID_TIERS:
        raise ValueError(
            f"Invalid tier {resolved_tier!r}. "
            f"Must be one of: {', '.join(sorted(_VALID_TIERS))}"
        )

    # -- Resume validation --
    if resume_from is not None:
        resume_from = resume_from.strip()
        if not _STEP_ID_PATTERN.match(resume_from):
            raise ValueError(
                f"Unrecognised resume step ID: {resume_from!r}. "
                f"Expected a known step pattern like 'parse-request', "
                f"'investigation-3', 'qa-synthesis-gate', etc."
            )

    # -- Path resolution --
    output_path = Path(output).resolve() if output else Path(".").resolve()

    # Derive product slug from product name or request
    product_name = product or ""
    product_slug = _slugify(product_name) if product_name else ""

    # Task directory: derived from output_path + product_slug (or 'prd-task')
    task_dir_name = f"prd-{product_slug}" if product_slug else "prd-task"
    task_dir = output_path / task_dir_name

    # Skill refs directory: auto-discover from known locations
    skill_refs_dir = _discover_skill_refs_dir()

    return PrdConfig(
        user_message=request,
        product_name=product_name,
        product_slug=product_slug,
        where=list(where) if where else [],
        output_path=output_path,
        tier=resolved_tier,
        task_dir=task_dir,
        skill_refs_dir=skill_refs_dir,
        max_turns=max_turns or 300,
        model=model or "",
        dry_run=dry_run,
        debug=debug,
        resume_from=resume_from,
    )


# ---------------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------------


def _slugify(name: str) -> str:
    """Convert a product name to a kebab-case slug."""
    slug = name.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


def _discover_skill_refs_dir() -> Path:
    """Find the skill refs directory from known locations.

    Returns the first existing directory, or the default if none found.
    """
    for candidate in _DEFAULT_SKILL_REFS_DIRS:
        if candidate.is_dir():
            return candidate
    # Fallback to the canonical source location even if it doesn't exist yet
    return _DEFAULT_SKILL_REFS_DIRS[0]
