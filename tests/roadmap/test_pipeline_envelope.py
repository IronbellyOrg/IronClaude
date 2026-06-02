"""Tests for the R1.2 ``PipelineEnvelope`` substrate + post-step dispatch.

Covers the surface described by BUILD-REQUEST §R1.2 + §MVR §1, plus the
sc:reflect UC-1 adjustments (dispatch-reachability, field-set conformance,
list-vs-tuple round-trip per Phase 6 OQ-2).

These tests guard:

1. ``test_envelope_round_trip`` — ``save_envelope`` → ``load_envelope``
   equality including explicit ``list[Finding]`` / ``list[AcceptedDeviation]``
   list-not-tuple assertions (Phase 6 OQ-2 invariants).
2. ``test_atomic_write_safety`` — the tmpfile + ``os.replace`` pattern
   leaves no partial ``envelope.json`` on a simulated mid-write failure.
3. ``test_dispatch_map_completeness`` — every step id used by
   ``_build_steps`` has an extractor resolvable via
   :func:`get_post_extractor` (covers both static IDs and dynamic
   ``generate-{agent.id}`` IDs).
4. ``test_dispatch_reachability`` — Contract #2 / sc:reflect UC-1 G1:
   AST walk asserts the dispatch is invoked from production entry
   points. Map-completeness alone is necessary but not sufficient.
5. ``test_field_set_conformance`` — sc:reflect UC-1 G3 / Phase 6 OQ-1
   parallel: the dataclass field set is exactly the §MVR §1 canonical
   8-field set; catches future drift.
6. ``test_dual_write_preservation`` — invoking the dual-write helper
   never mutates the step's existing markdown artifact (the envelope is
   additive, not destructive).
"""

from __future__ import annotations

import ast
import dataclasses
import json
from pathlib import Path

import pytest

from superclaude.cli.roadmap.convergence import ConvergenceResult
from superclaude.cli.roadmap.envelope import (
    POST_EXTRACTORS,
    AcceptedDeviation,
    ArtifactRef,
    PipelineEnvelope,
    envelope_from_dict,
    envelope_to_dict,
    get_post_extractor,
    load_envelope,
    save_envelope,
)
from superclaude.cli.roadmap.id_registry import SpecIdRegistry
from superclaude.cli.roadmap.models import Finding

# ---------------------------------------------------------------------------
# Fixture: a non-trivial envelope exercising every field type
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_envelope(tmp_path: Path) -> PipelineEnvelope:
    spec_path = tmp_path / "spec.md"
    spec_path.write_text("# spec\n")
    registry = SpecIdRegistry(
        fr_ids=("FR-1", "FR-2"),
        nfr_ids=("NFR-1",),
        sc_ids=("SC-1",),
        g_ids=(),
        d_ids=("D-1", "D-3"),
        accepted_deviation_ids=("D-7",),
        spec_hash="abc1234567890def",  # pragma: allowlist secret
        spec_path=spec_path,
    )
    finding = Finding(
        id="F-1",
        severity="HIGH",
        dimension="structural",
        description="missing FR",
        location="line 1",
        evidence="evidence text",
        fix_guidance="add FR",
    )
    convergence = ConvergenceResult(
        passed=True,
        run_count=2,
        final_high_count=0,
    )
    artifact = tmp_path / "extract.md"
    artifact.write_text("# extract\n")
    return PipelineEnvelope(
        release_id="r1",
        spec_hash="abc1234567890def",  # pragma: allowlist secret
        spec_ids=registry,
        artifacts={
            "extract": ArtifactRef(
                path=artifact,
                content_hash="0123456789abcdef",  # pragma: allowlist secret
            ),
        },
        findings=[finding],
        counts={"merge.roadmap_id_count": 4, "anti-instinct.high_count": 0},
        convergence=convergence,
        accepted_deviations=[
            AcceptedDeviation(id="D-7", reason="ok", timestamp="2026-06-01T00:00:00Z"),
        ],
    )


# ---------------------------------------------------------------------------
# 1. Round-trip (with Phase 6 OQ-2 list-vs-tuple assertions)
# ---------------------------------------------------------------------------


