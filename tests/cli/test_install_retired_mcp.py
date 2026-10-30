"""Retire step: stale codebase-memory-mcp and serena user registrations.

No real ``claude`` is ever run except the stub scripts a test writes itself.
"""

import json
import os
import stat
import time

import pytest
from click.testing import CliRunner

from superclaude.cli import install_mcp
from superclaude.cli import install_retired_mcp as retired
from superclaude.cli.main import main

CBM = "codebase-memory-mcp"
SER = "serena"
PIN = [
    "--from",
    "serena-agent==1.7.0",
    "serena",
    "start-mcp-server",
    "--context",
    "claude-code",
    "--project-from-cwd",
    "--enable-web-dashboard",
    "false",
    "--enable-gui-log-window",
    "false",
]
ROW_A = (
    "uvx",
    [
        "--from",
        "git+https://github.com/oraios/serena",
        "serena",
        "start-mcp-server",
        "--context",
        "ide-assistant",
        "--enable-web-dashboard",
        "false",
        "--enable-gui-log-window",
        "false",
    ],
)
ROW_B = (
    "uvx",
    [
        "--from",
        "git+https://github.com/oraios/serena",
        "serena",
        "start-mcp-server",
        "--context",
        "ide-assistant",
        "--project",
        "$(pwd)",
    ],
)
ROW_C = (
    "serena",
    ["start-mcp-server", "--context", "ide-assistant", "--project", "$(pwd)"],
)


def stdio(command, args, **extra):
    return {"type": "stdio", "command": command, "args": list(args), **extra}


class Env:
    def __init__(self, home, config):
        self.home = home
        self.config = config
        self.claude_calls = []

    @property
    def bin(self):
        return self.home / ".local" / "bin"

    def write(self, servers, projects=None):
        data = {"mcpServers": servers}
        if projects is not None:
            data["projects"] = projects
        (self.config / ".claude.json").write_text(json.dumps(data), encoding="utf-8")

    def read(self):
        return json.loads((self.config / ".claude.json").read_text(encoding="utf-8"))

    def private(self, name, mode=0o600):
        self.bin.mkdir(parents=True, exist_ok=True)
        path = self.bin / name
        path.write_text("{}", encoding="utf-8")
        path.chmod(mode)
        return path

    def binary(self):
        self.bin.mkdir(parents=True, exist_ok=True)
        path = self.bin / CBM
        path.write_text("benign fixture, never executed\n", encoding="utf-8")
        path.chmod(0o700)
        return path


@pytest.fixture
def env(tmp_path, monkeypatch):
    home = tmp_path / "home"
    config = tmp_path / "config"
    home.mkdir()
    config.mkdir()
    (home / ".local").mkdir(mode=0o755)
    (home / ".local").chmod(0o755)
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(config))
    state = Env(home, config)

    def fake_exec(argv, timeout):
        state.claude_calls.append(list(argv))
        assert argv[:3] == ["claude", "mcp", "remove"] and argv[4:] == [
            "--scope",
            "user",
        ]
        data = state.read()
        data["mcpServers"].pop(argv[3], None)
        (config / ".claude.json").write_text(json.dumps(data), encoding="utf-8")
        return 0

    monkeypatch.setattr(install_mcp, "_exec_claude", fake_exec)
    monkeypatch.setattr(retired.shutil, "which", lambda name: "/fixture/claude")
    return state


def classify(entry, name):
    return retired.RETIRED_MCP_SERVERS[name](entry, retired.Path.home().absolute())


# ---- classifier: codebase-memory-mcp -------------------------------------------


@pytest.mark.parametrize(
    "entry",
    [
        stdio("/usr/local/bin/codebase-memory-mcp", []),
        {"command": "/opt/x/codebase-memory-mcp"},
        stdio("/usr/local/bin/codebase-memory-mcp", [], env={}),
        stdio("/usr/local/bin/codebase-memory-mcp", [], headers={}),
    ],
)
def test_cbm_ironclaude_shapes_are_removed(env, entry):
    assert classify(entry, CBM)[0] == "remove"


@pytest.mark.parametrize(
    "entry",
    [
        stdio("codebase-memory-mcp", []),  # relative command
        stdio("/usr/local/bin/codebase-memory-mcp", ["--stale"]),
        stdio("/usr/local/bin/codebase-memory-mcp", [], env={"A": "1"}),
        stdio("/usr/local/bin/codebase-memory-mcp", [], headers={"A": "1"}),
        stdio("/usr/local/bin/other-binary", []),
        {"type": "http", "url": "https://example.invalid/mcp"},
        {"type": "sse", "command": "/usr/local/bin/codebase-memory-mcp"},
    ],
)
def test_cbm_other_shapes_are_kept(env, entry):
    verdict, reason = classify(entry, CBM)
    assert verdict == "keep" and reason == "not an IronClaude registration"


