"""R1.5 / §MVR §4 — fail-closed ``verify-implementation`` terminal-gate tests.

Exercises ``cli/roadmap/verify_implementation.assert_all_frs_resolved`` (the
``CodeAssertion``-only terminal gate that REPLACES the legacy
``wiring-verification`` shadow step) and its dispatch wiring.

Master:§Flaw 1 invariant under test — a green pipeline must NOT certify a
roadmap that silently dropped a functional requirement. The assertion is
fail-closed (Contract #4): an empty ``fr_ids`` set or any unresolved FR
yields a HIGH ``Finding`` rather than a silent PASS.

Resolution substrate (design §5, LOAD-BEARING): FRs resolve against the
run's OWN emitted tasklist/roadmap artifacts (``envelope.artifacts`` →
``ArtifactRef.path``, whole-token regex) OR an accepted-deviation channel
(``spec_ids.accepted_deviation_ids`` ∪ ``accepted_deviations[*].id``) —
NEVER the pipeline's own ``src/`` source tree. The source-tree path is
CI-only and is never asserted against the live gate here.

Design source of truth:
``.dev/tasks/to-do/TASK-RF-20260531-042405/phase-outputs/plans/
r1-5-verify-implementation-design.md``
"""

from __future__ import annotations

import ast
import inspect
from pathlib import Path

import pytest

from superclaude.cli.roadmap.envelope import (
    AcceptedDeviation,
    ArtifactRef,
    PipelineEnvelope,
)
from superclaude.cli.roadmap.executor import _build_steps, _get_all_step_ids
from superclaude.cli.roadmap.gates import ALL_GATES
from superclaude.cli.roadmap.id_registry import SpecIdRegistry
from superclaude.cli.roadmap.models import AgentSpec, RoadmapConfig
from superclaude.cli.roadmap.verify_implementation import (
    assert_all_frs_resolved,
    build_verify_implementation_step,
)

# Repo root: tests/roadmap/test_verify_implementation.py -> parents[2].
REPO_ROOT = Path(__file__).resolve().parents[2]


# ---------------------------------------------------------------------------
# Builders — construct the REAL types per the 10.2 API (no guessing).
# ---------------------------------------------------------------------------


def _make_registry(
    fr_ids: tuple[str, ...],
    accepted_deviation_ids: tuple[str, ...] = (),
) -> SpecIdRegistry:
    """Construct a frozen :class:`SpecIdRegistry` with the given FR set.

    All non-FR families are empty; only ``fr_ids`` and
    ``accepted_deviation_ids`` are load-bearing for the FR-resolution gate.
    """
    return SpecIdRegistry(
        fr_ids=fr_ids,
        nfr_ids=(),
        sc_ids=(),
        g_ids=(),
        d_ids=(),
        md_ids=(),
        accepted_deviation_ids=accepted_deviation_ids,
        spec_hash="deadbeefdeadbeef",
        spec_path=Path("spec.md"),
    )


def _make_envelope(
    spec_ids: SpecIdRegistry,
    artifacts: dict[str, ArtifactRef] | None = None,
    accepted_deviations: list[AcceptedDeviation] | None = None,
) -> PipelineEnvelope:
    """Construct a :class:`PipelineEnvelope` with the given registry + artifacts."""
    return PipelineEnvelope(
        release_id="r1-5-test",
        spec_hash="deadbeefdeadbeef",
        spec_ids=spec_ids,
        artifacts=artifacts or {},
        findings=[],
        counts={},
        convergence=None,
        accepted_deviations=accepted_deviations or [],
    )


def _write_artifact_ref(tmp_path: Path, name: str, text: str) -> ArtifactRef:
    """Write a small fixture artifact under ``tmp_path`` and return its ref.

    Channel (a) substrate: the FR tokens that resolve must appear in the
    run's OWN emitted artifact text — NOT an importable callable in the dev
    tree (that only passes under a dev checkout). Resolution is via artifact
    text, exactly as the live gate consumes it.
    """
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return ArtifactRef(path=path, content_hash="0" * 16)


