"""T06.01 -- INV-001 resume reads lens from manifest, not live LENSES.

Covers roadmap row R-110 (INV-001 / INV-016): once a job is accepted,
``manifest.json`` is the durable source-of-truth for the lens binding.
M6 resume must rehydrate from :attr:`Manifest.resolved_lens_entry`
verbatim and never call ``LENSES.get(name)`` against the live
registry, so lens-registry edits made between original Wave 0 emit
and the resume invocation are silently ignored. The opt-in
``--force-relens`` flag (T06.07) restores re-resolution semantics;
the default resume path stays manifest-driven.

The acceptance contract for T06.01 (phase-6-tasklist.md §T06.01):

    * ``preflight.resume_mode(manifest_path) -> JobSpec`` returns a
      JobSpec rehydrated from the manifest's resolved snapshot.
    * The lens-derived fields on the returned JobSpec
      (``prompt.system``, ``prompt.user_template``,
      ``normalization.recipe``, ``recommended_next_command_template``)
      come from the manifest, not from the live LENSES resolver.
    * Mutating the live registry between manifest emit and resume
      does **not** affect the rehydrated JobSpec.
    * ``resume_mode`` does **not** invoke the lens resolver
      (``LENSES.get(...)`` / :func:`resolve_lens`) at all -- the
      manifest carries the full snapshot.

This module pins all four properties; T06.03 (manifest-durable test)
piggybacks on the same mutation scenario for the byte-identical
manifest immunity check.
"""

# ruff: noqa: E402 -- module-level ``pytestmark`` intentionally precedes the
# superclaude imports so the marker is registered before collection.

from __future__ import annotations

from pathlib import Path

import pytest

# INV-001 manifest lens rehydration (T08.03 / NFR-007). Module-level
# marker so every test in this file is selected by ``pytest -m inv``.
pytestmark = pytest.mark.inv

from superclaude.cli.swarm import preflight
from superclaude.cli.swarm.models import (
    JobSpec,
    LensEntry,
    Manifest,
    PreflightSummary,
    ResolvedLensEntry,
)
from superclaude.cli.swarm.preflight import (
    resume_mode,
    set_lens_resolver,
    write_manifest,
)
from superclaude.cli.swarm.schema import CANONICAL_INJECTION_GUARD_SENTENCE

# ---------------------------------------------------------------------------
# Fixtures -- pinned manifest snapshot and the post-emit "live mutation"
# ---------------------------------------------------------------------------


ORIGINAL_FRAGMENT: str = (
    "ORIGINAL lens prompt fragment. " + CANONICAL_INJECTION_GUARD_SENTENCE
)
ORIGINAL_USER_TEMPLATE: str = "ORIGINAL user template: {{target}}"
ORIGINAL_RECIPE: str = "bare-review-v1"
ORIGINAL_NEXT_CMD: str = "sc:reflect on {job_id}"


MUTATED_FRAGMENT: str = (
    "MUTATED lens prompt fragment. " + CANONICAL_INJECTION_GUARD_SENTENCE
)
MUTATED_USER_TEMPLATE: str = "MUTATED user template: {{target}}"
MUTATED_RECIPE: str = "verdict-only-v1"
MUTATED_NEXT_CMD: str = "sc:troubleshoot {job_id}"


def _snapshot() -> ResolvedLensEntry:
    """The manifest-frozen lens snapshot stamped at Wave 0."""
    return ResolvedLensEntry(
        name="bare-review",
        system_prompt_fragment=ORIGINAL_FRAGMENT,
        user_template=ORIGINAL_USER_TEMPLATE,
        recipe_name=ORIGINAL_RECIPE,
        default_workers=3,
        suspect=True,
        tier="T2",
        recommended_next_command_template=ORIGINAL_NEXT_CMD,
        stability="stable",
    )