def test_cbm_home_path_with_binary_present_is_kept(env):
    path = env.binary()
    verdict, reason = classify(stdio(str(path), []), CBM)
    assert verdict == "keep" and "still present" in reason


def test_cbm_home_path_with_binary_gone_is_removed(env):
    verdict, _ = classify(stdio(str(env.bin / CBM), []), CBM)
    assert verdict == "remove"


def test_cbm_path_under_a_different_home_is_kept(env):
    entry = stdio("/home/someone-else/.local/bin/codebase-memory-mcp", [])
    assert classify(entry, CBM) == ("keep", "path differs from current HOME")


# ---- classifier: serena --------------------------------------------------------


@pytest.mark.parametrize("row", [ROW_A, ROW_B, ROW_C], ids=["a", "b", "c"])
@pytest.mark.parametrize(
    "extra", [{}, {"env": {}}, {"headers": {}}, {"env": {}, "headers": {}}]
)
def test_serena_tier_r_rows_are_removed(env, row, extra):
    verdict, reason = classify(stdio(row[0], row[1], **extra), SER)
    assert verdict == "remove" and row[0] in reason


def test_serena_tier_r_row_without_type_is_removed(env):
    assert classify({"command": ROW_A[0], "args": ROW_A[1]}, SER)[0] == "remove"


def _near_misses():
    cmd, args = ROW_A
    changed = list(args)
    changed[changed.index("ide-assistant")] = "ide-assistan"
    yield "token-changed", (cmd, changed)
    yield "extra-arg", (cmd, [*args, "--extra"])
    yield "missing-arg", (cmd, args[:-2])
    yield "expanded-pwd", (ROW_B[0], [*ROW_B[1][:-1], "/work/project"])
    yield "wrong-command", ("uvx2", args)
    yield "row-c-expanded", (ROW_C[0], [*ROW_C[1][:-1], "/work/project"])


@pytest.mark.parametrize(
    "label,shape", list(_near_misses()), ids=lambda v: v if isinstance(v, str) else ""
)
def test_serena_near_misses_are_tier_k(env, label, shape):
    assert classify(stdio(*shape), SER) == ("keep", retired.TIER_K_LINE)


@pytest.mark.parametrize(
    "shape",
    [
        ("uvx", PIN),  # the current pin: identical to what Coder's bundle writes
        (
            "uvx",
            [
                "--from",
                "git+https://github.com/oraios/serena",
                "serena",
                "start-mcp-server",
                "--context",
                "ide-assistant",
            ],
        ),
        ("uvx", [*ROW_B[1][:-1], "/abs/project"]),
        ("other-launcher", ["start-mcp-server"]),
    ],
    ids=["current-pin", "bare-ide-assistant", "project-abs-path", "other-launcher"],
)
@pytest.mark.parametrize("extra", [{}, {"env": {}}])
def test_serena_tier_k_is_kept_with_the_printed_line(env, shape, extra):
    assert classify(stdio(*shape, **extra), SER) == ("keep", retired.TIER_K_LINE)


@pytest.mark.parametrize("extra", [{"env": {"A": "1"}}, {"headers": {"A": "1"}}])
@pytest.mark.parametrize(
    "shape", [ROW_A, ("uvx", PIN)], ids=["tier-r-shape", "current-pin"]
)
def test_serena_customised_registration_is_never_removed(env, shape, extra):
    assert classify(stdio(*shape, **extra), SER) == ("keep", "customised registration")


@pytest.mark.parametrize(
    "entry",
    [
        stdio("serena", ["--version"]),
        {"type": "http", "url": "https://example.invalid/mcp"},
        {"command": 7, "args": "start-mcp-server"},
    ],
)
def test_serena_without_a_launcher_argv_is_not_touched(env, entry):
    assert classify(entry, SER) == ("keep", "not a Serena launcher registration")


# ---- the step: messages, scopes, files -----------------------------------------


