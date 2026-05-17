"""
Hook Installation

Installs SuperClaude hook scripts to ~/.claude/hooks/ and merges hook
registrations into ~/.claude/settings.json via additive atomic merge.

Critical design points (per .dev/releases/current/freshness-system/phase-4-tasklist.md
T04.01):
- Atomic write: temp file in same dir + os.replace (POSIX atomic).
- Backup before any write: ~/.claude/settings.json.bak.<ISO-8601> (install_hooks's
  own backup, separate from Claude Code's internal 5-rotate scheme).
- Refuses to overwrite a malformed target settings.json (explicit error;
  backup at <path> referenced in message).
- Additive merge for the hooks key: existing user hooks preserved; new
  registrations appended; matcher-collision detection (skip without --force,
  replace with --force).
- Pure stdlib (json + shutil + os + pathlib); no jq shell-out.
- chmod 0o755 happens AFTER copy so a failed copy never leaves a 0-byte
  executable.
"""

from __future__ import annotations

import json
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Tuple

# Paths matched here are the script names that get deposited at ~/.claude/hooks/.
# session-init.sh lives in src/superclaude/scripts/ (pre-existing single-script);
# all freshness-*.sh live in src/superclaude/hooks/scripts/.
#
# NOTE on freshness-file-changed.sh: this script is intentionally still copied
# even though the `FileChanged` event is NOT registered in v1's hooks.json. The
# T02.05 probe (2026-05-13) revealed Claude Code's FileChanged matcher accepts
# only |-separated literal filenames, not regex — design's matcher ".*" never
# matched anything. The script stays as a v1.5 starting point; CHANGELOG has
# the redesign options. A future `--no-orphans` flag (CHANGELOG v1.5 work
# items) will let strict deployments skip orphan scripts.
_FRESHNESS_SCRIPTS = [
    "freshness-session-start.sh",
    "freshness-user-prompt.sh",
    "freshness-pre-edit.sh",
    "freshness-post-read.sh",
    "freshness-file-changed.sh",  # v1: NOT registered. Kept on disk for v1.5.
    "freshness-subagent-start.sh",
    "freshness-subagent-stop.sh",
    # auggie-first PostToolUse hook (auggie-first-hook-proposal-v2.1.md).
    # Not strictly a "freshness" hook by lineage, but lives in the same hooks/scripts/
    # directory and shares the install pipeline; kept here to avoid a second list.
    "auggie-flag-clear.sh",
]
_LEGACY_SCRIPTS = ["session-init.sh"]

# Seed data files: shipped as <src_name> in src/superclaude/hooks/, deployed to
# ~/.claude/<dest_name> on install ONLY when no such file exists at the destination.
# This preserves user customizations across re-installs even with --force; user data
# is never overwritten (asymmetric vs scripts, which DO honor --force).
_SEED_FILES = [
    ("auggie-projects.txt.example", "auggie-projects.txt"),
]


