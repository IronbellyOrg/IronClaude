"""FR-ISO1 method-surface tests for HomeIsolation (Task T02.07 / D-0028).

This module owns the COMP-006 extension of :class:`HomeIsolation` — the
four methods (`setup`, `env`, `teardown`, `state_path`) that bolt a
per-eval HOME, ``CLAUDE_SESSION_ID`` stamp, and optional
``CLAUDE_FAKE_TIME_OFFSET`` onto the DM-006 record without disturbing
the four existing ``IsolationLayers`` guarantees (T02.05 probe).

Test invariants:

* The DM-006 frozen-dataclass surface (T02.04 contract) is preserved:
  the four declared fields stay immutable, and equality/hashing still
  work, even though :meth:`HomeIsolation.setup` writes a private slot.
* Sibling per-eval HOMEs created under the same ``home_root`` never
  collide or share filesystem state (concurrency-safe per FR-ISO1).
* ``env()`` returns ``HOME`` + ``CLAUDE_SESSION_ID`` unconditionally and
  ``CLAUDE_FAKE_TIME_OFFSET`` only when ``time_offset_sec != 0`` —
  keeping the OQ-8 gate from blocking adoption.
* ``state_path()`` refuses to escape ``home_path`` via absolute paths
  or ``..`` components (defense layered on top of T02.08).
* The upstream ``IsolationLayers`` probe (T02.05) still passes — proven
  by import-time co-residence here.

Cross-links:

* DM-006 frozen-record tests live in
  ``tests/cli/eval/test_isolation_dataclass.py`` (T02.04).
* COMP-012 probe lives in
  ``tests/cli/eval/test_isolation_layers_probe.py`` (T02.05).
* Containment guard tests land in ``test_path_containment.py`` (T02.08).
* Atomic-setup wrapper tests land in ``test_atomic_setup.py`` (T02.13).
* Hook-adapter idempotency lives in ``test_hook_adapter.py`` (T02.14).
"""

from __future__ import annotations

import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pytest

from superclaude.cli.eval import EvalConfig, HomeIsolation

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def scratch_root(tmp_path: Path) -> Path:
    """Per-test scratch root that stands in for the eval orchestrator's
    ``--scratch-root`` (FR-ISO1 / FR-ISO2)."""

    root = tmp_path / "eval-runs"
    root.mkdir()
    return root


@pytest.fixture
def permissive_config(scratch_root: Path) -> EvalConfig:
    """An :class:`EvalConfig` whose allowlist includes the test scratch
    root.

    Mirrors the orchestrator wiring (T03.16): production builds a config
    whose ``allowed_scratch_roots`` already contains the resolved
    scratch root for the run, then passes it into
    :meth:`HomeIsolation.setup`. T02.07 tests follow the same contract
    after the T02.08 hardening that made ``config`` required.
    """

    return EvalConfig(allowed_scratch_roots=(scratch_root,))


def _build(
    scratch_root: Path,
    *,
    eval_id: str = "E1",
    session_id: str = "sess-001",
    time_offset_sec: int = 0,
) -> HomeIsolation:
    """Convenience builder mirroring the orchestrator construction path."""

    return HomeIsolation(
        eval_id=eval_id,
        home_root=scratch_root,
        session_id=session_id,
        time_offset_sec=time_offset_sec,
    )


def _config_for(scratch_root: Path) -> EvalConfig:
    """Build a per-test :class:`EvalConfig` whose allowlist contains the
    given scratch root. Used by tests that build their own non-default
    scratch root (``test_setup_creates_home_root_if_missing``)."""

    return EvalConfig(allowed_scratch_roots=(scratch_root,))


# ---------------------------------------------------------------------------
# setup() — per-eval HOME materialization
# ---------------------------------------------------------------------------


def test_setup_creates_directory_under_home_root(
    scratch_root: Path, permissive_config: EvalConfig
) -> None:
    """``setup`` must materialize a real directory whose parent is the
    declared ``home_root``."""

    iso = _build(scratch_root)
    home = iso.setup(config=permissive_config)

    assert home.exists()
    assert home.is_dir()
    assert home.parent == scratch_root


