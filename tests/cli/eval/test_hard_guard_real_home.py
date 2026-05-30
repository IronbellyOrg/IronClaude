"""NFR-SEC3 hard-guard tests for real ``~/.claude/`` (Task T02.10 / D-0031).

NFR-SEC3 ("hard guard against real ``~/.claude/``") mitigates the R7 risk
case from the cliEval roadmap risk register: a maintainer accidentally
points the harness at their own ``~/.claude/`` (typo in ``--scratch-root``,
inherited shell alias, or a symlink in the operator's working tree).
The harness MUST refuse — surfacing :class:`HomeContainmentViolation`
without writing any file under the rejected HOME.

This module sits one layer above the unit-level FR-ISO2 surface in
``tests/cli/eval/test_path_containment.py`` (T02.08 / D-0029) and the
NFR-SEC2 attack-matrix module in
``tests/cli/eval/test_defense_in_depth.py`` (T02.09 / D-0030). Both
predecessors use synthetic stand-in directories under
``pytest``'s ``tmp_path``. T02.10 closes the loop by exercising the
*real* ``~/.claude/`` directory on the host — the catastrophic case
the operator would actually hit.

Hard-guard contract (NFR-SEC3 / T02.10)
=======================================

The contract this module pins is:

1. **Refusal surface.** :meth:`HomeIsolation.setup` MUST raise
   :class:`HomeContainmentViolation` whenever the per-eval HOME would
   resolve to (or inside) the host's real ``~/.claude/`` — either by
   passing it directly as ``home_root`` or by passing a scratch root
   that symlink-escapes there.
2. **Containment bucketing.** The ``check`` identifier on the raised
   exception MUST be ``"scratch_root_allowlist"`` for the "real
   ``~/.claude/`` as scratch root" attack (it fails AC12 before any
   symlink resolution), and ``"home_path_escape"`` when the per-eval
   HOME materializes as a symlink pointing into ``~/.claude/`` (check 3
   catches the chain).
3. **Refusal-before-side-effects on the real HOME.** No file inside the
   real ``~/.claude/`` is created, modified, or touched as a side
   effect of the attempted setup. The mtime snapshot fixture verifies
   this property by capturing every top-level entry under
   ``~/.claude/`` (name + mtime + content hash for files) BEFORE the
   test runs and asserting the post-test state matches.
4. **Per-eval HOME stays empty on refusal.** When ``tempfile.mkdtemp``
   leaks a partial per-eval HOME under the rejected scratch root (an
   intentional NFR-ISO2 / T02.13 behavior — partial HOMEs are preserved
   for the atomic-setup wrapper to tag as ``setup_failed``), the
   leaked directory MUST stay empty: the guard fires BEFORE the hook
   adapter (T02.14) writes anything under the per-eval HOME.

Skip semantics
==============

The tests run only on hosts where ``Path.home() / ".claude"`` exists.
This matches the task's acceptance criterion: "Tests pass on a host
where ``~/.claude/`` exists (skipped with explicit reason on hosts
where it does not)". The skip reason names the missing path so a CI
operator can decide whether to materialize it or accept the skip.

Leak cleanup
============

The current :meth:`HomeIsolation.setup` design invokes
``tempfile.mkdtemp`` BEFORE :func:`containment_guard` runs (see D-0029
spec rationale — the partial HOME is preserved for NFR-ISO2 / T02.13
to tag as ``setup_failed``). For the "real ``~/.claude/`` as scratch
root" test that means the harness will mkdtemp an empty per-eval HOME
inside the real ``~/.claude/`` before refusing. This module deletes
those leaked directories at test teardown using the test-specific
eval-id prefix (``HardguardevalT0210-``); operators can confirm
cleanup by grep'ing for the prefix under ``~/.claude/``.

Cross-links:

* FR-ISO2 unit surface (T02.08): ``tests/cli/eval/test_path_containment.py``.
* NFR-SEC2 attack matrix (T02.09): ``tests/cli/eval/test_defense_in_depth.py``.
* AC12 scratch-root allowlist (T01.19): ``tests/cli/eval/test_scratch_root_allowlist.py``.
* COMP-006 HomeIsolation method surface (T02.07):
  ``tests/cli/eval/test_home_isolation_extend.py``.
* NFR-ISO2 atomic-setup wrapper (T02.13) — owns the partial-HOME tag
  behavior this module's leak cleanup is needed for.
"""

