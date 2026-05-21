"""NFR-ISO2 atomic-setup contract tests (Task T02.13 / D-0033).

These tests pin the NFR-ISO2 contract layered on top of COMP-006
(T02.11): any exception raised from inside
:meth:`HomeIsolation.setup` AFTER :func:`tempfile.mkdtemp` MUST leave
the per-eval HOME on disk. Non-containment exceptions additionally
drop a ``setup_failed`` artifact tag at
``<home>/.eval-meta/setup_failed`` whose first line is the offending
exception class name. The tag is the disk-level signal an
:class:`EvalRunner` (T03.x) uses to bucket the eval as ERRORED rather
than FAIL.

:class:`HomeContainmentViolation` is the explicit exception to the
tag-write rule: writing under a HOME the FR-ISO2 guard just refused
could land under real ``~/.claude/`` when the scratch root or the
``mkdtemp`` result symlinks there (the attack matrix exercised by
NFR-SEC3 in ``test_hard_guard_real_home.py``). The violation
exception itself is the structured forensic signal.

Cross-links:

* COMP-006 integrated contract — ``tests/cli/eval/test_home_isolation.py``
  (T02.11 / D-0032).
* FR-ISO2 containment guard — ``tests/cli/eval/test_path_containment.py``
  (T02.08 / D-0029).
* NFR-SEC3 hard guard — ``tests/cli/eval/test_hard_guard_real_home.py``
  (T02.10 / D-0031).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.eval import (
    SETUP_FAILED_TAG_RELPATH,
    EvalConfig,
    HomeContainmentViolation,
    HomeIsolation,
)
from superclaude.cli.eval import isolation as iso_module


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def scratch_root(tmp_path: Path) -> Path:
    """Per-test scratch root mirroring the orchestrator's ``--scratch-root``."""

    root = tmp_path / "eval-runs"
    root.mkdir()
    return root


@pytest.fixture
def permissive_config(scratch_root: Path) -> EvalConfig:
    """``EvalConfig`` whose allowlist contains the test scratch root."""

    return EvalConfig(allowed_scratch_roots=(scratch_root,))


@pytest.fixture
def restrictive_config() -> EvalConfig:
    """``EvalConfig`` whose allowlist excludes the test scratch root."""

    return EvalConfig(allowed_scratch_roots=())


def _build(
    scratch_root: Path,
    *,
    eval_id: str = "E1",
    session_id: str = "sess-001",
) -> HomeIsolation:
    return HomeIsolation(
        eval_id=eval_id,
        home_root=scratch_root,
        session_id=session_id,
    )


def _list_partial_homes(scratch_root: Path, eval_id: str) -> list[Path]:
    """Return all mkdtemp-created HOMEs for ``eval_id`` under ``scratch_root``.

    ``tempfile.mkdtemp`` appends a random suffix, so the test fixture
    looks the HOME up by prefix rather than reconstructing the name.
    """

    return sorted(scratch_root.glob(f"{eval_id}-*"))


def _inject_containment_guard_exception(
    monkeypatch: pytest.MonkeyPatch, exc: BaseException
) -> None:
    """Replace ``containment_guard`` so it raises ``exc`` on next call.

    The atomic-setup wrapper sits AROUND ``containment_guard``, so
    swapping the guard for a function that raises a non-containment
    exception is the cleanest way to exercise the wrapper's
    "tag the HOME" branch without smuggling a real FR-ISO2 failure
    (which is deliberately exempt — see module docstring).
    """

    def _raise(**_kwargs: object) -> None:
        raise exc

    monkeypatch.setattr(iso_module, "containment_guard", _raise)


# ---------------------------------------------------------------------------
# AC1 — HOME preserved on disk after a post-mkdtemp exception
# ---------------------------------------------------------------------------


