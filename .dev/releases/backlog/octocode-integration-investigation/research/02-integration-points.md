# Codebase Research 02: Integration Points

**Investigation type:** Integration Mapper
**Status:** Complete
**Date:** 2026-05-30

---

## MCP Server Registration Surface (file:line, how to add)

The IronClaude codebase has **two parallel MCP registration paths**:

### Path A: Legacy Individual Server Registry (`install_mcp.py`)

**File:** `/config/workspace/IronClaude/src/superclaude/cli/install_mcp.py`

The `MCP_SERVERS` dict at **line 29** is the authoritative registry for individual servers. Each entry is a dict with keys: `name`, `description`, `transport`, `command`, optionally `api_key_env`, `api_key_description`, `requires_global_binary`, `post_install_message`.

**Adding octocode-mcp as a one-liner:** Append one entry to the `MCP_SERVERS` dict at line 29:

```python
    "octocode": {
        "name": "octocode",
        "description": "GitHub/GitLab/Bitbucket semantic code research + local FS + LSP (14 tools)",
        "transport": "stdio",
        "command": "npx -y octocode-mcp@latest",
        "required": False,
        "api_key_env": "GITHUB_TOKEN",
        "api_key_description": "GitHub PAT (or use `gh auth login` to reuse GH_TOKEN)",
    },
```

The `install_mcp_server()` function at **line 516** handles the full install lifecycle: checks if already installed (line 537), prompts for API keys if needed (line 543), and invokes `claude mcp add --transport <transport> <name> -e KEY=VAL -- <command>` at **lines 597-614**.

**Citation:** `src/superclaude/cli/install_mcp.py:29-110` (MCP_SERVERS registry), `:516-641` (install_mcp_server function).

### Path B: AIRIS Gateway

**File:** `/config/workspace/IronClaude/src/superclaude/cli/install_mcp.py:17-25`

The `AIRIS_GATEWAY` dict points to a Docker-based unified gateway. Adding octocode here means adding it to the gateway's `mcp-config.json` (downloaded from the agiletec-inc repo at **line 23**), which is external to this repo.

**Recommendation:** Path A is the simplest integration — one dict entry + the existing install pipeline handles everything.

### Path C: Project-level `.mcp.json`

**File:** `/config/workspace/IronClaude/.mcp.json:1-13`

This file currently registers only `auggie-mcp`. The format follows the standard MCP JSON config:

```json
{
  "mcpServers": {
    "octocode": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "octocode-mcp@latest"],
      "env": {}
    }
  }
}
```

**Citation:** `.mcp.json:1-13`

### Path D: User-level `.claude/settings.json` (hooks only, no MCP servers)

**File:** `/config/workspace/IronClaude/.claude/settings.json:1-30`

The project-level `settings.json` only contains hooks (PreToolUse, PostToolUse), not MCP server registrations. MCP servers are registered via `claude mcp add` CLI, not via settings.json.

**Total integration effort for MCP registration: 1 dict entry in `install_mcp.py:29` + optional `.mcp.json` addition.**

---

## Skills System Integration Points

| Skill Path | MCP Hook | Octocode Value |
|---|---|---|
| `src/superclaude/skills/tech-research/SKILL.md` | Phase 2: Codebase Research Agents (line 398-403), Phase 4: Web Research Agents (line 415-419) | Octocode tools could augment "Integration Mapper" and "Pattern Investigator" agent types by searching GitHub repos for reference implementations of similar patterns. Currently relies on Tavily for web research (line 419 mentions "official framework/engine documentation, design patterns, third-party tools/libraries/APIs"). |
| `src/superclaude/skills/tech-reference/SKILL.md` | Phase 2: Deep Investigation, Phase 4: Web Research | When documenting a feature, octocode could find how similar features are implemented in other open-source repos, providing reference architecture. Currently uses Context7 for library docs + Tavily for external research. |
| `src/superclaude/skills/sc-research/SKILL.md` | Wave 2A: Context Enrichment (codebase-retrieval at line 183-187) | The brainstorm protocol's enrichment matrix routes `domain in {code, architecture}` to `/sc:analyze` or `auggie-mcp__codebase-retrieval`. Octocode could add a "GitHub reference implementations" enrichment source alongside the existing codebase and web sources. |
| `src/superclaude/skills/task-builder/SKILL.md` | Phase A.3: Scope Discovery (line 151) | During task file creation, octocode could search for similar task implementations across GitHub repos to inform the builder's checklist structure. |

