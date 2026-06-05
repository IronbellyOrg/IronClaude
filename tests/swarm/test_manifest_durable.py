"""T06.03 -- INV-016 manifest immunity to lens-registry mutation.

Covers roadmap row R-112 (INV-016): once Wave 0 stamps
``manifest.json``, the on-disk bytes are the durable source-of-truth
for the lens binding. Any number of subsequent ``resume_mode`` reads,
arbitrary lens-registry hot edits between runs, and repeated
read/write cycles must leave the manifest file byte-identical and the
rehydrated :class:`JobSpec` aligned with the original snapshot.

T06.01 (``tests/swarm/test_resume_uses_manifest_lens.py``) pins the
per-field rehydration contract on the rehydrated :class:`JobSpec`.
This module covers the **complementary** durability property: the
on-disk ``manifest.json`` itself stays byte-identical across the
mutation scenario, and re-emitting the read-back manifest produces
the same bytes (the M6 resume → re-write cycle is byte-stable).

Acceptance contract (phase-6-tasklist.md §T06.03):

    * Manifest immutable across resume; mutation test passes.
    * Lens-registry edits between runs do not affect resumed jobs.
    * ``--force-relens`` opts into mutation visibility (T06.07; the
      durable-suite assertion is in :func:`test_force_relens_opts_into_lens_registry_mutation`
      below, and the full CLI surface is exercised in
      ``tests/swarm/test_force_relens.py``).
    * Diff of manifest contents pre/post resume identical.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.swarm import preflight
from superclaude.cli.swarm.models import (
    LensEntry,
    Manifest,
    PreflightSummary,
    ResolvedLensEntry,
    from_json,
    to_json,
)
from superclaude.cli.swarm.preflight import (
    resume_mode,
    set_lens_resolver,
    write_manifest,
)
from superclaude.cli.swarm.schema import CANONICAL_INJECTION_GUARD_SENTENCE


# ---------------------------------------------------------------------------
# Pinned snapshot + mutated-registry fixtures.
#
# The mutated registry overwrites every snapshot-visible field; any
# leakage from the live registry into the rehydrated JobSpec OR back
# onto the on-disk manifest bytes would be visible in the test
# assertions below.
# ---------------------------------------------------------------------------


ORIGINAL_FRAGMENT: str = (
    "ORIGINAL durable-manifest lens fragment. "
    + CANONICAL_INJECTION_GUARD_SENTENCE
)
ORIGINAL_USER_TEMPLATE: str = "ORIGINAL durable user template: {{target}}"
ORIGINAL_RECIPE: str = "bare-review-v1"
ORIGINAL_NEXT_CMD: str = "sc:reflect on {job_id}"


MUTATED_FRAGMENT: str = (
    "MUTATED durable-manifest lens fragment. "
    + CANONICAL_INJECTION_GUARD_SENTENCE
)
MUTATED_USER_TEMPLATE: str = "MUTATED durable user template: {{target}}"
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
    """A LensEntry overwriting every snapshot-visible field.

    Installing this via :func:`set_lens_resolver` simulates the
    operator hot-editing the lens registry between the original Wave 0
    emit and the resume invocation. INV-016 says neither the on-disk
    manifest bytes nor the rehydrated JobSpec carry these values.
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
        job_id="job-durable-T06.03",
        resolved_lens_entry=snapshot,
        preflight=PreflightSummary(
            target_checksum="a" * 64,
            workers_requested=3,
            transport_kind="openai_compat",
        ),
    )


@pytest.fixture
def emitted_manifest(tmp_path) -> tuple[Path, bytes]:
    """Emit a manifest carrying the pinned snapshot.

    Returns ``(path, original_bytes)`` -- the absolute path to
    ``manifest.json`` and the exact bytes written by
    :func:`write_manifest`. Subsequent assertions diff against
    ``original_bytes`` to catch any drift.
    """
    manifest = _manifest(_snapshot())
    path = Path(write_manifest(manifest, tmp_path))
    original_bytes = path.read_bytes()
    return path, original_bytes


@pytest.fixture
def install_mutated_registry():
    """Install the mutated lens resolver; track how often it was called.

    Yields the list of recorded lookups so each test can assert the
    resolver was (or was not) consulted. The fixture restores the
    previous resolver at teardown so cross-test isolation holds.
    """
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
# INV-016 on-disk bytes -- resume_mode never mutates manifest.json.
# ---------------------------------------------------------------------------


def test_manifest_bytes_unchanged_after_single_resume(
    emitted_manifest: tuple[Path, bytes],
) -> None:
    """A single ``resume_mode`` call leaves the file bytes untouched."""
    path, original_bytes = emitted_manifest
    resume_mode(path)
    assert path.read_bytes() == original_bytes