def test_tier_r_serena_removal_prints_argv_and_the_serena_local_hint(env, capsys):
    env.write(
        {
            SER: stdio(*ROW_A, env={}),
            "tavily": {"type": "stdio", "command": "npx", "args": []},
        }
    )
    outcomes = retired.run_retire_step()
    out = capsys.readouterr().out
    assert outcomes == {CBM: "absent", SER: "removed"}
    assert set(env.read()["mcpServers"]) == {"tavily"}
    assert env.claude_calls == [["claude", "mcp", "remove", SER, "--scope", "user"]]
    assert (
        "uvx --from git+https://github.com/oraios/serena serena start-mcp-server" in out
    )
    assert "serena-local" in out and "serena-agent==1.7.0" in out
    assert (
        "Restart running Claude sessions" in out and "superclaude install --list" in out
    )
    assert "uv tool uninstall serena-agent" in out


def test_cbm_removal_prints_the_companion_note_and_keeps_data(env, capsys):
    env.write({CBM: stdio("/usr/local/bin/codebase-memory-mcp", [])})
    assert retired.run_retire_step()[CBM] == "removed"
    out = capsys.readouterr().out
    assert "its own `uninstall` removes its client companions" in out
    assert "only if you no longer need the indexes" in out
    assert env.read()["mcpServers"] == {}


def test_tier_k_line_is_printed_and_nothing_is_removed(env, capsys):
    env.write({SER: stdio("uvx", PIN, env={})})
    assert retired.run_retire_step()[SER] == "kept"
    assert retired.TIER_K_LINE in capsys.readouterr().out
    assert env.claude_calls == [] and SER in env.read()["mcpServers"]


def test_local_scope_and_project_mcp_json_are_ignored(
    env, tmp_path, monkeypatch, capsys
):
    project = tmp_path / "project"
    project.mkdir()
    (project / ".mcp.json").write_text(
        json.dumps(
            {
                "mcpServers": {
                    SER: stdio(*ROW_A),
                    CBM: stdio("/usr/local/bin/" + CBM, []),
                }
            }
        )
    )
    monkeypatch.chdir(project)
    env.write({}, projects={"/x": {"mcpServers": {SER: stdio(*ROW_A)}}})
    assert retired.run_retire_step() == {}
    assert env.claude_calls == []
    assert env.read()["projects"]["/x"]["mcpServers"][SER] == stdio(*ROW_A)
    assert "No retired MCP registrations present" in capsys.readouterr().out
    assert json.loads((project / ".mcp.json").read_text())["mcpServers"][SER]


def test_receipt_and_marker_are_deleted_when_the_binary_is_gone_in_one_run(env, capsys):
    receipt = env.private(retired.RECEIPT_NAME)
    marker = env.private(retired.MARKER_NAME)
    env.write({CBM: stdio(str(env.bin / CBM), [])})
    outcomes = retired.run_retire_step()
    assert outcomes[CBM] == "removed"
    assert not receipt.exists() and not marker.exists()
    assert "Removed" in capsys.readouterr().out


def test_binary_present_keeps_registration_receipt_and_marker(env, capsys):
    env.binary()
    receipt = env.private(retired.RECEIPT_NAME)
    marker = env.private(retired.MARKER_NAME)
    env.write({CBM: stdio(str(env.bin / CBM), [])})
    assert retired.run_retire_step()[CBM] == "kept"
    out = capsys.readouterr().out
    assert receipt.exists() and marker.exists() and env.claude_calls == []
    assert f'"$HOME/.local/bin/{CBM}" uninstall -y --dir="$HOME/.local/bin"' in out


def test_receipt_failing_a_predicate_is_listed_not_deleted(env, capsys):
    shared = env.private(retired.RECEIPT_NAME, mode=0o644)
    target = env.bin / "elsewhere"
    target.write_text("{}")
    target.chmod(0o600)
    link = env.bin / retired.MARKER_NAME
    link.symlink_to(target)
    env.write({})
    retired.run_retire_step()
    out = capsys.readouterr().out
    assert shared.exists() and link.is_symlink() and target.exists()
    assert out.count("Left in place (not deleted)") == 2


def test_only_receipt_and_marker_are_ever_deleted(env):
    other = env.private("keep-me.json")
    receipt = env.private(retired.RECEIPT_NAME)
    env.write({})
    retired.run_retire_step()
    assert other.exists() and not receipt.exists()
    assert stat.S_ISREG(other.stat().st_mode)


def test_missing_claude_cli_prints_the_manual_commands(env, monkeypatch, capsys):
    monkeypatch.setattr(retired.shutil, "which", lambda name: None)
    env.write({SER: stdio(*ROW_A), CBM: stdio("/usr/local/bin/" + CBM, [])})
    outcomes = retired.run_retire_step()
    out = capsys.readouterr().out
    assert outcomes == {CBM: "skipped", SER: "skipped"}
    assert f"claude mcp remove {CBM} --scope user" in out
    assert f"claude mcp remove {SER} --scope user" in out
    assert env.claude_calls == [] and set(env.read()["mcpServers"]) == {CBM, SER}