**Skill Template for `octocode-research`:** The pattern from existing skills:

1. YAML frontmatter with `name:`, `description:`, `allowed-tools:`, optionally `mcp-servers:` and `personas:`
2. `## Why This Process Works` section
3. Variable Reference block
4. Input section
5. Depth Tiers table
6. Output Locations table
7. Execution Overview (Stage A / Stage B)
8. Agent Prompt Templates
9. Report Structure

**Citation:** `src/superclaude/skills/tech-research/SKILL.md:1-44` (frontmatter + structure), `src/superclaude/skills/tech-reference/SKILL.md:1-60` (similar pattern).

---

## Agent Integration Points

| Agent | File | Current Tools | Octocode Tools That Fit |
|---|---|---|---|
| **deep-research** | `src/superclaude/agents/deep-research.md:1-68` | Tavily-search, Tavily-extract, Context7, Sequential-thinking, WebSearch, WebFetch | `githubSearchCode`/`githubGetFileContent`/`githubViewRepoStructure` for finding GitHub reference implementations when researching "how does X work in practice". Tool Selection Policy (line 30-36) already defines primary/fallback patterns — octocode could be added as a "GitHub research" axis alongside Tavily (web) and Context7 (docs). |
| **rf-task-builder** | `src/superclaude/agents/rf-task-builder.md:444-452` | Tavily-search, Tavily-extract | Octocode could supplement the "Evidence-bound invariant preservation" (line 444-445) by finding how similar task files/checklists are structured in other repos. |
| **auggie-reviewer** | `src/superclaude/agents/auggie-reviewer.md:71-81` | auggie__codebase-retrieval, serena__find_symbol, Read, Grep, Glob, Bash | Octocode could add "cross-repo pattern review" — when reviewing a PR, finding how other repos handle the same pattern to flag inconsistencies or missing best practices. |
| **deep-research-agent** (agent definition) | `src/superclaude/agents/deep-research-agent.md` | Tavily-first, Context7 for docs | Same as deep-research above. The agent's "Execute web searches using Tavily MCP first" (line 26) could be extended to "search GitHub repos using octocode for implementation patterns." |

**Citation:** `src/superclaude/agents/deep-research.md:1-68` (full agent), `src/superclaude/agents/rf-task-builder.md:451` (Tavily-first web search), `src/superclaude/agents/auggie-reviewer.md:76-80` (current tool set).

---

## CLI Pipeline Integration Points

| Pipeline Stage | File:Line | Current External Lookups | Octocode Value |
|---|---|---|---|
| **Roadmap: extract** | `cli/roadmap/commands.py:113` (CLI step ID 1) | Reads spec file locally; no external lookups | Could augment extraction by searching GitHub for similar spec documents or requirement patterns. |
| **Roadmap: generate-{agent}** | `cli/roadmap/executor.py` (steps 2-3, parallel generation) | Context7 for template patterns | Octocode could pull reference roadmaps from similar open-source projects. |
| **Roadmap: test-strategy** | `cli/roadmap/executor.py` (step 9) | No external lookups | Could search GitHub for test strategies from projects with similar complexity profiles. |
| **Sprint: phase execution** | `src/superclaude/cli/sprint/executor.py` (via `process.py:73-95` ClaudeProcess) | Each phase spawns a Claude subprocess with `/sc:task-unified` command; MCP availability depends on session config | During execution, if a task involves unfamiliar patterns, octocode could provide reference implementations mid-phase without requiring a separate research step. |
| **Sprint: summarizer** | `src/superclaude/cli/sprint/summarizer.py:485-501` | Invokes model for narrative generation | Not directly applicable — local summarization. |
| **Tasklist: validate** | `src/superclaude/cli/tasklist/commands.py:73-173` | Validates against local roadmap.md | Not applicable — pure local fidelity check. |
| **Pipeline: generic** | `src/superclaude/cli/pipeline/process.py:36-156` (ClaudeProcess base) | Spawns claude subprocess; MCP tools available to subprocess | Octocode would be available to any pipeline step as an MCP tool in the subprocess context. |

