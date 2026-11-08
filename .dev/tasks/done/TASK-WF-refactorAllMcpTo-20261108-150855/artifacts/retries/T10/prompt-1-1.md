7e2d4f62a08882ecf5134701524d1cffbd10dd64
Review one task for spec compliance.

Task brief: ## Task 10: Update command call sites and allow-lists

Design section 3.3 items 1-3. `src/superclaude/commands/validate-roadmap.md` line 6: same replacement as the validate-roadmap skill (`mcp__auggie-mcp__codebase-retrieval` becomes `mcp__litellm__augment_code-augment_code_search, mcp__auggie__codebase-retrieval`). AUG phrase at `auggie-review.md` (about line 92), `brainstorm.md` (157), `recommend.md` (49) and `plugins/superclaude/commands/recommend.md` (its own line), `reflect.md` (157, 165) and `plugins/superclaude/commands/reflect.md` (about 146, 154), `troubleshoot.md` (90, 98). Context7/Tavily phrase at `reflect.md` (170, 171) and its plugin copy (about 159, 160), `troubleshoot.md` (100, 101). Codegraph rows unchanged.

Depends on: Task 6

Acceptance criteria:
- `grep -rn 'mcp__auggie-mcp__' src/superclaude/commands plugins/superclaude/commands` finds nothing.
- `uv run pytest tests/commands tests/skills/test_tier2_tavily_consistency.py -v` passes; output saved to `./artifacts/t10-pytest.log`.
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
Start sha: 7e2d4f62a08882ecf5134701524d1cffbd10dd64
Diff against the start snapshot: diff --git a/plugins/superclaude/commands/recommend.md b/plugins/superclaude/commands/recommend.md
index 4414b706..bee76a3e 100644
--- a/plugins/superclaude/commands/recommend.md
+++ b/plugins/superclaude/commands/recommend.md
@@ -46,7 +46,7 @@ argument-hint: "<goal description> [--plugin] [--eval <mode>] [--minstar <N>]"
 `/sc:recommend` generates a **paste-ready prompt** that hands the user's goal off to the right delegation — or recommends native `Read`/`Edit`/`Glob`/`Grep`/`Bash` when no delegation adds net value. Every invocation:
 
 1. Reads the routing guide first (`~/.claude/HOW-WE-WORK.md`, else the skill's `refs/HOW-WE-WORK.md` in a plugin install, else `src/superclaude/core/HOW-WE-WORK.md`; inside an IronClaude checkout, where `src/superclaude/commands/` exists under `git rev-parse --show-toplevel`, the `src/` copy is read first). It matches the whole requested outcome (deliverable, explicitly named command or existing artifact, compatible mode/depth/output choices and how much it may change) to one routing row, not any single phrase. A matched row's applicable steps are returned in order, with exactly one selected alternative and their verified flags, and stop at the requested deliverable: a report-only or plan-only request gains no execution, commit or push step. If the objective stays ambiguous, it asks one question and stops. No hand-written keyword table.
-2. When no row matches, it enumerates the installed (`~/.claude/`), project (`.claude/`), plugin and (in an IronClaude checkout) `src/` surface (commands, skills, agents, templates) and issues one `mcp__auggie__codebase-retrieval` query to rank candidates against the verbatim request. In an IronClaude checkout an optional local cache may suggest a candidate first; a cache hit is only a hint that is re-verified like any live candidate, and the handoff is rebuilt from the current request's own inputs, never emitted verbatim. Matched rows, a missing guide and runs outside a checkout do not use the cache.
+2. When no row matches, it enumerates the installed (`~/.claude/`), project (`.claude/`), plugin and (in an IronClaude checkout) `src/` surface (commands, skills, agents, templates) and issues one `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`) query to rank candidates against the verbatim request. In an IronClaude checkout an optional local cache may suggest a candidate first; a cache hit is only a hint that is re-verified like any live candidate, and the handoff is rebuilt from the current request's own inputs, never emitted verbatim. Matched rows, a missing guide and runs outside a checkout do not use the cache.
 3. Verifies every candidate before it is emitted: the copy that would actually run, its declared interface (option tables, argument hints, Usage, documented positional or keyword syntax), its backing skill and the references relevant to the advertised behavior, and current lifecycle guidance (deprecated or retired targets are excluded). A missing command or skill is shown as `not installed: <name>`; a material disagreement between sources is reported as a contract gap, not a runnable command.
 4. Applies the guide's levels: a bounded direct edit may use native tooling; larger implementation goes to `/sc:workflow`, then `/sc:implement`; MDTM task files only on explicit request or an exceptional documented need. Otherwise it falls back to native tooling when delegation does not earn its overhead.
 5. Emits a hand-off envelope that states which files, reports, memory or external systems the selected steps change, and never restates the target's protocol logic inline or runs it.