def test_unknown_lookup_warns_with_the_manual_command(env, monkeypatch, capsys):
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", "")
    outcomes = retired.run_retire_step()
    out = capsys.readouterr().out
    assert outcomes == {CBM: "unknown", SER: "unknown"}
    assert (
        "empty CLAUDE_CONFIG_DIR" in out
        and f"claude mcp remove {SER} --scope user" in out
    )
    assert env.claude_calls == []


def test_nothing_to_retire_runs_no_subprocess(env, monkeypatch):
    monkeypatch.setattr(
        install_mcp,
        "_exec_claude",
        lambda *a, **k: pytest.fail("subprocess for nothing"),
    )
    env.write({"tavily": {"type": "stdio", "command": "npx", "args": []}})
    assert retired.run_retire_step() == {}


# ---- the removal helper --------------------------------------------------------


def test_helper_keeps_an_entry_replaced_before_removal(env):
    env.write({SER: stdio("uvx", PIN)})
    status = install_mcp._remove_exact_user_entry(SER, lambda e: e["args"] == ROW_A[1])
    assert status == "changed" and env.claude_calls == []


def test_helper_keeps_an_entry_replaced_during_removal(env, monkeypatch):
    env.write({SER: stdio(*ROW_A)})

    def replace(argv, timeout):
        env.write({SER: stdio("uvx", PIN)})
        return 0

    monkeypatch.setattr(install_mcp, "_exec_claude", replace)
    status = install_mcp._remove_exact_user_entry(SER, lambda e: e["args"] == ROW_A[1])
    assert status == "replaced" and env.read()["mcpServers"][SER]["args"] == PIN


def test_helper_reports_unverified_when_the_same_shape_remains(env, monkeypatch):
    env.write({SER: stdio(*ROW_A)})
    calls = []
    monkeypatch.setattr(
        install_mcp, "_exec_claude", lambda argv, timeout: calls.append(argv) or 0
    )
    status = install_mcp._remove_exact_user_entry(SER, lambda e: True)
    assert status == "unverified" and len(calls) == 1  # never retried


@pytest.mark.parametrize("returncode,status", [(1, "failed"), (0, "removed")])
def test_helper_maps_exit_status(env, monkeypatch, returncode, status):
    env.write({SER: stdio(*ROW_A)})

    def run(argv, timeout):
        if returncode == 0:
            env.write({})
        return returncode

    monkeypatch.setattr(install_mcp, "_exec_claude", run)
    assert install_mcp._remove_exact_user_entry(SER, lambda e: True) == status


# ---- bounds: a hanging claude --------------------------------------------------


def _hanging_claude(tmp_path, monkeypatch):
    bin_dir = tmp_path / "stubbin"
    bin_dir.mkdir()
    pidfile = tmp_path / "child.pid"
    script = bin_dir / "claude"
    script.write_text(f"#!/bin/sh\nsleep 60 &\necho $! > {pidfile}\nwait\n")
    script.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ['PATH']}")
    return pidfile


def _alive(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    try:  # a zombie still answers signal 0
        return "Z" not in open(f"/proc/{pid}/stat").read().rsplit(")", 1)[1].split()[0]
    except OSError:
        return False


def test_hanging_claude_is_killed_with_its_process_group(env, tmp_path, monkeypatch):
    monkeypatch.undo()  # drop the stub `_exec_claude`; keep real subprocess handling
    monkeypatch.setenv("HOME", str(env.home))
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(env.config))
    pidfile = _hanging_claude(tmp_path, monkeypatch)
    env.write({SER: stdio(*ROW_A)})
    started = time.monotonic()
    status = install_mcp._remove_exact_user_entry(
        SER, lambda e: True, per_call_timeout=0.5
    )
    assert status == "timeout" and time.monotonic() - started < 5
    pid = int(pidfile.read_text())
    deadline = time.monotonic() + 3
    while _alive(pid) and time.monotonic() < deadline:
        time.sleep(0.05)
    assert not _alive(pid)


