"""Target resolution for the CLI Portify pipeline.

Resolves user-supplied targets (command names, paths, skill directories,
sc: prefixed names) into a ResolvedTarget with canonical paths.

Supports 6 input forms:
  1. COMMAND_NAME  — bare name like 'roadmap'
  2. COMMAND_PATH  — path to a .md command file
  3. SKILL_DIR     — path to a skill directory
  4. SKILL_NAME    — bare directory name like 'sc-roadmap-protocol'
  5. SKILL_FILE    — path to a SKILL.md file
  6. sc: prefix    — 'sc:roadmap' treated as COMMAND_NAME

Error codes:
  ERR_TARGET_NOT_FOUND     — target doesn't resolve to any known file/dir
  ERR_AMBIGUOUS_TARGET     — multiple matches (currently unused; command-first policy)
  ERR_BROKEN_ACTIVATION    — Activation section present but skill not found
  WARN_MISSING_AGENTS      — agents referenced but not found

Command-first policy: if the same name matches both a command and a skill,
the command interpretation wins.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from .models import (
    ERR_TARGET_NOT_FOUND,
    ERR_AMBIGUOUS_TARGET,
    ERR_BROKEN_ACTIVATION,
    WARN_MISSING_AGENTS,
    ResolvedTarget,
    TargetInputType,
)


# ---------------------------------------------------------------------------
# ResolutionError
# ---------------------------------------------------------------------------


class ResolutionError(Exception):
    """Raised when target resolution fails."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(f"[{code}] {message}")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def resolve_target(
    target: Optional[str],
    project_root: Optional[Path] = None,
    commands_dir: Optional[Path] = None,
    skills_dir: Optional[Path] = None,
    agents_dir: Optional[Path] = None,
) -> ResolvedTarget:
    """Resolve a user-supplied target into a ResolvedTarget.

    Accepts all 6 input forms.  Raises ResolutionError on failure.
    """
    # --- Validate input ---
    if not target or not target.strip():
        raise ResolutionError(ERR_TARGET_NOT_FOUND, "Target must be a non-empty string")

    target = target.strip()

    # --- Handle sc: prefix (Form 6) — strip and treat as COMMAND_NAME ---
    if target.startswith("sc:"):
        stripped = target[3:].strip()
        if not stripped:
            raise ResolutionError(ERR_TARGET_NOT_FOUND, f"Empty sc: target: {target!r}")
        target = stripped

    # --- Resolve directories from project_root if not supplied ---
    if project_root is not None:
        if commands_dir is None and (project_root / "commands").exists():
            commands_dir = project_root / "commands"
        if skills_dir is None and (project_root / "skills").exists():
            skills_dir = project_root / "skills"
        if agents_dir is None and (project_root / "agents").exists():
            agents_dir = project_root / "agents"

    target_path = Path(target)

    # --- Form 2: COMMAND_PATH — existing .md file ---
    if (
        target_path.is_file()
        and target.endswith(".md")
        and target_path.name != "SKILL.md"
    ):
        skill_dir = _find_skill_for_command(target_path, skills_dir)
        return ResolvedTarget(
            input_form=target,
            input_type=TargetInputType.COMMAND_PATH,
            command_path=target_path,
            skill_dir=skill_dir,
            project_root=project_root,
            commands_dir=commands_dir,
            skills_dir=skills_dir,
            agents_dir=agents_dir,
        )

    # --- Form 5: SKILL_FILE — path to SKILL.md ---
    if target_path.is_file() and target_path.name == "SKILL.md":
        skill_dir = target_path.parent
        cmd_path = _find_command_for_skill(skill_dir, commands_dir)
        return ResolvedTarget(
            input_form=target,
            input_type=TargetInputType.SKILL_FILE,
            command_path=cmd_path,
            skill_dir=skill_dir,
            project_root=project_root,
            commands_dir=commands_dir,
            skills_dir=skills_dir,
            agents_dir=agents_dir,
        )

    # --- Form 3: SKILL_DIR — existing directory containing SKILL.md ---
    if target_path.is_dir() and (target_path / "SKILL.md").exists():
        cmd_path = _find_command_for_skill(target_path, commands_dir)
        return ResolvedTarget(
            input_form=target,
            input_type=TargetInputType.SKILL_DIR,
            command_path=cmd_path,
            skill_dir=target_path,
            project_root=project_root,
            commands_dir=commands_dir,
            skills_dir=skills_dir,
            agents_dir=agents_dir,
        )

    # --- Form 1: COMMAND_NAME — search commands_dir for <target>.md ---
    # Command-first policy: try command before skill name
    if commands_dir is not None:
        cmd_path = commands_dir / f"{target}.md"
        if cmd_path.exists():
            skill_dir = _find_skill_for_command(cmd_path, skills_dir)
            return ResolvedTarget(
                input_form=target,
                input_type=TargetInputType.COMMAND_NAME,
                command_path=cmd_path,
                skill_dir=skill_dir,
                project_root=project_root,
                commands_dir=commands_dir,
                skills_dir=skills_dir,
                agents_dir=agents_dir,
            )

    # --- Form 4: SKILL_NAME — search skills_dir for directory named <target> ---
    if skills_dir is not None:
        skill_path = skills_dir / target
        if skill_path.is_dir() and (skill_path / "SKILL.md").exists():
            cmd_path = _find_command_for_skill(skill_path, commands_dir)
            return ResolvedTarget(
                input_form=target,
                input_type=TargetInputType.SKILL_NAME,
                command_path=cmd_path,
                skill_dir=skill_path,
                project_root=project_root,
                commands_dir=commands_dir,
                skills_dir=skills_dir,
                agents_dir=agents_dir,
            )

    raise ResolutionError(ERR_TARGET_NOT_FOUND, f"Target not found: {target!r}")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _parse_activation_skill(content: str) -> Optional[str]:
    """Extract the skill directory name from an ## Activation section.

    Looks for '> Skill sc:<name>' within the Activation section only.
    Returns the directory name (replacing ':' separator with '-'), or None.
    """
    # Find ## Activation section
    activation_match = re.search(r"^#{1,3}\s+Activation\b", content, re.MULTILINE)
    if not activation_match:
        return None

    # Extract content from Activation heading to next heading
    start = activation_match.end()
    next_heading = re.search(r"^#{1,3}\s+", content[start:], re.MULTILINE)
    section = (
        content[start : start + next_heading.start()]
        if next_heading
        else content[start:]
    )

    # Match "> Skill sc:<name>"
    skill_match = re.search(r">\s*Skill\s+sc:(\S+)", section)
    if not skill_match:
        return None

    skill_name = skill_match.group(1).rstrip(".,;")
    return f"sc-{skill_name}" if not skill_name.startswith("sc-") else skill_name


def _find_skill_for_command(
    command_path: Path,
    skills_dir: Optional[Path],
) -> Optional[Path]:
    """Resolve the skill directory linked from a command .md file.

    Reads the command's Activation section and resolves the referenced skill.
    Returns None if no Activation section or skill directory not found.
    """
    if skills_dir is None:
        return None

    try:
        content = command_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None

    skill_name = _parse_activation_skill(content)
    if skill_name is None:
        return None

    skill_path = skills_dir / skill_name
    if skill_path.is_dir() and (skill_path / "SKILL.md").exists():
        return skill_path
    return None


def _find_command_for_skill(
    skill_dir: Path,
    commands_dir: Optional[Path],
) -> Optional[Path]:
    """Reverse-resolve: find command file that activates this skill.

    Scans all .md files in commands_dir and finds one whose Activation section
    references this skill.  Returns None if no match found.
    """
    if commands_dir is None:
        return None

    try:
        cmd_files = list(commands_dir.glob("*.md"))
    except OSError:
        return None

    for cmd_file in cmd_files:
        try:
            content = cmd_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        skill_name = _parse_activation_skill(content)
        if skill_name is not None:
            # Direct check: does this command reference our skill?
            if skill_name == skill_dir.name:
                return cmd_file

    return None
