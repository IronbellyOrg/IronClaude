# Octocode Fit Analysis — Where Would It Add the Most Value?

**Date:** 2026-05-30
**Stage:** 2 of 3 (analysis → brainstorm)
**Input:** `octocode-research.md` (Stage 1 synthesis) + `research/02-integration-points.md` (codebase integration surface)
**Method:** `/sc:analyze`-style focused fit analysis across agents (40), skills (24), commands (40), and CLI pipelines (10) — scored by value × cost.

---

## Inventory Surveyed

| Surface | Count | Files |
|---|---|---|
| Skills | 24 | `src/superclaude/skills/` — `tech-research`, `tech-reference`, `sc-brainstorm-protocol`, `sc-roadmap-protocol`, `sc-auggie-review-protocol`, `sc-troubleshoot-protocol`, `task-builder`, `prd`, `tdd`, etc. |
| Agents | 40 | `src/superclaude/agents/` — `deep-research`, `deep-research-agent`, `auggie-reviewer`, `rf-task-researcher`, `system-architect`, `root-cause-analyst`, `security-engineer`, `python-expert`, etc. |
| Commands | 41 | `src/superclaude/commands/` — `analyze`, `auggie-review`, `brainstorm`, `design`, `implement`, `improve`, `research`, `roadmap`, `troubleshoot`, etc. |
| CLI Pipelines | 10 | `src/superclaude/cli/` — `audit`, `cleanup_audit`, `cli_portify`, `eval`, `pipeline`, `prd`, `roadmap`, `sprint`, `task_builder`, `tasklist` |

---

## Scoring Rubric

Each integration target scored across 3 dimensions (1–5 scale):

- **Value** — How much does octocode genuinely improve the surface vs. existing tools? Anchored on the "cross-repo + package ecosystem" unique value-add from Stage 1.
- **Cost (inverted)** — Effort + maintenance burden + context-tax. Lower cost = higher inverted score.
- **Risk (inverted)** — Supply-chain, breaking-change, scope-creep risk. Lower risk = higher inverted score.

**Total = Value × (Cost⁻¹ + Risk⁻¹)** — emphasizes value but penalizes high cost or risk.

---

## Top 10 Integration Candidates (Ranked)

| # | Target | Surface | Value | Cost⁻¹ | Risk⁻¹ | Total | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | **`deep-research` agent — add as 4th research axis** | Agent | 5 | 5 | 4 | 45 | **Top pick** |
| 2 | **`tech-research` skill Phase 4 web research** | Skill | 5 | 4 | 4 | 40 | Strong fit |
| 3 | **`sc:research` command** | Command | 4 | 5 | 4 | 36 | Strong fit |
| 4 | **`sc-brainstorm-protocol` Wave 2A enrichment matrix** | Skill | 4 | 4 | 4 | 32 | Strong fit |
| 5 | **MCP server registration in `install_mcp.py:29`** | CLI | 3 | 5 | 5 | 30 | Foundational (prereq for all others) |
| 6 | **`sc:troubleshoot` external-pattern lookup** | Command | 4 | 4 | 3 | 28 | Good fit |
| 7 | **`sc-roadmap-protocol` Wave 1B reference-roadmap discovery** | Skill | 3 | 4 | 4 | 24 | Moderate |
| 8 | **`sc:auggie-review` cross-repo pattern check** | Command | 3 | 3 | 3 | 18 | Moderate |
| 9 | **`sc:design` reference-architecture lookup** | Command | 3 | 3 | 3 | 18 | Moderate |
| 10 | **`rf-task-researcher` agent for codebase exploration** | Agent | 2 | 3 | 4 | 14 | Low — too redundant with auggie |

---

## Detailed Analysis — Top 5

### 1. `deep-research` agent — add as 4th research axis (Score: 45) ★ TOP PICK

**Location:** `src/superclaude/agents/deep-research.md:30-36` (Tool Selection Policy)

**Current state:** Defines a 3-axis model — Tavily (web), Context7 (library docs), Sequential (synthesis). Used by `tech-research`, `tech-reference`, `troubleshoot`, `brainstorm`, and downstream skills.

**Proposed change:**

```yaml
# In deep-research.md frontmatter `tools:` list, add:
- mcp__octocode__githubSearchCode
- mcp__octocode__githubGetFileContent
- mcp__octocode__githubSearchPullRequests
- mcp__octocode__packageSearch
- mcp__octocode__githubViewRepoStructure

# In the Tool Selection Policy, add 4th axis:
Axis 4: GitHub code-pattern discovery
  Primary: octocode (cross-repo semantic search, PR archaeology, package→repo resolution)
  Use when: question is "how do real projects implement X" or "what does package Y actually do"
  Avoid when: question is about local codebase (use auggie); about canonical library docs (use Context7)
```

