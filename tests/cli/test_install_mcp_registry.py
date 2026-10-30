"""Focused contracts for pinned, compatibility-preserving MCP registry entries."""

import json
import shlex
from pathlib import Path
from types import SimpleNamespace

from superclaude.cli import install_mcp


def test_updated_mcp_registry_commands_are_pinned_and_stable():
    expected = {
        "morphllm-fast-apply": "npx -y @morphllm/morphmcp",
        "auggie": "auggie --mcp --mcp-auto-workspace",
    }

    for key, command in expected.items():
        entry = install_mcp.MCP_SERVERS[key]
        assert entry["name"] == key
        assert entry["transport"] == "stdio"
        assert entry["command"] == command

    assert (
        install_mcp.MCP_SERVERS["morphllm-fast-apply"]["api_key_env"] == "MORPH_API_KEY"
    )
    assert (
        install_mcp.MCP_SERVERS["auggie"]["requires_global_binary"]["install_command"]
        == "npm install -g @augmentcode/auggie@0.36.0"
    )


def test_removed_mcp_servers_are_not_in_registry():
    for name in (
        "sequential-thinking",
        "magic",
        "chrome-devtools",
        "codebase-memory-mcp",
        "serena",
    ):
        assert name not in install_mcp.MCP_SERVERS


def test_distributable_mcp_templates_match_pinned_registry_commands():
    root = Path(__file__).resolve().parents[2]
    expected = {
        "morphllm.json": ["-y", "@morphllm/morphmcp"],
    }
    server_names = {
        "morphllm.json": "morphllm-fast-apply",
    }

    for base in (
        root / "src/superclaude/mcp/configs",
        root / "plugins/superclaude/mcp/configs",
    ):
        for filename, args in expected.items():
            template = json.loads((base / filename).read_text())
            server_name = server_names[filename]
            server = template[server_name]
            assert server["args"] == args
            assert [server["command"], *server["args"]] == shlex.split(
                install_mcp.MCP_SERVERS[server_name]["command"]
            )
            if filename == "morphllm.json":
                assert "@morph-llm/morph-fast-apply" not in json.dumps(template)
                assert "/home/" not in server["args"]


def test_auggie_global_binary_reconciles_stale_version(monkeypatch):
    calls = []
    versions = iter(["auggie 0.35.0", "auggie 0.36.0"])

    def fake_run_command(cmd, **kwargs):
        calls.append(cmd)
        if cmd == ["node", "--version"]:
            return SimpleNamespace(returncode=0, stdout="v20.0.0", stderr="")
        if cmd == ["auggie", "--version"]:
            return SimpleNamespace(returncode=0, stdout=next(versions), stderr="")
        assert cmd == ["npm", "install", "-g", "@augmentcode/auggie@0.36.0"]
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr(install_mcp, "_run_command", fake_run_command)
    monkeypatch.setattr(install_mcp.click, "confirm", lambda *args, **kwargs: True)

    assert install_mcp.ensure_global_binary(
        install_mcp.MCP_SERVERS["auggie"]["requires_global_binary"], False
    )
    assert calls == [
        ["node", "--version"],
        ["auggie", "--version"],
        ["npm", "install", "-g", "@augmentcode/auggie@0.36.0"],
        ["auggie", "--version"],
    ]


def test_auggie_global_binary_rejects_post_install_version_mismatch(monkeypatch):
    versions = iter(["auggie 0.35.0", "auggie 0.35.0"])

    def fake_run_command(cmd, **kwargs):
        if cmd == ["node", "--version"]:
            return SimpleNamespace(returncode=0, stdout="v20.0.0", stderr="")
        if cmd == ["auggie", "--version"]:
            return SimpleNamespace(returncode=0, stdout=next(versions), stderr="")
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr(install_mcp, "_run_command", fake_run_command)
    monkeypatch.setattr(install_mcp.click, "confirm", lambda *args, **kwargs: True)

    assert not install_mcp.ensure_global_binary(
        install_mcp.MCP_SERVERS["auggie"]["requires_global_binary"], False
    )


def test_auggie_global_binary_skips_install_at_pinned_version(monkeypatch):
    calls = []

    def fake_run_command(cmd, **kwargs):
        calls.append(cmd)
        output = "v20.0.0" if cmd == ["node", "--version"] else "auggie 0.36.0"
        return SimpleNamespace(returncode=0, stdout=output, stderr="")

    monkeypatch.setattr(install_mcp, "_run_command", fake_run_command)

    assert install_mcp.ensure_global_binary(
        install_mcp.MCP_SERVERS["auggie"]["requires_global_binary"], False
    )
    assert calls == [["node", "--version"], ["auggie", "--version"]]


