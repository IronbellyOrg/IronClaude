"""T02.25 -- DM-020 ``CallerMetadata`` field set + OQ-009 precedence.

Covers roadmap row R-056 / DM-020. The :class:`CallerMetadata` dataclass
is the lens/caller-attached output metadata that the executor stamps
onto :class:`ResultContract.caller_metadata` at Wave 3 reduce. T02.25
lands two pieces:

1. The two-field set ``suspect:bool`` + ``tier:str`` per the DM-020
   roadmap row (``.dev/releases/Current/MultiModelSwarm/roadmap.md``
   line 160).
2. :func:`preflight.resolve_caller_metadata` -- the OQ-009 precedence
   resolution: lens defaults supply the values; a caller-supplied
   override wins field-by-field per the §4.2 / FR-LENS-004 rule
   "caller-supplied values override lens defaults". The resolution
   record is in ``docs/swarm/oq-resolutions.md``.

The tests below pin both pieces. ``test_caller_metadata_field_set``
verifies the dataclass surface; the precedence tests pin the OQ-009
resolution at the :func:`preflight.resolve_caller_metadata` call site.
The Wave-0 wiring test (``test_run_preflight_attaches_resolved_caller_metadata``)
verifies the lens-side path stamps the resolved value onto
:class:`PreflightResult` and that the manifest's
:class:`ResolvedLensEntry` snapshot carries the lens-side contribution
(INV-001 / INV-016 -- the resolved metadata is recoverable from
``manifest.json`` alone).
"""

from __future__ import annotations

import dataclasses
import typing
from typing import Any

import pytest

from superclaude.cli.swarm import preflight
from superclaude.cli.swarm.models import (
    CallerMetadata,
    LensEntry,
    Manifest,
    ResolvedLensEntry,
    from_json,
    to_json,
)
from superclaude.cli.swarm.preflight import (
    MIN_TARGET_NON_WHITESPACE_BYTES,
    resolve_caller_metadata,
    run_preflight,
    set_lens_resolver,
)
from superclaude.cli.swarm.schema import (
    CANONICAL_INJECTION_GUARD_SENTENCE,
    CURRENT_SPEC_VERSION,
)

# ---------------------------------------------------------------------------
# DM-020 dataclass surface
# ---------------------------------------------------------------------------


def test_caller_metadata_is_a_dataclass() -> None:
    assert dataclasses.is_dataclass(CallerMetadata)


def test_caller_metadata_field_set() -> None:
    """DM-020 row pins the field set to ``suspect:bool`` + ``tier:str``."""
    declared = tuple(f.name for f in dataclasses.fields(CallerMetadata))
    assert declared == ("suspect", "tier"), (
        f"CallerMetadata field set diverged from DM-020 row: {declared!r}"
    )


def test_caller_metadata_field_types() -> None:
    hints = typing.get_type_hints(CallerMetadata)
    assert hints["suspect"] is bool
    assert hints["tier"] is str


def test_caller_metadata_defaults() -> None:
    """Conservative defaults so the no-arg round-trip stays valid."""
    metadata = CallerMetadata()
    assert metadata.suspect is False
    assert metadata.tier == ""


# ---------------------------------------------------------------------------
# OQ-009 precedence -- resolve_caller_metadata
# ---------------------------------------------------------------------------


def _lens(*, suspect: bool, tier: str) -> LensEntry:
    """Helper -- minimal LensEntry carrying the two DM-020 fields."""
    return LensEntry(
        name="bare-review",
        suspect=suspect,
        tier=tier,
    )


def test_resolve_caller_metadata_lens_only_default() -> None:
    """OQ-009 default branch: lens values flow through verbatim."""
    lens = _lens(suspect=True, tier="T2")
    resolved = resolve_caller_metadata(lens)
    assert resolved == CallerMetadata(suspect=True, tier="T2")


def test_resolve_caller_metadata_lens_only_false_default() -> None:
    """The conservative ``suspect=False`` default lens path also resolves."""
    lens = _lens(suspect=False, tier="")
    resolved = resolve_caller_metadata(lens)
    assert resolved == CallerMetadata(suspect=False, tier="")


def test_resolve_caller_metadata_caller_override_wins() -> None:
    """OQ-009 caller-overridable branch -- override wins field-by-field."""
    lens = _lens(suspect=True, tier="T2")
    override = CallerMetadata(suspect=False, tier="T1")
    resolved = resolve_caller_metadata(lens, override=override)
    assert resolved == CallerMetadata(suspect=False, tier="T1")


def test_resolve_caller_metadata_override_flipping_suspect() -> None:
    """Caller can flip ``suspect`` False even when the lens marks True."""
    lens = _lens(suspect=True, tier="T2")
    override = CallerMetadata(suspect=False, tier="T2")
    resolved = resolve_caller_metadata(lens, override=override)
    assert resolved.suspect is False
    assert resolved.tier == "T2"


def test_resolve_caller_metadata_accepts_resolved_lens_snapshot() -> None:
    """The executor calls this helper at reduce time against the manifest
    snapshot rather than the live LensEntry; both paths must work."""
    lens = _lens(suspect=True, tier="T2")
    snapshot = ResolvedLensEntry.from_lens(lens)
    resolved = resolve_caller_metadata(snapshot)
    assert resolved == CallerMetadata(suspect=True, tier="T2")


