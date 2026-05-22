"""TEST-002 containment acceptance tests (Task T02.21 / D-0040).

This module is the **first-class TEST-002 deliverable** the cliEval
roadmap (row 40 / R-040) calls out as a stand-alone proof that the
HomeIsolation containment story holds end-to-end. The four AC-named
slices below mirror the wording in ``phase-2-tasklist.md`` for
T02.21 verbatim:

    1. **Allowed roots accepted** — repo ``.dev/eval-runs`` and
       ``/tmp/eval-runs`` (the two canonical M1 scratch roots from
       :class:`EvalConfig` defaults) accept a real
       :meth:`HomeIsolation.setup` call without raising.
    2. **Non-allowlisted root rejected** — any scratch root absent
       from :attr:`EvalConfig.allowed_scratch_roots` surfaces
       :class:`HomeContainmentViolation` with
       ``check="scratch_root_allowlist"`` and a
       :class:`ScratchRootViolation` ``__cause__``.
    3. **Loader-bypass defense** — constructing
       :class:`HomeIsolation` directly (without funneling through
       :class:`SuiteLoader`) still hard-fails containment, both at
       construction (``__post_init__``) and at :meth:`setup`
       (``containment_guard``).
    4. **Exit-code-2 path covered** — every containment-failure
       surface chains a ``__cause__`` whose CLI mapping is exit code
       ``2`` (:data:`INVALID_EVAL_ID_EXIT_CODE` for FR-SCH2 rejects,
       :data:`SCRATCH_ROOT_VIOLATION_EXIT_CODE` for AC12 rejects). The
       exit-code constants themselves are asserted alongside the
       containment payloads so a future drift of the constant would
       break this test before any operator sees a wrong exit code.

The unit-level guard tests live in
``tests/cli/eval/test_path_containment.py`` (T02.08 / D-0029); the
NFR-SEC2 attack matrix lives in ``tests/cli/eval/test_defense_in_depth.py``
(T02.09 / D-0030). This module deliberately overlaps neither — it
sits at the contract layer where the four TEST-002 AC bullets are
the canonical readout for downstream gates (M2 exit checkpoint
``CP-P02-END.md`` cites this module by name).

Cross-links:

* TEST-002 (this task, T02.21 / D-0040 / R-040).
* AC12 / T01.19 (``resolve_scratch_root`` allowlist source of truth).
* FR-ISO2 / T02.08 (``containment_guard``).
* FR-SCH2 / T01.05 (``validate_eval_id``).
* NFR-SEC2 / T02.09 (positive attack-matrix tests).
"""

from __future__ import annotations

import shutil
import uuid
from pathlib import Path

import pytest

from superclaude.cli.eval import (
    INVALID_EVAL_ID_EXIT_CODE,
    SCRATCH_ROOT_VIOLATION_EXIT_CODE,
    EvalConfig,
    HomeContainmentViolation,
    HomeIsolation,
    InvalidEvalId,
    ScratchRootViolation,
    containment_guard,
)


# ---------------------------------------------------------------------------
# Canonical M1 scratch-root fixtures
# ---------------------------------------------------------------------------
#
# The default :class:`EvalConfig` ships ``allowed_scratch_roots = (
# "/tmp/eval-runs", ".dev/eval-runs")`` — the two M1 scratch roots
# documented in design-spec §6 and pinned by
# :func:`_default_allowed_scratch_roots` in
# ``src/superclaude/cli/eval/config.py``. TEST-002 AC asks for both to
# be exercised at the HomeIsolation contract layer with the default
# config (no narrowed allowlist), because those are the two roots a
# real operator actually points the harness at.
#
# Each fixture creates a per-test sub-directory under the canonical
# root so concurrent test runs do not collide, and aggressively cleans
# up at teardown so the repo (and ``/tmp``) stay tidy. Unique suffixes
# come from :func:`uuid.uuid4` rather than ``tmp_path_factory`` so the
# fixture writes under the *real* canonical root, not under a pytest
# sandbox — pinning the default-config allowlist is the entire point.