diff --git a/plugins/superclaude/commands/reflect.md b/plugins/superclaude/commands/reflect.md
index 90e8e3a3..a4c48c1e 100644
--- a/plugins/superclaude/commands/reflect.md
+++ b/plugins/superclaude/commands/reflect.md
@@ -143,7 +143,7 @@ Do NOT proceed with protocol execution using only this command file. The full be
 
 ## MCP Integration
 
-- **Auggie** (primary, free retrieval): Wave 0-2 codebase grounding via `mcp__auggie__codebase-retrieval`. Offloads heavy retrieval to the free tier, keeping Claude tokens tight.
+- **Auggie** (primary, free retrieval): Wave 0-2 codebase grounding via `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`). Offloads heavy retrieval to the free tier, keeping Claude tokens tight.
 - **codegraph**: Wave 0-6 symbol, caller and impact lookup above the native Grep/Read floor (guide `~/.claude/CODEGRAPH.md`); UC-2 Step 1B.3 calls `/sc:impact` and logs production and test caller counts only.
 - **Context7**: Tier 2 only; consulted when the spec/diff references a framework or library by name.
 - **Tavily**: Tier 2 only; rate-limited; used for external-symptom lookups when documentation grounding can't resolve a deviation.
@@ -151,13 +151,13 @@ Do NOT proceed with protocol execution using only this command file. The full be
 
 ## Tool Coordination
 
-- **`mcp__auggie__codebase-retrieval`**: in-repo grounding (all waves)
+- **`mcp__litellm__augment_code-augment_code_search`** (else `mcp__auggie__codebase-retrieval`): in-repo grounding (all waves)
 - **`mcp__codegraph__codegraph_status` / `_search` / `_node` / `_callers` / `_callees` / `_impact`**: one readiness check, then definitions, outlines, callers and impact above the floor (§6 Code-graph evidence chain); `Skill sc:impact-protocol` for the Step 1B.3 counts
 - **`Grep` then `Read`**: symbol navigation floor — Grep for the definition (`def <name>|class <name>|function <name>`) then Read the range (§6.1 steps 2a/3, FR-2); Grep with a word-boundary pattern for references, then Read the call sites (step 4); best-effort Grep for `class .*\(<Base>\)` / `implements <Iface>` for the polymorphic implementor surface (step 3b, FR-1)
 - **`Bash` (verification run)**: UC-2 §6.1 step 5 / 5.5 — the project's own linter or type-checker plus scoped non-mutating tests/build, run under the §6.1.1 safety envelope (timeout, output cap, verb allowlist, mutation denylist) and feeding §10.4 Regression detection; `--no-verify` disables
 - **Read / Write / Edit on `docs/memory/reflect/deviation-patterns-<slug>.md`**: cross-session learning capture (§6.3 — 20-entry, 90-day retention); a tracked project file, no MCP server needed
-- **`mcp__context7__resolve-library-id` / `query-docs`**: external library grounding (Tier 2)
-- **`mcp__tavily__tavily_search`**: targeted web search (Tier 2, rate-limited)
+- **`mcp__litellm__context7-resolve-library-id` / `query-docs`** (else `mcp__context7__resolve-library-id` / `query-docs`): external library grounding (Tier 2)
+- **`mcp__litellm__Tavily-tavily_search`** (else `mcp__tavily__tavily_search`): targeted web search (Tier 2, rate-limited)
 - **`Task`**: spawn `root-cause-analyst`, `self-review`, `requirements-analyst`, `confidence-calibrator`, `rf-qa`, `rf-qa-qualitative`, `audit-validator`, `evidence-validator`, `socratic-mentor`
 - **`Skill`**: invoke `sc:adversarial-protocol` (Wave 4 merge debate), `task-builder` (Wave 6 remediation), `confidence-check` / `tech-research` (auxiliary)
 - **`Read` / `Grep` / `Glob`**: native fallback when MCPs are unavailable; file:line re-Read for evidence-validator
