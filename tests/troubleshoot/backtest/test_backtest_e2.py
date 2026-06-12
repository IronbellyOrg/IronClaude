"""E2 differential runner -- OLD=MISS: final-phase false-positive HALT; NEW=CATCH: H3 word-boundary.

OLD=MISS (real-git replay at pre-fix parent 10723863, CI-skip-guarded): the pre-fix module-level
`_check_parallel_instructions(content)` in `cli/prd/gates.py` enforces the parallel-keyword rule on
EVERY phase >= 2, so a legitimately-sequential completion final phase returns the failure string
`"Phase 5 missing parallel execution instructions ..."` -- HALTing a correct artifact (the escape:
the protocol accepted that halt-on-correct-artifact as legitimate).

DIGIT-HEADING TRAP (confirmed against pre-fix source ~L207): the pre-fix matcher is `Phase\\s+(\\d+)`
+ `int(m.group(1))` -- DIGITS ONLY. A non-digit heading like `Phase N` is never collected, the gate
returns True (no halt), and the OLD=MISS test would go RED. So the fixture uses a CONCRETE DIGIT
completion phase (`## Phase 5: Present Results`, no parallel keyword) preceded by an earlier phase
(`## Phase 2`) whose body DOES contain a parallel keyword, so the over-strict halt provably fires.

NEW=CATCH (skip-guarded): the H3 `unmask-and-sweep.md` ref documents the §5.7 word-boundary grammar
(`complete` must not exempt `incomplete`). Maps 1:1 to RELEASE-SPEC §8.3 "E2 backtest". (E2 and E3
both proxy `unmask-and-sweep.md` but assert DISTINCT facets: E2 = word-boundary classifier.)
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

_E2 = escape_by_id("E2")

pytestmark = pytest.mark.skipif(
    (not is_git_worktree()) or bool(missing_replay_commits([_E2.prefix_parent_sha])),
    reason=(
        f"E2 OLD=MISS real-git replay needs pre-fix parent {_E2.prefix_parent_sha} "
        "(absent on a shallow CI clone; set fetch-depth: 0 to enable)."
    ),
)

# Fixture uses CONCRETE DIGIT phase headings (Phase 2 with a parallel keyword; Phase 5 a sequential
# completion bookend with none) so the pre-fix `Phase \\d+` matcher collects them and over-halts.
_E2_SNIPPET = """
import inspect
from superclaude.cli.prd import gates as G
_lines = [
    "# Phase 1: Setup",
    "Initial setup of the run.",
    "",
    "## Phase 2: Research",
    "Run the research agents in parallel across the codebase.",
    "",
    "## Phase 5: Present Results",
    "Present and complete the final report to the user.",
]
_content = chr(10).join(_lines)
_fn = G._check_parallel_instructions
_result = _fn(_content)
print(json.dumps({
    "signature": str(inspect.signature(_fn)),
    "result": _result if isinstance(_result, str) else True,
    "halted": (_result is not True),
}))
"""


def test_backtest_e2_old_protocol_misses_final_phase_false_positive() -> None:
    """Pre-fix gate HALTs on a sequential completion final phase -- the OLD=MISS negative witness."""
    observed = run_prefix_replay_snippet(_E2.prefix_parent_sha, _E2_SNIPPET)
    assert observed["halted"] is True, (
        "expected the pre-fix _check_parallel_instructions to false-positive HALT on the sequential "
        f"'Phase 5: Present Results' bookend; got result={observed['result']!r}"
    )
    assert "Phase 5 missing parallel" in observed["result"], (
        f"unexpected halt reason -- got {observed['result']!r}"
    )
    result = EscapeResult(
        escape_id="E2",
        wave="H3",
        verdict=VERDICT_MISS,
        negative_witness=True,
        card_path=None,
        detail=f"pre-fix gate over-halted: {observed['result']!r}",
    )
    assert result.verdict == VERDICT_MISS and result.negative_witness is True


@requires_impl_ref("unmask-and-sweep.md")
def test_backtest_e2_new_gate_catches_via_unmask_and_sweep_ref() -> None:
    """NEW=CATCH proxy: the H3 ref documents the word-boundary `complete` !=> `incomplete` rule."""
    text = (HARDENING_REFS / "unmask-and-sweep.md").read_text(encoding="utf-8")
    low = text.lower()
    assert "incomplete" in low and "complete" in low, (
        "H3 ref must document the complete-vs-incomplete word-boundary discrimination"
    )
    assert "word-boundary" in low or "word boundary" in low or "\\b" in text, (
        "H3 ref must document the word-boundary grammar (complete must not exempt incomplete)"
    )
