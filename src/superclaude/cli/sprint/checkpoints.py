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
from typing import TYPE_CHECKING

from .models import CheckpointEntry

if TYPE_CHECKING:
    from .recovery import RecoveryBundle

# Matches `Checkpoint Report Path: <path>`. Tolerates markdown-bold wrapping
# of the label (``**Checkpoint Report Path:**``) and optional surrounding
# backticks around the path. Case-insensitive. Captures the raw path string
# as declared in the tasklist (bolding/backticks stripped).
CHECKPOINT_PATH_PATTERN: re.Pattern[str] = re.compile(
    r"Checkpoint\s+Report\s+Path:\s*\*{0,2}\s*`?([^\s`\n*]+)`?",
    re.IGNORECASE,
)

# Matches `### Checkpoint: <name>` (legacy) and
# `### T<PP>.<NN> -- Checkpoint: <name>` (Wave-4, emitted by `/sc:tasklist`).
# The trailing name becomes the human-readable label (e.g. "End of Phase 3").
CHECKPOINT_HEADING_PATTERN: re.Pattern[str] = re.compile(
    r"^#{2,5}\s*(?:T\d{2}\.\d{2}\s*--\s*)?Checkpoint:\s*(.+?)\s*$",
    re.MULTILINE | re.IGNORECASE,
)


def _resolve_checkpoint_path(release_dir: Path, raw_path: str) -> Path:
    """Resolve a declared checkpoint path against ``release_dir``, idempotently.

    Declared ``Checkpoint Report Path:`` values come in three shapes:

    * **absolute** — used verbatim.
    * **release-relative** (``checkpoints/CP.md``) — joined onto ``release_dir``.
    * **release-prefixed** (``.dev/<release>/bundle/checkpoints/CP.md``) — the
      path already carries ``release_dir``'s own trailing components, so a naive
      ``release_dir / candidate`` would duplicate that prefix (the path-doubling
      defect). We strip the longest leading run of ``candidate`` that matches
      ``release_dir``'s trailing components before joining, which makes the join
      idempotent: a release-prefixed path resolves to the same location whether
      or not it was prefixed.

    Resolution is purely lexical — it does **not** probe the cwd or the
    filesystem — so the result is deterministic regardless of the process
    working directory or whether the target file exists yet. (The previous
    implementation branched on ``candidate.exists()``, which made a
    release-prefixed path resolve correctly only when its target already
    existed, doubling the prefix otherwise.)
    """
    candidate = Path(raw_path)
    if candidate.is_absolute():
        return candidate

    rd_parts = release_dir.parts
    cand_parts = candidate.parts
    # Longest k where release_dir's last k parts == candidate's first k parts.
    overlap = 0
    for k in range(min(len(rd_parts), len(cand_parts)), 0, -1):
        if rd_parts[-k:] == cand_parts[:k]:
            overlap = k
            break

    remainder = cand_parts[overlap:]
    if not remainder:
        return release_dir.resolve()
    return (release_dir / Path(*remainder)).resolve()


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

        # Strip the `TASKLIST_ROOT/` placeholder prefix that phase tasklists
        # emit as a portable, release-dir-agnostic anchor. The actual release
        # root is `release_dir`; treat the remainder as release-relative.
        if raw_path.startswith("TASKLIST_ROOT/"):
            raw_path = raw_path[len("TASKLIST_ROOT/") :]
        elif raw_path == "TASKLIST_ROOT":
            raw_path = "."

        name = _nearest_heading(headings, match.start())
        if not name:
            name = Path(raw_path).name

        resolved = _resolve_checkpoint_path(release_dir, raw_path)
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
        for name, expected_path in extract_checkpoint_paths(phase.file, release_dir):
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


# Verdict tokens a checkpoint report may carry (consistent with the
# PASS|FAIL|...|BLOCKED|SKIP matcher used by summarizer.py).
_CHECKPOINT_VERDICT_RE = re.compile(
    r"\b(PASS|FAIL|BLOCKED|SKIP|UNKNOWN)\b", re.IGNORECASE
)


