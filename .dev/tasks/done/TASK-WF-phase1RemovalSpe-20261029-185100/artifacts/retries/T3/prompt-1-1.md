156a61f5900807917014d54f20609cacb84c7964
Review one task for spec compliance.

Task brief: ## Task 3: Stop `superclaude install` and `install --list` from provisioning codebase-memory

Depends on: Task 2

Implements ./source.md §8 T2 and rows C3, C4, C7. Apply `.dev/codegraph-migration/inventory/codebase-memory.md` §4.2 exactly to `src/superclaude/cli/main.py` (`:66`, `:78-83`, `:161-186`, `:254-262`, the `native_success` exit term, help text `:38`, `:44`, `:50-52`), `tests/cli/test_update_command.py` (fixture `native_phase_guard` reduced to `HOME`, `CLAUDE_CONFIG_DIR` and the plugin/Orca stubs; delete the 5 test functions named in row C7; rewrite `test_install_force_target_do_not_redirect_or_force_native` to drop the native assertions) and `tests/cli/test_install_codebase_memory.py` (delete the cross-entry fixture and tests at `:1382`, `:1517`, `:1614`). The fixture and the `main.py` change land in the same commit, so no real-install test can reach the real upstream installer. Commit `feat(install)!: stop installing codebase-memory-mcp from superclaude install (#323)`.

Acceptance criteria:
- T3.AC1: `uv run pytest tests/cli/test_update_command.py tests/cli/test_install_codebase_memory.py tests/cli/test_install_mcp_cli.py tests/cli/test_cli_registration.py tests/unit/test_cli_install.py -q -p no:cacheprovider` passes.
- T3.AC2: `rg -n "install_codebase_memory|_NATIVE_INSTALLER|native_phase_guard" src/superclaude/cli/main.py tests/cli/test_update_command.py` prints nothing.

`$PKG` = /home/coder/workspaces/worktrees/IronClaude/feat-codememory-codegraph-init/.dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100 (repo root: the git top-level of that directory). The source spec for anything the brief says is in `$PKG/source.md`; the plan is `$PKG/TASK-WF-phase1RemovalSpe-20261029-185100.md`.