def test_auggie_reconciles_binary_before_up_to_date_registration(monkeypatch):
    calls = []
    versions = iter(["auggie 0.35.0", "auggie 0.36.0"])

    def fake_run_command(cmd, **kwargs):
        calls.append(cmd)
        if cmd == ["node", "--version"]:
            return SimpleNamespace(returncode=0, stdout="v20.0.0", stderr="")
        if cmd == ["auggie", "--version"]:
            return SimpleNamespace(returncode=0, stdout=next(versions), stderr="")
        if cmd == ["npm", "install", "-g", "@augmentcode/auggie@0.36.0"]:
            return SimpleNamespace(returncode=0, stdout="", stderr="")
        assert cmd == ["claude", "mcp", "get", "auggie"]
        return SimpleNamespace(
            returncode=0,
            stdout=(
                "auggie:\n"
                "  Scope: User config\n"
                "  Command: auggie\n"
                "  Args: --mcp --mcp-auto-workspace\n"
            ),
            stderr="",
        )

    monkeypatch.setattr(install_mcp, "_run_command", fake_run_command)
    monkeypatch.setattr(install_mcp, "check_mcp_server_installed", lambda name: True)
    monkeypatch.setattr(install_mcp.click, "confirm", lambda *args, **kwargs: True)

    assert install_mcp.install_mcp_server(install_mcp.MCP_SERVERS["auggie"])
    assert calls.index(
        ["npm", "install", "-g", "@augmentcode/auggie@0.36.0"]
    ) < calls.index(["claude", "mcp", "get", "auggie"])


def test_auggie_global_binary_rejects_node_19_before_binary_install(monkeypatch):
    calls = []

    def fake_run_command(cmd, **kwargs):
        calls.append(cmd)
        return SimpleNamespace(returncode=0, stdout="v19.0.0", stderr="")

    monkeypatch.setattr(install_mcp, "_run_command", fake_run_command)

    assert not install_mcp.ensure_global_binary(
        install_mcp.MCP_SERVERS["auggie"]["requires_global_binary"], False
    )
    assert calls == [["node", "--version"]]


def test_selected_npm_prerequisites_probe_only_claude_node_and_npx(monkeypatch):
    calls = []

    def run(cmd, **kwargs):
        calls.append(cmd)
        assert cmd in (
            ["claude", "--version"],
            ["node", "--version"],
            ["npx", "--version"],
        )
        return SimpleNamespace(returncode=0, stdout="v18.0.0", stderr="")

    monkeypatch.setattr(install_mcp, "_run_command", run)
    assert install_mcp.check_prerequisites(["context7"]) == (True, [])
    assert calls == [
        ["claude", "--version"],
        ["node", "--version"],
        ["npx", "--version"],
    ]


LITELLM_GET_OUTPUT = (
    "litellm:\n"
    "  Scope: User config (available in all your projects)\n"
    "  Status: ✔ Connected\n"
    "  Type: http\n"
    "  URL: http://ibcore:4000/mcp/\n"
    "  Headers:\n"
    "    x-litellm-api-key: Bearer ${LITELLM_API_KEY}\n"
    "\n"
    "To remove this server, run: claude mcp remove litellm -s user\n"
)


def test_litellm_registry_entry_is_http_with_literal_key_placeholder():
    entry = install_mcp.MCP_SERVERS["litellm"]
    assert entry["name"] == "litellm"
    assert entry["transport"] == "http"
    assert entry["url"] == "http://ibcore:4000/mcp/"
    assert entry["headers"] == {"x-litellm-api-key": "Bearer ${LITELLM_API_KEY}"}
    assert entry["opt_in_only"] is True
    assert "command" not in entry
    assert "api_key_env" not in entry


def test_litellm_dry_run_prints_http_command_with_literal_placeholder(
    monkeypatch, capsys
):
    monkeypatch.setattr(install_mcp, "check_mcp_server_installed", lambda name: False)
    monkeypatch.setenv("LITELLM_API_KEY", "sk-should-never-appear")

    assert install_mcp.install_mcp_server(
        install_mcp.MCP_SERVERS["litellm"], scope="user", dry_run=True
    )

    out = capsys.readouterr().out
    assert (
        "Would run: claude mcp add --transport http --scope user litellm "
        "http://ibcore:4000/mcp/ --header x-litellm-api-key: Bearer ${LITELLM_API_KEY}"
    ) in out
    assert "sk-should-never-appear" not in out
    assert " -- " not in out