_TMP_EVAL_RUNS_ROOT = Path("/tmp/eval-runs")
"""Canonical M1 scratch root the default :class:`EvalConfig` ships."""

_DEV_EVAL_RUNS_ROOT = Path(".dev/eval-runs")
"""Canonical M1 repo-relative scratch root the default config ships."""


@pytest.fixture
def tmp_eval_runs_subdir() -> Path:
    """Per-test sub-directory under ``/tmp/eval-runs`` for TEST-002 slice 1.

    Tests that target the canonical ``/tmp/eval-runs`` allowlist entry
    create their per-eval HOME *under* this directory so
    :meth:`HomeIsolation.setup` exercises the real default config —
    not a narrowed allowlist that would defeat the AC.
    """

    sub = _TMP_EVAL_RUNS_ROOT / f"test-containment-{uuid.uuid4().hex}"
    sub.mkdir(parents=True, exist_ok=True)
    try:
        yield sub
    finally:
        # ``ignore_errors`` keeps a test that left non-cleanable
        # artifacts from breaking subsequent tests; the per-test
        # uuid-suffix means a leak does not affect other tests.
        shutil.rmtree(sub, ignore_errors=True)


@pytest.fixture
def dev_eval_runs_subdir() -> Path:
    """Per-test sub-directory under repo ``.dev/eval-runs`` for slice 1.

    Repo-relative path so the resolution mirrors what a real operator
    running ``uv run pytest`` from the repo root would see — the
    default-config allowlist contains the *relative* ``.dev/eval-runs``
    entry and ``_resolve_prefix`` anchors it against the process CWD.
    """

    sub = _DEV_EVAL_RUNS_ROOT / f"test-containment-{uuid.uuid4().hex}"
    sub.mkdir(parents=True, exist_ok=True)
    try:
        yield sub
    finally:
        shutil.rmtree(sub, ignore_errors=True)


# ---------------------------------------------------------------------------
# Slice 1 — allowed roots accepted (TEST-002 AC: ``repo .dev`` + ``/tmp``)
# ---------------------------------------------------------------------------


