a35c7979faa2e5dbb7f99ee6a949b6bf3f8023f4
Review one task for spec compliance.

Task brief: ## Task 4: Add the proxy Augment tool to the Auggie agents

Design section 3.1 items 6-7. Insert AUG before `mcp__auggie__codebase-retrieval` in the `tools:` line (line 5) of `src/superclaude/agents/auggie-reviewer.md`, `eval-docs-loader.md`, `reflect-reviewer.md`, `reuse-auditor.md`, `troubleshoot-analyst.md`. Rewrite the prose at `auggie-reviewer.md` (about lines 37, 81, 96, 115), `eval-docs-loader.md` (about lines 28, 36) and `rf-team-lead.md` (about line 147) to the AUG phrase; the `auggie-reviewer.md` "in-session" wording states that AUG sees the pushed branch only and the uncommitted diff is read with Read, Grep or codegraph. In the same change, update the closed roster in `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (about line 31) so it matches the new `troubleshoot-analyst.md:5` list exactly, and update the positive roster in `tests/troubleshoot/test_diagnostic_worker_contract.py` (about line 24); keep its negative fixture (about lines 154-155).

Acceptance criteria:
- The five agents list AUG immediately before `mcp__auggie__codebase-retrieval`; codegraph entries unchanged.
- `uv run pytest tests/troubleshoot tests/agents -v` passes; output saved to `./artifacts/t4-pytest.log`.
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
Start sha: a35c7979faa2e5dbb7f99ee6a949b6bf3f8023f4
Diff against the start snapshot: diff --git a/src/superclaude/agents/auggie-reviewer.md b/src/superclaude/agents/auggie-reviewer.md
index d3a6ac3d..16e91376 100644
--- a/src/superclaude/agents/auggie-reviewer.md
+++ b/src/superclaude/agents/auggie-reviewer.md
@@ -2,7 +2,7 @@
 name: auggie-reviewer
 description: Independent code-review specialist that performs a Claude-side review pass alongside Auggie's deep retrieval pass, used in /sc:auggie-review --depth deep for cross-validation
 category: analysis
-tools: [Read, Grep, Glob, Bash, mcp__auggie__codebase-retrieval, mcp__codegraph__codegraph_search, mcp__codegraph__codegraph_node, mcp__codegraph__codegraph_callers]
+tools: [Read, Grep, Glob, Bash, mcp__litellm__augment_code-augment_code_search, mcp__auggie__codebase-retrieval, mcp__codegraph__codegraph_search, mcp__codegraph__codegraph_node, mcp__codegraph__codegraph_callers]
 model: opus
 ---
 
@@ -34,7 +34,7 @@ The orchestrator passes you:
 
 1. **Read the diff (or file list) end-to-end before forming any findings.** Do not start emitting findings while you're still building a mental model. A premature pass produces shallow, scattered findings.
 2. **For each non-trivial change, pull adjacent context** with `Read` (or `codegraph_node`; when you only know the name, find the definition with `codegraph_search`, else Grep): the surrounding function, the callers, the callees. Most bugs hide in the join between the new code and the unchanged code around it.
-3. **Use `mcp__auggie__codebase-retrieval` for codebase-wide questions** ("are there other call sites that pass `null` here?", "what's the existing convention for this kind of error handling?"). This is cheap and complementary — you can call it without overlapping Auggie's primary pass because the Auggie pass is already done by the time you start.
+3. **Use codebase search for codebase-wide questions** ("are there other call sites that pass `null` here?", "what's the existing convention for this kind of error handling?"). Codebase search: call `mcp__litellm__augment_code-augment_code_search` (`repo_owner`/`repo_name` from `git remote get-url origin`, `branch` = the repository's default branch; it sees pushed code only); if that tool is not available, call `mcp__auggie__codebase-retrieval`. For uncommitted or unpushed changes use codegraph or Grep. This is cheap and complementary — you can call it without overlapping Auggie's primary pass because the Auggie pass is already done by the time you start.
 4. **Form findings in five categories**, with one example each so you don't pad:
    - **Invariant violations**: code that breaks an invariant the surrounding code relies on (e.g., a method that promises sorted output but no longer guarantees it).
    - **Comment / code mismatches**: docstring says one thing, code does another. These are gold; flag every one.
@@ -78,7 +78,7 @@ If you have no findings, return `findings: []` with an honest note in `notes_for
 - **Grep / Glob**: find related call sites, similar patterns, prior conventions. To locate a definition, Grep for `def <name>|class <name>|function <name>` and Read the range; to confirm who calls what, Grep with a word-boundary pattern for the symbol and Read the call sites
 - **`codegraph_search` / `codegraph_callers`**: where a symbol is defined and who calls it (`codegraph_node` for one symbol's body or a file outline). For symbols and callers use the codegraph tools per `~/.claude/CODEGRAPH.md`: only when the brief says `index_state: fresh`, passing the brief's `projectPath`; Read a row before citing it, and fall back to the Grep floor above when codegraph is not usable or returns nothing. Do not run the `codegraph` CLI through Bash
 - **Bash**: `git log -p --follow <file>` for blame-style context when an unfamiliar pattern needs justification; `wc -l`, `find` for sizing
-- **mcp__auggie__codebase-retrieval**: codebase-wide semantic queries (not the same as Auggie's deep pass — this is in-session, cheap, and you can use it freely)
+- **`mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`)**: codebase-wide semantic queries (not the same as Auggie's deep pass — this is cheap and you can use it freely). The proxy tool sees the pushed branch only, so read the uncommitted diff with Read, Grep or codegraph
 
 ## Focus Areas
 
@@ -93,7 +93,7 @@ You focus on what indexed-retrieval is bad at:
 - ❌ Hardcoded secrets (Auggie's pattern match wins)
 - ❌ Obvious SQL injection / XSS (Auggie's pattern match wins)
 - ❌ Repo-wide layering violations (Auggie's retrieval wins)
-- ❌ "Is this pattern used elsewhere" questions (delegate to `mcp__auggie__codebase-retrieval` once, don't re-derive)
+- ❌ "Is this pattern used elsewhere" questions (delegate to `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`) once, don't re-derive)
 
 ## Outputs
 
@@ -112,7 +112,7 @@ You focus on what indexed-retrieval is bad at:
 **Will:**
 
 - Produce independent findings focused on what indexed-retrieval misses
-- Use cheap codebase queries (`mcp__auggie__codebase-retrieval`, codegraph symbol tools, Read, Grep) freely
+- Use cheap codebase queries (`mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`), codegraph symbol tools, Read, Grep) freely
 - Honestly report coverage gaps in `notes_for_orchestrator`
 
 **Will Not:**
diff --git a/src/superclaude/agents/eval-docs-loader.md b/src/superclaude/agents/eval-docs-loader.md
index 62d116b2..9141e255 100644
--- a/src/superclaude/agents/eval-docs-loader.md
+++ b/src/superclaude/agents/eval-docs-loader.md
@@ -2,7 +2,7 @@
 name: eval-docs-loader
 description: Loads the CURRENT cliEval pipeline documentation, contracts, and CLI flag surface from source and returns a citation-bearing digest. Used by /sc:cli-eval as the mandatory fresh-context gate before either the create or run pipeline acts, so the skill never reasons from a stale or hardcoded flag list / schema field.
 category: analysis
-tools: Read, Grep, Glob, mcp__auggie__codebase-retrieval
+tools: Read, Grep, Glob, mcp__litellm__augment_code-augment_code_search, mcp__auggie__codebase-retrieval
 model: sonnet
 ---
 
@@ -24,17 +24,21 @@ source is a finding, not a gap to fill from memory.
 
 ## Model Preference
 
-Sonnet is sufficient: this is bounded reading + extraction, not open-ended reasoning. Use auggie
-(`codebase-retrieval`) first for breadth ("where is the eval click group", "what enumerates suites"),
-then Read the exact lines to cite.
+Sonnet is sufficient: this is bounded reading + extraction, not open-ended reasoning. Use codebase
+search first for breadth ("where is the eval click group", "what enumerates suites"), then Read the
+exact lines to cite. Codebase search: call `mcp__litellm__augment_code-augment_code_search`
+(`repo_owner`/`repo_name` from `git remote get-url origin`, `branch` = the repository's default
+branch; it sees pushed code only); if that tool is not available, call
+`mcp__auggie__codebase-retrieval`. For uncommitted or unpushed changes use codegraph or Grep.
 
 ## Tools
 
 - **Grep / Glob**: locate the click command group, schema `$defs`, exit-code constants, artifact-path
   builders without reading whole files.
 - **Read**: open the exact lines that back each cited fact.
-- **mcp__auggie__codebase-retrieval**: free, broad codebase context to find the right files fast
-  before precise Reads.
+- **`mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`)**:
+  free, broad codebase context to find the right files fast before precise Reads (the proxy tool
+  sees pushed code only).
 
 ## Canonical sources (re-read every run; cite what exists, flag what is missing)
 
diff --git a/src/superclaude/agents/reflect-reviewer.md b/src/superclaude/agents/reflect-reviewer.md
index 8fd5ee8b..6b9a99b7 100644
--- a/src/superclaude/agents/reflect-reviewer.md
+++ b/src/superclaude/agents/reflect-reviewer.md
@@ -2,7 +2,7 @@
 name: reflect-reviewer
 description: Restricted read-only deviation-audit agent for sc:reflect Wave-3. Audits completed work against its driving spec/tasklist and classifies every divergence under the 4-category deviation taxonomy (Authorized expansion / Necessary deviation / Drift / Regression). Spawned as one of N heterogeneous Tier-2 reviewers; carries a read-only tool allowlist (no Bash/Edit/Write/Task) so a reviewer can never mutate the repository it is auditing. Returns structured deviation findings; the orchestrator persists them.
 category: quality
-tools: Read, Grep, Glob, mcp__auggie__codebase-retrieval, mcp__codegraph__codegraph_search, mcp__codegraph__codegraph_node, mcp__codegraph__codegraph_callers, mcp__codegraph__codegraph_impact
+tools: Read, Grep, Glob, mcp__litellm__augment_code-augment_code_search, mcp__auggie__codebase-retrieval, mcp__codegraph__codegraph_search, mcp__codegraph__codegraph_node, mcp__codegraph__codegraph_callers, mcp__codegraph__codegraph_impact
 model: sonnet
 maxTurns: 50
 permissionMode: plan
diff --git a/src/superclaude/agents/reuse-auditor.md b/src/superclaude/agents/reuse-auditor.md
index 7cd6cdf8..0171c22b 100644
--- a/src/superclaude/agents/reuse-auditor.md
+++ b/src/superclaude/agents/reuse-auditor.md
@@ -2,7 +2,7 @@
 name: reuse-auditor
 description: Independent reuse/consolidation auditor. For each new or proposed component, fingerprints its behaviour, searches the repo for prior art (name-agnostic), scores a composite similarity signal, and returns reuse findings with a verdict (reuse-by-import | mirror-shape | extract-shared | distinct) + consolidation recommendation. Detection only — never classifies deviations or gates. Reusable by any skill (sc:reflect, /tdd, cleanup-audit, analyze, code-review).
 category: analysis
-tools: Read, Grep, Glob, mcp__auggie__codebase-retrieval, mcp__codegraph__codegraph_search, mcp__codegraph__codegraph_node, mcp__codegraph__codegraph_callers
+tools: Read, Grep, Glob, mcp__litellm__augment_code-augment_code_search, mcp__auggie__codebase-retrieval, mcp__codegraph__codegraph_search, mcp__codegraph__codegraph_node, mcp__codegraph__codegraph_callers
 model: sonnet
 maxTurns: 50
 permissionMode: plan
diff --git a/src/superclaude/agents/rf-team-lead.md b/src/superclaude/agents/rf-team-lead.md
index d0961a90..76f0e3ec 100644
--- a/src/superclaude/agents/rf-team-lead.md
+++ b/src/superclaude/agents/rf-team-lead.md
@@ -146,7 +146,7 @@ Before spawning ANY researchers, perform a lightweight scan to map the problem s
 
 1. **Glob** — Find relevant files by pattern
 2. **Grep** — Find content patterns (class names, function names, imports)
-3. **codebase-retrieval** — Semantic search for subsystem understanding
+3. **Codebase search** — Semantic search for subsystem understanding. Call `mcp__litellm__augment_code-augment_code_search` (`repo_owner`/`repo_name` from `git remote get-url origin`, `branch` = the repository's default branch; it sees pushed code only); if that tool is not available, call `mcp__auggie__codebase-retrieval`. For uncommitted or unpushed changes use codegraph or Grep.
 
 **Output**: For each track, produce a scope map:
 
diff --git a/src/superclaude/agents/troubleshoot-analyst.md b/src/superclaude/agents/troubleshoot-analyst.md
index 3f3ba578..bb3b6013 100644
--- a/src/superclaude/agents/troubleshoot-analyst.md
+++ b/src/superclaude/agents/troubleshoot-analyst.md
@@ -2,7 +2,7 @@
 name: troubleshoot-analyst
 description: Read-only diagnostic worker for sc:troubleshoot. Applies the assigned specialist lens, returns structured findings and inert experiment proposals, and leaves execution and artifact persistence to the parent.
 category: quality
-tools: Read, Grep, Glob, mcp__auggie__codebase-retrieval, mcp__codegraph__codegraph_search, mcp__codegraph__codegraph_node, mcp__codegraph__codegraph_callers, mcp__codegraph__codegraph_impact
+tools: Read, Grep, Glob, mcp__litellm__augment_code-augment_code_search, mcp__auggie__codebase-retrieval, mcp__codegraph__codegraph_search, mcp__codegraph__codegraph_node, mcp__codegraph__codegraph_callers, mcp__codegraph__codegraph_impact
 permissionMode: plan
 ---
 
diff --git a/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md b/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md
index 06804f30..493efab1 100644
--- a/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md
@@ -28,7 +28,7 @@ Diagnose a reported issue with the smallest amount of work that produces a high-
 This contract applies to every troubleshooting-owned native diagnostic worker in Waves 1.5, 1.6, 1.7, 3, 4 and the native review fallbacks in Wave 6. It does not change delegated skills' internal agents or user-run remediation executors.
 
 - **Profile, not persona permissions:** use `subagent_type=troubleshoot-analyst`. A documentation branch, specialist or `self-review` is its `lens_name`, never an unrestricted runtime agent type. Keep `confidence-calibrator` and `evidence-validator` on their existing restricted profiles. Do not use forked workers that inherit the parent's capabilities.
-- **Resolve before dispatch:** inspect `.claude/agents/troubleshoot-analyst.md` first, then `~/.claude/agents/troubleshoot-analyst.md` only if the project copy is absent. Read the selected definition; it must declare the closed roster `Read, Grep, Glob, mcp__auggie__codebase-retrieval, mcp__codegraph__codegraph_search, mcp__codegraph__codegraph_node, mcp__codegraph__codegraph_callers, mcp__codegraph__codegraph_impact`. Missing/empty rosters, extra tools or wildcards are invalid. A shadowing invalid project definition is not repaired by silently selecting the global copy. Record availability in the audit log.
+- **Resolve before dispatch:** inspect `.claude/agents/troubleshoot-analyst.md` first, then `~/.claude/agents/troubleshoot-analyst.md` only if the project copy is absent. Read the selected definition; it must declare the closed roster `Read, Grep, Glob, mcp__litellm__augment_code-augment_code_search, mcp__auggie__codebase-retrieval, mcp__codegraph__codegraph_search, mcp__codegraph__codegraph_node, mcp__codegraph__codegraph_callers, mcp__codegraph__codegraph_impact`. Missing/empty rosters, extra tools or wildcards are invalid. A shadowing invalid project definition is not repaired by silently selecting the global copy. Record availability in the audit log.
 - **No unrestricted fallback:** if the profile is missing or invalid, do not substitute a general-purpose worker or the specialist's unrestricted definition. Record that branch/card/review as unavailable and use the existing degraded, inline-analysis or reporting path without fabricating a returned artifact. Inline analysis does not authorize an experiment or bypass a required independent gate.
 - **Codegraph run state in every brief:** every `troubleshoot-analyst` brief (Waves 1.5, 1.6, 1.7, 3, 4 and 6) carries the Wave 1 readiness result: `index_state`, `checked_at`, `worktree_root` and the `projectPath` to pass on every codegraph call. The analyst calls codegraph only when `index_state: fresh` (`~/.claude/CODEGRAPH.md`); otherwise it stays on its Grep/Read floor.
 - **Parent-owned persistence:** pass the assignment, `lens_name`, existing evidence, required schema and parent-owned `output_path`. The worker returns complete data, not a claimed file path. The orchestrator writes each returned result to that path on receipt, before any read, calibration or downstream consumer. Preserve existing filenames and specialist identities. The already restricted calibrator/validator reports are persisted by the same parent receipt rule.
diff --git a/tests/troubleshoot/test_diagnostic_worker_contract.py b/tests/troubleshoot/test_diagnostic_worker_contract.py
index 251c7dcb..7fc8e283 100644
--- a/tests/troubleshoot/test_diagnostic_worker_contract.py
+++ b/tests/troubleshoot/test_diagnostic_worker_contract.py
@@ -21,6 +21,7 @@ TOOLS = {
     "Read",
     "Grep",
     "Glob",
+    "mcp__litellm__augment_code-augment_code_search",
     "mcp__auggie__codebase-retrieval",
     "mcp__codegraph__codegraph_search",
     "mcp__codegraph__codegraph_node",
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
