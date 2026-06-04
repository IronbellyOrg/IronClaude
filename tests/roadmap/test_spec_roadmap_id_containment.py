"""Contract #9 regression tests — Spec-ID registry & MERGE_GATE containment.

Source authority:
    - BUILD-REQUEST §R0 item 1
    - BUILD-REQUEST §Contract item #9
    - master:§Recurrence #4 (A12:F-A12-01 — TUIBBS v1-MVP phantom IDs)
    - Phase 2 of TASK-RF-20260531-042405 (Steps 2.5, 2.6)

Contract #1 invariant: each test MUST FAIL pre-fix (before Phase 2 lands)
and MUST PASS post-fix. The MERGE_GATE assertion (Step 2.4) and the
sidecar-write hook (Step 2.3) together provide the post-fix behavior.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from superclaude.cli.roadmap import gates as _gates
from superclaude.cli.roadmap.id_registry import (
    SpecIdRegistry,
    build_id_registry,
    extract_roadmap_ids,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _slice_section(text: str, heading: str) -> str:
    """Return the H2 section body (heading exclusive, next H2 exclusive).

    Used by the test fixture to slice ``## spec`` and ``## roadmap``
    sections out of ``spec_roadmap_drift_case.md`` without needing two
    separate files. Matches loose markdown semantics.
    """
    marker = f"\n## {heading}\n"
    if marker not in text:
        # Try without leading newline (file starts with the section).
        marker = f"## {heading}\n"
    start = text.index(marker) + len(marker)
    # Find next "## " heading after start
    rest = text[start:]
    nxt = rest.find("\n## ")
    return rest if nxt == -1 else rest[:nxt]


def _write_spec(tmp_path: Path, spec_body: str) -> Path:
    spec = tmp_path / "spec.md"
    spec.write_text(spec_body, encoding="utf-8")
    return spec


@pytest.fixture(autouse=True)
def _isolate_gates_state():
    """Clear the gates-module sidecar hint between tests (test hygiene)."""
    _gates.set_id_registry_sidecar_path(None)
    yield
    _gates.set_id_registry_sidecar_path(None)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "recurrence_case",
    [("id_containment", "spec_roadmap_drift_case")],
    indirect=True,
)
def test_phantom_id_rejected(recurrence_case, tmp_path):
    """The MERGE_GATE SemanticCheck flags the master:§Recurrence #4 case."""
    input_path, expected = recurrence_case
    case_text = input_path.read_text(encoding="utf-8")
    spec_body = _slice_section(case_text, "spec")
    roadmap_body = _slice_section(case_text, "roadmap")

    spec_path = _write_spec(tmp_path, spec_body)
    registry = build_id_registry(spec_path)

    # Persist sidecar at the conventional location and register with gates.
    sidecar = tmp_path / "spec_id_registry.json"
    sidecar.write_text(
        json.dumps(registry.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    _gates.set_id_registry_sidecar_path(sidecar)

    # Sanity: spec IDs match the fixture expectation.
    expected_spec_ids = expected["expected_spec_ids"]
    assert sorted(registry.fr_ids) == sorted(expected_spec_ids["fr_ids"])
    assert sorted(registry.nfr_ids) == sorted(expected_spec_ids["nfr_ids"])
    assert sorted(registry.d_ids) == sorted(expected_spec_ids["d_ids"])

    # Drive the gate check.
    result = _gates._roadmap_ids_within_spec(roadmap_body)

    assert isinstance(result, str), (
        f"Expected failure string (phantom IDs present); got {result!r}"
    )
    expected_substring = expected["expected_failure_substring"]
    assert expected_substring in result, (
        f"Expected failure message to contain {expected_substring!r}; got {result!r}"
    )


@pytest.mark.parametrize(
    "recurrence_case",
    [("id_containment", "spec_roadmap_drift_case")],
    indirect=True,
)
def test_registry_contains_method(recurrence_case, tmp_path):
    """SpecIdRegistry.contains honors both real and phantom IDs."""
    input_path, expected = recurrence_case
    case_text = input_path.read_text(encoding="utf-8")
    spec_body = _slice_section(case_text, "spec")
    spec_path = _write_spec(tmp_path, spec_body)
    registry = build_id_registry(spec_path)

    assert registry.contains("FR-1") is expected["expected_contains_fr_1"]
    assert registry.contains("FR-99") is expected["expected_contains_fr_99"]


def test_spec_ids_contained_when_roadmap_matches_spec(tmp_path):
    """Anti-regression: a roadmap with no phantom IDs PASSES the gate."""
    spec_body = (
        "- **FR-1** Authentication.\n"
        "- **NFR-1** Performance budget.\n"
        "- **D1** Legacy session token format.\n"
    )
    roadmap_body = (
        "| # | ID | Title |\n"
        "|---|----|-------|\n"
        "| 1 | FR-1 | Auth |\n"
        "| 2 | NFR-1 | Perf |\n"
        "| 3 | D1 | Legacy |\n"
    )
    spec_path = _write_spec(tmp_path, spec_body)
    registry = build_id_registry(spec_path)
    sidecar = tmp_path / "spec_id_registry.json"
    sidecar.write_text(json.dumps(registry.to_dict()), encoding="utf-8")
    _gates.set_id_registry_sidecar_path(sidecar)

    result = _gates._roadmap_ids_within_spec(roadmap_body)
    assert result is True, f"Expected True; got {result!r}"


def test_accepted_deviation_allows_otherwise_phantom_id(tmp_path):
    """Accepted deviations widen the known set per Contract #9 wording."""
    spec_body = "- **FR-1** Auth.\n"
    roadmap_body = "| 1 | FR-1 | x |\n| 2 | FR-42 | accepted deviation |\n"
    spec_path = _write_spec(tmp_path, spec_body)
    registry = build_id_registry(spec_path, accepted_deviations=["FR-42"])
    sidecar = tmp_path / "spec_id_registry.json"
    sidecar.write_text(json.dumps(registry.to_dict()), encoding="utf-8")
    _gates.set_id_registry_sidecar_path(sidecar)

    assert _gates._roadmap_ids_within_spec(roadmap_body) is True


def test_fail_shut_when_sidecar_missing():
    """master:§Flaw 4 — no fail-open defaults; missing sidecar => failure."""
    # _isolate_gates_state already cleared the hint to None.
    result = _gates._roadmap_ids_within_spec("FR-1")
    assert isinstance(result, str), "Missing sidecar must NOT silently pass"
    assert "Contract #9" in result


def test_fail_shut_when_sidecar_unreadable(tmp_path):
    """Unreadable sidecar still returns a failure string, not True."""
    bogus = tmp_path / "does-not-exist.json"
    _gates.set_id_registry_sidecar_path(bogus)
    result = _gates._roadmap_ids_within_spec("FR-1")
    assert isinstance(result, str)
    assert "Contract #9" in result


def test_r2_run_start_reset_closes_stale_sidecar_leak(tmp_path):
    """R2: a fresh second in-process run that skips extract must NOT validate
    its roadmap against the PREVIOUS run's spec registry, and a legitimate
    --resume must re-point at its OWN persisted sidecar (resume-aware).

    Single test body by design: the autouse ``_isolate_gates_state`` fixture
    only clears the gates global BETWEEN test functions, so the cross-run
    stale-sidecar leak can only be exercised within ONE body where that reset
    does not fire between the two simulated runs (Step 5.5 test-design hazard).

    Fail-before/pass-after: ``_reset_id_registry_sidecar_hint`` is the R2 fix —
    pre-fix it did not exist (import fails) and a fresh second run would inherit
    run-1's stale sidecar and wrongly PASS ``FR-1`` against registry A.
    """
    from superclaude.cli.roadmap.executor import _reset_id_registry_sidecar_hint

    # --- Run 1 (spec A): extract sets the sidecar hint to A's registry ---
    run1_dir = tmp_path / "run1"
    run1_dir.mkdir()
    spec_a = run1_dir / "spec.md"
    spec_a.write_text("- **FR-1** Auth.\n- **FR-2** Sessions.\n", encoding="utf-8")
    registry_a = build_id_registry(spec_a)
    sidecar_a = run1_dir / "spec_id_registry.json"
    sidecar_a.write_text(json.dumps(registry_a.to_dict()), encoding="utf-8")
    _gates.set_id_registry_sidecar_path(sidecar_a)  # what the extract step does
    assert _gates._roadmap_ids_within_spec("FR-1") is True  # FR-1 ∈ A → passes

    # --- Run 2: a FRESH second pipeline (new output dir, extract skipped) ---
    # "FR-1" IS in stale registry A, so WITHOUT the R2 run-start reset the gate
    # would WRONGLY PASS against A. The R2 reset for a fresh run clears the hint
    # to None (run2 has no own sidecar yet), so the gate MUST fail-shut.
    run2_dir = tmp_path / "run2"
    run2_dir.mkdir()
    assert not (run2_dir / "spec_id_registry.json").exists()
    _reset_id_registry_sidecar_hint(run2_dir, resume=False)  # the R2 fix
    leaked = _gates._roadmap_ids_within_spec("FR-1")
    assert isinstance(leaked, str), (
        "R2: a fresh run that skipped extract must fail-shut, not validate "
        f"against run-1's stale registry; got {leaked!r}"
    )
    assert "Contract #9" in leaked

    # --- Resume-aware: a --resume run re-points at its OWN persisted sidecar ---
    spec_b = run2_dir / "spec.md"
    spec_b.write_text("- **NFR-9** Telemetry.\n", encoding="utf-8")
    registry_b = build_id_registry(spec_b)
    (run2_dir / "spec_id_registry.json").write_text(
        json.dumps(registry_b.to_dict()), encoding="utf-8"
    )
    _reset_id_registry_sidecar_hint(run2_dir, resume=True, spec_file=spec_b)
    assert _gates._roadmap_ids_within_spec("NFR-9") is True, (
        "R2 resume-aware: a --resume run with a persisted sidecar whose "
        "spec_hash matches the current spec must re-use its own registry, "
        "not fail-shut"
    )


def test_resume_rejects_sidecar_built_from_different_spec(tmp_path):
    """PR #112 identity guard: a --resume run whose output_dir holds a sidecar
    built from a DIFFERENT (or mutated) spec must fail-shut, not validate the
    roadmap against the wrong spec's id-registry.

    Fail-before/pass-after: pre-fix, ``_reset_id_registry_sidecar_hint`` trusted
    ``<output_dir>/spec_id_registry.json`` on existence alone, so a resume against
    a mutated spec would re-point at the STALE sidecar and wrongly PASS an ID that
    only belongs to the old spec. The ``spec_hash`` identity guard now rejects the
    provenance mismatch and clears the hint to ``None`` (fail-shut).
    """
    from superclaude.cli.roadmap.executor import _reset_id_registry_sidecar_hint

    out_dir = tmp_path / "out"
    out_dir.mkdir()

    # Original run: spec contained FR-1; its registry sidecar persisted here.
    spec_old = out_dir / "spec.md"
    spec_old.write_text("- **FR-1** Legacy auth.\n", encoding="utf-8")
    registry_old = build_id_registry(spec_old)
    (out_dir / "spec_id_registry.json").write_text(
        json.dumps(registry_old.to_dict()), encoding="utf-8"
    )

    # The spec is then MUTATED in place (FR-1 removed, NFR-9 added) but the
    # stale sidecar from the original run still sits in out_dir. A --resume run
    # now targets the mutated spec.
    spec_old.write_text("- **NFR-9** Telemetry only.\n", encoding="utf-8")

    _reset_id_registry_sidecar_hint(out_dir, resume=True, spec_file=spec_old)

    # FR-1 is in the STALE sidecar but NOT in the current (mutated) spec. The
    # identity guard must have cleared the hint, so the gate fails-shut instead
    # of validating FR-1 against the wrong registry.
    leaked = _gates._roadmap_ids_within_spec("FR-1")
    assert isinstance(leaked, str), (
        "Resume against a spec whose hash differs from the persisted sidecar "
        f"must fail-shut, not validate against the stale registry; got {leaked!r}"
    )
    assert "Contract #9" in leaked


def test_sidecar_match_fail_shut_on_non_utf8_spec(tmp_path):
    """A non-UTF8 spec must fail-shut (return False), not crash --resume.

    ``UnicodeDecodeError`` is a ``ValueError`` subclass — NOT an ``OSError`` —
    so the spec-read handler must catch it explicitly, matching the docstring's
    "unknown/unreadable spec" fail-shut contract.
    """
    from superclaude.cli.roadmap.executor import _sidecar_matches_spec

    spec = tmp_path / "spec.md"
    spec.write_bytes(b"\xff\xfe invalid utf-8 \x80\x81")
    sidecar = tmp_path / "spec_id_registry.json"
    sidecar.write_text(json.dumps({"spec_hash": "deadbeefdeadbeef"}), encoding="utf-8")
    assert _sidecar_matches_spec(sidecar, spec) is False


def test_sidecar_match_fail_shut_on_non_utf8_sidecar(tmp_path):
    """A non-UTF8 sidecar must fail-shut, not raise ``UnicodeDecodeError``."""
    from superclaude.cli.roadmap.executor import _sidecar_matches_spec

    spec = tmp_path / "spec.md"
    spec.write_text("- **FR-1** Real.\n", encoding="utf-8")
    sidecar = tmp_path / "spec_id_registry.json"
    sidecar.write_bytes(b"\xff\xfe\x00 not utf-8 json \x80")
    assert _sidecar_matches_spec(sidecar, spec) is False


def test_sidecar_match_fail_shut_on_non_dict_json(tmp_path):
    """A valid-but-non-object sidecar JSON (e.g. ``[]``) must fail-shut.

    Pre-fix, ``json.loads`` returns a list and ``payload.get("spec_hash")``
    raises ``AttributeError``; the ``isinstance(payload, dict)`` guard now
    declines the sidecar instead of crashing.
    """
    from superclaude.cli.roadmap.executor import _sidecar_matches_spec

    spec = tmp_path / "spec.md"
    spec.write_text("- **FR-1** Real.\n", encoding="utf-8")
    sidecar = tmp_path / "spec_id_registry.json"
    sidecar.write_text("[]", encoding="utf-8")
    assert _sidecar_matches_spec(sidecar, spec) is False


def test_extract_roadmap_ids_reuses_canonical_extractor():
    """Contract #8: no duplicate regex literals — must use spec_parser."""
    sample = "Roadmap references FR-1, NFR-2, SC-3, G-4, D-5, and D6."
    extracted = extract_roadmap_ids(sample)
    assert extracted == frozenset({"FR-1", "NFR-2", "SC-3", "G-4", "D-5", "D6"})


def test_registry_is_immutable_and_hashable(tmp_path):
    """SpecIdRegistry is frozen — required for envelope absorption (R1.2)."""
    spec_body = "- FR-1 stuff.\n"
    spec_path = _write_spec(tmp_path, spec_body)
    registry = build_id_registry(spec_path)
    # Frozen dataclass — mutation must raise.
    with pytest.raises(Exception):
        registry.fr_ids = ("FR-2",)  # type: ignore[misc]
    # Hashable.
    {registry}


def test_registry_sidecar_schema_stable(tmp_path):
    """to_dict() must produce the JSON schema the R0.1 sidecar contract promises."""
    spec_body = "- FR-1 x.\n- NFR-1 y.\n- D1 z.\n"
    spec_path = _write_spec(tmp_path, spec_body)
    registry = build_id_registry(spec_path, accepted_deviations=["FR-99"])
    payload = registry.to_dict()
    expected_keys = {
        "fr_ids",
        "nfr_ids",
        "sc_ids",
        "g_ids",
        "d_ids",
        "md_ids",
        "accepted_deviation_ids",
        "spec_hash",
        "spec_path",
    }
    assert set(payload.keys()) == expected_keys
    assert payload["fr_ids"] == ["FR-1"]
    assert payload["accepted_deviation_ids"] == ["FR-99"]
    # spec_hash is 16-char hex (sha256 prefix).
    assert isinstance(payload["spec_hash"], str)
    assert len(payload["spec_hash"]) == 16


def test_build_id_registry_picks_up_d_lenient_family(tmp_path):
    """Documents the lenient D-family extraction master:§Recurrence #4 cites."""
    spec_body = "- D1 alpha.\n- D-2 beta.\n- D3 gamma.\n"
    spec_path = _write_spec(tmp_path, spec_body)
    registry = build_id_registry(spec_path)
    # Both D1 and D-2 surface forms are extracted as-is (no canonicalization).
    assert "D1" in registry.d_ids
    assert "D-2" in registry.d_ids
    assert "D3" in registry.d_ids


def test_sidecar_schema_round_trip(tmp_path):
    """The sidecar JSON must round-trip into SpecIdRegistry without loss."""
    spec_body = "- FR-1 x.\n- NFR-1 y.\n"
    spec_path = _write_spec(tmp_path, spec_body)
    registry = build_id_registry(spec_path, accepted_deviations=["FR-42"])
    sidecar = tmp_path / "spec_id_registry.json"
    sidecar.write_text(
        json.dumps(registry.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )

    payload = json.loads(sidecar.read_text(encoding="utf-8"))
    reconstructed = SpecIdRegistry(
        fr_ids=tuple(payload["fr_ids"]),
        nfr_ids=tuple(payload["nfr_ids"]),
        sc_ids=tuple(payload["sc_ids"]),
        g_ids=tuple(payload["g_ids"]),
        d_ids=tuple(payload["d_ids"]),
        md_ids=tuple(payload["md_ids"]),
        accepted_deviation_ids=tuple(payload["accepted_deviation_ids"]),
        spec_hash=payload["spec_hash"],
        spec_path=Path(payload["spec_path"]),
    )
    assert reconstructed == registry
