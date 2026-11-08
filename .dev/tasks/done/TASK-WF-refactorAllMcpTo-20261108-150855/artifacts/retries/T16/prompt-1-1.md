6179ce34e9eebe2fa08f4ebb81f69a2cf924bfcf
Review one task for spec compliance.

Task brief: ## Task 16: Sync dev copies, lint and run the affected suites

Design section 8. Run `make sync-dev`, then `make lint`, then `make verify-sync`, then `uv run pytest tests/agents tests/skills tests/commands tests/hooks tests/core tests/troubleshoot tests/cli -v`, then `make test`. Fix any failure caused by Tasks 1-15. Do not stage `.claude/` mirrors; stage `.dev/tasks` as always.

Depends on: Task 1, Task 2, Task 8, Task 11, Task 13, Task 14, Task 15

Acceptance criteria:
- `make lint` and `make verify-sync` exit 0; logs in `./artifacts/t16-lint.log` and `./artifacts/t16-verify-sync.log`.
- The listed pytest directories pass and the `make test` result (pass count, any failures with cause) is recorded in `./artifacts/t16-tests.log`; any pre-existing failure unrelated to this change is shown failing on 0423fe5f too.
- `git status --short .claude` shows no staged `.claude/` path.
Global constraints: - Naming rule (design section 2): name both tools, proxy first, direct kept. Proxy names: Augment search `mcp__litellm__augment_code-augment_code_search` (called AUG below), `mcp__litellm__context7-resolve-library-id`, `mcp__litellm__context7-query-docs`, `mcp__litellm__Tavily-tavily_search`, `mcp__litellm__Tavily-tavily_extract`, `mcp__litellm__Tavily-tavily_crawl`, `mcp__litellm__Tavily-tavily_map` (capital `T`, case-sensitive). Playwright plugin names `mcp__plugin_playwright_playwright__browser_<x>`.
- AUG phrase (full form, verbatim): "Codebase search: call `mcp__litellm__augment_code-augment_code_search` (`repo_owner`/`repo_name` from `git remote get-url origin`, `branch` = the repository's default branch; it sees pushed code only); if that tool is not available, call `mcp__auggie__codebase-retrieval`. For uncommitted or unpushed changes use codegraph or Grep."
- AUG short form (inside lists and tables): "`mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`)".
- Tavily phrase: "`mcp__litellm__Tavily-tavily_<x>` (else `mcp__tavily__tavily_<x>`)", keeping any existing WebSearch/WebFetch fallback tail. Context7 phrase: "`mcp__litellm__context7-<tool>` (else `mcp__context7__<tool>`)". Wildcards: "`mcp__litellm__Tavily-*` or `mcp__tavily__*`", "`mcp__litellm__context7-*` or `mcp__context7__*`".
- Allow-lists (`tools:` / `allowed-tools:`): insert each proxy name immediately before its direct twin; never remove a direct name except `mcp__auggie-mcp__codebase-retrieval`, which is replaced by AUG followed by `mcp__auggie__codebase-retrieval`. `mcp__litellm__Tavily-tavily_research` is not added anywhere.
- `mcp-servers:` metadata: add `litellm` first; replace `auggie-mcp` with `auggie`; keep the other words (`[auggie, codegraph]` becomes `[litellm, auggie, codegraph]`).
- Availability tests ("if X is not available") become "if neither <proxy name> nor <direct name> is available". Every existing degrade or fail-open path is kept verbatim (design section 4).
- Never hard-code a repository owner, name or branch; never add a `src/superclaude/...` path to an installed primitive.
- Edit `src/superclaude/**` and the hand-maintained `plugins/superclaude/**` copies only; never edit or stage `.claude/` mirrors (run `make sync-dev` instead) and never hand-edit `~/.claude`.
- Line numbers below were recorded at commit 0423fe5f; re-locate each edit by its text before editing.
- Python only through UV (`uv run pytest ...`). Never print, log or write `LITELLM_API_KEY` or any token.
- `.dev/tasks/` is always staged (`git add .dev/tasks`); `.dev/issues/` stays out of the index. No push and no PR in this run.
Start sha: 6179ce34e9eebe2fa08f4ebb81f69a2cf924bfcf
Diff against the start snapshot: diff --git a/tests/skills/test_mcp_proxy_names.py b/tests/skills/test_mcp_proxy_names.py
deleted file mode 100644
index a761f7bc..00000000
--- a/tests/skills/test_mcp_proxy_names.py
+++ /dev/null
@@ -1,82 +0,0 @@
-"""Regression guard for the LiteLLM proxy MCP names (issue #454).
-
-Every installed primitive that names a direct MCP tool must also name its
-`mcp__litellm__` proxy twin, so a session that only has the proxy still finds the
-tool. CI-safe: pure file-content assertions over the source and plugin trees.
-"""
-
-import re
-from pathlib import Path
-
-_REPO = Path(__file__).resolve().parents[2]
-_ROOTS = [
-    _REPO / "src" / "superclaude" / "agents",
-    _REPO / "src" / "superclaude" / "skills",
-    _REPO / "src" / "superclaude" / "commands",
-    _REPO / "src" / "superclaude" / "core",
-    _REPO / "plugins" / "superclaude",
-]
-
-_AUGGIE = "mcp__auggie__codebase-retrieval"
-_AUG = "mcp__litellm__augment_code-augment_code_search"
-_AUGGIE_MCP = "mcp__auggie-mcp__"
-_TOOLS_LINE = re.compile(r"^\s*(?:-\s*)?(?:tools|allowed-tools)\s*:")
-_TAVILY_DIRECT = re.compile(r"mcp__tavily__tavily_([a-z]+)")
-
-
-def _lines():
-    for root in _ROOTS:
-        for path in sorted(root.rglob("*")):
-            if not path.is_file() or "__pycache__" in path.parts:
-                continue
-            try:
-                text = path.read_text(encoding="utf-8")
-            except UnicodeDecodeError:
-                continue
-            rel = path.relative_to(_REPO).as_posix()
-            for n, line in enumerate(text.splitlines(), 1):
-                yield path, f"{rel}:{n}", line
-
-
-def test_auggie_lines_also_name_the_proxy_tool():
-    bad = []
-    for path, where, line in _lines():
-        if _AUGGIE not in line:
-            continue
-        if path.name.startswith("freshness-") or path.name == "hooks.json":
-            continue
-        if _AUG not in line:
-            bad.append(f"{where}: names {_AUGGIE} without {_AUG}")
-        elif _TOOLS_LINE.match(line) and line.index(_AUG) > line.index(_AUGGIE):
-            bad.append(f"{where}: allow-list names {_AUGGIE} before {_AUG}")
-    assert not bad, "\n".join(bad)
-
-
-def test_tavily_allow_lists_also_name_the_proxy_tool():
-    bad = []
-    for _path, where, line in _lines():
-        if not _TOOLS_LINE.match(line):
-            continue
-        for tool in _TAVILY_DIRECT.findall(line):
-            if f"mcp__litellm__Tavily-tavily_{tool}" not in line:
-                bad.append(
-                    f"{where}: lists mcp__tavily__tavily_{tool} without its proxy twin"
-                )
-    assert not bad, "\n".join(bad)
-
-
-def test_auggie_mcp_prefix_only_in_hook_matchers():
-    allowed = {"hooks.json", "auggie-flag-clear.sh"}
-    bad = sorted(
-        {
-            where.rsplit(":", 1)[0]
-            for path, where, line in _lines()
-            if _AUGGIE_MCP in line and path.name not in allowed
-        }
-    )
-    assert not bad, "files naming " + _AUGGIE_MCP + ": " + ", ".join(bad)
-
-
-def test_guard_scans_the_expected_trees():
-    assert all(root.is_dir() for root in _ROOTS)
-    assert any(_AUGGIE in line for _p, _w, line in _lines())
diff --git a/tests/skills/test_mcp_proxy_names.py b/tests/skills/test_mcp_proxy_names.py
new file mode 100644
index 00000000..a761f7bc
--- /dev/null
+++ b/tests/skills/test_mcp_proxy_names.py
@@ -0,0 +1,82 @@
+"""Regression guard for the LiteLLM proxy MCP names (issue #454).
+
+Every installed primitive that names a direct MCP tool must also name its
+`mcp__litellm__` proxy twin, so a session that only has the proxy still finds the
+tool. CI-safe: pure file-content assertions over the source and plugin trees.
+"""
+
+import re
+from pathlib import Path
+
+_REPO = Path(__file__).resolve().parents[2]
+_ROOTS = [
+    _REPO / "src" / "superclaude" / "agents",
+    _REPO / "src" / "superclaude" / "skills",
+    _REPO / "src" / "superclaude" / "commands",
+    _REPO / "src" / "superclaude" / "core",
+    _REPO / "plugins" / "superclaude",
+]
+
+_AUGGIE = "mcp__auggie__codebase-retrieval"
+_AUG = "mcp__litellm__augment_code-augment_code_search"
+_AUGGIE_MCP = "mcp__auggie-mcp__"
+_TOOLS_LINE = re.compile(r"^\s*(?:-\s*)?(?:tools|allowed-tools)\s*:")
+_TAVILY_DIRECT = re.compile(r"mcp__tavily__tavily_([a-z]+)")
+
+
+def _lines():
+    for root in _ROOTS:
+        for path in sorted(root.rglob("*")):
+            if not path.is_file() or "__pycache__" in path.parts:
+                continue
+            try:
+                text = path.read_text(encoding="utf-8")
+            except UnicodeDecodeError:
+                continue
+            rel = path.relative_to(_REPO).as_posix()
+            for n, line in enumerate(text.splitlines(), 1):
+                yield path, f"{rel}:{n}", line
+
+
+def test_auggie_lines_also_name_the_proxy_tool():
+    bad = []
+    for path, where, line in _lines():
+        if _AUGGIE not in line:
+            continue
+        if path.name.startswith("freshness-") or path.name == "hooks.json":
+            continue
+        if _AUG not in line:
+            bad.append(f"{where}: names {_AUGGIE} without {_AUG}")
+        elif _TOOLS_LINE.match(line) and line.index(_AUG) > line.index(_AUGGIE):
+            bad.append(f"{where}: allow-list names {_AUGGIE} before {_AUG}")
+    assert not bad, "\n".join(bad)
+
+
+def test_tavily_allow_lists_also_name_the_proxy_tool():
+    bad = []
+    for _path, where, line in _lines():
+        if not _TOOLS_LINE.match(line):
+            continue
+        for tool in _TAVILY_DIRECT.findall(line):
+            if f"mcp__litellm__Tavily-tavily_{tool}" not in line:
+                bad.append(
+                    f"{where}: lists mcp__tavily__tavily_{tool} without its proxy twin"
+                )
+    assert not bad, "\n".join(bad)
+
+
+def test_auggie_mcp_prefix_only_in_hook_matchers():
+    allowed = {"hooks.json", "auggie-flag-clear.sh"}
+    bad = sorted(
+        {
+            where.rsplit(":", 1)[0]
+            for path, where, line in _lines()
+            if _AUGGIE_MCP in line and path.name not in allowed
+        }
+    )
+    assert not bad, "files naming " + _AUGGIE_MCP + ": " + ", ".join(bad)
+
+
+def test_guard_scans_the_expected_trees():
+    assert all(root.is_dir() for root in _ROOTS)
+    assert any(_AUGGIE in line for _p, _w, line in _lines())
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

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
