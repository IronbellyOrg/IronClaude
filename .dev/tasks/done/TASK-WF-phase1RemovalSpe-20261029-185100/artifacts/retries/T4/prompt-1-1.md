25c904b6172a1ef32eea5e5f1e75a6fbb076841a
Review one task for spec compliance.

Task brief: ## Task 4: Add the non-fatal retire step for existing workspaces

Depends on: Task 3

Implements ./source.md §3 (decision 3.1, matchers 3.2, behaviour and bounds 3.3, surfaces and messages 3.4, files and tests 3.5) and §8 T3. Create `src/superclaude/cli/install_retired_mcp.py` (the `RETIRED_MCP_SERVERS` table with the sunset comment, the pure `classify_retired_entries()` classifier, the receipt/marker predicates copied from `install_codebase_memory.py:95-100`, `:125-139`, `:185-199`, the message builder and `run_retire_step()`); add `_remove_exact_user_entry(name, matcher)` and a direct-exec `claude` wrapper (argv list, `start_new_session=True`, process-group kill, 10 s per call, 15 s step cap) to `src/superclaude/cli/install_mcp.py` beside the existing `_cleanup_user_native_registration`, which this task leaves untouched (it is still called by `uninstall_codebase_memory_mcp` at `install_mcp.py:993` and `:999`, which the tavily tests exercise until Task 5 deletes both together; the retire step uses only the new remover); call the step in `install()` in `src/superclaude/cli/main.py` in the slot of the deleted codebase-memory phase inside its own `try/except Exception`, and add the `install --list` lines and the `update` notice; add the warn-only check to `src/superclaude/cli/doctor.py`. Matchers, exactly as ./source.md §3.2: codebase-memory by absolute-path basename with the binary gate; Serena Tier R rows (a)-(c) removed with `env` and `headers` each absent or `{}`; Tier K (current pin and the other listed shapes) kept and printed as "Legacy Serena registration kept until codegraph is ready ...", only until Phase 2's `codegraph_ready()` gate removes it; the re-register hint uses the name `serena-local`. The literal server names live only in `install_retired_mcp.py` and its test; the module must not import `install_codebase_memory.py`. Write `tests/cli/test_install_retired_mcp.py` with every case listed in ./source.md §3.5, including `env: {}` / `headers: {}` counted as absent and the hint naming `serena-local`; update `tests/cli/test_update_command.py` so the expected call list includes the retire step after user setup. Commit `feat(install): retire stale codebase-memory-mcp and serena user registrations (#323)`.

Acceptance criteria:
- T4.AC1: `uv run pytest tests/cli/test_install_retired_mcp.py tests/cli/test_update_command.py tests/cli/test_update_script.py tests/cli/test_install_mcp_tavily.py tests/cli/test_install_mcp_cli.py tests/unit -q -p no:cacheprovider` passes.
- T4.AC2: `rg -n 'install_codebase_memory' src/superclaude/cli/install_retired_mcp.py` prints nothing.
- T4.AC3: In a sandbox HOME, `T=$(mktemp -d /tmp/p1-list.XXXXXX) && env HOME="$T" CLAUDE_CONFIG_DIR="$T" UV_CACHE_DIR="$(uv cache dir)" uv run --no-sync superclaude install --list > "$T/list.txt"` exits 0 and `rg -c 'codebase-memory-mcp|serena' "$T/list.txt"` prints at least 2 (both "absent"); then `rm -rf "$T"`.
- T4.AC4: A failing retire step never changes the `superclaude install` exit code (pinned by a test in `tests/cli/test_install_retired_mcp.py`).

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
Start sha: 25c904b6172a1ef32eea5e5f1e75a6fbb076841a
Diff against the start snapshot: Touched files: src/superclaude/cli/install_retired_mcp.py (new), tests/cli/test_install_retired_mcp.py (new), src/superclaude/cli/install_mcp.py, src/superclaude/cli/main.py, src/superclaude/cli/doctor.py, tests/cli/test_update_command.py. Spec text: $PKG/source.md section 3 (lines 303-376) and section 8.1 row T3. Observed by the implementer (verify yourself): the Task 4 pytest command gives 626 passed, 3 skipped; the sandboxed install --list exits 0 and prints both names as absent.

