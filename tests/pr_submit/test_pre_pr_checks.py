"""Pre-PR check tests (spec FR-1.4).

T-106 origin must match the RESOLVED target repo (else HALT); T-107 behind the base
branch → auto-rebase before create; T-108 a returned PR URL whose ``owner/repo`` ≠ the
resolved target → HALT + instruct the operator to close the misrouted PR (the FM-11
tie). The target repo is RESOLVED at runtime from origin (``gh repo view --json
nameWithOwner``, fallback ``git remote get-url origin``) and passed into the pure
checks — NOT a hardcoded fork — so every assertion parametrizes over an arbitrary
``owner/repo``. The de-hardcoding regression is the ``acme/widgets`` row: an unrelated
third-party repo must pass identically to this project's own origin, proving nothing is
pinned to one fork.
"""

from __future__ import annotations

import pytest

from superclaude.pr_submit.fsm import needs_rebase, origin_ok, pr_target_ok


@pytest.mark.parametrize(
    "repo, origin_https, origin_ssh, foreign_origin",
    [
        # This project's own origin (regression: the prior hardcoded slug still works).
        (
            "IronbellyOrg/IronClaude",
            "https://github.com/IronbellyOrg/IronClaude.git",
            "git@github.com:IronbellyOrg/IronClaude.git",
            # A DIFFERENT origin (the public upstream parent) → must be rejected.
            "https://github.com/SuperClaude-Org/SuperClaude_Framework.git",
        ),
        # An unrelated third-party repo (the de-hardcoding proof).
        (
            "acme/widgets",
            "https://github.com/acme/widgets.git",
            "git@github.com:acme/widgets.git",
            # A genuinely different repo → must be rejected.
            "https://github.com/contoso/gadgets.git",
        ),
    ],
)
def test_t106_origin_must_match_resolved_repo(
    repo, origin_https, origin_ssh, foreign_origin
):
    """T-106: origin must match the RESOLVED target repo; any other origin → HALT."""
    # The resolved repo (https and ssh origin forms, with/without the .git suffix) passes.
    assert origin_ok(origin_https, repo) is True
    assert origin_ok(origin_ssh, repo) is True
    assert origin_ok(origin_https.removesuffix(".git"), repo) is True
    # A different origin (e.g. an upstream parent) is rejected → HALT before opening the PR.
    assert origin_ok(foreign_origin, repo) is False
    # Degenerate inputs never pass.
    assert origin_ok("", repo) is False
    assert origin_ok(origin_https, "") is False


def test_t107_behind_base_triggers_rebase():
    """T-107: a branch behind its base branch (``origin/<default>``) must auto-rebase before `gh pr create`.

    ``needs_rebase`` is pure arithmetic over ``commits_behind`` — the SKILL computes the
    distance against the repo's ACTUAL default branch (or the ``--base`` override), so
    this carries no literal ``master`` assumption.
    """
    assert needs_rebase(commits_behind=3) is True
    assert needs_rebase(commits_behind=0) is False


@pytest.mark.parametrize(
    "repo, good, misrouted",
    [
        (
            "IronbellyOrg/IronClaude",
            "https://github.com/IronbellyOrg/IronClaude/pull/42",
            # gh's default-to-upstream-parent trap.
            "https://github.com/SuperClaude-Org/SuperClaude_Framework/pull/42",
        ),
        (
            "acme/widgets",
            "https://github.com/acme/widgets/pull/7",
            "https://github.com/contoso/gadgets/pull/7",
        ),
    ],
)
def test_t108_wrong_owner_url_halts_and_instructs_close(repo, good, misrouted):
    """T-108: a returned PR URL whose ``owner/repo`` ≠ the resolved target → HALT + instruct close (FM-11 tie)."""
    assert pr_target_ok(good, repo) is True
    # A misrouted URL → HALT, instruct the operator to close the misrouted PR.
    assert pr_target_ok(misrouted, repo) is False
    # Degenerate inputs never pass.
    assert pr_target_ok(good, "") is False
    assert pr_target_ok("", repo) is False


def test_t108_prefix_collision_does_not_falsely_pass():
    """A target that is a string-PREFIX of the URL's repo must NOT falsely pass (the
    ``/owner/repo/`` boundary guard). e.g. target ``acme/widgets`` vs a PR on
    ``acme/widgets-fork`` — the misroute must be caught."""
    assert (
        pr_target_ok("https://github.com/acme/widgets-fork/pull/7", "acme/widgets")
        is False
    )
    assert (
        pr_target_ok("https://github.com/acme/widgets/pull/7", "acme/widgets") is True
    )
