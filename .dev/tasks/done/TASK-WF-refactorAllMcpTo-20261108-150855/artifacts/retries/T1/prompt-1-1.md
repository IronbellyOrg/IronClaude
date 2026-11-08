6e1870367dd8fe9dc22746e993adb567c1aee5f3
Review one task for spec compliance.

Task brief: ## Task 1: Widen the Auggie flag-clear hook to the proxy Augment tool

Design section 6.1. In `src/superclaude/hooks/hooks.json` (PostToolUse matcher at about line 149) change the matcher `mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*` to `mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*|mcp__litellm__augment_code-.*`. Set `plugins/superclaude/hooks/hooks.json` (about line 119, currently `mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*`) to the same string. In `src/superclaude/hooks/scripts/auggie-flag-clear.sh` add `|mcp__litellm__augment_code-*` to the `case` pattern (about line 23) and list the fourth prefix in the header comment (line 3); make `plugins/superclaude/hooks/scripts/auggie-flag-clear.sh` identical to the src script's comment and case line. Do not change `freshness-user-prompt.sh` (design 6.2). Update the pinned matcher strings in `tests/cli/test_verify_sync_hooks.py` (about lines 179-216) and `tests/cli/eval/test_expect_settings_json.py` (about lines 178, 184, 328). In `tests/hooks/test_auggie_flag_clear_mcp_prefix.py` and `tests/hooks/test_auggie_first.py` add a case where `mcp__litellm__augment_code-augment_code_search` clears the flag and one where `mcp__litellm__Tavily-tavily_search` does not.

