36c5631536aac27f2178ed77be2a0e924dd4c42a
Review one task for spec compliance.

Task brief: ## Task 5: Update the sc-recommend skill and its plugin copy

Design section 3.2 item 1 and 3.7 item 1. In `src/superclaude/skills/sc-recommend/SKILL.md` add AUG, `mcp__litellm__Tavily-tavily_search`, `mcp__litellm__Tavily-tavily_extract` to `allowed-tools:` (line 4) before their direct twins and rewrite the call at about line 134 to the AUG phrase, keeping its degrade-to-Read sentence. In `src/superclaude/skills/sc-recommend/refs/plugin-ecosystem-sources.md` (about line 24) apply the Tavily phrase. Apply the identical edits to `plugins/superclaude/skills/sc-recommend/SKILL.md` and `plugins/superclaude/skills/sc-recommend/refs/plugin-ecosystem-sources.md`. In `src/superclaude/cli/recommend/prompts.py` (about line 146) and `src/superclaude/hooks/scripts/sc-recommend-phase0.sh` (about line 80) replace the call instruction with the AUG short form plus "repo from `git remote get-url origin`, default branch", keeping "Do not iterate file-by-file." and "Unavailable/empty ranking degrades to direct Read, never to a fabricated verified target." and the `auggie_status` output field.

Acceptance criteria:
- `cmp` of each src/plugin pair (`SKILL.md`, `refs/plugin-ecosystem-sources.md`) reports identical files.
- `uv run pytest tests -k recommend -v` passes; output saved to `./artifacts/t5-pytest.log`.
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
Start sha: 36c5631536aac27f2178ed77be2a0e924dd4c42a
Diff against the start snapshot: diff --git a/plugins/superclaude/skills/sc-recommend/SKILL.md b/plugins/superclaude/skills/sc-recommend/SKILL.md
index 9ff571e2..83d92f18 100644
--- a/plugins/superclaude/skills/sc-recommend/SKILL.md
+++ b/plugins/superclaude/skills/sc-recommend/SKILL.md
@@ -1,7 +1,7 @@
 ---
 name: sc-recommend
 description: "Build a refined, paste-ready prompt that hands the user's request off to the right local skill, command, agent, or native-tool sequence — only when delegation adds net value. Use this skill whenever the user asks 'which command should I use', 'how do I best prompt for X', 'help me invoke the right skill for Y', 'recommend a workflow for Z', or describes a task without naming a command. Also use proactively whenever the user pastes a goal that could plausibly map onto multiple skills/agents/commands in this repo and you would otherwise have to choose blindly. With --plugin, switches to ecosystem search (Claude plugin marketplaces + community skill repos) instead of the local project surface."
-allowed-tools: Read, Glob, Grep, Bash, mcp__auggie__codebase-retrieval, mcp__tavily__tavily_search, mcp__tavily__tavily_extract, WebFetch, WebSearch, Edit, Write, Agent, Task
+allowed-tools: Read, Glob, Grep, Bash, mcp__litellm__augment_code-augment_code_search, mcp__auggie__codebase-retrieval, mcp__litellm__Tavily-tavily_search, mcp__tavily__tavily_search, mcp__litellm__Tavily-tavily_extract, mcp__tavily__tavily_extract, WebFetch, WebSearch, Edit, Write, Agent, Task
 argument-hint: "[goal description] [--plugin] [--minstar <N>] [--eval none|quick|normal|deep]"
 category: utility
 ---
@@ -131,7 +131,7 @@ See `refs/surface-enumeration.md` for the full algorithm, the verification recor
 
 ### Step B — MANDATORY auggie semantic ranking
 
-Skip this step in matched mode (Step 0 matched a routing row) and set `auggie_status: skipped`. Otherwise, after enumeration, issue **one** `mcp__auggie__codebase-retrieval` query to semantically rank the enumerated surface against the user's request. Auggie is the speed lever: one semantic query ranks the whole surface; do not iterate file-by-file.
+Skip this step in matched mode (Step 0 matched a routing row) and set `auggie_status: skipped`. Otherwise, after enumeration, issue **one** codebase-search query to semantically rank the enumerated surface against the user's request. Codebase search: call `mcp__litellm__augment_code-augment_code_search` (`repo_owner`/`repo_name` from `git remote get-url origin`, `branch` = the repository's default branch; it sees pushed code only); if that tool is not available, call `mcp__auggie__codebase-retrieval`. For uncommitted or unpushed changes use codegraph or Grep. Auggie is the speed lever: one semantic query ranks the whole surface; do not iterate file-by-file.
 
 Query shape:
 