def test_setup_returns_same_path_as_home_path_property(
    scratch_root: Path, permissive_config: EvalConfig
) -> None:
    """The return value of ``setup`` must equal the ``home_path``
    accessor — callers should not have to choose between two sources."""

    iso = _build(scratch_root)
    returned = iso.setup(config=permissive_config)
    assert iso.home_path == returned


def test_setup_creates_home_root_if_missing(tmp_path: Path) -> None:
    """The scratch root may not exist yet (fresh harness invocation).
    ``setup`` must create it with ``parents=True`` so the orchestrator
    does not need an extra step."""

    nested_root = tmp_path / "deep" / "scratch"
    assert not nested_root.exists()

    iso = _build(nested_root)
    home = iso.setup(config=_config_for(nested_root))

    assert nested_root.exists()
    assert home.parent == nested_root


def test_setup_is_idempotent_one_shot(
    scratch_root: Path, permissive_config: EvalConfig
) -> None:
    """Calling ``setup`` twice on the same instance must raise rather
    than silently leak a second directory."""

    iso = _build(scratch_root)
    iso.setup(config=permissive_config)
    with pytest.raises(RuntimeError, match="already called"):
        iso.setup(config=permissive_config)


def test_setup_eval_id_appears_in_directory_name(
    scratch_root: Path, permissive_config: EvalConfig
) -> None:
    """``mkdtemp(prefix=eval_id+'-')`` produces an audit-friendly name —
    ``ls`` on the scratch root immediately reveals which eval owns which
    HOME without opening any metadata files."""

    iso = _build(scratch_root, eval_id="E42")
    home = iso.setup(config=permissive_config)
    assert home.name.startswith("E42-")


# ---------------------------------------------------------------------------
# Sibling-HOME concurrency (FR-ISO1)
# ---------------------------------------------------------------------------


def test_two_setups_under_same_root_are_siblings_and_isolated(
    scratch_root: Path, permissive_config: EvalConfig
) -> None:
    """Per FR-ISO1: two HomeIsolation instances sharing one ``home_root``
    must produce sibling per-eval HOMEs and writes to one must never
    leak into the other."""

    a = _build(scratch_root, eval_id="E1", session_id="sess-a")
    b = _build(scratch_root, eval_id="E2", session_id="sess-b")

    home_a = a.setup(config=permissive_config)
    home_b = b.setup(config=permissive_config)

    assert home_a != home_b
    assert home_a.parent == home_b.parent == scratch_root

    (home_a / "marker.txt").write_text("from-a")
    assert not (home_b / "marker.txt").exists()


def test_parallel_setup_does_not_collide(
    scratch_root: Path, permissive_config: EvalConfig
) -> None:
    """Spin up several HomeIsolation instances in parallel under the
    same scratch root and assert every resulting path is unique.
    Exercises the ``mkdtemp`` atomicity guarantee end-to-end."""

    barrier = threading.Barrier(8)

    def _build_and_setup(idx: int) -> Path:
        iso = _build(scratch_root, eval_id=f"E{idx}", session_id=f"sess-{idx}")
        barrier.wait()  # maximize collision odds
        return iso.setup(config=permissive_config)

    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(_build_and_setup, i) for i in range(8)]
        homes = [f.result() for f in as_completed(futures)]

    assert len({p.resolve() for p in homes}) == 8
    for home in homes:
        assert home.exists()
        assert home.parent == scratch_root


# ---------------------------------------------------------------------------
# env() — subprocess env dict
# ---------------------------------------------------------------------------


def test_env_requires_setup_first(scratch_root: Path) -> None:
    """``env`` reads ``HOME`` off the per-eval directory, so calling it
    before ``setup`` must raise rather than fabricate a placeholder."""

    iso = _build(scratch_root)
    with pytest.raises(RuntimeError, match="setup"):
        iso.env()


def test_env_includes_home_and_session_id(
    scratch_root: Path, permissive_config: EvalConfig
) -> None:
    """``HOME`` and ``CLAUDE_SESSION_ID`` are mandatory FR-ISO1 fields."""

    iso = _build(scratch_root, session_id="sess-xyz")
    iso.setup(config=permissive_config)
    env = iso.env()

    assert env["HOME"] == str(iso.home_path)
    assert env["CLAUDE_SESSION_ID"] == "sess-xyz"