Global constraints (plan `## Constraints`, verbatim):
- Work on branch `ironbelly/feat-codememory-codegraph-init`, base commit `55d40308`. Do not open a pull request to `master` for Phase 1 alone and do not push to `upstream`; Phases 1 and 2 merge as one unit (./source.md §2.2, D9).
- `$PKG` in every command below means this package's directory as the executor resolves it at run time (the folder that holds this plan); never hardcode it. Evidence goes under `$PKG/artifacts/`; handoff notes for other repos go under `$PKG/handoffs/`.
- One commit per task, conventional commit message as given in each task, ending with the attribution line the executor's session requires. Every commit stages the task package with `git add .dev/tasks` (package, `progress.md` and `artifacts/` included). Never stage or commit `.claude/` content (only `.claude/settings.json` is tracked, and Phase 1 does not touch it). Never use `git add -f` on a `.claude/` path.
- Every edit to a `src/superclaude/...` primitive is mirrored by hand, in the same commit, in its `plugins/superclaude/...` twin and its root `commands/sc-*.md` / `agents/sc-*.md` copy where ./source.md §1.2 lists one (D15).
- After editing `src/superclaude/core/HOW-WE-WORK.md`, copy it byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`; if the edit touches the block between `<!-- level-table:v1 -->` and `<!-- /level-table -->`, re-copy that block into `src/superclaude/core/CLAUDE.md`.
- Use `uv run` for Python; standalone scripts run with `uv run --no-project python -I`. Every pytest run uses `-p no:cacheprovider`. Full-suite runs always set `T02_15_PERF_REPORT=/tmp/p1-perf.json` so the tracked `.dev/releases/current/cliEval/evidence/T02.15/perf.json` is not rewritten. After every test run, `git status --short` must list only files the task intends to change; restore any tracked file a test changed.
- Test baseline: the full suite already has failures at the base (W1 saw 27 failed and 16 errors). "Passes" for a targeted command means no failing test id that is not in `$PKG/artifacts/baseline/full.txt` (compare with the `comm -13` form in Task 18); never assume a clean suite.
- Never run the real `./update.sh`, `superclaude install` (including `--list`) or `claude mcp add/remove` against the real `HOME`; every environment check runs in a sandbox `HOME` made with `mktemp -d` (./source.md §10, D8). Never delete user data (`~/.serena`, project `.serena/` folders outside this repo, `~/.cache/codebase-memory-mcp`). Never edit another repository.
- Progress reporting (./source.md §9): at the end of each task group (Phases 1-6 below, i.e. groups G0-G5) post exactly one comment on issue #323 of the fork, and only there. First run `gh repo view --json nameWithOwner -q .nameWithOwner` (must print `IronbellyOrg/IronClaude`; otherwise run `gh repo set-default IronbellyOrg/IronClaude`), then `gh issue comment 323 --repo IronbellyOrg/IronClaude --body "Phase 1 progress: <group id and name> committed on ironbelly/feat-codememory-codegraph-init at <short sha>. Tasks: <task ids>. Checks: <exact commands> -> <result>. Decisions logged: <count, path in task package>. Next: <next group>."`. Never use a bare `gh issue comment` and never `--repo SuperClaude-Org/...`. If `gh` is unauthenticated or fails, record the exact error and the intended body in `$PKG/progress.md` and continue (not a blocker).
- Decision rules (./source.md §10), never stop to ask the user: a simple decision (one obvious option, or one the source already constrains) is made by the executor and logged as one line in `$PKG/decisions.md` (decision, options, method `self`, rationale). A mid-level decision (two or more viable options with real trade-offs inside one task) writes each option to `$PKG/decisions/<task>-<slug>/option-<x>.md`, spawns an agent that runs `/sc:adversarial --compare <option files> --depth quick`, follows its recommendation and logs method `adversarial quick` with the merged-recommendation path. A complex decision (an architectural change to the source's design: retire-step scope, memory store layout, merge order, deleting a file the source keeps) does the same with `/sc:adversarial --compare <option files>` (standard depth) and logs method `adversarial full`.
- A blocked task stays blocked with its reason in `$PKG/progress.md`; continue with tasks that do not depend on it. If a task's acceptance fails, fix it within the task's files; if the fix needs a file another task owns, pull that edit forward and log it in `$PKG/decisions.md`. A task may not need a later task to go green.
- Scope limits (./source.md §2.1, §2.3): existing `.dev/` files outside `$PKG` are never edited; the only other `.dev/` writes are the new files `.dev/codegraph-migration/handoffs/phase3-codegraph-slots.md` and `.dev/codegraph-migration/handoffs/phase2-facts-from-phase1.md`, and each task that writes one stages that exact file (`git add <path>`, never the folder). No task uninstalls the `serena-agent` uv tool or removes `~/.local/bin/{serena,serena-agent,serena-hooks}`, the Coder `/usr/local/bin/codebase-memory-mcp` binary, bundle markers, upstream companions or `~/.local/bin/install.sh`; those are handed off, not removed by Phase 1.
- This plan was corrected after an advisory `/sc:reflect --mode pre` review (`.dev/codegraph-migration/review/F1-result.md`). Where a task's text here differs from `./source.md`, the task text wins.
- Human actions the executor must not attempt: merging Phases 1 and 2 to `master` (Phase 2's PR via `/sc:pr-submit`) and running the real `./update.sh` on a live workspace after that merge (Phase 2 owns that live check).
Start sha: 156a61f5900807917014d54f20609cacb84c7964
Diff against the start snapshot: Touched files: src/superclaude/cli/main.py, tests/cli/test_update_command.py, tests/cli/test_install_codebase_memory.py. Observed by the implementer (verify yourself): the Task 3 pytest command gives 272 passed; test_update_command.py collects 10 tests and test_install_codebase_memory.py collects 141 (inventory §4.2 expects 10 and 141). Inventory: .dev/codegraph-migration/inventory/codebase-memory.md §4.2 (lines 269-280). Output of git diff "$start" for the touched set follows.

diff --git a/src/superclaude/cli/main.py b/src/superclaude/cli/main.py
index b065ecde..8c4f63a7 100644
--- a/src/superclaude/cli/main.py
+++ b/src/superclaude/cli/main.py
@@ -35,21 +35,19 @@ def main():
 @click.option(
     "--force",
     is_flag=True,
-    help="Force reinstall framework files, never native upgrades or index resets",
+    help="Force reinstall framework files",
 )
 @click.option(
     "--list",
     "list_only",
     is_flag=True,
-    help="List framework components and native MCP status without installing",
+    help="List framework components without installing",
 )
 def install(target: str, force: bool, list_only: bool):
     """
     Install SuperClaude to Claude Code
 
-    Installs the framework to ~/.claude/ plus full user-level Codebase Memory
-    MCP setup on supported Linux systems. Native setup includes upstream's
-    detected-client/companion integrations and retains graph indexes.
+    Installs the framework to ~/.claude/.
 
     Examples:
         superclaude install
@@ -63,7 +61,6 @@ def install(target: str, force: bool, list_only: bool):
         list_installed_agents,
     )
     from .install_ccsession import wire_ccsession
-    from .install_codebase_memory import BINARY_NAME, discover_executable
     from .install_commands import (
         install_commands,
         list_available_commands,
@@ -75,12 +72,6 @@ def install(target: str, force: bool, list_only: bool):
         list_installed_core_files,
     )
     from .install_hooks import install_hooks
-    from .install_mcp import (
-        _native_registration_matches,
-        _native_selection_error,
-        install_codebase_memory_mcp,
-        read_user_mcp_entry,
-    )
     from .install_skill import list_available_skills
     from .install_skills import install_all_skills, list_installed_skills
     from .install_templates import (
@@ -158,32 +149,6 @@ def install(target: str, force: bool, list_only: bool):
         click.echo(
             f"\nTemplates: {len(templates_available)} available, {len(templates_installed)} installed"
         )
-        click.echo("\nCodebase Memory MCP (Linux amd64/arm64; user scope):")
-        unavailable = _native_selection_error("user")
-        found = None
-        if unavailable:
-            click.echo(f"   Native lifecycle unavailable: {unavailable}")
-        else:
-            found = discover_executable()
-            detail = f" at {found.executable}" if found.executable is not None else ""
-            if found.version is not None:
-                detail += f" ({found.version})"
-            click.echo(f"   Executable: {found.state}{detail}")
-        known, entry = read_user_mcp_entry(BINARY_NAME)
-        if not known:
-            registration = "unknown (read/parse failure; no repair attempted)"
-        elif entry is None:
-            registration = "absent"
-        elif (
-            found is not None
-            and found.state in {"canonical", "external"}
-            and found.executable is not None
-            and _native_registration_matches(entry, found.executable)
-        ):
-            registration = "matches verified executable (stdio, no arguments)"
-        else:
-            registration = "present but stale/unverified"
-        click.echo(f"   User registration: {registration}")
         return
 
     # Step 1: Install core framework files to ~/.claude/
@@ -251,16 +216,6 @@ def install(target: str, force: bool, list_only: bool):
     setup_success, setup_message = install_user_setup(force=force)
     click.echo(setup_message)
 
-    click.echo("\nInstalling Codebase Memory MCP (required user-level phase)...")
-    native_success, native_message = install_codebase_memory_mcp(scope="user")
-    click.echo(native_message)
-    if not native_success:
-        click.echo(
-            "Required Codebase Memory phase incomplete. Existing framework files were kept; "
-            "retry 'superclaude install' after addressing the reported stage.",
-            err=True,
-        )
-
     if (
         not core_success
         or not cmd_success
@@ -270,7 +225,6 @@ def install(target: str, force: bool, list_only: bool):
         or not hooks_success
         or not templates_success
         or not setup_success
-        or not native_success
     ):
         sys.exit(1)
 
diff --git a/tests/cli/test_install_codebase_memory.py b/tests/cli/test_install_codebase_memory.py
index 8537914d..0e9bc307 100644
--- a/tests/cli/test_install_codebase_memory.py
+++ b/tests/cli/test_install_codebase_memory.py
@@ -1,6 +1,5 @@
 """Isolated native acquisition tests; no upstream code is executed."""
 
-import json
 import os
 import subprocess
 import sys
@@ -1377,257 +1376,3 @@ def test_mcp_gateway_curl_preflight_before_any_selected_effects(
         )
         == before
     )
-
-
-@pytest.fixture(params=[False, True], ids=["default-config", "custom-config"])
-def cross_entry_lifecycle(isolated_home, tmp_path, monkeypatch, request):
-    """Keep coordinators/discovery/receipts real; intercept only process boundaries."""
-    from types import SimpleNamespace
-
-    from click.testing import CliRunner
-
-    from superclaude.cli import install_mcp
-    from superclaude.cli.main import main
-
-    monkeypatch.chdir(tmp_path)
-    if request.param:
-        config_dir = tmp_path / "custom Claude config"
-        config_dir.mkdir()
-        monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(config_dir))
-        config = config_dir / ".claude.json"
-    else:
-        monkeypatch.delenv("CLAUDE_CONFIG_DIR", raising=False)
-        config = isolated_home / ".claude.json"
-    cache = isolated_home / ".cache/codebase-memory-mcp"
-    monkeypatch.setenv("CBM_CACHE_DIR", str(cache))
-    root = {
-        "mcpServers": {
-            "codebase-memory-mcp-scout": {"command": "/keep/scout"},
-            "other-server": {"type": "http", "url": "https://keep.invalid"},
-        },
-        "projects": {
-            str(tmp_path): {
-                "mcpServers": {native.BINARY_NAME: {"command": "/keep/local"}}
-            }
-        },
-        "unrelated": {"preserve": [1, True, "value"]},
-    }
-    config.write_text(json.dumps(root))
-    keep = {
-        cache / "project.db": b"retained graph index",
-        isolated_home / ".claude/settings.json": b'{"hooks":{"keep":"unrelated hook"}}',
-        tmp_path
-        / ".mcp.json": b'{"mcpServers":{"codebase-memory-mcp":{"command":"/keep/project"}}}',
-    }
-    if request.param:
-        keep[isolated_home / ".claude.json"] = (
-            b'{"mcpServers":{"codebase-memory-mcp":{"command":"/keep/default-config"}}}'
-        )
-    for path, content in keep.items():
-        path.parent.mkdir(parents=True, exist_ok=True)
-        path.write_bytes(content)
-    calls, scripts, canonical = setup_acquisition(monkeypatch, isolated_home)
-    original_native_run = native._run_bounded
-    state = SimpleNamespace(
-        runner=CliRunner(),
-        main=main,
-        config=config,
-        root=root,
-        canonical=canonical,
-        updater=canonical.parent / "install.sh",
-        keep=keep,
-        native_calls=calls,
-        scripts=scripts,
-        claude_calls=[],
-        framework_calls=[],
-        downloads=0,
-        installs=0,
-        uninstalls=0,
-        uninstall_fails=False,
-    )
-
-    def native_process(argv, timeout, **kwargs):
-        if argv[0] == "/fixture/curl":
-            state.downloads += 1
-            return original_native_run(argv, timeout, **kwargs)
-        if argv[0] == "/fixture/bash":
-            state.installs += 1
-            print("fixture native installer invoked")
-            result = original_native_run(argv, timeout, **kwargs)
-            state.updater.write_bytes(b"upstream updater fixture")
-            return result
-        if argv == [str(canonical), "--version"]:
-            return original_native_run(argv, timeout, **kwargs)
-        assert argv == [str(canonical), "uninstall", "-y", f"--dir={canonical.parent}"]
-        assert timeout == native.INSTALL_TIMEOUT
-        state.uninstalls += 1
-        calls.append((argv, timeout, kwargs))
-        if state.uninstall_fails:
-            return subprocess.CompletedProcess(argv, 7, "", "mock native failure")
-        canonical.unlink()  # The upstream process boundary, not IronClaude cleanup.
-        return subprocess.CompletedProcess(argv, 0, "", "")
-
-    def claude_process(argv, **kwargs):
-        state.claude_calls.append(argv)
-        if argv == ["claude", "--version"]:
-            return subprocess.CompletedProcess(argv, 0, "Claude fixture", "")
-        assert argv[:3] in (["claude", "mcp", "add-json"], ["claude", "mcp", "remove"])
-        assert argv[3] == native.BINARY_NAME and argv[-2:] == ["--scope", "user"]
-        current = json.loads(config.read_text())
-        servers = current["mcpServers"]
-        if argv[2] == "add-json":
-            assert native.BINARY_NAME not in servers
-            servers[native.BINARY_NAME] = json.loads(argv[4])
-        else:
-            del servers[native.BINARY_NAME]
-        config.write_text(json.dumps(current))  # Mock scoped Claude CLI persistence.
-        return subprocess.CompletedProcess(argv, 0, "", "")
-
-    monkeypatch.setattr(native, "_run_bounded", native_process)
-    monkeypatch.setattr(install_mcp, "_run_command", claude_process)
-    monkeypatch.setattr(
-        install_mcp.click,
-        "confirm",
-        lambda *a, **k: pytest.fail("unexpected lifecycle confirmation"),
-    )
-    monkeypatch.setattr(
-        install_mcp.click,
-        "prompt",
-        lambda *a, **k: pytest.fail("unexpected lifecycle prompt"),
-    )
-    for module, function in (
-        ("install_core", "install_core_files"),
-        ("install_commands", "install_commands"),
-        ("install_agents", "install_agents"),
-        ("install_skills", "install_all_skills"),
-        ("install_ccsession", "wire_ccsession"),
-        ("install_hooks", "install_hooks"),
-        ("install_templates", "install_templates"),
-        ("install_user_setup", "install_user_setup"),
-    ):
-
-        def framework(*args, _name=function, **kwargs):
-            state.framework_calls.append(_name)
-            return True, f"{_name} fixture"
-
-        monkeypatch.setattr(f"superclaude.cli.{module}.{function}", framework)
-    return state
-
-
-def test_real_coordinators_cross_entry_lifecycle(cross_entry_lifecycle, isolated_home):
-    state = cross_entry_lifecycle
-    expected = {"type": "stdio", "command": str(state.canonical), "args": []}
-    result = state.runner.invoke(state.main, ["install"])
-    assert result.exit_code == 0, result.output
-    assert result.output.index(native.INSTALL_URL) < result.output.index(
-        "fixture native installer invoked"
-    )
-    assert str(state.canonical) in result.output and "account-wide" in result.output
-    assert "companion" in result.output and "indexes are retained" in result.output
-    assert state.framework_calls[-1] == "install_user_setup"
-    assert state.downloads == state.installs == 1
-    assert (
-        json.loads(state.config.read_text())["mcpServers"][native.BINARY_NAME]
-        == expected
-    )
-    receipt = native._receipt_path()
-    assert receipt.stat().st_mode & 0o777 == 0o600
-    assert json.loads(receipt.read_text())["identity"] == native._binary_identity(
-        state.canonical
-    )
-    for args in (["install", "--force"], ["mcp", "--servers", native.BINARY_NAME]):
-        result = state.runner.invoke(state.main, args)
-        assert result.exit_code == 0, result.output
-    assert state.downloads == state.installs == 1
-    assert (
-        sum(cmd[:3] == ["claude", "mcp", "add-json"] for cmd in state.claude_calls) == 1
-    )
-
-    # Remove only the user entry to exercise real cross-entry repair without a download.
-    root = json.loads(state.config.read_text())
-    del root["mcpServers"][native.BINARY_NAME]
-    state.config.write_text(json.dumps(root))
-    result = state.runner.invoke(state.main, ["mcp", "--servers", native.BINARY_NAME])
-    assert result.exit_code == 0, result.output
-    assert state.downloads == state.installs == 1
-    assert (
-        sum(cmd[:3] == ["claude", "mcp", "add-json"] for cmd in state.claude_calls) == 2
-    )
-
-    before_home = {
-        str(path.relative_to(isolated_home)): path.read_bytes()
-        for path in isolated_home.rglob("*")
-        if path.is_file()
-    }
-    before_config = state.config.read_bytes()
-    before_mutations = [
-        cmd for cmd in state.claude_calls if cmd[:2] == ["claude", "mcp"]
-    ]
-    for args in (
-        ["mcp", "--servers", native.BINARY_NAME, "--dry-run"],
-        ["mcp", "--servers", native.BINARY_NAME, "--uninstall", "--dry-run"],
-        ["install", "--list"],
-    ):
-        result = state.runner.invoke(state.main, args)
-        assert result.exit_code == 0, result.output
-    assert state.downloads == state.installs == 1 and state.uninstalls == 0
-    assert state.config.read_bytes() == before_config
-    assert {
-        str(path.relative_to(isolated_home)): path.read_bytes()
-        for path in isolated_home.rglob("*")
-        if path.is_file()
-    } == before_home
-    assert [
-        cmd for cmd in state.claude_calls if cmd[:2] == ["claude", "mcp"]
-    ] == before_mutations
-
-    result = state.runner.invoke(
-        state.main, ["mcp", "--servers", native.BINARY_NAME, "--uninstall", "--yes"]
-    )
-    assert result.exit_code == 0, result.output
-    assert (
-        state.uninstalls == 1 and not state.canonical.exists() and not receipt.exists()
-    )
-    assert json.loads(state.config.read_text()) == state.root
-    assert state.updater.read_bytes() == b"upstream updater fixture"
-    assert all(path.read_bytes() == content for path, content in state.keep.items())
-    before_update = (list(state.native_calls), list(state.claude_calls))
-    result = state.runner.invoke(state.main, ["update"])
-    assert result.exit_code == 0, result.output
-    assert (state.native_calls, state.claude_calls) == before_update
-    assert not state.canonical.exists() and not receipt.exists()
-    result = state.runner.invoke(state.main, ["install"])
-    assert result.exit_code == 0, result.output
-    assert state.downloads == state.installs == 2
-    assert state.canonical.is_file() and receipt.is_file()
-    assert (
-        json.loads(state.config.read_text())["mcpServers"][native.BINARY_NAME]
-        == expected
-    )
-    assert json.loads(receipt.read_text())["identity"] == native._binary_identity(
-        state.canonical
-    )
-    assert all(path.read_bytes() == content for path, content in state.keep.items())
-    assert all(not path.exists() and not path.parent.exists() for path in state.scripts)
-
-
-def test_real_coordinators_native_uninstall_failure_preserves_state(
-    cross_entry_lifecycle,
-):
-    state = cross_entry_lifecycle
-    result = state.runner.invoke(state.main, ["install"])
-    assert result.exit_code == 0, result.output
-    before_config = state.config.read_bytes()
-    before_proof = native._receipt_path().read_bytes()
-    state.uninstall_fails = True
-    result = state.runner.invoke(
-        state.main, ["mcp", "--servers", native.BINARY_NAME, "--uninstall", "--yes"]
-    )
-    assert result.exit_code == 1, result.output
-    assert "partial" in result.output.lower() and "retry" in result.output.lower()
-    assert state.uninstalls == 1 and state.downloads == state.installs == 1
-    assert state.canonical.is_file() and state.config.read_bytes() == before_config
-    assert native._receipt_path().read_bytes() == before_proof
-    assert not any(cmd[:3] == ["claude", "mcp", "remove"] for cmd in state.claude_calls)
-    assert state.updater.read_bytes() == b"upstream updater fixture"
-    assert all(path.read_bytes() == content for path, content in state.keep.items())
diff --git a/tests/cli/test_update_command.py b/tests/cli/test_update_command.py
index 7dd14ca4..6caffd0c 100644
--- a/tests/cli/test_update_command.py
+++ b/tests/cli/test_update_command.py
@@ -25,46 +25,17 @@ _INSTALLERS = (
 )
 
 
-_NATIVE_INSTALLER = "superclaude.cli.install_mcp.install_codebase_memory_mcp"
-
-
 @pytest.fixture(autouse=True)
-def native_phase_guard(tmp_path, monkeypatch):
-    from superclaude.cli import install_codebase_memory as native
-    from superclaude.cli import install_mcp, install_user_setup
+def isolated_home_guard(tmp_path, monkeypatch):
+    from superclaude.cli import install_user_setup
 
     home = tmp_path / "isolated-home"
     home.mkdir()
     monkeypatch.setenv("HOME", str(home))
     monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(home / "config"))
-    monkeypatch.setattr(native.platform, "system", lambda: "Linux")
-    monkeypatch.setattr(native.platform, "machine", lambda: "x86_64")
-    state = SimpleNamespace(
-        home=home, calls=[], found=native.Discovery("missing"), known=True, entry=None
-    )
-
-    def phase(*, scope):
-        state.calls.append({"scope": scope})
-        return True, "Codebase Memory shared phase fixture"
-
-    monkeypatch.setattr(install_mcp, "install_codebase_memory_mcp", phase)
-    monkeypatch.setattr(native, "discover_executable", lambda: state.found)
-    monkeypatch.setattr(
-        install_mcp, "read_user_mcp_entry", lambda name: (state.known, state.entry)
-    )
-    monkeypatch.setattr(
-        native,
-        "acquire_codebase_memory",
-        lambda **kwargs: pytest.fail("real native acquisition"),
-    )
-    monkeypatch.setattr(
-        native, "_run_bounded", lambda *a, **k: pytest.fail("real native process")
-    )
-    monkeypatch.setattr(
-        install_mcp, "_run_command", lambda *a, **k: pytest.fail("real Claude CLI")
-    )
+    state = SimpleNamespace(home=home)
     # The existing real-framework ccsession fixture must not download plugins or
-    # Orca skills while exercising the new mandatory native phase.
+    # Orca skills while exercising the real install.
     monkeypatch.setattr(
         install_user_setup, "install_plugins", lambda **kwargs: (True, "Plugin fixture")
     )
@@ -79,12 +50,10 @@ def native_phase_guard(tmp_path, monkeypatch):
 def _stub_installers(monkeypatch, *, failing: str | None = None):
     calls: list[str] = []
 
-    for path in (*_INSTALLERS, _NATIVE_INSTALLER):
+    for path in _INSTALLERS:
         name = path.rsplit(".", 1)[-1]
 
         def fake(*args, _name=name, **kwargs):
-            if _name == "install_codebase_memory_mcp":
-                assert not args and kwargs == {"scope": "user"}
             calls.append(_name)
             return (_name != failing, f"{_name} result")
 
@@ -135,7 +104,6 @@ def test_install_wires_before_hooks_and_templates(monkeypatch):
         "install_hooks",
         "install_templates",
         "install_user_setup",
-        "install_codebase_memory_mcp",
     ]
 
 
@@ -248,106 +216,10 @@ def test_real_update_restores_packaged_ccsession(native_install):
     assert "private-token" not in result.output
 
 
-@pytest.mark.parametrize(
-    "stage", ["download", "verification", "registration", "platform"]
-)
-def test_install_native_failure_is_mandatory_and_preserves_framework_work(
-    monkeypatch, native_phase_guard, stage
-):
-    calls = _stub_installers(monkeypatch)
-    marker = native_phase_guard.home / "framework-work-kept"
-
-    def core(*, force):
-        calls.append("install_core_files")
-        marker.write_text("existing successful framework phase")
-        return True, "framework phase completed"
-
-    def native_phase(*, scope):
-        assert scope == "user"
-        calls.append("install_codebase_memory_mcp")
-        return False, f"Native {stage} fixture failure"
-
-    monkeypatch.setattr("superclaude.cli.install_core.install_core_files", core)
-    monkeypatch.setattr(_NATIVE_INSTALLER, native_phase)
-    result = CliRunner().invoke(main, ["install"])
-    assert result.exit_code == 1, result.output
-    assert stage in result.output and "incomplete" in result.output.lower()
-    assert "retry" in result.output.lower() and "superclaude install" in result.output
-    assert marker.read_text() == "existing successful framework phase"
-    assert calls[-2:] == ["install_user_setup", "install_codebase_memory_mcp"]
-
-
-@pytest.mark.parametrize(
-    "state,registration,expected",
-    [
-        ("canonical", "matching", "matches verified"),
-        ("external", "matching", "external"),
-        ("canonical", "stale", "stale"),
-        ("canonical", "absent", "absent"),
-        ("missing", "absent", "missing"),
-        ("non_runnable", "absent", "non_runnable"),
-        ("ambiguous", "absent", "ambiguous"),
-        ("canonical", "unknown", "unknown"),
-    ],
-)
-def test_install_list_reports_native_and_exact_user_status_without_repair(
-    monkeypatch, native_phase_guard, state, registration, expected
-):
-    from superclaude.cli import install_codebase_memory as native
-
-    calls = _stub_installers(monkeypatch)
-    _stub_listings(monkeypatch)
-    executable = native_phase_guard.home / ".local/bin/codebase-memory-mcp"
-    native_phase_guard.found = native.Discovery(
-        state, executable, "0.12.1" if state in {"canonical", "external"} else None
-    )
-    native_phase_guard.known = registration != "unknown"
-    if registration in {"matching", "stale"}:
-        native_phase_guard.entry = {
-            "type": "stdio",
-            "command": str(executable),
-            "args": [] if registration == "matching" else ["--stale"],
-        }
-    before = sorted(str(path) for path in native_phase_guard.home.rglob("*"))
-    result = CliRunner().invoke(
-        main,
-        [
-            "install",
-            "--list",
-            "--force",
-            "--target",
-            str(native_phase_guard.home / "unused-target"),
-        ],
-    )
-    assert result.exit_code == 0, result.output
-    assert "Codebase Memory MCP" in result.output and expected in result.output
-    assert "User registration" in result.output
-    assert calls == [] and native_phase_guard.calls == []
-    assert sorted(str(path) for path in native_phase_guard.home.rglob("*")) == before
-
-
-def test_install_list_reports_unsupported_native_without_probe(
-    monkeypatch, native_phase_guard
-):
-    from superclaude.cli import install_codebase_memory as native
-
-    calls = _stub_installers(monkeypatch)
-    _stub_listings(monkeypatch)
-    monkeypatch.setattr(native.platform, "system", lambda: "Darwin")
-    monkeypatch.setattr(
-        native, "discover_executable", lambda: pytest.fail("unsupported native probe")
-    )
-    result = CliRunner().invoke(main, ["install", "--list"])
-    assert result.exit_code == 0 and "unavailable" in result.output.lower()
-    assert "Linux" in result.output and calls == []
-
-
-def test_install_force_target_do_not_redirect_or_force_native(
-    monkeypatch, native_phase_guard
-):
+def test_install_force_target_do_not_redirect(monkeypatch, isolated_home_guard):
     _stub_installers(monkeypatch)
     captured = {}
-    target = native_phase_guard.home / "custom commands"
+    target = isolated_home_guard.home / "custom commands"
 
     def commands(*, target_path, force):
         captured["commands"] = (target_path, force)
@@ -357,68 +229,13 @@ def test_install_force_target_do_not_redirect_or_force_native(
         captured["setup"] = force
         return True, "setup fixture"
 
-    def native_phase(*, scope):
-        captured["native"] = {"scope": scope}
-        return True, "native fixture"
-
     monkeypatch.setattr("superclaude.cli.install_commands.install_commands", commands)
     monkeypatch.setattr(
         "superclaude.cli.install_user_setup.install_user_setup", user_setup
     )
-    monkeypatch.setattr(_NATIVE_INSTALLER, native_phase)
     result = CliRunner().invoke(main, ["install", "--force", "--target", str(target)])
     assert result.exit_code == 0, result.output
     assert captured == {
         "commands": (target, True),
         "setup": True,
-        "native": {"scope": "user"},
     }
-
-
-@pytest.mark.parametrize(
-    "shared_result",
-    [
-        "Already correct; no-op",
-        "Missing user registration repaired without acquisition",
-        "External binary reused without replacement",
-    ],
-)
-def test_repeated_install_delegates_shared_noop_repair_external_policy(
-    monkeypatch, native_phase_guard, shared_result
-):
-    _stub_installers(monkeypatch)
-    external = native_phase_guard.home / "external manager" / "codebase-memory-mcp"
-    external.parent.mkdir()
-    external.write_bytes(b"external installation sentinel")
-    calls = []
-
-    def native_phase(*, scope):
-        calls.append({"scope": scope})
-        return True, shared_result
-
-    monkeypatch.setattr(_NATIVE_INSTALLER, native_phase)
-    for flags in ([], ["--force"]):
-        result = CliRunner().invoke(main, ["install", *flags])
-        assert result.exit_code == 0 and shared_result in result.output
-    assert calls == [{"scope": "user"}, {"scope": "user"}]
-    assert external.read_bytes() == b"external installation sentinel"
-
-
-def test_update_never_restores_native_but_later_install_calls_shared_phase(
-    monkeypatch, native_phase_guard
-):
-    from superclaude.cli import install_codebase_memory as native
-
-    calls = _stub_installers(monkeypatch)
-    monkeypatch.setattr(
-        native,
-        "discover_executable",
-        lambda: pytest.fail("native discovery during update"),
-    )
-    result = CliRunner().invoke(main, ["update"])
-    assert result.exit_code == 0
-    assert calls == [path.rsplit(".", 1)[-1] for path in _INSTALLERS]
-    assert not (native_phase_guard.home / ".local/bin/codebase-memory-mcp").exists()
-    calls.clear()
-    result = CliRunner().invoke(main, ["install"])
-    assert result.exit_code == 0 and calls[-1] == "install_codebase_memory_mcp"
Delta diff from the previous reviewed tree (empty on the first review): (empty)
Earlier blocking findings of this start (empty on the first review): (empty)
Saved-probe re-check hit locations (may be empty): (none)

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