def test_resolve_caller_metadata_returns_fresh_instance() -> None:
    """The helper never returns the override instance directly so mutation
    of the caller's payload after the call cannot retroactively change
    the resolved value."""
    lens = _lens(suspect=False, tier="T1")
    override = CallerMetadata(suspect=True, tier="T2")
    resolved = resolve_caller_metadata(lens, override=override)
    assert resolved is not override
    override.tier = "MUTATED"
    assert resolved.tier == "T2"


def test_resolve_caller_metadata_rejects_bad_source() -> None:
    with pytest.raises(TypeError, match="LensEntry or ResolvedLensEntry"):
        resolve_caller_metadata("not a lens")  # type: ignore[arg-type]


def test_resolve_caller_metadata_rejects_bad_override() -> None:
    lens = _lens(suspect=False, tier="")
    with pytest.raises(TypeError, match="CallerMetadata"):
        resolve_caller_metadata(lens, override={"suspect": True})  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Wave-0 wiring -- run_preflight stamps the resolved metadata
# ---------------------------------------------------------------------------


def _minimal_valid_spec() -> dict[str, Any]:
    """Minimal schema-valid JobSpec; mirrors tests/swarm/test_preflight.py."""
    return {
        "spec_version": CURRENT_SPEC_VERSION,
        "job_id": "job-callermeta-001",
        "created": "2026-06-01T00:00:00Z",
        "caller": {
            "skill": "sc-bare-review",
            "skill_version": "1.0.0",
            "invocation_label": "callermeta-T02.25",
            "kind": "claude",
        },
        "lens": "bare-review",
        "custom_prompt_dir": None,
        "workers": {
            "count": 3,
            "models": ["m1", "m2", "m3"],
            "timeout_sec": 180,
            "temperature": 0.2,
            "retry": {
                "on_5xx": True,
                "on_5xx_backoff_sec": 2,
                "on_4xx": False,
                "on_timeout": False,
            },
        },
        "transport": {
            "kind": "openai_compat",
            "base_url_env": "T2ProxyUrl",
            "api_key_env": "T2ProxyKey",
        },
        "prompt": {
            "system": ("You are a reviewer. " + CANONICAL_INJECTION_GUARD_SENTENCE),
            "user_template": "Review: {{target}}",
            "variables": {},
        },
        "target": {
            "kind": "file",
            "path": "/abs/path/to/target.py",
            "truncation": {"line_cap": 4000, "byte_floor": 50},
            "delimiters": {
                "open": "<<<TARGET>>>",
                "close": "<<<END TARGET>>>",
            },
            "injection_guard": {
                "enabled": True,
                "required_substring": CANONICAL_INJECTION_GUARD_SENTENCE,
            },
        },
        "normalization": {
            "recipe": "bare-review-v1",
            "template_path": "/abs/path/to/template.j2",
            "schema_version": "1.0",
            "recipe_args": {},
            "on_parse_error": {"salvage": True, "retain_raw": True},
        },
        "output": {
            "dir": "/abs/path/to/output",
            "filename_template": "{lens}-{index:02d}-{model_slug}.md",
            "lens_name": "bare-review",
            "atomic_write": True,
            "emit_meta_sidecar": True,
        },
        "amalgamation_mode": "normalize+merge",
        "status_policy": {
            "floor": 2,
            "success_first": True,
            "partial_threshold": 2,
        },
        "recommended_next_command_template": "sc:reflect on {job_id}",
        "recommended_next_command_substitutions": {"job_id": "job-callermeta-001"},
        "runtime": {
            "mode": "inline",
            "log_level": "info",
            "on_completion": {
                "write_done_sentinel": True,
                "print_contract_to_stdout": True,
            },
        },
    }


@pytest.fixture
def lens_resolver_stub():
    """Install a stub lens resolver with ``suspect=True`` / ``tier="T2"``."""
    lens = LensEntry(
        name="bare-review",
        description="bare review",
        system_prompt_fragment=(
            "Review with care. " + CANONICAL_INJECTION_GUARD_SENTENCE
        ),
        user_template="Review: {{target}}",
        output_template_path="/abs/path/to/template.j2",
        recipe_name="bare-review-v1",
        default_workers=3,
        default_target_line_cap=4000,
        suspect=True,
        tier="T2",
        recommended_next_command_template="sc:reflect on {job_id}",
        acceptance_notes="",
        stability="stable",
    )

    def resolver(name: str) -> LensEntry:
        if name != "bare-review":
            raise KeyError(name)
        return lens

    previous = set_lens_resolver(resolver)
    try:
        yield lens
    finally:
        set_lens_resolver(previous)


@pytest.fixture
def target_loader():
    return lambda _path: b"x" * (MIN_TARGET_NON_WHITESPACE_BYTES + 10)