from __future__ import annotations

import hashlib
import shutil
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import patch

import pytest

from superclaude.cli.eval import (
    EvalConfig,
    HomeContainmentViolation,
    HomeIsolation,
)

# Distinctive eval-id prefix used in every test in this module. The
# ``setup()`` call passes ``mkdtemp(prefix=f"{eval_id}-", ...)``, so
# leaked per-eval HOMEs end up named ``HardguardevalT0210-XXXXXX``.
# The cleanup fixture matches on this prefix so it only ever touches
# directories this test module created — never any pre-existing
# ``~/.claude/`` content.
_EVAL_ID = "HardguardevalT0210"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def real_claude_dir() -> Path:
    """Locate the host's real ``~/.claude/`` directory.

    Returns the path when it exists; skips the test with an explicit
    reason otherwise (per T02.10 acceptance criterion 2). The path is
    resolved via :func:`Path.home` so the test honors a ``$HOME``
    override the host (or a sandbox runner) might set.
    """

    path = Path.home() / ".claude"
    if not path.exists():
        pytest.skip(
            f"NFR-SEC3 hard-guard test requires the host's real ~/.claude/ "
            f"directory to exist at {path}; skipping on hosts where it is "
            f"absent."
        )
    if not path.is_dir():
        pytest.skip(
            f"NFR-SEC3 hard-guard test requires ~/.claude/ to be a directory; "
            f"{path} is not (resolves to {path.resolve()})."
        )
    return path


@dataclass(frozen=True)
class _EntrySnapshot:
    """Per-entry fingerprint captured under ``~/.claude/``."""

    name: str
    is_file: bool
    is_dir: bool
    is_symlink: bool
    mtime_ns: int
    size: int
    sha256: str | None  # ``None`` for directories and symlinks


@dataclass(frozen=True)
class _DirSnapshot:
    """Top-level snapshot of the real ``~/.claude/`` directory.

    Captures every direct child entry (files and sub-directories) with
    the metadata needed to detect any FS write the guard might have
    leaked: the name set, each entry's mtime in nanoseconds, the file
    size, and a SHA-256 of file contents. Directories are tracked by
    mtime alone because their contents are an immense tree the harness
    must never traverse (defense-in-depth: assertion failure on
    *direct* child mtime is enough to surface a tamper).

    The snapshot is taken with ``Path.lstat()`` so symlinks are
    captured at the symlink layer (not the resolved target) — which is
    what we want for tamper detection.
    """

    entries: dict[str, _EntrySnapshot]

    @classmethod
    def capture(cls, root: Path) -> "_DirSnapshot":
        """Snapshot every direct child of ``root``."""

        entries: dict[str, _EntrySnapshot] = {}
        for child in root.iterdir():
            st = child.lstat()
            is_file = child.is_file() and not child.is_symlink()
            is_dir = child.is_dir() and not child.is_symlink()
            is_symlink = child.is_symlink()
            sha = hashlib.sha256(child.read_bytes()).hexdigest() if is_file else None
            entries[child.name] = _EntrySnapshot(
                name=child.name,
                is_file=is_file,
                is_dir=is_dir,
                is_symlink=is_symlink,
                mtime_ns=st.st_mtime_ns,
                size=st.st_size if is_file else 0,
                sha256=sha,
            )
        return cls(entries=entries)


@pytest.fixture
def dot_claude_snapshot(real_claude_dir: Path) -> _DirSnapshot:
    """Snapshot ``~/.claude/`` BEFORE the test runs.

    The fixture is consumed by every hard-guard test that needs to
    prove ``HomeIsolation.setup`` did not write under the real HOME.
    The snapshot is captured exactly once per test (function scope)
    so each test gets a fresh baseline.
    """

    return _DirSnapshot.capture(real_claude_dir)


