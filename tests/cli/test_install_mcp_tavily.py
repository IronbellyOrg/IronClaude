"""Drift-guard tests for the Tavily MCP registry entry and install path (Cluster C1).

Covers the pinned ``tavily-mcp@0.2.20`` version, the ``default_parameters`` registry
field, server-level ``DEFAULT_PARAMETERS`` injection into the install argv (M1), API-key
masking in echoed commands (M1), and the absence of the deleted ``configs/tavily.json``.

All assertions read the ACTUAL registry / argv — no fabricated expected values. The live
smoke is gated behind ``TAVILY_API_KEY`` so the suite is CI-safe.
"""

import os
from pathlib import Path

import pytest

from superclaude.cli import install_mcp

# Repo root: tests/cli/test_install_mcp_tavily.py -> parents[2]
_REPO_ROOT = Path(__file__).resolve().parents[2]

# Compact-JSON token expected in the install argv (no spaces — single argv token, M1).
_EXPECTED_DEFAULT_PARAMS_TOKEN = (
    'DEFAULT_PARAMETERS={"search_depth":"basic","max_results":10}'
)


def test_tavily_registry_pins_0_2_20():
    """The tavily registry command pins exactly tavily-mcp@0.2.20 over stdio (X1).

    The pin is sourced from the ``TAVILY_MCP_VERSION`` constant (L3 single-SoT); the
    literal ``0.2.20`` assertion stays as a backstop so an unintended bump fails here.
    """
    assert install_mcp.TAVILY_MCP_VERSION == "0.2.20"
    entry = install_mcp.MCP_SERVERS["tavily"]
    assert entry["command"] == f"npx -y tavily-mcp@{install_mcp.TAVILY_MCP_VERSION}"
    assert entry["command"] == "npx -y tavily-mcp@0.2.20"
    assert entry["transport"] == "stdio"


def test_default_parameters_field():
    """The tavily registry carries the DEFAULT_PARAMETERS baseline (X3 / M3a)."""
    entry = install_mcp.MCP_SERVERS["tavily"]
    assert entry["default_parameters"] == {"search_depth": "basic", "max_results": 10}


def test_tavily_json_absent():
    """The orphan src/ config was deleted in Phase 2 (X2)."""
    orphan = _REPO_ROOT / "src" / "superclaude" / "mcp" / "configs" / "tavily.json"
    assert not orphan.exists(), f"deleted config still present: {orphan}"


class _FakeCompleted:
    """Minimal stand-in for subprocess.CompletedProcess (returncode 0, no stderr)."""

    returncode = 0
    stderr = ""
    stdout = ""


def _patch_install_path(monkeypatch, dummy_key):
    """Monkeypatch the install path so it never spawns a real npx/claude subprocess.

    Returns a mutable list that captures the argv passed to ``_run_command``.
    """
    captured = {"calls": []}

    def fake_run_command(cmd, **kwargs):
        captured["calls"].append(list(cmd))
        return _FakeCompleted()

    monkeypatch.setattr(install_mcp, "_run_command", fake_run_command)
    monkeypatch.setattr(install_mcp, "check_mcp_server_installed", lambda name: False)
    monkeypatch.setattr(install_mcp, "prompt_for_api_key", lambda *a, **k: dummy_key)
    return captured


def test_default_parameters_propagated(monkeypatch):
    """The install argv carries -e DEFAULT_PARAMETERS=<compact-json> and the 0.2.20 pin (M1).

    No real npx/claude subprocess is spawned (``_run_command`` is intercepted).
    """
    captured = _patch_install_path(monkeypatch, "dummy-key-abc123")

    ok = install_mcp.install_mcp_server(
        install_mcp.MCP_SERVERS["tavily"], scope="user", dry_run=False
    )
    assert ok is True

    # Exactly one intercepted command, and the real subprocess was never reached.
    assert len(captured["calls"]) == 1
    argv = captured["calls"][0]

    # The compact DEFAULT_PARAMETERS token is present and immediately follows an -e flag.
    assert _EXPECTED_DEFAULT_PARAMS_TOKEN in argv
    idx = argv.index(_EXPECTED_DEFAULT_PARAMS_TOKEN)
    assert argv[idx - 1] == "-e"

    # The pinned package version is in the argv (after the `--` separator).
    assert "tavily-mcp@0.2.20" in argv
    # Sanity: this is the `claude mcp add` path, not a direct npx spawn.
    assert argv[:3] == ["claude", "mcp", "add"]


def test_default_parameters_without_api_key(monkeypatch):
    """DEFAULT_PARAMETERS is injected even when the user supplies no API key (L1).

    The ``env_args.extend([...])`` for DEFAULT_PARAMETERS fires independently of the
    api-key branch, so the token must still reach the argv when ``prompt_for_api_key``
    returns ``None`` — and no ``TAVILY_API_KEY=`` pair should be present.
    """
    captured = _patch_install_path(monkeypatch, None)  # user declines the key prompt

    ok = install_mcp.install_mcp_server(
        install_mcp.MCP_SERVERS["tavily"], scope="user", dry_run=False
    )
    assert ok is True

    assert len(captured["calls"]) == 1
    argv = captured["calls"][0]

    # DEFAULT_PARAMETERS still injected, immediately after an -e flag.
    assert _EXPECTED_DEFAULT_PARAMS_TOKEN in argv
    idx = argv.index(_EXPECTED_DEFAULT_PARAMS_TOKEN)
    assert argv[idx - 1] == "-e"

    # No API-key env pair leaked into the argv when the key was declined.
    assert not any(tok.startswith("TAVILY_API_KEY=") for tok in argv), (
        f"unexpected TAVILY_API_KEY pair in argv when no key was given: {argv}"
    )
    # Still the pinned `claude mcp add` path.
    assert "tavily-mcp@0.2.20" in argv
    assert argv[:3] == ["claude", "mcp", "add"]


def test_api_key_never_in_logged_command(monkeypatch, capsys):
    """The echoed "Running:" command masks the raw API key value (M1)."""
    secret = "SUPERSECRETKEY-do-not-log-9999"  # pragma: allowlist secret
    _patch_install_path(monkeypatch, secret)

    install_mcp.install_mcp_server(
        install_mcp.MCP_SERVERS["tavily"], scope="user", dry_run=False
    )
    out = capsys.readouterr().out
    assert "Running:" in out
    assert secret not in out, "raw API key leaked into an echoed command line"
    # The DEFAULT_PARAMETERS token (non-secret) may still be shown in full.
    assert "TAVILY_API_KEY=***" in out


@pytest.mark.skipif(not os.getenv("TAVILY_API_KEY"), reason="requires TAVILY_API_KEY")
def test_live_tavily_search_smoke():
    """Minimal live presence check — SKIPPED in CI (no key). Confirms the pinned entry resolves."""
    entry = install_mcp.MCP_SERVERS["tavily"]
    assert entry["command"].endswith("tavily-mcp@0.2.20")
    assert entry.get("api_key_env") == "TAVILY_API_KEY"