def test_manifest_bytes_unchanged_after_repeated_resume(
    emitted_manifest: tuple[Path, bytes],
) -> None:
    """N consecutive ``resume_mode`` reads stay byte-identical.

    The manifest is the source-of-truth anchor; repeated reads cannot
    rewrite, truncate, normalise, or canonicalise the on-disk payload.
    """
    path, original_bytes = emitted_manifest
    for _ in range(5):
        resume_mode(path)
        assert path.read_bytes() == original_bytes


def test_manifest_bytes_unchanged_under_lens_registry_mutation(
    emitted_manifest: tuple[Path, bytes],
    install_mutated_registry: list[str],
) -> None:
    """Mutating the lens registry between emit and resume cannot edit
    the manifest file. The on-disk bytes survive the mutation
    scenario the operator throws at the system."""
    path, original_bytes = emitted_manifest
    resume_mode(path)
    assert path.read_bytes() == original_bytes
    # The mutation never reached the resume path -- the resolver was
    # not consulted because the snapshot is on the manifest.
    assert install_mutated_registry == []


def test_manifest_diff_pre_post_resume_is_empty(
    emitted_manifest: tuple[Path, bytes],
    install_mutated_registry: list[str],
) -> None:
    """T06.03 validation line: "Diff of manifest contents pre/post
    resume identical." Diff is computed at byte level against the
    bytes write_manifest produced."""
    path, original_bytes = emitted_manifest
    pre = path.read_bytes()
    resume_mode(path)
    post = path.read_bytes()
    assert pre == post == original_bytes


# ---------------------------------------------------------------------------
# Snapshot durability -- the manifest payload, parsed back, carries the
# original snapshot field-for-field even under registry mutation.
# ---------------------------------------------------------------------------


def test_parsed_manifest_snapshot_matches_pinned_snapshot(
    emitted_manifest: tuple[Path, bytes],
    install_mutated_registry: list[str],
) -> None:
    """Loading the manifest after mutation yields the pinned snapshot."""
    path, _original_bytes = emitted_manifest
    manifest: Manifest = from_json(Manifest, path.read_text(encoding="utf-8"))
    assert manifest.resolved_lens_entry == _snapshot()
    # The mutated registry must not have been consulted as a side
    # effect of either the resume_mode call elsewhere or the parse.
    assert install_mutated_registry == []


def test_parsed_snapshot_fields_carry_original_values(
    emitted_manifest: tuple[Path, bytes],
) -> None:
    """Field-by-field assertion: every snapshot field round-trips
    through the on-disk payload with the ORIGINAL values, never the
    MUTATED ones. Catches drift in any single field even if dataclass
    equality were ever relaxed."""
    path, _ = emitted_manifest
    manifest = from_json(Manifest, path.read_text(encoding="utf-8"))
    snap = manifest.resolved_lens_entry

    assert snap.name == "bare-review"
    assert snap.system_prompt_fragment == ORIGINAL_FRAGMENT
    assert snap.user_template == ORIGINAL_USER_TEMPLATE
    assert snap.recipe_name == ORIGINAL_RECIPE
    assert snap.recommended_next_command_template == ORIGINAL_NEXT_CMD
    assert snap.suspect is True
    assert snap.tier == "T2"
    assert snap.stability == "stable"
    assert snap.default_workers == 3

    # The MUTATED values must NOT appear anywhere in the on-disk payload.
    raw = path.read_text(encoding="utf-8")
    assert MUTATED_FRAGMENT not in raw
    assert MUTATED_USER_TEMPLATE not in raw
    assert MUTATED_RECIPE not in raw
    assert MUTATED_NEXT_CMD not in raw


# ---------------------------------------------------------------------------
# Resume JobSpec immunity -- the rehydrated spec is unaffected by
# registry mutation, byte-for-byte across runs.
# ---------------------------------------------------------------------------


def test_resume_jobspec_identical_under_mutation_and_without(
    emitted_manifest: tuple[Path, bytes],
) -> None:
    """The mutate-then-resume JobSpec equals the no-mutation JobSpec.

    This is INV-016 stated at the spec level: arbitrary edits to the
    live LENSES registry cannot move the rehydrated JobSpec, because
    ``resume_mode`` reads only the manifest.
    """
    path, _ = emitted_manifest

    # First read: no resolver installed.
    set_lens_resolver(None)
    spec_baseline = resume_mode(path)

    # Second read: mutated resolver installed.
    previous = set_lens_resolver(lambda name: _mutated_lens())
    try:
        spec_under_mutation = resume_mode(path)
    finally:
        set_lens_resolver(previous)

    assert spec_baseline == spec_under_mutation


