fdeba1a744a7db65b9ac1ea1e65a8997d57f83b4
Review one task for spec compliance.

Task brief: ## Task 2: Count proxy tools in the eval coverage gate

Design section 6.4. In `src/superclaude/cli/eval/coverage.py` add `"mcp__litellm__"` as a fourth entry of `_DEFAULT_MCP_TOOL_PREFIXES` (about lines 100-104), change the comment above it from three to four prefixes, and update the docstrings that enumerate the prefixes (about lines 9-10, 195, 253). Do not change `eval_covers_pattern` and do not add a `mcp_server.litellm` capability to `src/superclaude/cli/eval/capabilities.py`. In `src/superclaude/cli/eval/suites/real.yaml` update only the assertions (about lines 72, 80, 87, 94) that compare the whole flag-clear matcher string so they expect the Task 1 matcher; leave prompts, gates and the E16 Tavily entry unchanged. In `src/superclaude/cli/eval/suites/installer_sync_drift.yaml` (about lines 20, 65) update wording that lists the flag-clear case globs. Add a unit test in the existing coverage-gate test module under `tests/cli/eval/` asserting that the default filter selects a matcher `mcp__litellm__augment_code-.*` and that an eval expecting `mcp__litellm__augment_code-augment_code_search` covers it.

Depends on: Task 1

Acceptance criteria:
- `_DEFAULT_MCP_TOOL_PREFIXES` has four entries including `mcp__litellm__`; `capabilities.py` is unchanged (`git diff --quiet src/superclaude/cli/eval/capabilities.py`).
- `uv run pytest tests/cli/eval -v` passes including the new test; output saved to `./artifacts/t2-pytest.log`.
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
Start sha: fdeba1a744a7db65b9ac1ea1e65a8997d57f83b4
Diff against the start snapshot: 
diff --git a/src/superclaude/cli/eval/coverage.py b/src/superclaude/cli/eval/coverage.py
index a1dcfeaf..01aad3de 100644
--- a/src/superclaude/cli/eval/coverage.py
+++ b/src/superclaude/cli/eval/coverage.py
@@ -5,10 +5,10 @@ hook matcher pattern P registered in ``~/.claude/settings.json``, an
 eval MUST exist in the suite under test that issues a real tool call
 whose name matches P. The bug PR #49 fixed was exactly this class of
 silent regression — a matcher pattern broke and no eval noticed because
-no eval issued a matching tool call. The v1 surface covers the three
-known auggie-prefix matchers (``mcp__auggie__*``, ``mcp__auggie-mcp__*``,
-``mcp__airis-mcp-gateway__*``); future suites extend the coverage by
-declaring additional ``expect_tool_call`` inputs.
+no eval issued a matching tool call. The v1 surface covers the four
+known MCP-prefix matchers (``mcp__auggie__*``, ``mcp__auggie-mcp__*``,
+``mcp__airis-mcp-gateway__*``, ``mcp__litellm__*``); future suites extend
+the coverage by declaring additional ``expect_tool_call`` inputs.
 
 Public surface
 ==============
@@ -93,7 +93,7 @@ so the artifact can also be tar'd up without escaping.
 """
 
 
-# v1 covers these three MCP tool prefixes per design-spec §1.5. The
+# v1 covers these four MCP tool prefixes per design-spec §1.5. The
 # tuple is module-private because the default filter is exported as a
 # function — callers that need to extend coverage compose their own
 # predicate rather than mutating this list.
@@ -101,6 +101,7 @@ _DEFAULT_MCP_TOOL_PREFIXES: tuple[str, ...] = (
     "mcp__auggie__",
     "mcp__auggie-mcp__",
     "mcp__airis-mcp-gateway__",
+    "mcp__litellm__",
 )
 
 
@@ -196,7 +197,7 @@ def default_matcher_filter(pattern: str) -> bool:
     tool prefixes with built-in tool names — these are bookkeeping
     hooks that no eval needs to issue a tool call for. The v1 gate
     therefore restricts itself to matchers that mention one of the
-    three known auggie/airis MCP prefixes; T05.25 extends the
+    four known auggie/airis/litellm MCP prefixes; T05.25 extends the
     predicate as additional MCP tool families come online.
     """
     return any(prefix in pattern for prefix in _DEFAULT_MCP_TOOL_PREFIXES)