def test_step_cap_skips_the_remaining_calls(env, tmp_path, monkeypatch, capsys):
    monkeypatch.undo()
    monkeypatch.setenv("HOME", str(env.home))
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(env.config))
    _hanging_claude(tmp_path, monkeypatch)
    monkeypatch.setattr(retired, "STEP_CAP", 0.4)
    monkeypatch.setattr(retired, "PER_CALL_TIMEOUT", 5.0)
    env.write({CBM: stdio("/usr/local/bin/" + CBM, []), SER: stdio(*ROW_A)})
    started = time.monotonic()
    outcomes = retired.run_retire_step()
    assert time.monotonic() - started < 5
    assert outcomes == {CBM: "timeout", SER: "skipped"}
    out = capsys.readouterr().out
    assert "time cap" in out and f"claude mcp remove {SER} --scope user" in out
    assert set(env.read()["mcpServers"]) == {CBM, SER}


# ---- CLI integration -----------------------------------------------------------

_INSTALLERS = (
    "superclaude.cli.install_core.install_core_files",
    "superclaude.cli.install_commands.install_commands",
    "superclaude.cli.install_agents.install_agents",
    "superclaude.cli.install_skills.install_all_skills",
    "superclaude.cli.install_ccsession.wire_ccsession",
    "superclaude.cli.install_hooks.install_hooks",
    "superclaude.cli.install_templates.install_templates",
    "superclaude.cli.install_user_setup.install_user_setup",
)


def _stub_framework(monkeypatch, *, failing=None):
    for path in _INSTALLERS:
        name = path.rsplit(".", 1)[-1]
        monkeypatch.setattr(path, lambda *a, _n=name, **k: (_n != failing, f"{_n} ok"))
    # the required codegraph phase runs between user setup and the retire step
    monkeypatch.setattr(
        "superclaude.cli.install_mcp.install_codegraph_mcp",
        lambda **k: (True, "install_codegraph_mcp ok"),
    )


@pytest.mark.parametrize("failing", [None, "install_hooks"])
def test_a_failing_retire_step_never_changes_the_install_exit_code(
    env, monkeypatch, failing
):
    _stub_framework(monkeypatch, failing=failing)

    def boom():
        raise RuntimeError("retire exploded")

    monkeypatch.setattr(retired, "run_retire_step", boom)
    result = CliRunner().invoke(main, ["install"])
    assert result.exit_code == (1 if failing else 0), result.output
    assert "Retire step skipped" in result.output and "RuntimeError" in result.output


def test_install_runs_the_retire_step_after_user_setup(env, monkeypatch):
    _stub_framework(monkeypatch)
    env.write({SER: stdio(*ROW_A, env={})})
    result = CliRunner().invoke(main, ["install", "--force"])
    assert result.exit_code == 0, result.output
    assert env.claude_calls == [["claude", "mcp", "remove", SER, "--scope", "user"]]
    assert result.output.index("install_user_setup ok") < result.output.index(
        "Retiring stale"
    )


def test_install_list_reports_each_retired_name_without_changes(env, monkeypatch):
    monkeypatch.setattr(
        install_mcp, "_exec_claude", lambda *a, **k: pytest.fail("list must not exec")
    )
    env.write({SER: stdio("uvx", PIN, env={}), CBM: stdio("/usr/local/bin/" + CBM, [])})
    before = env.read()
    result = CliRunner().invoke(main, ["install", "--list"])
    assert result.exit_code == 0, result.output
    assert "will be removed (IronClaude shape)" in result.output
    assert "kept: " + retired.TIER_K_LINE in result.output
    assert env.read() == before
    env.write({})
    result = CliRunner().invoke(main, ["install", "--list"])
    assert result.output.count("absent") >= 2


def test_update_and_doctor_never_mutate_and_never_change_their_exit_code(
    env, monkeypatch
):
    from superclaude.cli.doctor import _check_retired_mcp, run_doctor

    monkeypatch.setattr(
        install_mcp, "_exec_claude", lambda *a, **k: pytest.fail("must not exec")
    )
    _stub_framework(monkeypatch)
    env.write({SER: stdio(*ROW_A, env={})})
    before = env.read()

    update = CliRunner().invoke(main, ["update"])
    assert update.exit_code == 0, update.output
    assert "legacy registration present: run `superclaude install`" in update.output

    check = _check_retired_mcp()
    assert check["passed"] is True and "warning" in check["name"]
    assert any(c["name"].startswith("Retired MCP") for c in run_doctor()["checks"])
    assert env.read() == before

    env.write({})
    assert (
        "legacy registration present" not in CliRunner().invoke(main, ["update"]).output
    )
    assert (
        _check_retired_mcp()["passed"] is True
        and "warning" not in _check_retired_mcp()["name"]
    )


def test_module_does_not_depend_on_the_deleted_installer():
    import superclaude.cli.install_retired_mcp as module

    source = open(module.__file__, encoding="utf-8").read()
    assert "install_codebase_memory" not in source