def test_env_omits_time_offset_when_zero(
    scratch_root: Path, permissive_config: EvalConfig
) -> None:
    """Default ``time_offset_sec=0`` must keep ``CLAUDE_FAKE_TIME_OFFSET``
    out of the env dict — OQ-8 gating means the variable only shows up
    when the caller explicitly asks for an offset."""

    iso = _build(scratch_root, time_offset_sec=0)
    iso.setup(config=permissive_config)
    env = iso.env()
    assert "CLAUDE_FAKE_TIME_OFFSET" not in env


@pytest.mark.parametrize("offset", [1, 60, -30, 86400])
def test_env_includes_time_offset_when_nonzero(
    scratch_root: Path, permissive_config: EvalConfig, offset: int
) -> None:
    """A non-zero ``time_offset_sec`` must be reflected as the string
    representation of the integer (env vars are str-only)."""

    iso = _build(scratch_root, time_offset_sec=offset)
    iso.setup(config=permissive_config)
    env = iso.env()
    assert env["CLAUDE_FAKE_TIME_OFFSET"] == str(offset)


def test_env_returns_a_fresh_dict_each_call(
    scratch_root: Path, permissive_config: EvalConfig
) -> None:
    """Callers ``.update()`` the returned dict — mutating one returned
    instance must not leak into the next call."""

    iso = _build(scratch_root)
    iso.setup(config=permissive_config)

    first = iso.env()
    first["MUTATED"] = "yes"
    second = iso.env()

    assert "MUTATED" not in second


def test_env_return_type_is_str_to_str(
    scratch_root: Path, permissive_config: EvalConfig
) -> None:
    """``dict[str, str]`` is the contract IsolationLayers.env_vars also
    uses; pin it here so a callsite can merge both without coercion."""

    iso = _build(scratch_root, time_offset_sec=42)
    iso.setup(config=permissive_config)
    env = iso.env()
    assert all(isinstance(k, str) and isinstance(v, str) for k, v in env.items())


# ---------------------------------------------------------------------------
# state_path() — relative joins under home_path
# ---------------------------------------------------------------------------


def test_state_path_joins_under_home(
    scratch_root: Path, permissive_config: EvalConfig
) -> None:
    """Happy path: a simple relative suffix lands directly under the
    per-eval HOME."""

    iso = _build(scratch_root)
    iso.setup(config=permissive_config)
    p = iso.state_path(".claude/hooks.json")
    assert p == iso.home_path / ".claude" / "hooks.json"
    assert p.is_relative_to(iso.home_path)


def test_state_path_requires_setup(scratch_root: Path) -> None:
    """``state_path`` cannot synthesize a path before ``setup`` has
    materialized the HOME directory."""

    iso = _build(scratch_root)
    with pytest.raises(RuntimeError, match="setup"):
        iso.state_path(".claude/hooks.json")


@pytest.mark.parametrize(
    "bad_suffix",
    ["/etc/passwd", "/abs/path", "/"],
)
def test_state_path_rejects_absolute(
    scratch_root: Path, permissive_config: EvalConfig, bad_suffix: str
) -> None:
    """Absolute-path suffixes would escape ``home_path`` immediately;
    they must raise ``ValueError`` instead of returning a footgun."""

    iso = _build(scratch_root)
    iso.setup(config=permissive_config)
    with pytest.raises(ValueError, match="absolute"):
        iso.state_path(bad_suffix)


@pytest.mark.parametrize(
    "bad_suffix",
    ["../escape", "..", "child/../../escape", ".claude/../../etc"],
)
def test_state_path_rejects_dotdot(
    scratch_root: Path, permissive_config: EvalConfig, bad_suffix: str
) -> None:
    """``..`` components could collapse out of ``home_path`` lexically —
    refuse them outright. FR-ISO2 (T02.08) layers symlink-resolution on
    top; this is the local lexical guard."""

    iso = _build(scratch_root)
    iso.setup(config=permissive_config)
    with pytest.raises(ValueError, match=".."):
        iso.state_path(bad_suffix)