class TestPartialHomePreservedOnException:
    """Inducing an exception inside ``setup`` after mkdtemp leaves the
    per-eval HOME on disk so the orchestrator (and post-mortem operators)
    can inspect it."""

    def test_containment_violation_preserves_home(
        self, scratch_root: Path, restrictive_config: EvalConfig
    ) -> None:
        iso = _build(scratch_root)
        with pytest.raises(HomeContainmentViolation):
            iso.setup(config=restrictive_config)
        partials = _list_partial_homes(scratch_root, "E1")
        assert len(partials) == 1
        assert partials[0].is_dir()

    def test_partial_home_recorded_on_instance_slot(
        self, scratch_root: Path, restrictive_config: EvalConfig
    ) -> None:
        iso = _build(scratch_root)
        with pytest.raises(HomeContainmentViolation):
            iso.setup(config=restrictive_config)
        # The slot stays populated so ``teardown(keep=True)`` can preserve
        # the partial HOME without re-resolving from disk.
        assert iso.is_set_up
        partials = _list_partial_homes(scratch_root, "E1")
        assert iso.home_path == partials[0]

    def test_injected_exception_preserves_home(
        self,
        scratch_root: Path,
        permissive_config: EvalConfig,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Any post-mkdtemp exception (not just FR-ISO2) preserves the HOME."""

        _inject_containment_guard_exception(
            monkeypatch, RuntimeError("synthetic harness bug")
        )

        iso = _build(scratch_root, eval_id="E2")
        with pytest.raises(RuntimeError, match="synthetic harness bug"):
            iso.setup(config=permissive_config)

        partials = _list_partial_homes(scratch_root, "E2")
        assert len(partials) == 1
        assert partials[0].is_dir()


# ---------------------------------------------------------------------------
# AC2 — setup_failed artifact tag is written for non-containment exceptions
# ---------------------------------------------------------------------------


class TestSetupFailedTagWritten:
    """The preserved HOME carries a ``.eval-meta/setup_failed`` tag whose
    first line is the offending exception class — but ONLY for
    non-containment failures (see ``TestContainmentViolationDoesNotWriteTag``
    for the NFR-SEC3 exception)."""

    def test_tag_exists_at_canonical_relpath(
        self,
        scratch_root: Path,
        permissive_config: EvalConfig,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        _inject_containment_guard_exception(
            monkeypatch, RuntimeError("post-containment bug")
        )

        iso = _build(scratch_root)
        with pytest.raises(RuntimeError):
            iso.setup(config=permissive_config)

        tag_path = iso.home_path / SETUP_FAILED_TAG_RELPATH
        assert tag_path.is_file()
        # Sanity: relpath is the documented constant.
        assert SETUP_FAILED_TAG_RELPATH == ".eval-meta/setup_failed"

    def test_tag_first_line_is_exception_class_name(
        self,
        scratch_root: Path,
        permissive_config: EvalConfig,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        _inject_containment_guard_exception(
            monkeypatch, RuntimeError("post-containment bug")
        )

        iso = _build(scratch_root)
        with pytest.raises(RuntimeError):
            iso.setup(config=permissive_config)

        tag_path = iso.home_path / SETUP_FAILED_TAG_RELPATH
        first_line = tag_path.read_text(encoding="utf-8").splitlines()[0]
        assert first_line == "RuntimeError"

    def test_tag_records_injected_exception_class(
        self,
        scratch_root: Path,
        permissive_config: EvalConfig,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        class SyntheticBug(Exception):
            pass

        _inject_containment_guard_exception(monkeypatch, SyntheticBug("kaboom"))

        iso = _build(scratch_root, eval_id="E3")
        with pytest.raises(SyntheticBug):
            iso.setup(config=permissive_config)

        tag_path = iso.home_path / SETUP_FAILED_TAG_RELPATH
        first_line = tag_path.read_text(encoding="utf-8").splitlines()[0]
        assert first_line == "SyntheticBug"

    def test_tag_body_contains_traceback(
        self,
        scratch_root: Path,
        permissive_config: EvalConfig,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        _inject_containment_guard_exception(
            monkeypatch, RuntimeError("post-containment bug")
        )

        iso = _build(scratch_root)
        with pytest.raises(RuntimeError):
            iso.setup(config=permissive_config)

        tag_path = iso.home_path / SETUP_FAILED_TAG_RELPATH
        body = tag_path.read_text(encoding="utf-8")
        assert "Traceback" in body
        # The traceback should mention the setup frame so forensics can
        # pinpoint the entry path without parsing line numbers.
        assert "isolation.py" in body

    def test_tag_relative_path_resolves_under_home(
        self,
        scratch_root: Path,
        permissive_config: EvalConfig,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        _inject_containment_guard_exception(
            monkeypatch, RuntimeError("post-containment bug")
        )

        iso = _build(scratch_root)
        with pytest.raises(RuntimeError):
            iso.setup(config=permissive_config)

        tag_path = iso.home_path / SETUP_FAILED_TAG_RELPATH
        # Defense-in-depth: the tag must live under the per-eval HOME
        # itself, never outside it.
        assert tag_path.is_relative_to(iso.home_path)


# ---------------------------------------------------------------------------
# AC2b — Containment violations DO NOT write the tag (NFR-SEC3 contract)
# ---------------------------------------------------------------------------


class TestContainmentViolationDoesNotWriteTag:
    """When :func:`containment_guard` raises, the wrapper MUST NOT write
    the ``setup_failed`` tag.

    Writing the tag under a refused HOME would breach the NFR-SEC3
    invariant exercised by ``test_hard_guard_real_home.py``: when the
    declared scratch root is (or symlinks to) real ``~/.claude/``, or
    when ``mkdtemp`` returned a symlinked path that escapes the
    scratch root, any write under the per-eval HOME lands inside the
    real ``~/.claude/`` directory. The containment exception itself
    carries the forensic payload (``check``, ``home_path``,
    ``scratch_root``, ``eval_id``, ``detail``)."""

    def test_no_tag_after_containment_violation(
        self, scratch_root: Path, restrictive_config: EvalConfig
    ) -> None:
        iso = _build(scratch_root)
        with pytest.raises(HomeContainmentViolation):
            iso.setup(config=restrictive_config)

        tag_path = iso.home_path / SETUP_FAILED_TAG_RELPATH
        assert not tag_path.exists(), (
            "containment violation MUST NOT write a tag under the refused HOME "
            "— that would breach the NFR-SEC3 no-writes invariant when the "
            "scratch root or mkdtemp result symlinks into real ~/.claude/."
        )

    def test_eval_meta_dir_not_created_after_containment_violation(
        self, scratch_root: Path, restrictive_config: EvalConfig
    ) -> None:
        iso = _build(scratch_root)
        with pytest.raises(HomeContainmentViolation):
            iso.setup(config=restrictive_config)

        eval_meta_dir = iso.home_path / ".eval-meta"
        # Stronger: not just the tag, but the parent dir must be absent
        # so listing the refused HOME shows zero post-mkdtemp writes.
        assert not eval_meta_dir.exists()

    def test_containment_violation_carries_forensic_payload(
        self, scratch_root: Path, restrictive_config: EvalConfig
    ) -> None:
        """The HomeContainmentViolation is the structured signal — it
        carries everything a reporter would have read from a tag."""

        iso = _build(scratch_root)
        try:
            iso.setup(config=restrictive_config)
        except HomeContainmentViolation as exc:
            assert exc.check  # short identifier (e.g. 'scratch_root_allowlist')
            assert exc.home_path == iso.home_path
            assert exc.scratch_root == iso.home_root
            assert exc.eval_id == iso.eval_id
            assert exc.detail  # human-readable detail
        else:
            pytest.fail("containment violation was not raised")


# ---------------------------------------------------------------------------
# AC3 — Normal path leaves no tag behind
# ---------------------------------------------------------------------------


class TestSuccessfulSetupHasNoTag:
    """A successful ``setup`` MUST NOT leave a ``setup_failed`` tag — the
    tag is the disk-level ERRORED signal."""

    def test_successful_setup_does_not_write_tag(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        iso = _build(scratch_root)
        home = iso.setup(config=permissive_config)
        try:
            tag_path = home / SETUP_FAILED_TAG_RELPATH
            assert not tag_path.exists()
        finally:
            iso.teardown(keep=False)


# ---------------------------------------------------------------------------
# AC4 — Mock EvalRunner buckets the failure as ERRORED, not FAIL
# ---------------------------------------------------------------------------


class _MockEvalRunner:
    """Minimum-viable stand-in for the T03.x :class:`EvalRunner`.

    The real EvalRunner ships in Phase 3. T02.13 only needs the
    "outcome bucketing on setup exception" surface. The mock buckets
    ERRORED on any setup exception (the exception is in hand) and
    additionally records whether the disk-level ``setup_failed`` tag
    is present — which is the contract real EvalRunner uses for
    post-mortem inspection of non-containment failures.
    """

    def __init__(self) -> None:
        self.status: str | None = None
        self.error_class: str | None = None
        self.tag_present: bool | None = None

    def run(self, iso: HomeIsolation, config: EvalConfig) -> str:
        try:
            iso.setup(config=config)
        except Exception as exc:
            # The exception itself is sufficient to bucket as ERRORED —
            # this mirrors how production EvalRunner will handle
            # non-FAIL outcomes.
            tag_path = iso.home_path / SETUP_FAILED_TAG_RELPATH
            self.tag_present = tag_path.exists()
            self.status = "ERRORED"
            self.error_class = type(exc).__name__
            iso.teardown(keep=True)
            return self.status

        # Eval body would run here. For the mock, simulate a FAIL.
        try:
            self.status = "FAIL"
            return self.status
        finally:
            iso.teardown(keep=False)


class TestMockEvalRunnerBucketsAsErrored:
    """A setup exception surfaces as ERRORED; a normal completion path
    stays FAIL/PASS-shaped."""

    def test_containment_failure_buckets_as_errored_without_tag(
        self, scratch_root: Path, restrictive_config: EvalConfig
    ) -> None:
        iso = _build(scratch_root)
        runner = _MockEvalRunner()
        outcome = runner.run(iso, restrictive_config)
        assert outcome == "ERRORED"
        assert runner.error_class == "HomeContainmentViolation"
        # NFR-SEC3 contract: refused HOMEs do not carry a tag.
        assert runner.tag_present is False

    def test_non_containment_failure_buckets_as_errored_with_tag(
        self,
        scratch_root: Path,
        permissive_config: EvalConfig,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        _inject_containment_guard_exception(
            monkeypatch, RuntimeError("synthetic harness bug")
        )

        iso = _build(scratch_root, eval_id="E4")
        runner = _MockEvalRunner()
        outcome = runner.run(iso, permissive_config)
        assert outcome == "ERRORED"
        assert runner.error_class == "RuntimeError"
        # NFR-ISO2 contract: non-containment failures DO carry a tag.
        assert runner.tag_present is True

    def test_successful_setup_does_not_bucket_as_errored(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        iso = _build(scratch_root)
        runner = _MockEvalRunner()
        outcome = runner.run(iso, permissive_config)
        # Mock body returns FAIL on success path; the point is "not ERRORED".
        assert outcome == "FAIL"
        assert runner.error_class is None


# ---------------------------------------------------------------------------
# AC5 — Tag write best-effort: secondary failures don't mask the original
# ---------------------------------------------------------------------------


class TestTagWriteBestEffort:
    """If the helper that writes the tag itself raises, the original
    exception MUST still propagate — the orchestrator MUST NOT see a
    wrapped ``OSError`` instead of the underlying setup failure."""

    def test_secondary_tag_failure_does_not_mask_original(
        self,
        scratch_root: Path,
        permissive_config: EvalConfig,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        # First, force a non-containment exception so the wrapper takes
        # the tag-write branch.
        _inject_containment_guard_exception(
            monkeypatch, RuntimeError("post-containment bug")
        )

        # Then make the tag-write helper itself raise.
        def explode(*_args: object, **_kwargs: object) -> None:
            raise OSError("tag-write boom")

        monkeypatch.setattr(iso_module, "_write_setup_failed_tag", explode)

        iso = _build(scratch_root)
        with pytest.raises(RuntimeError, match="post-containment bug"):
            iso.setup(config=permissive_config)


# ---------------------------------------------------------------------------
# AC6 — Teardown(keep=True) after failure preserves the HOME (and tag, if any)
# ---------------------------------------------------------------------------


class TestTeardownKeepTruePreservesPartialHome:
    """The orchestrator's failure branch — ``teardown(keep=True)`` after
    a failed ``setup`` — preserves the partial HOME on disk."""

    def test_teardown_keep_true_preserves_home_after_containment_violation(
        self, scratch_root: Path, restrictive_config: EvalConfig
    ) -> None:
        iso = _build(scratch_root)
        with pytest.raises(HomeContainmentViolation):
            iso.setup(config=restrictive_config)
        home = iso.home_path
        tag_path = home / SETUP_FAILED_TAG_RELPATH
        iso.teardown(keep=True)
        assert home.exists()
        # Containment violations do not write the tag.
        assert not tag_path.exists()

    def test_teardown_keep_true_preserves_home_and_tag_after_injected_exception(
        self,
        scratch_root: Path,
        permissive_config: EvalConfig,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        _inject_containment_guard_exception(
            monkeypatch, RuntimeError("post-containment bug")
        )

        iso = _build(scratch_root, eval_id="E5")
        with pytest.raises(RuntimeError):
            iso.setup(config=permissive_config)
        home = iso.home_path
        tag_path = home / SETUP_FAILED_TAG_RELPATH
        iso.teardown(keep=True)
        assert home.exists()
        assert tag_path.is_file()
        first_line = tag_path.read_text(encoding="utf-8").splitlines()[0]
        assert first_line == "RuntimeError"

    def test_teardown_keep_false_after_failure_removes_home(
        self, scratch_root: Path, restrictive_config: EvalConfig
    ) -> None:
        iso = _build(scratch_root)
        with pytest.raises(HomeContainmentViolation):
            iso.setup(config=restrictive_config)
        home = iso.home_path
        iso.teardown(keep=False)
        assert not home.exists()
