"""Git-worktree replay helper for the E1-E5 differential backtest.

Mirrors the ``src/superclaude/cli/sprint/process.py`` subprocess seam: ``subprocess`` is
imported module-top as ``_subprocess`` so unit tests can patch
``tests.troubleshoot.backtest.git_replay._subprocess.run`` and exercise the
checkout -> yield -> guaranteed-teardown control flow with zero real git side effects.

G1 CHECKOUT RULE (load-bearing): the checkout target is the BARE ``prefix_parent_sha`` stored
in ``REPLAY_ESCAPES`` -- runtime issues ``git worktree add --detach <wt> <prefix_parent_sha>``
with NO ``^`` suffix, EVER. The ``prefix_parent_sha`` values were already resolved from
``<fix>^`` once at authoring time (per research/08); applying ``^`` again double-decrements
(e.g. ``94d5baa0^`` -> ``ac80f176``) and replays one commit too early -- a green-but-meaningless
backtest where the escape's bug isn't even present. Never apply ``^`` at runtime.
"""

from __future__ import annotations

import shutil
import subprocess as _subprocess
import tempfile
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import NamedTuple


class ReplayEscape(NamedTuple):
    """One canonical pipeline escape and its pinned pre-fix PARENT checkout target.

    Fields:
        escape_id: Canonical escape id (E1..E5).
        fix_sha: The fix commit (provenance / audit only -- NOT the checkout target).
        prefix_parent_sha: The BARE pre-fix PARENT sha -- the checkout target, no ``^``.
        wave: The H-wave the escape maps to in RELEASE-SPEC sec 8.3. H0..H5 is the FULL wave
            taxonomy; the E1-E5 escapes themselves only ever map to H1..H4 (the subset
            ``EscapeResult.wave`` in ``catch_rate.py`` documents) -- the two ranges are consistent,
            not contradictory.
    """

    escape_id: str
    fix_sha: str
    prefix_parent_sha: str
    wave: str


# Pinned at authoring time per research/08 (G1 authoritative table). The prefix_parent_sha
# values are the bare checkout targets -- runtime does NOT apply ``^``. Chain note: E5's fix
# (10723863) is E2's checkout parent, and E2's fix (e97aa4fd) is E3's checkout parent; the
# escapes interleave on one linear history, which is why per-escape parent pinning is required.
REPLAY_ESCAPES: tuple[ReplayEscape, ...] = (
    ReplayEscape("E1", "7601ad25", "94d5baa0", "H1"),
    ReplayEscape("E2", "e97aa4fd", "10723863", "H3"),
    ReplayEscape("E3", "eb9a2633", "e97aa4fd", "H3"),
    ReplayEscape(
        "E4", "b97c9960", "1b0264f1", "H2"
    ),  # fix UNMERGED; replay against parent
    ReplayEscape("E5", "10723863", "d878bc6d", "H4"),
)


def escape_by_id(escape_id: str) -> ReplayEscape:
    """Return the ReplayEscape record for ``escape_id`` (raises KeyError if unknown)."""
    for esc in REPLAY_ESCAPES:
        if esc.escape_id == escape_id:
            return esc
    raise KeyError(
        f"Unknown escape id: {escape_id!r} (known: {[e.escape_id for e in REPLAY_ESCAPES]})"
    )


