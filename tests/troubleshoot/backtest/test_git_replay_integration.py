"""Integration tests for the real-git differential replay (G2 CI skip-guard + G3 no-leak).

These tests exercise REAL git worktree operations against the pinned pre-fix parent commits, so
they require a full-depth clone. On CI, ``actions/checkout@v4`` defaults to a shallow
``fetch-depth: 1`` clone where the 5 replay parents are absent, so the whole module SKIPS (not
fails) via a module-level ``pytest.mark.skipif`` that probes ``git cat-file -e <sha>^{commit}``
per escape, guarded first by ``git rev-parse --is-inside-work-tree``. G3: every real checkout
runs inside ``checkout_worktree``'s try/finally (force-remove + prune), and the no-leak test
passes a known ``scratch_root`` then asserts -- even when the replay body raises -- that the
checkout dir is gone AND no ``git worktree list --porcelain`` stanza points under that
scratch_root, proving teardown fired on the failure path. The scoped assertion (vs a global
before/after byte-compare) is robust to concurrent unrelated worktrees in this shared
multi-worktree repo. The live work-tree HEAD is never mutated (all checkouts are detached
worktrees under tmp dirs).
"""

from __future__ import annotations

import subprocess

import pytest

from tests.troubleshoot.backtest import git_replay


def _not_a_git_worktree() -> bool:
    proc = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        capture_output=True,
        text=True,
    )
    return proc.returncode != 0 or proc.stdout.strip() != "true"


def _missing_replay_shas() -> list[tuple[str, str]]:
    """Return [(escape_id, sha), ...] for any pinned parent absent from local history.

    ``git cat-file -e <sha>^{commit}`` exits 0 iff the object exists locally AND is a commit.
    The ``^{commit}`` peel is deliberate (a bare ``-e <sha>`` would also pass for a loose
    blob/tree sharing the prefix). The ``{{`` / ``}}`` are f-string-escaped literal braces.
    """
    missing: list[tuple[str, str]] = []
    for esc in git_replay.REPLAY_ESCAPES:
        proc = subprocess.run(
            ["git", "cat-file", "-e", f"{esc.prefix_parent_sha}^{{commit}}"],
            capture_output=True,
        )
        if proc.returncode != 0:
            missing.append((esc.escape_id, esc.prefix_parent_sha))
    return missing


_GIT_UNAVAILABLE = _not_a_git_worktree()
_MISSING = [] if _GIT_UNAVAILABLE else _missing_replay_shas()

pytestmark = pytest.mark.skipif(
    _GIT_UNAVAILABLE or bool(_MISSING),
    reason=(
        "Not inside a git work-tree -- real-git replay requires repo history."
        if _GIT_UNAVAILABLE
        else (
            "Integration replay requires a full-depth clone; the following pre-fix parent "
            f"commit(s) are absent from local history (shallow CI clone, actions/checkout@v4 "
            f"default fetch-depth: 1): {_MISSING}. Set `fetch-depth: 0` on the checkout step to "
            "enable (the OLD=MISS unit + report-schema tests run green unconditionally)."
        )
    ),
)


def test_backtest_real_worktree_checkout_lands_on_prefix_parent() -> None:
    """A real detached checkout of E1's bare parent sha lands the worktree HEAD on that commit."""
    e1 = git_replay.escape_by_id("E1")
    full_parent = subprocess.run(
        ["git", "rev-parse", e1.prefix_parent_sha],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()

    with git_replay.checkout_worktree(e1.prefix_parent_sha) as wt:
        head = subprocess.run(
            ["git", "-C", str(wt), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

    assert head == full_parent, (
        f"detached checkout of {e1.prefix_parent_sha} (no caret) must land on {full_parent}, "
        f"got {head}"
    )


def test_backtest_replay_leaves_no_leaked_worktree(tmp_path) -> None:
    """G3: a failing replay leaves no leak SCOPED to this escape's own scratch_root.

    SCOPING RATIONALE (concurrency-robustness): this repo is a shared multi-worktree git
    common-dir. A global ``after == baseline`` porcelain byte-compare is fragile here -- any
    unrelated concurrent ``git worktree add`` (or a pre-existing stanza) by another process
    breaks it, producing a false leak report (observed: a sibling QA agent's in-flight
    ``locked initializing`` worktree wrongly attributed as this replay's leak). Instead we pass a
    known ``scratch_root`` (``tmp_path``, unique per test) to ``checkout_worktree`` and assert ONLY
    about worktrees under that root. This still proves G3 (THIS replay leaves no leak on the
    failure path) while being immune to concurrent, unrelated worktrees.
    """
    e1 = git_replay.escape_by_id("E1")

    captured: list = []
    with pytest.raises(RuntimeError):
        with git_replay.checkout_worktree(
            e1.prefix_parent_sha, scratch_root=tmp_path
        ) as wt:
            captured.append(wt)
            # Non-vacuous: the worktree REALLY was created before we exercise teardown.
            assert wt.exists(), f"worktree was not created at {wt}"
            # An AssertionError/RuntimeError in the body must NOT leak the worktree.
            raise RuntimeError("simulated replay failure")

    assert captured, "the with-body never ran -- checkout_worktree did not yield"
    wt = captured[0]

    # (a) The checkout dir for THIS replay is gone (rmtree + remove --force fired in finally).
    assert not wt.exists(), (
        f"Leaked git worktree checkout dir after a failing replay: {wt} still exists -- "
        "teardown (remove --force + rmtree) did not fully fire."
    )

    # (b) No worktree registered in the common-dir points under OUR scratch_root. Scoped to
    # str(scratch_root) so concurrent unrelated worktrees elsewhere can never trip this.
    scratch = str(tmp_path)
    after = git_replay.worktree_list_porcelain()
    leaked = [
        ln for ln in after.splitlines() if ln.startswith("worktree ") and scratch in ln
    ]
    assert not leaked, (
        "Leaked git worktree admin record under this replay's scratch_root -- teardown "
        f"(remove --force + prune) did not fully fire.\nscratch_root: {scratch}\n"
        f"leaked stanzas:\n{chr(10).join(leaked)}\nfull list:\n{after}"
    )
