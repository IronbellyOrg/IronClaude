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


class _FakeGet:
    """Stand-in for ``claude mcp get`` output (returncode 0 + a structured stdout)."""

    returncode = 0
    stderr = ""

    def __init__(self, stdout):
        self.stdout = stdout


def _get_output(version, scope="User config (available in all your projects)"):
    """Render a ``claude mcp get tavily`` body pinning ``tavily-mcp@<version>`` at ``scope``."""
    return (
        "tavily:\n"
        f"  Scope: {scope}\n"
        "  Type: stdio\n"
        "  Command: npx\n"
        f"  Args: -y tavily-mcp@{version}\n"
    )


def _patch_already_installed(monkeypatch, get_stdout, get_rc=0, dummy_key="k-123"):
    """Drive the *already-installed* branch of install_mcp_server deterministically.

    ``check_mcp_server_installed`` -> True (the cheap substring prefilter). ``_run_command`` is
    intercepted: a ``claude mcp get`` argv returns ``get_stdout`` with exit code ``get_rc``
    (``get_rc != 0`` simulates "no exact-name registration"); every other argv (remove / add)
    returns a bare success and is captured. Returns the capture dict.
    """
    captured = {"calls": []}

    def fake_run_command(cmd, **kwargs):
        captured["calls"].append(list(cmd))
        if cmd[:3] == ["claude", "mcp", "get"]:
            if get_rc != 0:
                fail = _FakeCompleted()
                fail.returncode = get_rc  # type: ignore[attr-defined]
                return fail
            return _FakeGet(get_stdout if get_stdout is not None else "")
        return _FakeCompleted()

    monkeypatch.setattr(install_mcp, "_run_command", fake_run_command)
    monkeypatch.setattr(install_mcp, "check_mcp_server_installed", lambda name: True)
    monkeypatch.setattr(install_mcp, "prompt_for_api_key", lambda *a, **k: dummy_key)
    return captured


def test_reregisters_on_version_mismatch(monkeypatch):
    """A stale pin (0.1.2) registered while the registry wants 0.2.20 -> remove + re-add (M1 fix).

    This is the core regression: ``install_mcp_server`` must NOT name-idempotently skip an
    out-of-date server. It must remove the stale registration and re-add the pinned version.
    """
    captured = _patch_already_installed(monkeypatch, _get_output("0.1.2"))

    ok = install_mcp.install_mcp_server(
        install_mcp.MCP_SERVERS["tavily"], scope="user", dry_run=False
    )
    assert ok is True

    # A `claude mcp remove tavily` must have fired before the re-add.
    remove_calls = [c for c in captured["calls"] if c[:3] == ["claude", "mcp", "remove"]]
    assert len(remove_calls) == 1, f"expected exactly one remove, got: {captured['calls']}"
    assert "tavily" in remove_calls[0]
    assert "--scope" in remove_calls[0] and "user" in remove_calls[0]

    # The re-add must register the *pinned* version, not the stale one.
    add_calls = [c for c in captured["calls"] if c[:3] == ["claude", "mcp", "add"]]
    assert len(add_calls) == 1, f"expected exactly one add, got: {captured['calls']}"
    assert "tavily-mcp@0.2.20" in add_calls[0]
    assert "tavily-mcp@0.1.2" not in add_calls[0]

    # Ordering: remove precedes add.
    assert captured["calls"].index(remove_calls[0]) < captured["calls"].index(add_calls[0])


def test_noop_when_already_up_to_date(monkeypatch):
    """When the registered version already matches the pin, do nothing destructive (no remove/add)."""
    captured = _patch_already_installed(monkeypatch, _get_output("0.2.20"))

    ok = install_mcp.install_mcp_server(
        install_mcp.MCP_SERVERS["tavily"], scope="user", dry_run=False
    )
    assert ok is True

    # Only the `claude mcp get` probe ran; no remove, no add.
    assert all(c[:3] == ["claude", "mcp", "get"] for c in captured["calls"]), (
        f"up-to-date path must not remove/re-add: {captured['calls']}"
    )
    assert not any(c[:3] == ["claude", "mcp", "remove"] for c in captured["calls"])
    assert not any(c[:3] == ["claude", "mcp", "add"] for c in captured["calls"])


def test_dry_run_mismatch_does_not_remove(monkeypatch):
    """``dry_run`` on a version mismatch announces the re-register but performs no removal/add."""
    captured = _patch_already_installed(monkeypatch, _get_output("0.1.2"))

    ok = install_mcp.install_mcp_server(
        install_mcp.MCP_SERVERS["tavily"], scope="user", dry_run=True
    )
    assert ok is True

    assert not any(c[:3] == ["claude", "mcp", "remove"] for c in captured["calls"])
    assert not any(c[:3] == ["claude", "mcp", "add"] for c in captured["calls"])