def test_envelope_round_trip(sample_envelope: PipelineEnvelope, tmp_path: Path) -> None:
    """save_envelope → load_envelope produces an equal envelope.

    Explicitly asserts that list-typed fields (findings, accepted_deviations)
    survive deserialize as ``list`` not ``tuple`` — addresses Phase 6 OQ-2.
    """
    path = tmp_path / "envelope.json"
    save_envelope(sample_envelope, path)

    assert path.exists()
    round_tripped = load_envelope(path)

    assert round_tripped == sample_envelope
    # OQ-2 invariant: list-typed fields stay list, not tuple
    assert isinstance(round_tripped.findings, list)
    assert not isinstance(round_tripped.findings, tuple)
    assert isinstance(round_tripped.accepted_deviations, list)
    assert not isinstance(round_tripped.accepted_deviations, tuple)
    # And mutable dicts stay mutable dicts
    assert isinstance(round_tripped.artifacts, dict)
    assert isinstance(round_tripped.counts, dict)


def test_envelope_to_dict_shape(sample_envelope: PipelineEnvelope) -> None:
    """envelope_to_dict produces JSON-safe primitives (no Path, no dataclass)."""
    d = envelope_to_dict(sample_envelope)
    # All top-level fields present
    assert set(d.keys()) == {
        "release_id",
        "spec_hash",
        "spec_ids",
        "artifacts",
        "findings",
        "counts",
        "convergence",
        "accepted_deviations",
    }
    # JSON-safe: must round-trip through json.dumps/loads
    raw = json.dumps(d)
    parsed = json.loads(raw)
    assert envelope_from_dict(parsed) == sample_envelope


# ---------------------------------------------------------------------------
# 2. Atomic write safety
# ---------------------------------------------------------------------------


def test_atomic_write_uses_tmpfile(
    sample_envelope: PipelineEnvelope, tmp_path: Path, monkeypatch
) -> None:
    """save_envelope writes via a .tmp file + os.replace (POSIX atomic rename).

    Verifies the tmpfile is created during the write and replaced via the
    os.replace call (the convergence.py:315-317 pattern).
    """
    import os

    path = tmp_path / "envelope.json"
    seen_replace_calls: list[tuple[str, str]] = []

    real_replace = os.replace

    def spying_replace(src: str, dst: str) -> None:
        seen_replace_calls.append((str(src), str(dst)))
        real_replace(src, dst)

    monkeypatch.setattr("superclaude.cli.roadmap.envelope.os.replace", spying_replace)
    save_envelope(sample_envelope, path)

    assert len(seen_replace_calls) == 1
    src, dst = seen_replace_calls[0]
    assert src.endswith(".tmp")
    assert dst == str(path)
    assert path.exists()
    # No .tmp file orphaned after atomic replace
    assert not (tmp_path / "envelope.json.tmp").exists()


def test_atomic_write_no_partial_on_interrupt(
    sample_envelope: PipelineEnvelope, tmp_path: Path, monkeypatch
) -> None:
    """If os.replace raises mid-write, the final envelope.json is never partial.

    Simulates a mid-write OS failure between tmpfile.write_text and
    os.replace — the .tmp file may exist but the destination must NOT.
    """

    def boom(src, dst):
        raise OSError("simulated rename failure")

    monkeypatch.setattr("superclaude.cli.roadmap.envelope.os.replace", boom)
    path = tmp_path / "envelope.json"
    with pytest.raises(OSError):
        save_envelope(sample_envelope, path)
    # Destination not partially written
    assert not path.exists()


# ---------------------------------------------------------------------------
# 3. Dispatch map completeness
# ---------------------------------------------------------------------------


def test_dispatch_map_has_canonical_step_ids() -> None:
    """Every step id verified in research/02 §1.1 has an extractor entry.

    Static IDs (12) + 1 dynamic prefix entry ('generate'). Dynamic
    'generate-{agent.id}' IDs are tested separately via prefix-match.
    """
    canonical_static = {
        "extract",
        "diff",
        "debate",
        "score",
        "merge",
        "anti-instinct",
        "test-strategy",
        "spec-fidelity",
        "wiring-verification",
        "deviation-analysis",
        "remediate",
        "certify",
    }
    canonical_all = canonical_static | {"generate"}
    assert canonical_all <= set(POST_EXTRACTORS.keys())