**Citation:** `src/superclaude/cli/roadmap/commands.py:113-127`, `src/superclaude/cli/pipeline/process.py:73-95`.

---

## Command Integration Points

| Command | File:Line | Current External Tools | Octocode Value |
|---|---|---|---|
| **/sc:research** | `src/superclaude/commands/research.md:1-60` | Tavily MCP (primary), Sequential, Playwright, Serena (line 6) | Octocode adds "GitHub research" source — code-pattern discovery across GitHub repos. Particularly useful for "how is X implemented in production" queries. |
| **/sc:brainstorm** | `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:1-422` | Sequential, Serena, Auggie, Tavily | Wave 2A enrichment (line 171-200) — adding "octocode enrichment" row for `domain in {code, architecture}` gives brainstorming sessions access to real-world implementation examples. |
| **/sc:roadmap** | `src/superclaude/skills/sc-roadmap-protocol/SKILL.md:1-530` | Sequential, Context7, Serena | Wave 1B extraction (line 206-223) could use octocode to find similar projects' roadmaps. Wave 2 template discovery (line 225-261) could pull reference templates from GitHub. |
| **/sc:auggie-review** | `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md` | Auggie codebase-retrieval | Could add octocode as a "cross-repo review" dimension — comparing PR's approach to similar changes in other repos. |
| **/sc:adversarial** | `src/superclaude/commands/adversarial.md:1-182` | Sequential, Context7, Serena | When comparing designs, octocode could provide third-party reference points for "which approach is more common in the wild." |
| **/sc:analyze** | Command file in `src/superclaude/commands/` | Auggie, Serena, Context7 | Octocode could add "external pattern analysis" — finding how other repos implement similar architecture to benchmark against. |
| **/sc:troubleshoot** | `src/superclaude/commands/troubleshoot.md:93-100` | Auggie, Serena, Context7, Tavily | When root-causing issues, octocode could search GitHub issues/PRs from similar projects for known solutions. |

**Citation:** `src/superclaude/commands/research.md:6`, `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:15`, `src/superclaude/skills/sc-roadmap-protocol/SKILL.md:13`, `src/superclaude/commands/troubleshoot.md:93-100`.

---

## Hooks Integration Points

**Hook Configuration:** `/config/workspace/IronClaude/src/superclaude/hooks/hooks.json:1-95`

| Hook Event | File:Line | Current Behavior | Octocode Integration Opportunity |
|---|---|---|---|
| **PreToolUse (Edit-class)** | `hooks.json:35-45` + `freshness-pre-edit.sh:1-80` | Validates that the file was recently read before editing (freshness gate) | **Low value.** Safety gate, not lookup surface. Octocode would add latency to every edit. |
| **PostToolUse (Read)** | `hooks.json:47-58` + `freshness-post-read.sh` | Logs read operations to state files | **Medium value.** Could log which files are being read and trigger an octocode "similar files in other repos" lookup in async background. |
| **PostToolUse (Auggie)** | `hooks.json:59-68` + `auggie-flag-clear.sh` | Clears the auggie-first flag after first auggie tool use | **High value.** When auggie codebase-retrieval is used, a parallel octocode lookup could find how similar code patterns exist in other GitHub repos. |
| **UserPromptSubmit** | `hooks.json:24-33` + `freshness-user-prompt.sh` | Injects session context (git dirty, delta, cwd) | **Low value.** Adding octocode here would fire on every user message — too noisy. |
| **SessionStart** | `hooks.json:3-22` + `freshness-session-start.sh` | Reports git status, project info | **Low value.** Not a lookup surface. |
| **PreToolUse (workspace writes)** | `.claude/settings.json:3-14` (project-level hook) | Rejects writes to `-workspace/` dirs | **No value.** Pure safety gate. |

