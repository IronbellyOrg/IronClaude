"""Contract #4 CI lint -- no gate silently PASSes on an empty/wrong target.

BUILD-REQUEST §Contract #4 forbids a gate returning PASS on empty or
wrong-target input (the fail-open / vacuous-pass failure mode). This lint
iterates every gate registered in ``roadmap/gates.py:ALL_GATES`` and asserts
that, given an empty output file, the ``gate_passed`` dispatch does NOT report
PASS.

Why an empty FILE is the universal empty-input fixture
------------------------------------------------------
``gate_passed`` validates tier-proportionally (pipeline/gates.py): for every
non-EXEMPT tier it first requires the output file to exist and be non-empty.
All 14 ALL_GATES gates are STRICT/STANDARD, so a 0-byte file fails at the
empty-content guard for every one of them -- the assertion holds uniformly.

Shim-awareness (code_assertion gates) -- NOT a Contract #4 violation
--------------------------------------------------------------------
The code_assertion-bearing gates (CERTIFY_GATE, SPEC_FIDELITY_GATE_CONVERGENCE_
AWARE, VERIFY_IMPLEMENTATION_GATE) skip their assertions when called via
``gate_passed(file, GATE)`` with no ``envelope``/``repo_root`` -- the PRESERVED
envelope-None shim (the correct skip-path for CI-only/source-tree assertions on
a pipx package, and for live callers that gate on rendered output). That shim
returning PASS-on-no-envelope for a *valid* file is intentional and is NOT a
Contract #4 violation. For the EMPTY-input fixture here the question never
arises: the empty-content guard fails first, so code_assertions are never
reached. The code_assertions themselves are exercised by their dedicated tests
(``test_dispatch_reachability.py``, ``test_verify_implementation.py``).
"""

from __future__ import annotations

import pytest

from superclaude.cli.pipeline.gates import gate_passed
from superclaude.cli.roadmap.gates import ALL_GATES


@pytest.mark.parametrize("gate_name", [name for name, _ in ALL_GATES])
def test_all_gates_reject_empty(gate_name, tmp_path):
    """No gate PASSes on a 0-byte output file (Contract #4 -- no silent PASS)."""
    gate = dict(ALL_GATES)[gate_name]

    # EXEMPT gates intentionally always pass and are not Contract #4 targets.
    # (None today -- guard kept so a future EXEMPT addition is handled, not
    # mis-flagged.)
    if gate.enforcement_tier == "EXEMPT":
        pytest.skip(f"Gate '{gate_name}' is EXEMPT (always-pass by design).")

    empty_file = tmp_path / f"{gate_name}.empty.md"
    empty_file.write_text("", encoding="utf-8")

    passed, reason = gate_passed(empty_file, gate)
    assert not passed, (
        f"Contract #4 violation: gate '{gate_name}' PASSED on empty input "
        f"(reason={reason!r}). A gate must never silently pass an empty target."
    )


def test_all_gates_reject_missing_file(tmp_path):
    """No non-EXEMPT gate PASSes when the target file does not exist."""
    missing = tmp_path / "does-not-exist.md"
    for gate_name, gate in ALL_GATES:
        if gate.enforcement_tier == "EXEMPT":
            continue
        passed, reason = gate_passed(missing, gate)
        assert not passed, (
            f"Contract #4 violation: gate '{gate_name}' PASSED on a missing "
            f"target (reason={reason!r})."
        )
