"""FR-ISO2 ``containment_guard`` tests (Task T02.08 / D-0029).

This module owns the three-check defense-in-depth guard that
:meth:`HomeIsolation.setup` applies AFTER ``mkdtemp`` and BEFORE any
hook adapter (T02.14) writes under the per-eval HOME:

1. ``eval_id`` re-validation (FR-SCH2 / T01.05) — loader-bypass defense.
2. Scratch-root allowlist (AC12 / T01.19) — catches a scratch root
   that is symlinked to a non-allowlisted target.
3. Post-``mkdtemp`` symlink-resolved containment — catches a symlink
   inside ``home_path`` escaping ``scratch_root`` even when the textual
   prefix check would have passed.

Each check raises :class:`HomeContainmentViolation` with a distinct
``check`` identifier so reporters can bucket failures without parsing
the human-readable message. Underlying causes
(:class:`InvalidEvalId`, :class:`ScratchRootViolation`,
:class:`FileNotFoundError`) are chained via ``__cause__``.

Cross-links:

* COMP-006 method surface (T02.07): ``tests/cli/eval/test_home_isolation_extend.py``.
* AC12 / T01.19 allowlist: ``tests/cli/eval/test_scratch_root_allowlist.py``.
* FR-SCH2 / T01.05 regex: ``tests/cli/eval/test_eval_id_regex.py``.
* NFR-SEC2 attack matrix (T02.09): ``tests/cli/eval/test_defense_in_depth.py``.
* NFR-SEC3 hard guard (T02.10): ``tests/cli/eval/test_hard_guard_real_home.py``.
"""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from superclaude.cli.eval import (
    EvalConfig,
    HomeContainmentViolation,
    HomeIsolation,
    InvalidEvalId,
    ScratchRootViolation,
    containment_guard,
)

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
    """``EvalConfig`` whose allowlist includes the test's scratch root.

    Mirrors the production wiring: the orchestrator passes a config
    whose ``allowed_scratch_roots`` already contains the resolved
    scratch-root for the run; the guard then enforces against that
    same allowlist.
    """

    return EvalConfig(allowed_scratch_roots=(scratch_root,))


def _materialize_home(scratch_root: Path, eval_id: str = "E1") -> Path:
    """Helper: create a per-eval HOME the same way :meth:`HomeIsolation.setup`
    would, so the strict ``Path.resolve(strict=True)`` succeeds."""

    home = scratch_root / f"{eval_id}-test-home"
    home.mkdir()
    return home


# ---------------------------------------------------------------------------
# Check 1: eval_id regex re-validation (loader-bypass defense)
# ---------------------------------------------------------------------------


class TestEvalIdReValidation:
    """The guard re-applies :func:`validate_eval_id` so a caller that
    constructed a :class:`HomeIsolation` while bypassing
    :class:`SuiteLoader` still hard-fails."""

    @pytest.mark.parametrize(
        "bad_eval_id",
        [
            "../escape",
            "/etc/passwd",
            "E1/x",
            "..",
            "9bad",  # leading digit rejected by FR-SCH2 regex
            "",
            "with spaces",
            "{{template}}",
            "${var}",
            "E1\nE2",
        ],
    )
    def test_raises_on_unsafe_eval_id(
        self,
        scratch_root: Path,
        permissive_config: EvalConfig,
        bad_eval_id: str,
    ) -> None:
        """Any FR-SCH2-rejected id must surface as a containment
        violation with ``check='eval_id'``."""

        home = _materialize_home(scratch_root)
        with pytest.raises(HomeContainmentViolation) as exc_info:
            containment_guard(
                home_path=home,
                scratch_root=scratch_root,
                eval_id=bad_eval_id,
                config=permissive_config,
            )
        assert exc_info.value.check == "eval_id"
        assert isinstance(exc_info.value.__cause__, InvalidEvalId)
        assert exc_info.value.eval_id == bad_eval_id

    @pytest.mark.parametrize(
        "non_string_eval_id",
        [
            42,
            0,
            -1,
            True,
            False,
            None,
            Path("E1"),
            b"E1",
            ["E1"],
            {"id": "E1"},
            ("E1",),
            3.14,
        ],
    )
    def test_non_string_eval_id_is_rejected(
        self,
        scratch_root: Path,
        permissive_config: EvalConfig,
        non_string_eval_id: object,
    ) -> None:
        """YAML / programmatic scalars that decode to non-string values
        (int, bool, ``None``, ``Path``, ``bytes``, collection types,
        float) must not bypass the regex check via duck typing —
        :func:`validate_eval_id` runs ``isinstance(value, str)`` first
        and rejects every non-string."""

        home = _materialize_home(scratch_root)
        with pytest.raises(HomeContainmentViolation) as exc_info:
            containment_guard(
                home_path=home,
                scratch_root=scratch_root,
                eval_id=non_string_eval_id,  # type: ignore[arg-type]
                config=permissive_config,
            )
        assert exc_info.value.check == "eval_id"
        assert isinstance(exc_info.value.__cause__, InvalidEvalId)

    @pytest.mark.parametrize(
        "good_eval_id", ["E1", "E15", "D7", "E2.1", "E2.10", "Foo"]
    )
    def test_accepts_canonical_eval_ids(
        self,
        scratch_root: Path,
        permissive_config: EvalConfig,
        good_eval_id: str,
    ) -> None:
        """Canonical and parameterize-expanded ids must pass check 1."""

        home = _materialize_home(scratch_root, eval_id=good_eval_id)
        # No exception
        containment_guard(
            home_path=home,
            scratch_root=scratch_root,
            eval_id=good_eval_id,
            config=permissive_config,
        )