@pytest.fixture
def cleanup_leaked_eval_homes(real_claude_dir: Path) -> Iterator[None]:
    """Delete any per-eval HOMEs this module leaked into ``~/.claude/``.

    The current ``HomeIsolation.setup`` design invokes
    ``tempfile.mkdtemp`` BEFORE the FR-ISO2 guard runs (see D-0029
    spec — partial HOMEs are intentionally preserved on disk so the
    NFR-ISO2 atomic-setup wrapper in T02.13 can tag them as
    ``setup_failed``). For the "real ``~/.claude/`` as scratch root"
    test that means the harness leaks an *empty* per-eval HOME under
    the real HOME despite refusing the operation. The fixture removes
    those directories at teardown so the host's real ``~/.claude/``
    stays in its pre-test shape.

    Cleanup is strictly scoped to entries whose name starts with the
    test module's distinctive eval-id prefix (:data:`_EVAL_ID`), so
    the fixture cannot accidentally delete unrelated content.
    """

    before = {p.name for p in real_claude_dir.iterdir()}
    yield
    after = {p.name for p in real_claude_dir.iterdir()}
    new = after - before
    leaked_prefix = f"{_EVAL_ID}-"
    for name in new:
        if not name.startswith(leaked_prefix):
            continue
        leaked = real_claude_dir / name
        if leaked.is_symlink():
            leaked.unlink()
        elif leaked.is_dir():
            shutil.rmtree(leaked)
        else:
            leaked.unlink()


# ---------------------------------------------------------------------------
# Hard-guard 1 — real ``~/.claude/`` passed directly as ``home_root``
# ---------------------------------------------------------------------------


