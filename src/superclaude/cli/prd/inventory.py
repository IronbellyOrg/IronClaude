"""PRD pipeline inventory -- file discovery and existing work detection.

Pure-function module for scanning task directories, detecting existing
PRD work state, and selecting templates. All functions are side-effect-free
except ``create_task_dirs`` which creates subdirectories.

Dependencies: models (ExistingWorkState, PrdConfig)
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import PrdConfig

from .models import ExistingWorkState


# ---------------------------------------------------------------------------
# Existing Work Detection (FR-PRD.1)
# ---------------------------------------------------------------------------


def check_existing_work(config: PrdConfig) -> ExistingWorkState:
    """Detect pre-existing PRD work in the task directory tree.

    Scans ``.dev/tasks/to-do/TASK-PRD-*/`` for matching product work.
    Returns one of four states:

    - NO_EXISTING: No matching task directory found.
    - RESUME_STAGE_A: Task dir exists but no completed research files.
    - RESUME_STAGE_B: Research files exist; synthesis/assembly incomplete.
    - ALREADY_COMPLETE: Final PRD artifact present and passing.

    F-008: Short product names (< 3 chars) match via frontmatter
    ``product_name`` field instead of full-content substring.
    """
    tasks_root = config.work_dir / ".dev" / "tasks" / "to-do"
    if not tasks_root.is_dir():
        return ExistingWorkState.NO_EXISTING

    # Find matching TASK-PRD-* directories
    matching_dirs = _find_matching_task_dirs(
        tasks_root, config.product_name, config.product_slug
    )
    if not matching_dirs:
        return ExistingWorkState.NO_EXISTING

    # Use most recently modified matching dir
    task_dir = max(matching_dirs, key=lambda p: p.stat().st_mtime)

    # Check for final PRD artifact
    results_dir = task_dir / "results"
    if results_dir.is_dir():
        prd_files = list(results_dir.glob("*.md"))
        if prd_files:
            return ExistingWorkState.ALREADY_COMPLETE

    # Check for research files
    research_files = discover_research_files(task_dir)
    if not research_files:
        return ExistingWorkState.RESUME_STAGE_A

    return ExistingWorkState.RESUME_STAGE_B


def _find_matching_task_dirs(
    tasks_root: Path, product_name: str, product_slug: str
) -> list[Path]:
    """Find TASK-PRD-* directories matching the product.

    F-008: For short product names (< 3 chars), requires frontmatter
    product_name match rather than substring search to avoid false positives.
    """
    matches: list[Path] = []
    for task_dir in tasks_root.glob("TASK-PRD-*"):
        if not task_dir.is_dir():
            continue

        # Check slug in directory name first
        dir_name = task_dir.name.lower()
        if product_slug and product_slug.lower() in dir_name:
            matches.append(task_dir)
            continue

        # For short product names, require frontmatter match
        if len(product_name) < 3:
            if _frontmatter_matches(task_dir, product_name):
                matches.append(task_dir)
        else:
            # Full-content substring match for longer names
            if _content_matches(task_dir, product_name):
                matches.append(task_dir)

    return matches


def _frontmatter_matches(task_dir: Path, product_name: str) -> bool:
    """Check if any markdown file in task_dir has matching product_name in frontmatter."""
    for md_file in task_dir.glob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")[:2000]
            fm_match = re.search(
                r"^---\s*\n(.*?)\n---", content, re.DOTALL
            )
            if fm_match:
                fm_text = fm_match.group(1)
                name_match = re.search(
                    r"product_name\s*:\s*(.+)", fm_text, re.IGNORECASE
                )
                if name_match and name_match.group(1).strip().lower() == product_name.lower():
                    return True
        except (OSError, UnicodeDecodeError):
            continue
    return False


def _content_matches(task_dir: Path, product_name: str) -> bool:
    """Check if any markdown file in task_dir contains the product name."""
    for md_file in task_dir.glob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")[:5000]
            if product_name.lower() in content.lower():
                return True
        except (OSError, UnicodeDecodeError):
            continue
    return False


# ---------------------------------------------------------------------------
# File Discovery
# ---------------------------------------------------------------------------


def discover_research_files(task_dir: Path) -> list[Path]:
    """Find completed research files in the task directory.

    Scans ``research/*.md`` and returns only files that are considered
    complete (non-empty and not containing incomplete markers).
    """
    research_dir = task_dir / "research"
    if not research_dir.is_dir():
        return []

    completed: list[Path] = []
    for md_file in sorted(research_dir.glob("*.md")):
        try:
            content = md_file.read_text(encoding="utf-8")
            if len(content.strip()) == 0:
                continue
            # Skip files with incomplete markers
            if re.search(r"\[INCOMPLETE\]", content, re.IGNORECASE):
                continue
            completed.append(md_file)
        except (OSError, UnicodeDecodeError):
            continue
    return completed


def discover_synth_files(task_dir: Path) -> list[Path]:
    """Find synthesis files matching the ``synth-*.md`` pattern."""
    synth_dir = task_dir / "synthesis"
    if not synth_dir.is_dir():
        return []
    return sorted(synth_dir.glob("synth-*.md"))


# ---------------------------------------------------------------------------
# Template Selection (FR-PRD.6)
# ---------------------------------------------------------------------------


def select_template(prd_scope: str) -> int:
    """Select the PRD template variant based on scope.

    Returns:
        2 for "product" scope (full creation template)
        1 for "feature" or any other scope (update template)
    """
    if prd_scope.lower() == "product":
        return 2
    return 1


# ---------------------------------------------------------------------------
# Directory Creation
# ---------------------------------------------------------------------------


def create_task_dirs(task_dir: Path) -> None:
    """Create the 5 required subdirectories for a PRD task.

    Creates: research/, synthesis/, qa/, reviews/, results/
    """
    for subdir in ("research", "synthesis", "qa", "reviews", "results"):
        (task_dir / subdir).mkdir(parents=True, exist_ok=True)