class TestAllowedRootsAccepted:
    """Slice 1 of TEST-002.

    The default :class:`EvalConfig` ships both canonical M1 scratch
    roots (``/tmp/eval-runs`` and repo ``.dev/eval-runs``). A
    legitimate :meth:`HomeIsolation.setup` under either must succeed
    without raising. Asserts cover three independent layers:

    * :func:`containment_guard` returns cleanly (no exception).
    * :meth:`HomeIsolation.setup` returns a real per-eval HOME path.
    * The returned HOME resolves under the canonical allowlist entry,
      proving the default-config wiring (not a narrowed test allowlist)
      is the surface under test.
    """

    def test_tmp_eval_runs_accepted_under_default_config(
        self, tmp_eval_runs_subdir: Path
    ) -> None:
        """``/tmp/eval-runs`` is accepted by the default config.

        Pins the default-config wiring: no narrowed allowlist, no
        per-test ``EvalConfig(allowed_scratch_roots=...)``. The
        canonical ``/tmp/eval-runs`` entry alone must let the call
        through.
        """

        config = EvalConfig()  # canonical M1 defaults — no override
        iso = HomeIsolation(
            eval_id="E1",
            home_root=tmp_eval_runs_subdir,
            session_id="sess-tmp-slice1",
        )

        home = iso.setup(config=config)

        # The per-eval HOME was minted under the canonical allowlist
        # entry — proving the default-config allowlist is the
        # acceptance surface.
        assert home.resolve().is_relative_to(_TMP_EVAL_RUNS_ROOT.resolve())
        assert iso.is_set_up is True

        iso.teardown(keep=False)

    def test_dev_eval_runs_accepted_under_default_config(
        self, dev_eval_runs_subdir: Path
    ) -> None:
        """Repo ``.dev/eval-runs`` is accepted by the default config.

        ``.dev/eval-runs`` ships *relative* in the default allowlist
        so resolution anchors against the process CWD. This test
        pins that property — running ``uv run pytest`` from the repo
        root must resolve the prefix to the in-repo directory.
        """

        config = EvalConfig()  # canonical M1 defaults — no override
        iso = HomeIsolation(
            eval_id="E1",
            home_root=dev_eval_runs_subdir,
            session_id="sess-dev-slice1",
        )

        home = iso.setup(config=config)

        assert home.resolve().is_relative_to(_DEV_EVAL_RUNS_ROOT.resolve())
        assert iso.is_set_up is True

        iso.teardown(keep=False)

    def test_containment_guard_passes_for_tmp_eval_runs(
        self, tmp_eval_runs_subdir: Path
    ) -> None:
        """Pure ``containment_guard`` accepts ``/tmp/eval-runs``.

        Strips the :meth:`HomeIsolation.setup` wrapper so the guard's
        positive-acceptance behavior on the canonical root is pinned
        without ``mkdtemp`` side effects in the loop.
        """

        # ``containment_guard`` requires ``home_path`` to exist on disk
        # (its ``Path.resolve(strict=True)`` enforces post-mkdtemp
        # ordering); the fixture already created the sub-directory.
        containment_guard(
            home_path=tmp_eval_runs_subdir,
            scratch_root=_TMP_EVAL_RUNS_ROOT,
            eval_id="E1",
            config=EvalConfig(),
        )

    def test_containment_guard_passes_for_dev_eval_runs(
        self, dev_eval_runs_subdir: Path
    ) -> None:
        """Pure ``containment_guard`` accepts ``.dev/eval-runs``."""

        containment_guard(
            home_path=dev_eval_runs_subdir,
            scratch_root=_DEV_EVAL_RUNS_ROOT,
            eval_id="E1",
            config=EvalConfig(),
        )


# ---------------------------------------------------------------------------
# Slice 2 — non-allowlisted roots rejected (TEST-002 AC)
# ---------------------------------------------------------------------------