diff --git a/src/superclaude/commands/auggie-review.md b/src/superclaude/commands/auggie-review.md
index 41fff550..49a76c29 100644
--- a/src/superclaude/commands/auggie-review.md
+++ b/src/superclaude/commands/auggie-review.md
@@ -89,7 +89,7 @@ External tool (not MCP, but central): **`auggie` CLI** is the primary review eng
 - **Bash(git *)**: Resolve diff ranges, list changed files
 - **Read / Grep / Glob**: Validate Auggie's file:line citations against actual files
 - **mcp__codegraph__codegraph_status / _search / _node / _callers**: one readiness check, then definition and caller cross-checks of cited lines
-- **mcp__auggie__codebase-retrieval**: In-session codebase queries when validating findings without spawning a full Auggie subprocess
+- **`mcp__litellm__augment_code-augment_code_search`** (else `mcp__auggie__codebase-retrieval`): In-session codebase queries when validating findings without spawning a full Auggie subprocess
 - **Write**: Emit the markdown report and audit log under `--output-dir`
 - **Task**: Spawn the `auggie-reviewer` agent for the `--depth deep` cross-check pass (protocol Wave 2 step 5), passing the `model` parameter when `--revagent` is set (per-persona deep passes are Auggie CLI calls, not agents)
 
diff --git a/src/superclaude/commands/brainstorm.md b/src/superclaude/commands/brainstorm.md
index ab8db87d..5e1e4680 100644
--- a/src/superclaude/commands/brainstorm.md
+++ b/src/superclaude/commands/brainstorm.md
@@ -154,7 +154,7 @@ The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This sect
 - **Contract.** With `--output` the worker fields are added to the command's own `<output>/return-contract.yaml` beside every existing field, its own `status` included. With `--report-dir` the worker contract is a separate `<report-dir>/return-contract.yaml` that lists the own contract in `artifacts`. It is written on every other outcome, including each stop of Wave 0 of the skill (the stop text goes to `reason`). `report_path` is `merged-requirements.md` (null when the merge was not reached, and on `--dry-run`). The own status values success, partial, failed and dry-run map to succeeded, partial, failed and succeeded.
 - **Person-mode flags.** `--interactive` and its short form `-i` are refused before any work (contract `worker_status: failed`, the flag in `reason`). The Socratic dialogue proceeds on the best available context, and there is no other gate.
 - **Research.** Under `--unattended`, the research-light route (automatic, or an explicit `--research light`) invokes `/sc:research` with `--unattended --strategy planning --depth quick --report-dir <report-dir>/nested/research-<n>/`, and its contract is listed in `artifacts`, also when the call failed; the research-deep route (automatic, or an explicit `--research deep`) invokes `tech-research`, which has no Unattended mode, so research-deep is skipped and recorded in `enrichment_used` with `quality_tier: skipped`.
-- **Nested invocations.** The `/sc:analyze` codebase enrichment receives `--unattended --report-dir <report-dir>/nested/analyze-<n>/`, and the Wave 3 adversarial call receives `--unattended --output <report-dir>/nested/adversarial-<n>/` in place of `<output>/adversarial/`. `adversarial_artifacts_dir` and the nested contracts are listed in `artifacts`. `<n>` starts at 1 for each nested command, and the one retry of a nested call (the adversarial `F1` retry) uses the next number, so a nested directory is never reused. A codebase scan through `mcp__auggie__codebase-retrieval` or through the `fallback_1` tier (codegraph, then Glob and Grep) is not a nested command and writes no nested directory and no nested contract, so `nested/analyze-<n>/` is written only by a `/sc:analyze` call; `enrichment_used` records the scan's tier, which does not show whether that directory exists.
+- **Nested invocations.** The `/sc:analyze` codebase enrichment receives `--unattended --report-dir <report-dir>/nested/analyze-<n>/`, and the Wave 3 adversarial call receives `--unattended --output <report-dir>/nested/adversarial-<n>/` in place of `<output>/adversarial/`. `adversarial_artifacts_dir` and the nested contracts are listed in `artifacts`. `<n>` starts at 1 for each nested command, and the one retry of a nested call (the adversarial `F1` retry) uses the next number, so a nested directory is never reused. A codebase scan through `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`) or through the `fallback_1` tier (codegraph, then Glob and Grep) is not a nested command and writes no nested directory and no nested contract, so `nested/analyze-<n>/` is written only by a `/sc:analyze` call; `enrichment_used` records the scan's tier, which does not show whether that directory exists.
 - **Handoffs.** The `tasklist` and `task` handoffs are skipped and recorded: `status: partial` with one line in `unresolved_conflicts` (their skills do not accept the flag at this phase), and the Wave 0 check that their skills are installed is skipped too. The `design` and `none` handoffs are unchanged.
 - **Outward actions.** It pushes, commits and stages nothing.
 