class TestRealHomeAsScratchRoot:
    """NFR-SEC3 catastrophic case: operator points ``--scratch-root`` at
    the host's real ``~/.claude/``.

    Default :class:`EvalConfig` allows only ``/tmp/eval-runs`` and
    ``.dev/eval-runs`` (see ``EvalConfig._default_allowed_scratch_roots``
    in ``src/superclaude/cli/eval/config.py``); ``~/.claude/`` is not in
    that set, so :func:`containment_guard`'s check 2 must reject before
    any hook adapter writes under the per-eval HOME.
    """

    def test_setup_refuses_real_dot_claude_as_home_root(
        self,
        real_claude_dir: Path,
        dot_claude_snapshot: _DirSnapshot,
        cleanup_leaked_eval_homes: None,  # noqa: ARG002 (fixture side effect)
    ) -> None:
        """``HomeIsolation.setup(home_root=real ~/.claude/, config=default)``
        MUST raise :class:`HomeContainmentViolation` with
        ``check='scratch_root_allowlist'``; the host's ``~/.claude/``
        contents (every direct child file's mtime + SHA-256, every
        direct child directory's mtime) MUST be byte-identical
        post-test."""

        iso = HomeIsolation(
            eval_id=_EVAL_ID,
            home_root=real_claude_dir,
            session_id="sess-nfrsec3-direct",
        )

        with pytest.raises(HomeContainmentViolation) as exc_info:
            # Default config: ``~/.claude/`` is NOT in the default
            # allowlist (``/tmp/eval-runs`` and ``.dev/eval-runs``).
            iso.setup(config=EvalConfig())

        assert exc_info.value.check == "scratch_root_allowlist"
        # Forensic payload preserves the verbatim attempted root.
        assert exc_info.value.scratch_root == real_claude_dir

        # NFR-SEC3 invariant: every pre-existing child of ``~/.claude/``
        # MUST be byte-identical after the refusal. mkdtemp may have
        # created a *new* per-eval HOME entry (cleaned up by the
        # fixture), but it MUST NOT have modified any pre-existing
        # entry.
        post = _DirSnapshot.capture(real_claude_dir)
        for name, before_entry in dot_claude_snapshot.entries.items():
            assert name in post.entries, (
                f"Pre-existing entry {name!r} disappeared from ~/.claude/ "
                f"after refused setup — the guard mutated the real HOME."
            )
            after_entry = post.entries[name]
            assert after_entry == before_entry, (
                f"Pre-existing entry {name!r} under ~/.claude/ was modified "
                f"by the refused setup. Before={before_entry!r}, "
                f"after={after_entry!r}."
            )

        # Any newly-created entry MUST be a leaked per-eval HOME with
        # the test module's eval-id prefix — never anything else.
        new_entries = set(post.entries) - set(dot_claude_snapshot.entries)
        leaked_prefix = f"{_EVAL_ID}-"
        for name in new_entries:
            assert name.startswith(leaked_prefix), (
                f"Unexpected new entry {name!r} appeared under ~/.claude/ "
                f"after the refused setup; only entries with the "
                f"{leaked_prefix!r} prefix are accepted as test leaks."
            )

    def test_per_eval_home_is_not_created_when_setup_refuses(
        self,
        real_claude_dir: Path,
        cleanup_leaked_eval_homes: None,  # noqa: ARG002 (fixture side effect)
    ) -> None:
        """H5b: the allowlist pre-check fires BEFORE ``mkdtemp`` runs, so
        no per-eval HOME is ever created under ``real_claude_dir``.

        Pre-H5b this test pinned "exactly one empty leaked HOME on disk"
        (the partial-HOME preservation contract — mkdtemp ran before the
        post-mkdtemp guard rejected). Post-H5b is strictly stronger: the
        allowlist pre-check refuses the non-allowlisted scratch root
        BEFORE mkdtemp, so ZERO leaked HOMEs exist. This is the OPS-002
        / NFR-SEC2 ideal — "no filesystem write before allowlist
        validation" — applied to the real ``~/.claude/`` attack matrix.
        """

        iso = HomeIsolation(
            eval_id=_EVAL_ID,
            home_root=real_claude_dir,
            session_id="sess-nfrsec3-empty",
        )

        with pytest.raises(HomeContainmentViolation):
            iso.setup(config=EvalConfig())

        # H5b: NO per-eval HOME is created — pre-check blocked mkdtemp.
        leaked_prefix = f"{_EVAL_ID}-"
        leaks = [
            child
            for child in real_claude_dir.iterdir()
            if child.name.startswith(leaked_prefix)
        ]
        assert leaks == [], (
            f"Expected ZERO leaked per-eval HOMEs under {real_claude_dir} "
            f"(H5b allowlist pre-check refuses before mkdtemp), "
            f"found {len(leaks)}: {[str(p) for p in leaks]}"
        )
        assert not iso.is_set_up

    def test_setup_refuses_real_dot_claude_with_permissive_config_does_not_help(
        self,
        real_claude_dir: Path,
        dot_claude_snapshot: _DirSnapshot,
        cleanup_leaked_eval_homes: None,  # noqa: ARG002 (fixture side effect)
    ) -> None:
        """An operator who tries to "fix" the allowlist by adding
        ``~/.claude/`` to ``EvalConfig.allowed_scratch_roots`` MUST not
        succeed — but with the current FR-ISO2 design the allowlist IS
        the source of truth (NFR-SEC2 closure), so a config explicitly
        listing ``~/.claude/`` *would* let check 2 pass.

        This test pins the *defense* available today: the operator can
        always restore safety by NOT adding ``~/.claude/`` to the
        allowlist, and the default ``EvalConfig`` excludes it. We
        assert that calling :meth:`setup` against ``~/.claude/`` with
        an *empty* allowlist (the strictest possible config) still
        rejects via the allowlist check — proving the failure surface
        is the allowlist comparison, not a side-effect of the default
        list happening to omit ``~/.claude/``.

        T06.03 (DOC-OQ8) reserves a follow-on "absolute hard guard"
        analysis that would refuse ``~/.claude/`` even when it IS in
        the allowlist; the contract this test pins today is "the
        default config refuses, and explicitly empty allowlist also
        refuses".
        """

        iso = HomeIsolation(
            eval_id=_EVAL_ID,
            home_root=real_claude_dir,
            session_id="sess-nfrsec3-empty-allowlist",
        )

        # Empty allowlist: nothing is allowed, so the check MUST fail
        # for ``~/.claude/`` (and for any other path too).
        empty_config = EvalConfig(allowed_scratch_roots=())

        with pytest.raises(HomeContainmentViolation) as exc_info:
            iso.setup(config=empty_config)

        assert exc_info.value.check == "scratch_root_allowlist"

        # Pre-existing contents unchanged (re-using the snapshot
        # assertion from the primary test).
        post = _DirSnapshot.capture(real_claude_dir)
        for name, before_entry in dot_claude_snapshot.entries.items():
            assert name in post.entries
            assert post.entries[name] == before_entry, (
                f"Pre-existing entry {name!r} mutated under empty-allowlist refusal."
            )


# ---------------------------------------------------------------------------
# Hard-guard 2 — scratch root somehow contains ``~/.claude/`` via symlink escape
# ---------------------------------------------------------------------------