**New Hook Opportunity:** A `PostToolUse` hook matching `mcp__tavily__tavily-search|mcp__context7__query-docs` could fire octocode lookups in parallel when external docs/web searches are performed, finding GitHub repos that demonstrate the same patterns being searched for externally.

**Citation:** `src/superclaude/hooks/hooks.json:35-68`, `src/superclaude/hooks/scripts/freshness-pre-edit.sh:1-80`.

---

## Documentation Lookup Integration Points

| Location | File:Line | Current Approach | Octocode Augmentation |
|---|---|---|---|
| **deep-research agent** | `src/superclaude/agents/deep-research.md:26-36` | Tavily-first for web, Context7 for library docs | Octocode fills the gap between "web search" (Tavily) and "library docs" (Context7) — finding real-world implementation examples in GitHub repos. Adds a 4th "code pattern discovery" axis to the existing 3-axis model. |
| **tech-research skill** | `src/superclaude/skills/tech-research/SKILL.md:415-419` (Phase 4 Web Research) | Web agents search "official framework/engine documentation, design patterns, third-party tools/libraries/APIs, community solutions" | Octocode could augment Phase 4 for "implementation pattern" research topics. Instead of searching the web for patterns, octocode searches GitHub for actual repos implementing them. |
| **tech-reference skill** | `src/superclaude/skills/tech-reference/SKILL.md:24-29` | Codebase verification + web research | When documenting a feature, octocode could find comparable implementations in other repos for "Industry Patterns" or "Reference Implementations" sections. |
| **roadmap skill** | `src/superclaude/skills/sc-roadmap-protocol/SKILL.md:206-223` (Wave 1B extraction) | Extracts from local spec files; Context7 for template patterns | Could use octocode to find roadmaps/CHANGELOGs from similar projects to inform milestone sizing. |
| **troubleshoot command** | `src/superclaude/commands/troubleshoot.md:93-100` | Auggie + Serena + Context7 + Tavily | Octocode could search GitHub issues/PRs of the same library/framework for known issues matching the error pattern. |
| **design command** | `src/superclaude/commands/` (design.md) | Context7 for framework patterns, Sequential for analysis | Octocode could find reference architectures and design patterns from GitHub repos when designing new systems. |
| **brainstorm enrichment** | `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:171-200` (Wave 2A) | Auggie codebase + Tavily/web research | Octocode adds a "competitor/peer analysis" enrichment source — how do other similar projects solve this problem? |

**Citation:** `src/superclaude/agents/deep-research.md:26-36`, `src/superclaude/skills/tech-research/SKILL.md:415-419`, `src/superclaude/commands/troubleshoot.md:93-100`.

---

## Top 5 Highest-Value Integration Targets (ranked, with rationale)

### 1. MCP Server Registration (install_mcp.py:29)

**Rationale:** Lowest effort, highest leverage. Adding octocode to the `MCP_SERVERS` dict at `src/superclaude/cli/install_mcp.py:29` immediately makes it available to every skill, command, agent, and pipeline that already declares MCP dependencies. One dict entry unlocks the entire codebase. The existing `install_mcp_server()` function (line 516) handles API key prompting, installation, and registration automatically.
**Effort:** ~5 lines of config
**Impact:** Framework-wide availability

### 2. deep-research Agent Tool Selection Policy (agents/deep-research.md:30-36)

**Rationale:** The deep-research agent is the primary external research workhorse. Its Tool Selection Policy at `src/superclaude/agents/deep-research.md:30-36` already defines a clear 3-axis model (Tavily=web, Context7=docs, Sequential=synthesis). Adding octocode as a 4th axis ("GitHub code patterns") is a natural extension that requires only updating the policy document and the `tools:` frontmatter list (lines 5-15). This agent is invoked by tech-research, tech-reference, troubleshoot, and brainstorm protocols.
**Effort:** ~10 lines of agent definition updates
**Impact:** Amplifies every research workflow that uses this agent

### 3. tech-research Skill Phase 4 Web Research (skills/tech-research/SKILL.md:415-419)