def _make_config(tmp_path: Path) -> RoadmapConfig:
    """Minimal RoadmapConfig for the step-count budget test (mirrors test_executor)."""
    spec = tmp_path / "spec.md"
    spec.write_text("# Test Spec\nContent for testing.\n")
    output = tmp_path / "output"
    output.mkdir(exist_ok=True)
    return RoadmapConfig(
        spec_file=spec,
        output_dir=output,
        agents=[AgentSpec("opus", "architect"), AgentSpec("haiku", "architect")],
        depth="standard",
    )


# ---------------------------------------------------------------------------
# Core resolution semantics
# ---------------------------------------------------------------------------


def test_all_frs_resolve(tmp_path):
    """Every FR resolves against the run's own emitted artifacts → PASS (None).

    Resolution is via artifact TEXT (channel a), not a dev-tree importable
    callable: a fixture roadmap/tasklist file is written containing the FR
    tokens, and ``envelope.artifacts`` points at it.
    """
    fr_ids = ("FR-001", "FR-002", "FR-003")
    roadmap_ref = _write_artifact_ref(
        tmp_path,
        "roadmap.md",
        "# Roadmap\n- M1 covers FR-001 and FR-002.\n",
    )
    tasklist_ref = _write_artifact_ref(
        tmp_path,
        "tasklist.md",
        "# Tasklist\n- Implement FR-003 in the auth module.\n",
    )
    envelope = _make_envelope(
        _make_registry(fr_ids),
        artifacts={"merge": roadmap_ref, "test-strategy": tasklist_ref},
    )

    result = assert_all_frs_resolved(envelope)
    assert result is None, (
        "Expected PASS (None) when every FR resolves against emitted artifacts; "
        f"got Finding: {getattr(result, 'description', result)!r}"
    )


def test_unresolved_fr_halts(tmp_path):
    """An FR absent from all artifacts + not accepted → HIGH Finding (fail-closed)."""
    fr_ids = ("FR-001", "FR-002", "FR-999")
    roadmap_ref = _write_artifact_ref(
        tmp_path,
        "roadmap.md",
        "# Roadmap\n- M1 covers FR-001 and FR-002.\n",  # FR-999 absent
    )
    envelope = _make_envelope(
        _make_registry(fr_ids),
        artifacts={"merge": roadmap_ref},
    )

    result = assert_all_frs_resolved(envelope)
    assert result is not None, "Expected a Finding for the unresolved FR-999"
    assert result.severity == "HIGH"
    assert result.id == "CA-VERIFY-IMPL-001"
    assert result.dimension == "fr-resolution"
    # The unresolved FR is named in the evidence; the resolved ones are not flagged.
    assert "FR-999" in result.description
    assert "FR-999" in result.evidence


def test_accepted_deviation_resolves(tmp_path):
    """An otherwise-unresolvable FR with a matching accepted deviation → PASS.

    Covers BOTH accepted-deviation channels (design §5.1 b + c):
    ``spec_ids.accepted_deviation_ids`` (b) and an ``accepted_deviations``
    record's ``id`` (c).
    """
    fr_ids = ("FR-001", "FR-DEV-B", "FR-DEV-C")
    roadmap_ref = _write_artifact_ref(
        tmp_path,
        "roadmap.md",
        "# Roadmap\n- M1 covers FR-001 only.\n",  # neither deviation FR present
    )
    envelope = _make_envelope(
        _make_registry(fr_ids, accepted_deviation_ids=("FR-DEV-B",)),
        artifacts={"merge": roadmap_ref},
        accepted_deviations=[
            AcceptedDeviation(
                id="FR-DEV-C",
                reason="Deferred to next release per stakeholder sign-off.",
                timestamp="2026-06-02T00:00:00Z",
            )
        ],
    )

    result = assert_all_frs_resolved(envelope)
    assert result is None, (
        "Expected PASS (None): FR-001 resolves via artifact, FR-DEV-B via "
        "spec_ids.accepted_deviation_ids, FR-DEV-C via accepted_deviations "
        f"record; got Finding: {getattr(result, 'description', result)!r}"
    )


