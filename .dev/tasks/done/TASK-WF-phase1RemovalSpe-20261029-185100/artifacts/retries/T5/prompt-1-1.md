01dfbead33b83ec88fc2769a69d90847b8e6e6a1
Review one task for spec compliance.

Task brief: ## Task 5: Detach `superclaude mcp` and the MCP registry from codebase-memory

Depends on: Task 4

Implements ./source.md §8 T4, rows C2, C5, C6 and the §7 `install_mcp.py` row. Apply `.dev/codegraph-migration/inventory/codebase-memory.md` §4.3 to `src/superclaude/cli/main.py` and `src/superclaude/cli/install_mcp.py`: delete `--uninstall`/`--yes`, the native blocks listed under row C2 (including `_cleanup_user_native_registration` at `:916-948`, together with its caller `uninstall_codebase_memory_mcp`), and make the menu "1. Install MCP servers (default)" / "2. Cancel"; keep `read_user_mcp_entry`, `_run_registration_command` and the Task 4 remover. In tests: delete `tests/cli/test_install_codebase_memory.py` lines 834-1380, `tests/cli/test_install_mcp_tavily.py` 382-end (keep 1-375), `tests/cli/test_install_mcp_registry.py` 192-240 (the 3 tests named in row C5); port the 5 deferred menu/message tests into `tests/cli/test_install_mcp_cli.py` and add one `mcp --list` output test; add `"codebase-memory-mcp"` to the `test_removed_mcp_servers_are_not_in_registry` tuple. Commit `feat(mcp)!: remove codebase-memory-mcp from the MCP registry and drop --uninstall/--yes (#323)`.

Acceptance criteria:
- T5.AC1: `uv run pytest tests/cli/test_install_mcp_cli.py tests/cli/test_install_mcp_registry.py tests/cli/test_install_mcp_tavily.py tests/cli/test_install_codebase_memory.py tests/cli/test_update_command.py tests/cli/test_install_retired_mcp.py tests/docs/test_tavily_doc_alignment.py tests/recommend -q -p no:cacheprovider` passes.
- T5.AC2: `rg -n "codebase_memory|_native_|install_codebase_memory_mcp|uninstall_codebase_memory_mcp|--uninstall|--yes" src/superclaude/cli/main.py src/superclaude/cli/install_mcp.py` prints nothing.

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
Start sha: 01dfbead33b83ec88fc2769a69d90847b8e6e6a1
Diff against the start snapshot: Touched files: src/superclaude/cli/main.py, src/superclaude/cli/install_mcp.py, tests/cli/test_install_codebase_memory.py, tests/cli/test_install_mcp_tavily.py, tests/cli/test_install_mcp_registry.py, tests/cli/test_install_mcp_cli.py. Spec: $PKG/source.md section 8 T4 and .dev/codegraph-migration/inventory/codebase-memory.md section 4.3 and rows C2, C5, C6, plus the plan's Task 5 text. Observed by the implementer (verify yourself): the Task 5 pytest command gives 534 passed, 1 skipped; the rg check prints nothing. Test files lose large blocks (stat below); read them from disk and use git diff yourself for the deleted ranges.

 src/superclaude/cli/install_mcp.py        | 391 ++---------------
 src/superclaude/cli/main.py               |  31 +-
 tests/cli/test_install_codebase_memory.py | 548 ------------------------
 tests/cli/test_install_mcp_cli.py         |  63 +++
 tests/cli/test_install_mcp_registry.py    |  57 +--
 tests/cli/test_install_mcp_tavily.py      | 677 ------------------------------
 6 files changed, 107 insertions(+), 1660 deletions(-)

diff --git a/src/superclaude/cli/install_mcp.py b/src/superclaude/cli/install_mcp.py
index 61c11bcf..750bd395 100644
--- a/src/superclaude/cli/install_mcp.py
+++ b/src/superclaude/cli/install_mcp.py
@@ -20,8 +20,6 @@ from typing import Dict, List, Optional, Tuple
 
 import click
 
-from superclaude.cli import install_codebase_memory as codebase_memory
-
 # AIRIS MCP Gateway - Unified MCP solution (recommended)
 AIRIS_GATEWAY = {
     "name": "airis-mcp-gateway",
@@ -100,14 +98,6 @@ MCP_SERVERS = {
             "      Docs: https://docs.augmentcode.com/context-services/mcp/quickstart-claude-code"
         ),
     },