**Rationale:** The tech-research skill's Phase 4 "Web Research" at `src/superclaude/skills/tech-research/SKILL.md:415-419` explicitly targets "design patterns and best practices, third-party tools/libraries/APIs, community solutions to similar problems, GitHub issues and discussions." This is a perfect fit for octocode. Adding octocode tool calls to Phase 4 agent prompts (line 574-672) would give research agents the ability to discover reference implementations alongside web sources.
**Effort:** ~20 lines of agent prompt template additions
**Impact:** Every deep technical investigation gains GitHub pattern discovery

### 4. brainstorm Wave 2A Enrichment Matrix (skills/sc-brainstorm-protocol/SKILL.md:179-187)

**Rationale:** The brainstorm protocol's enrichment routing matrix at `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:179-187` already dispatches parallel enrichment agents for codebase and web research. Adding an "octocode enrichment" row for `domain in {code, architecture}` would give brainstorming sessions access to real-world implementation examples from GitHub. The quality-tier tracking system (line 189-194) already handles partial failures gracefully.
**Effort:** ~15 lines in the routing matrix + quality tier
**Impact:** Every brainstorm gains external pattern awareness

### 5. PostToolUse Hook for Auggie (hooks/hooks.json:59-68)

**Rationale:** The existing `PostToolUse` hook matching `mcp__auggie__.*|mcp__auggie-mcp__.*` at `src/superclaude/hooks/hooks.json:59-68` fires after every auggie codebase retrieval. Extending this hook (or adding a new one) to also fire octocode lookups when auggie is used would create a "local + global" codebase awareness pattern: auggie searches the local repo, octocode searches GitHub for similar patterns. This is the most architecturally elegant integration because it piggybacks on existing behavioral triggers.
**Effort:** ~10 lines of hook config + new script
**Impact:** Automatic GitHub pattern discovery whenever codebase exploration happens

---

## Key Takeaways

1. **The MCP registry is the master switch.** `install_mcp.py:29` controls which servers are installable. Adding octocode there makes it available everywhere with zero additional integration code.
2. **Agent tool surfaces are declarative.** Agents like `deep-research.md` declare their tools in YAML frontmatter (lines 5-15). Adding octocode tools requires only frontmatter updates plus behavioral instructions.
3. **Skills already plan for GitHub research.** The tech-research skill's Phase 4 (line 419) explicitly mentions "GitHub issues and discussions" as a research target. Octocode would operationalize this intent.
4. **The enrichment pattern is proven.** The brainstorm protocol's Wave 2A (line 171-200) demonstrates parallel, fail-open enrichment with quality-tier tracking. Octocode fits this pattern perfectly.
5. **Hooks provide automatic activation.** The `PostToolUse(Auggie)` hook at `hooks.json:59-68` shows that behavioral triggers can activate lookups without explicit user requests.

---

## Gaps and Questions

1. **What is the exact octocode API surface?** This analysis was performed before web-01 landed — web-01 confirms the 14-tool surface (`githubSearchCode`, `githubGetFileContent`, `githubViewRepoStructure`, `githubSearchRepositories`, `githubSearchPullRequests`, `githubCloneRepo`, `packageSearch`, `localSearchCode`, `localViewStructure`, `localFindFiles`, `localGetFileContent`, `lspGotoDefinition`, `lspFindReferences`, `lspCallHierarchy`).
2. **Does octocode require authentication?** Yes — `GITHUB_TOKEN`/`OCTOCODE_TOKEN`/`GH_TOKEN`. Already accounted for in the `MCP_SERVERS` entry above.
3. **Rate limiting considerations:** The circuit breaker configuration at `src/superclaude/core/MCP.md:277-286` defines per-server thresholds. Octocode would need its own row in this table. GitHub Search API caps at 30 req/min.
4. **Fallback strategy:** If octocode is unavailable, fallback would likely be Tavily web search + `gh` CLI shell-out.
5. **Persona assignment:** Which personas should auto-activate octocode? Octocode might fit `architect`, `backend`, and `analyzer` based on `src/superclaude/core/CLAUDE.md:86-96`.
6. **Transport type:** Octocode is stdio (npx-based) — goes in `MCP_SERVERS` (Path A).

---

## Status: Complete