diff --git a/plugins/superclaude/skills/sc-recommend/refs/plugin-ecosystem-sources.md b/plugins/superclaude/skills/sc-recommend/refs/plugin-ecosystem-sources.md
index 26a2fc9b..b037b62e 100644
--- a/plugins/superclaude/skills/sc-recommend/refs/plugin-ecosystem-sources.md
+++ b/plugins/superclaude/skills/sc-recommend/refs/plugin-ecosystem-sources.md
@@ -21,7 +21,7 @@ Use, in order:
 
 1. **`/sc:research "<query>" --depth deep`** — preferred when the user wants depth (compatibility checks, version pinning, multiple candidates compared). Hand off via a refined prompt; do not run it inline.
 2. **`deep-research` agent** — when the user wants a single focused answer (e.g., "find one good Notion plugin"). One `Agent` call.
-3. **Tavily MCP directly** (`mcp__tavily__tavily_search`, `mcp__tavily__tavily_extract`) — when the search is shallow and `/sc:research` overhead is not justified.
+3. **Tavily MCP directly** (`mcp__litellm__Tavily-tavily_search` (else `mcp__tavily__tavily_search`), `mcp__litellm__Tavily-tavily_extract` (else `mcp__tavily__tavily_extract`)) — when the search is shallow and `/sc:research` overhead is not justified.
 4. **WebFetch / WebSearch** — last-resort fallback. Tavily generally has better signal-to-noise for plugin discovery.
 
 Never use `/tech-research` for this search: it investigates the local codebase, not the web.
