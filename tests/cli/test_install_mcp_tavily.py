"""Drift-guard tests for the Tavily MCP registry entry and install path (Cluster C1).

Covers the pinned ``tavily-mcp@0.2.22`` version, the ``default_parameters`` registry
field, server-level ``DEFAULT_PARAMETERS`` injection into the install argv (M1), API-key
masking in echoed commands (M1), and the absence of the deleted ``configs/tavily.json``.

All assertions read the ACTUAL registry / argv — no fabricated expected values. The live
smoke is gated behind ``TAVILY_API_KEY`` so the suite is CI-safe.
"""

import json
import os
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from superclaude.cli import install_mcp

# Repo root: tests/cli/test_install_mcp_tavily.py -> parents[2]
_REPO_ROOT = Path(__file__).resolve().parents[2]

# Compact-JSON token expected in the install argv (no spaces — single argv token, M1).
_EXPECTED_DEFAULT_PARAMS_TOKEN = (
    'DEFAULT_PARAMETERS={"search_depth":"basic","max_results":10}'
)


def test_tavily_registry_pins_0_2_22():
    """The tavily registry command pins exactly tavily-mcp@0.2.22 over stdio (X1).

    The pin is sourced from the ``TAVILY_MCP_VERSION`` constant (L3 single-SoT); the
    literal ``0.2.22`` assertion stays as a backstop so an unintended bump fails here.
    """
    assert install_mcp.TAVILY_MCP_VERSION == "0.2.22"
    entry = install_mcp.MCP_SERVERS["tavily"]
    assert entry["command"] == f"npx -y tavily-mcp@{install_mcp.TAVILY_MCP_VERSION}"
    assert entry["command"] == "npx -y tavily-mcp@0.2.22"
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
    """The install argv carries -e DEFAULT_PARAMETERS=<compact-json> and the 0.2.22 pin (M1).

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
    assert "tavily-mcp@0.2.22" in argv
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
    assert "tavily-mcp@0.2.22" in argv
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
    """A stale pin (0.1.2) registered while the registry wants 0.2.22 -> remove + re-add (M1 fix).

    This is the core regression: ``install_mcp_server`` must NOT name-idempotently skip an
    out-of-date server. It must remove the stale registration and re-add the pinned version.
    """
    captured = _patch_already_installed(monkeypatch, _get_output("0.1.2"))

    ok = install_mcp.install_mcp_server(
        install_mcp.MCP_SERVERS["tavily"], scope="user", dry_run=False
    )
    assert ok is True

    # A `claude mcp remove tavily` must have fired before the re-add.
    remove_calls = [
        c for c in captured["calls"] if c[:3] == ["claude", "mcp", "remove"]
    ]
    assert len(remove_calls) == 1, (
        f"expected exactly one remove, got: {captured['calls']}"
    )
    assert "tavily" in remove_calls[0]
    assert "--scope" in remove_calls[0] and "user" in remove_calls[0]

    # The re-add must register the *pinned* version, not the stale one.
    add_calls = [c for c in captured["calls"] if c[:3] == ["claude", "mcp", "add"]]
    assert len(add_calls) == 1, f"expected exactly one add, got: {captured['calls']}"
    assert "tavily-mcp@0.2.22" in add_calls[0]
    assert "tavily-mcp@0.1.2" not in add_calls[0]

    # Ordering: remove precedes add.
    assert captured["calls"].index(remove_calls[0]) < captured["calls"].index(
        add_calls[0]
    )


def test_noop_when_already_up_to_date(monkeypatch):
    """When the registered version already matches the pin, do nothing destructive (no remove/add)."""
    captured = _patch_already_installed(monkeypatch, _get_output("0.2.22"))

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
        '  Args: -y tavily-mcp@0.2.22 "unterminated\n'  # unbalanced quote
    )
    captured = _patch_already_installed(
        monkeypatch, malformed
    )  # exit 0, present-but-unparseable

    ok = install_mcp.install_mcp_server(
        install_mcp.MCP_SERVERS["tavily"], scope="user", dry_run=False
    )
    assert ok is True

    assert any(c[:3] == ["claude", "mcp", "remove"] for c in captured["calls"])
    add_calls = [c for c in captured["calls"] if c[:3] == ["claude", "mcp", "add"]]
    assert len(add_calls) == 1 and "tavily-mcp@0.2.22" in add_calls[0]


def test_parse_command_returns_none_on_malformed_quoting():
    """``_parse_mcp_get_command`` returns None (not raise) on unbalanced quoting (r3476286558)."""
    assert (
        install_mcp._parse_mcp_get_command('  Command: npx\n  Args: -y "oops\n') is None
    )


def test_substring_false_positive_installs_fresh_without_remove(monkeypatch):
    """Substring prefilter hits but no EXACT-name registration -> fresh install, no destructive remove (r3476286564).

    ``check_mcp_server_installed`` is an unscoped substring scan, so it can match a
    similarly-named server. When ``claude mcp get <name>`` finds no exact registration
    (exit != 0), the code must NOT issue a ``claude mcp remove`` (which would target the
    wrong server / scope) — it installs fresh instead.
    """
    captured = _patch_already_installed(
        monkeypatch, None, get_rc=1
    )  # exact-name lookup fails

    ok = install_mcp.install_mcp_server(
        install_mcp.MCP_SERVERS["tavily"], scope="user", dry_run=False
    )
    assert ok is True

    assert not any(c[:3] == ["claude", "mcp", "remove"] for c in captured["calls"]), (
        f"must not remove on a substring-only false positive: {captured['calls']}"
    )
    add_calls = [c for c in captured["calls"] if c[:3] == ["claude", "mcp", "add"]]
    assert len(add_calls) == 1 and "tavily-mcp@0.2.22" in add_calls[0]


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

    remove_calls = [
        c for c in captured["calls"] if c[:3] == ["claude", "mcp", "remove"]
    ]
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
        return _FakeGet(_get_output("0.2.22"))

    monkeypatch.setattr(install_mcp, "_run_command", fake_run_command)
    assert (
        install_mcp.get_registered_mcp_command("tavily") == "npx -y tavily-mcp@0.2.22"
    )


def test_parse_scope_normalizes_scope_line():
    """``_parse_mcp_get_scope`` maps the `Scope:` line to local|user|project (or None)."""
    assert (
        install_mcp._parse_mcp_get_scope("  Scope: User config (all projects)\n")
        == "user"
    )
    assert install_mcp._parse_mcp_get_scope("  Scope: Project config\n") == "project"
    assert install_mcp._parse_mcp_get_scope("  Scope: Local config\n") == "local"
    assert install_mcp._parse_mcp_get_scope("  Type: stdio\n") is None


@pytest.mark.skipif(not os.getenv("TAVILY_API_KEY"), reason="requires TAVILY_API_KEY")
def test_live_tavily_search_smoke():
    """Minimal live presence check — SKIPPED in CI (no key). Confirms the pinned entry resolves."""
    entry = install_mcp.MCP_SERVERS["tavily"]
    assert entry["command"].endswith("tavily-mcp@0.2.22")
    assert entry.get("api_key_env") == "TAVILY_API_KEY"


@pytest.fixture
def native_registration(tmp_path, monkeypatch):
    from superclaude.cli import install_codebase_memory as native

    home = tmp_path / "isolated home"
    home.mkdir()
    config_dir = tmp_path / "config with spaces"
    config_dir.mkdir()
    config = config_dir / ".claude.json"
    config.write_text(json.dumps({"mcpServers": {}}))
    exe = home / ".local/bin/codebase-memory-mcp"
    expected = {"type": "stdio", "command": str(exe), "args": []}
    state = SimpleNamespace(
        config=config,
        home=home,
        exe=exe,
        expected=expected,
        calls=[],
        fail_adds=0,
        fail_remove=False,
        remove_persists_then=None,
        timeout_add=False,
        bad_postcheck=False,
    )
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(config_dir))
    monkeypatch.setattr(native.platform, "system", lambda: "Linux")
    monkeypatch.setattr(native.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(
        native,
        "discover_executable",
        lambda: native.Discovery("canonical", exe, "codebase-memory-mcp 0.12.1"),
    )
    monkeypatch.setattr(
        native, "_run_bounded", lambda *a, **k: pytest.fail("native process/download")
    )
    acquire = native.acquire_codebase_memory

    def acquisition(**kwargs):
        state.calls.append(["acquire"])
        return acquire(**kwargs)

    monkeypatch.setattr(native, "acquire_codebase_memory", acquisition)

    def run(cmd, **kwargs):
        state.calls.append(cmd)
        assert kwargs["timeout"] <= 60
        if cmd == ["claude", "--version"]:
            return subprocess.CompletedProcess(cmd, 0, "fixture version", "")
        assert cmd[:3] in (["claude", "mcp", "add-json"], ["claude", "mcp", "remove"])
        assert cmd[-2:] == ["--scope", "user"]
        assert cmd[3] == "codebase-memory-mcp"
        root = json.loads(config.read_text())
        servers = root.setdefault("mcpServers", {})
        if cmd[2] == "remove":
            if state.fail_remove:
                return subprocess.CompletedProcess(
                    cmd, 1, "credential-sensitive output", "secret error"
                )
            servers.pop(cmd[3], None)
            if state.remove_persists_then:
                failure, state.remove_persists_then = state.remove_persists_then, None
                config.write_text(json.dumps(root))
                if failure == "timeout":
                    raise subprocess.TimeoutExpired(cmd, 60, stderr="secret error")
                return subprocess.CompletedProcess(cmd, 1, "", "secret error")
        else:
            if state.timeout_add:
                state.timeout_add = False
                raise subprocess.TimeoutExpired(
                    cmd, 60, stderr="credential-sensitive output"
                )
            if state.fail_adds:
                state.fail_adds -= 1
                return subprocess.CompletedProcess(
                    cmd, 1, "credential-sensitive output", "secret error"
                )
            assert cmd[3] not in servers
            servers[cmd[3]] = (
                {"type": "http", "url": "https://wrong.invalid"}
                if state.bad_postcheck
                else json.loads(cmd[4])
            )
        config.write_text(json.dumps(root))
        return subprocess.CompletedProcess(cmd, 0, "", "")

    monkeypatch.setattr(install_mcp, "_run_command", run)
    return state


def _native_entry(state):
    return (
        json.loads(state.config.read_text())
        .get("mcpServers", {})
        .get("codebase-memory-mcp")
    )


def _seed_native_entry(state, entry):
    root = json.loads(state.config.read_text())
    root.setdefault("mcpServers", {})["codebase-memory-mcp"] = entry
    state.config.write_text(json.dumps(root))


def test_native_missing_registration_reuses_binary_without_download(
    native_registration, capsys
):
    state = native_registration
    success, message = install_mcp.install_codebase_memory_mcp()
    assert success and _native_entry(state) == state.expected
    assert state.calls[0] == ["claude", "--version"]
    assert state.calls[1] == ["acquire"]
    assert state.calls[2][:3] == ["claude", "mcp", "add-json"]
    assert json.loads(state.calls[2][4])["command"] == str(state.exe)
    assert "0.12.1" in capsys.readouterr().out and "Restart" in message
    assert "no indexing" in message.lower() and "handshake" in message.lower()


def test_native_correct_user_entry_is_noop(native_registration):
    state = native_registration
    _seed_native_entry(state, state.expected)
    assert install_mcp.install_codebase_memory_mcp()[0]
    assert state.calls == [["claude", "--version"], ["acquire"]]


def test_native_upstream_registration_is_not_replaced(native_registration, monkeypatch):
    from superclaude.cli import install_codebase_memory as native

    state = native_registration

    def acquisition(**kwargs):
        state.calls.append(["acquire"])
        _seed_native_entry(state, state.expected)
        return native.AcquisitionResult(
            True, "verification", "fixture", state.exe, "0.12.1", True
        )

    monkeypatch.setattr(native, "acquire_codebase_memory", acquisition)
    assert install_mcp.install_codebase_memory_mcp()[0]
    assert state.calls == [["claude", "--version"], ["acquire"]]


@pytest.mark.parametrize("user_state", ["missing", "stale", "correct"])
def test_native_scope_shadowing_preserves_local_project_and_similar_names(
    native_registration, tmp_path, user_state
):
    state = native_registration
    local = {"type": "stdio", "command": "/local/tool", "args": ["local"]}
    similar = {"command": "/similar/tool"}
    root = {
        "projects": {str(tmp_path): {"mcpServers": {"codebase-memory-mcp": local}}},
        "mcpServers": {"codebase-memory-mcp-scout": similar},
        "unrelated": "keep",
    }
    if user_state != "missing":
        root["mcpServers"]["codebase-memory-mcp"] = (
            state.expected
            if user_state == "correct"
            else {"command": "/old/native", "args": []}
        )
    state.config.write_text(json.dumps(root))
    project = tmp_path / ".mcp.json"
    project.write_text(json.dumps({"mcpServers": {"codebase-memory-mcp": local}}))
    project_before = project.read_bytes()
    assert install_mcp.install_codebase_memory_mcp()[0]
    result = json.loads(state.config.read_text())
    assert result["projects"] == root["projects"]
    assert result["mcpServers"]["codebase-memory-mcp-scout"] == similar
    assert result["unrelated"] == "keep" and project.read_bytes() == project_before
    removed = [cmd for cmd in state.calls if cmd[:3] == ["claude", "mcp", "remove"]]
    assert len(removed) == int(user_state == "stale")
    assert all(cmd[-2:] == ["--scope", "user"] for cmd in removed)


@pytest.mark.parametrize(
    "drift",
    [
        {"type": "http", "url": "https://old.invalid"},
        {"type": "stdio", "command": "/old/native", "args": []},
        {"type": "stdio", "command": "codebase-memory-mcp", "args": []},
        {"args": ["--stale"]},
    ],
)
def test_native_transport_path_arguments_drift_replaced(native_registration, drift):
    state = native_registration
    old = {**state.expected, **drift}
    _seed_native_entry(state, old)
    assert install_mcp.install_codebase_memory_mcp()[0]
    assert _native_entry(state) == state.expected
    assert state.calls[2] == [
        "claude",
        "mcp",
        "remove",
        "codebase-memory-mcp",
        "--scope",
        "user",
    ]


@pytest.mark.parametrize(
    "bad",
    [
        "not-json secret",
        "[]",
        '{"mcpServers": []}',
        '{"mcpServers":{"codebase-memory-mcp":null}}',
        '{"mcpServers":{},"mcpServers":{}}',
    ],
)
def test_native_malformed_user_query_fails_closed(native_registration, bad, capsys):
    state = native_registration
    state.config.write_text(bad)
    success, message = install_mcp.install_codebase_memory_mcp()
    assert not success and "lookup" in message.lower()
    assert state.calls == [["claude", "--version"], ["acquire"]]
    assert "secret" not in message + str(capsys.readouterr())


def test_native_user_read_error_distinct_from_absence(native_registration, monkeypatch):
    state = native_registration
    original = Path.read_text

    def read(path, *args, **kwargs):
        if path == state.config:
            raise PermissionError("sensitive read failure")
        return original(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", read)
    success, message = install_mcp.install_codebase_memory_mcp()
    assert not success and "lookup" in message.lower()
    assert "sensitive" not in message and len(state.calls) == 2


def test_native_default_config_location_missing_is_confirmed_absence(
    native_registration, monkeypatch
):
    state = native_registration
    monkeypatch.delenv("CLAUDE_CONFIG_DIR")
    assert install_mcp.read_user_mcp_entry("codebase-memory-mcp") == (True, None)
    (state.home / ".claude.json").write_text(
        json.dumps({"mcpServers": {"codebase-memory-mcp": state.expected}})
    )
    assert install_mcp.read_user_mcp_entry("codebase-memory-mcp") == (
        True,
        state.expected,
    )


def test_native_dangling_config_not_absence(native_registration):
    state = native_registration
    state.config.unlink()
    state.config.symlink_to(state.config.parent / "missing")
    assert install_mcp.read_user_mcp_entry("codebase-memory-mcp") == (False, None)


@pytest.mark.parametrize("scope", ["project", "local"])
def test_native_scope_rejected_before_any_process(native_registration, scope):
    state = native_registration
    success, message = install_mcp.install_codebase_memory_mcp(scope=scope)
    assert not success and "user" in message
    assert state.calls == []


@pytest.mark.parametrize("failure", ["nonzero", "timeout", "oserror"])
def test_native_claude_readiness_precedes_acquisition(
    native_registration, monkeypatch, failure
):
    state = native_registration

    def run(cmd, **kwargs):
        assert cmd == ["claude", "--version"]
        if failure == "timeout":
            raise subprocess.TimeoutExpired(cmd, 10, stderr="secret readiness")
        if failure == "oserror":
            raise OSError("secret readiness")
        return subprocess.CompletedProcess(cmd, 1, "", "secret readiness")

    monkeypatch.setattr(install_mcp, "_run_command", run)
    success, message = install_mcp.install_codebase_memory_mcp()
    assert not success and "Claude CLI" in message and "secret" not in message
    assert state.calls == []


def test_native_acquisition_failure_prevents_registration_query(
    native_registration, monkeypatch
):
    from superclaude.cli import install_codebase_memory as native

    state = native_registration
    monkeypatch.setattr(
        native,
        "acquire_codebase_memory",
        lambda **kwargs: native.AcquisitionResult(False, "download", "fixture failed"),
    )
    monkeypatch.setattr(
        install_mcp,
        "read_user_mcp_entry",
        lambda *a: pytest.fail("dependent registration query"),
    )
    success, message = install_mcp.install_codebase_memory_mcp()
    assert not success and "download" in message and len(state.calls) == 1


@pytest.mark.parametrize("failure", ["nonzero", "timeout"])
def test_native_add_failure_restores_complete_prior_entry(
    native_registration, failure, capsys
):
    state = native_registration
    old = {
        "type": "http",
        "url": "https://old.invalid",
        "unknown": {"preserve": [1, True, "value"]},
    }
    _seed_native_entry(state, old)
    state.fail_adds = int(failure == "nonzero")
    state.timeout_add = failure == "timeout"
    success, message = install_mcp.install_codebase_memory_mcp()
    assert not success and "restored" in message.lower()
    assert _native_entry(state) == old
    assert json.loads(state.calls[-1][4]) == old
    assert "secret" not in message + str(capsys.readouterr())


def test_native_failed_restoration_distinct(native_registration, capsys):
    state = native_registration
    _seed_native_entry(state, {"command": "/old/tool", "args": ["--keep"]})
    state.fail_adds = 2
    success, message = install_mcp.install_codebase_memory_mcp()
    assert not success and "restoration failed" in message.lower()
    assert "secret" not in message + str(capsys.readouterr())


def test_native_remove_failure_stops_without_add(native_registration):
    state = native_registration
    old = {"command": "/old/native", "args": []}
    _seed_native_entry(state, old)
    state.fail_remove = True
    success, message = install_mcp.install_codebase_memory_mcp()
    assert not success and "removal" in message.lower()
    assert _native_entry(state) == old and len(state.calls) == 3


@pytest.mark.parametrize("failure", ["nonzero", "timeout"])
def test_native_remove_persisted_then_failed_restores_previous(
    native_registration, capsys, failure
):
    state = native_registration
    old = {"command": "/old/native", "args": ["--keep"]}
    _seed_native_entry(state, old)
    state.remove_persists_then = failure
    success, message = install_mcp.install_codebase_memory_mcp()
    assert not success and "intact" in message.lower()
    assert _native_entry(state) == old
    assert "secret" not in message + str(capsys.readouterr())


def test_native_post_add_verification_required(native_registration):
    state = native_registration
    state.bad_postcheck = True
    success, message = install_mcp.install_codebase_memory_mcp()
    assert not success and "verification" in message.lower()


def test_native_implicit_stdio_defaults_are_noop(native_registration):
    state = native_registration
    _seed_native_entry(state, {"command": str(state.exe), "env": {"EXTRA": "keep"}})
    assert install_mcp.install_codebase_memory_mcp()[0]
    assert state.calls == [["claude", "--version"], ["acquire"]]


@pytest.mark.parametrize(
    "secrets",
    [
        {"env": {"TOKEN": "SECRET-IN-ENTRY"}},
        {"headers": {"Authorization": "SECRET-IN-ENTRY"}},
    ],
)
def test_native_secret_bearing_entry_is_refused_before_mutation(
    native_registration, capsys, secrets
):
    state = native_registration
    old = {"command": "/old/native", **secrets}
    _seed_native_entry(state, old)
    success, message = install_mcp.install_codebase_memory_mcp()
    assert not success and "not replaced" in message
    assert _native_entry(state) == old
    assert state.calls == [["claude", "--version"], ["acquire"]]
    assert "SECRET-IN-ENTRY" not in message + str(capsys.readouterr())


def test_native_timeout_after_add_write_restores_prior_entry(
    native_registration, monkeypatch
):
    state = native_registration
    old = {"command": "/old/native", "args": ["--preserve"], "unknown": [1, 2]}
    _seed_native_entry(state, old)
    original = install_mcp._run_command
    failed = False

    def run(cmd, **kwargs):
        nonlocal failed
        result = original(cmd, **kwargs)
        if cmd[:3] == ["claude", "mcp", "add-json"] and not failed:
            failed = True
            raise subprocess.TimeoutExpired(cmd, 60)
        return result

    monkeypatch.setattr(install_mcp, "_run_command", run)
    success, message = install_mcp.install_codebase_memory_mcp()
    assert not success and "restored" in message.lower()
    assert _native_entry(state) == old
    assert [cmd[2] for cmd in state.calls if len(cmd) > 2] == [
        "remove",
        "add-json",
        "remove",
        "add-json",
    ]


def test_native_rollback_preserves_unattributed_concurrent_entry(
    native_registration, monkeypatch
):
    state = native_registration
    old = {"command": "/old/native"}
    concurrent = {"command": "/concurrently/changed", "env": {"OTHER": "keep"}}
    _seed_native_entry(state, old)
    original = install_mcp._run_command

    def run(cmd, **kwargs):
        if cmd[:3] == ["claude", "mcp", "add-json"]:
            state.calls.append(cmd)
            _seed_native_entry(state, concurrent)
            return subprocess.CompletedProcess(cmd, 1, "", "")
        return original(cmd, **kwargs)

    monkeypatch.setattr(install_mcp, "_run_command", run)
    success, message = install_mcp.install_codebase_memory_mcp()
    assert not success and "restoration failed" in message.lower()
    assert _native_entry(state) == concurrent
    assert sum(cmd[:3] == ["claude", "mcp", "remove"] for cmd in state.calls) == 1


def test_native_dry_run_never_acquires_or_mutates(native_registration):
    state = native_registration
    before = state.config.read_bytes()
    success, message = install_mcp.install_codebase_memory_mcp(dry_run=True)
    assert success and "DRY RUN" in message
    assert state.calls == [] and state.config.read_bytes() == before


@pytest.fixture
def native_removal(native_registration, monkeypatch):
    from superclaude.cli import install_codebase_memory as native

    state = native_registration
    state.removal_state = "ready"
    state.upstream_cleans_registration = True
    state.native_failure = False
    state.post_query_failure = False
    state.remaining = ()
    monkeypatch.setattr(
        native,
        "acquire_codebase_memory",
        lambda **kwargs: pytest.fail("acquisition during removal"),
    )
    monkeypatch.setattr(
        install_mcp.click,
        "confirm",
        lambda *a, **k: pytest.fail("helper must not prompt"),
    )

    def preview():
        return native.RemovalPreview(
            state.removal_state, native.REMOVAL_EFFECTS, state.exe, state.remaining
        )

    def remove(*, scope, confirmed):
        assert scope == "user" and confirmed is True
        state.calls.append(["native-uninstall"])
        if state.native_failure:
            return native.RemovalResult(
                False,
                "uninstall",
                "Possible partial removal; inspect output and retry.",
            )
        if state.upstream_cleans_registration:
            root = json.loads(state.config.read_text())
            root.get("mcpServers", {}).pop("codebase-memory-mcp", None)
            state.config.write_text(json.dumps(root))
        if state.post_query_failure:
            state.config.write_text("not-json secret-payload")
        return native.RemovalResult(
            True,
            "verification",
            "Canonical executable removed; indexes retained; updater left in place.",
            state.remaining,
        )

    monkeypatch.setattr(native, "preview_codebase_memory_removal", preview)
    monkeypatch.setattr(native, "uninstall_codebase_memory", remove)
    return state


def test_native_full_removal_upstream_registration_already_gone(native_removal):
    state = native_removal
    _seed_native_entry(state, state.expected)
    success, message = install_mcp.uninstall_codebase_memory_mcp(confirmed=True)
    assert success and _native_entry(state) is None
    assert state.calls == [["native-uninstall"]]
    assert "indexes" in message and "updater" in message


def test_native_full_removal_cleans_only_surviving_exact_user_entry(
    native_removal, tmp_path
):
    state = native_removal
    state.upstream_cleans_registration = False
    root = {
        "mcpServers": {
            "codebase-memory-mcp": state.expected,
            "codebase-memory-mcp-scout": {"command": "/keep"},
        },
        "projects": {
            str(tmp_path): {
                "mcpServers": {"codebase-memory-mcp": {"command": "/local/keep"}}
            }
        },
    }
    state.config.write_text(json.dumps(root))
    project = tmp_path / ".mcp.json"
    project.write_text(
        json.dumps(
            {"mcpServers": {"codebase-memory-mcp": {"command": "/project/keep"}}}
        )
    )
    before = project.read_bytes()
    success, message = install_mcp.uninstall_codebase_memory_mcp(confirmed=True)
    assert success
    after = json.loads(state.config.read_text())
    assert (
        after["projects"] == root["projects"]
        and "codebase-memory-mcp-scout" in after["mcpServers"]
    )
    assert project.read_bytes() == before
    assert state.calls == [
        ["native-uninstall"],
        ["claude", "mcp", "remove", "codebase-memory-mcp", "--scope", "user"],
    ]


def test_native_missing_binary_registration_only_partial_cleanup(native_removal):
    state = native_removal
    state.removal_state = "missing"
    _seed_native_entry(state, state.expected)
    success, message = install_mcp.uninstall_codebase_memory_mcp(confirmed=True)
    assert success and _native_entry(state) is None
    assert (
        "registration-only" in message.lower()
        and "companion" in message.lower()
        and "not audited" in message.lower()
    )
    assert state.calls == [
        ["claude", "mcp", "remove", "codebase-memory-mcp", "--scope", "user"]
    ]


def test_native_complete_absence_is_idempotent(native_removal):
    state = native_removal
    state.removal_state = "missing"
    success, message = install_mcp.uninstall_codebase_memory_mcp(confirmed=True)
    assert success and "absent" in message.lower() and state.calls == []


@pytest.mark.parametrize("state_name", ["external", "ambiguous", "unsupported"])
def test_native_removal_unsafe_discovery_stops_without_user_cleanup(
    native_removal, state_name
):
    state = native_removal
    state.removal_state = state_name
    _seed_native_entry(state, state.expected)
    before = state.config.read_bytes()
    success, message = install_mcp.uninstall_codebase_memory_mcp(confirmed=True)
    assert not success and state.calls == [] and state.config.read_bytes() == before


def test_native_removal_lookup_error_prevents_native_effects(native_removal, capsys):
    state = native_removal
    state.config.write_text("not-json secret-query")
    success, message = install_mcp.uninstall_codebase_memory_mcp(confirmed=True)
    assert not success and "lookup" in message.lower() and state.calls == []
    assert "secret-query" not in message + str(capsys.readouterr())


def test_native_removal_failure_never_blindly_cleans_registration(native_removal):
    state = native_removal
    state.native_failure = True
    _seed_native_entry(state, state.expected)
    before = state.config.read_bytes()
    success, message = install_mcp.uninstall_codebase_memory_mcp(confirmed=True)
    assert not success and "partial" in message.lower()
    assert state.calls == [["native-uninstall"]] and state.config.read_bytes() == before


def test_native_removal_post_query_failure_is_partial(native_removal, capsys):
    state = native_removal
    state.post_query_failure = True
    success, message = install_mcp.uninstall_codebase_memory_mcp(confirmed=True)
    assert (
        not success
        and "partial" in message.lower()
        and state.calls == [["native-uninstall"]]
    )
    assert "secret-payload" not in message + str(capsys.readouterr())


def test_native_residual_cleanup_failure_is_not_success(native_removal):
    state = native_removal
    state.upstream_cleans_registration = False
    state.fail_remove = True
    _seed_native_entry(state, state.expected)
    success, message = install_mcp.uninstall_codebase_memory_mcp(confirmed=True)
    assert (
        not success
        and "partial" in message.lower()
        and _native_entry(state) == state.expected
    )


def test_native_removal_surviving_alternates_reported(native_removal):
    state = native_removal
    state.remaining = (state.home / "another install" / "codebase-memory-mcp",)
    success, message = install_mcp.uninstall_codebase_memory_mcp(confirmed=True)
    assert success and str(state.remaining[0]) in message


@pytest.mark.parametrize("binary_state", ["ready", "missing"])
def test_native_removal_without_confirmation_never_mutates(
    native_removal, binary_state
):
    state = native_removal
    state.removal_state = binary_state
    _seed_native_entry(state, state.expected)
    before = state.config.read_bytes()
    success, message = install_mcp.uninstall_codebase_memory_mcp()
    assert not success and "confirm" in message.lower()
    assert state.calls == [] and state.config.read_bytes() == before


def test_native_removal_dry_run_previews_without_prompts_or_mutations(native_removal):
    state = native_removal
    _seed_native_entry(state, state.expected)
    before = state.config.read_bytes()
    success, message = install_mcp.uninstall_codebase_memory_mcp(dry_run=True)
    assert success and "DRY RUN" in message
    for phrase in (
        "detected clients",
        "companion",
        "active sessions",
        "indexes",
        "updater",
    ):
        assert phrase in message.lower()
    assert state.calls == [] and state.config.read_bytes() == before


@pytest.mark.parametrize("scope", ["project", "local"])
def test_native_removal_other_scope_rejected_before_effects(native_removal, scope):
    state = native_removal
    success, message = install_mcp.uninstall_codebase_memory_mcp(
        scope=scope, confirmed=True
    )
    assert not success and "user" in message and state.calls == []
