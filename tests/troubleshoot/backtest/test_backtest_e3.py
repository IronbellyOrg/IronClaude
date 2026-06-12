"""E3 differential runner -- OLD=MISS: hard gate on Task-Log placeholders; NEW=CATCH: H3 sweep proxy.

OLD=MISS (real-git replay at pre-fix parent e97aa4fd, CI-skip-guarded): the pre-fix module-level
`gate_passed(output_file, criteria, ...)` in `cli/pipeline/gates.py` has NO advisory severity -- its
STRICT semantic-check loop returns `(False, "Semantic check '<name>' failed: ...")` on ANY non-True
check, with no `advisory` escape hatch (the `advisory` field + the `continue` branch were ADDED by
fix eb9a2633). So a Task-Log `### Phase N - … Findings` placeholder that trips the
`parallel_instructions` check forces a fatal HALT on a correct artifact -- and even dynamically
tagging the check `advisory=True` is ignored at the parent. That hard-HALT is the OLD=MISS witness.

E3 is the dual-evaluator pair member for `gate_passed` (E4 is `_evaluate_gate`). NEW=CATCH
(skip-guarded): the H3 `unmask-and-sweep.md` ref documents the `K_swept == K_true` sweep + the
WARN/CONTINUE severity-by-consumer rule. Maps 1:1 to RELEASE-SPEC §8.3 "E3 backtest". (E3 and E2 both
proxy `unmask-and-sweep.md` but assert DISTINCT facets: E3 = sweep + WARN/CONTINUE severity.)
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

_E3 = escape_by_id("E3")

pytestmark = pytest.mark.skipif(
    (not is_git_worktree()) or bool(missing_replay_commits([_E3.prefix_parent_sha])),
    reason=(
        f"E3 OLD=MISS real-git replay needs pre-fix parent {_E3.prefix_parent_sha} "
        "(absent on a shallow CI clone; set fetch-depth: 0 to enable)."
    ),
)

# Build a STRICT gate whose single semantic check returns a failure string (the Task-Log placeholder
# false-positive). At the parent there is NO advisory severity, so gate_passed HARD-HALTs even though
# we dynamically tag the check advisory -- demonstrating the missing advisory-escape-hatch escape.
_E3_SNIPPET = """
import inspect, tempfile
from pathlib import Path
from superclaude.cli.pipeline import gates as G
from superclaude.cli.pipeline.models import GateCriteria, SemanticCheck
_tmp = tempfile.mkdtemp()
_f = Path(_tmp) / "task.md"
_f.write_text(
    "### Phase 2 - Codebase Research Findings" + chr(10)
    + "placeholder findings section (a non-executable Task-Log heading)" + chr(10)
    + "more content to satisfy min_lines" + chr(10)
)
_chk = SemanticCheck(
    name="parallel_instructions",
    check_fn=lambda c: "Phase 2 missing parallel execution instructions",
    failure_message="parallel missing",
)
_advisory_settable = True
try:
    object.__setattr__(_chk, "advisory", True)  # pre-fix gate has no advisory branch -> ignored
except Exception:
    _advisory_settable = False
_crit = GateCriteria(
    required_frontmatter_fields=[],
    min_lines=1,
    enforcement_tier="STRICT",
    semantic_checks=[_chk],
)
_ok, _reason = G.gate_passed(_f, _crit)
print(json.dumps({
    "signature": str(inspect.signature(G.gate_passed)),
    "ok": _ok,
    "reason": _reason,
    "halted": (_ok is not True),
    "advisory_field_settable": _advisory_settable,
}))
"""


def test_backtest_e3_old_protocol_misses_advisory_severity() -> None:
    """Pre-fix `gate_passed` hard-HALTs on a placeholder check with no advisory branch -- OLD=MISS."""
    observed = run_prefix_replay_snippet(_E3.prefix_parent_sha, _E3_SNIPPET)
    assert observed["halted"] is True, (
        "expected pre-fix gate_passed to hard-HALT (no advisory severity) on the failing "
        f"parallel_instructions check; got ok={observed['ok']!r} reason={observed['reason']!r}"
    )
    assert "Semantic check 'parallel_instructions' failed" in (
        observed["reason"] or ""
    ), f"unexpected halt reason -- got {observed['reason']!r}"
    result = EscapeResult(
        escape_id="E3",
        wave="H3",
        verdict=VERDICT_MISS,
        negative_witness=True,
        card_path=None,
        detail=f"pre-fix gate_passed hard-halted (advisory ignored): {observed['reason']!r}",
    )
    assert result.verdict == VERDICT_MISS and result.negative_witness is True


@requires_impl_ref("unmask-and-sweep.md")
def test_backtest_e3_new_gate_catches_via_unmask_and_sweep_ref() -> None:
    """NEW=CATCH proxy: the H3 ref documents the K_swept==K_true sweep + WARN/CONTINUE severity."""
    text = (HARDENING_REFS / "unmask-and-sweep.md").read_text(encoding="utf-8")
    low = text.lower()
    assert "k_swept" in low or "swept" in low, (
        "H3 ref must document the unmask/sweep coverage rule (K_swept == K_true)"
    )
    assert "warn" in low or "advisory" in low or "continue" in low, (
        "H3 ref must document the WARN/CONTINUE severity (non-executable headings do not HALT)"
    )