def _mutated_lens() -> LensEntry:
    """A LensEntry that overwrites every field captured in the snapshot.

    Installing this via :func:`set_lens_resolver` simulates the
    operator hot-editing the lens registry after the manifest was
    emitted. If :func:`resume_mode` consulted the live registry, the
    rehydrated JobSpec would carry these mutated values; the INV-001
    contract requires it to carry the snapshot values instead.
    """
    return LensEntry(
        name="bare-review",
        description="mutated lens registry entry",
        system_prompt_fragment=MUTATED_FRAGMENT,
        user_template=MUTATED_USER_TEMPLATE,
        output_template_path="/abs/path/to/mutated-template.j2",
        recipe_name=MUTATED_RECIPE,
        normalizer_strategy="passthrough",
        default_workers=5,
        default_target_line_cap=6000,
        suspect=False,
        tier="T3",
        recommended_next_command_template=MUTATED_NEXT_CMD,
        acceptance_notes="mutated",
        stability="experimental",
    )


def _manifest(snapshot: ResolvedLensEntry) -> Manifest:
    return Manifest(
        contract_version="1.0",
        job_id="job-resume-T06.01",
        resolved_lens_entry=snapshot,
        preflight=PreflightSummary(
            target_checksum="a" * 64,
            workers_requested=3,
            transport_kind="openai_compat",
        ),
    )


@pytest.fixture
def emitted_manifest_path(tmp_path) -> Path:
    """Emit a manifest carrying the pinned snapshot and return its path."""
    manifest = _manifest(_snapshot())
    path = write_manifest(manifest, tmp_path)
    return Path(path)


@pytest.fixture
def mutated_registry():
    """Install a mutated lens resolver and track whether resume calls it."""
    calls: list[str] = []

    def resolver(name: str) -> LensEntry:
        calls.append(name)
        return _mutated_lens()

    previous = set_lens_resolver(resolver)
    try:
        yield calls
    finally:
        set_lens_resolver(previous)


# ---------------------------------------------------------------------------
# resume_mode contract -- lens-derived JobSpec fields come from the manifest
# ---------------------------------------------------------------------------


def test_resume_mode_returns_jobspec(emitted_manifest_path: Path) -> None:
    """The function signature contract: manifest path -> JobSpec."""
    spec = resume_mode(emitted_manifest_path)
    assert isinstance(spec, JobSpec)


def test_resume_mode_rehydrates_lens_name_from_manifest(
    emitted_manifest_path: Path, mutated_registry: list[str]
) -> None:
    """The lens name is the snapshot's name, not the mutated entry's."""
    spec = resume_mode(emitted_manifest_path)
    assert spec.lens == "bare-review"
    # Even though we installed a mutated resolver, resume_mode never
    # calls it -- INV-001 requires byte-for-byte manifest fidelity.
    assert mutated_registry == []


def test_resume_mode_uses_manifest_prompt_fragment_not_live_registry(
    emitted_manifest_path: Path, mutated_registry: list[str]
) -> None:
    """``prompt.system`` carries the snapshot fragment verbatim."""
    spec = resume_mode(emitted_manifest_path)
    assert spec.prompt.system == ORIGINAL_FRAGMENT
    # The mutated fragment must NOT leak into the rehydrated spec.
    assert MUTATED_FRAGMENT not in spec.prompt.system
    assert mutated_registry == []


def test_resume_mode_uses_manifest_user_template_not_live_registry(
    emitted_manifest_path: Path, mutated_registry: list[str]
) -> None:
    spec = resume_mode(emitted_manifest_path)
    assert spec.prompt.user_template == ORIGINAL_USER_TEMPLATE
    assert spec.prompt.user_template != MUTATED_USER_TEMPLATE
    assert mutated_registry == []


def test_resume_mode_uses_manifest_recipe_not_live_registry(
    emitted_manifest_path: Path, mutated_registry: list[str]
) -> None:
    spec = resume_mode(emitted_manifest_path)
    assert spec.normalization.recipe == ORIGINAL_RECIPE
    assert spec.normalization.recipe != MUTATED_RECIPE
    assert mutated_registry == []


