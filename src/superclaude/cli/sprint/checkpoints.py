"""Sprint checkpoint utilities — shared module for parsing and verifying
`Checkpoint Report Path:` entries declared in phase tasklists.

Used by both the per-phase verification gate (Wave 2) and the post-sprint
manifest (Wave 3). Keeping the parsing logic in a single module prevents
the two consumers from drifting.
"""

from __future__ import annotations

import re
from pathlib import Path

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
