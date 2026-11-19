"""Helpers for installers that keep or overwrite files a user may have edited.

``install`` keeps an existing file, so a kept file that differs from this
version's copy is stale or customized and should be named in the report.
``install --force`` and ``update`` overwrite, so a differing file is saved
next to itself first (``<name>.bak.<UTC stamp>``, which Claude Code does not
load) and the overwrite is skipped when that save fails.
"""

from __future__ import annotations

import filecmp
import shutil
from datetime import datetime, timezone
from pathlib import Path


def same_content(a: Path, b: Path) -> bool:
    """True only when both files are readable and byte-identical."""
    try:
        return filecmp.cmp(a, b, shallow=False)
    except OSError:
        return False


def _backup_target(target: Path) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    candidate = target.with_name(f"{target.name}.bak.{stamp}")
    n = 1
    while candidate.exists():
        n += 1
        candidate = target.with_name(f"{target.name}.bak.{stamp}-{n}")
    return candidate


def backup_if_differs(shipped: Path, target: Path) -> Path | None:
    """Copy ``target`` aside when it differs from ``shipped``; return the copy.

    Returns ``None`` when the files already match. Raises ``OSError`` when the
    copy cannot be made; the caller must then leave ``target`` untouched.
    """
    if same_content(shipped, target):
        return None
    backup = _backup_target(target)
    shutil.copy2(target, backup)
    return backup
