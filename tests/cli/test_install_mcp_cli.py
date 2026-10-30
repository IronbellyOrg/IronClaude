"""Generic ``superclaude mcp`` command tests; no external process is ever run."""

import subprocess

import pytest


@pytest.fixture(autouse=True)
def isolated_home(tmp_path, monkeypatch):
    home = tmp_path / "test home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("PATH", "")
    return home


@pytest.fixture
def mcp_cli(monkeypatch, isolated_home):
    from types import SimpleNamespace

    from click.testing import CliRunner

    from superclaude.cli import install_mcp
    from superclaude.cli.main import main

    config = isolated_home / "cli config"
    config.mkdir()
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(config))
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    monkeypatch.delenv("MORPH_API_KEY", raising=False)
    state = SimpleNamespace(
        runner=CliRunner(),
        main=main,
        module=install_mcp,
        interactive=False,
        calls=[],
        processes=[],
        gateway_ok=True,
        claude_ok=True,
        docker_ok=True,
        node_version="v20.0.0",
        auggie_version="auggie 0.36.0",
        missing_tools=set(),
        real_gateway=install_mcp.install_airis_gateway,
    )
    monkeypatch.setattr(
        install_mcp, "_is_interactive", lambda: state.interactive, raising=False
    )
    monkeypatch.setattr(
        install_mcp.shutil,
        "which",
        lambda name: None if name in state.missing_tools else f"/fixture/{name}",
    )
    monkeypatch.setattr(install_mcp, "check_mcp_server_installed", lambda name: False)

    def command(argv, **kwargs):
        state.processes.append(argv)
        if argv == ["claude", "--version"]:
            return subprocess.CompletedProcess(
                argv, 0 if state.claude_ok else 1, "fixture", ""
            )
        if argv == ["node", "--version"]:
            return subprocess.CompletedProcess(
                argv, 0 if state.node_version else 1, state.node_version or "", ""
            )
        if argv == ["docker", "info"]:
            return subprocess.CompletedProcess(
                argv, 0 if state.docker_ok else 1, "", ""
            )
        if argv == ["auggie", "--version"]:
            return subprocess.CompletedProcess(argv, 0, state.auggie_version, "")
        if argv == ["uv", "--version"]:
            return subprocess.CompletedProcess(argv, 0, "uv fixture", "")
        if len(argv) == 2 and argv[0] in {"npx", "npm"} and argv[1] == "--version":
            return subprocess.CompletedProcess(
                argv, 1 if argv[0] in state.missing_tools else 0, "fixture version", ""
            )
        if argv[:3] == ["claude", "mcp", "add"]:
            return subprocess.CompletedProcess(argv, 0, "", "")
        if argv[:3] == ["claude", "mcp", "get"]:
            return subprocess.CompletedProcess(
                argv,
                0,
                "tavily:\n  Scope: User config\n  Command: npx\n  Args: -y tavily-mcp@0.1.2\n",
                "",
            )
        pytest.fail(f"Unexpected external command: {argv}")

    def gateway(dry_run=False):
        state.calls.append(("gateway", dry_run))
        return state.gateway_ok

    monkeypatch.setattr(install_mcp, "_run_command", command)
    monkeypatch.setattr(install_mcp, "install_airis_gateway", gateway)
    return state


def test_mcp_list_shows_every_registry_server(mcp_cli):
    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp", "--list"])
    assert result.exit_code == 0, result.output
    for name in mcp_cli.module.MCP_SERVERS:
        assert name in result.output
    assert "airis-mcp-gateway" in result.output
    assert mcp_cli.calls == [] and not any(
        cmd[:3] == ["claude", "mcp", "add"] for cmd in mcp_cli.processes
    )


def test_mcp_noninteractive_requires_selection_without_prompt(mcp_cli, monkeypatch):
    monkeypatch.setattr(
        mcp_cli.module.click, "prompt", lambda *a, **k: pytest.fail("non-TTY menu")
    )
    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp"])
    assert result.exit_code != 0 and "select" in result.output.lower()
    assert mcp_cli.calls == [] and mcp_cli.processes == []


def test_mcp_no_selection_dry_run_prints_choices(mcp_cli, monkeypatch):
    monkeypatch.setattr(
        mcp_cli.module.click, "prompt", lambda *a, **k: pytest.fail("dry-run prompt")
    )
    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp", "--dry-run"])
    assert result.exit_code == 0
    for text in (
        "1. Install MCP servers (default)",
        "2. Cancel",
        "airis-mcp-gateway",
        *mcp_cli.module.MCP_SERVERS,
    ):
        assert text in result.output
    assert "Uninstall" not in result.output
    assert mcp_cli.calls == [] and mcp_cli.processes == []