def test_state_path_can_precede_file_creation(
    scratch_root: Path, permissive_config: EvalConfig
) -> None:
    """``state_path`` must not require the target file to exist —
    artifact writers call it to compute a destination before the
    write."""

    iso = _build(scratch_root)
    iso.setup(config=permissive_config)
    p = iso.state_path("artifacts/run-001/result.json")
    assert not p.exists()
    assert p.is_relative_to(iso.home_path)


# ---------------------------------------------------------------------------
# teardown(keep)
# ---------------------------------------------------------------------------


def test_teardown_removes_when_keep_false(
    scratch_root: Path, permissive_config: EvalConfig
) -> None:
    """``keep=False`` deletes the directory tree."""

    iso = _build(scratch_root)
    home = iso.setup(config=permissive_config)
    (home / "file.txt").write_text("x")

    iso.teardown(keep=False)

    assert not home.exists()


def test_teardown_preserves_when_keep_true(
    scratch_root: Path, permissive_config: EvalConfig
) -> None:
    """``keep=True`` leaves the directory on disk for inspection (the
    branch the atomic-setup wrapper T02.13 takes on failure, and the
    branch taken under ``--keep-home``)."""

    iso = _build(scratch_root)
    home = iso.setup(config=permissive_config)
    (home / "file.txt").write_text("x")

    iso.teardown(keep=True)

    assert home.exists()
    assert (home / "file.txt").exists()


def test_teardown_is_noop_when_setup_never_ran(scratch_root: Path) -> None:
    """Callers should not need to track setup state; teardown on a
    not-yet-set-up instance is a no-op."""

    iso = _build(scratch_root)
    iso.teardown(keep=False)  # must not raise


def test_teardown_clears_home_path_slot(
    scratch_root: Path, permissive_config: EvalConfig
) -> None:
    """After teardown, ``home_path`` must raise — the path is no longer
    trustworthy and consumers should re-setup explicitly."""

    iso = _build(scratch_root)
    iso.setup(config=permissive_config)
    iso.teardown(keep=False)

    with pytest.raises(RuntimeError, match="setup"):
        _ = iso.home_path


def test_teardown_after_keep_still_clears_slot(
    scratch_root: Path, permissive_config: EvalConfig
) -> None:
    """``teardown(keep=True)`` leaves the directory on disk but the
    instance still relinquishes ownership — re-running env() / state_path()
    would otherwise point at a path nobody is managing any more."""

    iso = _build(scratch_root)
    iso.setup(config=permissive_config)
    iso.teardown(keep=True)

    assert iso.is_set_up is False
    with pytest.raises(RuntimeError):
        iso.env()


def test_setup_can_run_after_teardown(
    scratch_root: Path, permissive_config: EvalConfig
) -> None:
    """Idempotency is one-shot per setup call, not per instance:
    after teardown clears the slot, a second setup must succeed and
    create a fresh sibling HOME."""

    iso = _build(scratch_root, eval_id="E7")
    first = iso.setup(config=permissive_config)
    iso.teardown(keep=False)

    second = iso.setup(config=permissive_config)
    assert second != first
    assert second.parent == scratch_root
    assert second.exists()


# ---------------------------------------------------------------------------
# DM-006 invariants preserved by the extension (T02.04 contract)
# ---------------------------------------------------------------------------


def test_dm006_fields_remain_frozen_after_setup(
    scratch_root: Path, permissive_config: EvalConfig
) -> None:
    """The four declared fields must stay immutable even after the
    private ``_home_path`` slot has been written via
    ``object.__setattr__``."""

    import dataclasses

    iso = _build(scratch_root)
    iso.setup(config=permissive_config)
    with pytest.raises(dataclasses.FrozenInstanceError):
        iso.eval_id = "E99"  # type: ignore[misc]
    with pytest.raises(dataclasses.FrozenInstanceError):
        iso.session_id = "different"  # type: ignore[misc]