@@ -250,7 +251,8 @@ def eval_covers_pattern(spec: EvalSpec, pattern: str) -> bool:
     """Return ``True`` if ``spec`` issues any tool call matched by ``pattern``.
 
     ``pattern`` is compiled with :func:`re.search` so a matcher like
-    ``mcp__auggie__.*`` correctly anchors against the prefix. An
+    ``mcp__auggie__.*`` or ``mcp__litellm__augment_code-.*`` correctly
+    anchors against the prefix. An
     unparseable pattern returns ``False`` rather than raising so the
     gate can still report it as ``missing`` (with the regex error
     surfaced via the artifact payload).
diff --git a/src/superclaude/cli/eval/suites/installer_sync_drift.yaml b/src/superclaude/cli/eval/suites/installer_sync_drift.yaml
index 76f9cc0c..4364a0e2 100644
--- a/src/superclaude/cli/eval/suites/installer_sync_drift.yaml
+++ b/src/superclaude/cli/eval/suites/installer_sync_drift.yaml
@@ -17,7 +17,9 @@
 #      src/, not registered → end-user `superclaude install` skips it) and no
 #      STALE (registered, missing from src/ → install crashes).
 #   3. Cross-consistency between hooks.json PostToolUse matcher prefixes and
-#      auggie-flag-clear.sh case-body prefixes.
+#      auggie-flag-clear.sh case-body prefixes (mcp__auggie__*,
+#      mcp__auggie-mcp__*, mcp__airis-mcp-gateway__auggie_*,
+#      mcp__litellm__augment_code-*).
 #
 # WHY home_strategy=shared:
 #   `make verify-sync` MUST run against the actual repository tree — an
@@ -62,7 +64,9 @@ evals:
     #   - Installer Registration: _FRESHNESS_SCRIPTS list vs.
     #     src/superclaude/hooks/scripts/*.sh — flags MISSING + STALE entries.
     #   - Hooks Cross-Consistency: hooks.json PostToolUse matcher prefixes
-    #     vs. auggie-flag-clear.sh case-body prefixes.
+    #     vs. auggie-flag-clear.sh case-body prefixes (the four globs
+    #     mcp__auggie__*, mcp__auggie-mcp__*, mcp__airis-mcp-gateway__auggie_*,
+    #     mcp__litellm__augment_code-*).
     #
     # On clean tree the target prints "✅ All components in sync." and exits 0.
     # On drift it prints "❌ DRIFT" / "MISSING from _FRESHNESS_SCRIPTS" /
diff --git a/src/superclaude/cli/eval/suites/real.yaml b/src/superclaude/cli/eval/suites/real.yaml
index 52b207b3..df75aa00 100644
--- a/src/superclaude/cli/eval/suites/real.yaml
+++ b/src/superclaude/cli/eval/suites/real.yaml
@@ -69,8 +69,9 @@ evals:
   # E2.1 / E2.2 / E2.3 — auggie matcher-coverage trio. T05.03 authors
   # E2.1 with its full body; T05.04 / T05.05 land E2.2 / E2.3 bodies.
   # OQ-2 (D-0082 §3 hook-surface coverage map) freezes E2.1-3 as the
-  # static coverage triad for the PostToolUse `mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*`
-  # matcher. Splitting the original E2 parameterize block into three
+  # static coverage triad for the PostToolUse `mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*|mcp__litellm__augment_code-.*`
+  # matcher (the `mcp__litellm__augment_code-.*` branch, issue #454, has
+  # no E2 entry here; its hook behaviour is pinned by tests/hooks/). Splitting the original E2 parameterize block into three
   # static entries (vs. one ``parameterize:`` row) is mandated by two
   # v1 constraints: (a) per-entry `requires:` capability tags differ
   # (FR-CAP1 — D-0082 §6), and (b) no runtime template-substitution
diff --git a/tests/cli/eval/test_coverage_gate.py b/tests/cli/eval/test_coverage_gate.py
index 287b8014..f47c0dad 100644
--- a/tests/cli/eval/test_coverage_gate.py
+++ b/tests/cli/eval/test_coverage_gate.py
@@ -134,6 +134,14 @@ def test_eval_covers_pattern_handles_invalid_regex() -> None:
     assert eval_covers_pattern(spec, "[broken") is False
 
 
+def test_litellm_augment_matcher_is_selected_and_covered() -> None:
+    """Issue #454: the LiteLLM proxy Augment matcher is in scope and coverable."""
+    pattern = "mcp__litellm__augment_code-.*"
+    assert default_matcher_filter(pattern) is True
+    spec = _spec("E1", "mcp__litellm__augment_code-augment_code_search")
+    assert eval_covers_pattern(spec, pattern) is True
+
+
 def test_eval_covers_pattern_ignores_non_string_tool_calls() -> None:
     spec = EvalSpec(
         id="E1",

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