def test_all_servers_choice_excludes_opt_in_litellm(monkeypatch):
    answers = iter(["1", "0"])
    installed = []
    monkeypatch.setattr(install_mcp, "_is_interactive", lambda: True)
    monkeypatch.setattr(
        install_mcp.click, "prompt", lambda *args, **kwargs: next(answers)
    )
    monkeypatch.setattr(install_mcp, "check_prerequisites", lambda selected: (True, []))
    monkeypatch.setattr(
        install_mcp,
        "install_mcp_server",
        lambda info, scope, dry_run: installed.append(info["name"]) or True,
    )

    ok, _ = install_mcp.install_mcp_servers()

    assert ok
    assert "litellm" not in installed
    assert "context7" in installed


def test_litellm_can_still_be_selected_by_name(monkeypatch):
    installed = []
    monkeypatch.setattr(install_mcp, "check_prerequisites", lambda selected: (True, []))
    monkeypatch.setattr(
        install_mcp,
        "install_mcp_server",
        lambda info, scope, dry_run: installed.append(info["name"]) or True,
    )

    ok, _ = install_mcp.install_mcp_servers(["litellm"])

    assert ok
    assert installed == ["litellm"]


def test_litellm_matching_registration_is_not_removed_and_re_added(monkeypatch):
    calls = []

    def fake_run_command(cmd, **kwargs):
        calls.append(cmd)
        assert cmd == ["claude", "mcp", "get", "litellm"]
        return SimpleNamespace(returncode=0, stdout=LITELLM_GET_OUTPUT, stderr="")

    monkeypatch.setattr(install_mcp, "_run_command", fake_run_command)
    monkeypatch.setattr(install_mcp, "check_mcp_server_installed", lambda name: True)

    assert install_mcp.install_mcp_server(install_mcp.MCP_SERVERS["litellm"])
    assert calls == [["claude", "mcp", "get", "litellm"]]


def test_litellm_changed_header_is_removed_and_re_added(monkeypatch):
    calls = []
    stale = LITELLM_GET_OUTPUT.replace("LITELLM_API_KEY", "OLD_KEY")

    def fake_run_command(cmd, **kwargs):
        calls.append(cmd)
        if cmd == ["claude", "mcp", "get", "litellm"]:
            return SimpleNamespace(returncode=0, stdout=stale, stderr="")
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr(install_mcp, "_run_command", fake_run_command)
    monkeypatch.setattr(install_mcp, "check_mcp_server_installed", lambda name: True)

    assert install_mcp.install_mcp_server(install_mcp.MCP_SERVERS["litellm"])
    assert ["claude", "mcp", "remove", "litellm", "--scope", "user"] in calls
    assert [
        "claude",
        "mcp",
        "add",
        "--transport",
        "http",
        "--scope",
        "user",
        "litellm",
        "http://ibcore:4000/mcp/",
        "--header",
        "x-litellm-api-key: Bearer ${LITELLM_API_KEY}",
    ] in calls


def test_codegraph_registry_entry_contract():
    entry = install_mcp.MCP_SERVERS["codegraph"]
    assert entry["name"] == "codegraph"
    assert entry["transport"] == "stdio"
    assert entry["command"] == "codegraph"
    assert entry["args"] == ["serve", "--mcp"]
    assert entry["required"] is False


def test_codegraph_dispatches_to_phase_function_never_generic_add(monkeypatch):
    seen = []

    def phase(**kwargs):
        seen.append(kwargs)
        return True, "phase ran"

    def forbidden(*args, **kwargs):
        raise AssertionError("generic registration path used")

    monkeypatch.setattr(install_mcp, "install_codegraph_mcp", phase)
    monkeypatch.setattr(install_mcp, "_run_command", forbidden)
    monkeypatch.setattr(install_mcp, "_exec_claude", forbidden)
    assert install_mcp.install_mcp_server(
        install_mcp.MCP_SERVERS["codegraph"], scope="user", dry_run=True
    )
    assert seen == [{"scope": "user", "dry_run": True}]

    monkeypatch.setattr(install_mcp, "install_codegraph_mcp", lambda **k: (False, "no"))
    assert not install_mcp.install_mcp_server(install_mcp.MCP_SERVERS["codegraph"])


def test_codegraph_is_listed_by_mcp_list(monkeypatch, capsys):
    monkeypatch.setattr(install_mcp, "check_mcp_server_installed", lambda name: False)
    install_mcp.list_available_servers()
    assert "codegraph" in capsys.readouterr().out