Acceptance criteria:
- Both `hooks.json` files carry the identical four-alternative matcher; both flag-clear scripts carry the identical four-glob case line.
- `uv run pytest tests/hooks/test_auggie_flag_clear_mcp_prefix.py tests/hooks/test_auggie_first.py tests/cli/test_verify_sync_hooks.py tests/cli/eval/test_expect_settings_json.py tests/cli/test_install_hooks.py -v` passes, including the two new cases; output saved to `./artifacts/t1-pytest.log`.
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
Start sha: 6e1870367dd8fe9dc22746e993adb567c1aee5f3
Diff against the start snapshot: 
diff --git a/plugins/superclaude/hooks/hooks.json b/plugins/superclaude/hooks/hooks.json
index 3d6e03a7..005b826b 100644
--- a/plugins/superclaude/hooks/hooks.json
+++ b/plugins/superclaude/hooks/hooks.json
@@ -116,7 +116,7 @@
         ]
       },
       {
-        "matcher": "mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*",
+        "matcher": "mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*|mcp__litellm__augment_code-.*",
         "hooks": [
           {
             "type": "command",
diff --git a/plugins/superclaude/hooks/scripts/auggie-flag-clear.sh b/plugins/superclaude/hooks/scripts/auggie-flag-clear.sh
index 7d6af8fb..c4ee84c8 100755
--- a/plugins/superclaude/hooks/scripts/auggie-flag-clear.sh
+++ b/plugins/superclaude/hooks/scripts/auggie-flag-clear.sh
@@ -1,5 +1,6 @@
 #!/usr/bin/env bash
-# PostToolUse: clear auggie-first sticky after any mcp__auggie__* tool call.
+# PostToolUse: clear auggie-first sticky after any auggie-prefixed or Augment proxy tool call
+# (mcp__auggie__*, mcp__auggie-mcp__*, mcp__airis-mcp-gateway__auggie_*, mcp__litellm__augment_code-*).
 # auggie-first-hook-proposal-v2.1.md §6 — synchronous (no async:true) per spec-panel Wh-8.
 # Fail-open per NFR-3.
 set -u
@@ -19,7 +20,7 @@ TOOL_NAME=$(printf '%s' "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null || tr
 [ -z "$SESSION_ID" ] && exit 0
 
 case "$TOOL_NAME" in
-    mcp__auggie__*|mcp__airis-mcp-gateway__auggie_*)
+    mcp__auggie__*|mcp__auggie-mcp__*|mcp__airis-mcp-gateway__auggie_*|mcp__litellm__augment_code-*)
         STICKY="$STATE_DIR/auggie-first-pending/$SESSION_ID.txt"
         if [ -f "$STICKY" ]; then
             rm -f "$STICKY" 2>/dev/null || true
diff --git a/src/superclaude/hooks/hooks.json b/src/superclaude/hooks/hooks.json
index 8fa3755c..da09d9b1 100644
--- a/src/superclaude/hooks/hooks.json
+++ b/src/superclaude/hooks/hooks.json
@@ -146,7 +146,7 @@
         ]
       },
       {
-        "matcher": "mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*",
+        "matcher": "mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*|mcp__litellm__augment_code-.*",
         "hooks": [
           {
             "type": "command",
diff --git a/src/superclaude/hooks/scripts/auggie-flag-clear.sh b/src/superclaude/hooks/scripts/auggie-flag-clear.sh
index c740392f..c4ee84c8 100755
--- a/src/superclaude/hooks/scripts/auggie-flag-clear.sh
+++ b/src/superclaude/hooks/scripts/auggie-flag-clear.sh
@@ -1,6 +1,6 @@
 #!/usr/bin/env bash
-# PostToolUse: clear auggie-first sticky after any auggie-prefixed tool call
-# (mcp__auggie__*, mcp__auggie-mcp__*, mcp__airis-mcp-gateway__auggie_*).
+# PostToolUse: clear auggie-first sticky after any auggie-prefixed or Augment proxy tool call
+# (mcp__auggie__*, mcp__auggie-mcp__*, mcp__airis-mcp-gateway__auggie_*, mcp__litellm__augment_code-*).
 # auggie-first-hook-proposal-v2.1.md §6 — synchronous (no async:true) per spec-panel Wh-8.
 # Fail-open per NFR-3.
 set -u
@@ -20,7 +20,7 @@ TOOL_NAME=$(printf '%s' "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null || tr
 [ -z "$SESSION_ID" ] && exit 0
 
 case "$TOOL_NAME" in
-    mcp__auggie__*|mcp__auggie-mcp__*|mcp__airis-mcp-gateway__auggie_*)
+    mcp__auggie__*|mcp__auggie-mcp__*|mcp__airis-mcp-gateway__auggie_*|mcp__litellm__augment_code-*)
         STICKY="$STATE_DIR/auggie-first-pending/$SESSION_ID.txt"
         if [ -f "$STICKY" ]; then
             rm -f "$STICKY" 2>/dev/null || true
diff --git a/tests/cli/eval/test_expect_settings_json.py b/tests/cli/eval/test_expect_settings_json.py
index c3d55832..963d9348 100644
--- a/tests/cli/eval/test_expect_settings_json.py
+++ b/tests/cli/eval/test_expect_settings_json.py
@@ -325,7 +325,12 @@ def test_equals_supports_list_values(
     eval_spec: EvalSpec, home: HomeIsolation, tmp_path: Path
 ) -> None:
     """``equals`` compares JSON arrays with strict order + element parity."""
-    matchers = ["mcp__auggie__*", "mcp__auggie-mcp__*", "mcp__airis-mcp-gateway__*"]
+    matchers = [
+        "mcp__auggie__*",
+        "mcp__auggie-mcp__*",
+        "mcp__airis-mcp-gateway__*",
+        "mcp__litellm__augment_code-*",
+    ]
     _write_settings(home, {"hooks": {"matchers": matchers}})
     ctx = _make_ctx(eval_spec=eval_spec, home=home, run_dir=tmp_path)
     result = Expect.settings_json(
diff --git a/tests/cli/test_verify_sync_hooks.py b/tests/cli/test_verify_sync_hooks.py
index a359e2a6..c88e3af9 100644
--- a/tests/cli/test_verify_sync_hooks.py
+++ b/tests/cli/test_verify_sync_hooks.py
@@ -213,7 +213,9 @@ def test_V7_regression_to_master():  # noqa: N802 — V1-V7 are release-spec §9
             if "auggie-flag-clear" in h.get("command", ""):
                 reg["matcher"] = "mcp__auggie__.*|mcp__airis-mcp-gateway__auggie_.*"
     original_script = AUGGIE_FLAG_CLEAR.read_text()
-    mutated_script = original_script.replace("|mcp__auggie-mcp__*", "")
+    mutated_script = original_script.replace("|mcp__auggie-mcp__*", "").replace(
+        "|mcp__litellm__augment_code-*", ""
+    )
     with _temporarily_replace_file(HOOKS_JSON, json.dumps(new_data, indent=2)):
         with _temporarily_replace_file(AUGGIE_FLAG_CLEAR, mutated_script):
             result = _run_verify_sync()
diff --git a/tests/hooks/test_auggie_first.py b/tests/hooks/test_auggie_first.py
index 8ea9e5c6..ed5cacd7 100644
--- a/tests/hooks/test_auggie_first.py
+++ b/tests/hooks/test_auggie_first.py
@@ -82,6 +82,40 @@ def test_gateway_alias_clears_sticky(tmp_path: Path) -> None:
     assert '"event":"sticky_cleared"' in telemetry
 
 
+def test_litellm_augment_proxy_clears_sticky(tmp_path: Path) -> None:
+    """The LiteLLM proxy name for Augment codebase search also clears the sticky."""
+    home = tmp_path / "home"
+    sid = "test-clear-litellm"
+    (home / ".claude" / "state" / "auggie-first-pending").mkdir(
+        parents=True, exist_ok=True
+    )
+    _sticky_path(home, sid).write_text("pending\n")
+    payload = {
+        "session_id": sid,
+        "tool_name": "mcp__litellm__augment_code-augment_code_search",
+    }
+    result = _run_hook(payload, fake_home=home)
+    assert result.returncode == 0, result.stderr.decode()
+    assert not _sticky_path(home, sid).exists()
+    telemetry = (home / ".claude" / "logs" / "auggie-first.jsonl").read_text()
+    assert '"tool":"mcp__litellm__augment_code-augment_code_search"' in telemetry
+
+
+def test_litellm_non_augment_tool_preserves_sticky(tmp_path: Path) -> None:
+    """Other LiteLLM proxy tools (Tavily) are not codebase search and keep the sticky."""
+    home = tmp_path / "home"
+    sid = "test-preserve-litellm-tavily"
+    (home / ".claude" / "state" / "auggie-first-pending").mkdir(
+        parents=True, exist_ok=True
+    )
+    sticky = _sticky_path(home, sid)
+    sticky.write_text("pending\n")
+    payload = {"session_id": sid, "tool_name": "mcp__litellm__Tavily-tavily_search"}
+    result = _run_hook(payload, fake_home=home)
+    assert result.returncode == 0, result.stderr.decode()
+    assert sticky.exists(), "sticky must survive non-Augment proxy tool calls"
+
+
 def test_unrelated_tool_preserves_sticky(tmp_path: Path) -> None:
     """A non-auggie tool name must not clear the sticky."""
     home = tmp_path / "home"
diff --git a/tests/hooks/test_auggie_flag_clear_mcp_prefix.py b/tests/hooks/test_auggie_flag_clear_mcp_prefix.py
index 3ec53a71..c64c13cc 100644
--- a/tests/hooks/test_auggie_flag_clear_mcp_prefix.py
+++ b/tests/hooks/test_auggie_flag_clear_mcp_prefix.py
@@ -114,6 +114,11 @@ _AUGGIE_PREFIX_RE = re.compile(
 )
 
 
+def _is_search_prefix(part: str) -> bool:
+    """Auggie prefixes plus the LiteLLM proxy's Augment prefix (issue #454)."""
+    return "auggie" in part or "augment_code" in part
+
+
 def _normalize_prefixes(raw: list[str]) -> set[str]:
     """Strip trailing ``.*`` (regex) and ``*`` (glob) so both forms compare equal."""
     out: set[str] = set()
@@ -131,7 +136,7 @@ def _extract_matcher_prefixes() -> set[str]:
         if "auggie" not in matcher:
             continue
         parts = matcher.split("|")
-        return _normalize_prefixes([p for p in parts if "auggie" in p])
+        return _normalize_prefixes([p for p in parts if _is_search_prefix(p)])
     return set()
 
 
@@ -142,7 +147,7 @@ def _extract_case_prefixes() -> set[str]:
     match = re.search(r"case\s+\"\$TOOL_NAME\"\s+in\s*\n\s*([^\n)]+)\)", body)
     assert match, "could not locate case body in auggie-flag-clear.sh"
     parts = match.group(1).split("|")
-    return _normalize_prefixes([p.strip() for p in parts if "auggie" in p])
+    return _normalize_prefixes([p.strip() for p in parts if _is_search_prefix(p)])
 
 
 def test_matcher_and_case_body_reference_same_auggie_prefixes() -> None:
@@ -175,3 +180,59 @@ def test_pr47_widened_prefixes_present_in_both_surfaces() -> None:
         f"auggie-flag-clear.sh case body missing mcp__auggie-mcp__ prefix; "
         f"got {sorted(case_prefixes)}"
     )
+
+
+def test_litellm_augment_prefix_present_in_both_surfaces() -> None:
+    """Issue #454 lands ``mcp__litellm__augment_code-`` in both files. Pin it."""
+    assert "mcp__litellm__augment_code-" in _extract_matcher_prefixes()
+    assert "mcp__litellm__augment_code-" in _extract_case_prefixes()
+
+
+def test_litellm_augment_proxy_clears_sticky(tmp_path: Path) -> None:
+    """The LiteLLM proxy's Augment search tool clears the sticky (issue #454)."""
+    home = tmp_path / "home"
+    sid = "test-litellm-augment"
+    (home / ".claude" / "state" / "auggie-first-pending").mkdir(
+        parents=True, exist_ok=True
+    )
+    _sticky_path(home, sid).write_text("pending\n")
+    payload = {
+        "session_id": sid,
+        "tool_name": "mcp__litellm__augment_code-augment_code_search",
+    }
+    result = _run_hook(payload, fake_home=home)
+    assert result.returncode == 0, result.stderr.decode()
+    assert not _sticky_path(home, sid).exists()
+    telemetry = (home / ".claude" / "logs" / "auggie-first.jsonl").read_text()
+    assert '"tool":"mcp__litellm__augment_code-augment_code_search"' in telemetry
+
+
+def test_litellm_tavily_proxy_does_not_clear_sticky(tmp_path: Path) -> None:
+    """A LiteLLM proxy tool that is not Augment search leaves the sticky in place."""
+    home = tmp_path / "home"
+    sid = "test-litellm-tavily"
+    (home / ".claude" / "state" / "auggie-first-pending").mkdir(
+        parents=True, exist_ok=True
+    )
+    _sticky_path(home, sid).write_text("pending\n")
+    payload = {"session_id": sid, "tool_name": "mcp__litellm__Tavily-tavily_search"}
+    result = _run_hook(payload, fake_home=home)
+    assert result.returncode == 0, result.stderr.decode()
+    assert _sticky_path(home, sid).exists()
+
+
+def _flag_clear_matcher(path: Path) -> str:
+    data = json.loads(path.read_text())
+    for entry in data["hooks"]["PostToolUse"]:
+        for h in entry.get("hooks", []):
+            if "auggie-flag-clear" in h.get("command", ""):
+                return entry.get("matcher", "")
+    return ""
+
+
+def test_plugin_and_src_flag_clear_matchers_agree() -> None:
+    """The plugin hooks.json flag-clear matcher must equal the src one."""
+    plugin_json = REPO_ROOT / "plugins" / "superclaude" / "hooks" / "hooks.json"
+    src_matcher = _flag_clear_matcher(HOOKS_JSON)
+    assert src_matcher, "src hooks.json has no auggie-flag-clear registration"
+    assert _flag_clear_matcher(plugin_json) == src_matcher
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
