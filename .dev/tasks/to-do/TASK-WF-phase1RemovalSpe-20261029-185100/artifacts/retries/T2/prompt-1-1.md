c407ddfe63775b976d98019a4f845433437c907e
Review one task for spec compliance.

Task brief: ## Task 2: Port the generic `superclaude mcp` tests to a new test file

Depends on: Task 1

Implements ./source.md §8 T1 and row C4. Create `tests/cli/test_install_mcp_cli.py` exactly per `.dev/codegraph-migration/inventory/codebase-memory.md` §4.1: its own home fixture and an `mcp_cli` fixture without any `native`/`install_codebase_memory_mcp` patching; port the 11 tests listed there (971 without the `--uninstall`/`--yes` cases, 1126, 1195, 1217, 1229, 1274, 1285, 1298, 1306, 1114 with `context7` instead of codebase-memory, 1334 gateway part only). The 5 menu/message tests (990, 1001, 1023, 1034, 1049) wait for Task 5. Commit `test(mcp): port generic superclaude mcp tests out of the codebase-memory suite (#323)`.

Acceptance criteria:
- T2.AC1: `uv run pytest tests/cli/test_install_mcp_cli.py -q -p no:cacheprovider` passes.
- T2.AC2: `uv run pytest tests/cli/test_install_codebase_memory.py tests/cli/test_install_mcp_registry.py tests/cli/test_install_mcp_tavily.py tests/cli/test_update_command.py tests/docs/test_tavily_doc_alignment.py -q -p no:cacheprovider` still shows the counts in `$PKG/artifacts/baseline/cbm.txt`.

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
Start sha: c407ddfe63775b976d98019a4f845433437c907e
Diff against the start snapshot: Touched files: tests/cli/test_install_mcp_cli.py (new, untracked). Tracked diff of the touched set vs start: none. Full new-file contents follow; the source being ported is tests/cli/test_install_codebase_memory.py:834-1380, and the porting rules are .dev/codegraph-migration/inventory/codebase-memory.md section 4.1 and 1.4.