-    "codebase-memory-mcp": {
-        "name": "codebase-memory-mcp",
-        "description": "Native codebase graph memory with full upstream companion setup",
-        "transport": "stdio",
-        "command": "codebase-memory-mcp",
-        "args": [],
-        "required": False,
-    },
 }
 
 
@@ -485,26 +475,6 @@ def _is_interactive() -> bool:
     return sys.stdin.isatty()
 
 
-def _native_selection_error(scope: str) -> Optional[str]:
-    if scope != "user":
-        return "Codebase Memory full native lifecycle supports user scope only."
-    if platform.system() != "Linux" or platform.machine().lower() not in {
-        "amd64",
-        "x86_64",
-        "arm64",
-        "aarch64",
-    }:
-        return "Automated Codebase Memory lifecycle requires Linux amd64/arm64; use the official manual mechanism on other platforms."
-    return None
-
-
-def _native_lifecycle_notice() -> str:
-    return (
-        f"Upstream source: {codebase_memory.INSTALL_URL}. Native location: {codebase_memory.canonical_executable()}. "
-        "This user/account-wide lifecycle affects detected clients and companion instructions, skills, agents and hooks; graph indexes are retained."
-    )
-
-
 def check_prerequisites(
     selected_servers: Optional[List[str]] = None,
 ) -> Tuple[bool, List[str]]:
