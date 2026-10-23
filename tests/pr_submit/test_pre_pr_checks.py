"""Pre-PR check tests (spec FR-1.4).

T-106 origin must match the RESOLVED target repo (else HALT); T-107 behind the base
branch → auto-rebase before create; T-108 a returned PR URL whose ``owner/repo`` ≠ the
resolved target → HALT + instruct the operator to close the misrouted PR (the FM-11
tie). The target repo is RESOLVED at runtime from origin (``git remote get-url
origin``, fallback ``gh repo view --json nameWithOwner``) and passed into the pure
checks — NOT a hardcoded fork — so every assertion parametrizes over an arbitrary
``owner/repo``. The de-hardcoding regression is the ``acme/widgets`` row: an unrelated
third-party repo must pass identically to this project's own origin, proving nothing is
pinned to one fork.
"""

from __future__ import annotations

import pytest

from superclaude.pr_submit.fsm import (
    needs_rebase,
    origin_ok,
    pr_branch_ok,
    pr_head_ok,
    pr_target_ok,
    push_parent_ok,
)


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


def test_t106_origin_substring_collision_does_not_falsely_pass():
    """origin_ok must NOT falsely pass when the target is a string-PREFIX of the origin's
    repo (the ``/owner/repo`` boundary guard, symmetric with ``pr_target_ok``).

    e.g. target ``acme/widgets`` against an origin of ``acme/widgets-upstream`` /
    ``acme/widgets-fork`` is a different repo → must be rejected. The exact repo (in
    https, scp-style ssh, and url-style ssh forms, with/without ``.git``) still passes.
    """
    # Prefix-collision origins → rejected (the de-hardcoding-audit D1 regression guard).
    assert (
        origin_ok("https://github.com/acme/widgets-upstream.git", "acme/widgets")
        is False
    )
    assert origin_ok("git@github.com:acme/widgets-fork.git", "acme/widgets") is False
    # The exact repo passes across all remote-URL shapes, incl. url-style ssh.
    assert origin_ok("https://github.com/acme/widgets.git", "acme/widgets") is True
    assert origin_ok("git@github.com:acme/widgets.git", "acme/widgets") is True
    assert origin_ok("ssh://git@github.com/acme/widgets.git", "acme/widgets") is True


# --- Head binding (PR #287 review finding): the checkout and push target must be the PR head.

BRANCH = "fix/pr-submit-skill-cleanup"
SHA = "2916e0627c5d2c96aed50fab61748ff4df24d984"
OTHER_SHA = "070399eb" + "0" * 32


def test_head_binding_matches_pr_head():
    assert pr_head_ok(BRANCH, SHA, BRANCH, SHA, False) is True
    # Commit ids compare case-insensitively.
    assert pr_head_ok(BRANCH, SHA.upper(), BRANCH, SHA, False) is True


@pytest.mark.parametrize(
    "local_branch",
    ["fix/other", f"{BRANCH}/b", f"{BRANCH}-2", f"refs/heads/{BRANCH}", BRANCH.upper()],
)
def test_head_binding_requires_exact_branch(local_branch):
    """A different, descendant, prefixed or case-folded branch name is a different branch."""
    assert pr_head_ok(local_branch, SHA, BRANCH, SHA, False) is False
    assert pr_head_ok(BRANCH, SHA, local_branch, SHA, False) is False


def test_head_binding_rejects_local_commit_ahead_or_behind():
    assert pr_head_ok(BRANCH, OTHER_SHA, BRANCH, SHA, False) is False


@pytest.mark.parametrize("bad_branch", ["", "HEAD", "null", None])
def test_head_binding_fails_closed_on_missing_or_detached_branch(bad_branch):
    assert pr_head_ok(bad_branch, SHA, BRANCH, SHA, False) is False
    assert pr_head_ok(BRANCH, SHA, bad_branch, SHA, False) is False
    # Equal on both sides (a detached checkout and an unparsed head) must still fail.
    assert pr_head_ok(bad_branch, SHA, bad_branch, SHA, False) is False
    assert pr_branch_ok(bad_branch, bad_branch, False) is False


@pytest.mark.parametrize("bad_sha", ["", "null", None, SHA[:7], SHA + "0", "g" * 40])
def test_head_binding_fails_closed_on_bad_commit_ids(bad_sha):
    assert pr_head_ok(BRANCH, bad_sha, BRANCH, SHA, False) is False
    assert pr_head_ok(BRANCH, SHA, BRANCH, bad_sha, False) is False
    # Equal on both sides (e.g. two identical short ids) must still fail.
    assert pr_head_ok(BRANCH, bad_sha, BRANCH, bad_sha, False) is False


def test_head_binding_cross_repo_rule():
    """A fork-hosted head passes only when the caller allows it (below L3); None fails."""
    assert pr_head_ok(BRANCH, SHA, BRANCH, SHA, True) is False
    assert pr_head_ok(BRANCH, SHA, BRANCH, SHA, True, allow_cross_repo=True) is True
    for unknown in (None, "false"):
        assert pr_head_ok(BRANCH, SHA, BRANCH, SHA, unknown) is False
        assert (
            pr_head_ok(BRANCH, SHA, BRANCH, SHA, unknown, allow_cross_repo=True)
            is False
        )


def test_resume_branch_only_check():
    """On resume with a dangling push, only the branch is checked (local HEAD may already
    be the fix commit); the recorded target branch must be the PR head branch."""
    assert pr_branch_ok(BRANCH, BRANCH, False) is True
    assert pr_branch_ok("fix/other", BRANCH, False) is False
    assert pr_branch_ok(BRANCH, BRANCH, None) is False


# --- Push range (PR #287 review round 2): a push carries only the cycle's fix commit.


def test_push_parent_ok_single_commit_on_pr_head():
    assert push_parent_ok([SHA], SHA) is True
    assert push_parent_ok([SHA.upper()], SHA) is True
    assert push_parent_ok([SHA], SHA.upper()) is True
    # Unstripped history output (a trailing newline or space) fails closed.
    assert push_parent_ok([SHA + "\n"], SHA) is False
    assert push_parent_ok([SHA], " " + SHA) is False


def test_push_parent_ok_rejects_extra_local_commit():
    """An unreviewed local commit between the PR head and the fix becomes the fix's
    parent, so the fast-forward push would publish it too."""
    assert push_parent_ok([OTHER_SHA], SHA) is False


@pytest.mark.parametrize(
    "parents",
    [[], [SHA, OTHER_SHA], None, "not-a-list", [None]],
    ids=["root", "merge", "none", "string", "null-entry"],
)
def test_push_parent_ok_fails_closed_on_parent_shape(parents):
    assert push_parent_ok(parents, SHA) is False


@pytest.mark.parametrize("bad_sha", ["", "null", None, SHA[:7], SHA + "0", "g" * 40])
def test_push_parent_ok_fails_closed_on_bad_ids(bad_sha):
    assert push_parent_ok([bad_sha], SHA) is False
    assert push_parent_ok([SHA], bad_sha) is False
    # Equal on both sides must still fail.
    assert push_parent_ok([bad_sha], bad_sha) is False
