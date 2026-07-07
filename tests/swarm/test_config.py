"""T01.09 -- SwarmConfig dataclass + path resolution tests.

Covers AC-017 (T2 proxy env-var contract), COMP-003 (immutable
configuration dataclass), and the path-resolution helpers. The
"missing-env" path verifies INV-007's contract: config construction
itself is total -- absences are recorded, not raised -- and the
dispatch surface can interrogate :meth:`SwarmConfig.missing_t2_env_vars`
to emit a structured error.
"""

from __future__ import annotations

import dataclasses
from pathlib import Path

import pytest

from superclaude.cli.swarm.config import (
    DEFAULT_OUTPUT_DIR,
    T1_MODEL_ENV_PREFIX,
    T1_MODEL_MAX_SLOTS,
    T2_MODEL_ENV_PREFIX,
    T2_MODEL_MAX_SLOTS,
    T2_PROXY_KEY_ENV,
    T2_PROXY_URL_ENV,
    SwarmConfig,
)

# ---------------------------------------------------------------------------
# Frozen / immutability semantics (COMP-003)
# ---------------------------------------------------------------------------


def test_swarm_config_is_frozen_dataclass(tmp_path: Path) -> None:
    """SwarmConfig must be a frozen dataclass per COMP-003."""
    cfg = SwarmConfig(work_dir=tmp_path, output_dir=tmp_path / "out")
    assert dataclasses.is_dataclass(cfg)
    params = cfg.__dataclass_params__
    assert params.frozen is True, "SwarmConfig must be @dataclass(frozen=True)"


def test_mutating_frozen_field_raises(tmp_path: Path) -> None:
    """Attempting to mutate any field raises FrozenInstanceError."""
    cfg = SwarmConfig(work_dir=tmp_path, output_dir=tmp_path / "out")
    with pytest.raises(dataclasses.FrozenInstanceError):
        cfg.work_dir = tmp_path / "other"  # type: ignore[misc]
    with pytest.raises(dataclasses.FrozenInstanceError):
        cfg.dry_run = True  # type: ignore[misc]
    with pytest.raises(dataclasses.FrozenInstanceError):
        cfg.t2_models = ("m1",)  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Happy path: from_env resolves output dir, env vars, defaults
# ---------------------------------------------------------------------------


def test_from_env_happy_path_resolves_all_fields(tmp_path: Path) -> None:
    """All three resolution responsibilities discharged in one call."""
    env = {
        T2_PROXY_URL_ENV: "https://proxy.example/v1",
        T2_PROXY_KEY_ENV: "secret-abc",
        f"{T2_MODEL_ENV_PREFIX}1": "vendor/model-a",
        f"{T2_MODEL_ENV_PREFIX}2": "vendor/model-b",
        f"{T2_MODEL_ENV_PREFIX}3": "vendor/model-c",
    }
    cfg = SwarmConfig.from_env(
        work_dir=tmp_path,
        output_dir=Path("artifacts/run-1"),
        env=env,
    )
    assert cfg.work_dir == tmp_path.resolve()
    assert cfg.output_dir == (tmp_path / "artifacts/run-1").resolve()
    assert cfg.t2_proxy_url == "https://proxy.example/v1"
    assert cfg.t2_proxy_key == "secret-abc"
    assert cfg.t2_models == ("vendor/model-a", "vendor/model-b", "vendor/model-c")
    # Operational defaults
    assert cfg.dry_run is False
    assert cfg.debug is False
    assert cfg.log_level == "INFO"
    assert cfg.missing_t2_env_vars() == ()


def test_from_env_uses_default_output_dir_when_none(tmp_path: Path) -> None:
    """``output_dir=None`` falls back to DEFAULT_OUTPUT_DIR under work_dir."""
    cfg = SwarmConfig.from_env(work_dir=tmp_path, env={})
    assert cfg.output_dir == (tmp_path / DEFAULT_OUTPUT_DIR).resolve()


def test_from_env_accepts_absolute_output_dir(tmp_path: Path) -> None:
    """Absolute output paths are not re-rooted under work_dir."""
    work = tmp_path / "work"
    work.mkdir()
    elsewhere = tmp_path / "elsewhere" / "out"
    cfg = SwarmConfig.from_env(work_dir=work, output_dir=elsewhere, env={})
    assert cfg.output_dir == elsewhere
    assert not cfg.output_dir.is_relative_to(work)