def test_mcp_menu_defaults_install_then_gateway(mcp_cli):
    mcp_cli.interactive = True
    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp"], input="\n\n")
    assert result.exit_code == 0, result.output
    assert "Install MCP servers" in result.output and "Cancel" in result.output
    assert "Uninstall" not in result.output
    assert mcp_cli.calls == [("gateway", False)]


def test_mcp_menu_cancel_has_no_effects(mcp_cli):
    mcp_cli.interactive = True
    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp"], input="2\n")
    assert result.exit_code == 0 and "cancel" in result.output.lower()
    assert mcp_cli.calls == [] and mcp_cli.processes == []


def test_mcp_menu_install_all_installs_the_individual_servers(mcp_cli, monkeypatch):
    mcp_cli.interactive = True
    monkeypatch.setattr(mcp_cli.module, "prompt_for_api_key", lambda *a, **k: None)
    codegraph_calls = []
    monkeypatch.setattr(
        mcp_cli.module,
        "install_codegraph_mcp",
        lambda **kwargs: codegraph_calls.append(kwargs) or (True, "codegraph fixture"),
    )
    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp"], input="1\n0\n")
    assert result.exit_code == 0, result.output
    assert any("tavily-mcp@0.2.22" in cmd for cmd in mcp_cli.processes)
    assert codegraph_calls == [{"scope": "user", "dry_run": False}]
    assert ("gateway", False) not in mcp_cli.calls


@pytest.mark.parametrize(
    "extra",
    [
        ["--dry-run"],
        ["--servers", "context7"],
        ["--scope", "project"],
    ],
)
def test_mcp_list_rejects_incompatible_modes_before_lookup(mcp_cli, monkeypatch, extra):
    monkeypatch.setattr(
        mcp_cli.module,
        "list_available_servers",
        lambda: pytest.fail("list lookup before option validation"),
    )
    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp", "--list", *extra])
    assert result.exit_code != 0 and mcp_cli.calls == [] and mcp_cli.processes == []


def test_mcp_unknown_mixed_selection_rejected_before_any_prerequisites(mcp_cli):
    result = mcp_cli.runner.invoke(
        mcp_cli.main, ["mcp", "-s", "context7", "-s", "unknown"]
    )
    assert result.exit_code != 0 and "unknown" in result.output
    assert mcp_cli.calls == [] and mcp_cli.processes == []


@pytest.mark.parametrize(
    "selection,version,minimum",
    [("context7", "v17.0.0", "18"), ("auggie", "v19.0.0", "20")],
)
def test_mcp_selected_npm_node_minimum_before_any_install(
    mcp_cli, selection, version, minimum
):
    mcp_cli.node_version = version
    result = mcp_cli.runner.invoke(
        mcp_cli.main, ["mcp", "-s", "airis-mcp-gateway", "-s", selection]
    )
    assert result.exit_code != 0 and minimum in result.output
    assert mcp_cli.calls == []


@pytest.mark.parametrize("server", ["tavily", "auggie"])
def test_mcp_dry_run_api_key_and_binary_paths_never_prompt_or_mutate(
    mcp_cli, monkeypatch, server
):
    monkeypatch.setattr(
        mcp_cli.module.click,
        "confirm",
        lambda *a, **k: pytest.fail("dry-run confirmation"),
    )
    monkeypatch.setattr(
        mcp_cli.module.click,
        "prompt",
        lambda *a, **k: pytest.fail("dry-run key prompt"),
    )
    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp", "-s", server, "--dry-run"])
    assert result.exit_code == 0, result.output
    assert not any(
        cmd[:3] in (["claude", "mcp", "add"], ["claude", "mcp", "remove"])
        or cmd[0] in {"npm", "curl"}
        for cmd in mcp_cli.processes
    )


def test_mcp_dry_run_stale_registration_does_not_remove(mcp_cli, monkeypatch):
    monkeypatch.setattr(mcp_cli.module, "check_mcp_server_installed", lambda name: True)
    monkeypatch.setattr(
        mcp_cli.module.click,
        "confirm",
        lambda *a, **k: pytest.fail("dry-run confirmation"),
    )
    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp", "-s", "tavily", "--dry-run"])
    assert result.exit_code == 0 and "re-register" in result.output
    assert mcp_cli.processes == [["claude", "mcp", "get", "tavily"]]