def test_empty_fr_set():
    """Empty ``fr_ids`` → Finding (Contract #4: NOT a silent PASS)."""
    envelope = _make_envelope(_make_registry(fr_ids=()))

    result = assert_all_frs_resolved(envelope)
    assert result is not None, (
        "Contract #4: an empty FR token set MUST NOT silently PASS — "
        "expected a Finding."
    )
    assert result.severity == "HIGH"
    assert result.id == "CA-VERIFY-IMPL-000"
    assert result.dimension == "fr-resolution"
    assert result.location == "envelope.spec_ids.fr_ids"


# ---------------------------------------------------------------------------
# Accessor-guard regression (envelope.spec_ids.fr_ids accessor, not subscript)
# ---------------------------------------------------------------------------


def test_accessor_not_subscript(tmp_path):
    """``assert_all_frs_resolved`` uses the ``.fr_ids`` accessor; subscript raises.

    Guards the regression where a caller might index ``envelope.spec_ids[FR]``.
    The frozen :class:`SpecIdRegistry` dataclass is not subscriptable, so any
    such access raises ``TypeError`` — the source uses the accessor instead.
    """
    fr_ids = ("FR-001",)
    roadmap_ref = _write_artifact_ref(tmp_path, "roadmap.md", "covers FR-001\n")
    registry = _make_registry(fr_ids)
    envelope = _make_envelope(registry, artifacts={"merge": roadmap_ref})

    # The accessor the source actually uses resolves correctly.
    assert envelope.spec_ids.fr_ids == fr_ids
    assert assert_all_frs_resolved(envelope) is None

    # Subscripting the registry (the regression shape) raises TypeError.
    with pytest.raises(TypeError):
        envelope.spec_ids["FR-001"]  # type: ignore[index]


# ---------------------------------------------------------------------------
# Dispatch reachability (mirrors test_dispatch_reachability.py)
# ---------------------------------------------------------------------------


def _build_verify_step_has_production_caller(tree: ast.Module) -> bool:
    """True iff ``build_verify_implementation_step(...)`` is called in executor.py.

    Mirrors ``code_assertions._build_certify_step_has_production_caller``: a
    direct ``Call`` whose ``.func`` is ``Name("build_verify_implementation_step")``
    anywhere outside the function's own definition constitutes a production
    caller (executor.py is the pipeline-driver module).
    """
    def_node: ast.FunctionDef | None = None
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.FunctionDef)
            and node.name == "build_verify_implementation_step"
        ):
            def_node = node
            break
    def_lineno = def_node.lineno if def_node is not None else -1
    def_end = getattr(def_node, "end_lineno", def_lineno) if def_node else -1

    for node in ast.walk(tree):
        if not (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "build_verify_implementation_step"
        ):
            continue
        call_line = getattr(node, "lineno", -1)
        if def_node is not None and def_lineno <= call_line <= def_end:
            continue
        return True
    return False


def _function_called_in(tree: ast.Module, caller: str, callee: str) -> bool:
    """True iff ``callee(...)`` is invoked within the body of ``def caller``."""
    for node in ast.walk(tree):
        if not (isinstance(node, ast.FunctionDef) and node.name == caller):
            continue
        for inner in ast.walk(node):
            if (
                isinstance(inner, ast.Call)
                and isinstance(inner.func, ast.Name)
                and inner.func.id == callee
            ):
                return True
    return False


def test_step_in_dispatch_map():
    """``verify-implementation`` is wired into the pipeline dispatch (dynamic).

    Reachability mirrors the R1.3 ``assert_step_reachable`` walker shape: the
    terminal step is dispatched DYNAMICALLY after certify, so reachability is
    demonstrated by (1) registration in ``ALL_GATES`` + ``_get_all_step_ids``,
    and (2) an AST proof that ``build_verify_implementation_step`` has a
    production caller in executor.py, invoked from ``execute_roadmap`` via
    ``_run_verify_implementation`` — exactly the dynamic-after-certify wiring.
    """
    # (1) Registered in the gate registry + the all-step-ids resolver.
    gate_names = {name for name, _ in ALL_GATES}
    assert "verify-implementation" in gate_names, (
        "verify-implementation must be registered in ALL_GATES"
    )

    executor_path = (
        REPO_ROOT / "src" / "superclaude" / "cli" / "roadmap" / "executor.py"
    )
    tree = ast.parse(executor_path.read_text(encoding="utf-8"))

    # (2) build_verify_implementation_step has a production caller in executor.py.
    assert _build_verify_step_has_production_caller(tree), (
        "build_verify_implementation_step has no production caller in "
        "executor.py — the terminal step would ship unwired (master:§Flaw 1)."
    )

    # (3) The caller is _run_verify_implementation, dispatched from execute_roadmap
    #     AFTER certify (dynamic-after-certify wiring, design §2/§7.3).
    assert _function_called_in(
        tree, "_run_verify_implementation", "build_verify_implementation_step"
    ), "_run_verify_implementation must build the verify-implementation step"
    assert _function_called_in(tree, "execute_roadmap", "_run_verify_implementation"), (
        "execute_roadmap must dispatch _run_verify_implementation (after certify)"
    )