# ---------------------------------------------------------------------------
# Check 2: scratch-root allowlist (AC12)
# ---------------------------------------------------------------------------


class TestScratchRootAllowlist:
    """The guard re-routes through :func:`resolve_scratch_root` so a
    scratch root that is not in :attr:`EvalConfig.allowed_scratch_roots`
    — or one whose symlink target escapes the allowlist — fails."""

    def test_raises_when_scratch_root_outside_default_allowlist(
        self, scratch_root: Path
    ) -> None:
        """A default :class:`EvalConfig` does not allow random tmp paths;
        passing it explicitly proves the canonical allowlist refuses
        ``tmp_path``-derived scratch roots."""

        home = _materialize_home(scratch_root)
        with pytest.raises(HomeContainmentViolation) as exc_info:
            containment_guard(
                home_path=home,
                scratch_root=scratch_root,
                eval_id="E1",
                config=EvalConfig(),  # canonical defaults
            )
        assert exc_info.value.check == "scratch_root_allowlist"
        assert isinstance(exc_info.value.__cause__, ScratchRootViolation)

    def test_raises_when_scratch_root_symlinked_outside_allowlist(
        self, tmp_path: Path
    ) -> None:
        """A scratch root that LOOKS allowlisted but is actually a
        symlink to a non-allowlisted target must fail."""

        # Build a real "outside" target the symlink will point to.
        outside_target = tmp_path / "OUTSIDE_ALLOWLIST"
        outside_target.mkdir()
        (outside_target / "marker").write_text("would-be-escape")

        # Real allowlisted dir (will be referenced via symlink).
        allowed_dir = tmp_path / "allowed"
        allowed_dir.mkdir()

        scratch_link = tmp_path / "scratch-symlink"
        scratch_link.symlink_to(outside_target)

        # Config allows only ``allowed_dir`` — the symlink target
        # ``outside_target`` is NOT in the allowlist.
        config = EvalConfig(allowed_scratch_roots=(allowed_dir,))

        home = scratch_link / "E1-home"
        home.mkdir()

        with pytest.raises(HomeContainmentViolation) as exc_info:
            containment_guard(
                home_path=home,
                scratch_root=scratch_link,
                eval_id="E1",
                config=config,
            )
        assert exc_info.value.check == "scratch_root_allowlist"

    def test_uses_evalconfig_allowed_scratch_roots_as_source_of_truth(
        self, tmp_path: Path
    ) -> None:
        """The allowlist MUST come from ``config.allowed_scratch_roots``;
        no other module embeds a hard-coded copy. Narrow the config to
        a single non-default root and prove the guard follows."""

        only_allowed = tmp_path / "only-this"
        only_allowed.mkdir()
        other = tmp_path / "other"
        other.mkdir()

        home = other / "E1-home"
        home.mkdir()

        config = EvalConfig(allowed_scratch_roots=(only_allowed,))

        # ``other`` is NOT in the narrowed allowlist; must fail.
        with pytest.raises(HomeContainmentViolation) as exc_info:
            containment_guard(
                home_path=home,
                scratch_root=other,
                eval_id="E1",
                config=config,
            )
        assert exc_info.value.check == "scratch_root_allowlist"

    def test_passes_when_scratch_root_in_explicit_allowlist(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        """Happy path: the scratch root is in the supplied allowlist."""

        home = _materialize_home(scratch_root)
        containment_guard(
            home_path=home,
            scratch_root=scratch_root,
            eval_id="E1",
            config=permissive_config,
        )


# ---------------------------------------------------------------------------
# Check 3: post-mkdtemp symlink-resolved containment
# ---------------------------------------------------------------------------


class TestSymlinkResolvedContainment:
    """The guard resolves ``home_path`` with ``Path.resolve(strict=True)``
    so symlinks inside the per-eval HOME are collapsed and the result
    must equal or live beneath the resolved ``scratch_root``."""

    def test_raises_when_home_path_not_created(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        """``strict=True`` resolution must surface as a containment
        violation when the per-eval HOME has not been ``mkdtemp``-ed
        yet — this is the check that pins ordering AFTER mkdtemp."""

        nonexistent = scratch_root / "never-created"
        with pytest.raises(HomeContainmentViolation) as exc_info:
            containment_guard(
                home_path=nonexistent,
                scratch_root=scratch_root,
                eval_id="E1",
                config=permissive_config,
            )
        assert exc_info.value.check == "home_path_resolution"
        assert isinstance(exc_info.value.__cause__, FileNotFoundError)

    def test_raises_when_home_path_symlink_escapes_scratch_root(
        self, scratch_root: Path, tmp_path: Path, permissive_config: EvalConfig
    ) -> None:
        """A per-eval HOME that is actually a symlink to somewhere
        outside the scratch_root must fail check 3 even though the
        textual prefix would pass."""

        escape_target = tmp_path / "ESCAPE_TARGET"
        escape_target.mkdir()
        (escape_target / "marker").write_text("escape")

        # Symlink lives under scratch_root (so the lexical parent check
        # passes), but resolves outside scratch_root.
        home_symlink = scratch_root / "E1-via-symlink"
        home_symlink.symlink_to(escape_target)

        with pytest.raises(HomeContainmentViolation) as exc_info:
            containment_guard(
                home_path=home_symlink,
                scratch_root=scratch_root,
                eval_id="E1",
                config=permissive_config,
            )
        assert exc_info.value.check == "home_path_escape"

    def test_accepts_resolved_home_under_resolved_scratch_root(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        """Happy path: home_path is a real sub-directory of scratch_root."""

        home = _materialize_home(scratch_root)
        containment_guard(
            home_path=home,
            scratch_root=scratch_root,
            eval_id="E1",
            config=permissive_config,
        )

    def test_raises_on_symlink_chain_escape(
        self, scratch_root: Path, tmp_path: Path, permissive_config: EvalConfig
    ) -> None:
        """Resolution must chase the full symlink chain: A → B → outside.

        ``Path.resolve(strict=True)`` collapses the chain in one shot,
        so this test pins that property at the public API rather than
        trusting the standard library; if any intermediate component
        re-routes outside ``scratch_root`` the guard MUST surface
        ``check='home_path_escape'``."""

        outside = tmp_path / "OUTSIDE_FINAL"
        outside.mkdir()
        intermediate = tmp_path / "INTERMEDIATE_LINK"
        intermediate.symlink_to(outside)

        home_chain = scratch_root / "E1-via-chain"
        home_chain.symlink_to(intermediate)

        with pytest.raises(HomeContainmentViolation) as exc_info:
            containment_guard(
                home_path=home_chain,
                scratch_root=scratch_root,
                eval_id="E1",
                config=permissive_config,
            )
        assert exc_info.value.check == "home_path_escape"

    def test_accepts_home_path_equal_to_scratch_root(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        """Edge case: when home_path resolves equal to scratch_root the
        containment check must still pass (``is_relative_to`` returns
        ``False`` for equal paths in some Python versions; we cover
        both branches)."""

        containment_guard(
            home_path=scratch_root,
            scratch_root=scratch_root,
            eval_id="E1",
            config=permissive_config,
        )


# ---------------------------------------------------------------------------
# HomeIsolation.setup() integration: AFTER mkdtemp, BEFORE hook deploy
# ---------------------------------------------------------------------------


class TestIntegrationWithHomeIsolationSetup:
    """:meth:`HomeIsolation.setup` calls :func:`containment_guard`
    AFTER :func:`tempfile.mkdtemp` and BEFORE any hook deploy. The
    integration tests pin both the ordering and the failure surface
    (the partial HOME is preserved on disk so the NFR-ISO2 atomic
    wrapper in T02.13 can tag it)."""

    def test_setup_runs_containment_guard_after_mkdtemp(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        """The guard MUST observe the freshly created HOME — assertable
        by patching ``containment_guard`` to require ``home_path.exists()``
        at call time."""

        observed: dict[str, object] = {}

        def _spy(
            *,
            home_path: Path,
            scratch_root: Path,  # noqa: ARG001
            eval_id: str,  # noqa: ARG001
            config: EvalConfig | None,  # noqa: ARG001
        ) -> None:
            observed["existed_at_guard"] = home_path.exists()
            observed["home_path"] = home_path

        with patch(
            "superclaude.cli.eval.isolation.containment_guard",
            side_effect=_spy,
        ):
            iso = HomeIsolation(
                eval_id="E1",
                home_root=scratch_root,
                session_id="sess-001",
            )
            iso.setup(config=permissive_config)

        assert observed["existed_at_guard"] is True
        assert observed["home_path"] == iso.home_path

    def test_setup_allowlist_failure_blocks_mkdtemp(
        self, scratch_root: Path, tmp_path: Path
    ) -> None:
        """H5b: scratch-root allowlist refusal pre-checks BEFORE mkdtemp.

        Pre-H5b this test pinned "partial HOME preserved on disk after
        check 2 fails" — but that violated OPS-002 / NFR-SEC2 because the
        mkdtemp happened against a non-allowlisted root. Post-H5b the
        allowlist pre-check at the top of ``HomeIsolation.setup`` catches
        non-allowlisted scratch roots BEFORE mkdtemp, so no per-eval HOME
        is created. The forensic forensic_payload still carries
        ``check == "scratch_root_allowlist"`` so reporters can still
        bucket the eval as ERRORED. Symlink-escape (check 3) failures
        still preserve the partial HOME — that path is unchanged.
        """

        # Narrow config that does not include scratch_root → pre-check
        # will refuse.
        unrelated = tmp_path / "unrelated-allowlist"
        unrelated.mkdir()
        strict_config = EvalConfig(allowed_scratch_roots=(unrelated,))

        iso = HomeIsolation(
            eval_id="E1",
            home_root=scratch_root,
            session_id="sess-001",
        )
        with pytest.raises(HomeContainmentViolation) as exc_info:
            iso.setup(config=strict_config)

        assert exc_info.value.check == "scratch_root_allowlist"
        # H5b: NO per-eval HOME created — pre-check blocked mkdtemp.
        remaining = [p for p in scratch_root.iterdir() if p.name.startswith("E1-")]
        assert remaining == []
        assert not iso.is_set_up

    def test_setup_requires_explicit_config(self, scratch_root: Path) -> None:
        """:meth:`HomeIsolation.setup` MUST refuse to synthesize a
        default config that injects ``home_root`` into the allowlist —
        the QA-flagged D-0029 bypass (NFR-SEC2) where a caller could
        construct ``HomeIsolation(home_root=<attacker-controlled>)``
        and have ``setup`` add that root to the allowlist after the
        fact. Omitting ``config`` is a programming error, surfaced as
        :class:`TypeError` from the keyword-only argument."""

        iso = HomeIsolation(
            eval_id="E1",
            home_root=scratch_root,
            session_id="sess-001",
        )
        with pytest.raises(TypeError, match=r"config"):
            iso.setup()  # type: ignore[call-arg]
        # And the HOME must NOT have been created — refusal-before-
        # side-effects per NFR-SEC2.
        assert not any(scratch_root.iterdir())

    def test_setup_catches_symlink_escape_under_explicit_config(
        self, tmp_path: Path
    ) -> None:
        """Check 3 (symlink-resolved containment) still fires when a
        legitimate caller supplies a permissive ``EvalConfig`` whose
        allowlist matches the scratch root but the per-eval HOME is a
        symlink to a target outside the scratch root. This pins that
        the three checks are layered (not "first match wins")."""

        escape_target = tmp_path / "ESCAPE_TARGET"
        escape_target.mkdir()

        scratch_root = tmp_path / "eval-runs"
        scratch_root.mkdir()

        # Pre-create a symlinked HOME with the eval_id prefix that
        # ``mkdtemp`` would return. Patch ``tempfile.mkdtemp`` to hand
        # the symlink back so :func:`containment_guard` sees a path
        # that lives lexically under ``scratch_root`` but resolves
        # outside it.
        with patch("superclaude.cli.eval.isolation.tempfile.mkdtemp") as mock_mkdtemp:
            evil_home = scratch_root / "E1-evilXXXXXX"
            evil_home.symlink_to(escape_target)
            mock_mkdtemp.return_value = str(evil_home)

            iso = HomeIsolation(
                eval_id="E1",
                home_root=scratch_root,
                session_id="sess-001",
            )
            config = EvalConfig(allowed_scratch_roots=(scratch_root,))
            with pytest.raises(HomeContainmentViolation) as exc_info:
                iso.setup(config=config)
            assert exc_info.value.check == "home_path_escape"

    def test_setup_propagates_eval_id_check_from_guard(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        """The constructor's ``__post_init__`` already enforces the
        regex, so a containment failure on check 1 should be
        unreachable via the public API — but we pin the behavior by
        patching :func:`validate_eval_id` to no-op at construction
        time, proving the guard is the second layer that catches a
        bypass."""

        iso = HomeIsolation(
            eval_id="E1",
            home_root=scratch_root,
            session_id="sess-001",
        )
        # Force-mutate the (frozen) eval_id via object.__setattr__ to
        # simulate post-construction tampering: the guard inside
        # setup() must still reject.
        object.__setattr__(iso, "eval_id", "../escape")

        with pytest.raises(HomeContainmentViolation) as exc_info:
            iso.setup(config=permissive_config)
        assert exc_info.value.check == "eval_id"


# ---------------------------------------------------------------------------
# Exception payload contract
# ---------------------------------------------------------------------------


class TestHomeContainmentViolationPayload:
    """The exception carries forensic-quality fields so reporters can
    render the failure without re-resolving paths or re-running regex
    checks."""

    def test_exception_records_check_identifier(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        home = _materialize_home(scratch_root)
        with pytest.raises(HomeContainmentViolation) as exc_info:
            containment_guard(
                home_path=home,
                scratch_root=scratch_root,
                eval_id="../escape",
                config=permissive_config,
            )
        assert exc_info.value.check == "eval_id"

    def test_exception_records_verbatim_inputs(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        """The original (un-resolved) ``home_path`` / ``scratch_root``
        and the raw ``eval_id`` must be retained verbatim."""

        home = _materialize_home(scratch_root)
        with pytest.raises(HomeContainmentViolation) as exc_info:
            containment_guard(
                home_path=home,
                scratch_root=scratch_root,
                eval_id="../escape",
                config=permissive_config,
            )
        assert exc_info.value.home_path == home
        assert exc_info.value.scratch_root == scratch_root
        assert exc_info.value.eval_id == "../escape"

    def test_exception_str_includes_all_fields(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        """The default ``str()`` rendering must be self-contained so
        ``logger.error(exc)`` produces a one-line forensic trail."""

        home = _materialize_home(scratch_root)
        with pytest.raises(HomeContainmentViolation) as exc_info:
            containment_guard(
                home_path=home,
                scratch_root=scratch_root,
                eval_id="../escape",
                config=permissive_config,
            )
        rendered = str(exc_info.value)
        assert "eval_id" in rendered
        assert "../escape" in rendered
        assert str(home) in rendered
        assert str(scratch_root) in rendered

    def test_exception_chains_underlying_cause(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        """``__cause__`` MUST point at the underlying exception so
        forensic tooling can walk the chain (e.g., to recover the
        offending ``ValidationError`` path)."""

        home = _materialize_home(scratch_root)
        with pytest.raises(HomeContainmentViolation) as exc_info:
            containment_guard(
                home_path=home,
                scratch_root=scratch_root,
                eval_id="../escape",
                config=permissive_config,
            )
        assert isinstance(exc_info.value.__cause__, InvalidEvalId)
        assert exc_info.value.__cause__.eval_id == "../escape"


# ---------------------------------------------------------------------------
# Hard-guard sanity: real ``~/.claude`` is never touched by the guard
# ---------------------------------------------------------------------------


def test_guard_does_not_write_under_real_home(
    scratch_root: Path,
    permissive_config: EvalConfig,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Sanity check: invoking the guard does not touch
    ``os.path.expanduser('~')``. Full hard-guard testing lives in
    T02.10."""

    fake_home = tmp_path / "FAKE_REAL_HOME_SENTINEL"
    fake_home.mkdir()
    monkeypatch.setenv("HOME", str(fake_home))

    home = _materialize_home(scratch_root)
    containment_guard(
        home_path=home,
        scratch_root=scratch_root,
        eval_id="E1",
        config=permissive_config,
    )

    # Nothing should have been created under the fake HOME sentinel.
    assert not any(fake_home.iterdir())
    # And the real $HOME path must not have been used for resolution.
    assert os.path.commonpath([str(home), str(fake_home)]) != str(fake_home)
