"""TEST-003 symlink attack tests (Task T02.22 / D-0041).

This module is the first-class symlink-attack test deliverable that
proves the FR-ISO2 ``containment_guard`` (T02.08 / D-0029) and the
NFR-ISO2 atomic-setup wrapper (T02.13 / D-0033) cooperate to catch
*every* symlink-shaped escape attempt that targets either the declared
scratch root or the per-eval HOME ``mkdtemp``-ed underneath it.

Where T02.08 (``tests/cli/eval/test_path_containment.py``) pins the
unit-level guard contract and T02.09
(``tests/cli/eval/test_defense_in_depth.py``) pins the NFR-SEC2 attack
matrix at the ``HomeIsolation.setup`` boundary, this module focuses
explicitly on the *symlink* attack class — the one D-0029/D-0030 single
out as the easiest operator-facing misconfiguration vector:

    1. ``scratch->HOME symlink``  — declared scratch root is a symlink
       whose resolved target is the real ``$HOME``/``.claude``
       (catastrophic case) or any non-allowlisted directory. Guard
       check 2 (``scratch_root_allowlist``) MUST refuse.
    2. ``nested symlink escape``  — declared scratch root is real and
       allowlisted, but the per-eval HOME ``mkdtemp`` returned is itself
       a symlink (or contains a symlink chain) whose resolved target
       lives outside the scratch root. Guard check 3
       (``home_path_escape``) MUST refuse.
    3. ``partial HOME preserved``  — every symlink-shaped containment
       violation MUST leave the partial per-eval HOME on disk so the
       NFR-ISO2 atomic-setup wrapper (T02.13) can route teardown
       through ``teardown(keep=True)`` for forensic inspection.
    4. ``setup_failed tag``       — the ``setup_failed`` artifact tag
       is the disk-level ERRORED signal. The two-branch contract from
       NFR-ISO2 / NFR-SEC3 holds *unchanged* under the symlink attack
       class:

         * :class:`HomeContainmentViolation` (which is what every
           symlink-shaped attack surfaces as) MUST NOT write the tag —
           the violation exception is itself the structured forensic
           signal. See ``tests/cli/eval/test_atomic_setup.py`` for the
           rationale (writing under a refused HOME could land inside
           the real ``~/.claude/`` when the scratch root symlinks
           there).
         * Any OTHER exception raised AFTER ``mkdtemp`` (e.g. a
           synthetic harness bug injected at the guard call site) MUST
           drop the canonical ``setup_failed`` tag whose first line is
           the exception class name.

Ordering — AFTER mkdtemp AND BEFORE hook deploy
================================================

Every symlink-attack test in this module proves the rejection lands
in the canonical "after mkdtemp, before hook deploy" window:

* AFTER mkdtemp is observable through ``HomeIsolation.is_set_up`` and
  by listing the leaked per-eval HOME under the declared scratch root
  (``mkdtemp(prefix=f"{eval_id}-", dir=str(home_root))`` creates the
  directory atomically before returning).
* BEFORE hook deploy is observable by spying on
  :func:`superclaude.cli.eval.hook_adapter.deploy_hooks_to` — when the
  guard refuses, the adapter MUST NOT have been invoked. This module
  patches a sentinel at the import surface
  ``superclaude.cli.eval.hook_adapter.deploy_hooks_to`` (since the
  current ``HomeIsolation.setup`` does not call hook deploy itself —
  that wiring lands in T02.14 / Phase 3); the assertion proves no
  caller has been added in this module's lifetime that would write
  under the rejected HOME.

Cross-links:

* FR-ISO2 unit surface (T02.08): ``tests/cli/eval/test_path_containment.py``.
* NFR-SEC2 attack matrix (T02.09): ``tests/cli/eval/test_defense_in_depth.py``.
* NFR-SEC3 hard guard (T02.10): ``tests/cli/eval/test_hard_guard_real_home.py``.
* NFR-ISO2 atomic-setup contract (T02.13):
  ``tests/cli/eval/test_atomic_setup.py``.
* AC12 scratch-root allowlist source-of-truth (T01.19):
  ``tests/cli/eval/test_scratch_root_allowlist.py``.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from superclaude.cli.eval import (
    SETUP_FAILED_TAG_RELPATH,
    EvalConfig,
    HomeContainmentViolation,
    HomeIsolation,
)
from superclaude.cli.eval import hook_adapter as hook_adapter_module
from superclaude.cli.eval import isolation as iso_module

# Anchor the BEFORE-hook-deploy assertion to a real symbol resolution at
# collection time — a future rename of ``deploy_hooks_to`` (e.g. to
# ``install_hooks_to``) surfaces as ``AttributeError`` here rather than
# letting the ``patch(...)`` targets below silently swallow the rename
# and pass vacuously. Referenced by the slice-5 hook-deploy spies; the
# attribute access is the load-bearing check.
_DEPLOY_HOOKS_TO = hook_adapter_module.deploy_hooks_to


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def scratch_root(tmp_path: Path) -> Path:
    """Per-test scratch root mirroring the orchestrator's ``--scratch-root``.

    The directory exists on disk so :meth:`HomeIsolation.setup` can
    legitimately ``mkdtemp`` under it for any test whose attack vector
    targets a path *under* the scratch root rather than the scratch
    root itself.
    """

    root = tmp_path / "eval-runs"
    root.mkdir()
    return root


@pytest.fixture
def permissive_config(scratch_root: Path) -> EvalConfig:
    """``EvalConfig`` whose allowlist explicitly includes the test's scratch
    root.

    Mirrors production wiring: the orchestrator (T03.16) hands the
    runner a config whose ``allowed_scratch_roots`` already contains
    the resolved scratch root for the run. Tests that target check 3
    (``home_path_escape``) need a permissive config so the failure
    that surfaces is the symlink escape — not a coincidental allowlist
    miss.
    """

    return EvalConfig(allowed_scratch_roots=(scratch_root,))


def _build(
    home_root: Path,
    *,
    eval_id: str = "E1",
    session_id: str = "sess-001",
) -> HomeIsolation:
    """Construct a :class:`HomeIsolation` with the canonical test defaults."""

    return HomeIsolation(
        eval_id=eval_id,
        home_root=home_root,
        session_id=session_id,
    )


def _list_partial_homes(scratch_root: Path, eval_id: str) -> list[Path]:
    """Return all ``mkdtemp``-created HOMEs for ``eval_id`` under ``scratch_root``.

    ``tempfile.mkdtemp(prefix=f"{eval_id}-", ...)`` appends a random
    suffix, so the test fixture looks the HOME up by prefix rather
    than reconstructing the name.
    """

    return sorted(scratch_root.glob(f"{eval_id}-*"))


# ---------------------------------------------------------------------------
# Attack vector 1 — scratch root is a symlink to a non-allowlisted target
# ---------------------------------------------------------------------------


class TestScratchSymlinkToHome:
    """Vector 1 — ``scratch->HOME symlink``.

    The declared scratch root looks legitimate (it lives under the
    operator's chosen path) but is actually a symlink whose resolved
    target is outside :attr:`EvalConfig.allowed_scratch_roots`. The
    canonical catastrophic case is a symlink to the host's real
    ``$HOME``/``.claude`` (covered end-to-end with mtime snapshotting
    in :mod:`tests.cli.eval.test_hard_guard_real_home`); this module
    exercises the same vector against arbitrary non-allowlisted
    directories so the contract is portable across hosts.

    Containment bucketing
    ---------------------

    Every test in this class asserts the raised
    :class:`HomeContainmentViolation` carries ``check ==
    'scratch_root_allowlist'`` — the AC12 check fires before the
    post-``mkdtemp`` resolve in :func:`containment_guard`. The
    forensic payload preserves the *verbatim* attempted scratch root
    (the symlink, not its target) so a reporter can render the
    operator-facing path.
    """

    def test_scratch_root_symlink_to_non_allowlisted_target_is_refused(
        self, tmp_path: Path
    ) -> None:
        """Declared scratch root is a symlink to a non-allowlisted dir.

        Build:

            outside_target/         <- real, non-allowlisted
            allowed_dir/            <- the one entry in the allowlist
            scratch_symlink -> outside_target

        Pass ``scratch_symlink`` to :meth:`HomeIsolation.setup`; the
        guard's check 2 must reject because the resolved target is not
        in the allowlist.
        """

        outside_target = tmp_path / "OUTSIDE_ALLOWLIST"
        outside_target.mkdir()

        allowed_dir = tmp_path / "allowed"
        allowed_dir.mkdir()

        scratch_symlink = tmp_path / "scratch-symlink"
        scratch_symlink.symlink_to(outside_target)

        # Config allows ``allowed_dir`` only — ``outside_target`` is
        # NOT in the allowlist, so the symlinked scratch resolves to a
        # non-allowlisted root.
        config = EvalConfig(allowed_scratch_roots=(allowed_dir,))

        iso = _build(scratch_symlink)
        with pytest.raises(HomeContainmentViolation) as exc_info:
            iso.setup(config=config)

        assert exc_info.value.check == "scratch_root_allowlist"
        # Forensic payload preserves the symlink path verbatim — not
        # its resolved target.
        assert exc_info.value.scratch_root == scratch_symlink

    def test_scratch_root_symlink_chain_to_outside_is_refused(
        self, tmp_path: Path
    ) -> None:
        """Chained symlink: ``scratch -> intermediate -> outside``.

        ``Path.resolve(strict=False)`` (used by
        :func:`resolve_scratch_root` for check 2) collapses the full
        chain in one shot, so a multi-hop symlink chain must surface
        the same allowlist-miss as a one-hop link.
        """

        outside = tmp_path / "OUTSIDE_FINAL"
        outside.mkdir()
        intermediate = tmp_path / "INTERMEDIATE_LINK"
        intermediate.symlink_to(outside)

        scratch_symlink = tmp_path / "scratch-chain"
        scratch_symlink.symlink_to(intermediate)

        allowed_dir = tmp_path / "allowed"
        allowed_dir.mkdir()
        config = EvalConfig(allowed_scratch_roots=(allowed_dir,))

        iso = _build(scratch_symlink)
        with pytest.raises(HomeContainmentViolation) as exc_info:
            iso.setup(config=config)

        assert exc_info.value.check == "scratch_root_allowlist"

    def test_scratch_symlink_refusal_runs_before_mkdtemp(
        self, tmp_path: Path
    ) -> None:
        """H5b: scratch-root allowlist refusal fires BEFORE ``mkdtemp``.

        Pre-H5b this asserted ``mkdtemp`` ran before the post-mkdtemp
        guard rejected — leaving a partial HOME observable inside the
        symlink target. That behavior violated OPS-002 / NFR-SEC2: a
        symlink-based scratch-root attack got to materialize a file on
        disk before the gate fired. Post-H5b the allowlist pre-check at
        the top of ``HomeIsolation.setup`` resolves the symlink and
        refuses BEFORE mkdtemp — so the symlink target stays empty.

        Symlink Check 3 (``home_path_escape``) — where the per-eval
        HOME *itself* is a symlink that escapes a real scratch root —
        still runs post-mkdtemp and still preserves the partial HOME
        (covered by ``TestNestedSymlinkEscape`` below).
        """

        outside_target = tmp_path / "OUTSIDE_ALLOWLIST"
        outside_target.mkdir()
        allowed_dir = tmp_path / "allowed"
        allowed_dir.mkdir()
        scratch_symlink = tmp_path / "scratch-symlink"
        scratch_symlink.symlink_to(outside_target)
        config = EvalConfig(allowed_scratch_roots=(allowed_dir,))

        iso = _build(scratch_symlink, eval_id="Eaftermk")
        with pytest.raises(HomeContainmentViolation):
            iso.setup(config=config)

        # H5b: ZERO per-eval HOMEs created — pre-check resolved the
        # symlink and refused before mkdtemp could materialize anything
        # under the outside target.
        partials = _list_partial_homes(outside_target, "Eaftermk")
        assert partials == []
        assert not iso.is_set_up


# ---------------------------------------------------------------------------
# Attack vector 2 — per-eval HOME mkdtemp returned a symlink escape
# ---------------------------------------------------------------------------


class TestNestedSymlinkEscape:
    """Vector 2 — ``nested symlink escape``.

    The scratch root is real and allowlisted, but the path
    :func:`tempfile.mkdtemp` returned for the per-eval HOME is itself
    a symlink (or contains a symlink chain) whose resolved target
    escapes the scratch root. Guard check 3 (``home_path_escape``)
    catches this because it uses ``Path.resolve(strict=True)`` —
    collapsing every symlink component before the prefix check.

    The test injects the symlinked path by patching
    :func:`tempfile.mkdtemp` to return a pre-created symlink that
    lives lexically under the scratch root but resolves to an
    outside target. This is the only realistic way to exercise the
    vector deterministically — ``mkdtemp`` itself does not produce
    symlinks, but a future filesystem-shim or hostile shared NAS
    could (the guard is the defense regardless of how the symlink
    appeared).
    """

    def test_mkdtemp_returns_symlink_escape_refused(
        self, scratch_root: Path, tmp_path: Path, permissive_config: EvalConfig
    ) -> None:
        """``mkdtemp`` returns a symlink whose target lives outside the
        scratch root; the post-resolve containment check refuses with
        ``check='home_path_escape'``."""

        escape_target = tmp_path / "ESCAPE_TARGET"
        escape_target.mkdir()
        (escape_target / "marker").write_text("would-be-escape")

        with patch(
            "superclaude.cli.eval.isolation.tempfile.mkdtemp"
        ) as mock_mkdtemp:
            # Pre-create a symlink with the eval-id prefix that
            # ``mkdtemp`` would have returned. The path lives lexically
            # under ``scratch_root`` (so a textual prefix check would
            # pass) but resolves outside the scratch root.
            evil_home = scratch_root / "E1-evilXXXXXX"
            evil_home.symlink_to(escape_target)
            mock_mkdtemp.return_value = str(evil_home)

            iso = _build(scratch_root)
            with pytest.raises(HomeContainmentViolation) as exc_info:
                iso.setup(config=permissive_config)

        assert exc_info.value.check == "home_path_escape"
        # The instance's recorded home_path is the symlink (verbatim).
        assert iso.home_path == evil_home

    def test_nested_symlink_chain_refused(
        self, scratch_root: Path, tmp_path: Path, permissive_config: EvalConfig
    ) -> None:
        """Multi-hop symlink chain ``home -> intermediate -> outside``
        must collapse via ``resolve(strict=True)`` and refuse with
        ``check='home_path_escape'``."""

        final_target = tmp_path / "FINAL_OUTSIDE"
        final_target.mkdir()
        intermediate = tmp_path / "INTERMEDIATE_LINK"
        intermediate.symlink_to(final_target)

        with patch(
            "superclaude.cli.eval.isolation.tempfile.mkdtemp"
        ) as mock_mkdtemp:
            chained_home = scratch_root / "E2-chainXXXXXX"
            chained_home.symlink_to(intermediate)
            mock_mkdtemp.return_value = str(chained_home)

            iso = _build(scratch_root, eval_id="E2")
            with pytest.raises(HomeContainmentViolation) as exc_info:
                iso.setup(config=permissive_config)

        assert exc_info.value.check == "home_path_escape"

    def test_symlink_escape_refusal_observes_post_mkdtemp_path(
        self, scratch_root: Path, tmp_path: Path, permissive_config: EvalConfig
    ) -> None:
        """The guard runs AFTER ``mkdtemp`` returns, so the recorded
        ``home_path`` is the symlinked path (the mkdtemp output) — not
        a path the guard synthesized for itself. This proves the
        ordering AFTER mkdtemp without relying on monkey-patching the
        guard itself."""

        escape_target = tmp_path / "ESCAPE_TARGET"
        escape_target.mkdir()

        with patch(
            "superclaude.cli.eval.isolation.tempfile.mkdtemp"
        ) as mock_mkdtemp:
            evil_home = scratch_root / "E3-postXXXXXX"
            evil_home.symlink_to(escape_target)
            mock_mkdtemp.return_value = str(evil_home)

            iso = _build(scratch_root, eval_id="E3")
            with pytest.raises(HomeContainmentViolation) as exc_info:
                iso.setup(config=permissive_config)

        # mkdtemp ran (the mock was invoked exactly once).
        assert mock_mkdtemp.call_count == 1
        # And the violation carries the post-mkdtemp path verbatim.
        assert exc_info.value.home_path == evil_home


# ---------------------------------------------------------------------------
# Attack vector 3 — partial HOME preserved on symlink-shaped containment
# ---------------------------------------------------------------------------


class TestPartialHomePreservedOnSymlinkAttack:
    """Vector 3 — ``partial HOME preserved``.

    NFR-ISO2 requires every post-``mkdtemp`` exception to leave the
    per-eval HOME on disk so a wrapper can route teardown through
    ``teardown(keep=True)``. This class proves the contract holds
    specifically under the symlink attack class — both for the
    scratch-symlink vector (check 2) and the per-eval HOME symlink
    escape vector (check 3).
    """

    def test_no_partial_home_after_scratch_symlink_refusal(
        self, tmp_path: Path
    ) -> None:
        """H5b: scratch->outside symlink triggers the allowlist pre-check.

        Pre-H5b this asserted "partial HOME preserved under symlink target
        for forensics" — the pre-H5b mkdtemp path materialized a directory
        under the OUTSIDE target before the post-mkdtemp guard rejected.
        That defeated the OPS-002 / NFR-SEC2 invariant (filesystem write
        before allowlist validation against a symlink-spoofed root).

        Post-H5b: the pre-check ``Path.expanduser().resolve(strict=False)``
        collapses the symlink to its outside target, then refuses against
        the allowlist BEFORE ``mkdtemp`` runs. Nothing lands on disk —
        ``teardown(keep=True)`` has nothing to preserve. Symlink Check 3
        (per-eval HOME itself is a symlink escape) still preserves the
        partial HOME — see
        :meth:`test_partial_home_preserved_after_symlink_escape_refusal`.
        """

        outside_target = tmp_path / "OUTSIDE_ALLOWLIST"
        outside_target.mkdir()
        allowed_dir = tmp_path / "allowed"
        allowed_dir.mkdir()
        scratch_symlink = tmp_path / "scratch-symlink"
        scratch_symlink.symlink_to(outside_target)
        config = EvalConfig(allowed_scratch_roots=(allowed_dir,))

        iso = _build(scratch_symlink, eval_id="Epartial1")
        with pytest.raises(HomeContainmentViolation):
            iso.setup(config=config)

        # H5b: nothing under the outside target — pre-check refused first.
        partials = _list_partial_homes(outside_target, "Epartial1")
        assert partials == []
        assert not iso.is_set_up
        # teardown(keep=True) is a benign no-op when nothing was created.
        iso.teardown(keep=True)
        # Outside target remains empty — no leaked partial HOME.
        assert list(outside_target.iterdir()) == []

    def test_partial_home_preserved_after_symlink_escape_refusal(
        self, scratch_root: Path, tmp_path: Path, permissive_config: EvalConfig
    ) -> None:
        """After the nested-symlink-escape vector triggers check 3, the
        symlinked per-eval HOME stays on disk and the instance's
        ``home_path`` points at it for ``teardown(keep=True)``."""

        escape_target = tmp_path / "ESCAPE_TARGET"
        escape_target.mkdir()

        with patch(
            "superclaude.cli.eval.isolation.tempfile.mkdtemp"
        ) as mock_mkdtemp:
            evil_home = scratch_root / "Epartial2-XXXXXX"
            evil_home.symlink_to(escape_target)
            mock_mkdtemp.return_value = str(evil_home)

            iso = _build(scratch_root, eval_id="Epartial2")
            with pytest.raises(HomeContainmentViolation):
                iso.setup(config=permissive_config)

        # The symlink under the scratch root remains.
        assert evil_home.is_symlink()
        assert iso.is_set_up
        assert iso.home_path == evil_home
        # ``teardown(keep=True)`` does not remove the symlink.
        iso.teardown(keep=True)
        assert evil_home.is_symlink()


# ---------------------------------------------------------------------------
# Attack vector 4 — setup_failed tag contract under the symlink attack class
# ---------------------------------------------------------------------------


class TestSetupFailedTagUnderSymlinkAttack:
    """Vector 4 — ``setup_failed`` tag contract under the symlink class.

    The NFR-ISO2 / NFR-SEC3 two-branch contract from
    :mod:`tests.cli.eval.test_atomic_setup` is repeated here against
    the symlink attack matrix to prove the tag rule survives whatever
    symlink shenanigans the caller throws at ``setup``:

    * Every symlink-shaped :class:`HomeContainmentViolation` MUST NOT
      drop a ``setup_failed`` tag. Writing under a refused HOME could
      land inside the real ``~/.claude/`` when the scratch root or
      ``mkdtemp`` result symlinks there — the very class of
      catastrophic case NFR-SEC3 mitigates.
    * A non-containment exception raised AFTER ``mkdtemp`` (here
      simulated by patching ``containment_guard`` to raise a
      synthetic ``RuntimeError``) MUST drop the tag whose first line
      is the exception class name. This pins that the tag rule
      survives even when the symlink-resolution path inside the guard
      is intercepted.
    """

    def test_scratch_symlink_violation_does_not_write_tag(
        self, tmp_path: Path
    ) -> None:
        """H5b: scratch->outside symlink refusal blocks mkdtemp entirely,
        so the ``setup_failed`` tag is trivially absent.

        Pre-H5b: mkdtemp ran first, partial HOME materialized under the
        outside symlink target, then the post-mkdtemp guard rejected and
        the wrapper explicitly withheld the tag (NFR-SEC3 invariant).
        Post-H5b: the allowlist pre-check resolves the symlink and refuses
        before mkdtemp — no per-eval HOME exists, so the tag is absent a
        fortiori. The NFR-SEC3 invariant (refused HOMEs do not carry a
        tag) is satisfied by the stronger "refused HOMEs do not exist."
        """

        outside_target = tmp_path / "OUTSIDE_ALLOWLIST"
        outside_target.mkdir()
        allowed_dir = tmp_path / "allowed"
        allowed_dir.mkdir()
        scratch_symlink = tmp_path / "scratch-symlink"
        scratch_symlink.symlink_to(outside_target)
        config = EvalConfig(allowed_scratch_roots=(allowed_dir,))

        iso = _build(scratch_symlink, eval_id="Enotag1")
        with pytest.raises(HomeContainmentViolation):
            iso.setup(config=config)

        # H5b: no per-eval HOME was created, so no tag, no .eval-meta dir
        # under any conceivable location.
        assert not iso.is_set_up
        assert list(outside_target.iterdir()) == [], (
            "scratch-symlink pre-check MUST refuse before mkdtemp — "
            "no leaked partial HOME under the outside target."
        )

    def test_symlink_escape_violation_does_not_write_tag(
        self, scratch_root: Path, tmp_path: Path, permissive_config: EvalConfig
    ) -> None:
        """Nested-symlink-escape refusal must also withhold the tag.

        The per-eval HOME is itself a symlink to an outside target;
        writing the tag would land *inside* the outside target (the
        symlink transparently forwards the write through), which is
        exactly the catastrophic case NFR-SEC3 forbids.
        """

        escape_target = tmp_path / "ESCAPE_TARGET"
        escape_target.mkdir()

        with patch(
            "superclaude.cli.eval.isolation.tempfile.mkdtemp"
        ) as mock_mkdtemp:
            evil_home = scratch_root / "Enotag2-XXXXXX"
            evil_home.symlink_to(escape_target)
            mock_mkdtemp.return_value = str(evil_home)

            iso = _build(scratch_root, eval_id="Enotag2")
            with pytest.raises(HomeContainmentViolation):
                iso.setup(config=permissive_config)

        # No write inside the symlink target — confirmed by absence of
        # ``.eval-meta`` under the resolved location.
        assert not (escape_target / ".eval-meta").exists()
        # And no tag at the symlinked path either.
        tag_path = iso.home_path / SETUP_FAILED_TAG_RELPATH
        assert not tag_path.exists()

    def test_non_containment_exception_in_symlink_context_writes_tag(
        self,
        scratch_root: Path,
        permissive_config: EvalConfig,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """A non-containment exception raised AFTER ``mkdtemp`` MUST drop
        the canonical ``setup_failed`` tag whose first line is the
        exception class name.

        Patching :func:`containment_guard` to raise a synthetic
        ``RuntimeError`` lets us exercise the tag-write branch of the
        atomic-setup wrapper under the symlink attack class without
        actually constructing a containment violation: the wrapper
        treats any non-:class:`HomeContainmentViolation` as a harness
        bug and tags the HOME.
        """

        def _raise(**_kwargs: object) -> None:
            raise RuntimeError("symlink-class harness bug")

        monkeypatch.setattr(iso_module, "containment_guard", _raise)

        iso = _build(scratch_root, eval_id="Etag")
        with pytest.raises(RuntimeError, match="symlink-class harness bug"):
            iso.setup(config=permissive_config)

        tag_path = iso.home_path / SETUP_FAILED_TAG_RELPATH
        assert tag_path.is_file()
        first_line = tag_path.read_text(encoding="utf-8").splitlines()[0]
        assert first_line == "RuntimeError"
        # Tag lives under the per-eval HOME (defense-in-depth: never
        # outside it).
        assert tag_path.is_relative_to(iso.home_path)


# ---------------------------------------------------------------------------
# Attack vector 5 — ordering: AFTER mkdtemp AND BEFORE hook deploy
# ---------------------------------------------------------------------------


class TestOrderingAfterMkdtempBeforeHookDeploy:
    """The T02.22 acceptance criterion 3 mandates that every refusal
    lands in the canonical "after mkdtemp, before hook deploy" window.

    AFTER mkdtemp is observed by listing the partial per-eval HOME on
    disk and reading ``iso.is_set_up`` (the slot is populated only
    AFTER ``mkdtemp`` succeeds inside ``HomeIsolation.setup``).

    BEFORE hook deploy is observed by spying on
    :func:`superclaude.cli.eval.hook_adapter.deploy_hooks_to` — the
    adapter that T02.14 (Phase 3) will wire to ``setup``. The current
    ``HomeIsolation.setup`` does not invoke ``deploy_hooks_to`` itself
    (the wiring is in T03.x); this spy proves that nobody in this
    module's lifetime has changed that — any future caller that adds
    a hook-deploy step BEFORE the containment guard would break this
    assertion before it ships.
    """

    def test_hook_deploy_not_called_when_scratch_symlink_refused(
        self, tmp_path: Path
    ) -> None:
        """H5b: hook_adapter still MUST NOT be called — and now mkdtemp
        also doesn't run thanks to the allowlist pre-check.

        Pre-H5b: mkdtemp ran, then containment_guard refused, then the
        atomic-setup wrapper bubbled the exception without touching the
        hook adapter (mkdtemp-before-hook-deploy ordering invariant).
        Post-H5b: the allowlist pre-check refuses before mkdtemp runs,
        so the invariant strengthens: nothing on the lifecycle path
        (mkdtemp OR hook-deploy) fires for the scratch-symlink vector.
        """

        outside_target = tmp_path / "OUTSIDE_ALLOWLIST"
        outside_target.mkdir()
        allowed_dir = tmp_path / "allowed"
        allowed_dir.mkdir()
        scratch_symlink = tmp_path / "scratch-symlink"
        scratch_symlink.symlink_to(outside_target)
        config = EvalConfig(allowed_scratch_roots=(allowed_dir,))

        with patch(
            "superclaude.cli.eval.hook_adapter.deploy_hooks_to"
        ) as mock_deploy:
            iso = _build(scratch_symlink, eval_id="Eorder1")
            with pytest.raises(HomeContainmentViolation):
                iso.setup(config=config)

        mock_deploy.assert_not_called()
        # H5b: no partial HOME under the outside symlink target.
        partials = _list_partial_homes(outside_target, "Eorder1")
        assert partials == []

    def test_hook_deploy_not_called_when_symlink_escape_refused(
        self, scratch_root: Path, tmp_path: Path, permissive_config: EvalConfig
    ) -> None:
        """Spy on the hook adapter while the nested-symlink-escape
        vector triggers the guard. The adapter MUST NOT be called."""

        escape_target = tmp_path / "ESCAPE_TARGET"
        escape_target.mkdir()

        with patch(
            "superclaude.cli.eval.hook_adapter.deploy_hooks_to"
        ) as mock_deploy, patch(
            "superclaude.cli.eval.isolation.tempfile.mkdtemp"
        ) as mock_mkdtemp:
            evil_home = scratch_root / "Eorder2-XXXXXX"
            evil_home.symlink_to(escape_target)
            mock_mkdtemp.return_value = str(evil_home)

            iso = _build(scratch_root, eval_id="Eorder2")
            with pytest.raises(HomeContainmentViolation):
                iso.setup(config=permissive_config)

        mock_deploy.assert_not_called()
        # mkdtemp was invoked exactly once — AFTER mkdtemp ordering.
        assert mock_mkdtemp.call_count == 1
        assert iso.is_set_up

    def test_containment_guard_runs_after_mkdtemp(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        """Spy on :func:`containment_guard` and assert the per-eval
        HOME exists on disk at guard-call time. This is the same
        ordering check pinned by ``test_path_containment.py``, repeated
        here so this module's contract is self-contained for the
        symlink attack class."""

        observed: dict[str, object] = {}

        def _spy(
            *,
            home_path: Path,
            scratch_root: Path,  # noqa: ARG001
            eval_id: str,  # noqa: ARG001
            config: EvalConfig,  # noqa: ARG001
        ) -> None:
            observed["home_existed_at_guard"] = home_path.exists()
            observed["guard_home_path"] = home_path

        with patch(
            "superclaude.cli.eval.isolation.containment_guard",
            side_effect=_spy,
        ):
            iso = _build(scratch_root, eval_id="Eorderaftermk")
            iso.setup(config=permissive_config)

        assert observed["home_existed_at_guard"] is True
        assert observed["guard_home_path"] == iso.home_path