def test_step_count_budget(tmp_path):
    """Acceptance Gate #6 — total dispatched steps stay ≤ 14 (regression guard).

    Step-count basis (mirrors test_executor.test_get_all_step_ids_includes_certify):
    static ``_build_steps`` flattened + the two dynamic steps (certify +
    verify-implementation) == ``_get_all_step_ids`` == ``len(ALL_GATES)`` == 14.
    verify-implementation REPLACES wiring-verification, so the net delta is 0.
    """
    config = _make_config(tmp_path)
    steps = _build_steps(config)
    flat_count = sum(len(s) if isinstance(s, list) else 1 for s in steps)

    all_ids = _get_all_step_ids(config)
    # Static flattened + 2 dynamic (certify + verify-implementation).
    assert len(all_ids) == flat_count + 2
    # The budget invariant: total dispatched steps ≤ 14.
    assert len(all_ids) <= 14
    assert len(all_ids) == 14
    # ALL_GATES is the documented step-count basis and must match.
    assert len(ALL_GATES) <= 14
    assert len(ALL_GATES) == 14
    # verify-implementation present; legacy wiring-verification gone.
    assert "verify-implementation" in all_ids
    assert "wiring-verification" not in all_ids


# ---------------------------------------------------------------------------
# CI-only: source-tree resolution is NOT the live gate (design §5.2).
# Asserted here ONLY as documentation of the non-runtime path; the live gate
# resolves via artifacts, exercised above. No assertion couples the gate to
# the src/ tree.
# ---------------------------------------------------------------------------


def test_repo_path_is_path_normalisation_only(tmp_path):
    """``repo_path`` normalises a RELATIVE artifact path; it is not src/ scanning.

    Design §4.1/§5.2: ``repo_path`` exists for signature-parity with the
    dispatch contract and to resolve a relative artifact path against the run
    dir — NOT to resolve FRs against the pipeline's own source tree.
    """
    fr_ids = ("FR-100",)
    # Write the artifact under tmp_path; reference it by a RELATIVE path so the
    # gate must join it against repo_path to read it.
    (tmp_path / "roadmap.md").write_text("covers FR-100\n", encoding="utf-8")
    rel_ref = ArtifactRef(path=Path("roadmap.md"), content_hash="0" * 16)
    envelope = _make_envelope(_make_registry(fr_ids), artifacts={"merge": rel_ref})

    # Without repo_path the relative artifact cannot be read → unresolved (FAIL).
    miss = assert_all_frs_resolved(envelope)
    assert miss is not None and miss.id == "CA-VERIFY-IMPL-001"

    # With repo_path the relative path normalises and the FR resolves (PASS).
    hit = assert_all_frs_resolved(envelope, repo_path=tmp_path)
    assert hit is None


def test_build_verify_implementation_step_shape(tmp_path):
    """The terminal Step builder returns a code-assertion-only Step (no LLM prompt)."""
    config = _make_config(tmp_path)
    step = build_verify_implementation_step(config)
    assert step.id == "verify-implementation"
    assert step.prompt == ""  # code-assertion-only; no LLM invocation
    assert step.retry_limit == 0

    # Signature parity: assert_all_frs_resolved accepts (envelope, repo_path).
    sig = inspect.signature(assert_all_frs_resolved)
    params = list(sig.parameters)
    assert params[0] == "envelope"
    assert params[1] == "repo_path"
