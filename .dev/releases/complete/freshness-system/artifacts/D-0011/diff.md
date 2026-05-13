--- .dev/releases/current/freshness-system/artifacts/D-0011/before.md	2026-05-12 19:54:15.168758348 +0000
+++ .dev/releases/current/freshness-system/artifacts/D-0011/after.md	2026-05-12 19:54:30.685143143 +0000
@@ -90,3 +90,51 @@
 Commands in `~/.claude/commands/sc/` — use `/sc:help` to list all available.
 Agents in `~/.claude/agents/` — delegated by skills and commands.
 Full behavioral specs (personas, MCP workflows, wave strategies) live in the skill files.
+
+## Context freshness discipline
+
+Long sessions accumulate **derived facts** in working memory: file paths,
+line numbers, IPs, credential IDs, mtime relationships. These age out
+silently when the user (or other agents) modifies the underlying files.
+The hook layer enforces this at edit time; this section binds the
+behavior for **citations made in chat responses with no tool call**, which
+hooks cannot catch.
+
+### The five content-signal triggers
+
+Treat the following as **mandatory re-verification triggers** before
+output:
+
+- **S1.** About to cite `file:line` or "at line N" of a specific file.
+- **S2.** About to issue an Edit / Write / replace_content / replace_symbol_body
+  / insert_*_symbol against a file. (Hook enforces; mention here for completeness.)
+- **S3.** About to assert that file A agrees or disagrees with file B.
+- **S4.** About to quote an IP, hostname, credential ID, port, path, or
+  config value tied to a specific source file.
+- **S5.** About to recommend an infrastructure change that depends on a
+  remembered fact.
+
+### Self-check pattern (factual phrasing)
+
+Before producing output that hits S1, S3, S4, or S5: ask, "Did I Read the
+source file in the last 5 tool calls of this turn, AND has nothing
+modified it since?" If the answer is no, OR uncertain, perform a fresh
+Read first. The cost of a Read is trivial compared to a wrong citation.
+
+### Refresh-tool selection
+
+Pick the refresh tool by the content type of the claim:
+
+| Content | Tool |
+|---|---|
+| Exact line numbers / file content | `Read` |
+| Symbolic queries (which function, where defined, what references) | `mcp__serena__find_symbol` / `find_referencing_symbols` |
+| Semantic / cross-cutting ("is there an X anywhere") | `mcp__auggie__codebase-retrieval` |
+| Runtime state (permissions, mounts, sockets) | `Bash` (user-executed read-only command) |
+
+### Session context envelope
+
+Every user prompt is prefixed with a `<session-context>` block injected
+by the UserPromptSubmit hook. Fields like `turn=`, `Δ=`, `git=dirty=...`,
+`changed_since_last_turn=...` are factual and current as of that prompt.
+Treat as ground truth for that turn; do not override from older context.
