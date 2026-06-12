"""E5 differential runner -- OLD=MISS: `start_commit..HEAD` vacuous-PASS; NEW=CATCH: H4 proxy.

OLD=MISS (real-git replay at pre-fix parent d878bc6d, CI-skip-guarded): the pre-fix
`task-builder/SKILL.md` POST-reflect item emits `--diff <BASE>..HEAD` -- a two-dot COMMIT RANGE that
audits NONE of uncommitted `/task` work (the usual outcome: `/task` edits the working tree but does
not commit, so a `..HEAD` range sees nothing) and/or spans a foreign interleaved commit -> reflect
returns a vacuous PASS over the wrong surface. The escape lives in markdown (the generated reflect
command), so the OLD=MISS witness is a SOURCE-TEXT assertion on the checked-out parent tree: the
two-dot `<BASE>..HEAD` selector is present, and the fix's single-ref guidance + the explicit "Do NOT
use `start_commit..HEAD`" prohibition are ABSENT.

NEW=CATCH (skip-guarded): the H4 `effective-input-proof.md` ref documents wrong-surface fail-closed
(`E>0` insufficient; an `|E ∩ true_runtime_surface|` intersection proof is required). Maps 1:1 to
RELEASE-SPEC §8.3 "E5 backtest".
"""

from __future__ import annotations

import pytest

from tests.troubleshoot.backtest._impl_guard import HARDENING_REFS, requires_impl_ref
from tests.troubleshoot.backtest.catch_rate import VERDICT_MISS, EscapeResult
from tests.troubleshoot.backtest.git_replay import (
    checkout_worktree,
    escape_by_id,
    is_git_worktree,
    missing_replay_commits,
)
from tests.troubleshoot.backtest.replay_executor import read_source_from_worktree

_E5 = escape_by_id("E5")
_SKILL_RELPATH = "src/superclaude/skills/task-builder/SKILL.md"

pytestmark = pytest.mark.skipif(
    (not is_git_worktree()) or bool(missing_replay_commits([_E5.prefix_parent_sha])),
    reason=(
        f"E5 OLD=MISS real-git replay needs pre-fix parent {_E5.prefix_parent_sha} "
        "(absent on a shallow CI clone; set fetch-depth: 0 to enable)."
    ),
)


def test_backtest_e5_old_protocol_misses_wrong_diff_surface() -> None:
    """Pre-fix SKILL.md POST-reflect item uses the `<BASE>..HEAD` range selector -- the OLD=MISS witness."""
    with checkout_worktree(_E5.prefix_parent_sha) as wt:
        text = read_source_from_worktree(wt, _SKILL_RELPATH)

    assert "--diff <BASE>..HEAD" in text, (
        "expected the pre-fix POST-reflect ACTION to use the two-dot `--diff <BASE>..HEAD` range "
        "selector (the wrong surface that misses uncommitted work). The bare `<BASE>..HEAD` substring "
        "is non-discriminating -- it also appears post-fix inside the `NOT <BASE>..HEAD` prohibition; "
        "the `--diff <BASE>..HEAD` ACTION form appears ONLY at the pre-fix parent (post-fix uses the "
        "`--diff <BASE>` single-ref)"
    )
    # The fix's single-ref correction + the explicit prohibition must be ABSENT at the pre-fix parent.
    assert "Do NOT use `start_commit..HEAD`" not in text, (
        "the fix's `start_commit..HEAD` prohibition must be absent at the pre-fix parent"
    )
    result = EscapeResult(
        escape_id="E5",
        wave="H4",
        verdict=VERDICT_MISS,
        negative_witness=True,
        card_path=None,
        detail="pre-fix SKILL.md POST-reflect uses `<BASE>..HEAD` (vacuous PASS over wrong surface)",
    )
    assert result.verdict == VERDICT_MISS and result.negative_witness is True


@requires_impl_ref("effective-input-proof.md")
def test_backtest_e5_new_gate_catches_via_effective_input_ref() -> None:
    """NEW=CATCH proxy: the H4 ref documents wrong-surface fail-closed + intersection proof."""
    text = (HARDENING_REFS / "effective-input-proof.md").read_text(encoding="utf-8")
    low = text.lower()
    assert "fail-closed" in low or "fail closed" in low, (
        "H4 ref must document wrong-surface fail-closed behavior"
    )
    assert "intersection" in low or "∩" in text or "effective input" in low, (
        "H4 ref must require the effective-input intersection proof (E>0 insufficient)"
    )