diff --git a/src/superclaude/commands/recommend.md b/src/superclaude/commands/recommend.md
index 4414b706..bee76a3e 100644
--- a/src/superclaude/commands/recommend.md
+++ b/src/superclaude/commands/recommend.md
@@ -46,7 +46,7 @@ argument-hint: "<goal description> [--plugin] [--eval <mode>] [--minstar <N>]"
 `/sc:recommend` generates a **paste-ready prompt** that hands the user's goal off to the right delegation — or recommends native `Read`/`Edit`/`Glob`/`Grep`/`Bash` when no delegation adds net value. Every invocation:
 
 1. Reads the routing guide first (`~/.claude/HOW-WE-WORK.md`, else the skill's `refs/HOW-WE-WORK.md` in a plugin install, else `src/superclaude/core/HOW-WE-WORK.md`; inside an IronClaude checkout, where `src/superclaude/commands/` exists under `git rev-parse --show-toplevel`, the `src/` copy is read first). It matches the whole requested outcome (deliverable, explicitly named command or existing artifact, compatible mode/depth/output choices and how much it may change) to one routing row, not any single phrase. A matched row's applicable steps are returned in order, with exactly one selected alternative and their verified flags, and stop at the requested deliverable: a report-only or plan-only request gains no execution, commit or push step. If the objective stays ambiguous, it asks one question and stops. No hand-written keyword table.
-2. When no row matches, it enumerates the installed (`~/.claude/`), project (`.claude/`), plugin and (in an IronClaude checkout) `src/` surface (commands, skills, agents, templates) and issues one `mcp__auggie__codebase-retrieval` query to rank candidates against the verbatim request. In an IronClaude checkout an optional local cache may suggest a candidate first; a cache hit is only a hint that is re-verified like any live candidate, and the handoff is rebuilt from the current request's own inputs, never emitted verbatim. Matched rows, a missing guide and runs outside a checkout do not use the cache.
+2. When no row matches, it enumerates the installed (`~/.claude/`), project (`.claude/`), plugin and (in an IronClaude checkout) `src/` surface (commands, skills, agents, templates) and issues one `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`) query to rank candidates against the verbatim request. In an IronClaude checkout an optional local cache may suggest a candidate first; a cache hit is only a hint that is re-verified like any live candidate, and the handoff is rebuilt from the current request's own inputs, never emitted verbatim. Matched rows, a missing guide and runs outside a checkout do not use the cache.
 3. Verifies every candidate before it is emitted: the copy that would actually run, its declared interface (option tables, argument hints, Usage, documented positional or keyword syntax), its backing skill and the references relevant to the advertised behavior, and current lifecycle guidance (deprecated or retired targets are excluded). A missing command or skill is shown as `not installed: <name>`; a material disagreement between sources is reported as a contract gap, not a runnable command.
 4. Applies the guide's levels: a bounded direct edit may use native tooling; larger implementation goes to `/sc:workflow`, then `/sc:implement`; MDTM task files only on explicit request or an exceptional documented need. Otherwise it falls back to native tooling when delegation does not earn its overhead.
 5. Emits a hand-off envelope that states which files, reports, memory or external systems the selected steps change, and never restates the target's protocol logic inline or runs it.
diff --git a/src/superclaude/commands/reflect.md b/src/superclaude/commands/reflect.md
index 657ff714..3788a085 100644
--- a/src/superclaude/commands/reflect.md
+++ b/src/superclaude/commands/reflect.md
@@ -154,7 +154,7 @@ Do NOT proceed with protocol execution using only this command file. The full be
 
 ## MCP Integration
 