def test_from_env_skips_empty_t2_model_slots(tmp_path: Path) -> None:
    """Empty / missing T2Model0N slots are skipped; the tuple stays dense."""
    env = {
        f"{T2_MODEL_ENV_PREFIX}1": "first",
        f"{T2_MODEL_ENV_PREFIX}2": "",  # empty -> skip
        f"{T2_MODEL_ENV_PREFIX}3": "third",
    }
    cfg = SwarmConfig.from_env(work_dir=tmp_path, env=env)
    assert cfg.t2_models == ("first", "third")


def test_from_env_respects_max_slot_ceiling(tmp_path: Path) -> None:
    """Only T2Model01..T2Model0{MAX} are probed; higher indices ignored."""
    env = {
        f"{T2_MODEL_ENV_PREFIX}{i}": f"model-{i}"
        for i in range(1, T2_MODEL_MAX_SLOTS + 2)  # one past the ceiling
    }
    cfg = SwarmConfig.from_env(work_dir=tmp_path, env=env)
    assert len(cfg.t2_models) == T2_MODEL_MAX_SLOTS
    assert f"model-{T2_MODEL_MAX_SLOTS + 1}" not in cfg.t2_models


# ---------------------------------------------------------------------------
# T1 fallback pool (§7.1) -- mirrors the T2 assertions above
# ---------------------------------------------------------------------------


def test_from_env_happy_path_resolves_t1_models(tmp_path: Path) -> None:
    """T1Model0N slots resolve into a dense t1_models tuple in slot order."""
    env = {
        f"{T1_MODEL_ENV_PREFIX}1": "vendor/m-a",
        f"{T1_MODEL_ENV_PREFIX}2": "m-b",
    }
    cfg = SwarmConfig.from_env(work_dir=tmp_path, env=env)
    assert cfg.t1_models == ("vendor/m-a", "m-b")


def test_from_env_t1_models_empty_default_when_absent(tmp_path: Path) -> None:
    """Absent T1 env yields the empty-tuple default (from_env stays total)."""
    cfg = SwarmConfig.from_env(work_dir=tmp_path, env={})
    assert cfg.t1_models == ()


def test_from_env_skips_empty_t1_model_slots(tmp_path: Path) -> None:
    """Empty / missing T1Model0N slots are skipped; the tuple stays dense."""
    env = {
        f"{T1_MODEL_ENV_PREFIX}1": "first",
        f"{T1_MODEL_ENV_PREFIX}2": "",  # empty -> skip
        f"{T1_MODEL_ENV_PREFIX}3": "third",
    }
    cfg = SwarmConfig.from_env(work_dir=tmp_path, env=env)
    assert cfg.t1_models == ("first", "third")


def test_from_env_respects_t1_max_slot_ceiling(tmp_path: Path) -> None:
    """Only T1Model01..T1Model0{MAX} are probed; higher indices ignored."""
    env = {
        f"{T1_MODEL_ENV_PREFIX}{i}": f"t1-{i}"
        for i in range(1, T1_MODEL_MAX_SLOTS + 2)  # one past the ceiling
    }
    cfg = SwarmConfig.from_env(work_dir=tmp_path, env=env)
    assert len(cfg.t1_models) == T1_MODEL_MAX_SLOTS
    assert f"t1-{T1_MODEL_MAX_SLOTS + 1}" not in cfg.t1_models


def test_from_env_t1_and_t2_pools_are_independent(tmp_path: Path) -> None:
    """T1 and T2 slot families resolve into separate tuples, no cross-talk."""
    env = {
        f"{T2_MODEL_ENV_PREFIX}1": "t2-a",
        f"{T1_MODEL_ENV_PREFIX}1": "t1-a",
        f"{T1_MODEL_ENV_PREFIX}2": "t1-b",
    }
    cfg = SwarmConfig.from_env(work_dir=tmp_path, env=env)
    assert cfg.t2_models == ("t2-a",)
    assert cfg.t1_models == ("t1-a", "t1-b")


# ---------------------------------------------------------------------------
# Missing-env paths (INV-007 surface)
# ---------------------------------------------------------------------------