class TestNonAllowlistedRootsRejected:
    """Slice 2 of TEST-002.

    A scratch root absent from :attr:`EvalConfig.allowed_scratch_roots`
    must surface :class:`HomeContainmentViolation` with the
    ``scratch_root_allowlist`` check identifier. The chained
    ``__cause__`` is the :class:`ScratchRootViolation` from
    :func:`resolve_scratch_root` — the single AC12 source of truth.

    Both ingress surfaces are exercised:

    * :func:`containment_guard` called directly (the unit boundary).
    * :meth:`HomeIsolation.setup` (the integration boundary).
    """

    @pytest.mark.parametrize(
        "rejected_subpath",
        [
            "user-home-dot-claude",  # stands in for ``$HOME/.claude``
            "etc-style-system-path",  # stands in for ``/etc/...``
            "var-lib-eval-runs",      # ``/var/lib`` close-but-not-allowed
            "root-dot-claude",        # stands in for ``/root/.claude``
            "tmp-other-runs",         # ``/tmp/other-runs`` prefix-collision
        ],
    )
    def test_setup_rejects_root_outside_default_allowlist(
        self, tmp_path: Path, rejected_subpath: str
    ) -> None:
        """A ``tmp_path``-derived directory is the safest stand-in for
        every "non-allowlisted" filesystem location an operator might
        mis-supply. The default :class:`EvalConfig` allowlist does NOT
        cover ``tmp_path``, so every parametrized scratch_root must
        fail with ``check="scratch_root_allowlist"``.
        """

        scratch = tmp_path / rejected_subpath
        scratch.mkdir(parents=True)
        iso = HomeIsolation(
            eval_id="E1",
            home_root=scratch,
            session_id="sess-rejected",
        )

        with pytest.raises(HomeContainmentViolation) as exc_info:
            iso.setup(config=EvalConfig())  # default allowlist — rejects

        assert exc_info.value.check == "scratch_root_allowlist"
        assert isinstance(exc_info.value.__cause__, ScratchRootViolation)
        # The verbatim (un-resolved) ``scratch_root`` is preserved for
        # forensic rendering — operators see exactly what they typed.
        assert exc_info.value.scratch_root == scratch

    def test_containment_guard_rejects_root_outside_default_allowlist(
        self, tmp_path: Path
    ) -> None:
        """Unit-level mirror: pure ``containment_guard`` rejects the
        same way :meth:`HomeIsolation.setup` does. Keeps the guard
        from drifting away from the setup wrapper's behavior."""

        scratch = tmp_path / "off-policy-scratch"
        scratch.mkdir()
        home = scratch / "E1-home"
        home.mkdir()

        with pytest.raises(HomeContainmentViolation) as exc_info:
            containment_guard(
                home_path=home,
                scratch_root=scratch,
                eval_id="E1",
                config=EvalConfig(),
            )

        assert exc_info.value.check == "scratch_root_allowlist"
        assert isinstance(exc_info.value.__cause__, ScratchRootViolation)

    def test_narrowed_allowlist_rejects_canonical_tmp_eval_runs(
        self, tmp_path: Path
    ) -> None:
        """The allowlist is the *sole* source of truth: a config that
        narrows the allowlist to a single non-canonical entry must
        reject even the canonical ``/tmp/eval-runs`` prefix. Proves
        :class:`EvalConfig.allowed_scratch_roots` is what drives the
        check — nothing inside :func:`containment_guard` synthesizes
        a canonical fallback after the fact (the NFR-SEC2 bypass
        closure)."""

        only_allowed = tmp_path / "narrowed-allowlist-only"
        only_allowed.mkdir()
        config = EvalConfig(allowed_scratch_roots=(only_allowed,))

        iso = HomeIsolation(
            eval_id="E1",
            home_root=_TMP_EVAL_RUNS_ROOT,
            session_id="sess-narrowed",
        )

        # The canonical root is NOT in the narrowed allowlist — must reject.
        with pytest.raises(HomeContainmentViolation) as exc_info:
            iso.setup(config=config)

        assert exc_info.value.check == "scratch_root_allowlist"


# ---------------------------------------------------------------------------
# Slice 3 — loader-bypass defense (TEST-002 AC)
# ---------------------------------------------------------------------------


