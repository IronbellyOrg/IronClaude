"""COMP-006 integrated HomeIsolation contract tests (Task T02.11 / D-0032).

This module owns the COMP-006 finalization contract: the four
:class:`HomeIsolation` methods (``setup``, ``env``, ``teardown``,
``state_path``) wired together with the FR-ISO2 containment guard,
exercised as a single integrated unit rather than method-by-method.

Per-method behavior is exhaustively covered upstream:

* ``tests/cli/eval/test_home_isolation_extend.py`` (T02.07 / D-0028) —
  per-method FR-ISO1 surface tests.
* ``tests/cli/eval/test_path_containment.py`` (T02.08 / D-0029) —
  per-check FR-ISO2 guard tests.
* ``tests/cli/eval/test_defense_in_depth.py`` (T02.09 / D-0030) —
  NFR-SEC2 attack-matrix tests.
* ``tests/cli/eval/test_hard_guard_real_home.py`` (T02.10 / D-0031) —
  NFR-SEC3 real-``~/.claude/`` refusal tests.

What this module adds on top is the **integrated COMP-006 contract** —
the four AC bullets from T02.11:

1. ``HomeIsolation`` exposes the four COMP-006 methods with their
   declared signatures.
2. ``state_path(suffix)`` returns paths that ``is_relative_to`` both
   ``home_path`` AND ``home_root`` — the per-eval HOME stays anchored
   under the scratch root that the orchestrator (T03.16) declared.
3. ``teardown(keep=True)`` preserves the per-eval HOME on disk;
   ``teardown(keep=False)`` removes it. Both branches clear the
   private ``_home_path`` slot so subsequent ``env`` / ``state_path``
   calls fail loudly.
4. The lifecycle ``setup -> env -> state_path -> teardown`` round-
   trips cleanly on a fresh instance, on a re-setup after teardown,
   and across parallel sibling instances.

Cross-links: D-0032 spec records the integrated component contract;
the hook-adapter integration surface (``deploy_hooks_to``) lands in
T02.14 / D-0034 and slots in via the public ``home_path`` property
without touching this contract.
"""

from __future__ import annotations

