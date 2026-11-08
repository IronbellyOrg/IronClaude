b21a58d193265e861a319f6003e4a3620cb55c30
Review one task for spec compliance.

Task brief: ## Task 8: Update `mcp-servers:` metadata in the remaining skills

Design section 3.2 item 8. Apply the metadata rule to the `mcp-servers:` line of these `SKILL.md` files under `src/superclaude/skills/`: `sc-issue-protocol` (line 10), `sc-cli-portify-protocol` (line 7), `sc-cleanup-audit-protocol` (line 6), `sc-adversarial-protocol` (line 12), `sc-cli-eval-protocol` (line 11), `sc-release-split-protocol` (line 13), `sc-roadmap-protocol` (line 13), `sc-tasklist-protocol` (line 7). Only add `litellm` where the line already names `auggie`, `auggie-mcp`, `context7` or `tavily`.

Acceptance criteria:
- Each of the eight lines names `litellm` first and no longer names `auggie-mcp`; no other line of those files changed.
- `uv run pytest tests/skills -v` passes; output saved to `./artifacts/t8-pytest.log`.
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
Start sha: b21a58d193265e861a319f6003e4a3620cb55c30
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-adversarial-protocol/SKILL.md b/src/superclaude/skills/sc-adversarial-protocol/SKILL.md
index 59112b78..2b2872b8 100644
--- a/src/superclaude/skills/sc-adversarial-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-adversarial-protocol/SKILL.md
@@ -9,7 +9,7 @@ allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill
 <!-- Extended metadata (for documentation, not parsed):
 category: analysis
 complexity: advanced
-mcp-servers: [context7]
+mcp-servers: [litellm, context7]
 personas: [architect, analyzer, scribe]
 -->
 
diff --git a/src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md b/src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md
index 13f408f2..ed2cdcf3 100644
--- a/src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md
@@ -3,7 +3,7 @@ name: sc:cleanup-audit-protocol
 description: "Multi-pass read-only repository audit producing evidence-backed cleanup recommendations"
 category: utility
 complexity: high
-mcp-servers: [codegraph, context7]
+mcp-servers: [litellm, codegraph, context7]
 personas: [analyzer, architect, devops, qa, refactorer]
 allowed-tools: Read, Grep, Glob, Bash(git *), Bash(wc *), Bash(find *), Bash(du *), TodoWrite, Task, Write, mcp__codegraph__codegraph_status, mcp__codegraph__codegraph_callers, mcp__codegraph__codegraph_files
 argument-hint: "[target-path] [--pass surface|structural|cross-cutting|all] [--batch-size N] [--focus infrastructure|frontend|backend|all]"
diff --git a/src/superclaude/skills/sc-cli-eval-protocol/SKILL.md b/src/superclaude/skills/sc-cli-eval-protocol/SKILL.md
index 9f815bc8..75d1799a 100644
--- a/src/superclaude/skills/sc-cli-eval-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-cli-eval-protocol/SKILL.md
@@ -8,7 +8,7 @@ argument-hint: "create|run [--name <stem>] [--from @<spec>] [--suite <name>] [--
 <!-- Extended metadata (for documentation, not parsed):
 category: testing
 complexity: advanced
-mcp-servers: [context7]
+mcp-servers: [litellm, context7]
 personas: [architect, analyzer, qa, scribe]
 version: 1.0.0
 -->
diff --git a/src/superclaude/skills/sc-cli-portify-protocol/SKILL.md b/src/superclaude/skills/sc-cli-portify-protocol/SKILL.md
index 0adfee9d..6d2925df 100644
--- a/src/superclaude/skills/sc-cli-portify-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-cli-portify-protocol/SKILL.md
@@ -4,7 +4,7 @@ description: "Full behavioral protocol for sc:cli-portify — port inference-bas
 category: development
 complexity: high
 allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task
-mcp-servers: [context7, auggie-mcp]
+mcp-servers: [litellm, context7, auggie]
 personas: [architect, analyzer, backend]
 argument-hint: "--workflow <skill-name-or-path> [--name <cli-name>] [--output <dir>] [--dry-run]"
 ---
diff --git a/src/superclaude/skills/sc-issue-protocol/SKILL.md b/src/superclaude/skills/sc-issue-protocol/SKILL.md
index eae97bb2..104ee159 100644
--- a/src/superclaude/skills/sc-issue-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-issue-protocol/SKILL.md
@@ -7,7 +7,7 @@ allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, Skill, AskUserQuestion
 <!-- Extended metadata (for documentation, not parsed):
 category: workflow
 complexity: advanced
-mcp-servers: [auggie, codegraph]
+mcp-servers: [litellm, auggie, codegraph]
 -->
 
 # /sc:issue protocol
diff --git a/src/superclaude/skills/sc-release-split-protocol/SKILL.md b/src/superclaude/skills/sc-release-split-protocol/SKILL.md
index 5d76c6fe..fb1d13d1 100644
--- a/src/superclaude/skills/sc-release-split-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-release-split-protocol/SKILL.md
@@ -10,7 +10,7 @@ argument-hint: "<spec-file-path> [--output dir] [--depth quick|standard|deep] [-
 <!-- Extended metadata (for documentation, not parsed):
 category: planning
 complexity: advanced
-mcp-servers: [context7]
+mcp-servers: [litellm, context7]
 personas: [architect, analyzer, scribe]
 version: 1.0.0
 -->
diff --git a/src/superclaude/skills/sc-roadmap-protocol/SKILL.md b/src/superclaude/skills/sc-roadmap-protocol/SKILL.md
index b0cba50d..dff34376 100644
--- a/src/superclaude/skills/sc-roadmap-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-roadmap-protocol/SKILL.md
@@ -10,7 +10,7 @@ argument-hint: "<spec-file-path> [--specs ...] [--multi-roadmap --agents ...] [-
 <!-- Extended metadata (for documentation, not parsed):
 category: planning
 complexity: advanced
-mcp-servers: [context7]
+mcp-servers: [litellm, context7]
 personas: [architect, scribe, analyzer]
 version: 2.0.0
 spec: SC-ROADMAP-V2-SPEC.md
diff --git a/src/superclaude/skills/sc-tasklist-protocol/SKILL.md b/src/superclaude/skills/sc-tasklist-protocol/SKILL.md
index 0e907517..eabfcd48 100644
--- a/src/superclaude/skills/sc-tasklist-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-tasklist-protocol/SKILL.md
@@ -4,7 +4,7 @@ description: "Deterministic roadmap-to-tasklist generator with integrated roadma
 category: utility
 complexity: high
 allowed-tools: Read, Glob, Grep, Write, Bash, TaskCreate, TaskUpdate, TaskList, TaskGet, Task, Skill
-mcp-servers: [context7]
+mcp-servers: [litellm, context7]
 personas: [analyzer, architect]
 argument-hint: "<roadmap-path> [--spec <spec-path>] [--output <output-dir>] [--no-reflect]"
 ---
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
