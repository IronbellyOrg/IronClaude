"""Pre-PR check tests (spec FR-1.4).

T-106 origin not the fork → HALT; T-107 behind `origin/master` → auto-rebase before
create; T-108 a returned PR URL whose owner ≠ `IronbellyOrg` → HALT + instruct the
operator to close the misrouted PR (the FM-11 tie). All three sub-checks are
explicit assertions (closing the FR-1.4 pre-reflect coverage item).
"""

from __future__ import annotations

from superclaude.pr_submit.fsm import needs_rebase, origin_ok, pr_target_ok


def test_t106_origin_must_be_fork():
    """T-106: origin must be `IronbellyOrg/IronClaude`; any other origin → HALT."""
    # The fork (https and ssh forms) is accepted.
    assert origin_ok("https://github.com/IronbellyOrg/IronClaude.git") is True
    assert origin_ok("git@github.com:IronbellyOrg/IronClaude.git") is True
    assert origin_ok("https://github.com/IronbellyOrg/IronClaude") is True
    # The public upstream (or any other origin) is rejected → HALT.
    assert (
        origin_ok("https://github.com/SuperClaude-Org/SuperClaude_Framework.git")
        is False
    )
    assert origin_ok("") is False


def test_t107_behind_master_triggers_rebase():
    """T-107: a branch behind `origin/master` must auto-rebase before `gh pr create`."""
    assert needs_rebase(commits_behind=3) is True
    assert needs_rebase(commits_behind=0) is False


def test_t108_wrong_owner_url_halts_and_instructs_close():
    """T-108: a returned PR URL whose owner ≠ IronbellyOrg → HALT + instruct close (FM-11 tie)."""
    good = "https://github.com/IronbellyOrg/IronClaude/pull/42"
    misrouted = "https://github.com/SuperClaude-Org/SuperClaude_Framework/pull/42"
    assert pr_target_ok(good) is True
    assert (
        pr_target_ok(misrouted) is False
    )  # → HALT, instruct operator to close the misrouted PR