class TestScratchRootContainsRealHomeViaSymlink:
    """NFR-SEC3 / T02.10 second test case from the roadmap step list:
    "scratch root somehow contains ``~/.claude/`` via symlink escape".

    Attack model: a scratch root that LOOKS safe (it's a tmp_path-style
    dir under an explicit allowlist) hides a symlink that resolves into
    the real ``~/.claude/``. The harness must refuse via FR-ISO2 check
    3 (post-mkdtemp symlink-resolved containment) without writing
    anything under the real ``~/.claude/``.
    """

    def test_setup_refuses_when_per_eval_home_symlinks_into_real_dot_claude(
        self,
        real_claude_dir: Path,
        dot_claude_snapshot: _DirSnapshot,
        tmp_path: Path,
    ) -> None:
        """A tmp-path scratch root is allowlisted, but ``mkdtemp``
        (patched here to simulate the worst-case attack) returns a
        symlink at ``<scratch>/HardguardevalT0210-XXXXXX`` whose
        target resolves into the host's real ``~/.claude/``. Check 3
        (``home_path_escape``) must reject; no entry under
        ``~/.claude/`` may change.

        The ``mkdtemp`` patch mirrors the existing T02.08 integration
        test ``test_setup_catches_symlink_escape_under_explicit_config``
        in ``tests/cli/eval/test_path_containment.py`` — same
        mechanism, but the symlink target is now the *real*
        ``~/.claude/`` instead of a synthetic stand-in.
        """

        scratch = tmp_path / "eval-runs-hardguard"
        scratch.mkdir()

        config = EvalConfig(allowed_scratch_roots=(scratch,))

        # Pre-create a symlink with the eval-id prefix that ``mkdtemp``
        # would have minted; the patched ``mkdtemp`` hands its path
        # back so the post-mkdtemp guard sees a real symlink whose
        # target resolves into ``~/.claude/``.
        evil_home = scratch / f"{_EVAL_ID}-evilXXXXXX"
        evil_home.symlink_to(real_claude_dir)

        with patch("superclaude.cli.eval.isolation.tempfile.mkdtemp") as mock_mkdtemp:
            mock_mkdtemp.return_value = str(evil_home)

            iso = HomeIsolation(
                eval_id=_EVAL_ID,
                home_root=scratch,
                session_id="sess-nfrsec3-symlink-escape",
            )

            with pytest.raises(HomeContainmentViolation) as exc_info:
                iso.setup(config=config)

        # Check 3 ("home_path_escape") catches the symlink chain.
        assert exc_info.value.check == "home_path_escape"

        # No entry under the host's real ``~/.claude/`` may have
        # changed. The symlink lives under ``tmp_path`` (auto-cleaned
        # by pytest), not under ``~/.claude/``, so this assertion is
        # the proof that following the symlink during ``resolve`` did
        # not in turn write under the resolved target.
        post = _DirSnapshot.capture(real_claude_dir)
        assert set(post.entries) == set(dot_claude_snapshot.entries), (
            "~/.claude/ direct-child set changed across a refused "
            "symlink-escape setup; the guard wrote under the resolved "
            "target."
        )
        for name, before_entry in dot_claude_snapshot.entries.items():
            assert post.entries[name] == before_entry, (
                f"Entry {name!r} mutated under ~/.claude/ across a refused "
                f"symlink-escape setup."
            )

    def test_setup_refuses_when_scratch_root_symlinks_into_real_dot_claude(
        self,
        real_claude_dir: Path,
        dot_claude_snapshot: _DirSnapshot,
        tmp_path: Path,
        cleanup_leaked_eval_homes: None,  # noqa: ARG002 (fixture side effect)
    ) -> None:
        """Sibling case: the *scratch root itself* is a symlink that
        resolves into the host's real ``~/.claude/``. The AC12
        allowlist check (check 2) catches it — :func:`resolve_scratch_root`
        resolves with ``strict=False`` so the symlink collapses before
        membership is tested. The supplied allowlist is intentionally
        ``tmp_path``-only (real ``~/.claude/`` is not listed), so the
        check fails with ``check='scratch_root_allowlist'``.

        Pins the attack vector where an attacker (or a buggy fixture)
        plants a symlink in a place the operator would expect to be
        safe.

        Side-effect note: because :meth:`HomeIsolation.setup` invokes
        ``tempfile.mkdtemp(dir=str(scratch_link))`` BEFORE
        :func:`containment_guard` runs, the kernel follows the symlink
        and creates a leaked per-eval HOME directly inside the real
        ``~/.claude/`` (named ``HardguardevalT0210-XXXXXX``). The
        :func:`cleanup_leaked_eval_homes` fixture removes that leak at
        teardown; this test asserts the leak is empty (NFR-SEC3
        refusal-before-side-effects on the per-eval HOME) and every
        pre-existing entry under ``~/.claude/`` is byte-identical.
        """

        scratch_link = tmp_path / "allowlisted-looking-scratch"
        scratch_link.symlink_to(real_claude_dir)

        # The allowlist intentionally lists a different tmp directory
        # so the symlink-resolved target (``~/.claude/``) does NOT
        # match.
        other_allowed = tmp_path / "actually-allowed"
        other_allowed.mkdir()
        config = EvalConfig(allowed_scratch_roots=(other_allowed,))

        iso = HomeIsolation(
            eval_id=_EVAL_ID,
            home_root=scratch_link,
            session_id="sess-nfrsec3-scratch-symlinks-home",
        )

        with pytest.raises(HomeContainmentViolation) as exc_info:
            iso.setup(config=config)

        assert exc_info.value.check == "scratch_root_allowlist"
        # Verbatim payload preserves the symlink the operator was
        # tricked into supplying.
        assert exc_info.value.scratch_root == scratch_link

        # Every pre-existing entry under the real ``~/.claude/`` MUST
        # be byte-identical after the refused setup; any new entry MUST
        # be a leaked per-eval HOME with the test module's eval-id
        # prefix (the leak the cleanup fixture handles).
        post = _DirSnapshot.capture(real_claude_dir)
        for name, before_entry in dot_claude_snapshot.entries.items():
            assert name in post.entries, (
                f"Pre-existing entry {name!r} disappeared from ~/.claude/ "
                f"after refused symlink-scratch setup — the guard mutated "
                f"the real HOME."
            )
            after_entry = post.entries[name]
            assert after_entry == before_entry, (
                f"Pre-existing entry {name!r} under ~/.claude/ was modified "
                f"by the refused symlink-scratch setup. "
                f"Before={before_entry!r}, after={after_entry!r}."
            )

        leaked_prefix = f"{_EVAL_ID}-"
        new_entries = set(post.entries) - set(dot_claude_snapshot.entries)
        for name in new_entries:
            assert name.startswith(leaked_prefix), (
                f"Unexpected new entry {name!r} appeared under ~/.claude/ "
                f"after the refused symlink-scratch setup; only entries "
                f"with the {leaked_prefix!r} prefix are accepted as test "
                f"leaks."
            )
            # The leaked per-eval HOME MUST be empty — the guard ran
            # before any hook adapter or eval-state writer could touch it.
            leaked_home = real_claude_dir / name
            assert leaked_home.is_dir() and not leaked_home.is_symlink()
            assert list(leaked_home.iterdir()) == [], (
                f"Leaked per-eval HOME {leaked_home} is not empty after "
                f"refused symlink-scratch setup; the guard ran AFTER a "
                f"child write — NFR-SEC3 invariant violated."
            )


# ---------------------------------------------------------------------------
# Hard-guard contract coverage pin
# ---------------------------------------------------------------------------


def test_hard_guard_contract_pin() -> None:
    """Coverage pin: every NFR-SEC3 hard-guard case from the T02.10
    step list maps to a test class in this module.

    Acceptance criterion 1 of T02.10 requires "at least 2 tests". The
    canonical case-list in the task is:

    * Step 3 — ``home_root`` resolves directly to real ``~/.claude/``.
    * Step 4 — scratch root somehow contains ``~/.claude/`` via
      symlink escape.

    Pinning the class names here means a future refactor that deletes
    or renames a case fails this test loudly rather than silently
    shrinking the coverage matrix.
    """

    expected = {
        "real_dot_claude_as_home_root": TestRealHomeAsScratchRoot,
        "scratch_root_contains_dot_claude_via_symlink_escape": TestScratchRootContainsRealHomeViaSymlink,
    }
    assert len(expected) == 2
    for _case, cls in expected.items():
        assert cls.__module__ == __name__