def install_hooks(
    target_path: Path | None = None, force: bool = False
) -> Tuple[bool, str]:
    """
    Install hook scripts to ~/.claude/hooks/ and merge hook registrations into
    ~/.claude/settings.json.

    Args:
        target_path: Path to settings.json (default: ~/.claude/settings.json).
        force: If True, overwrite existing hook scripts and replace
            matcher-colliding registrations.

    Returns:
        (success, message) tuple matching the install_core_files convention.
    """
    if target_path is None:
        target_path = Path.home() / ".claude" / "settings.json"

    target_path = Path(target_path).expanduser()

    hooks_dir = target_path.parent / "hooks"
    source_hooks_json = _get_hooks_source()
    source_scripts_dir = _get_hooks_scripts_source()
    legacy_scripts_dir = _get_legacy_scripts_source()

    if not source_hooks_json.exists():
        return False, f"Source hooks.json not found: {source_hooks_json}"
    if not source_scripts_dir.exists():
        return False, f"Source scripts dir not found: {source_scripts_dir}"

    messages: list[str] = []

    # ===== STEP 1: copy hook scripts =====
    try:
        hooks_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return False, f"Could not create hooks dir {hooks_dir}: {exc}"

    copied, skipped, failed = _copy_scripts(
        source_scripts_dir,
        legacy_scripts_dir,
        hooks_dir,
        force=force,
    )

    if copied:
        messages.append(f"✅ Copied {len(copied)} hook script(s) to {hooks_dir}:")
        for name in copied:
            messages.append(f"   - {name}")
    if skipped:
        messages.append(
            f"\n⚠️  Skipped {len(skipped)} existing script(s) (use --force to overwrite):"
        )
        for name in skipped:
            messages.append(f"   - {name}")
    if failed:
        messages.append(f"\n❌ Failed to copy {len(failed)} script(s):")
        for line in failed:
            messages.append(f"   - {line}")

    # ===== STEP 2: merge into settings.json =====
    settings_merge_result = _merge_settings(
        target_path=target_path,
        source_hooks_json=source_hooks_json,
        force=force,
    )
    success_settings, settings_message, backup_path = settings_merge_result
    messages.append("")
    messages.append(settings_message)
    if backup_path is not None:
        messages.append(f"💾 Backup: {backup_path}")

    # ===== STEP 3: deploy seed data files (skip-if-exists, never overwrite) =====
    seed_copied, seed_skipped = _deploy_seed_files(
        hooks_source_root=_get_hooks_source_root(),
        dest_root=target_path.parent,
    )
    if seed_copied:
        messages.append("")
        messages.append(f"📦 Seeded {len(seed_copied)} data file(s):")
        for name in seed_copied:
            messages.append(f"   - {name}")
    if seed_skipped:
        messages.append("")
        messages.append(f"⏭️  Preserved {len(seed_skipped)} existing data file(s):")
        for name in seed_skipped:
            messages.append(f"   - {name} (user-edited; not overwritten)")

    # Overall success only if scripts AND settings merge both succeeded.
    overall = success_settings and not failed
    return overall, "\n".join(messages)


# ---------------------------------------------------------------------------
# Scripts
# ---------------------------------------------------------------------------


def _copy_scripts(
    freshness_dir: Path,
    legacy_dir: Path | None,
    dest: Path,
    *,
    force: bool,
) -> Tuple[list[str], list[str], list[str]]:
    copied: list[str] = []
    skipped: list[str] = []
    failed: list[str] = []

    # Build (source_path, dest_name) list
    sources: list[Tuple[Path, str]] = []
    for name in _FRESHNESS_SCRIPTS:
        sources.append((freshness_dir / name, name))
    if legacy_dir is not None:
        for name in _LEGACY_SCRIPTS:
            src = legacy_dir / name
            if src.exists():
                sources.append((src, name))

    for src, dest_name in sources:
        dest_file = dest / dest_name

        if not src.exists():
            failed.append(f"{dest_name}: source missing at {src}")
            continue

        if dest_file.exists() and not force:
            skipped.append(dest_name)
            continue

        try:
            shutil.copy2(src, dest_file)
            os.chmod(dest_file, 0o755)
            copied.append(dest_name)
        except OSError as exc:
            failed.append(f"{dest_name}: {exc}")

    return copied, skipped, failed


# ---------------------------------------------------------------------------
# settings.json merge
# ---------------------------------------------------------------------------