def test_equality_ignores_private_setup_state(
    scratch_root: Path, permissive_config: EvalConfig
) -> None:
    """Two HomeIsolation instances with the same four DM-006 fields
    must compare equal even when only one has been ``setup`` — the
    private slot is not part of the record identity."""

    a = _build(scratch_root)
    b = _build(scratch_root)
    a.setup(config=permissive_config)
    assert a == b


def test_is_set_up_flag(scratch_root: Path, permissive_config: EvalConfig) -> None:
    """``is_set_up`` is the lightweight predicate the orchestrator uses
    instead of catching ``RuntimeError`` from ``home_path``."""

    iso = _build(scratch_root)
    assert iso.is_set_up is False
    iso.setup(config=permissive_config)
    assert iso.is_set_up is True
    iso.teardown(keep=False)
    assert iso.is_set_up is False


# ---------------------------------------------------------------------------
# IsolationLayers probe (T02.05) re-verification
# ---------------------------------------------------------------------------


def test_isolation_layers_probe_still_passes_after_extension() -> None:
    """COMP-012 probe (T02.05) must keep passing — HomeIsolation
    extension does not (and must not) touch the upstream
    ``cli/sprint/executor.IsolationLayers`` shape. Re-import the probe
    asserts here so a regression here surfaces in this module first."""

    import tests.cli.eval.test_isolation_layers_probe as probe  # type: ignore[import-untyped]

    probe.test_isolation_layers_is_dataclass()
    probe.test_isolation_layers_lives_in_sprint_executor_module()
    probe.test_isolation_layers_field_names_and_order()
    probe.test_isolation_layers_env_vars_is_property()
    probe.test_isolation_layers_env_vars_return_annotation_is_str_dict()
    probe.test_isolation_layers_layers_active_is_property()
    probe.test_isolation_layers_layers_active_return_annotation_is_list_str()
    probe.test_setup_isolation_module_path()


def test_home_isolation_env_does_not_collide_with_isolation_layers_keys(
    scratch_root: Path, permissive_config: EvalConfig
) -> None:
    """HomeIsolation.env() and IsolationLayers.env_vars are merged at
    the orchestrator; assert the key sets are disjoint so neither
    overrides the other silently."""

    from superclaude.cli.sprint.executor import IsolationLayers

    iso = _build(scratch_root, time_offset_sec=10)
    iso.setup(config=permissive_config)
    home_keys = set(iso.env().keys())

    isolation_layers_keys = {
        "CLAUDE_WORK_DIR",
        "GIT_CEILING_DIRECTORIES",
        "CLAUDE_PLUGIN_DIR",
        "CLAUDE_SETTINGS_DIR",
    }

    # Sanity: the upstream shape still produces the four expected keys.
    layers = IsolationLayers(
        scoped_work_dir=scratch_root,
        git_boundary=scratch_root,
        plugin_dir=scratch_root,
        settings_dir=scratch_root,
    )
    assert set(layers.env_vars.keys()) == isolation_layers_keys

    assert home_keys.isdisjoint(isolation_layers_keys)


# ---------------------------------------------------------------------------
# Real-world HOME safety
# ---------------------------------------------------------------------------


