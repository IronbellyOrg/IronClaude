"""Contract #2 / master:§Flaw 1 — dispatch-reachability CodeAssertion tests (R1.3).

Verifies the first ``GateCriteria.code_assertions`` predicate
(``cli/roadmap/code_assertions.assert_step_reachable``) genuinely enforces
that the terminal ``certify`` step is reachable from a production dispatch
path, that the ``code_assertions`` slot does not silently weaken any STRICT
gate, and that every ``CodeAssertion.check_fn`` honours the widened
``(PipelineEnvelope, Path) -> Finding | None`` return contract from §MVR §2.

Design source of truth:
``.dev/tasks/to-do/TASK-RF-20260531-042405/phase-outputs/plans/r1-3-codeassertion-design.md``
"""

from __future__ import annotations

import inspect
from pathlib import Path

from superclaude.cli.roadmap.code_assertions import (
    assert_envelope_artifacts_present,
    assert_step_reachable,
)
from superclaude.cli.roadmap.gates import ALL_GATES, CERTIFY_GATE

# Repo root: tests/roadmap/test_dispatch_reachability.py -> parents[2].
REPO_ROOT = Path(__file__).resolve().parents[2]


# Minimal synthetic executor.py with a _build_steps that OMITS certify and
# NO build_certify_step caller — reproduces the pre-R1.3 master:§Flaw 1 state.
_UNWIRED_EXECUTOR_SRC = '''\
"""synthetic executor for the unwired-state test."""


def _build_steps(config):
    return [
        Step(id="extract", prompt="", output_file=None, gate=None, timeout_seconds=1),
        Step(id="merge", prompt="", output_file=None, gate=None, timeout_seconds=1),
        Step(id="remediate", prompt="", output_file=None, gate=None, timeout_seconds=1),
    ]


def build_certify_step(config):
    # Defined but never called from any production dispatch (the Flaw 1 state).
    return Step(id="certify", prompt="", output_file=None, gate=None, timeout_seconds=1)


def execute_roadmap(config):
    steps = _build_steps(config)
    return steps
'''


def _write_synthetic_repo(tmp_path: Path, executor_src: str) -> Path:
    """Materialise a fake repo_root whose executor.py is ``executor_src``."""
    exec_path = tmp_path / "src" / "superclaude" / "cli" / "roadmap" / "executor.py"
    exec_path.parent.mkdir(parents=True, exist_ok=True)
    exec_path.write_text(executor_src, encoding="utf-8")
    return tmp_path


def test_certify_step_reachable():
    """The real executor.py wires certify -> assertion returns None (PASS)."""
    # envelope is unused by this assertion (del envelope); None is fine.
    result = assert_step_reachable(envelope=None, repo_root=REPO_ROOT)
    assert result is None, (
        "Expected certify reachable in production executor.py, got a Finding: "
        f"{getattr(result, 'description', result)!r}"
    )


def test_unwired_step_caught(tmp_path):
    """A synthetic executor without certify wiring yields a HIGH Finding."""
    repo = _write_synthetic_repo(tmp_path, _UNWIRED_EXECUTOR_SRC)
    result = assert_step_reachable(envelope=None, repo_root=repo)
    assert result is not None, "Expected a Finding for the unwired certify state"
    assert result.severity == "HIGH"
    assert result.id == "CA-DISPATCH-002"
    assert "certify" in result.description


def test_wired_via_build_steps_literal_passes(tmp_path):
    """Static shape: certify as a _build_steps Step literal also passes."""
    wired_src = _UNWIRED_EXECUTOR_SRC.replace(
        '        Step(id="remediate", prompt="", output_file=None, gate=None, timeout_seconds=1),\n',
        '        Step(id="remediate", prompt="", output_file=None, gate=None, timeout_seconds=1),\n'
        '        Step(id="certify", prompt="", output_file=None, gate=None, timeout_seconds=1),\n',
    )
    repo = _write_synthetic_repo(tmp_path, wired_src)
    assert assert_step_reachable(envelope=None, repo_root=repo) is None


def test_executor_missing_yields_finding(tmp_path):
    """A repo_root with no executor.py yields the CA-DISPATCH-001 Finding."""
    result = assert_step_reachable(envelope=None, repo_root=tmp_path)
    assert result is not None
    assert result.id == "CA-DISPATCH-001"
    assert result.severity == "HIGH"


def test_all_strict_gates_have_assertions():
    """No STRICT gate is silently empty.

    A STRICT-tier gate with neither ``semantic_checks`` nor
    ``code_assertions`` degrades to STANDARD behaviour — a silent PASS at
    the STRICT level (Contract #4 spirit, as cited by Step 8.4). The
    invariant therefore targets STRICT gates specifically.

    STANDARD/LIGHT/EXEMPT gates are intentionally excluded: they gate on
    frontmatter fields + min_lines (STANDARD) or existence (LIGHT) or
    nothing (EXEMPT) by design, so emptiness there is not a silent STRICT
    pass. The companion assertion below ensures such gates remain
    non-STRICT — if a future edit promotes ``diff``/``score`` to STRICT
    without adding checks, this test catches the regression.
    """
    for name, gate in ALL_GATES:
        has_checks = bool(gate.semantic_checks) or bool(gate.code_assertions)
        if gate.enforcement_tier == "STRICT":
            assert has_checks, (
                f"STRICT gate {name!r} has neither semantic_checks nor "
                f"code_assertions — it is a silent PASS (Contract #4 spirit)."
            )
        elif not has_checks:
            # Non-STRICT gate without checks: confirm it is genuinely a
            # lower tier (frontmatter/line/existence gating), not STRICT.
            assert gate.enforcement_tier in ("STANDARD", "LIGHT", "EXEMPT"), (
                f"Gate {name!r} has no checks but tier is "
                f"{gate.enforcement_tier!r} (expected STANDARD/LIGHT/EXEMPT)."
            )


def test_certify_gate_has_code_assertion():
    """CERTIFY_GATE carries the R1.3 dispatch-reachability CodeAssertion."""
    assert CERTIFY_GATE.code_assertions, "CERTIFY_GATE must define code_assertions"
    names = {ca.name for ca in CERTIFY_GATE.code_assertions}
    assert "step_reachable" in names


def test_codeassertion_signature_invariant():
    """Every CodeAssertion check_fn returns ``Finding | None`` (§MVR §2).

    With ``from __future__ import annotations`` the return annotation is a
    string; assert each public assertion's return annotation is exactly
    ``"Finding | None"`` and that it accepts the widened
    ``(envelope, repo_root)`` parameter pair.
    """
    assertion_fns = [assert_step_reachable, assert_envelope_artifacts_present]
    # Include the check_fn wired into CERTIFY_GATE so the live gate is covered.
    assertion_fns.extend(ca.check_fn for ca in (CERTIFY_GATE.code_assertions or []))

    for fn in assertion_fns:
        sig = inspect.signature(fn)
        assert sig.return_annotation == "Finding | None", (
            f"{fn.__name__} return annotation is {sig.return_annotation!r}, "
            "expected 'Finding | None' (§MVR §2 widened access)."
        )
        params = list(sig.parameters)
        assert params[:2] == ["envelope", "repo_root"], (
            f"{fn.__name__} params are {params!r}, expected leading "
            "(envelope, repo_root)."
        )