**Why this scores highest:**

- **Value 5/5** — `deep-research` is the workhorse agent for every research-style task in the framework. Adding octocode here propagates to all downstream consumers (tech-research, troubleshoot, brainstorm) with one change.
- **Cost⁻¹ 5/5** — Pure declarative change (~15 lines in one file). No new code paths. The Tool Selection Policy pattern is already in place.
- **Risk⁻¹ 4/5** — Adding to one agent's frontmatter is reversible. Penalty for one point: this agent is invoked by many skills, so a bad octocode response (rate limit, hallucinated repo) propagates broadly.

**Highest-value queries this unlocks:**

- "How does `httpx` actually implement retry logic?" → `packageSearch(httpx)` → `githubViewRepoStructure` → `githubSearchCode("retry")` → `githubGetFileContent`
- "Show me 3 production examples of pydantic-ai agent registration" → `githubSearchCode("pydantic_ai.Agent")` → fan-out reads
- "Why did langchain change their tool calling API?" → `githubSearchPullRequests(repo=langchain-ai/langchain, query="tool calling")` → diff inspection

### 2. `tech-research` skill Phase 4 Web Research (Score: 40)

**Location:** `src/superclaude/skills/tech-research/SKILL.md:415-419` (Phase 4 agent prompts)

**Current state:** Phase 4 spawns N parallel web-research agents that target "official framework/engine documentation, design patterns and best practices, third-party tools/libraries/APIs, community solutions, GitHub issues and discussions, conference talks and technical blog posts." The "GitHub issues and discussions" target is **already named** but currently handled by Tavily web search.

**Proposed change:** Add octocode tools to the Web Research Agent Prompt template (line ~565–630), specifically the GitHub-archaeology subset:

- For "community solutions to similar problems" → use `githubSearchCode` instead of Tavily
- For "GitHub issues and discussions" → use `githubSearchPullRequests` + issue search
- For "third-party tools/libraries/APIs" → use `packageSearch` to resolve package → repo, then read source

**Why it scores high:**

- **Value 5/5** — Tech-research is one of the most expensive skills in the framework (30+ agents per Deep tier run). Octocode here would replace 2-4 Tavily searches per investigation with higher-quality first-party source reads.
- **Cost⁻¹ 4/5** — Requires editing the Web Research Agent Prompt template in SKILL.md (~30 lines) and updating the BUILD_REQUEST so the task builder embeds the right tools.
- **Risk⁻¹ 4/5** — Tech-research already has Phase 5 synthesis QA and Phase 6 validation gates that catch bad data. Penalty: rate limits could degrade an in-flight Deep-tier run.

### 3. `sc:research` command (Score: 36)

**Location:** `src/superclaude/commands/research.md`

**Current state:** "Deep web research with adaptive planning and intelligent search" — Tavily-first, with Sequential for synthesis.

**Proposed change:** Add octocode as a research source. Particularly valuable for `--mode code` or new `--mode github` mode that targets cross-repo investigation.

**Why it scores high:**

- **Value 4/5** — Direct user-facing command; users invoke this when they want research. Octocode genuinely expands what research can find.
- **Cost⁻¹ 5/5** — Self-contained command file (~50 lines). Add MCP server to frontmatter, document new modes.
- **Risk⁻¹ 4/5** — User-facing means failure visibility is high but blast radius is low (one command invocation).

### 4. `sc-brainstorm-protocol` Wave 2A enrichment matrix (Score: 32)

**Location:** `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:179-187`

**Current state:** Routing matrix dispatches parallel enrichment agents for `domain in {code, architecture, incident}` → codebase-retrieval (auggie). Quality-tier tracking handles partial failures.

**Proposed change:** Add an "octocode enrichment" row for `domain in {code, architecture}`. Each brainstorm spawns one octocode enrichment agent in parallel with the existing auggie enrichment, asking "how have similar projects solved this?"

**Why it scores high:**

- **Value 4/5** — Brainstorming benefits massively from external precedents ("React/Vue both solved this with X, Y respectively"). Currently only the framework's own auggie context informs brainstorms.
- **Cost⁻¹ 4/5** — Editing the routing matrix (~20 lines). The quality-tier system already handles octocode unavailability gracefully.
- **Risk⁻¹ 4/5** — Wave 2A is fail-open by design. Octocode failure = lower-quality brainstorm, not broken brainstorm.

### 5. MCP server registration in `install_mcp.py:29` (Score: 30)