def _parse_checkpoint_verdict(path: Path) -> str | None:
    """Best-effort: read the current verdict token from an EXISTING checkpoint
    report. Inspects a ``status:``/``verdict:`` frontmatter key first (only
    within the leading ``---`` fenced block), then the ``## Result`` body
    section. Returns the uppercased token (e.g. ``"FAIL"``) or ``None`` when no
    verdict can be read. Used by the Fix-2 stale-verdict re-evaluation path —
    the recovered-report template itself writes no ``status:`` frontmatter key,
    so a stale FAIL/BLOCKED can only have been written by an agent.
    """
    try:
        content = path.read_text(errors="replace")
    except OSError:
        return None
    lines = content.splitlines()
    # Frontmatter block (between the first two --- fences).
    if lines and lines[0].strip() == "---":
        for line in lines[1:]:
            if line.strip() == "---":
                break
            key_match = re.match(
                r"\s*(?:status|verdict)\s*:\s*(.+?)\s*$", line, re.IGNORECASE
            )
            if key_match:
                token = _CHECKPOINT_VERDICT_RE.search(key_match.group(1))
                if token:
                    return token.group(1).upper()
    # ## Result body token (the form recovered reports and many agents use).
    result_idx = content.find("## Result")
    if result_idx != -1:
        token = _CHECKPOINT_VERDICT_RE.search(content[result_idx:])
        if token:
            return token.group(1).upper()
    return None


