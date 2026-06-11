"""Troubleshoot-seeding tests (spec FR-3.3/FR-3.4).

T-320 the seeded `--scope` contains the finding's file:line; T-330 three same-file
findings → a single batch; T-331 findings exceeding the round budget → truncate and
HALT with a summary. No dispatch emits `--depth quick --fix`.
"""

from __future__ import annotations

from superclaude.pr_submit.fsm import batch_by_file, plan_dispatch, seed_troubleshoot
from superclaude.pr_submit.models import Finding


def _f(path, line, **kw) -> Finding:
    base = dict(severity_hint="high", category="correctness", in_diff=True)
    base.update(kw)
    return Finding(path=path, line=line, body="bug", **base)


def test_t320_seed_scope_contains_file_line():
    """T-320: the dispatched `scope` contains the finding's exact file:line."""
    finding = _f("src/app/auth.py", 137)
    seed = seed_troubleshoot(finding)
    assert seed["scope"] == "src/app/auth.py:137"
    assert "src/app/auth.py:137" in seed["scope"]
    # The seed route is never the conflicting form.
    assert seed["route"] != "--depth quick --fix"


def test_t330_three_same_file_findings_single_batch():
    """T-330: three findings in the same file dispatch as ONE batch."""
    findings = [_f("src/app/auth.py", n) for n in (10, 20, 30)]
    batches = batch_by_file(findings)
    assert len(batches) == 1
    assert len(batches[0]) == 3


def test_t331_over_budget_truncates_and_halts_with_summary():
    """T-331: findings exceeding the round budget → truncate + HALT + residual summary."""
    # Five distinct-file (so five batches) High findings, budget of 2 remaining rounds.
    findings = [_f(f"src/m{i}.py", 1) for i in range(5)]
    plan = plan_dispatch(findings, max_rounds=2, current_round=0)
    assert plan.truncated is True
    assert len(plan.batches) == 2  # truncated to the remaining budget
    assert plan.summary  # a non-empty HALT/residual summary is recorded
    assert "budget" in plan.summary.lower()


def test_t331_within_budget_not_truncated():
    """T-331 (negative): findings within budget are NOT truncated."""
    findings = [_f(f"src/m{i}.py", 1) for i in range(2)]
    plan = plan_dispatch(findings, max_rounds=3, current_round=0)
    assert plan.truncated is False
    assert len(plan.batches) == 2
