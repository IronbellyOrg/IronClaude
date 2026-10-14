"""sc-recommend lookup-cache reader/writer.

YAML adaptation of ``roadmap/convergence.py::DeviationRegistry`` (atomic
``tmp + os.replace`` write, hash-reset-on-mismatch load) swapping the JSON codec
for ``yaml.safe_dump``/``yaml.safe_load`` and the ``spec_hash`` reset key for
``surface_hash``. The atomic writer uses a randomized same-directory temp name
(per ``install_hooks._atomic_write_json``) with a ``finally`` cleanup so a crash
mid-``os.replace`` never leaves a partial target or a stray temp file
(spec Risk #12 worktree-concurrency mitigation).

Schema (schema_version 2): top-level ``surface_hash``/``generated``/``generator``
plus a ``rows`` list scanned by ``key``. ``sort_keys=False`` is non-negotiable --
it preserves the authored per-row field order.
"""

from __future__ import annotations

import hashlib
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)

SCHEMA_VERSION = 2
GENERATOR = "sc-recommend-cache/v0.2"

# Glob patterns whose sorted output defines the live command/skill/agent surface.
_SURFACE_GLOBS = ("commands/*.md", "skills/*/SKILL.md", "agents/*.md")
_SURFACE_BASE = Path("src/superclaude")
_GUIDE_RELPATH = Path("core") / "HOW-WE-WORK.md"
# Installed and project locations the skill also searches (spec 3.2):
# ~/.claude/{commands/sc,skills,agents} and the project's .claude/{commands,skills,agents}.
_INSTALLED_GLOBS = (
    "commands/sc/*.md",
    "commands/*.md",
    "skills/*/SKILL.md",
    "agents/*.md",
)


def _default_installed_roots() -> tuple[Path, ...]:
    return (Path.home() / ".claude", Path(".claude"))


class _IndentDumper(yaml.SafeDumper):
    """SafeDumper that indents block sequences under their key (yamllint-conformant).

    PyYAML's default places a block sequence's ``-`` at the parent key's indent,
    which the repo yamllint config (``indent-sequences: true``) rejects. Overriding
    ``increase_indent`` to never go indentless emits ``key:\\n  - item`` instead of
    ``key:\\n- item``. Behavior is unchanged (``safe_load`` reads either form); only
    the emitted indentation conforms to the project style.
    """

    def increase_indent(self, flow=False, indentless=False):  # noqa: N802 (PyYAML API)
        return super().increase_indent(flow, False)


def compute_surface_hash(
    base: Path = _SURFACE_BASE,
    guide_path: Path | None = None,
    installed_roots: tuple[Path, ...] | None = None,
) -> str:
    """Return the full sha256 hexdigest of the live surface plus the routing guide.

    surface_hash = SHA256(sorted(Glob(
        'src/superclaude/{commands/*.md,skills/*/SKILL.md,agents/*.md}'
    )) + ["guide:<sha256 of core/HOW-WE-WORK.md bytes, or 'absent'>"]).
    Path additions, renames and deletions change the digest, and so does any
    edit to the routing guide. ``guide_path`` overrides the guide location
    (default: ``base / core / HOW-WE-WORK.md``; never the user's home).
    ``installed_roots`` lists the installed and project ``.claude`` folders whose
    command, skill and agent paths are also hashed (default: ``~/.claude`` and
    ``./.claude``), so installing or removing a command invalidates old answers.
    Full digest -- NOT truncated.
    """
    matches: list[str] = []
    for pattern in _SURFACE_GLOBS:
        matches.extend(p.as_posix() for p in base.glob(pattern))
    roots = _default_installed_roots() if installed_roots is None else installed_roots
    for root in roots:
        for pattern in _INSTALLED_GLOBS:
            matches.extend(f"installed:{p.as_posix()}" for p in root.glob(pattern))
    guide = guide_path if guide_path is not None else base / _GUIDE_RELPATH
    try:
        guide_digest = hashlib.sha256(guide.read_bytes()).hexdigest()
    except OSError:
        guide_digest = "absent"
    joined = "\n".join(sorted(matches) + [f"guide:{guide_digest}"])
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()


def compute_source_hash(path_bytes: bytes) -> str:
    """Return the full sha256 hexdigest (64 hex chars) of a candidate source file's bytes.

    Used for the hot-path per-row ``source_hash`` validation Read. Full digest --
    NOT truncated (content-integrity hashes are never shortened).
    """
    return hashlib.sha256(path_bytes).hexdigest()


@dataclass
class LookupCache:
    """In-memory view of the lookup-cache YAML with atomic persistence."""

    path: Path
    surface_hash: str
    rows: list[dict] = field(default_factory=list)
    generated: str | None = None
    generator: str = GENERATOR
    schema_version: int = SCHEMA_VERSION

    @classmethod
    def load_or_create(cls, path: Path, surface_hash: str) -> LookupCache:
        """Load the cache at ``path`` or create a fresh one.

        If the stored ``surface_hash`` differs from the current one, the rows are
        DISCARDED (the live surface changed -- additions/renames/deletions). A
        corrupted YAML body logs a warning and falls through to a fresh cache.
        """
        if path.exists():
            try:
                data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
                if data.get("surface_hash") == surface_hash:
                    return cls(
                        path=path,
                        surface_hash=surface_hash,
                        rows=data.get("rows", []),
                        generated=data.get("generated"),
                        generator=data.get("generator", GENERATOR),
                        schema_version=data.get("schema_version", SCHEMA_VERSION),
                    )
                logger.info("Surface hash changed; resetting lookup cache rows")
            except yaml.YAMLError:
                logger.warning("Corrupted lookup cache at %s; creating fresh", path)
        return cls(path=path, surface_hash=surface_hash, rows=[])

    def get_row(self, key: str) -> dict | None:
        """Return the row whose ``key == key`` (linear scan), or None."""
        for row in self.rows:
            if row.get("key") == key:
                return row
        return None

    def upsert_row(self, row: dict) -> None:
        """Insert ``row`` or replace the existing row with the same ``key``."""
        key = row.get("key")
        for idx, existing in enumerate(self.rows):
            if existing.get("key") == key:
                self.rows[idx] = row
                return
        self.rows.append(row)

    def save(self) -> None:
        """Atomically write the cache to ``self.path`` (randomized tmp + os.replace).

        ``sort_keys=False`` preserves the authored row-field order;
        ``default_flow_style=False`` keeps block style for multi-line templates;
        ``allow_unicode=True`` keeps prose fields readable. A ``finally`` block
        removes the temp file if ``os.replace`` never ran (crash safety).
        """
        self.generated = datetime.now(timezone.utc).isoformat()
        data = {
            "schema_version": self.schema_version,
            "surface_hash": self.surface_hash,
            "generated": self.generated,
            "generator": self.generator,
            "rows": self.rows,
        }
        parent = self.path.parent
        parent.mkdir(parents=True, exist_ok=True)
        # Randomized same-directory temp name bounds the worktree-concurrency
        # last-write-wins window (spec Risk #12) and keeps os.replace atomic.
        tmp = parent / f".{self.path.name}.tmp.{os.getpid()}.{id(self)}"
        try:
            tmp.write_text(
                yaml.dump(
                    data,
                    Dumper=_IndentDumper,
                    sort_keys=False,
                    default_flow_style=False,
                    allow_unicode=True,
                ),
                encoding="utf-8",
            )
            os.replace(tmp, self.path)
        finally:
            if tmp.exists():
                try:
                    tmp.unlink()
                except OSError:
                    pass