def recover_missing_checkpoints(
    manifest: list[CheckpointEntry],
    artifacts_dir: Path,
    phase_tasklists: dict[int, Path],
    *,
    return_bundle: bool = False,
    reevaluate_stale: bool = False,
) -> list[CheckpointEntry] | RecoveryBundle:
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

    When ``return_bundle`` is True, the recovered manifest is wrapped in a
    :class:`~superclaude.cli.sprint.recovery.RecoveryBundle` for the v4.4.0
    unified recovery surface; otherwise the list of ``CheckpointEntry`` is
    returned unchanged (byte-identical to v4.2.x behavior).

    ``reevaluate_stale`` (Fix-2 FALLBACK; default False ⇒ behavior unchanged):
    when True, an EXISTING checkpoint file whose current verdict is FAIL or
    BLOCKED is re-stamped to ``UNKNOWN``/Auto-Recovered (via the same recovered
    report template) IFF the phase's gating tasks have recovered — determined
    from freshly-discovered evidence under ``artifacts_dir`` for that phase. It
    is NEVER auto-stamped PASS (the UNKNOWN-not-PASS hard constraint). When the
    gating tasks have not recovered (no fresh evidence), the stale FAIL/BLOCKED
    verdict is preserved unchanged. With ``reevaluate_stale=False`` the existing
    idempotent no-op (existing file returned unchanged) is byte-identical.
    """
    out: list[CheckpointEntry] = []
    for entry in manifest:
        # Refresh existence — a previous iteration may have written the file.
        if entry.expected_path.is_file():
            # Fix-2 FALLBACK: optionally re-evaluate an EXISTING stale verdict.
            # The default (reevaluate_stale=False) skips straight to the
            # historical idempotent no-op below (append unchanged + continue).
            if reevaluate_stale and entry.phase in phase_tasklists:
                stale_verdict = _parse_checkpoint_verdict(entry.expected_path)
                if stale_verdict in ("FAIL", "BLOCKED"):
                    # "Now-passing" is the same evidence-to-phase association the
                    # recovery path uses: fresh evidence discovered under
                    # artifacts_dir for this phase ⇒ gating tasks recovered.
                    evidence = _discover_phase_artifacts(artifacts_dir, entry.phase)
                    if evidence:
                        # Re-stamp the stale FAIL/BLOCKED to UNKNOWN/Auto-Recovered
                        # (NEVER auto-PASS — the UNKNOWN-not-PASS hard constraint).
                        verification_block = _extract_verification_block(
                            phase_tasklists[entry.phase], entry.name
                        )
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
                            + f" (stale {stale_verdict} re-stamped to UNKNOWN)"
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
                        continue
                    # No fresh evidence ⇒ gating tasks did NOT recover: fall
                    # through and preserve the stale FAIL/BLOCKED verdict.
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

    if return_bundle:
        # v4.4.0 forward-compat: wrap the recovered manifest in a RecoveryBundle
        # for the unified recovery surface. Lazy import avoids the
        # recovery -> models -> checkpoints -> recovery cycle (researcher 2 §1.7).
        from .recovery import RecoveryBundle, RecoveryStatus

        all_recovered = all(e.exists for e in out)
        return RecoveryBundle(
            bundle_id=f"verify-checkpoints-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}",
            affected_phase=out[0].phase if out else 0,
            verb="verify-checkpoints",
            affected_tasks=[],
            artifacts_produced=[entry.expected_path for entry in out],
            artifacts_replaced={},
            source_tasklist_sha256="",
            end_tasklist_sha256=None,
            status=RecoveryStatus.SUCCESS if all_recovered else RecoveryStatus.PARTIAL,
            rerun_attempt=1,
        )

    return out


def _extract_verification_block(tasklist_path: Path, checkpoint_name: str) -> str:
    """Return the verification body for a named checkpoint in a tasklist.

    Locates the ``### Checkpoint: <name>`` heading (or the Wave-4
    ``### T<PP>.<NN> -- Checkpoint: <name>`` task form) and returns everything
    up to the next top-level or peer heading. Empty string when the heading
    is not found (e.g. name came from a basename fallback).
    """
    try:
        content = tasklist_path.read_text(errors="replace")
    except OSError:
        return ""

    lines = content.splitlines()
    start: int | None = None
    heading_level = 0
    for i, line in enumerate(lines):
        match = re.match(
            r"^(#{2,5})\s*(?:T\d{2}\.\d{2}\s*--\s*)?Checkpoint:\s*(.+?)\s*$",
            line,
            re.IGNORECASE,
        )
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


# Executor gate substrings (executor._check_checkpoint_pass does a case-insensitive
# substring match for these on the report body). A recovered/re-stamped report's
# verdict is ALWAYS UNKNOWN, but the renderer interpolates caller-supplied fields
# (entry.name, the tasklist verification block, evidence paths) verbatim — so a
# tasklist whose verification prose literally contains one of these tokens could
# make an UNKNOWN report read as PASS at the gate (the DEV-2 regression). This
# matcher neutralizes the exact gate substrings in interpolated text.
_GATE_PASS_TOKEN_RE = re.compile(r"(STATUS|\*\*RESULT\*\*):(\s*)PASS", re.IGNORECASE)


def _neutralize_gate_tokens(text: str) -> str:
    """Break the executor gate substrings ``STATUS: PASS`` / ``**RESULT**: PASS``
    (case-insensitive) by inserting a space before the colon, so the exact gate
    substring no longer survives in ``body.upper()`` while the text stays human
    readable (e.g. ``STATUS: PASS`` -> ``STATUS : PASS``). Idempotent: already
    neutralized text (with the space before the colon) no longer matches.
    """
    return _GATE_PASS_TOKEN_RE.sub(lambda m: f"{m.group(1)} :{m.group(2)}PASS", text)


def _render_recovered_checkpoint(
    *,
    entry: CheckpointEntry,
    verification_block: str,
    evidence: list[Path],
) -> str:
    """Build the body of an auto-recovered checkpoint report.

    All caller-supplied interpolated fields (``entry.name``, the verification
    block, evidence paths) are passed through :func:`_neutralize_gate_tokens` so
    a verbatim ``STATUS: PASS`` / ``**RESULT**: PASS`` in tasklist prose can never
    make this UNKNOWN report read as PASS at ``_check_checkpoint_pass`` (DEV-2).
    """
    timestamp = datetime.now(timezone.utc).isoformat()
    safe_name = _neutralize_gate_tokens(entry.name)
    evidence_lines = (
        "\n".join(f"- `{_neutralize_gate_tokens(str(p))}`" for p in evidence)
        if evidence
        else "- _(no matching artifacts discovered under artifacts_dir)_"
    )
    verification_section = _neutralize_gate_tokens(
        verification_block
        or "_(no verification block found in the originating tasklist)_"
    )
    body = (
        "---\n"
        f"checkpoint: {safe_name}\n"
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
        f"## Checkpoint: {safe_name}\n\n"
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
    # Belt-and-suspenders: guarantee the assembled body carries neither gate
    # token regardless of how any field was constructed (idempotent re-pass).
    return _neutralize_gate_tokens(body)