def test_dispatch_resolves_dynamic_generate_ids() -> None:
    """get_post_extractor resolves dynamic 'generate-{agent.id}' via prefix-match.

    Resolves to the SAME extractor function for every dynamic agent id —
    the function keys its ArtifactRef by ``artifact_path.stem`` internally.
    """
    generate_a = get_post_extractor("generate-opus-architect")
    generate_b = get_post_extractor("generate-sonnet-qa")
    assert generate_a is not None
    assert generate_a is generate_b
    # Unknown step IDs resolve to None (caller treats as no-op)
    assert get_post_extractor("not-a-real-step") is None


# ---------------------------------------------------------------------------
# 4. Dispatch reachability (sc:reflect UC-1 G1 / Contract #2)
# ---------------------------------------------------------------------------


def test_dispatch_reachable_from_production_entry_point() -> None:
    """AST walk: get_post_extractor is reachable from a production entry point.

    Contract #2 / sc:reflect UC-1 G1: map-completeness alone is necessary
    but NOT sufficient — the dispatch must be reachable from a real
    StepRunner entry point. The chain is:

        roadmap_run_step (production callback registered at executor.py)
          → _apply_post_step_envelope_update
          → get_post_extractor → POST_EXTRACTORS

    This test walks the executor.py AST and verifies both edges of that
    chain are statically present.
    """
    import superclaude.cli.roadmap.executor as executor_mod

    source = Path(executor_mod.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)

    def function_calls(fn_name: str) -> set[str]:
        """Collect all called identifiers within the body of fn_name."""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == fn_name:
                calls: set[str] = set()
                for child in ast.walk(node):
                    if isinstance(child, ast.Call):
                        func = child.func
                        if isinstance(func, ast.Name):
                            calls.add(func.id)
                        elif isinstance(func, ast.Attribute):
                            calls.add(func.attr)
                return calls
        return set()

    wrapper_calls = function_calls("roadmap_run_step")
    helper_calls = function_calls("_apply_post_step_envelope_update")

    # Edge 1: wrapper → helper
    assert "_apply_post_step_envelope_update" in wrapper_calls, (
        "roadmap_run_step wrapper must invoke _apply_post_step_envelope_update"
    )
    # Edge 2: helper → dispatch
    assert "get_post_extractor" in helper_calls, (
        "_apply_post_step_envelope_update must invoke get_post_extractor"
    )


# ---------------------------------------------------------------------------
# 5. Field-set conformance (sc:reflect UC-1 G3 / R1.1 OQ-1 parallel)
# ---------------------------------------------------------------------------


def test_field_set_matches_mvr_section_1() -> None:
    """PipelineEnvelope field set is exactly the §MVR §1 canonical 8-field set.

    Catches future drift from BUILD-REQUEST §MVR §1 lines 89-99. Parallel
    to Phase 6 OQ-1 (the same shape was applied to AdversarialReturn).
    """
    canonical = {
        "release_id",
        "spec_hash",
        "spec_ids",
        "artifacts",
        "findings",
        "counts",
        "convergence",
        "accepted_deviations",
    }
    actual = {f.name for f in dataclasses.fields(PipelineEnvelope)}
    assert actual == canonical


# ---------------------------------------------------------------------------
# 6. Dual-write preservation
# ---------------------------------------------------------------------------


def test_dual_write_does_not_mutate_markdown(
    sample_envelope: PipelineEnvelope, tmp_path: Path
) -> None:
    """Invoking the post-step extractor never mutates the step's artifact.

    The envelope is additive — it records an ArtifactRef pointing at the
    markdown. The markdown bytes must be identical before and after.
    """
    from superclaude.cli.roadmap.envelope import (
        extract_extract_envelope_fields,
    )

    artifact = tmp_path / "extract.md"
    artifact.write_text("# extract\n\n## FRs\nFR-1\nFR-2\n", encoding="utf-8")
    before = artifact.read_bytes()

    updated = extract_extract_envelope_fields(artifact, sample_envelope)
    after = artifact.read_bytes()

    # Markdown bytes unchanged
    assert before == after
    # Envelope was additively updated: extract entry now references this artifact
    assert "extract" in updated.artifacts
    assert updated.artifacts["extract"].path == artifact
    assert len(updated.artifacts["extract"].content_hash) == 16