def test_resume_mode_uses_manifest_next_command_template_not_live_registry(
    emitted_manifest_path: Path, mutated_registry: list[str]
) -> None:
    spec = resume_mode(emitted_manifest_path)
    assert spec.recommended_next_command_template == ORIGINAL_NEXT_CMD
    assert spec.recommended_next_command_template != MUTATED_NEXT_CMD
    assert mutated_registry == []


# ---------------------------------------------------------------------------
# Manifest-derived non-lens fields -- job_id, workers, transport
# ---------------------------------------------------------------------------


def test_resume_mode_carries_manifest_job_id(emitted_manifest_path: Path) -> None:
    spec = resume_mode(emitted_manifest_path)
    assert spec.job_id == "job-resume-T06.01"


def test_resume_mode_carries_manifest_workers_requested(
    emitted_manifest_path: Path,
) -> None:
    spec = resume_mode(emitted_manifest_path)
    assert spec.workers.count == 3


def test_resume_mode_carries_manifest_transport_kind(
    emitted_manifest_path: Path,
) -> None:
    spec = resume_mode(emitted_manifest_path)
    assert spec.transport.kind == "openai_compat"


# ---------------------------------------------------------------------------
# Invariance under mutation -- the registry can change arbitrarily between
# emit and resume; the rehydrated JobSpec stays byte-for-byte aligned
# with the snapshot.
# ---------------------------------------------------------------------------


def test_resume_mode_invariant_under_post_emit_lens_mutation(
    emitted_manifest_path: Path, mutated_registry: list[str]
) -> None:
    """Mutate-then-resume yields the same JobSpec as resume-without-mutation."""
    # First call with the mutated resolver installed.
    spec_after_mutation = resume_mode(emitted_manifest_path)

    # Restore the default resolver (no live LENSES entry registered).
    set_lens_resolver(None)
    try:
        spec_without_mutation = resume_mode(emitted_manifest_path)
    finally:
        # Re-install the mutated one so the fixture's finalizer pops the
        # correct previous resolver -- we left the stack at "default" but
        # the fixture expects to find the mutated one on its yield path.
        set_lens_resolver(lambda name: _mutated_lens())

    assert spec_after_mutation == spec_without_mutation
    # The resolver was never consulted during either resume call.
    assert mutated_registry == []


def test_resume_mode_does_not_invoke_lens_resolver(
    emitted_manifest_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """No call to ``resolve_lens`` is made during resume rehydration.

    The resolver is the live-registry escape hatch. INV-001 requires
    the resume path to be entirely manifest-driven, so any consult of
    ``resolve_lens`` would be a contract violation regardless of what
    the resolver returns.
    """
    invocations: list[str] = []

    def boom(name: str) -> LensEntry:
        invocations.append(name)
        raise AssertionError(
            "resume_mode must not call resolve_lens -- INV-001 violation"
        )

    monkeypatch.setattr(preflight, "resolve_lens", boom)
    resume_mode(emitted_manifest_path)
    assert invocations == []


# ---------------------------------------------------------------------------
# Snapshot-source fidelity -- the snapshot embedded in the manifest is the
# exact ResolvedLensEntry; round-tripping it through resume yields the same
# field values (the byte-identical INV-016 contract is exercised in
# tests/swarm/test_manifest.py and tests/swarm/test_manifest_durable.py;
# this assertion is the smaller per-field check).
# ---------------------------------------------------------------------------


def test_resume_mode_preserves_snapshot_field_set(
    emitted_manifest_path: Path,
) -> None:
    spec = resume_mode(emitted_manifest_path)
    snapshot = _snapshot()
    assert spec.lens == snapshot.name
    assert spec.prompt.system == snapshot.system_prompt_fragment
    assert spec.prompt.user_template == snapshot.user_template
    assert spec.normalization.recipe == snapshot.recipe_name
    assert (
        spec.recommended_next_command_template
        == snapshot.recommended_next_command_template
    )


# ---------------------------------------------------------------------------
# Public surface -- resume_mode is exported.
# ---------------------------------------------------------------------------


def test_resume_mode_exported_from_preflight() -> None:
    assert "resume_mode" in preflight.__all__
    assert callable(getattr(preflight, "resume_mode"))