@@ -570,19 +540,6 @@ def check_prerequisites(
                 click.echo("uv not found - required to run Serena MCP server", err=True)
         except (OSError, subprocess.SubprocessError):
             click.echo("uv not found - required to run Serena MCP server", err=True)
-    if codebase_memory.BINARY_NAME in selected:
-        found = codebase_memory.discover_executable()
-        if found.state == "ambiguous" or (
-            found.state == "non_runnable"
-            and found.executable != codebase_memory.canonical_executable()
-        ):
-            errors.append(
-                "Native executable discovery is ambiguous or externally non-runnable; resolve it before installation"
-            )
-        elif found.state not in {"canonical", "external"}:
-            for tool in ("curl", "bash"):
-                if shutil.which(tool) is None:
-                    errors.append(f"{tool} is required for missing native acquisition")
     return not errors, errors
 
 
@@ -756,15 +713,6 @@ def read_user_mcp_entry(server_name: str) -> tuple[bool, dict | None]:
         return False, None
 
 
-def _native_registration_matches(entry: dict | None, executable: Path) -> bool:
-    return bool(
-        entry is not None
-        and entry.get("type", "stdio") == "stdio"
-        and entry.get("command") == str(executable)
-        and entry.get("args", []) == []
-    )
-
-
 def _run_registration_command(cmd: list[str]) -> bool:
     """Do not expose Claude output/exception argv, which can contain old secrets."""
     try:
@@ -774,182 +722,6 @@ def _run_registration_command(cmd: list[str]) -> bool:
         return False
 
 
-def _add_user_native_entry(entry: dict) -> bool:
-    return _run_registration_command(
-        [
-            "claude",
-            "mcp",
-            "add-json",
-            codebase_memory.BINARY_NAME,
-            json.dumps(entry),
-            "--scope",
-            "user",
-        ]
-    )
-
-
-def _restore_user_native_entry(previous: dict, attempted: dict) -> bool:
-    known, current = read_user_mcp_entry(codebase_memory.BINARY_NAME)
-    if not known:
-        return False
-    if current == previous:
-        return True
-    if current is not None:
-        # A timed-out add may have written our entry. Do not overwrite a third
-        # party's concurrent edit when its contents cannot be attributed to us.
-        if current != attempted or not _run_registration_command(
-            [
-                "claude",
-                "mcp",
-                "remove",
-                codebase_memory.BINARY_NAME,
-                "--scope",
-                "user",
-            ]
-        ):
-            return False
-    if not _add_user_native_entry(previous):
-        return False
-    known, current = read_user_mcp_entry(codebase_memory.BINARY_NAME)
-    return known and current == previous
-
-
-def install_codebase_memory_mcp(
-    *, scope: str = "user", dry_run: bool = False
-) -> tuple[bool, str]:
-    """Shared native install/register boundary for framework and MCP callers."""
-    invalid = _native_selection_error(scope)
-    if invalid:
-        return False, invalid
-    if dry_run:
-        return (
-            True,
-            "[DRY RUN] "
-            + _native_lifecycle_notice()
-            + " Would reuse a usable executable or acquire full upstream setup if missing, then ensure exact user stdio registration. No changes made.",
-        )
-    try:
-        ready = _run_command(
-            ["claude", "--version"], capture_output=True, text=True, timeout=10
-        )
-        if ready is None or ready.returncode != 0:
-            return (
-                False,
-                "Prerequisites: Claude CLI is unavailable; acquisition was not started.",
-            )
-    except (OSError, subprocess.SubprocessError):
-        return (
-            False,
-            "Prerequisites: Claude CLI readiness failed; acquisition was not started.",
-        )
-
-    click.echo(_native_lifecycle_notice())
-    click.echo("Acquisition: preparing Codebase Memory through the native helper.")
-    acquired = codebase_memory.acquire_codebase_memory(scope=scope)
-    if not acquired.success:
-        return False, f"Acquisition ({acquired.stage}) failed: {acquired.message}"
-    executable = acquired.executable
-    if executable is None or not executable.is_absolute() or not acquired.version:
-        return (
-            False,
-            "Executable verification: native helper did not provide an absolute executable and version.",
-        )
-    click.echo(f"Executable verification: {acquired.version} at {executable}")
-
-    known, previous = read_user_mcp_entry(codebase_memory.BINARY_NAME)
-    if not known:
-        return (
-            False,
-            "Registration lookup failed: cannot establish the exact user entry; no registration reconciliation was attempted.",
-        )
-    success_message = f"Registration: exact user stdio entry verified ({acquired.version}). Restart clients to load integrations; no indexing or live MCP handshake was performed."
-    if _native_registration_matches(previous, executable):
-        return True, success_message
-    expected = {"type": "stdio", "command": str(executable), "args": []}
-    if previous is not None and (previous.get("env") or previous.get("headers")):
-        # Restoring this entry would put its values on a process command line
-        # (`claude mcp add-json` takes JSON only as an argument), so never replace it.
-        return (
-            False,
-            "Registration: the existing user codebase-memory-mcp entry has env or headers values, so it was not replaced. Update it by hand or remove it with `claude mcp remove codebase-memory-mcp --scope user`, then retry.",
-        )
-    if previous is not None and not _run_registration_command(
-        [
-            "claude",
-            "mcp",
-            "remove",
-            codebase_memory.BINARY_NAME,
-            "--scope",
-            "user",
-        ]
-    ):
-        # A failed or timed-out remove may still have persisted; only `previous`
-        # is attributable to us here, so never remove an entry that differs from it.
-        if _restore_user_native_entry(previous, previous):
-            return (
-                False,
-                "Registration removal failed; previous user registration is intact. No replacement was attempted.",
-            )
-        return (
-            False,
-            "Registration removal failed; restoration failed. User registration may be partial; inspect it before retrying.",
-        )
-    added = _add_user_native_entry(expected)
-    known, current = read_user_mcp_entry(codebase_memory.BINARY_NAME)
-    if added and known and _native_registration_matches(current, executable):
-        return True, success_message
-    failure = "Registration verification failed" if added else "Registration add failed"
-    if previous is not None:
-        if _restore_user_native_entry(previous, expected):
-            return (
-                False,
-                f"{failure}; previous user registration restored. Retry the installation.",
-            )
-        return (
-            False,
-            f"{failure}; restoration failed. User registration may be partial; inspect it before retrying.",
-        )
-    return (
-        False,
-        f"{failure}; user registration may be partial. Inspect it before retrying.",
-    )
-
-
-def _cleanup_user_native_registration() -> tuple[bool, str]:
-    known, entry = read_user_mcp_entry(codebase_memory.BINARY_NAME)
-    if not known:
-        return (
-            False,
-            "Registration lookup failed; possible partial removal. Inspect user configuration before retrying.",
-        )
-    if entry is None:
-        return True, "Exact user registration is absent."
-    if not _run_registration_command(
-        [
-            "claude",
-            "mcp",
-            "remove",
-            codebase_memory.BINARY_NAME,
-            "--scope",
-            "user",
-        ]
-    ):
-        return (
-            False,
-            "User registration cleanup failed; possible partial removal. Inspect it before retrying.",
-        )
-    known, entry = read_user_mcp_entry(codebase_memory.BINARY_NAME)
-    if not known or entry is not None:
-        return (
-            False,
-            "User registration absence could not be verified; possible partial removal. Inspect it before retrying.",
-        )
-    return (
-        True,
-        "Exact user registration removed; other scopes were not changed by IronClaude.",
-    )
-
-
 def _exec_claude(argv: list[str], timeout: float) -> int:
     """Run ``claude`` directly (no shell) in its own session; kill the group on timeout.
 
@@ -1022,65 +794,6 @@ def _remove_exact_user_entry(
     return "unverified" if matcher(after) else "replaced"
 
 
-def uninstall_codebase_memory_mcp(
-    *, scope: str = "user", confirmed: bool = False, dry_run: bool = False
-) -> tuple[bool, str]:
-    """Account-wide native removal, then exact-user residual cleanup, with no prompts."""
-    if scope != "user":
-        return False, "Full Codebase Memory removal supports user scope only."
-    preview = codebase_memory.preview_codebase_memory_removal()
-    if preview.state not in {"ready", "missing"}:
-        return False, preview.message
-    known, entry = read_user_mcp_entry(codebase_memory.BINARY_NAME)
-    if not known:
-        return (
-            False,
-            "Registration lookup failed before removal; no native removal or registration cleanup was attempted.",
-        )
-    partial = "Registration-only partial cleanup: companion assets were not audited or removed; indexes and updater are retained."
-    if dry_run:
-        plan = (
-            partial
-            if preview.state == "missing" and entry is not None
-            else preview.message
-        )
-        return (
-            True,
-            "[DRY RUN] "
-            + _native_lifecycle_notice()
-            + " "
-            + plan
-            + " No native lifecycle, registration changes or prompts were performed.",
-        )
-    if not confirmed:
-        return (
-            False,
-            preview.message
-            + " Explicit confirmation is required (default No); no removal was performed.",
-        )
-    if preview.state == "missing":
-        if entry is None:
-            return (
-                True,
-                "Native executable and exact user registration are absent; no changes made. Companion assets were not audited; indexes and updater are retained.",
-            )
-        success, message = _cleanup_user_native_registration()
-        return success, partial + " " + message
-
-    removed = codebase_memory.uninstall_codebase_memory(scope=scope, confirmed=True)
-    if not removed.success:
-        return False, removed.message
-    success, message = _cleanup_user_native_registration()
-    combined = removed.message + " " + message
-    if removed.remaining:
-        combined += (
-            " Alternate PATH entries remain: "
-            + ", ".join(map(str, removed.remaining))
-            + "."
-        )
-    return success, combined
-
-
 def install_mcp_server(
     server_info: Dict, scope: str = "user", dry_run: bool = False
 ) -> bool:
@@ -1096,10 +809,6 @@ def install_mcp_server(
         True if successful, False otherwise
     """
     server_name = server_info["name"]
-    if server_name == codebase_memory.BINARY_NAME:
-        success, message = install_codebase_memory_mcp(scope=scope, dry_run=dry_run)
-        click.echo(message, err=not success)
-        return success
     transport = server_info["transport"]
     command = server_info["command"]
 
@@ -1319,14 +1028,10 @@ def install_mcp_servers(
     scope: str = "user",
     dry_run: bool = False,
     use_gateway: Optional[bool] = None,
-    *,
-    uninstall: bool = False,
-    yes: bool = False,
 ) -> Tuple[bool, str]:
-    """Validate the whole selection, then install it or remove only Codebase Memory.
+    """Validate the whole selection, then install it.
 
-    `yes` controls native removal consent only. It never bypasses API-key or
-    global-binary prompts. Dry-run never enters prerequisite/mutation paths.
+    Dry-run never enters prerequisite/mutation paths.
     """
     if scope not in {"local", "project", "user"}:
         return False, "Invalid MCP scope"
@@ -1335,55 +1040,45 @@ def install_mcp_servers(
         selected = ["airis-mcp-gateway"]
     if not selected:
         if dry_run:
-            click.echo(
-                "1. Install MCP servers (default)\n2. Uninstall Codebase Memory MCP\n3. Cancel"
-            )
+            click.echo("1. Install MCP servers (default)\n2. Cancel")
             _show_mcp_install_choices()
             return (
                 True,
-                "[DRY RUN] Available choices only; select servers explicitly to preview an operation. "
-                + _native_lifecycle_notice(),
+                "[DRY RUN] Available choices only; select servers explicitly to preview an operation.",
             )
-        if uninstall or yes or not _is_interactive():
+        if not _is_interactive():
             return (
                 False,
-                "Explicit server selection is required; use --servers codebase-memory-mcp for native lifecycle actions.",
+                "Explicit server selection is required; use --servers.",
             )
-        click.echo(
-            "1. Install MCP servers (default)\n2. Uninstall Codebase Memory MCP\n3. Cancel"
-        )
-        action = click.prompt("Action", default="1", type=click.Choice(["1", "2", "3"]))
-        if action == "3":
-            return True, "Cancelled; no changes made."
+        click.echo("1. Install MCP servers (default)\n2. Cancel")
+        action = click.prompt("Action", default="1", type=click.Choice(["1", "2"]))
         if action == "2":
-            selected, uninstall = [codebase_memory.BINARY_NAME], True
-        else:
-            _show_mcp_install_choices()
-            choice = (
-                click.prompt(
-                    "Select g for gateway, 0 for all, or comma-separated numbers",
-                    default="g",
-                )
-                .strip()
-                .lower()
+            return True, "Cancelled; no changes made."
+        _show_mcp_install_choices()
+        choice = (
+            click.prompt(
+                "Select g for gateway, 0 for all, or comma-separated numbers",
+                default="g",
             )
-            if choice == "g":
-                selected = ["airis-mcp-gateway"]
-            elif choice == "0":
-                selected = list(MCP_SERVERS)
-            else:
-                try:
-                    indices = [int(value.strip()) for value in choice.split(",")]
-                    names = list(MCP_SERVERS)
-                    if not indices or any(
-                        index < 1 or index > len(names) for index in indices
-                    ):
-                        return False, "Invalid selection; no changes made."
-                    selected = list(
-                        dict.fromkeys(names[index - 1] for index in indices)
-                    )
-                except ValueError:
+            .strip()
+            .lower()
+        )
+        if choice == "g":
+            selected = ["airis-mcp-gateway"]
+        elif choice == "0":
+            selected = list(MCP_SERVERS)
+        else:
+            try:
+                indices = [int(value.strip()) for value in choice.split(",")]
+                names = list(MCP_SERVERS)
+                if not indices or any(
+                    index < 1 or index > len(names) for index in indices
+                ):
                     return False, "Invalid selection; no changes made."
+                selected = list(dict.fromkeys(names[index - 1] for index in indices))
+            except ValueError:
+                return False, "Invalid selection; no changes made."
     unknown = [
         name
         for name in selected
@@ -1391,30 +1086,6 @@ def install_mcp_servers(
     ]
     if unknown:
         return False, "Unknown MCP server selection: " + ", ".join(unknown)
-    if uninstall and selected != [codebase_memory.BINARY_NAME]:
-        return (
-            False,
-            "Uninstall accepts only --servers codebase-memory-mcp, not mixed or other servers.",
-        )
-    if codebase_memory.BINARY_NAME in selected:
-        invalid = _native_selection_error(scope)
-        if invalid:
-            return False, invalid
-    if uninstall:
-        if not dry_run and not yes and not _is_interactive():
-            return (
-                False,
-                "Noninteractive native removal requires --yes; no changes made.",
-            )
-        valid, preview = uninstall_codebase_memory_mcp(scope=scope, dry_run=True)
-        if dry_run or not valid:
-            return valid, preview
-        click.echo("Removal preview: " + preview.removeprefix("[DRY RUN] "))
-        if not yes and not click.confirm(
-            "Proceed with account-wide Codebase Memory removal?", default=False
-        ):
-            return True, "Removal declined; no changes made."
-        return uninstall_codebase_memory_mcp(scope=scope, confirmed=True)
 
     if not dry_run:
         ready, errors = check_prerequisites(selected)
diff --git a/src/superclaude/cli/main.py b/src/superclaude/cli/main.py
index d2e7d396..5624c254 100644
--- a/src/superclaude/cli/main.py
+++ b/src/superclaude/cli/main.py
@@ -255,7 +255,7 @@ def install(target: str, force: bool, list_only: bool):
     "--servers",
     "-s",
     multiple=True,
-    help="Specific MCP servers to install or remove (repeatable)",
+    help="Specific MCP servers to install (repeatable)",
 )
 @click.option(
     "--list", "list_only", is_flag=True, help="List available MCP servers (read-only)"
@@ -264,44 +264,29 @@ def install(target: str, force: bool, list_only: bool):
     "--scope",
     default="user",
     type=click.Choice(["local", "project", "user"]),
-    help="Registration scope; native Codebase Memory supports user only",
+    help="Registration scope",
 )
 @click.option(
     "--dry-run",
     is_flag=True,
-    help="Preview choices or selected lifecycle without prompts or changes",
+    help="Preview choices or selected installs without prompts or changes",
 )
-@click.option(
-    "--uninstall",
-    is_flag=True,
-    help="NEW: remove only codebase-memory-mcp and its owned integrations; retain indexes",
-)
-@click.option(
-    "--yes",
-    "-y",
-    is_flag=True,
-    help="NEW: confirm selected Codebase Memory removal only; never selects servers or deletes indexes",
-)
-def mcp(servers, list_only, scope, dry_run, uninstall, yes):
+def mcp(servers, list_only, scope, dry_run):
     """Install and manage MCP servers for Claude Code.
 
-    No selection opens an action menu on a terminal. Native Codebase Memory uses
-    full account-wide upstream setup on Linux, not project-only registration.
+    No selection opens an action menu on a terminal.
 
     Examples:
         superclaude mcp --list
         superclaude mcp --servers tavily --servers context7
-        superclaude mcp --servers codebase-memory-mcp
-        superclaude mcp --uninstall --servers codebase-memory-mcp --yes
-        superclaude mcp --servers codebase-memory-mcp --uninstall --dry-run
         superclaude mcp --dry-run
     """
     from .install_mcp import install_mcp_servers, list_available_servers
 
     if list_only:
-        if servers or uninstall or yes or dry_run or scope != "user":
+        if servers or dry_run or scope != "user":
             raise click.UsageError(
-                "--list cannot be combined with selections, lifecycle flags, --dry-run or another scope"
+                "--list cannot be combined with selections, --dry-run or another scope"
             )
         list_available_servers()
         return
@@ -310,8 +295,6 @@ def mcp(servers, list_only, scope, dry_run, uninstall, yes):
         selected_servers=list(servers) if servers else None,
         scope=scope,
         dry_run=dry_run,
-        uninstall=uninstall,
-        yes=yes,
     )
     click.echo(message)
     if not success:
diff --git a/tests/cli/test_install_mcp_cli.py b/tests/cli/test_install_mcp_cli.py
index 704f8902..f8500bac 100644
--- a/tests/cli/test_install_mcp_cli.py
+++ b/tests/cli/test_install_mcp_cli.py
@@ -95,6 +95,69 @@ def mcp_cli(monkeypatch, isolated_home):
     return state
 
 
+def test_mcp_list_shows_every_registry_server_and_no_retired_one(mcp_cli):
+    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp", "--list"])
+    assert result.exit_code == 0, result.output
+    for name in mcp_cli.module.MCP_SERVERS:
+        assert name in result.output
+    assert "airis-mcp-gateway" in result.output
+    assert "codebase-memory-mcp" not in result.output
+    assert mcp_cli.calls == [] and not any(
+        cmd[:3] == ["claude", "mcp", "add"] for cmd in mcp_cli.processes
+    )
+
+
+def test_mcp_noninteractive_requires_selection_without_prompt(mcp_cli, monkeypatch):
+    monkeypatch.setattr(
+        mcp_cli.module.click, "prompt", lambda *a, **k: pytest.fail("non-TTY menu")
+    )
+    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp"])
+    assert result.exit_code != 0 and "select" in result.output.lower()
+    assert mcp_cli.calls == [] and mcp_cli.processes == []
+
+
+def test_mcp_no_selection_dry_run_prints_choices(mcp_cli, monkeypatch):
+    monkeypatch.setattr(
+        mcp_cli.module.click, "prompt", lambda *a, **k: pytest.fail("dry-run prompt")
+    )
+    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp", "--dry-run"])
+    assert result.exit_code == 0
+    for text in (
+        "1. Install MCP servers (default)",
+        "2. Cancel",
+        "airis-mcp-gateway",
+        *mcp_cli.module.MCP_SERVERS,
+    ):
+        assert text in result.output
+    assert "Uninstall" not in result.output
+    assert mcp_cli.calls == [] and mcp_cli.processes == []
+
+
+def test_mcp_menu_defaults_install_then_gateway(mcp_cli):
+    mcp_cli.interactive = True
+    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp"], input="\n\n")
+    assert result.exit_code == 0, result.output
+    assert "Install MCP servers" in result.output and "Cancel" in result.output
+    assert "Uninstall" not in result.output
+    assert mcp_cli.calls == [("gateway", False)]
+
+
+def test_mcp_menu_cancel_has_no_effects(mcp_cli):
+    mcp_cli.interactive = True
+    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp"], input="2\n")
+    assert result.exit_code == 0 and "cancel" in result.output.lower()
+    assert mcp_cli.calls == [] and mcp_cli.processes == []
+
+
+def test_mcp_menu_install_all_installs_the_individual_servers(mcp_cli, monkeypatch):
+    mcp_cli.interactive = True
+    monkeypatch.setattr(mcp_cli.module, "prompt_for_api_key", lambda *a, **k: None)
+    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp"], input="1\n0\n")
+    assert result.exit_code == 0, result.output
+    assert any("tavily-mcp@0.2.22" in cmd for cmd in mcp_cli.processes)
+    assert ("gateway", False) not in mcp_cli.calls
+
+
 @pytest.mark.parametrize(
     "extra",
     [
diff --git a/tests/cli/test_install_mcp_registry.py b/tests/cli/test_install_mcp_registry.py
index 67c0ad89..242713fa 100644
--- a/tests/cli/test_install_mcp_registry.py
+++ b/tests/cli/test_install_mcp_registry.py
@@ -35,7 +35,12 @@ def test_updated_mcp_registry_commands_are_pinned_and_stable():
 
 
 def test_removed_mcp_servers_are_not_in_registry():
-    for name in ("sequential-thinking", "magic", "chrome-devtools"):
+    for name in (
+        "sequential-thinking",
+        "magic",
+        "chrome-devtools",
+        "codebase-memory-mcp",
+    ):
         assert name not in install_mcp.MCP_SERVERS
 
 
@@ -189,56 +194,6 @@ def test_auggie_global_binary_rejects_node_19_before_binary_install(monkeypatch)
     assert calls == [["node", "--version"]]
 
 
-def test_codebase_memory_native_registry_contract():
-    entry = install_mcp.MCP_SERVERS["codebase-memory-mcp"]
-    assert entry["name"] == "codebase-memory-mcp"
-    assert entry["transport"] == "stdio"
-    assert entry["command"] == "codebase-memory-mcp"
-    assert entry["args"] == []
-    assert "api_key_env" not in entry
-    assert "requires_global_binary" not in entry
-
-
-def test_codebase_memory_dispatch_uses_shared_install(monkeypatch, capsys):
-    calls = []
-
-    def install(*, scope, dry_run):
-        calls.append((scope, dry_run))
-        return True, "native registration fixture"
-
-    monkeypatch.setattr(install_mcp, "install_codebase_memory_mcp", install)
-    monkeypatch.setattr(
-        install_mcp,
-        "check_mcp_server_installed",
-        lambda *a: (_ for _ in ()).throw(AssertionError("legacy list lookup")),
-    )
-    assert install_mcp.install_mcp_server(
-        install_mcp.MCP_SERVERS["codebase-memory-mcp"], scope="user", dry_run=True
-    )
-    assert calls == [("user", True)]
-    assert "native registration fixture" in capsys.readouterr().out
-
-
-def test_selected_native_prerequisites_do_not_probe_other_runtimes(monkeypatch):
-    from superclaude.cli import install_codebase_memory as native
-
-    calls = []
-    monkeypatch.setattr(
-        native,
-        "discover_executable",
-        lambda: native.Discovery("canonical", Path("/fixture/native"), "fixture"),
-    )
-
-    def run(cmd, **kwargs):
-        calls.append(cmd)
-        assert cmd == ["claude", "--version"]
-        return SimpleNamespace(returncode=0, stdout="fixture", stderr="")
-
-    monkeypatch.setattr(install_mcp, "_run_command", run)
-    assert install_mcp.check_prerequisites(["codebase-memory-mcp"]) == (True, [])
-    assert calls == [["claude", "--version"]]
-
-
 def test_selected_npm_prerequisites_probe_only_claude_node_and_npx(monkeypatch):
     calls = []
 
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