=== tracked diff vs start ===
diff --git a/src/superclaude/cli/doctor.py b/src/superclaude/cli/doctor.py
index e2503f63..c529121a 100644
--- a/src/superclaude/cli/doctor.py
+++ b/src/superclaude/cli/doctor.py
@@ -43,6 +43,8 @@ def run_doctor(verbose: bool = False) -> Dict[str, Any]:
 
     checks.append(_check_ccsession())
 
+    checks.append(_check_retired_mcp())
+
     return {
         "checks": checks,
         "passed": all(check["passed"] for check in checks),
@@ -108,6 +110,31 @@ def _check_ccsession(home: Path | None = None) -> Dict[str, Any]:
     }
 
 
+def _check_retired_mcp() -> Dict[str, Any]:
+    """Warn (never fail) when a retired MCP registration is still present."""
+    try:
+        from .install_retired_mcp import doctor_warning
+
+        warning = doctor_warning()
+    except Exception as exc:
+        return {
+            "name": "Retired MCP registrations (warning: check skipped)",
+            "passed": True,
+            "details": [f"Could not check: {type(exc).__name__}"],
+        }
+    if warning:
+        return {
+            "name": "Retired MCP registrations (warning: legacy registration present)",
+            "passed": True,
+            "details": [warning],
+        }
+    return {
+        "name": "Retired MCP registrations",
+        "passed": True,
+        "details": ["No legacy registration to retire"],
+    }
+
+
 def _check_pytest_plugin() -> Dict[str, Any]:
     """
     Check if pytest plugin is loaded
diff --git a/src/superclaude/cli/install_mcp.py b/src/superclaude/cli/install_mcp.py
index 66351aef..61c11bcf 100644
--- a/src/superclaude/cli/install_mcp.py
+++ b/src/superclaude/cli/install_mcp.py
@@ -11,8 +11,10 @@ import platform
 import re
 import shlex
 import shutil
+import signal
 import subprocess
 import sys
+import time
 from pathlib import Path
 from typing import Dict, List, Optional, Tuple
 
@@ -948,6 +950,78 @@ def _cleanup_user_native_registration() -> tuple[bool, str]:
     )
 
 
+def _exec_claude(argv: list[str], timeout: float) -> int:
+    """Run ``claude`` directly (no shell) in its own session; kill the group on timeout.
+
+    Output is discarded: Claude's text or the exception argv can contain old secrets.
+    Raises ``subprocess.TimeoutExpired`` after the process group is killed.
+    """
+    process = subprocess.Popen(
+        argv,
+        stdin=subprocess.DEVNULL,
+        stdout=subprocess.DEVNULL,
+        stderr=subprocess.DEVNULL,
+        start_new_session=True,
+    )
+    try:
+        return process.wait(timeout=timeout)
+    except subprocess.TimeoutExpired:
+        try:
+            os.killpg(process.pid, signal.SIGKILL)
+        except (ProcessLookupError, PermissionError):
+            process.kill()
+        try:
+            process.wait(timeout=2)
+        except subprocess.TimeoutExpired:
+            pass
+        raise
+
+
+def _remove_exact_user_entry(
+    name: str,
+    matcher,
+    *,
+    deadline: float | None = None,
+    per_call_timeout: float = 10.0,
+) -> str:
+    """Remove the user-scope entry ``name`` only while ``matcher(entry)`` is true.
+
+    The entry is re-read and re-matched right before ``claude mcp remove`` and read
+    again afterwards. Returns one of: removed, absent, changed (no longer matches
+    before removal; kept), replaced (a different shape appeared after removal; kept),
+    unverified, unknown (lookup failed), timeout, failed, skipped (``deadline`` hit,
+    a ``time.monotonic()`` value). Nothing is ever retried.
+    """
+    known, entry = read_user_mcp_entry(name)
+    if not known:
+        return "unknown"
+    if entry is None:
+        return "absent"
+    if not matcher(entry):
+        return "changed"
+    timeout = per_call_timeout
+    if deadline is not None:
+        timeout = min(timeout, deadline - time.monotonic())
+        if timeout <= 0:
+            return "skipped"
+    try:
+        returncode = _exec_claude(
+            ["claude", "mcp", "remove", name, "--scope", "user"], timeout
+        )
+    except subprocess.TimeoutExpired:
+        return "timeout"
+    except OSError:
+        return "failed"
+    if returncode != 0:
+        return "failed"
+    known, after = read_user_mcp_entry(name)
+    if not known:
+        return "unverified"
+    if after is None:
+        return "removed"
+    return "unverified" if matcher(after) else "replaced"
+
+
 def uninstall_codebase_memory_mcp(
     *, scope: str = "user", confirmed: bool = False, dry_run: bool = False
 ) -> tuple[bool, str]:
diff --git a/src/superclaude/cli/main.py b/src/superclaude/cli/main.py
index 8c4f63a7..d2e7d396 100644
--- a/src/superclaude/cli/main.py
+++ b/src/superclaude/cli/main.py
@@ -149,6 +149,15 @@ def install(target: str, force: bool, list_only: bool):
         click.echo(
             f"\nTemplates: {len(templates_available)} available, {len(templates_installed)} installed"
         )
+
+        click.echo("\nRetired MCP registrations (user scope):")
+        try:
+            from .install_retired_mcp import list_lines
+
+            for line in list_lines():
+                click.echo(line)
+        except Exception as exc:
+            click.echo(f"   unavailable ({type(exc).__name__})")
         return
 
     # Step 1: Install core framework files to ~/.claude/
@@ -216,6 +225,18 @@ def install(target: str, force: bool, list_only: bool):
     setup_success, setup_message = install_user_setup(force=force)
     click.echo(setup_message)
 
+    # Step 8: retire stale MCP registrations IronClaude can prove it wrote.
+    # Non-fatal by design: nothing here may change the exit code.
+    click.echo("\n📦 Retiring stale MCP registrations...")
+    try:
+        from .install_retired_mcp import run_retire_step
+
+        run_retire_step()
+    except Exception as exc:
+        click.echo(
+            f"   ⚠️  Retire step skipped ({type(exc).__name__}); install is complete."
+        )
+
     if (
         not core_success
         or not cmd_success
@@ -370,6 +391,16 @@ def update(target: str):
     setup_success, setup_message = install_user_setup(force=True)
     click.echo(setup_message)
 
+    # Read-only: update never touches MCP registrations.
+    try:
+        from .install_retired_mcp import update_notice
+
+        notice = update_notice()
+        if notice:
+            click.echo(f"\n{notice}")
+    except Exception:
+        pass
+
     if not all(
         (
             core_success,
diff --git a/tests/cli/test_update_command.py b/tests/cli/test_update_command.py
index 6caffd0c..885dc5ef 100644
--- a/tests/cli/test_update_command.py
+++ b/tests/cli/test_update_command.py
@@ -24,6 +24,9 @@ _INSTALLERS = (
     "superclaude.cli.install_user_setup.install_user_setup",
 )
 
+# Runs at the end of ``install`` only; ``update`` never touches MCP registrations.
+_RETIRE_STEP = "superclaude.cli.install_retired_mcp.run_retire_step"
+
 
 @pytest.fixture(autouse=True)
 def isolated_home_guard(tmp_path, monkeypatch):
@@ -59,6 +62,11 @@ def _stub_installers(monkeypatch, *, failing: str | None = None):
 
         monkeypatch.setattr(path, fake)
 
+    def retire(*args, **kwargs):
+        calls.append("run_retire_step")
+        return {}
+
+    monkeypatch.setattr(_RETIRE_STEP, retire)
     return calls
 
 
@@ -104,6 +112,7 @@ def test_install_wires_before_hooks_and_templates(monkeypatch):
         "install_hooks",
         "install_templates",
         "install_user_setup",
+        "run_retire_step",
     ]
 
 

=== new file src/superclaude/cli/install_retired_mcp.py (read it from disk) ===
=== new file tests/cli/test_install_retired_mcp.py (read it from disk) ===
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
