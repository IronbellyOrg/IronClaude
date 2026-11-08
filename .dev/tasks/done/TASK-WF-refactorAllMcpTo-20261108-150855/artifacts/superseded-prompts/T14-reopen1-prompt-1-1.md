d227979bd306fd95922f73e070fc534ae2f6d2a0
Review one task for spec compliance.

Task brief: ## Task 14: Remove the repository `.mcp.json` auggie-mcp stdio entry

Design section 5. Precondition: the owner approved removal (owner question 2). If not approved when this task starts, make no change to `.mcp.json` or its test, write `./artifacts/t14-skipped.md` stating "skipped: owner decision 2 open", and finish the task. If approved: delete the repository root `.mcp.json` (its only entry is `auggie-mcp`, a stdio `auggie --mcp --mcp-auto-workspace` that fails with ENOENT where the `auggie` binary is absent) and rewrite `tests/cli/test_mcp_project_config.py` to assert that if `.mcp.json` exists at the repository root it has no `auggie-mcp` entry and no stdio entry whose `command` is `auggie`.

Acceptance criteria:
- Either `./artifacts/t14-skipped.md` exists and `git diff --quiet .mcp.json tests/cli/test_mcp_project_config.py` holds, or `.mcp.json` is deleted and `uv run pytest tests/cli/test_mcp_project_config.py -v` passes (output in `./artifacts/t14-pytest.log`).

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
Start sha: d227979bd306fd95922f73e070fc534ae2f6d2a0
Diff against the start snapshot: diff --git a/.mcp.json b/.mcp.json
deleted file mode 100644
index a0308c1c..00000000
--- a/.mcp.json
+++ /dev/null
@@ -1,13 +0,0 @@
-{
-  "mcpServers": {
-    "auggie-mcp": {
-      "type": "stdio",
-      "command": "auggie",
-      "args": [
-        "--mcp",
-        "--mcp-auto-workspace"
-      ],
-      "env": {}
-    }
-  }
-}
\ No newline at end of file
diff --git a/tests/cli/test_mcp_project_config.py b/tests/cli/test_mcp_project_config.py
index 23336cf9..aeac9074 100644
--- a/tests/cli/test_mcp_project_config.py
+++ b/tests/cli/test_mcp_project_config.py
@@ -1,4 +1,9 @@
-"""Contracts for the repository-owned Claude MCP configuration."""
+"""Contracts for the repository-owned Claude MCP configuration.
+
+Codebase search now goes through the central LiteLLM proxy (issue #454), so the
+repository must not register the local ``auggie`` stdio server, which fails
+with ENOENT wherever the ``auggie`` binary is absent.
+"""
 
 import json
 from pathlib import Path
@@ -6,15 +11,15 @@ from pathlib import Path
 _REPO_ROOT = Path(__file__).resolve().parents[2]
 
 
-def test_project_auggie_configuration_uses_official_cli_and_stable_key():
-    config = json.loads((_REPO_ROOT / ".mcp.json").read_text())
-    server = config["mcpServers"]["auggie-mcp"]
+def test_project_mcp_config_has_no_auggie_stdio_server():
+    path = _REPO_ROOT / ".mcp.json"
+    if not path.exists():
+        return
+    servers = json.loads(path.read_text()).get("mcpServers", {})
 
-    assert server == {
-        "type": "stdio",
-        "command": "auggie",
-        "args": ["--mcp", "--mcp-auto-workspace"],
-        "env": {},
-    }
-    assert server["command"] != "npx"
-    assert "AUGMENT_SESSION_AUTH" not in server["env"]
+    assert "auggie-mcp" not in servers
+    assert not [
+        name
+        for name, server in servers.items()
+        if server.get("type", "stdio") == "stdio" and server.get("command") == "auggie"
+    ]
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

Reopen note (orchestrator): this is a reopened Task 14. The owner approved removal (owner question 2, recorded in .dev/issues/454/owner-decisions.md), and the coordinator ruled to reopen Task 14 and take the removal branch: remove the auggie-mcp entry, delete .mcp.json only if no servers remain and nothing else reads it, and rewrite tests/cli/test_mcp_project_config.py to assert the entry is absent. The AC evidence log is .dev/tasks/to-do/TASK-WF-refactorAllMcpTo-20261108-150855/artifacts/t14-pytest.log. The superseded file artifacts/t14-skipped.md comes from the first, wrong skip-branch run and is not the branch under review. Check that no repository file still reads the root .mcp.json (Makefile, pyproject.toml, .claude/settings.json, .github/workflows, .pre-commit-config.yaml, installer code under src/superclaude/cli, hooks). tests/skills/test_mcp_proxy_names.py is an untracked file from Task 15 and is unchanged since the start snapshot; it is excluded from the diff. Write your review to .dev/tasks/to-do/TASK-WF-refactorAllMcpTo-20261108-150855/artifacts/retries/T14/reopen-1/review-1-1.out and return only that path.
