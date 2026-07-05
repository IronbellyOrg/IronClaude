"""T06.05 -- FR-016 ``preflight.emit_manifest`` Wave-0 emission contract.

Covers roadmap row R-114 (FR-016): Wave 0 must produce a durable
``manifest.json`` capturing the full :class:`ResolvedLensEntry`
snapshot plus the :class:`PreflightSummary` triple
(target_checksum, workers_requested, transport_kind). The on-disk
artifact is the INV-001 / INV-016 source-of-truth anchor: resume reads
it byte-for-byte rather than re-resolving the lens.

This suite pins:

    1. The deliverable signature
       ``emit_manifest(resolved_lens_entry, target_checksum,
       transport_kind, *, output_dir, ...) -> Path``.
    2. Round-trip equality -- emit → load → equality against the input
       Manifest payload.
    3. Every listed DM-011 snapshot field appears verbatim under
       ``resolved_lens_entry`` (yq-grep acceptance).
    4. Atomic write semantics -- no partial manifest left on disk if a
       caller never reads the returned path.
    5. Return type is :class:`pathlib.Path` (not ``str``) per the
       deliverable.

STRICT-tier task per phase-6-tasklist §T06.05.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from superclaude.cli.swarm.models import (
    LensEntry,
    Manifest,
    PreflightSummary,
    ResolvedLensEntry,
    from_json,
    to_json,
)
from superclaude.cli.swarm.preflight import emit_manifest
from superclaude.cli.swarm.schema import CANONICAL_INJECTION_GUARD_SENTENCE

# ---------------------------------------------------------------------------
# Fixtures -- a fully-populated snapshot so every field is observable.
# ---------------------------------------------------------------------------


PINNED_FRAGMENT: str = (
    "Wave-0 emission lens fragment. " + CANONICAL_INJECTION_GUARD_SENTENCE
)
PINNED_USER_TEMPLATE: str = "Review the target.\n\nTarget:\n{target}\n"
PINNED_RECIPE: str = "bare_review"
PINNED_NEXT_CMD: str = "/sc:troubleshoot {job_id}"
PINNED_CHECKSUM: str = "a" * 64
PINNED_TRANSPORT: str = "openai_compat"
PINNED_JOB_ID: str = "job-T06.05-emission"
PINNED_WORKERS: int = 4


def _snapshot() -> ResolvedLensEntry:
    return ResolvedLensEntry(
        name="bare_review",
        system_prompt_fragment=PINNED_FRAGMENT,
        user_template=PINNED_USER_TEMPLATE,
        recipe_name=PINNED_RECIPE,
        default_workers=3,
        suspect=True,
        tier="T2",
        recommended_next_command_template=PINNED_NEXT_CMD,
        stability="stable",
    )


def _emit(tmp_path: Path) -> Path:
    return emit_manifest(
        _snapshot(),
        PINNED_CHECKSUM,
        PINNED_TRANSPORT,
        output_dir=tmp_path,
        job_id=PINNED_JOB_ID,
        workers_requested=PINNED_WORKERS,
    )


# ---------------------------------------------------------------------------
# Signature + return-type contract.
# ---------------------------------------------------------------------------


def test_emit_manifest_returns_pathlib_path(tmp_path: Path) -> None:
    """Deliverable line -- ``-> Path``, not ``-> str``."""
    out = _emit(tmp_path)
    assert isinstance(out, Path)


def test_emit_manifest_writes_under_output_dir(tmp_path: Path) -> None:
    """File lands at ``<output_dir>/manifest.json``."""
    out = _emit(tmp_path)
    assert out.exists()
    assert out.name == "manifest.json"
    assert out.parent.resolve() == tmp_path.resolve()


def test_emit_manifest_rejects_non_resolvedlens_first_arg(tmp_path: Path) -> None:
    """The first positional must be a ResolvedLensEntry; a raw LensEntry
    or dict slips the INV-001 contract because the snapshot would carry
    fields the manifest schema does not name."""
    lens = LensEntry(name="x")
    with pytest.raises(TypeError):
        emit_manifest(
            lens,  # type: ignore[arg-type]
            PINNED_CHECKSUM,
            PINNED_TRANSPORT,
            output_dir=tmp_path,
        )


# ---------------------------------------------------------------------------
# Round-trip -- emit → load → equality.
# ---------------------------------------------------------------------------


def test_emit_then_load_round_trip(tmp_path: Path) -> None:
    """Acceptance: round-trip test (emit → load → assert equality)."""
    out = _emit(tmp_path)
    loaded = from_json(Manifest, out.read_text(encoding="utf-8"))
    expected = Manifest(
        contract_version="1.0",
        job_id=PINNED_JOB_ID,
        resolved_lens_entry=_snapshot(),
        preflight=PreflightSummary(
            target_checksum=PINNED_CHECKSUM,
            workers_requested=PINNED_WORKERS,
            transport_kind=PINNED_TRANSPORT,
        ),
    )
    assert loaded == expected


def test_emit_payload_matches_to_json_bytes(tmp_path: Path) -> None:
    """Bytes-identical: the on-disk payload equals ``to_json(manifest)``
    so INV-016 byte-stability holds at the emission site."""
    out = _emit(tmp_path)
    loaded = from_json(Manifest, out.read_text(encoding="utf-8"))
    assert to_json(loaded) == out.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# DM-011 field coverage -- every snapshot field appears verbatim.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "field_name,expected",
    [
        ("name", "bare_review"),
        ("system_prompt_fragment", PINNED_FRAGMENT),
        ("user_template", PINNED_USER_TEMPLATE),
        ("recipe_name", PINNED_RECIPE),
        ("default_workers", 3),
        ("suspect", True),
        ("tier", "T2"),
        ("recommended_next_command_template", PINNED_NEXT_CMD),
        ("stability", "stable"),
    ],
)
def test_resolved_lens_entry_field_present_in_manifest(
    tmp_path: Path, field_name: str, expected: object
) -> None:
    """Acceptance: ``yq '.resolved_lens_entry.<field>' manifest.json``
    returns non-null for every DM-011 snapshot field."""
    out = _emit(tmp_path)
    payload = json.loads(out.read_text(encoding="utf-8"))
    snap = payload["resolved_lens_entry"]
    assert field_name in snap
    assert snap[field_name] == expected


def test_preflight_summary_fields_present(tmp_path: Path) -> None:
    out = _emit(tmp_path)
    payload = json.loads(out.read_text(encoding="utf-8"))
    preflight = payload["preflight"]
    assert preflight["target_checksum"] == PINNED_CHECKSUM
    assert preflight["workers_requested"] == PINNED_WORKERS
    assert preflight["transport_kind"] == PINNED_TRANSPORT


def test_top_level_fields_present(tmp_path: Path) -> None:
    out = _emit(tmp_path)
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["contract_version"] == "1.0"
    assert payload["job_id"] == PINNED_JOB_ID


# ---------------------------------------------------------------------------
# Atomic write -- no partial manifest left on disk.
# ---------------------------------------------------------------------------


def test_atomic_write_leaves_no_tmp_file(tmp_path: Path) -> None:
    """The tmp file used during write-to-tmp + ``os.replace`` must be
    consumed by ``os.replace``; the destination directory should hold
    only ``manifest.json`` after a successful emit."""
    _emit(tmp_path)
    leftovers = [p.name for p in tmp_path.iterdir() if p.name != "manifest.json"]
    assert leftovers == []


def test_emit_overwrites_prior_manifest_atomically(tmp_path: Path) -> None:
    """A second emit replaces the first manifest atomically (same path,
    new bytes). No half-written intermediate states are observable on
    the success path."""
    first = _emit(tmp_path)
    first_bytes = first.read_bytes()

    second = emit_manifest(
        ResolvedLensEntry(
            name="bare_review",
            system_prompt_fragment=PINNED_FRAGMENT,
            user_template="DIFFERENT user template",
            recipe_name=PINNED_RECIPE,
            default_workers=3,
            suspect=True,
            tier="T2",
            recommended_next_command_template=PINNED_NEXT_CMD,
            stability="stable",
        ),
        PINNED_CHECKSUM,
        PINNED_TRANSPORT,
        output_dir=tmp_path,
        job_id=PINNED_JOB_ID,
        workers_requested=PINNED_WORKERS,
    )
    assert second == first  # same path
    assert second.read_bytes() != first_bytes


# ---------------------------------------------------------------------------
# Defaults -- the kwarg defaults yield a valid Manifest.
# ---------------------------------------------------------------------------


def test_emit_with_default_kwargs_produces_valid_manifest(tmp_path: Path) -> None:
    out = emit_manifest(
        _snapshot(),
        PINNED_CHECKSUM,
        PINNED_TRANSPORT,
        output_dir=tmp_path,
    )
    loaded = from_json(Manifest, out.read_text(encoding="utf-8"))
    assert loaded.contract_version == "1.0"
    assert loaded.job_id == ""
    assert loaded.preflight.workers_requested == 0
    assert loaded.preflight.target_checksum == PINNED_CHECKSUM
    assert loaded.preflight.transport_kind == PINNED_TRANSPORT
    assert loaded.resolved_lens_entry == _snapshot()
