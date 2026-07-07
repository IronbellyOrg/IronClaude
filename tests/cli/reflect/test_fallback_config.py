"""Config-threading tests for the Tier-2 fallback ladder (§7.2).

Proves ``resolve_config`` derives ``tier2_fallback_enabled`` correctly (stub
defaults OFF, real transport defaults ON, explicit OFF forces OFF) and that the
non-CLI ``ReflectConfig`` fields carry their design §7.2 defaults. Uses the
``temp_tasklist`` + ``patch_git`` fixtures so no real git/env is required.
"""

from __future__ import annotations

from pathlib import Path

from superclaude.cli.reflect.config import resolve_config


def _resolve(temp_tasklist: Path, **kwargs):
    return resolve_config(
        str(temp_tasklist),
        depth="deep",
        model="test-model",
        **kwargs,
    )


def test_stub_transport_defaults_fallback_off(temp_tasklist, patch_git) -> None:
    config = _resolve(temp_tasklist, transport="stub")
    assert config.tier2_fallback_enabled is False


def test_openai_compat_defaults_fallback_on(temp_tasklist, patch_git) -> None:
    config = _resolve(temp_tasklist, transport="openai_compat")
    assert config.tier2_fallback_enabled is True


def test_explicit_disable_forces_off_on_real_transport(
    temp_tasklist, patch_git
) -> None:
    config = _resolve(
        temp_tasklist, transport="openai_compat", tier2_fallback_enabled=False
    )
    assert config.tier2_fallback_enabled is False


def test_explicit_enable_still_off_for_stub(temp_tasklist, patch_git) -> None:
    # Stub certifies on its own: even an explicit enable stays OFF for stub.
    config = _resolve(temp_tasklist, transport="stub", tier2_fallback_enabled=True)
    assert config.tier2_fallback_enabled is False


def test_reflectconfig_ladder_and_max_attempt_defaults(
    temp_tasklist, patch_git
) -> None:
    config = _resolve(temp_tasklist, transport="openai_compat")
    assert config.tier2_fallback_ladder == ("T1Model01", "T1Model02")
    assert config.tier2_fallback_max_attempts == 2