diff --git a/src/superclaude/cli/recommend/prompts.py b/src/superclaude/cli/recommend/prompts.py
index be18cdce..9ea3ac46 100644
--- a/src/superclaude/cli/recommend/prompts.py
+++ b/src/superclaude/cli/recommend/prompts.py
@@ -143,8 +143,10 @@ A. Enumerate installed $HOME/.claude/commands/sc/*.md,
    prefer project then installed; skills prefer installed then project; agents
    prefer project then installed. Preserve a plugin-qualified namespace. Read
    both relevant surfaces where needed and disclose a material active-copy gap.
-B. Issue one mcp__auggie__codebase-retrieval query for the enumerated surface
-   and verbatim request. Unavailable/empty ranking degrades to direct Read,
+B. Issue one mcp__litellm__augment_code-augment_code_search (else
+   mcp__auggie__codebase-retrieval) query, repo from `git remote get-url
+   origin`, default branch, for the enumerated surface and verbatim request.
+   Do not iterate file-by-file. Unavailable/empty ranking degrades to direct Read,
    never to a fabricated verified target. Use the parent's resolved reference
    paths for the full surface-enumeration and net-value rules.
 C. Read the target's actual interface and relevant backing skill/references.
diff --git a/src/superclaude/hooks/scripts/sc-recommend-phase0.sh b/src/superclaude/hooks/scripts/sc-recommend-phase0.sh
index b486b2ec..5ce49935 100755
--- a/src/superclaude/hooks/scripts/sc-recommend-phase0.sh
+++ b/src/superclaude/hooks/scripts/sc-recommend-phase0.sh
@@ -77,8 +77,9 @@ Local mode, before emitting any recommendation:
      src/superclaude/examples/*-template.md, under `git rev-parse --show-toplevel`
      (only inside an IronClaude checkout: src/superclaude/commands/ exists there)
 
-3. Unless matched, issue ONE mcp__auggie__codebase-retrieval query that ranks
-   the enumerated surface against the user's verbatim request. Do not iterate
+3. Unless matched, issue ONE mcp__litellm__augment_code-augment_code_search
+   (else mcp__auggie__codebase-retrieval) query, repo from `git remote get-url
+   origin`, default branch, that ranks the enumerated surface against the user's verbatim request. Do not iterate
    file-by-file.
 
 4. Before any candidate enters the recommendation (each selected step when
diff --git a/src/superclaude/skills/sc-recommend/SKILL.md b/src/superclaude/skills/sc-recommend/SKILL.md
index 9ff571e2..83d92f18 100644
--- a/src/superclaude/skills/sc-recommend/SKILL.md
+++ b/src/superclaude/skills/sc-recommend/SKILL.md
@@ -1,7 +1,7 @@
 ---
 name: sc-recommend
 description: "Build a refined, paste-ready prompt that hands the user's request off to the right local skill, command, agent, or native-tool sequence — only when delegation adds net value. Use this skill whenever the user asks 'which command should I use', 'how do I best prompt for X', 'help me invoke the right skill for Y', 'recommend a workflow for Z', or describes a task without naming a command. Also use proactively whenever the user pastes a goal that could plausibly map onto multiple skills/agents/commands in this repo and you would otherwise have to choose blindly. With --plugin, switches to ecosystem search (Claude plugin marketplaces + community skill repos) instead of the local project surface."
-allowed-tools: Read, Glob, Grep, Bash, mcp__auggie__codebase-retrieval, mcp__tavily__tavily_search, mcp__tavily__tavily_extract, WebFetch, WebSearch, Edit, Write, Agent, Task
+allowed-tools: Read, Glob, Grep, Bash, mcp__litellm__augment_code-augment_code_search, mcp__auggie__codebase-retrieval, mcp__litellm__Tavily-tavily_search, mcp__tavily__tavily_search, mcp__litellm__Tavily-tavily_extract, mcp__tavily__tavily_extract, WebFetch, WebSearch, Edit, Write, Agent, Task
 argument-hint: "[goal description] [--plugin] [--minstar <N>] [--eval none|quick|normal|deep]"
 category: utility
 ---
@@ -131,7 +131,7 @@ See `refs/surface-enumeration.md` for the full algorithm, the verification recor
 
 ### Step B — MANDATORY auggie semantic ranking
 
-Skip this step in matched mode (Step 0 matched a routing row) and set `auggie_status: skipped`. Otherwise, after enumeration, issue **one** `mcp__auggie__codebase-retrieval` query to semantically rank the enumerated surface against the user's request. Auggie is the speed lever: one semantic query ranks the whole surface; do not iterate file-by-file.
+Skip this step in matched mode (Step 0 matched a routing row) and set `auggie_status: skipped`. Otherwise, after enumeration, issue **one** codebase-search query to semantically rank the enumerated surface against the user's request. Codebase search: call `mcp__litellm__augment_code-augment_code_search` (`repo_owner`/`repo_name` from `git remote get-url origin`, `branch` = the repository's default branch; it sees pushed code only); if that tool is not available, call `mcp__auggie__codebase-retrieval`. For uncommitted or unpushed changes use codegraph or Grep. Auggie is the speed lever: one semantic query ranks the whole surface; do not iterate file-by-file.
 
 Query shape:
 
diff --git a/src/superclaude/skills/sc-recommend/refs/plugin-ecosystem-sources.md b/src/superclaude/skills/sc-recommend/refs/plugin-ecosystem-sources.md
index 26a2fc9b..b037b62e 100644
--- a/src/superclaude/skills/sc-recommend/refs/plugin-ecosystem-sources.md
+++ b/src/superclaude/skills/sc-recommend/refs/plugin-ecosystem-sources.md
@@ -21,7 +21,7 @@ Use, in order:
 
 1. **`/sc:research "<query>" --depth deep`** — preferred when the user wants depth (compatibility checks, version pinning, multiple candidates compared). Hand off via a refined prompt; do not run it inline.
 2. **`deep-research` agent** — when the user wants a single focused answer (e.g., "find one good Notion plugin"). One `Agent` call.
-3. **Tavily MCP directly** (`mcp__tavily__tavily_search`, `mcp__tavily__tavily_extract`) — when the search is shallow and `/sc:research` overhead is not justified.
+3. **Tavily MCP directly** (`mcp__litellm__Tavily-tavily_search` (else `mcp__tavily__tavily_search`), `mcp__litellm__Tavily-tavily_extract` (else `mcp__tavily__tavily_extract`)) — when the search is shallow and `/sc:research` overhead is not justified.
 4. **WebFetch / WebSearch** — last-resort fallback. Tavily generally has better signal-to-noise for plugin discovery.
 
 Never use `/tech-research` for this search: it investigates the local codebase, not the web.
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