def test_mcp_gateway_dry_run_needs_no_docker_and_writes_nothing(
    mcp_cli, monkeypatch, isolated_home
):
    mcp_cli.docker_ok = False
    monkeypatch.setattr(mcp_cli.module, "install_airis_gateway", mcp_cli.real_gateway)
    result = mcp_cli.runner.invoke(
        mcp_cli.main, ["mcp", "-s", "airis-mcp-gateway", "--dry-run"]
    )
    assert result.exit_code == 0, result.output
    assert mcp_cli.processes == [] and not (isolated_home / ".superclaude").exists()


@pytest.mark.parametrize("server,tool", [("context7", "npx"), ("auggie", "npm")])
def test_mcp_missing_selected_package_tool_prevents_all_effects(mcp_cli, server, tool):
    mcp_cli.missing_tools = {tool}
    mcp_cli.auggie_version = "auggie 0.35.0"
    result = mcp_cli.runner.invoke(
        mcp_cli.main, ["mcp", "-s", "airis-mcp-gateway", "-s", server]
    )
    assert result.exit_code != 0 and tool in result.output
    assert mcp_cli.calls == []


@pytest.mark.parametrize("scope", ["project", "local"])
def test_mcp_other_servers_retain_requested_scope(mcp_cli, monkeypatch, scope):
    monkeypatch.setattr(mcp_cli.module, "prompt_for_api_key", lambda *a, **k: None)
    result = mcp_cli.runner.invoke(
        mcp_cli.main, ["mcp", "-s", "tavily", "--scope", scope]
    )
    assert result.exit_code == 0, result.output
    add = next(cmd for cmd in mcp_cli.processes if cmd[:3] == ["claude", "mcp", "add"])
    if scope == "project":
        assert add[add.index("--scope") + 1] == "project"
    else:
        assert "--scope" not in add  # Legacy local default remains unchanged.


def test_mcp_invalid_menu_number_does_not_install_partial_valid_selection(mcp_cli):
    mcp_cli.interactive = True
    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp"], input="1\n1,999\n")
    assert result.exit_code != 0 and "Invalid selection" in result.output
    assert mcp_cli.calls == [] and mcp_cli.processes == []


@pytest.mark.parametrize("missing", ["claude", "docker"])
def test_mcp_readiness_failure_prevents_all_mixed_install_effects(mcp_cli, missing):
    mcp_cli.claude_ok = missing != "claude"
    mcp_cli.docker_ok = missing != "docker"
    result = mcp_cli.runner.invoke(
        mcp_cli.main, ["mcp", "-s", "context7", "-s", "airis-mcp-gateway"]
    )
    assert result.exit_code != 0 and mcp_cli.calls == []


@pytest.mark.parametrize("dry_run", [False, True])
def test_mcp_gateway_curl_preflight_before_any_selected_effects(
    mcp_cli, isolated_home, monkeypatch, dry_run
):
    mcp_cli.missing_tools = {"curl"}
    monkeypatch.setattr(mcp_cli.module, "install_airis_gateway", mcp_cli.real_gateway)
    original = mcp_cli.module._run_command

    def command(argv, **kwargs):
        if argv[0] == "curl":
            mcp_cli.processes.append(argv)
            return subprocess.CompletedProcess(argv, 127, "", "curl not found")
        return original(argv, **kwargs)

    monkeypatch.setattr(mcp_cli.module, "_run_command", command)
    before = sorted(
        str(path.relative_to(isolated_home)) for path in isolated_home.rglob("*")
    )
    args = ["mcp", "--servers", "airis-mcp-gateway"]
    if dry_run:
        args.append("--dry-run")
    result = mcp_cli.runner.invoke(mcp_cli.main, args)
    assert result.exit_code == (0 if dry_run else 1), result.output
    if not dry_run:
        assert "curl" in result.output and mcp_cli.calls == []
    else:
        assert "DRY RUN" in result.output
    assert not any(
        cmd[0] == "curl"
        or cmd[:3]
        in (
            ["claude", "mcp", "add"],
            ["claude", "mcp", "add-json"],
            ["claude", "mcp", "remove"],
        )
        for cmd in mcp_cli.processes
    )
    assert not (isolated_home / ".superclaude").exists()
    assert (
        sorted(
            str(path.relative_to(isolated_home)) for path in isolated_home.rglob("*")
        )
        == before
    )
