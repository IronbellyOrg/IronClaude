"""NFR-SEC2 defense-in-depth attack matrix (Task T02.09 / D-0030).

This module is the *positive containment-rejection* test deliverable for
NFR-SEC2. The unit-level FR-ISO2 surface lives in
``tests/cli/eval/test_path_containment.py`` (T02.08 / D-0029); this
module sits one layer higher and exercises :meth:`HomeIsolation.setup`
end-to-end against the four NFR-SEC2 attack vectors enumerated in the
cliEval roadmap (row 30):

    1. ``scratch-is-symlink-to-HOME`` — scratch root looks legitimate
       but is a symlink whose resolved target is non-allowlisted
       (catastrophic case: symlinks to the real ``$HOME``/``.claude``).
    2. ``scratch-outside-allowlist``  — scratch root is a real
       directory but not present in
       :attr:`EvalConfig.allowed_scratch_roots`.
    3. ``eval_id-mutation-post-construction`` — a caller force-mutates
       the (frozen) ``eval_id`` field after
       ``HomeIsolation.__post_init__`` ran, simulating a tampered
       instance reaching ``setup()``.
    4. ``loader-bypass`` — a caller constructs ``HomeIsolation``
       directly (skipping :class:`SuiteLoader`) with a clearly
       loader-rejected id; the second-layer guard in
       :meth:`HomeIsolation.setup` (and the constructor's
       ``__post_init__``) must still hard-fail.

Each test asserts :class:`HomeContainmentViolation` (the canonical
NFR-SEC2 failure surface) and pins the ``check`` identifier so
reporters can bucket each vector without parsing the message.
``__cause__`` is asserted where applicable to verify the underlying
exception is chained for forensic walks.

Cross-links:

* NFR-SEC2 roadmap row 30 (``allowed_scratch_roots`` allowlist +
  loader-bypass defense + post-construction tamper defense).
* FR-ISO2 unit surface (T02.08): ``tests/cli/eval/test_path_containment.py``.
* NFR-SEC3 real-HOME hard guard (T02.10):
  ``tests/cli/eval/test_hard_guard_real_home.py``.
* Allowlist source-of-truth (AC12 / T01.19):
  ``tests/cli/eval/test_scratch_root_allowlist.py``.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.eval import (
    EvalConfig,
    HomeContainmentViolation,
    HomeIsolation,
    InvalidEvalId,
    ScratchRootViolation,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def scratch_root(tmp_path: Path) -> Path:
    """Per-test scratch root mirroring the orchestrator's ``--scratch-root``.

    The directory exists on disk so :meth:`HomeIsolation.setup` can
    legitimately ``mkdtemp`` under it for any test whose attack vector
    isn't the scratch root itself.
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
    the resolved scratch root for the run. Tests that target a vector
    *other* than the allowlist need a permissive config so the failure
    that surfaces is the vector under test (not a coincidental
    allowlist miss).
    """

    return EvalConfig(allowed_scratch_roots=(scratch_root,))


# ---------------------------------------------------------------------------
# Attack vector 1 — scratch root is a symlink to a non-allowlisted target
# ---------------------------------------------------------------------------


class TestVectorScratchSymlinkToHome:
    """Vector 1 (``scratch-is-symlink-to-HOME``).

    The catastrophic case from the roadmap risk register (R2): a
    scratch root that *looks* like an allowed prefix but is actually a
    symlink whose resolved target lies outside the allowlist — the
    real ``$HOME``/``.claude`` being the worst-case target. The
    AC12 allowlist check inside :func:`containment_guard` calls
    :func:`resolve_scratch_root`, which resolves with
    ``strict=False`` so any symlink component collapses before the
    membership test runs. The expected failure surface is
    :class:`HomeContainmentViolation` with
    ``check="scratch_root_allowlist"`` and ``__cause__`` chained to
    :class:`ScratchRootViolation`.
    """

    def test_setup_rejects_scratch_root_symlinked_outside_allowlist(
        self, tmp_path: Path
    ) -> None:
        """Build a scratch root whose textual path is allowlist-friendly
        but whose symlink target points at a stand-in for the real
        ``$HOME`` (a directory deliberately outside the allowlist).

        Calling :meth:`HomeIsolation.setup` MUST raise
        :class:`HomeContainmentViolation` with
        ``check="scratch_root_allowlist"`` and a chained
        :class:`ScratchRootViolation` cause — proving the
        symlink-resolved allowlist check is the layer that catches the
        attack rather than any lexical prefix comparison.
        """

        # Stand-in for the real ``$HOME``/``.claude`` an attacker would
        # try to escape into. Deliberately *not* in the allowlist.
        fake_real_home = tmp_path / "FAKE_HOME_DOT_CLAUDE"
        fake_real_home.mkdir()
        (fake_real_home / "settings.json").write_text("{}")  # plausible target

        # The "legitimate-looking" scratch root the caller passes is a
        # symlink to the fake real HOME. Its lexical parent path is
        # under tmp_path, but ``Path.resolve(strict=False)`` will
        # collapse it to ``fake_real_home``.
        scratch_link = tmp_path / "looks-like-eval-runs"
        scratch_link.symlink_to(fake_real_home)

        # Real allowlisted directory the operator *intended* — note it
        # is a different, real directory; the symlink target is NOT
        # this path.
        allowed_dir = tmp_path / "really-allowed"
        allowed_dir.mkdir()
        config = EvalConfig(allowed_scratch_roots=(allowed_dir,))

        iso = HomeIsolation(
            eval_id="E1",
            home_root=scratch_link,
            session_id="sess-vector-1",
        )

        with pytest.raises(HomeContainmentViolation) as exc_info:
            iso.setup(config=config)

        assert exc_info.value.check == "scratch_root_allowlist"
        assert isinstance(exc_info.value.__cause__, ScratchRootViolation)
        # The exception payload preserves the verbatim (un-resolved)
        # scratch root so forensics can show the operator the symlink
        # they were tricked into supplying.
        assert exc_info.value.scratch_root == scratch_link


# ---------------------------------------------------------------------------
# Attack vector 2 — scratch root outside the AC12 allowlist
# ---------------------------------------------------------------------------


class TestVectorScratchOutsideAllowlist:
    """Vector 2 (``scratch-outside-allowlist``).

    The scratch root is a real, non-symlinked directory whose path is
    not present in :attr:`EvalConfig.allowed_scratch_roots`. This is
    the "policy" failure mode that catches a configuration mistake or
    a malicious ``--scratch-root`` flag value pointing at an
    unintended location.
    """

    def test_setup_rejects_scratch_root_not_in_allowlist(
        self, tmp_path: Path
    ) -> None:
        """A real scratch directory that is not listed in the config's
        ``allowed_scratch_roots`` must fail with ``check="scratch_root_allowlist"``."""

        # Real directory, not symlinked anywhere.
        scratch = tmp_path / "off-policy-scratch"
        scratch.mkdir()

        # Allowlist contains a *different* directory, mirroring a real
        # production config (e.g. only ``/tmp/eval-runs`` is permitted).
        allowed_only = tmp_path / "only-allowed-policy"
        allowed_only.mkdir()
        config = EvalConfig(allowed_scratch_roots=(allowed_only,))

        iso = HomeIsolation(
            eval_id="E1",
            home_root=scratch,
            session_id="sess-vector-2",
        )

        with pytest.raises(HomeContainmentViolation) as exc_info:
            iso.setup(config=config)

        assert exc_info.value.check == "scratch_root_allowlist"
        assert isinstance(exc_info.value.__cause__, ScratchRootViolation)
        assert exc_info.value.scratch_root == scratch


# ---------------------------------------------------------------------------
# Attack vector 3 — eval_id mutation after construction
# ---------------------------------------------------------------------------


class TestVectorEvalIdMutationPostConstruction:
    """Vector 3 (``eval_id-mutation-post-construction``).

    :class:`HomeIsolation` is a ``@dataclass(frozen=True)``; ordinary
    assignment raises :class:`dataclasses.FrozenInstanceError`. However
    a determined caller can still bypass the freeze via
    ``object.__setattr__`` (the same mechanism the class itself uses
    for the private ``_home_path`` slot). The defense-in-depth contract
    requires that even an instance whose ``eval_id`` was force-mutated
    *after* ``__post_init__`` ran still fails inside
    :meth:`HomeIsolation.setup` — the guard re-runs
    :func:`validate_eval_id` so post-construction tampering cannot
    sneak an unsafe id into ``tempfile.mkdtemp``.
    """

    # Tamper values are restricted to FR-SCH2-rejected ids whose textual
    # form is still a *legal POSIX filename component* (no ``/``, no
    # leading ``/``). This pins the failure surface unambiguously to
    # the containment guard rather than to an incidental
    # ``tempfile.mkdtemp`` ``OSError`` raised by the kernel before the
    # guard runs. The path-separator-bearing values (``/etc/passwd``,
    # ``E1/x``, ``../escape``) are covered by the loader-bypass vector
    # below at *construction* time, where ``__post_init__`` rejects
    # them before any filesystem call.
    @pytest.mark.parametrize(
        "tampered_eval_id",
        [
            "9bad",  # FR-SCH2 leading-digit reject
            "",  # empty string
            "with spaces",  # whitespace not in FR-SCH2 charset
            "{{template}}",  # template smuggling
            "${shell}",  # shell-substitution smuggling
            "E1\nE2",  # newline injection
            "-leading-dash",  # FR-SCH2 leading-char must be [A-Z]
            "lowerStart",  # FR-SCH2 leading-char must be [A-Z]
        ],
    )
    def test_setup_rejects_post_construction_eval_id_mutation(
        self,
        scratch_root: Path,
        permissive_config: EvalConfig,
        tampered_eval_id: str,
    ) -> None:
        """Construct ``HomeIsolation`` with a valid id (passes
        ``__post_init__``), then force-mutate ``eval_id`` to a FR-SCH2-
        rejected value via ``object.__setattr__`` and call
        :meth:`setup`. The containment guard's eval_id check must
        surface a :class:`HomeContainmentViolation` with
        ``check="eval_id"`` and :class:`InvalidEvalId` chained as
        ``__cause__``."""

        iso = HomeIsolation(
            eval_id="E1",  # safe at construction
            home_root=scratch_root,
            session_id="sess-vector-3",
        )

        # Bypass the dataclass freeze the same way an attacker (or an
        # accidental ``__setattr__`` shim) would.
        object.__setattr__(iso, "eval_id", tampered_eval_id)

        with pytest.raises(HomeContainmentViolation) as exc_info:
            iso.setup(config=permissive_config)

        assert exc_info.value.check == "eval_id"
        assert isinstance(exc_info.value.__cause__, InvalidEvalId)
        assert exc_info.value.eval_id == tampered_eval_id


# ---------------------------------------------------------------------------
# Attack vector 4 — loader-bypass: caller skips SuiteLoader entirely
# ---------------------------------------------------------------------------


class TestVectorLoaderBypass:
    """Vector 4 (``loader-bypass``).

    The FR-SCH2 regex enforcement lives in
    :func:`validate_eval_id` and is applied by
    :class:`SuiteLoader` on every parsed-and-expanded eval id (T01.05
    + T01.07). NFR-SEC2 mandates that a caller skipping the loader —
    for example a programmatic test, a future REPL entry point, or an
    accidentally instantiated ``HomeIsolation`` in an integration
    fixture — STILL fails closed. Two layers enforce this:

    1. ``HomeIsolation.__post_init__`` re-runs
       :func:`validate_eval_id` at construction.
    2. :func:`containment_guard` re-runs
       :func:`validate_eval_id` inside :meth:`HomeIsolation.setup`.

    The first layer raises :class:`InvalidEvalId` directly because
    ``__post_init__`` runs before any guard-wrapping; the second is
    proven separately by the post-construction mutation vector above.
    Acceptance criteria require this test to prove that *constructing*
    ``HomeIsolation`` without going through :class:`SuiteLoader` still
    fails containment — so we assert the constructor-time defense
    here. :class:`InvalidEvalId` is the canonical loader-bypass
    failure surface; in production code the CLI boundary maps it to
    :data:`INVALID_EVAL_ID_EXIT_CODE` (= 2). This pins the same
    error class :func:`containment_guard` would have chained as
    ``__cause__`` if the constructor's guard had been removed —
    keeping the bypass closure consistent across both layers.
    """

    @pytest.mark.parametrize(
        "loader_rejected_eval_id",
        [
            "../escape",
            "/absolute/path",
            "E1/with/sep",
            "9bad",
            "{{template}}",
            "${shell}",
            "E1\nE2",
        ],
    )
    def test_construction_rejects_loader_rejected_eval_id(
        self,
        scratch_root: Path,
        loader_rejected_eval_id: str,
    ) -> None:
        """Constructing :class:`HomeIsolation` directly with a
        loader-rejected eval id must raise :class:`InvalidEvalId`
        before any filesystem operation becomes reachable — proving
        the loader-bypass surface is closed at construction time."""

        with pytest.raises(InvalidEvalId) as exc_info:
            HomeIsolation(
                eval_id=loader_rejected_eval_id,
                home_root=scratch_root,
                session_id="sess-vector-4",
            )
        assert exc_info.value.eval_id == loader_rejected_eval_id

    def test_loader_bypass_setup_still_fails_when_post_init_disabled(
        self,
        scratch_root: Path,
        permissive_config: EvalConfig,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Second-layer defense: even if the constructor's
        ``__post_init__`` regex check were *removed* by a refactor
        (simulated by replacing it with a slot-only initializer), the
        guard inside :meth:`HomeIsolation.setup` MUST still reject the
        unsafe id with :class:`HomeContainmentViolation`.

        Without this layered defense the loader-bypass risk would
        re-appear the moment a future refactor weakened the
        constructor's guarantees. Asserting it here pins
        defense-in-depth as a *property*, not as a single line of
        code.

        The patch deliberately targets ``__post_init__`` (not
        ``validate_eval_id``), so the guard's own
        :func:`validate_eval_id` reference remains the real
        implementation — the two layers stay genuinely independent.
        We use a tamper id (``"9bad"``) whose textual form is a legal
        POSIX filename component so ``tempfile.mkdtemp`` succeeds
        cleanly under ``scratch_root`` and the failure that surfaces
        is the guard's eval_id check, not a kernel-level
        ``mkdtemp`` ``OSError``.
        """

        def _slot_only_init(self_inner: HomeIsolation) -> None:
            """Replacement for ``__post_init__`` that initializes the
            private slot but skips the FR-SCH2 validation."""
            object.__setattr__(self_inner, "_home_path", None)

        monkeypatch.setattr(HomeIsolation, "__post_init__", _slot_only_init)

        iso = HomeIsolation(
            eval_id="9bad",  # FR-SCH2-rejected; safe filename prefix
            home_root=scratch_root,
            session_id="sess-vector-4b",
        )

        with pytest.raises(HomeContainmentViolation) as exc_info:
            iso.setup(config=permissive_config)

        assert exc_info.value.check == "eval_id"
        # ``containment_guard`` chains the real :class:`InvalidEvalId`
        # via ``__cause__`` — proving the second layer is genuinely
        # independent of the disabled constructor check.
        assert isinstance(exc_info.value.__cause__, InvalidEvalId)
        assert exc_info.value.eval_id == "9bad"


# ---------------------------------------------------------------------------
# Coverage assertion: every NFR-SEC2 vector is exercised
# ---------------------------------------------------------------------------


def test_attack_matrix_coverage_is_complete() -> None:
    """Pin the four NFR-SEC2 vectors in code so a future refactor that
    deletes a vector class is caught here rather than silently shrinking
    the matrix.

    The roadmap row 30 wording — *"scratch-is-symlink-to-HOME attack;
    scratch-outside-allowlist; eval_id mutation post-construction;
    loader-bypass still rejected"* — is the canonical four-item list.
    """

    expected = {
        "scratch-is-symlink-to-HOME": TestVectorScratchSymlinkToHome,
        "scratch-outside-allowlist": TestVectorScratchOutsideAllowlist,
        "eval_id-mutation-post-construction": TestVectorEvalIdMutationPostConstruction,
        "loader-bypass": TestVectorLoaderBypass,
    }
    assert len(expected) == 4
    # Every vector class is importable from this module (catches a
    # rename or accidental deletion).
    for _vector, cls in expected.items():
        assert cls.__module__ == __name__