def is_git_worktree() -> bool:
    """True iff the process CWD is inside a git work-tree (first-line guard for the CI skip-guard).

    Pure probe (no pytest dependency) so per-escape runners can build their own module-level
    ``pytest.mark.skipif`` from it. Prevents the replay tests from ERRORing (vs cleanly skipping)
    when pytest runs outside a git checkout (unpacked sdist, Docker layer with no ``.git``).
    """
    try:
        proc = _subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=_repo_anchor(),
        )
    except (_subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False
    return proc.returncode == 0 and proc.stdout.strip() == "true"


def missing_replay_commits(shas: tuple[str, ...] | list[str]) -> list[str]:
    """Return the subset of ``shas`` ABSENT from local history (the CI shallow-clone skip predicate).

    ``git cat-file -e <sha>^{commit}`` exits 0 iff the object exists locally AND is a commit. On a
    shallow CI clone (actions/checkout@v4 default fetch-depth: 1) the pre-fix parent commits are not
    fetched, so the probe exits non-zero and the replay test SKIPS rather than fails. Pure probe (no
    pytest dependency).
    """
    missing: list[str] = []
    anchor = _repo_anchor()
    for sha in shas:
        try:
            proc = _subprocess.run(
                ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
                check=False,
                capture_output=True,
                timeout=120,
                cwd=anchor,
            )
        except (_subprocess.TimeoutExpired, FileNotFoundError, OSError):
            missing.append(sha)
            continue
        if proc.returncode != 0:
            missing.append(sha)
    return missing


def _repo_anchor() -> str | None:
    """Resolve the repo worktree root once so all ``git worktree`` calls target the SAME repo.

    Returns the absolute ``git rev-parse --show-toplevel`` path to pass as ``cwd=`` to every
    ``worktree add/remove/prune`` + ``worktree list`` invocation, so ``add`` and its matching
    ``remove``/``prune`` never resolve a *different* repo when the process CWD differs (P2-2
    isolation hazard). Anchoring goes through ``_subprocess.run`` (NOT ``-C``) so it stays under
    the unit-test mock seam and does not alter the argv shape the tests assert on. Returns
    ``None`` -- meaning "inherit process CWD", the prior behavior -- if the anchor cannot be
    resolved (git absent, not a work-tree, or the mocked seam yields an empty stdout), so the
    helper never raises and the subprocess-mocked unit tests stay green.
    """
    try:
        out = _subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        ).stdout
    except (_subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return None
    root = (out or "").strip()
    return root or None


def worktree_list_porcelain() -> str:
    """Return ``git worktree list --porcelain`` output (the no-leaked-worktree baseline, G3)."""
    return _subprocess.run(
        ["git", "worktree", "list", "--porcelain"],
        check=True,
        capture_output=True,
        text=True,
        cwd=_repo_anchor(),
    ).stdout


@contextmanager
def checkout_worktree(
    commitish: str, *, scratch_root: str | Path | None = None
) -> Iterator[Path]:
    """Add a detached git worktree at ``commitish``, yield its path, and ALWAYS tear it down.

    ``commitish`` is passed through UNCHANGED -- callers pass the bare ``prefix_parent_sha``
    (no ``^``). The teardown runs in a ``finally`` block with ``check=False`` so a failed
    ``remove`` never masks a real exception raised inside the ``with`` body, and ``prune`` is
    ALWAYS called (G3): the ``.git/worktrees/<name>/`` admin record lives in the common-dir and
    is NOT reaped by deleting the checkout dir -- only ``git worktree prune`` reaps it.

    Args:
        commitish: The bare checkout target (a ``prefix_parent_sha``), passed through verbatim.
        scratch_root: Optional parent dir for the temp worktree. A unique subdir is minted under
            it (so a caller-owned scratch_root is never itself removed). When ``None``, a fresh
            ``tempfile.mkdtemp`` dir is used.

    Yields:
        Path to the checked-out worktree directory.
    """
    if scratch_root is not None:
        base = Path(scratch_root) / f"replay-{uuid.uuid4().hex[:12]}"
        # mkdtemp (the else branch) already creates the dir; only the caller-scratch_root
        # branch needs to mint it (P2-3).
        base.mkdir(parents=True, exist_ok=True)
    else:
        base = Path(tempfile.mkdtemp(prefix="backtest-replay-"))
    wt = base / "wt"
    # Anchor add + teardown to the SAME repo (P2-2): resolve once so the matching
    # remove/prune can never target a different repo than the add when CWD differs.
    anchor = _repo_anchor()
    try:
        _subprocess.run(
            ["git", "worktree", "add", "--detach", str(wt), commitish],
            check=True,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=anchor,
        )
        yield wt
    finally:
        # Best-effort teardown. Each subprocess step is wrapped in its OWN try/except (P2-1):
        # subprocess.run raises TimeoutExpired/FileNotFoundError/OSError REGARDLESS of
        # check=False (which only suppresses CalledProcessError). Without per-call guards a
        # raise here would propagate out of `finally` -- masking any body exception AND
        # skipping the rmtree + the MANDATORY prune (leaking the .git/worktrees/<name>/ admin
        # record). The guards mirror the process.py seam, which catches exactly these.
        # Best-effort UNLOCK first: if THIS process's own worktree somehow ended up locked,
        # `remove --force` + `prune` cannot reap a locked worktree, so clear our own lock
        # before removing. Targets only OUR wt -- never touches other processes' worktrees.
        try:
            _subprocess.run(
                ["git", "worktree", "unlock", str(wt)],
                check=False,
                capture_output=True,
                text=True,
                timeout=120,
                cwd=anchor,
            )
        except (_subprocess.TimeoutExpired, FileNotFoundError, OSError):
            pass
        try:
            _subprocess.run(
                ["git", "worktree", "remove", "--force", str(wt)],
                check=False,
                capture_output=True,
                text=True,
                timeout=120,
                cwd=anchor,
            )
        except (_subprocess.TimeoutExpired, FileNotFoundError, OSError):
            pass
        shutil.rmtree(base, ignore_errors=True)
        # MANDATORY: reap the .git/worktrees/<name>/ admin record in the common-dir.
        try:
            _subprocess.run(
                ["git", "worktree", "prune"],
                check=False,
                capture_output=True,
                text=True,
                timeout=120,
                cwd=anchor,
            )
        except (_subprocess.TimeoutExpired, FileNotFoundError, OSError):
            pass