import inspect
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from superclaude.cli.eval import (
    EvalConfig,
    HomeContainmentViolation,
    HomeIsolation,
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
    """``EvalConfig`` whose allowlist contains the test scratch root."""

    return EvalConfig(allowed_scratch_roots=(scratch_root,))


def _build(
    scratch_root: Path,
    *,
    eval_id: str = "E1",
    session_id: str = "sess-001",
    time_offset_sec: int = 0,
) -> HomeIsolation:
    """Convenience builder mirroring orchestrator construction (T03.16)."""

    return HomeIsolation(
        eval_id=eval_id,
        home_root=scratch_root,
        session_id=session_id,
        time_offset_sec=time_offset_sec,
    )


# ---------------------------------------------------------------------------
# AC1 — COMP-006 method surface
# ---------------------------------------------------------------------------


class TestComp006MethodSurface:
    """The four COMP-006 method names exist with the declared signatures."""

    def test_setup_signature_takes_keyword_only_config(self) -> None:
        sig = inspect.signature(HomeIsolation.setup)
        params = sig.parameters
        assert "config" in params
        assert params["config"].kind is inspect.Parameter.KEYWORD_ONLY
        assert params["config"].default is inspect.Parameter.empty

    def test_env_signature_is_zero_arg_returning_dict(self) -> None:
        sig = inspect.signature(HomeIsolation.env)
        # Only ``self`` — no positional arguments.
        params = [p for p in sig.parameters.values() if p.name != "self"]
        assert params == []

    def test_teardown_signature_takes_keep_flag(self) -> None:
        sig = inspect.signature(HomeIsolation.teardown)
        assert "keep" in sig.parameters

    def test_state_path_signature_takes_suffix(self) -> None:
        sig = inspect.signature(HomeIsolation.state_path)
        assert "suffix" in sig.parameters

    def test_all_four_methods_are_callable_on_instance(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        iso = _build(scratch_root)
        # ``setup`` returns a Path; the next three are reachable post-setup.
        home = iso.setup(config=permissive_config)
        try:
            assert callable(iso.env)
            assert callable(iso.state_path)
            assert callable(iso.teardown)
            assert isinstance(home, Path)
        finally:
            iso.teardown(keep=False)


# ---------------------------------------------------------------------------
# AC2 — state_path is anchored under home_path AND home_root
# ---------------------------------------------------------------------------


class TestStatePathIsAnchoredUnderHomeRoot:
    """``state_path`` results live exclusively under the per-eval HOME, which
    itself lives under the declared scratch root."""

    def test_state_path_is_relative_to_home_root(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        iso = _build(scratch_root)
        iso.setup(config=permissive_config)
        try:
            child = iso.state_path(".eval-meta/marker")
            # Per T02.11 AC: verified by is_relative_to(home_root)
            assert child.is_relative_to(scratch_root)
        finally:
            iso.teardown(keep=False)

    def test_state_path_is_also_relative_to_home_path(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        iso = _build(scratch_root)
        iso.setup(config=permissive_config)
        try:
            child = iso.state_path("artifacts/log.txt")
            assert child.is_relative_to(iso.home_path)
        finally:
            iso.teardown(keep=False)

    def test_nested_suffix_components_are_preserved(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        iso = _build(scratch_root)
        iso.setup(config=permissive_config)
        try:
            child = iso.state_path("a/b/c/d.txt")
            assert child.is_relative_to(scratch_root)
            assert child.name == "d.txt"
            assert child.parent.name == "c"
        finally:
            iso.teardown(keep=False)

    def test_state_path_rejects_absolute_suffix(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        iso = _build(scratch_root)
        iso.setup(config=permissive_config)
        try:
            with pytest.raises(ValueError, match="must be relative"):
                iso.state_path("/etc/passwd")
        finally:
            iso.teardown(keep=False)

    def test_state_path_rejects_dotdot_components(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        iso = _build(scratch_root)
        iso.setup(config=permissive_config)
        try:
            with pytest.raises(ValueError, match=r"must not contain '\.\.'"):
                iso.state_path("../escaping")
        finally:
            iso.teardown(keep=False)

    def test_state_path_before_setup_raises_runtimeerror(
        self, scratch_root: Path
    ) -> None:
        iso = _build(scratch_root)
        with pytest.raises(RuntimeError, match="setup\\(\\) must be called"):
            iso.state_path("anything")


# ---------------------------------------------------------------------------
# AC3 — teardown keep/remove semantics
# ---------------------------------------------------------------------------


class TestTeardownKeepFlag:
    """``teardown(keep=True)`` preserves the HOME; ``keep=False`` removes it.
    Both branches clear the private slot."""

    def test_teardown_keep_true_preserves_home_on_disk(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        iso = _build(scratch_root)
        home = iso.setup(config=permissive_config)
        # Write a marker so the directory has non-trivial content.
        (home / "marker.txt").write_text("preserved", encoding="utf-8")
        iso.teardown(keep=True)
        assert home.exists()
        assert (home / "marker.txt").read_text(encoding="utf-8") == "preserved"

    def test_teardown_keep_false_removes_home_from_disk(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        iso = _build(scratch_root)
        home = iso.setup(config=permissive_config)
        (home / "marker.txt").write_text("ephemeral", encoding="utf-8")
        iso.teardown(keep=False)
        assert not home.exists()

    def test_teardown_clears_slot_on_keep_true(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        iso = _build(scratch_root)
        iso.setup(config=permissive_config)
        assert iso.is_set_up
        iso.teardown(keep=True)
        assert not iso.is_set_up

    def test_teardown_clears_slot_on_keep_false(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        iso = _build(scratch_root)
        iso.setup(config=permissive_config)
        iso.teardown(keep=False)
        assert not iso.is_set_up

    def test_teardown_is_noop_when_setup_never_ran(
        self, scratch_root: Path
    ) -> None:
        iso = _build(scratch_root)
        # Must not raise; orchestrator is allowed to call teardown
        # unconditionally in a ``finally`` block.
        iso.teardown(keep=False)
        iso.teardown(keep=True)
        assert not iso.is_set_up

    def test_env_after_teardown_raises_runtimeerror(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        iso = _build(scratch_root)
        iso.setup(config=permissive_config)
        iso.teardown(keep=False)
        with pytest.raises(RuntimeError, match="setup\\(\\) must be called"):
            iso.env()

    def test_state_path_after_teardown_raises_runtimeerror(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        iso = _build(scratch_root)
        iso.setup(config=permissive_config)
        iso.teardown(keep=True)
        with pytest.raises(RuntimeError, match="setup\\(\\) must be called"):
            iso.state_path("after-teardown.txt")


# ---------------------------------------------------------------------------
# AC4 — integrated lifecycle round-trip
# ---------------------------------------------------------------------------


class TestIntegratedLifecycle:
    """End-to-end ``setup -> env -> state_path -> teardown`` round-trips."""

    def test_full_lifecycle_round_trip(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        iso = _build(
            scratch_root,
            eval_id="E1",
            session_id="sess-rt-001",
            time_offset_sec=0,
        )
        # 1. setup
        home = iso.setup(config=permissive_config)
        assert home.exists() and home.is_dir()
        assert home.parent == scratch_root
        # 2. env
        env = iso.env()
        assert env == {
            "HOME": str(home),
            "CLAUDE_SESSION_ID": "sess-rt-001",
        }
        # 3. state_path
        meta = iso.state_path(".eval-meta/started")
        meta.parent.mkdir(parents=True, exist_ok=True)
        meta.write_text("ok", encoding="utf-8")
        assert meta.read_text(encoding="utf-8") == "ok"
        assert meta.is_relative_to(home)
        # 4. teardown
        iso.teardown(keep=False)
        assert not home.exists()
        assert not iso.is_set_up

    def test_re_setup_after_teardown_returns_fresh_home(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        iso = _build(scratch_root)
        first = iso.setup(config=permissive_config)
        iso.teardown(keep=False)
        second = iso.setup(config=permissive_config)
        try:
            assert second.exists()
            assert second != first
            assert second.parent == scratch_root
        finally:
            iso.teardown(keep=False)

    def test_env_with_time_offset_includes_fake_time_offset(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        iso = _build(scratch_root, time_offset_sec=7)
        iso.setup(config=permissive_config)
        try:
            env = iso.env()
            assert env["CLAUDE_FAKE_TIME_OFFSET"] == "7"
            assert env["CLAUDE_SESSION_ID"] == "sess-001"
        finally:
            iso.teardown(keep=False)

    def test_env_without_time_offset_omits_fake_time_offset(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        iso = _build(scratch_root, time_offset_sec=0)
        iso.setup(config=permissive_config)
        try:
            assert "CLAUDE_FAKE_TIME_OFFSET" not in iso.env()
        finally:
            iso.teardown(keep=False)


# ---------------------------------------------------------------------------
# Containment guard integration — re-confirm at the COMP-006 level
# ---------------------------------------------------------------------------


class TestContainmentGuardIntegratedIntoSetup:
    """Per the D-0029 contract, ``setup`` invokes ``containment_guard``
    after ``mkdtemp``; the integrated component must still reject the
    scratch-root-not-in-allowlist case at this layer."""

    def test_setup_rejects_scratch_root_outside_allowlist(
        self, scratch_root: Path
    ) -> None:
        # Build a config whose allowlist does NOT include ``scratch_root``.
        config = EvalConfig(allowed_scratch_roots=())
        iso = _build(scratch_root)
        with pytest.raises(HomeContainmentViolation) as ei:
            iso.setup(config=config)
        assert ei.value.check == "scratch_root_allowlist"

    def test_setup_requires_explicit_config(self, scratch_root: Path) -> None:
        iso = _build(scratch_root)
        with pytest.raises(TypeError):
            iso.setup()  # type: ignore[call-arg]


# ---------------------------------------------------------------------------
# Concurrency — sibling instances under one scratch root
# ---------------------------------------------------------------------------


class TestParallelSiblings:
    """Sibling per-eval HOMEs created under one scratch root never collide
    and never share state — the integrated lifecycle is concurrency-safe
    under :class:`ThreadPoolExecutor`."""

    def test_parallel_lifecycle_round_trip(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        n = 8

        def run(idx: int) -> tuple[Path, Path]:
            iso = HomeIsolation(
                eval_id=f"E{idx}",
                home_root=scratch_root,
                session_id=f"sess-{idx:03d}",
            )
            home = iso.setup(config=permissive_config)
            try:
                marker = iso.state_path("marker.txt")
                marker.write_text(f"hello-{idx}", encoding="utf-8")
                env = iso.env()
                assert env["HOME"] == str(home)
                return home, marker
            finally:
                iso.teardown(keep=False)

        with ThreadPoolExecutor(max_workers=n) as pool:
            results = list(
                as_completed([pool.submit(run, i) for i in range(n)])
            )
        homes = [r.result()[0] for r in results]
        assert len({str(h) for h in homes}) == n  # no collisions
        # All scratched out post-teardown.
        for h in homes:
            assert not h.exists()


# ---------------------------------------------------------------------------
# DM-006 invariants survive integration
# ---------------------------------------------------------------------------


class TestDm006InvariantsSurviveIntegration:
    """The frozen-dataclass invariants from T02.04 must survive the
    full setup/env/state_path/teardown lifecycle."""

    def test_fields_are_immutable_after_setup(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        iso = _build(scratch_root)
        iso.setup(config=permissive_config)
        try:
            with pytest.raises(FrozenInstanceError):
                iso.eval_id = "mutated"  # type: ignore[misc]
            with pytest.raises(FrozenInstanceError):
                iso.home_root = scratch_root.parent  # type: ignore[misc]
            with pytest.raises(FrozenInstanceError):
                iso.session_id = "mutated"  # type: ignore[misc]
            with pytest.raises(FrozenInstanceError):
                iso.time_offset_sec = 42  # type: ignore[misc]
        finally:
            iso.teardown(keep=False)

    def test_equality_unchanged_post_setup(
        self, scratch_root: Path, permissive_config: EvalConfig
    ) -> None:
        a = _build(scratch_root, eval_id="E1", session_id="s")
        b = _build(scratch_root, eval_id="E1", session_id="s")
        assert a == b
        a.setup(config=permissive_config)
        try:
            # Lifecycle state lives on a private slot — equality across
            # the four declared DM-006 fields is unaffected.
            assert a == b
        finally:
            a.teardown(keep=False)