diff --git a/tests/cli/test_install_mcp_cli.py b/tests/cli/test_install_mcp_cli.py
new file mode 100644
index 00000000..704f8902
--- /dev/null
+++ b/tests/cli/test_install_mcp_cli.py
@@ -0,0 +1,271 @@
+"""Generic ``superclaude mcp`` command tests; no external process is ever run."""
+
+import subprocess
+
+import pytest
+
+
+@pytest.fixture(autouse=True)
+def isolated_home(tmp_path, monkeypatch):
+    home = tmp_path / "test home"
+    home.mkdir()
+    monkeypatch.setenv("HOME", str(home))
+    monkeypatch.setenv("PATH", "")
+    return home
+
+
+@pytest.fixture
+def mcp_cli(monkeypatch, isolated_home):
+    from types import SimpleNamespace
+
+    from click.testing import CliRunner
+
+    from superclaude.cli import install_mcp
+    from superclaude.cli.main import main
+
+    config = isolated_home / "cli config"
+    config.mkdir()
+    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(config))
+    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
+    monkeypatch.delenv("MORPH_API_KEY", raising=False)
+    state = SimpleNamespace(
+        runner=CliRunner(),
+        main=main,
+        module=install_mcp,
+        interactive=False,
+        calls=[],
+        processes=[],
+        gateway_ok=True,
+        claude_ok=True,
+        docker_ok=True,
+        node_version="v20.0.0",
+        auggie_version="auggie 0.36.0",
+        missing_tools=set(),
+        real_gateway=install_mcp.install_airis_gateway,
+    )
+    monkeypatch.setattr(
+        install_mcp, "_is_interactive", lambda: state.interactive, raising=False
+    )
+    monkeypatch.setattr(
+        install_mcp.shutil,
+        "which",
+        lambda name: None if name in state.missing_tools else f"/fixture/{name}",
+    )
+    monkeypatch.setattr(install_mcp, "check_mcp_server_installed", lambda name: False)
+
+    def command(argv, **kwargs):
+        state.processes.append(argv)
+        if argv == ["claude", "--version"]:
+            return subprocess.CompletedProcess(
+                argv, 0 if state.claude_ok else 1, "fixture", ""
+            )
+        if argv == ["node", "--version"]:
+            return subprocess.CompletedProcess(
+                argv, 0 if state.node_version else 1, state.node_version or "", ""
+            )
+        if argv == ["docker", "info"]:
+            return subprocess.CompletedProcess(
+                argv, 0 if state.docker_ok else 1, "", ""
+            )
+        if argv == ["auggie", "--version"]:
+            return subprocess.CompletedProcess(argv, 0, state.auggie_version, "")
+        if argv == ["uv", "--version"]:
+            return subprocess.CompletedProcess(argv, 0, "uv fixture", "")
+        if len(argv) == 2 and argv[0] in {"npx", "npm"} and argv[1] == "--version":
+            return subprocess.CompletedProcess(
+                argv, 1 if argv[0] in state.missing_tools else 0, "fixture version", ""
+            )
+        if argv[:3] == ["claude", "mcp", "add"]:
+            return subprocess.CompletedProcess(argv, 0, "", "")
+        if argv[:3] == ["claude", "mcp", "get"]:
+            return subprocess.CompletedProcess(
+                argv,
+                0,
+                "tavily:\n  Scope: User config\n  Command: npx\n  Args: -y tavily-mcp@0.1.2\n",
+                "",
+            )
+        pytest.fail(f"Unexpected external command: {argv}")
+
+    def gateway(dry_run=False):
+        state.calls.append(("gateway", dry_run))
+        return state.gateway_ok
+
+    monkeypatch.setattr(install_mcp, "_run_command", command)
+    monkeypatch.setattr(install_mcp, "install_airis_gateway", gateway)
+    return state
+
+
+@pytest.mark.parametrize(
+    "extra",
+    [
+        ["--dry-run"],
+        ["--servers", "context7"],
+        ["--scope", "project"],
+    ],
+)
+def test_mcp_list_rejects_incompatible_modes_before_lookup(mcp_cli, monkeypatch, extra):
+    monkeypatch.setattr(
+        mcp_cli.module,
+        "list_available_servers",
+        lambda: pytest.fail("list lookup before option validation"),
+    )
+    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp", "--list", *extra])
+    assert result.exit_code != 0 and mcp_cli.calls == [] and mcp_cli.processes == []
+
+
+def test_mcp_unknown_mixed_selection_rejected_before_any_prerequisites(mcp_cli):
+    result = mcp_cli.runner.invoke(
+        mcp_cli.main, ["mcp", "-s", "context7", "-s", "unknown"]
+    )
+    assert result.exit_code != 0 and "unknown" in result.output
+    assert mcp_cli.calls == [] and mcp_cli.processes == []
+
+
+@pytest.mark.parametrize(
+    "selection,version,minimum",
+    [("context7", "v17.0.0", "18"), ("auggie", "v19.0.0", "20")],
+)
+def test_mcp_selected_npm_node_minimum_before_any_install(
+    mcp_cli, selection, version, minimum
+):
+    mcp_cli.node_version = version
+    result = mcp_cli.runner.invoke(
+        mcp_cli.main, ["mcp", "-s", "airis-mcp-gateway", "-s", selection]
+    )
+    assert result.exit_code != 0 and minimum in result.output
+    assert mcp_cli.calls == []
+
+
+@pytest.mark.parametrize("server", ["tavily", "auggie"])
+def test_mcp_dry_run_api_key_and_binary_paths_never_prompt_or_mutate(
+    mcp_cli, monkeypatch, server
+):
+    monkeypatch.setattr(
+        mcp_cli.module.click,
+        "confirm",
+        lambda *a, **k: pytest.fail("dry-run confirmation"),
+    )
+    monkeypatch.setattr(
+        mcp_cli.module.click,
+        "prompt",
+        lambda *a, **k: pytest.fail("dry-run key prompt"),
+    )
+    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp", "-s", server, "--dry-run"])
+    assert result.exit_code == 0, result.output
+    assert not any(
+        cmd[:3] in (["claude", "mcp", "add"], ["claude", "mcp", "remove"])
+        or cmd[0] in {"npm", "curl"}
+        for cmd in mcp_cli.processes
+    )
+
+
+def test_mcp_dry_run_stale_registration_does_not_remove(mcp_cli, monkeypatch):
+    monkeypatch.setattr(mcp_cli.module, "check_mcp_server_installed", lambda name: True)
+    monkeypatch.setattr(
+        mcp_cli.module.click,
+        "confirm",
+        lambda *a, **k: pytest.fail("dry-run confirmation"),
+    )
+    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp", "-s", "tavily", "--dry-run"])
+    assert result.exit_code == 0 and "re-register" in result.output
+    assert mcp_cli.processes == [["claude", "mcp", "get", "tavily"]]
+
+
+def test_mcp_gateway_dry_run_needs_no_docker_and_writes_nothing(
+    mcp_cli, monkeypatch, isolated_home
+):
+    mcp_cli.docker_ok = False
+    monkeypatch.setattr(mcp_cli.module, "install_airis_gateway", mcp_cli.real_gateway)
+    result = mcp_cli.runner.invoke(
+        mcp_cli.main, ["mcp", "-s", "airis-mcp-gateway", "--dry-run"]
+    )
+    assert result.exit_code == 0, result.output
+    assert mcp_cli.processes == [] and not (isolated_home / ".superclaude").exists()
+
+
+@pytest.mark.parametrize("server,tool", [("context7", "npx"), ("auggie", "npm")])
+def test_mcp_missing_selected_package_tool_prevents_all_effects(mcp_cli, server, tool):
+    mcp_cli.missing_tools = {tool}
+    mcp_cli.auggie_version = "auggie 0.35.0"
+    result = mcp_cli.runner.invoke(
+        mcp_cli.main, ["mcp", "-s", "airis-mcp-gateway", "-s", server]
+    )
+    assert result.exit_code != 0 and tool in result.output
+    assert mcp_cli.calls == []
+
+
+@pytest.mark.parametrize("scope", ["project", "local"])
+def test_mcp_other_servers_retain_requested_scope(mcp_cli, monkeypatch, scope):
+    monkeypatch.setattr(mcp_cli.module, "prompt_for_api_key", lambda *a, **k: None)
+    result = mcp_cli.runner.invoke(
+        mcp_cli.main, ["mcp", "-s", "tavily", "--scope", scope]
+    )
+    assert result.exit_code == 0, result.output
+    add = next(cmd for cmd in mcp_cli.processes if cmd[:3] == ["claude", "mcp", "add"])
+    if scope == "project":
+        assert add[add.index("--scope") + 1] == "project"
+    else:
+        assert "--scope" not in add  # Legacy local default remains unchanged.
+
+
+def test_mcp_invalid_menu_number_does_not_install_partial_valid_selection(mcp_cli):
+    mcp_cli.interactive = True
+    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp"], input="1\n1,999\n")
+    assert result.exit_code != 0 and "Invalid selection" in result.output
+    assert mcp_cli.calls == [] and mcp_cli.processes == []
+
+
+@pytest.mark.parametrize("missing", ["claude", "docker"])
+def test_mcp_readiness_failure_prevents_all_mixed_install_effects(mcp_cli, missing):
+    mcp_cli.claude_ok = missing != "claude"
+    mcp_cli.docker_ok = missing != "docker"
+    result = mcp_cli.runner.invoke(
+        mcp_cli.main, ["mcp", "-s", "context7", "-s", "airis-mcp-gateway"]
+    )
+    assert result.exit_code != 0 and mcp_cli.calls == []
+
+
+@pytest.mark.parametrize("dry_run", [False, True])
+def test_mcp_gateway_curl_preflight_before_any_selected_effects(
+    mcp_cli, isolated_home, monkeypatch, dry_run
+):
+    mcp_cli.missing_tools = {"curl"}
+    monkeypatch.setattr(mcp_cli.module, "install_airis_gateway", mcp_cli.real_gateway)
+    original = mcp_cli.module._run_command
+
+    def command(argv, **kwargs):
+        if argv[0] == "curl":
+            mcp_cli.processes.append(argv)
+            return subprocess.CompletedProcess(argv, 127, "", "curl not found")
+        return original(argv, **kwargs)
+
+    monkeypatch.setattr(mcp_cli.module, "_run_command", command)
+    before = sorted(
+        str(path.relative_to(isolated_home)) for path in isolated_home.rglob("*")
+    )
+    args = ["mcp", "--servers", "airis-mcp-gateway"]
+    if dry_run:
+        args.append("--dry-run")
+    result = mcp_cli.runner.invoke(mcp_cli.main, args)
+    assert result.exit_code == (0 if dry_run else 1), result.output
+    if not dry_run:
+        assert "curl" in result.output and mcp_cli.calls == []
+    else:
+        assert "DRY RUN" in result.output
+    assert not any(
+        cmd[0] == "curl"
+        or cmd[:3]
+        in (
+            ["claude", "mcp", "add"],
+            ["claude", "mcp", "add-json"],
+            ["claude", "mcp", "remove"],
+        )
+        for cmd in mcp_cli.processes
+    )
+    assert not (isolated_home / ".superclaude").exists()
+    assert (
+        sorted(
+            str(path.relative_to(isolated_home)) for path in isolated_home.rglob("*")
+        )
+        == before
+    )
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
