"""Sprint checkpoint utilities — shared module for parsing, verifying, and
managing `Checkpoint Report Path:` entries declared in phase tasklists.

Used by the per-phase verification gate (Wave 2), the post-sprint manifest
(Wave 3), and the auto-recovery tool (Wave 3). Keeping everything in one
module prevents the consumers from drifting.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from .models import CheckpointEntry

# Matches `Checkpoint Report Path: <path>`. Tolerates markdown-bold wrapping
# of the label (``**Checkpoint Report Path:**``) and optional surrounding
# backticks around the path. Case-insensitive. Captures the raw path string
# as declared in the tasklist (bolding/backticks stripped).
CHECKPOINT_PATH_PATTERN: re.Pattern[str] = re.compile(
    r"Checkpoint\s+Report\s+Path:\s*\*{0,2}\s*`?([^\s`\n*]+)`?",
    re.IGNORECASE,
)

# Matches `### Checkpoint: <name>` headings. The trailing name becomes the
# human-readable label for the checkpoint (e.g. "End of Phase 3").
CHECKPOINT_HEADING_PATTERN: re.Pattern[str] = re.compile(
    r"^#{2,5}\s*Checkpoint:\s*(.+?)\s*$",
    re.MULTILINE | re.IGNORECASE,
)


def extract_checkpoint_paths(
    phase_file: Path,
    release_dir: Path,
) -> list[tuple[str, Path]]:
    """Return the list of (name, expected_path) checkpoints declared in a phase.

    Parses every ``Checkpoint Report Path:`` line from ``phase_file``. Each
    checkpoint's *name* is derived from the nearest preceding
    ``### Checkpoint: <name>`` heading when one exists; otherwise the basename
    of the declared path is used. Relative paths are resolved against
    ``release_dir`` (the sprint's work dir) so the returned path is always an
    absolute ``Path`` suitable for existence checks.

    Returns an empty list if the phase file cannot be read or if no checkpoint
    declarations are present.
    """
    try:
        content = phase_file.read_text(errors="replace")
    except OSError:
        return []

    # Build a sorted list of checkpoint headings with their byte offsets so we
    # can pair each path declaration with the closest preceding heading.
    headings: list[tuple[int, str]] = [
        (m.start(), m.group(1).strip())
        for m in CHECKPOINT_HEADING_PATTERN.finditer(content)
    ]

    results: list[tuple[str, Path]] = []
    for match in CHECKPOINT_PATH_PATTERN.finditer(content):
        raw_path = match.group(1).strip()
        if not raw_path:
            continue

        name = _nearest_heading(headings, match.start())
        if not name:
            name = Path(raw_path).name

        candidate = Path(raw_path)
        if candidate.is_absolute():
            resolved = candidate
        elif candidate.exists():
            # Accept a relative path as-is when it already resolves (repo-root
            # invocations), matching how sprint agents write checkpoint files.
            resolved = candidate.resolve()
        else:
            resolved = (release_dir / candidate).resolve()

        results.append((name, resolved))

    return results


def verify_checkpoint_files(
    paths: list[tuple[str, Path]],
) -> list[tuple[str, Path, bool]]:
    """Return (name, path, exists) for each declared checkpoint.

    The input is the output of :func:`extract_checkpoint_paths`. Order is
    preserved so callers can correlate tuples positionally.
    """
    results: list[tuple[str, Path, bool]] = []
    for name, path in paths:
        try:
            exists = path.is_file()
        except OSError:
            exists = False
        results.append((name, path, exists))
    return results


def _nearest_heading(headings: list[tuple[int, str]], offset: int) -> str:
    """Return the name of the last heading whose start is <= offset.

    Returns an empty string if no heading precedes the offset.
    """
    best = ""
    for start, name in headings:
        if start <= offset:
            best = name
        else:
            break
    return best


# ---------------------------------------------------------------------------
# Wave 3 — manifest + auto-recovery
# ---------------------------------------------------------------------------


def build_manifest(
    tasklist_index: Path,
    release_dir: Path,
) -> list[CheckpointEntry]:
    """Walk every phase tasklist and return the sprint's checkpoint manifest.

    Uses the canonical ``discover_phases`` helper so the manifest sees the
    same phases the executor does. Each declared checkpoint becomes one
    :class:`CheckpointEntry` with ``exists`` populated by an on-disk check.

    Returns an empty list if the index is unreadable or no phases are found.
    """
    # Local import: ``config`` imports from this module path indirectly via
    # ``models`` → avoid cycles at module import time.
    from .config import discover_phases

    try:
        phases = discover_phases(tasklist_index)
    except Exception:  # noqa: BLE001
        return []

    entries: list[CheckpointEntry] = []
    for phase in phases:
        for name, expected_path in extract_checkpoint_paths(
            phase.file, release_dir
        ):
            entries.append(
                CheckpointEntry(
                    phase=phase.number,
                    name=name,
                    expected_path=expected_path,
                    exists=expected_path.is_file(),
                )
            )
    return entries


def write_manifest(entries: list[CheckpointEntry], output_path: Path) -> None:
    """Serialise the manifest to JSON at ``output_path``.

    The JSON payload contains a ``summary`` object (counts) and an
    ``entries`` list (one object per checkpoint). Paths are emitted as
    strings. Written atomically via a temp-file + replace so a partial
    write cannot corrupt an existing manifest.
    """
    total = len(entries)
    found = sum(1 for e in entries if e.exists)
    recovered = sum(1 for e in entries if e.recovered)
    missing = total - found

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total": total,
            "found": found,
            "missing": missing,
            "recovered": recovered,
        },
        "entries": [
            {
                "phase": e.phase,
                "name": e.name,
                "expected_path": str(e.expected_path),
                "exists": e.exists,
                "recovered": e.recovered,
                "recovery_source": e.recovery_source,
            }
            for e in entries
        ],
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = output_path.with_suffix(output_path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2) + "\n")
    tmp.replace(output_path)


def recover_missing_checkpoints(
    manifest: list[CheckpointEntry],
    artifacts_dir: Path,
    phase_tasklists: dict[int, Path],
) -> list[CheckpointEntry]:
    """Regenerate missing checkpoint reports from evidence files.

    For every entry in ``manifest`` with ``exists == False`` that also has no
    file at its ``expected_path`` yet, write a placeholder checkpoint report
    containing:

    - A prominent ``## Note: Auto-Recovered`` banner.
    - Frontmatter with ``recovered: true`` and ``source:`` metadata.
    - The verification criteria copied verbatim from the phase tasklist's
      matching ``### Checkpoint:`` section (if found).
    - A list of evidence artifacts discovered under ``artifacts_dir`` whose
      paths reference the phase number in their deliverable id.

    The function is idempotent: if the expected file already exists on disk
    (whether written by the agent, by a prior recovery run, or otherwise),
    the entry is returned unchanged. Returns a NEW list — the input
    ``manifest`` is not mutated.

    ``phase_tasklists`` maps phase number → phase tasklist path; entries
    whose phase is absent from the map are skipped (cannot be recovered).
    """
    out: list[CheckpointEntry] = []
    for entry in manifest:
        # Refresh existence — a previous iteration may have written the file.
        if entry.expected_path.is_file():
            out.append(
                CheckpointEntry(
                    phase=entry.phase,
                    name=entry.name,
                    expected_path=entry.expected_path,
                    exists=True,
                    recovered=entry.recovered,
                    recovery_source=entry.recovery_source,
                )
            )
            continue

        if entry.exists or entry.phase not in phase_tasklists:
            out.append(entry)
            continue

        tasklist_path = phase_tasklists[entry.phase]
        verification_block = _extract_verification_block(tasklist_path, entry.name)
        evidence = _discover_phase_artifacts(artifacts_dir, entry.phase)

        report = _render_recovered_checkpoint(
            entry=entry,
            verification_block=verification_block,
            evidence=evidence,
        )

        entry.expected_path.parent.mkdir(parents=True, exist_ok=True)
        entry.expected_path.write_text(report)

        recovery_source = (
            ", ".join(
                str(p.relative_to(artifacts_dir.parent))
                if p.is_relative_to(artifacts_dir.parent)
                else str(p)
                for p in evidence
            )
            if evidence
            else "(no artifacts discovered)"
        )

        out.append(
            CheckpointEntry(
                phase=entry.phase,
                name=entry.name,
                expected_path=entry.expected_path,
                exists=True,
                recovered=True,
                recovery_source=recovery_source,
            )
        )

    return out


def _extract_verification_block(tasklist_path: Path, checkpoint_name: str) -> str:
    """Return the verification body for a named checkpoint in a tasklist.

    Locates the ``### Checkpoint: <name>`` heading and returns everything up
    to the next top-level or peer heading. Empty string when the heading is
    not found (e.g. name came from a basename fallback).
    """
    try:
        content = tasklist_path.read_text(errors="replace")
    except OSError:
        return ""

    lines = content.splitlines()
    start: int | None = None
    heading_level = 0
    for i, line in enumerate(lines):
        match = re.match(r"^(#{2,5})\s*Checkpoint:\s*(.+?)\s*$", line, re.IGNORECASE)
        if match and match.group(2).strip() == checkpoint_name:
            heading_level = len(match.group(1))
            start = i + 1
            break
    if start is None:
        return ""

    end = len(lines)
    for j in range(start, len(lines)):
        stripped = lines[j].lstrip()
        if stripped.startswith("#"):
            # Count leading '#'s.
            level = len(stripped) - len(stripped.lstrip("#"))
            if level <= heading_level:
                end = j
                break
    return "\n".join(lines[start:end]).strip()


def _discover_phase_artifacts(artifacts_dir: Path, phase_number: int) -> list[Path]:
    """Return evidence artifacts that belong to the given phase.

    Two heuristics, unioned:

    1. Directory names referencing the phase (``D-####`` entries whose
       containing path mentions ``phase-N``).
    2. Markdown files whose text contains ``T<phase_number:02d>.\\d{2}`` task
       identifiers.

    Missing artifacts directory returns an empty list.
    """
    if not artifacts_dir.exists():
        return []

    task_pattern = re.compile(rf"\bT{phase_number:02d}\.\d{{2}}\b", re.IGNORECASE)
    matches: set[Path] = set()
    for path in artifacts_dir.rglob("*"):
        if not path.is_file():
            continue
        parts = {p.lower() for p in path.parts}
        if f"phase-{phase_number}" in parts:
            matches.add(path)
            continue
        if path.suffix.lower() in {".md", ".txt"}:
            try:
                if task_pattern.search(path.read_text(errors="replace")):
                    matches.add(path)
            except OSError:
                continue
    return sorted(matches)


def _render_recovered_checkpoint(
    *,
    entry: CheckpointEntry,
    verification_block: str,
    evidence: list[Path],
) -> str:
    """Build the body of an auto-recovered checkpoint report."""
    timestamp = datetime.now(timezone.utc).isoformat()
    evidence_lines = (
        "\n".join(f"- `{p}`" for p in evidence)
        if evidence
        else "- _(no matching artifacts discovered under artifacts_dir)_"
    )
    verification_section = (
        verification_block
        or "_(no verification block found in the originating tasklist)_"
    )
    return (
        "---\n"
        f"checkpoint: {entry.name}\n"
        f"phase: {entry.phase}\n"
        "recovered: true\n"
        f"generated_at: {timestamp}\n"
        "---\n\n"
        "## Note: Auto-Recovered\n\n"
        "This checkpoint report was **not** written by the sprint agent at the\n"
        "time the phase completed. It has been reconstructed retroactively by\n"
        "`recover_missing_checkpoints()` from the artifacts produced during\n"
        "the phase. Treat the status below as provisional — the original\n"
        "real-time verification did not occur.\n\n"
        f"## Checkpoint: {entry.name}\n\n"
        f"- **Phase:** {entry.phase}\n"
        f"- **Expected report path:** `{entry.expected_path}`\n\n"
        "## Verification Criteria (copied from tasklist)\n\n"
        f"{verification_section}\n\n"
        "## Evidence Artifacts Used for Recovery\n\n"
        f"{evidence_lines}\n\n"
        "## Result\n\n"
        "`UNKNOWN` — recovered without live verification. Re-run the phase or\n"
        "manually inspect the evidence artifacts listed above to confirm the\n"
        "acceptance criteria were met.\n"
    )
