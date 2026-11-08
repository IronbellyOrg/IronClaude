f89cc1825d4498ef8034c913d7b5e4b3e2a0f97e
Review one task for spec compliance.

Task brief: ## Task 7: Update the brainstorm, auggie-review and pr-submit skills

Design section 3.2 items 5-7. `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` (about lines 187, 195) and `refs/handoff-routing.md` (about line 16): Tier 1 primary names AUG then `mcp__auggie__codebase-retrieval`; `quality_tier: primary` is earned by either; the `fallback_1` and `skipped` chain is unchanged. `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md` (about lines 20, 225): AUG phrase at the MCP mentions only; the `auggie` CLI path and `mcp-servers:` line 10 are unchanged. `src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md` (about line 31): AUG phrase with `branch` = the PR head branch and a note that only pushed commits are visible. Apply the `mcp-servers:` metadata rule to `sc-brainstorm-protocol/SKILL.md` (line 15) and `sc-pr-submit-protocol/SKILL.md` (line 10).

Acceptance criteria:
- The brainstorm skill still contains its `fallback_1` and `skipped` tier text unchanged (`git diff` shows no removed line containing them).
- `uv run pytest tests -k "brainstorm or auggie_review or pr_submit" -v` passes; output saved to `./artifacts/t7-pytest.log`.
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
Start sha: f89cc1825d4498ef8034c913d7b5e4b3e2a0f97e
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-auggie-review-protocol/SKILL.md b/src/superclaude/skills/sc-auggie-review-protocol/SKILL.md
index 5464616d..e7eff8f9 100644
--- a/src/superclaude/skills/sc-auggie-review-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-auggie-review-protocol/SKILL.md
@@ -222,7 +222,8 @@ auggie --print \
 3. **File:line validation pass** (non-negotiable):
    - For each finding, `Read` the cited file at the cited line range. Confirm the line exists and (where possible) confirm the cited snippet actually appears on that line.
    - For PR/diff mode, additionally confirm the line is within the diff hunks (a finding citing a line nowhere near the changes is downgraded to "context" or dropped, depending on severity).
-   - For `needs-grounding` findings, attempt to ground them using `mcp__auggie__codebase-retrieval`, `codegraph_search` / `codegraph_callers` (definition and caller cross-check, only when `index_state: fresh`; then Read the line) or `Grep`. If grounding succeeds, promote; if not, drop and log.
+   - For `needs-grounding` findings, attempt to ground them using codebase search (below), `codegraph_search` / `codegraph_callers` (definition and caller cross-check, only when `index_state: fresh`; then Read the line) or `Grep`. If grounding succeeds, promote; if not, drop and log.
+     Codebase search: call `mcp__litellm__augment_code-augment_code_search` (`repo_owner`/`repo_name` from `git remote get-url origin`, `branch` = the repository's default branch; it sees pushed code only); if that tool is not available, call `mcp__auggie__codebase-retrieval`. For uncommitted or unpushed changes use codegraph or Grep.
 4. **Dedupe pass**:
    - Findings on the same `file:line` with similar titles → merge, keep the higher severity and union the evidence.
    - Findings that are restatements of the PR description's own caveats → drop with a note in the audit log.
diff --git a/src/superclaude/skills/sc-brainstorm-protocol/SKILL.md b/src/superclaude/skills/sc-brainstorm-protocol/SKILL.md
index 469fbd29..ff4b668b 100644
--- a/src/superclaude/skills/sc-brainstorm-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-brainstorm-protocol/SKILL.md
@@ -12,7 +12,7 @@ argument-hint: "<topic> [--proposals N] [--depth quick|standard|deep] [--strateg
 <!-- Extended metadata (for documentation, not parsed):
 category: orchestration
 complexity: advanced
-mcp-servers: [auggie-mcp, codegraph, tavily]
+mcp-servers: [litellm, auggie, codegraph, tavily]
 personas: [architect, analyzer, scribe]
 version: 2.0.0
 spec: .dev/eval-workspaces/sc-brainstorm/SPEC.md
@@ -184,7 +184,7 @@ Orchestrate parallel brainstorming via:
 
    | Condition | Action | Output |
    |-----------|--------|--------|
-   | `domain ∈ {code, architecture, incident}` AND NOT `--no-codebase` | Invoke `/sc:analyze <relevant-paths> --focus quality --depth quick` OR `mcp__auggie__codebase-retrieval` for quick scan | `enrichment/codebase-context.md` |
+   | `domain ∈ {code, architecture, incident}` AND NOT `--no-codebase` | Invoke `/sc:analyze <relevant-paths> --focus quality --depth quick` OR `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`) for quick scan | `enrichment/codebase-context.md` |
    | `--codebase` (forced) | Same as above regardless of domain | Same |
    | `--research light` OR (auto: topic mentions framework/library names not in project) | Invoke `Skill sc-research-protocol` with `--depth quick` (or `/sc:research` if standalone) | `enrichment/research-light.md` |
    | `--research deep` OR (auto: `--strategy enterprise` + novel topic) | Invoke `Skill tech-research` with topic | `enrichment/research-deep.md` |