**Location:** `src/superclaude/cli/install_mcp.py:29` (`MCP_SERVERS` registry)

**Current state:** Registry of installable MCP servers. New entries are 5-line dicts.

**Proposed change:**

```python
"octocode": {
    "name": "octocode",
    "description": "GitHub/GitLab/Bitbucket semantic code research (14 tools)",
    "transport": "stdio",
    "command": "npx -y octocode-mcp@14.2.0",  # PINNED version, never @latest
    "required": False,
    "api_key_env": "GITHUB_TOKEN",
    "api_key_description": "GitHub PAT (or use `gh auth login` for GH_TOKEN reuse)",
    "post_install_message": "Set LOG=false to opt out of octocode telemetry. Use TOOLS_TO_RUN=githubSearchCode,githubGetFileContent,githubSearchPullRequests,packageSearch,githubViewRepoStructure to restrict to cross-repo tools only.",
},
```

**Why it scores high but not top:**

- **Value 3/5** — Foundational but not transformative on its own. Registration only matters when something downstream uses it.
- **Cost⁻¹ 5/5** — One dict entry. Lowest possible effort.
- **Risk⁻¹ 5/5** — Registration is opt-in by users; doesn't auto-activate.

**Required pairing:** This MUST land before targets #1–#4 are usable. It's the prereq, not the headline.

---

## Honorable Mentions (not in top 5)

### #6: `sc:troubleshoot` command (Score: 28)

The troubleshoot protocol already uses Auggie + Serena + Context7 + Tavily. Adding octocode for "find GitHub issues/PRs from similar projects that match this error signature" is genuinely useful, but the existing 4-tool stack already covers most cases. Marginal value-add.

### #7: `sc-roadmap-protocol` Wave 1B (Score: 24)

Could use octocode to find reference roadmaps from similar projects. Useful for novel domains but most IronClaude roadmaps are extracted from local specs, not cross-repo precedent.

### Low-value targets (DO NOT integrate)

| Target | Reason to skip |
|---|---|
| `repo-index` agent | Pure local — auggie covers this |
| `task` skill execution | Local task file processing — no benefit from cross-repo |
| `confidence-check` skill | Local quality gate — no benefit |
| `sc:cleanup` / `sc:cleanup-audit` | Operates on local repo — auggie + serena cover this |
| `rf-task-builder` agent | Already uses Tavily for external context; octocode would duplicate |
| `audit-*` agents | Local audit scope — no benefit |
| Hook-level integration (PostToolUse) | Adds latency on every tool use; high noise-to-signal |

---

## Highest-ROI Integration Path (Sequenced)

If the team decides to adopt octocode, this is the minimum viable rollout:

**Phase A (foundational — 1 PR):**

1. Add octocode to `MCP_SERVERS` registry (#5) — pinned to v14.2.0, `LOG=false`, `TOOLS_TO_RUN` whitelist of cross-repo tools only
2. Document install steps in `docs/configuration/`

**Phase B (highest leverage — 1 PR):**

3. Update `deep-research` agent's Tool Selection Policy to add 4th axis (#1)
4. Add octocode tools to `deep-research` agent frontmatter `tools:` list

**Phase C (highest visibility — 1 PR):**

5. Update `tech-research` skill Phase 4 Web Research Agent Prompt template (#2)
6. Update `sc:research` command to mention new GitHub research mode (#3)

**Phase D (enrichment — 1 PR):**

7. Add octocode row to `sc-brainstorm-protocol` Wave 2A enrichment matrix (#4)

**Total scope:** 4 PRs, ~150 LoC of declarative changes, no new agents or skills required.

---

## The Stage-3 Brainstorm Question

Given the analysis above, the most natural Stage-3 target for parallel brainstorming is **#1: the `deep-research` agent integration**, because:

1. It scores highest (45)
2. It propagates value to all downstream consumers (tech-research, troubleshoot, brainstorm) without requiring per-skill changes
3. It has multiple plausible implementation paths (declarative-only? new persona? routing-aware?)
4. The trade-offs are non-obvious (when to prefer octocode vs Tavily vs Context7 vs auggie) — exactly what brainstorming is for

Stage 3 will spawn 6 parallel brainstorm agents, each proposing a **different integration approach** for the `deep-research` agent integration, with diverse perspectives (declarative purist, behavioral-router, persona-aware, hook-driven, sub-agent delegate, prompt-template-only). The final synthesis will pick the top 2-3 for recommendation.

---

**Status:** Complete
**Next:** Stage 3 — 6 parallel `/sc:brainstorm` agents proposing diverse integration approaches for target #1.