class TestLoaderBypassDefense:
    """Slice 3 of TEST-002.

    NFR-SEC2 requires that a caller constructing :class:`HomeIsolation`
    directly — bypassing :class:`SuiteLoader` — still hard-fails
    containment. Two independent layers enforce the property:

    * Layer A: ``__post_init__`` re-runs :func:`validate_eval_id` so
      an unsafe ``eval_id`` raises :class:`InvalidEvalId` at
      construction, before any filesystem write becomes reachable.
    * Layer B: :func:`containment_guard` re-runs the same check
      inside :meth:`setup`, so a future refactor that weakens
      ``__post_init__`` does not re-open the bypass.

    Both layers are pinned here. The acceptance criterion specifically
    calls out "constructing HomeIsolation directly (without SuiteLoader)
    and confirms containment still applies" — layer A is the most
    direct readout of that, and layer B keeps the defense layered.
    """

    @pytest.mark.parametrize(
        "loader_rejected_eval_id",
        [
            "../escape",         # path traversal
            "/etc/passwd",       # absolute-path smuggling
            "E1/with/sep",       # embedded path separator
            "..",                # parent-dir literal
            "9bad",              # FR-SCH2 leading-digit reject
            "",                  # empty string
            "with spaces",       # whitespace
            "{{template}}",      # un-expanded parameterize token
            "${shell}",          # shell-substitution smuggling
            "E1\nE2",            # newline injection
        ],
    )
    def test_direct_construction_rejects_loader_rejected_id(
        self,
        tmp_path: Path,
        loader_rejected_eval_id: str,
    ) -> None:
        """Layer A: a caller skipping :class:`SuiteLoader` and feeding
        an unsafe id to :class:`HomeIsolation` hard-fails at
        construction time (``__post_init__``)."""

        # ``home_root`` is intentionally a real, in-allowlist tmp_path —
        # we want the failure surface to be the eval_id check, not a
        # coincidental allowlist miss.
        with pytest.raises(InvalidEvalId) as exc_info:
            HomeIsolation(
                eval_id=loader_rejected_eval_id,
                home_root=tmp_path,
                session_id="sess-loader-bypass-A",
            )
        assert exc_info.value.eval_id == loader_rejected_eval_id

    def test_direct_construction_with_post_init_disabled_is_caught_by_guard(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Layer B: even if ``__post_init__`` is replaced with a
        slot-only initializer (simulating a refactor that drops the
        constructor check), :func:`containment_guard` inside
        :meth:`setup` MUST still reject the unsafe id.

        Patches ``__post_init__`` rather than :func:`validate_eval_id`
        so the guard's own validator reference remains the real
        implementation — the two layers must stay independent.
        Uses ``"9bad"`` (FR-SCH2-rejected; legal POSIX filename) so
        ``tempfile.mkdtemp`` succeeds and the failure surfaces from
        the guard, not from the kernel.
        """

        scratch = tmp_path / "scratch"
        scratch.mkdir()
        config = EvalConfig(allowed_scratch_roots=(scratch,))

        def _slot_only_init(self_inner: HomeIsolation) -> None:
            object.__setattr__(self_inner, "_home_path", None)

        monkeypatch.setattr(HomeIsolation, "__post_init__", _slot_only_init)

        iso = HomeIsolation(
            eval_id="9bad",  # FR-SCH2 reject; legal filename
            home_root=scratch,
            session_id="sess-loader-bypass-B",
        )

        with pytest.raises(HomeContainmentViolation) as exc_info:
            iso.setup(config=config)

        assert exc_info.value.check == "eval_id"
        assert isinstance(exc_info.value.__cause__, InvalidEvalId)
        assert exc_info.value.eval_id == "9bad"

    def test_direct_construction_without_loader_still_hits_allowlist_check(
        self, tmp_path: Path
    ) -> None:
        """A loader-bypassing caller that supplies a valid id but a
        non-allowlisted ``home_root`` ALSO hits containment — pins
        that the bypass closure covers both the eval_id check and
        the scratch-root check (loader bypass is not "eval_id-only").
        """

        # Default allowlist does not include ``tmp_path`` — perfect
        # stand-in for "any non-allowlisted location an attacker could
        # smuggle past the loader".
        iso = HomeIsolation(
            eval_id="E1",
            home_root=tmp_path,
            session_id="sess-loader-bypass-C",
        )
        with pytest.raises(HomeContainmentViolation) as exc_info:
            iso.setup(config=EvalConfig())  # canonical defaults

        assert exc_info.value.check == "scratch_root_allowlist"
        assert isinstance(exc_info.value.__cause__, ScratchRootViolation)


# ---------------------------------------------------------------------------
# Slice 4 — exit-code-2 path covered (TEST-002 AC)
# ---------------------------------------------------------------------------


class TestExitCodeTwoPath:
    """Slice 4 of TEST-002.

    Every containment-failure exception that reaches the CLI boundary
    MUST map to exit code ``2``. There are two underlying causes a
    :class:`HomeContainmentViolation` can chain (per FR-ISO2):

    * :class:`InvalidEvalId` — CLI mapping
      :data:`INVALID_EVAL_ID_EXIT_CODE` (= 2).
    * :class:`ScratchRootViolation` — CLI mapping
      :data:`SCRATCH_ROOT_VIOLATION_EXIT_CODE` (= 2).

    The constants are asserted as ``== 2`` so a future drift of the
    exit-code mapping breaks this test before any operator sees a
    wrong exit code. The chained ``__cause__`` is asserted on a real
    containment failure so the wiring stays end-to-end.
    """

    def test_invalid_eval_id_exit_code_is_two(self) -> None:
        """FR-SCH2 reject → exit 2 (constant pin)."""

        assert INVALID_EVAL_ID_EXIT_CODE == 2

    def test_scratch_root_violation_exit_code_is_two(self) -> None:
        """AC12 reject → exit 2 (constant pin)."""

        assert SCRATCH_ROOT_VIOLATION_EXIT_CODE == 2

    def test_exit_codes_are_aligned_with_each_other(self) -> None:
        """Pins the "single ``2`` from the operator's POV" invariant
        documented at ``config.py`` and ``loader.py``. If a future
        refactor accidentally diverges the two surfaces (e.g., makes
        AC12 → exit 3), this test catches it before it ships."""

        assert INVALID_EVAL_ID_EXIT_CODE == SCRATCH_ROOT_VIOLATION_EXIT_CODE

    def test_containment_failure_chains_exit2_cause_for_eval_id(
        self, tmp_path: Path
    ) -> None:
        """Eval-id rejection inside :meth:`HomeIsolation.setup`
        surfaces a :class:`HomeContainmentViolation` whose
        ``__cause__`` is :class:`InvalidEvalId` — the CLI maps that
        cause to :data:`INVALID_EVAL_ID_EXIT_CODE` (= 2). Asserts
        both the chain and the constant so the readout is unambiguous.
        """

        scratch = tmp_path / "scratch"
        scratch.mkdir()
        config = EvalConfig(allowed_scratch_roots=(scratch,))

        iso = HomeIsolation(
            eval_id="E1",
            home_root=scratch,
            session_id="sess-exit2-eval-id",
        )
        # Post-construction tamper — the constructor's
        # ``__post_init__`` already passed, so the guard inside
        # :meth:`setup` is the layer that fires.
        object.__setattr__(iso, "eval_id", "9bad")

        with pytest.raises(HomeContainmentViolation) as exc_info:
            iso.setup(config=config)

        assert exc_info.value.check == "eval_id"
        assert isinstance(exc_info.value.__cause__, InvalidEvalId)
        # The chained cause is the exit-2 mapped exception.
        assert INVALID_EVAL_ID_EXIT_CODE == 2

    def test_containment_failure_chains_exit2_cause_for_scratch_root(
        self, tmp_path: Path
    ) -> None:
        """AC12 rejection inside :meth:`HomeIsolation.setup` surfaces
        a :class:`HomeContainmentViolation` whose ``__cause__`` is
        :class:`ScratchRootViolation` — the CLI maps that cause to
        :data:`SCRATCH_ROOT_VIOLATION_EXIT_CODE` (= 2). Both the
        chain and the constant are pinned."""

        # ``tmp_path`` is not in the canonical default allowlist.
        iso = HomeIsolation(
            eval_id="E1",
            home_root=tmp_path,
            session_id="sess-exit2-scratch-root",
        )
        with pytest.raises(HomeContainmentViolation) as exc_info:
            iso.setup(config=EvalConfig())

        assert exc_info.value.check == "scratch_root_allowlist"
        assert isinstance(exc_info.value.__cause__, ScratchRootViolation)
        assert SCRATCH_ROOT_VIOLATION_EXIT_CODE == 2

    def test_direct_loader_bypass_exit_path_is_invalid_eval_id(
        self, tmp_path: Path
    ) -> None:
        """The TEST-002 AC for loader-bypass explicitly references
        the exit-2 path: a caller constructing :class:`HomeIsolation`
        directly with an unsafe id raises :class:`InvalidEvalId` at
        construction (``__post_init__``) which the CLI maps to exit
        ``2``. Asserts the exception class and the constant together
        so the bypass closure and the exit code stay consistent."""

        with pytest.raises(InvalidEvalId):
            HomeIsolation(
                eval_id="../escape",
                home_root=tmp_path,
                session_id="sess-exit2-loader-bypass",
            )
        assert INVALID_EVAL_ID_EXIT_CODE == 2


# ---------------------------------------------------------------------------
# T4b / H5b — isolation.py pre-check refuses non-allowlisted home_root
#             BEFORE mkdir (OPS-002 ordering site 2)
# ---------------------------------------------------------------------------


def test_home_isolation_setup_rejects_non_allowlisted_home_root_before_mkdir(
    tmp_path: Path,
) -> None:
    """T4b / H5b / OPS-002: ``HomeIsolation.setup`` refuses a non-allowlisted
    ``home_root`` BEFORE ``self.home_root.mkdir(...)`` materializes anything.

    Pre-H5b the post-mkdtemp ``containment_guard`` was the gate — meaning
    ``self.home_root.mkdir(...)`` ran first, then ``tempfile.mkdtemp``
    created a per-eval HOME under it, and only AFTER all that did the
    allowlist check refuse. That violated OPS-002 because every refused
    invocation materialized a directory tree on disk outside the
    allowlist.

    Post-H5b the pre-check at the top of ``setup`` resolves ``self.home_root``
    and refuses against ``config.allowed_scratch_roots`` BEFORE any
    filesystem write. This test pins both halves of the contract:

    1. ``HomeContainmentViolation`` raises (with ``check == "scratch_root_allowlist"``).
    2. No directory was created under the non-allowlisted ``home_root``.
    """

    non_allowlisted_root = tmp_path / "outside-allowlist-root"
    # Pre-create the parent so the test can observe whether ``setup``'s
    # internal ``home_root.mkdir`` ran (it must NOT post-H5b).
    parent = non_allowlisted_root.parent

    allowed = tmp_path / "allowed"
    allowed.mkdir()
    narrow_config = EvalConfig(allowed_scratch_roots=(allowed,))

    iso = HomeIsolation(
        eval_id="E1",
        home_root=non_allowlisted_root,
        session_id="sess-t4b",
    )

    parent_contents_before = sorted(p.name for p in parent.iterdir())

    with pytest.raises(HomeContainmentViolation) as exc_info:
        iso.setup(config=narrow_config)

    assert exc_info.value.check == "scratch_root_allowlist"
    # H5b: no on-disk side effect — ``home_root`` itself was never
    # created, and certainly no per-eval HOME was mkdtemp'd under it.
    assert not non_allowlisted_root.exists(), (
        f"H5b violation: pre-check did NOT refuse before mkdir — "
        f"{non_allowlisted_root} exists on disk after the refusal."
    )
    parent_contents_after = sorted(p.name for p in parent.iterdir())
    assert parent_contents_before == parent_contents_after, (
        f"H5b violation: parent directory contents changed during the "
        f"refused setup. before={parent_contents_before} "
        f"after={parent_contents_after}"
    )
    assert not iso.is_set_up


# ---------------------------------------------------------------------------
# Slice coverage pin — every TEST-002 AC slice has at least one test
# ---------------------------------------------------------------------------


def test_test_002_slice_coverage_is_complete() -> None:
    """Pin the four TEST-002 AC slices in code so a future refactor
    that deletes a slice class is caught here rather than silently
    shrinking the matrix.

    The acceptance-criteria wording — *"repo .dev accepted, /tmp
    accepted, non-allowlisted root rejected, loader-bypass rejected,
    exit-2 path covered"* — collapses to the four slices below.
    """

    expected = {
        "allowed-roots-accepted": TestAllowedRootsAccepted,
        "non-allowlisted-rejected": TestNonAllowlistedRootsRejected,
        "loader-bypass-defense": TestLoaderBypassDefense,
        "exit-code-2-path": TestExitCodeTwoPath,
    }
    assert len(expected) == 4
    for _slice, cls in expected.items():
        assert cls.__module__ == __name__