def _merge_settings(
    *,
    target_path: Path,
    source_hooks_json: Path,
    force: bool,
) -> Tuple[bool, str, Path | None]:
    # Read source registrations.
    try:
        source = json.loads(source_hooks_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return (
            False,
            f"❌ Source hooks.json malformed at {source_hooks_json}: {exc}",
            None,
        )
    source_hooks = source.get("hooks", {})
    if not isinstance(source_hooks, dict):
        return (
            False,
            f"❌ Source hooks.json has non-object 'hooks' key: {type(source_hooks).__name__}",
            None,
        )

    # Ensure target dir exists.
    try:
        target_path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return (
            False,
            f"❌ Could not create target dir {target_path.parent}: {exc}",
            None,
        )

    backup_path: Path | None = None

    if target_path.exists():
        # Backup BEFORE any write — preserves user's pre-install state.
        backup_path = _backup_path(target_path)
        try:
            shutil.copy2(target_path, backup_path)
        except OSError as exc:
            return (
                False,
                f"❌ Could not back up existing settings.json to {backup_path}: {exc}",
                None,
            )

        try:
            existing = json.loads(target_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return (
                False,
                (
                    f"❌ Target settings.json is malformed; refusing to write. "
                    f"Backup at {backup_path}. Parse error: {exc}"
                ),
                backup_path,
            )
        if not isinstance(existing, dict):
            return (
                False,
                (
                    f"❌ Target settings.json is not a JSON object; refusing to write. "
                    f"Backup at {backup_path}."
                ),
                backup_path,
            )
    else:
        existing = {}

    existing_hooks = existing.get("hooks") or {}
    if not isinstance(existing_hooks, dict):
        return (
            False,
            f"❌ Target settings.json 'hooks' key has non-object type "
            f"({type(existing_hooks).__name__}); refusing to write.",
            backup_path,
        )

    added = 0
    skipped_collision = 0
    replaced = 0

    for event, registrations in source_hooks.items():
        if not isinstance(registrations, list):
            continue
        event_list = existing_hooks.setdefault(event, [])
        if not isinstance(event_list, list):
            return (
                False,
                (
                    f"❌ Target settings.json hooks.{event} is not a list "
                    f"({type(event_list).__name__}); refusing to write."
                ),
                backup_path,
            )

        # Snapshot the matchers that existed in the target BEFORE this merge.
        # Collisions are user-vs-source, not source-vs-source: two of our own
        # registrations with the same matcher (e.g., the SessionStart pair —
        # session-init.sh + freshness-session-start.sh, both implicit/explicit
        # `*` matcher) must BOTH land.
        original_target_matchers = {
            r.get("matcher", "*") for r in event_list if isinstance(r, dict)
        }
        # Also track exact (matcher, command-list) tuples that already exist
        # so a true duplicate (same matcher + same exact inner commands) is
        # always treated as a collision regardless of source-vs-source distinction.
        original_target_signatures = {
            _registration_signature(r) for r in event_list if isinstance(r, dict)
        }

        for new_reg in registrations:
            if not isinstance(new_reg, dict):
                continue
            new_matcher = new_reg.get("matcher", "*")
            new_signature = _registration_signature(new_reg)

            # Exact-duplicate check: same matcher AND same inner commands →
            # always a collision (no work to do).
            if new_signature in original_target_signatures:
                if force:
                    # Find and replace the first matching original.
                    for idx, existing_reg in enumerate(event_list):
                        if (
                            isinstance(existing_reg, dict)
                            and _registration_signature(existing_reg) == new_signature
                        ):
                            event_list[idx] = new_reg
                            replaced += 1
                            break
                else:
                    skipped_collision += 1
                continue

            # Matcher-only collision against ORIGINAL target (user-vs-source):
            # only counts when the user had this matcher pre-merge.
            if new_matcher in original_target_matchers:
                # Find the original registration with this matcher
                collision_idx = None
                for idx, existing_reg in enumerate(event_list):
                    if (
                        isinstance(existing_reg, dict)
                        and existing_reg.get("matcher", "*") == new_matcher
                        and _registration_signature(existing_reg)
                        in original_target_signatures
                    ):
                        collision_idx = idx
                        break

                if collision_idx is not None:
                    if force:
                        event_list[collision_idx] = new_reg
                        replaced += 1
                    else:
                        skipped_collision += 1
                    continue

            # No collision with original target → append (even if it shares a
            # matcher with a sibling we already added from this same source list).
            event_list.append(new_reg)
            added += 1

    existing["hooks"] = existing_hooks

    # Atomic write: tempfile in same dir + os.replace.
    try:
        _atomic_write_json(target_path, existing)
    except OSError as exc:
        return (
            False,
            f"❌ Atomic write to {target_path} failed: {exc}",
            backup_path,
        )

    summary_parts = [f"📋 settings.json merge: events={len(source_hooks)}"]
    summary_parts.append(f"added={added}")
    if replaced:
        summary_parts.append(f"replaced={replaced}")
    if skipped_collision:
        summary_parts.append(
            f"skipped-collision={skipped_collision} (use --force to replace)"
        )
    return True, " ".join(summary_parts), backup_path


def _registration_signature(reg: dict) -> tuple:
    """
    Build a hashable signature for a hook registration: (matcher, tuple-of-commands).
    Used to detect exact duplicates regardless of object identity.
    """
    matcher = reg.get("matcher", "*")
    inner = reg.get("hooks", [])
    if not isinstance(inner, list):
        return (matcher, ())
    commands = tuple(h.get("command", "") for h in inner if isinstance(h, dict))
    return (matcher, commands)


def _atomic_write_json(target: Path, payload: dict) -> None:
    """Write `payload` to `target` atomically via tempfile + os.replace."""
    parent = target.parent
    # Use a deterministic-prefix temp name in the same directory so os.replace
    # is a same-filesystem operation (atomic on POSIX).
    tmp = parent / f".{target.name}.tmp.{os.getpid()}"
    try:
        tmp.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        os.replace(tmp, target)
    finally:
        # If os.replace succeeded, tmp no longer exists (rename). If it
        # failed, clean up.
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:
                pass


def _backup_path(target: Path) -> Path:
    # ISO-8601 with no colons (colons are problematic on some filesystems).
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return target.with_suffix(target.suffix + f".bak.{stamp}")


# ---------------------------------------------------------------------------
# Source-path resolution
# ---------------------------------------------------------------------------


def _get_hooks_source() -> Path:
    """Locate the canonical hooks.json. Same convention as install_core."""
    package_root = Path(__file__).resolve().parent.parent
    package_hooks = package_root / "hooks" / "hooks.json"
    return package_hooks


def _get_hooks_scripts_source() -> Path:
    """Locate src/superclaude/hooks/scripts/ in the package or checkout."""
    package_root = Path(__file__).resolve().parent.parent
    return package_root / "hooks" / "scripts"


def _get_hooks_source_root() -> Path:
    """Locate src/superclaude/hooks/ (parent of scripts/ and home of seed data files)."""
    package_root = Path(__file__).resolve().parent.parent
    return package_root / "hooks"


def _deploy_seed_files(
    *, hooks_source_root: Path, dest_root: Path
) -> Tuple[list[str], list[str]]:
    """
    Deploy seed data files from src/superclaude/hooks/<src_name> to dest_root/<dest_name>.

    Skip-if-exists semantics: never overwrites an existing destination, even when
    install_hooks(force=True). This preserves user customizations to data files
    like auggie-projects.txt across re-installs.

    Best-effort on OSError: a missed seed deploy must not fail the broader install.
    Hooks degrade gracefully when seed data is absent.

    Returns (copied, skipped) lists of destination names.
    """
    copied: list[str] = []
    skipped: list[str] = []
    for src_name, dest_name in _SEED_FILES:
        src = hooks_source_root / src_name
        dest = dest_root / dest_name
        if not src.exists():
            continue
        if dest.exists():
            skipped.append(dest_name)
            continue
        try:
            shutil.copy2(src, dest)
            copied.append(dest_name)
        except OSError:
            # Intentionally silent — telemetry path is per-hook, not per-install.
            pass
    return copied, skipped


def _get_legacy_scripts_source() -> Path | None:
    """Locate src/superclaude/scripts/ for the pre-existing session-init.sh."""
    package_root = Path(__file__).resolve().parent.parent
    candidate = package_root / "scripts"
    if candidate.exists():
        return candidate
    return None


_SESSION_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")


def validate_session_id(session_id: str) -> bool:
    """
    Validate a session_id is filesystem-safe (used by hook scripts to interpolate
    into ~/.claude/state/<bucket>/<session_id>.txt paths).

    This is a defense-in-depth helper exposed for hook-author convenience; the
    hooks themselves do not currently sanitize. Phase 4 follow-up F7 in
    CP-P02-END.md tracks adding this to the hook bodies if needed.
    """
    return bool(_SESSION_ID_PATTERN.match(session_id or ""))