@@ -193,6 +193,7 @@ Orchestrate parallel brainstorming via:
    Research depth/params are owned by `/sc:research` and `tech-research` — see RESEARCH_CONFIG.md; brainstorm selects the route only.
 
    **Under `--unattended`**: the research-light row invokes `/sc:research` with `--unattended --strategy planning --depth quick --report-dir <report-dir>/nested/research-<n>/` (`<n>` starts at 1; also for an explicit `--research light`) and lists the nested contract in `artifacts`, also when the call failed; the research-deep row invokes `tech-research`, which has no Unattended mode, so research-deep is skipped, also for an explicit `--research deep`, and recorded in `enrichment_used` with `quality_tier: skipped`. The codebase row invokes `/sc:analyze` with `--unattended --report-dir <report-dir>/nested/analyze-<n>/` (`<n>` starts at 1); the `mcp__auggie__codebase-retrieval` alternative and the `fallback_1` tier (codegraph, then native Glob and Grep, `refs/handoff-routing.md` Tier 2) are unchanged and write no nested directory and no nested contract, so `nested/analyze-<n>/` is written only by a `/sc:analyze` call, and `enrichment_used` does not show whether it exists. The nested contract is listed in `artifacts`, also when the call failed.
+   That codebase alternative is `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`); either tool is the alternative named above and earns `quality_tier: primary`.
 
 2. **Quality-tier tracking** (mandatory per enrichment source):
    - `primary` — first-choice source ran cleanly
diff --git a/src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md b/src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md
index 5dc0bea0..8646cf33 100644
--- a/src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md
+++ b/src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md
@@ -13,13 +13,14 @@ Loaded in Wave 2A. Defines the matrix of enrichment options and quality-tier fal
 - `domain ∈ {code, architecture, incident}` AND NOT `--no-codebase`, OR
 - `--codebase` (forced) regardless of domain
 
-**Tier 1 (primary)**: `mcp__auggie__codebase-retrieval`
+**Tier 1 (primary)**: `mcp__litellm__augment_code-augment_code_search`, then `mcp__auggie__codebase-retrieval`
 
+- Codebase search: call `mcp__litellm__augment_code-augment_code_search` (`repo_owner`/`repo_name` from `git remote get-url origin`, `branch` = the repository's default branch; it sees pushed code only); if that tool is not available, call `mcp__auggie__codebase-retrieval`. For uncommitted or unpushed changes use codegraph or Grep.
 - Two parallel queries (per existing brainstorm v1 pattern):
   - Query 1: `"{topic} - find relevant code, existing implementations, related components, and integration points"`
   - Query 2: `"Project architecture, structure, patterns, and conventions related to {topic_domain_area}"`
 - Output budget: ~800-1200 tokens summary per query
-- quality_tier: `primary`
+- quality_tier: `primary` (earned by either tool)
 - Under `--unattended` this tier writes no nested directory and no nested contract; `nested/analyze-<n>/` is written only by a `/sc:analyze` call (the skill's other codebase action), and the scan is recorded in `enrichment_used` with this tier's `quality_tier`.
 
 **Tier 2 (fallback_1)**: codegraph, then native Glob/Grep
diff --git a/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md b/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
index 4f125b04..ebb48e78 100644
--- a/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md
@@ -7,7 +7,7 @@ allowed-tools: Read, Grep, Glob, Write, Edit, Bash(gh *), Bash(git *), Bash(uv *
 <!-- Extended metadata (for documentation, not parsed):
 category: quality
 complexity: advanced
-mcp-servers: [auggie]
+mcp-servers: [litellm, auggie]
 personas: [analyzer, architect, security, qa, devops]
 -->
 
diff --git a/src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md b/src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md
index d1d8e8b4..1cdbbfdb 100644
--- a/src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md
+++ b/src/superclaude/skills/sc-pr-submit-protocol/refs/finding-verify.md
@@ -8,7 +8,8 @@ rather than authoring a new verifier.
 
 > **Inside the core-purity boundary (NFR-6).** This wave is **read-only**: it `Read`s cited lines and
 > spawns a read-only validator agent. It performs NO version-control mutation and contains no shell
-> command tokens. The verdict it emits (`verified` / `unverified`) is consumed by the FSM.
+> command tokens other than the read-only `git remote get-url origin` lookup that the codebase-search
+> step below names. The verdict it emits (`verified` / `unverified`) is consumed by the FSM.
 
 ## Governing rule — the hallucination contract (reuse, verbatim)
 
@@ -28,8 +29,11 @@ The structural grounding floor is the auggie-review **Wave-3 step-3 "File:line v
 1. For each finding, **`Read` the cited file at the cited line range**; confirm the line exists and
    (where possible) confirm the cited snippet actually appears on that line (`:207`).
 2. For PR/diff mode, additionally confirm the line is within the diff hunks (`:208`).
-3. For `needs-grounding` findings, attempt grounding via `mcp__auggie__codebase-retrieval` or `Grep`;
-   promote on success, **drop and log** on failure (`:209`).
+3. For `needs-grounding` findings, attempt grounding via codebase search or `Grep`;
+   promote on success, **drop and log** on failure (`:209`). Codebase search: call
+   `mcp__litellm__augment_code-augment_code_search` (`repo_owner`/`repo_name` from
+   `git remote get-url origin`, `branch` = the PR head branch; it sees pushed commits only); if
+   that tool is not available, call `mcp__auggie__codebase-retrieval`. For uncommitted or unpushed changes use codegraph or Grep.
 
 ## The delta C3a adds — "does the defect reproduce"
 
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