-- **Auggie** (primary, free retrieval): Wave 0-2 codebase grounding via `mcp__auggie__codebase-retrieval`. Offloads heavy retrieval to the free tier, keeping Claude tokens tight.
+- **Auggie** (primary, free retrieval): Wave 0-2 codebase grounding via `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`). Offloads heavy retrieval to the free tier, keeping Claude tokens tight.
 - **codegraph**: Wave 0-6 symbol, caller and impact lookup above the native Grep/Read floor (guide `~/.claude/CODEGRAPH.md`); UC-2 Step 1B.3 calls `/sc:impact` and logs production and test caller counts only.
 - **Context7**: Tier 2 only; consulted when the spec/diff references a framework or library by name.
 - **Tavily**: Tier 2 only; rate-limited; used for external-symptom lookups when documentation grounding can't resolve a deviation.
@@ -162,13 +162,13 @@ Do NOT proceed with protocol execution using only this command file. The full be
 
 ## Tool Coordination
 
-- **`mcp__auggie__codebase-retrieval`**: in-repo grounding (all waves)
+- **`mcp__litellm__augment_code-augment_code_search`** (else `mcp__auggie__codebase-retrieval`): in-repo grounding (all waves)
 - **`mcp__codegraph__codegraph_status` / `_search` / `_node` / `_callers` / `_callees` / `_impact`**: one readiness check, then definitions, outlines, callers and impact above the floor (§6 Code-graph evidence chain); `Skill sc:impact-protocol` for the Step 1B.3 counts
 - **`Grep` then `Read`**: symbol navigation floor — Grep for the definition (`def <name>|class <name>|function <name>`) then Read the range (§6.1 steps 2a/3, FR-2); Grep with a word-boundary pattern for references, then Read the call sites (step 4); best-effort Grep for `class .*\(<Base>\)` / `implements <Iface>` for the polymorphic implementor surface (step 3b, FR-1)
 - **`Bash` (verification run)**: UC-2 §6.1 step 5 / 5.5 — the project's own linter or type-checker plus scoped non-mutating tests/build, run under the §6.1.1 safety envelope (timeout, output cap, verb allowlist, mutation denylist) and feeding §10.4 Regression detection; `--no-verify` disables
 - **Read / Write / Edit on `docs/memory/reflect/deviation-patterns-<slug>.md`**: cross-session learning capture (§6.3 — 20-entry, 90-day retention); a tracked project file, no MCP server needed
-- **`mcp__context7__resolve-library-id` / `query-docs`**: external library grounding (Tier 2)
-- **`mcp__tavily__tavily_search`**: targeted web search (Tier 2, rate-limited)
+- **`mcp__litellm__context7-resolve-library-id` / `query-docs`** (else `mcp__context7__resolve-library-id` / `query-docs`): external library grounding (Tier 2)
+- **`mcp__litellm__Tavily-tavily_search`** (else `mcp__tavily__tavily_search`): targeted web search (Tier 2, rate-limited)
 - **`Task`**: spawn `root-cause-analyst`, `self-review`, `requirements-analyst`, `confidence-calibrator`, `rf-qa`, `rf-qa-qualitative`, `audit-validator`, `evidence-validator`, `socratic-mentor`
 - **`Skill`**: invoke `sc:adversarial-protocol` (Wave 4 merge debate), `sc:workflow-protocol` (Wave 6 remediation, plan route — the default), `task-builder` (Wave 6 remediation, MDTM route — only with `--remediate --depth deep`), `confidence-check` / `tech-research` (auxiliary)
 - **`Read` / `Grep` / `Glob`**: native fallback when MCPs are unavailable; file:line re-Read for evidence-validator
diff --git a/src/superclaude/commands/troubleshoot.md b/src/superclaude/commands/troubleshoot.md
index b35c991f..97593352 100644
--- a/src/superclaude/commands/troubleshoot.md
+++ b/src/superclaude/commands/troubleshoot.md
@@ -87,7 +87,7 @@ Do NOT proceed with protocol execution using only this command file. The full be
 
 ## MCP Integration
 