def test_resume_does_not_consult_lens_resolver(
    emitted_manifest: tuple[Path, bytes],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A booby-trapped ``resolve_lens`` is never called during resume.

    INV-016 forbids any consult of the live resolver on the default
    resume path. Replacing ``resolve_lens`` with a function that
    raises lets us prove the contract via observable side effects
    rather than relying on the absence of mutation, which could
    otherwise be a no-op coincidence.
    """
    def boom(name: str) -> LensEntry:
        raise AssertionError(
            "resume_mode must not call resolve_lens -- INV-016 violation"
        )

    monkeypatch.setattr(preflight, "resolve_lens", boom)
    resume_mode(emitted_manifest[0])  # must not raise


# ---------------------------------------------------------------------------
# Read → re-emit byte stability -- a manifest read back by resume_mode
# and re-emitted via write_manifest produces the same bytes (the M6
# rewrite cycle stays byte-stable under the INV-016 contract).
# ---------------------------------------------------------------------------


def test_manifest_round_trip_via_disk_is_byte_identical(
    emitted_manifest: tuple[Path, bytes], tmp_path
) -> None:
    """Read manifest.json from disk, parse, re-emit -- bytes match.

    This piggybacks on the ``to_json`` / ``from_json`` byte-stability
    contract pinned in ``tests/swarm/test_manifest.py`` but pulls the
    bytes back through the on-disk path that resume actually exercises.
    """
    path, original_bytes = emitted_manifest
    manifest = from_json(Manifest, path.read_text(encoding="utf-8"))

    rewrite_dir = tmp_path / "rewrite"
    rewritten_path = Path(write_manifest(manifest, rewrite_dir))
    assert rewritten_path.read_bytes() == original_bytes


def test_manifest_round_trip_via_disk_stable_across_multiple_cycles(
    emitted_manifest: tuple[Path, bytes], tmp_path
) -> None:
    """Five read+rewrite cycles still produce the same bytes."""
    _, original_bytes = emitted_manifest
    payload = original_bytes
    for i in range(5):
        manifest = from_json(Manifest, payload.decode("utf-8"))
        cycle_dir = tmp_path / f"cycle-{i}"
        cycle_path = Path(write_manifest(manifest, cycle_dir))
        payload = cycle_path.read_bytes()
        assert payload == original_bytes


def test_in_memory_to_json_matches_on_disk_bytes(
    emitted_manifest: tuple[Path, bytes],
) -> None:
    """The on-disk bytes match the in-memory ``to_json`` payload for
    the same Manifest. Anchors that ``write_manifest`` emits exactly
    ``to_json(...)`` and nothing else (no trailing newline, no encoding
    rewrites)."""
    path, original_bytes = emitted_manifest
    manifest = from_json(Manifest, path.read_text(encoding="utf-8"))
    assert to_json(manifest).encode("utf-8") == original_bytes


# ---------------------------------------------------------------------------
# --force-relens (T06.07) -- the acceptance line says this flag opts
# into mutation visibility. The pinning assertion lives here so the
# durability suite stays the one-stop test for "manifest immune by
# default; --force-relens is the explicit override". The full T06.07
# surface (CLI flag wiring, usage gating, end-to-end dispatch
# snapshot) is exercised in ``tests/swarm/test_force_relens.py``.
# ---------------------------------------------------------------------------


def test_force_relens_opts_into_lens_registry_mutation(
    emitted_manifest: tuple[Path, bytes],
    install_mutated_registry: list[str],
) -> None:
    """T06.07 contract: ``--force-relens`` re-resolves against the
    current registry, surfacing the mutated lens on the rehydrated
    JobSpec. The default ``resume_mode`` path remains manifest-driven.
    """
    path, _ = emitted_manifest
    spec = resume_mode(path, force_relens=True)
    assert spec.prompt.system == MUTATED_FRAGMENT
    assert spec.prompt.user_template == MUTATED_USER_TEMPLATE
    assert spec.normalization.recipe == MUTATED_RECIPE
    assert spec.recommended_next_command_template == MUTATED_NEXT_CMD
    # The mutated resolver IS consulted on the force-relens path.
    assert install_mutated_registry == ["bare-review"]


def test_default_resume_path_remains_manifest_driven_without_force_relens(
    emitted_manifest: tuple[Path, bytes],
    install_mutated_registry: list[str],
) -> None:
    """Inverse of the force-relens contract: with the flag absent (the
    only path that exists today), resume yields the manifest snapshot
    even when the registry has been mutated. This pins the default
    behaviour so any future implementation of ``--force-relens`` is
    forced to be opt-in, not on-by-default."""
    path, _ = emitted_manifest
    spec = resume_mode(path)
    assert spec.prompt.system == ORIGINAL_FRAGMENT
    assert spec.prompt.user_template == ORIGINAL_USER_TEMPLATE
    assert spec.normalization.recipe == ORIGINAL_RECIPE
    assert spec.recommended_next_command_template == ORIGINAL_NEXT_CMD
    assert install_mutated_registry == []
