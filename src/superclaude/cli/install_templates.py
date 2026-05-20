"""
Template Installation

Installs SuperClaude document/workflow templates to ``~/.claude/templates/``
preserving the ``workflow/`` and ``documents/`` subdirectory structure.

Templates are the canonical document schemas (PRD, TDD, MDTM task,
release-spec, etc.) consumed by the various ``superclaude`` CLI
pipelines. They must be resolvable from any CWD by the pipeline code,
which is why they live under ``~/.claude/`` after install rather than
inside the package's ``src/`` tree.

The installer NEVER touches ``~/.claude/agent-memory/`` — that directory
is reserved for per-agent runtime memory and is owned by the agents
themselves, not by ``superclaude install``.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import List, Tuple

# Files we refuse to ever write into the target directory (defensive —
# the source tree shouldn't contain these names, but if it did, we
# would still skip them).
_PROTECTED_TARGET_SUBDIRS = ("agent-memory",)


def install_templates(
    target_path: Path | None = None, force: bool = False
) -> Tuple[bool, str]:
    """Install all SuperClaude templates to ``~/.claude/templates/``.

    Args:
        target_path: Target installation directory. Defaults to
            ``~/.claude/templates``.
        force: Overwrite existing files. Without this flag, files
            already present in the target are left untouched.

    Returns:
        Tuple of ``(success, summary_message)``.
    """
    if target_path is None:
        target_path = Path.home() / ".claude" / "templates"

    source = _get_templates_source()

    if not source or not source.is_dir():
        return False, f"Template source directory not found: {source}"

    target_path.mkdir(parents=True, exist_ok=True)

    installed: List[str] = []
    skipped: List[str] = []
    failed: List[str] = []

    for src_file in sorted(source.rglob("*")):
        if not src_file.is_file():
            continue
        if "__pycache__" in src_file.parts:
            continue

        rel = src_file.relative_to(source)

        # Defensive: never write into a protected subdir.
        if any(p in _PROTECTED_TARGET_SUBDIRS for p in rel.parts):
            continue

        dest = target_path / rel
        if dest.exists() and not force:
            skipped.append(str(rel))
            continue
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, dest)
            installed.append(str(rel))
        except Exception as exc:  # noqa: BLE001 — surface any IO failure
            failed.append(f"{rel}: {exc}")

    messages: List[str] = []
    if installed:
        messages.append(f"✅ Installed {len(installed)} templates:")
        for rel in installed:
            messages.append(f"   - {rel}")
    if skipped:
        messages.append(
            f"\n⚠️  Skipped {len(skipped)} existing templates (use --force to overwrite):"
        )
        for rel in skipped:
            messages.append(f"   - {rel}")
    if failed:
        messages.append(f"\n❌ Failed to install {len(failed)} templates:")
        for fail in failed:
            messages.append(f"   - {fail}")

    if not installed and not skipped and not failed:
        return False, "No templates were installed (source directory empty?)"

    messages.append(f"\n📁 Installation directory: {target_path}")

    success = len(failed) == 0
    return success, "\n".join(messages)


def _get_templates_source() -> Path:
    """Locate ``src/superclaude/templates/`` for both layouts.

    1. **Editable install** (this file at ``<repo>/src/superclaude/cli/install_templates.py``)
       — templates live at ``<repo>/src/superclaude/templates``.
    2. **pipx / wheel install** (force-include puts ``src/`` at
       ``<site-packages>/superclaude/_src/``) — templates live at
       ``<site-packages>/superclaude/_src/superclaude/templates``.
    """
    here = Path(__file__).resolve()
    package_root = here.parent.parent  # .../superclaude/

    editable = package_root / "templates"
    if editable.is_dir():
        return editable

    wheel = package_root / "_src" / "superclaude" / "templates"
    if wheel.is_dir():
        return wheel

    # Return the editable candidate even if missing so the error message
    # cites an absolute path the user can easily inspect.
    return editable


def list_available_templates() -> List[str]:
    """Return relative paths of templates available for installation."""
    source = _get_templates_source()
    if not source.is_dir():
        return []
    return sorted(
        str(f.relative_to(source))
        for f in source.rglob("*")
        if f.is_file()
        and "__pycache__" not in f.parts
        and not any(p in _PROTECTED_TARGET_SUBDIRS for p in f.relative_to(source).parts)
    )


def list_installed_templates() -> List[str]:
    """Return relative paths of templates currently installed at ~/.claude/templates/."""
    target = Path.home() / ".claude" / "templates"
    if not target.is_dir():
        return []
    return sorted(
        str(f.relative_to(target))
        for f in target.rglob("*")
        if f.is_file()
        and "__pycache__" not in f.parts
        and not any(p in _PROTECTED_TARGET_SUBDIRS for p in f.relative_to(target).parts)
    )