-- **Auggie** (primary, free retrieval): Tier 1, Wave 1.5 (documentation grounding fan-out across release artifacts + architectural docs + semantic restrictions), and Tier 2 codebase grounding via `mcp__auggie__codebase-retrieval`. Offloads heavy retrieval to a free / low-cost tier, keeping the Claude token budget tight.
+- **Auggie** (primary, free retrieval): Tier 1, Wave 1.5 (documentation grounding fan-out across release artifacts + architectural docs + semantic restrictions), and Tier 2 codebase grounding via `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`). Offloads heavy retrieval to a free / low-cost tier, keeping the Claude token budget tight.
 - **codegraph**: Tier 1 + Tier 2 symbol, caller and impact lookup (`codegraph_search`, `codegraph_node`, `codegraph_callers`, `codegraph_impact`); guide `~/.claude/CODEGRAPH.md`. Tier 1 writes the caller rows to `tier1-callers.md`; graph rows are leads, Read before citing.
 - **Native floor**: below codegraph, Tier 1 + Tier 2 symbol-level navigation with `Grep` for the definition (`def name`, `class name`, `function name`) then `Read` of the range, and `Grep` with a word-boundary pattern then `Read` of the call sites for references. Critical when the issue names a specific function or class.
 - **Context7**: Tier 2 when the symptom mentions a framework or library by name or the stack trace ends in third-party code; also the skill's conditional Tier 1 behaviour-definition fetch, not general Tier 1 web research.
@@ -95,10 +95,10 @@ Do NOT proceed with protocol execution using only this command file. The full be
 - **Native reasoning**: Tier 2 synthesis when reconciling competing hypotheses.
 ## Tool Coordination
 
-- **`mcp__auggie__codebase-retrieval`**: in-repo grounding (Tier 1 + Tier 2)
+- **`mcp__litellm__augment_code-augment_code_search`** (else `mcp__auggie__codebase-retrieval`): in-repo grounding (Tier 1 + Tier 2)
 - **`mcp__codegraph__codegraph_status` / `_search` / `_node` / `_callers` / `_impact`**: one readiness check, then symbol, caller and impact lookups (Tier 1 + Tier 2)
-- **`mcp__context7__resolve-library-id` / `query-docs`**: external library docs (Tier 2 and the skill's conditional Tier 1 behaviour-definition fetch)
-- **`mcp__tavily__tavily_search`**: targeted web search (Tier 2, rate-limited)
+- **`mcp__litellm__context7-resolve-library-id` / `query-docs`** (else `mcp__context7__resolve-library-id` / `query-docs`): external library docs (Tier 2 and the skill's conditional Tier 1 behaviour-definition fetch)
+- **`mcp__litellm__Tavily-tavily_search`** (else `mcp__tavily__tavily_search`): targeted web search (Tier 2, rate-limited)
 - **`Task`**: spawn `root-cause-analyst`, Tier 2 specialist agents, `confidence-calibrator`, `evidence-validator`, `self-review`
 - **`Skill`**: invoke `sc:adversarial-protocol` (Wave 4), `sc:workflow-protocol` (Wave 6, plan route), `task-builder` (Wave 6, `--depth deep` MDTM route), `/sc:reflect` (Wave 6)
 - **`Read` / `Grep` / `Glob`**: native floor for symbol, definition and caller lookups and the fallback when MCPs are unavailable; file:line validation
diff --git a/src/superclaude/commands/validate-roadmap.md b/src/superclaude/commands/validate-roadmap.md
index 06f69b9e..455b2dd8 100644
--- a/src/superclaude/commands/validate-roadmap.md
+++ b/src/superclaude/commands/validate-roadmap.md
@@ -3,7 +3,7 @@ name: sc:validate-roadmap
 description: "Validate roadmap pipeline outputs (roadmap.md, test-strategy.md, extraction.md) produced by `superclaude roadmap run`. Mirrors the CLI `roadmap validate` surface: single-agent reflection by default, adversarial merge when N≥2 agents; always exits 0 per NFR-006 with findings surfaced as console output."
 category: analysis
 complexity: advanced
-allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill, mcp__auggie-mcp__codebase-retrieval, mcp__codegraph__codegraph_search, mcp__codegraph__codegraph_node
+allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill, mcp__litellm__augment_code-augment_code_search, mcp__auggie__codebase-retrieval, mcp__codegraph__codegraph_search, mcp__codegraph__codegraph_node
 mcp-servers: [auggie, codegraph]
 personas: [analyzer, architect, qa]
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