def test_run_preflight_attaches_resolved_caller_metadata(
    lens_resolver_stub, target_loader
) -> None:
    """Wave 0 stamps the lens-default CallerMetadata onto the result."""
    result = run_preflight(_minimal_valid_spec(), target_loader=target_loader)
    assert isinstance(result.caller_metadata, CallerMetadata)
    assert result.caller_metadata == CallerMetadata(suspect=True, tier="T2")


def test_run_preflight_honours_caller_override(
    lens_resolver_stub, target_loader
) -> None:
    """OQ-009 caller-overridable precedence at the Wave-0 entrypoint."""
    override = CallerMetadata(suspect=False, tier="T1")
    result = run_preflight(
        _minimal_valid_spec(),
        target_loader=target_loader,
        caller_metadata_override=override,
    )
    assert result.caller_metadata == CallerMetadata(suspect=False, tier="T1")


def test_manifest_resolved_lens_carries_caller_metadata_inputs(
    lens_resolver_stub, target_loader
) -> None:
    """The manifest's ResolvedLensEntry snapshot carries the lens-side
    contribution to CallerMetadata so the resolved value is recoverable
    from ``manifest.json`` alone (INV-001 / INV-016).
    """
    result = run_preflight(_minimal_valid_spec(), target_loader=target_loader)
    snapshot = result.manifest.resolved_lens_entry
    assert snapshot.suspect is True
    assert snapshot.tier == "T2"
    # Re-resolve from the snapshot -- mirrors what the executor does at
    # reduce time when stamping the contract.
    recovered = preflight.resolve_caller_metadata(snapshot)
    assert recovered == result.caller_metadata


def test_resolve_caller_metadata_is_exported() -> None:
    """Public surface gate -- the helper must be exported."""
    assert "resolve_caller_metadata" in preflight.__all__


# ---------------------------------------------------------------------------
# F-P2-2 -- Manifest.caller_metadata persistence + JSON round-trip
# ---------------------------------------------------------------------------


def test_manifest_field_carries_caller_metadata_default() -> None:
    """F-P2-2: Manifest has a defaulted CallerMetadata field (no-arg safe)."""
    m = Manifest()
    assert isinstance(m.caller_metadata, CallerMetadata)
    assert m.caller_metadata == CallerMetadata()


def test_manifest_persists_resolved_lens_default_caller_metadata(
    lens_resolver_stub, target_loader
) -> None:
    """F-P2-2: Wave 0 stamps the lens-default CallerMetadata onto the manifest.

    Previously the resolved value lived only on PreflightResult; now it is on
    ``manifest.caller_metadata`` so it survives executor restart / resume.
    """
    result = run_preflight(_minimal_valid_spec(), target_loader=target_loader)
    assert result.manifest.caller_metadata == CallerMetadata(suspect=True, tier="T2")
    # Consistency: the manifest field matches the in-memory resolved value.
    assert result.manifest.caller_metadata == result.caller_metadata


def test_manifest_persists_caller_override(lens_resolver_stub, target_loader) -> None:
    """F-P2-2: an OQ-009 caller override diverging from the lens default
    persists on the manifest (the gap the remediation closes)."""
    override = CallerMetadata(suspect=False, tier="T1")
    result = run_preflight(
        _minimal_valid_spec(),
        target_loader=target_loader,
        caller_metadata_override=override,
    )
    # Lens default is suspect=True/tier=T2; the override must win AND persist.
    assert result.manifest.caller_metadata == CallerMetadata(suspect=False, tier="T1")


def test_manifest_caller_metadata_survives_json_round_trip(
    lens_resolver_stub, target_loader
) -> None:
    """F-P2-2: caller_metadata round-trips byte-identically through JSON
    (INV-016) and the override is recoverable from manifest.json alone."""
    override = CallerMetadata(suspect=False, tier="T1")
    result = run_preflight(
        _minimal_valid_spec(),
        target_loader=target_loader,
        caller_metadata_override=override,
    )
    payload = to_json(result.manifest)
    rehydrated = from_json(Manifest, payload)
    # Byte-identical round-trip + the override is recoverable from JSON alone.
    assert to_json(rehydrated) == payload
    assert rehydrated.caller_metadata == CallerMetadata(suspect=False, tier="T1")


def test_emit_manifest_stamps_caller_metadata(tmp_path) -> None:
    """F-P2-2: emit_manifest accepts and persists an explicit caller_metadata."""
    from superclaude.cli.swarm.preflight import emit_manifest

    out = emit_manifest(
        ResolvedLensEntry(
            name="bare-review",
            system_prompt_fragment="frag " + CANONICAL_INJECTION_GUARD_SENTENCE,
            user_template="u",
            recipe_name="bare-review-v1",
            default_workers=3,
            suspect=True,
            tier="T2",
            recommended_next_command_template="sc:reflect on {job_id}",
            stability="stable",
        ),
        "a" * 64,
        "openai_compat",
        output_dir=tmp_path,
        job_id="job-emit-callermeta",
        workers_requested=3,
        caller_metadata=CallerMetadata(suspect=False, tier="T1"),
    )
    loaded = from_json(Manifest, out.read_text(encoding="utf-8"))
    assert loaded.caller_metadata == CallerMetadata(suspect=False, tier="T1")