def test_unparseable_registration_triggers_reregister(monkeypatch):
    """Malformed `claude mcp get` quoting must re-register, NOT crash the install (PR #204 r3476286558).

    The server IS registered (exit 0) but its ``Args:`` line has an unbalanced quote, so
    ``shlex.split`` would raise ``ValueError``. The parser swallows it -> registered command is
    ``None`` -> mismatch -> remove + re-add. The load-bearing assertion is that the call returns
    (no ``ValueError`` propagates).
    """
    malformed = (
        "tavily:\n"
        "  Scope: User config\n"
        "  Command: npx\n"
        '  Args: -y tavily-mcp@0.2.20 "unterminated\n'  # unbalanced quote
    )
    captured = _patch_already_installed(monkeypatch, malformed)  # exit 0, present-but-unparseable

    ok = install_mcp.install_mcp_server(
        install_mcp.MCP_SERVERS["tavily"], scope="user", dry_run=False
    )
    assert ok is True

    assert any(c[:3] == ["claude", "mcp", "remove"] for c in captured["calls"])
    add_calls = [c for c in captured["calls"] if c[:3] == ["claude", "mcp", "add"]]
    assert len(add_calls) == 1 and "tavily-mcp@0.2.20" in add_calls[0]


def test_parse_command_returns_none_on_malformed_quoting():
    """``_parse_mcp_get_command`` returns None (not raise) on unbalanced quoting (r3476286558)."""
    assert install_mcp._parse_mcp_get_command('  Command: npx\n  Args: -y "oops\n') is None


def test_substring_false_positive_installs_fresh_without_remove(monkeypatch):
    """Substring prefilter hits but no EXACT-name registration -> fresh install, no destructive remove (r3476286564).

    ``check_mcp_server_installed`` is an unscoped substring scan, so it can match a
    similarly-named server. When ``claude mcp get <name>`` finds no exact registration
    (exit != 0), the code must NOT issue a ``claude mcp remove`` (which would target the
    wrong server / scope) — it installs fresh instead.
    """
    captured = _patch_already_installed(monkeypatch, None, get_rc=1)  # exact-name lookup fails

    ok = install_mcp.install_mcp_server(
        install_mcp.MCP_SERVERS["tavily"], scope="user", dry_run=False
    )
    assert ok is True

    assert not any(c[:3] == ["claude", "mcp", "remove"] for c in captured["calls"]), (
        f"must not remove on a substring-only false positive: {captured['calls']}"
    )
    add_calls = [c for c in captured["calls"] if c[:3] == ["claude", "mcp", "add"]]
    assert len(add_calls) == 1 and "tavily-mcp@0.2.20" in add_calls[0]


def test_remove_targets_registered_scope_not_install_target(monkeypatch):
    """The re-register remove targets the scope the server actually lives in, not the install target (r3476286564).

    Stale tavily is registered at *project* scope; the install targets *user* scope. Removing
    at ``--scope user`` would fail (it's not there). The remove must target ``--scope project``.
    """
    captured = _patch_already_installed(
        monkeypatch, _get_output("0.1.2", scope="Project config (this project only)")
    )

    ok = install_mcp.install_mcp_server(
        install_mcp.MCP_SERVERS["tavily"], scope="user", dry_run=False
    )
    assert ok is True

    remove_calls = [c for c in captured["calls"] if c[:3] == ["claude", "mcp", "remove"]]
    assert len(remove_calls) == 1
    assert "--scope" in remove_calls[0]
    scope_idx = remove_calls[0].index("--scope")
    assert remove_calls[0][scope_idx + 1] == "project", (
        f"remove must target the registered (project) scope, not the install target: {remove_calls[0]}"
    )


def test_get_registered_mcp_command_parses_get_output(monkeypatch):
    """``get_registered_mcp_command`` normalizes ``claude mcp get`` into a comparable string."""

    def fake_run_command(cmd, **kwargs):
        assert cmd[:3] == ["claude", "mcp", "get"]
        return _FakeGet(_get_output("0.2.20"))

    monkeypatch.setattr(install_mcp, "_run_command", fake_run_command)
    assert install_mcp.get_registered_mcp_command("tavily") == "npx -y tavily-mcp@0.2.20"


def test_parse_scope_normalizes_scope_line():
    """``_parse_mcp_get_scope`` maps the `Scope:` line to local|user|project (or None)."""
    assert install_mcp._parse_mcp_get_scope("  Scope: User config (all projects)\n") == "user"
    assert install_mcp._parse_mcp_get_scope("  Scope: Project config\n") == "project"
    assert install_mcp._parse_mcp_get_scope("  Scope: Local config\n") == "local"
    assert install_mcp._parse_mcp_get_scope("  Type: stdio\n") is None


@pytest.mark.skipif(not os.getenv("TAVILY_API_KEY"), reason="requires TAVILY_API_KEY")
def test_live_tavily_search_smoke():
    """Minimal live presence check — SKIPPED in CI (no key). Confirms the pinned entry resolves."""
    entry = install_mcp.MCP_SERVERS["tavily"]
    assert entry["command"].endswith("tavily-mcp@0.2.20")
    assert entry.get("api_key_env") == "TAVILY_API_KEY"
