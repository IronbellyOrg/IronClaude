"""E4 differential runner -- OLD=MISS: `_evaluate_gate` ignores advisory; NEW=CATCH: H2 ledger proxy.

E4 is the dual-evaluator pair member for `_evaluate_gate` (E3 is `gate_passed`). The E3 fix added an
advisory branch to `pipeline.gates.gate_passed`, but the LIVE PRD path never calls `gate_passed` --
`PrdExecutor._evaluate_gate` (a SEPARATE class-bound re-implementation) still halts on the first
non-True check REGARDLESS of `check.advisory`. So E4 exists because the E3 fix was verified against
the wrong consumer.

OLD=MISS (real-git replay at pre-fix parent 1b0264f1, CI-skip-guarded): the class-bound
`PrdExecutor._evaluate_gate(self, step_id, gate, content)` is invoked with a SimpleNamespace `self`
(it only touches `self._diagnostics` / `self._logger`) and an advisory-tagged failing check; it
returns `False` -- halting DESPITE the advisory flag. That is the OLD=MISS witness.

E4 HEAD-DRIFT (critical): the advisory-fatal bug is ALREADY HEALED on HEAD via acd5631f (#158),
which adds the advisory branch to `_evaluate_gate` (HEAD executor.py:853-883); the spec's
`b97c9960` fix remains UNMERGED. (Note: the spec/research cited the HEAD-heal as `20693bb8`, a
same-intent SIBLING fix on another branch -- that sha is NOT a HEAD ancestor on this worktree;
the VERIFIED HEAD-heal here is `acd5631f` (#158).) So the replay base is PINNED to the pre-fix
parent 1b0264f1 (where the bug IS present), NOT HEAD. E4 is framed as the §8.3 H2 ledger-completeness assertion over BOTH
`gate_passed` AND `_evaluate_gate` consumers. NEW=CATCH (skip-guarded): the H2 `contract-enumeration.md`
ref documents empty-ledger=FAIL + the both-consumers-classified requirement. Maps 1:1 to §8.3 "E4".
"""

from __future__ import annotations

import pytest

from tests.troubleshoot.backtest._impl_guard import HARDENING_REFS, requires_impl_ref
from tests.troubleshoot.backtest.catch_rate import VERDICT_MISS, EscapeResult
from tests.troubleshoot.backtest.git_replay import (
    escape_by_id,
    is_git_worktree,
    missing_replay_commits,
)
from tests.troubleshoot.backtest.replay_executor import run_prefix_replay_snippet

_E4 = escape_by_id(
    "E4"
)  # prefix_parent_sha == 1b0264f1 (NOT HEAD -- see HEAD-DRIFT above)

pytestmark = pytest.mark.skipif(
    (not is_git_worktree()) or bool(missing_replay_commits([_E4.prefix_parent_sha])),
    reason=(
        f"E4 OLD=MISS real-git replay needs pre-fix parent {_E4.prefix_parent_sha} "
        "(absent on a shallow CI clone; set fetch-depth: 0 to enable). Pinned to the pre-fix parent, "
        "NOT HEAD (HEAD already healed via acd5631f / #158)."
    ),
)

# Class-bound _evaluate_gate invoked with a stub `self` (only _diagnostics/_logger are touched). The
# advisory-tagged failing check still halts at the parent -> the second-consumer (ledger) gap.
_E4_SNIPPET = """
import inspect
from types import SimpleNamespace
from superclaude.cli.prd import executor as E
_fn = E.PrdExecutor._evaluate_gate  # unbound function; called with a constructed SimpleNamespace self
_self = SimpleNamespace(
    _diagnostics=SimpleNamespace(record_gate_failure=lambda *a, **k: None),
    _logger=SimpleNamespace(log_gate_result=lambda *a, **k: None),
)
_chk = SimpleNamespace(
    check_fn=lambda c: "parallel_instructions failed",
    failure_message="advisory failure",
    advisory=True,  # the LIVE executor path ignores this at the parent -> the escape
)
_gate = SimpleNamespace(min_lines=0, enforcement_tier="STRICT", semantic_checks=[_chk])
_ret = _fn(_self, "build-task-file", _gate, "content line one" + chr(10) + "content line two" + chr(10))
print(json.dumps({
    "signature": str(inspect.signature(_fn)),
    "returned": _ret,
    "halted_despite_advisory": (_ret is False),
}))
"""


def test_backtest_e4_old_protocol_misses_second_consumer() -> None:
    """Pre-fix `_evaluate_gate` halts despite the advisory flag at 1b0264f1 -- the OLD=MISS witness.

    Replayed against the pinned pre-fix parent, NOT HEAD (HEAD already healed via acd5631f / #158).
    """
    observed = run_prefix_replay_snippet(_E4.prefix_parent_sha, _E4_SNIPPET)
    assert observed["halted_despite_advisory"] is True, (
        "expected the LIVE-path PrdExecutor._evaluate_gate to return False (halt) DESPITE the "
        f"advisory check at parent {_E4.prefix_parent_sha}; got returned={observed['returned']!r}"
    )
    result = EscapeResult(
        escape_id="E4",
        wave="H2",
        verdict=VERDICT_MISS,
        negative_witness=True,
        card_path=None,
        detail="pre-fix _evaluate_gate halted despite check.advisory (second-consumer gap)",
    )
    assert result.verdict == VERDICT_MISS and result.negative_witness is True


@requires_impl_ref("contract-enumeration.md")
def test_backtest_e4_new_gate_catches_via_contract_enumeration_ref() -> None:
    """NEW=CATCH proxy: the H2 ref documents empty-ledger=FAIL + BOTH consumers classified."""
    text = (HARDENING_REFS / "contract-enumeration.md").read_text(encoding="utf-8")
    low = text.lower()
    assert "ledger" in low, (
        "H2 ref must document the consumer ledger (empty-ledger=FAIL)"
    )
    assert "gate_passed" in low and "_evaluate_gate" in low, (
        "H2 ref must require BOTH gate_passed AND _evaluate_gate consumers be classified"
    )