def test_from_env_missing_all_t2_vars_does_not_raise(tmp_path: Path) -> None:
    """Construction is total even when the entire T2 contract is absent."""
    cfg = SwarmConfig.from_env(work_dir=tmp_path, env={})
    assert cfg.t2_proxy_url is None
    assert cfg.t2_proxy_key is None
    assert cfg.t2_models == ()


def test_missing_t2_env_vars_reports_all_absent(tmp_path: Path) -> None:
    """When nothing is set, every contract slot surfaces in the report."""
    cfg = SwarmConfig.from_env(work_dir=tmp_path, env={})
    missing = cfg.missing_t2_env_vars()
    assert T2_PROXY_URL_ENV in missing
    assert T2_PROXY_KEY_ENV in missing
    assert any(name.startswith(T2_MODEL_ENV_PREFIX) for name in missing)


def test_missing_t2_env_vars_reports_only_partial_absence(tmp_path: Path) -> None:
    """Partial env -- only the absent slots are reported."""
    env = {
        T2_PROXY_URL_ENV: "https://proxy.example",
        f"{T2_MODEL_ENV_PREFIX}1": "m1",
    }
    cfg = SwarmConfig.from_env(work_dir=tmp_path, env=env)
    missing = cfg.missing_t2_env_vars()
    assert T2_PROXY_URL_ENV not in missing
    assert T2_PROXY_KEY_ENV in missing
    assert not any(name.startswith(T2_MODEL_ENV_PREFIX) for name in missing)


def test_from_env_empty_string_env_treated_as_missing(tmp_path: Path) -> None:
    """Empty-string env values are normalized to None (INV-007 friendliness)."""
    env = {T2_PROXY_URL_ENV: "", T2_PROXY_KEY_ENV: ""}
    cfg = SwarmConfig.from_env(work_dir=tmp_path, env=env)
    assert cfg.t2_proxy_url is None
    assert cfg.t2_proxy_key is None


# ---------------------------------------------------------------------------
# Path resolution helper
# ---------------------------------------------------------------------------


def test_resolve_path_returns_absolute_for_relative_input(tmp_path: Path) -> None:
    cfg = SwarmConfig(work_dir=tmp_path, output_dir=tmp_path / "out")
    resolved = cfg.resolve_path("artifacts/manifest.json")
    assert resolved == (tmp_path / "artifacts/manifest.json").resolve()
    assert resolved.is_absolute()


def test_resolve_path_passes_through_absolute_input(tmp_path: Path) -> None:
    cfg = SwarmConfig(work_dir=tmp_path, output_dir=tmp_path / "out")
    absolute = tmp_path / "somewhere" / "file.json"
    assert cfg.resolve_path(absolute) == absolute


def test_resolve_path_accepts_string_argument(tmp_path: Path) -> None:
    cfg = SwarmConfig(work_dir=tmp_path, output_dir=tmp_path / "out")
    resolved = cfg.resolve_path("nested/file.txt")
    assert isinstance(resolved, Path)
    assert resolved == (tmp_path / "nested/file.txt").resolve()


# ---------------------------------------------------------------------------
# os.environ fallback (default path when env=None)
# ---------------------------------------------------------------------------


def test_from_env_falls_back_to_process_environ(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """When ``env=None``, values come from ``os.environ``."""
    monkeypatch.setenv(T2_PROXY_URL_ENV, "https://env-fallback.example")
    monkeypatch.setenv(T2_PROXY_KEY_ENV, "env-key")
    monkeypatch.setenv(f"{T2_MODEL_ENV_PREFIX}1", "env-model")
    # Drop other T2Model slots so the test stays deterministic regardless
    # of any host-provided values.
    for index in range(2, T2_MODEL_MAX_SLOTS + 1):
        monkeypatch.delenv(f"{T2_MODEL_ENV_PREFIX}{index}", raising=False)

    cfg = SwarmConfig.from_env(work_dir=tmp_path)
    assert cfg.t2_proxy_url == "https://env-fallback.example"
    assert cfg.t2_proxy_key == "env-key"
    assert cfg.t2_models == ("env-model",)


def test_from_env_defaults_work_dir_to_cwd(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """``work_dir=None`` resolves to the current working directory."""
    monkeypatch.chdir(tmp_path)
    cfg = SwarmConfig.from_env(env={})
    assert cfg.work_dir == tmp_path.resolve()