def test_setup_never_touches_real_home(
    scratch_root: Path,
    permissive_config: EvalConfig,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Sanity check: setup() must not write under ``os.path.expanduser('~')``.

    Full hard-guard testing lives in T02.10 (``test_hard_guard_real_home.py``);
    here we just confirm the basic path computation does not accidentally
    use ``$HOME`` as a fallback."""

    fake_home = scratch_root / "FAKE_HOME_SENTINEL"
    fake_home.mkdir()
    monkeypatch.setenv("HOME", str(fake_home))

    iso = _build(scratch_root)
    home = iso.setup(config=permissive_config)

    assert os.path.commonpath([str(home), str(fake_home)]) != str(fake_home)
    assert not any(fake_home.iterdir())


# ---------------------------------------------------------------------------
# T4a / H5a — commands.eval_run extends allowlist BEFORE home_root.mkdir
# ---------------------------------------------------------------------------


def test_eval_run_extends_allowlist_before_mkdir(
    allowlisted_output_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """T4a / H5a / OPS-002: the runtime ``EvalConfig`` extension precedes
    the ``home_root.mkdir`` filesystem write inside ``eval_run``.

    Pre-H5a the ``commands.py`` ``eval_run`` body called
    ``home_root.mkdir(...)`` BEFORE building ``runtime_config`` with the
    extended ``allowed_scratch_roots`` tuple. That violated the OPS-002
    invariant "no filesystem write before allowlist validation": a path
    crash between the mkdir and the runtime_config construction would
    leave a directory on disk that the allowlist had not validated.

    Post-H5a the ordering is reversed: ``runtime_config = EvalConfig(...)``
    is built first, then ``home_root.mkdir(...)`` runs. This test spies
    on ``EvalConfig.__init__`` and ``pathlib.Path.mkdir`` to record their
    invocation order, then asserts ``EvalConfig`` (with the extended
    allowlist) was constructed before ``home_root.mkdir`` fired.
    """
    from click.testing import CliRunner

    import superclaude.cli.eval.commands as commands_module
    from superclaude.cli.eval.commands import RUN_CLEAN_EXIT_CODE, eval_group
    from superclaude.cli.eval.suites import SCHEMA_PATH

    real_suite_path = SCHEMA_PATH.parent / "real.yaml"
    output_dir = allowlisted_output_dir / "t4a-ordering"

    event_log: list[tuple[str, object]] = []

    real_evalconfig_init = commands_module.EvalConfig.__init__

    def spy_evalconfig_init(self, *args, **kwargs):
        # Only record the runtime EvalConfig (the one with the extended
        # allowlist) — the base_config build at eval_run start uses
        # default ``allowed_scratch_roots`` and would otherwise pollute
        # the log. The runtime instance always has a longer allowlist
        # than the default (extended with output_root + run_dir + home_root).
        result = real_evalconfig_init(self, *args, **kwargs)
        if len(self.allowed_scratch_roots) > 2:
            event_log.append(("EvalConfig.__init__", tuple(self.allowed_scratch_roots)))
        return result

    monkeypatch.setattr(commands_module.EvalConfig, "__init__", spy_evalconfig_init)

    real_path_mkdir = Path.mkdir

    def spy_path_mkdir(self, *args, **kwargs):
        # Record only the ``home_root`` mkdir — its directory name is
        # the literal ``"homes"`` (see ``commands.py:home_root = resolved_run_dir / "homes"``).
        if self.name == "homes":
            event_log.append(("home_root.mkdir", str(self)))
        return real_path_mkdir(self, *args, **kwargs)

    monkeypatch.setattr(Path, "mkdir", spy_path_mkdir)

    runner = CliRunner()
    result = runner.invoke(
        eval_group,
        [
            "run",
            "--suite",
            str(real_suite_path),
            "--eval",
            "E1",
            "--no-pty",
            "--output-dir",
            str(output_dir),
            "--parallel",
            "1",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == RUN_CLEAN_EXIT_CODE, result.stdout + (
        result.stderr or ""
    )

    config_idx = next(
        (i for i, (kind, _) in enumerate(event_log) if kind == "EvalConfig.__init__"),
        None,
    )
    mkdir_idx = next(
        (i for i, (kind, _) in enumerate(event_log) if kind == "home_root.mkdir"),
        None,
    )

    assert config_idx is not None, (
        f"No EvalConfig.__init__ with extended allowlist was recorded; "
        f"event_log={event_log}"
    )
    assert mkdir_idx is not None, (
        f"No home_root.mkdir was recorded; event_log={event_log}"
    )
    assert config_idx < mkdir_idx, (
        f"H5a ordering violation: home_root.mkdir at index {mkdir_idx} "
        f"preceded EvalConfig allowlist extension at index {config_idx}. "
        f"event_log={event_log}"
    )

    # Defense-in-depth: the recorded extended allowlist contains a path
    # ending in ``homes`` — the OPS-002 contract is that home_root is in
    # the allowlist at the moment of its mkdir.
    _, allowed = event_log[config_idx]
    assert any(str(p).endswith("homes") for p in allowed), (  # type: ignore[arg-type]
        f"Extended allowlist did not contain home_root: allowed={allowed}"
    )
