# Top 5 Targets for Octocode Integration

**Date:** 2026-05-30
**Stage:** 3 v2 (redo) — pre-brainstorm selection
**Method:** Re-rank across 40 agents × 24 skills × 41 commands using Value × (Cost⁻¹ + Risk⁻¹) from `octocode-fit-analysis.md`, **excluding MCP registration** (foundational, not a behavioral integration).

---

## Selection Criteria

The user's directive: "pick the top 5 to benefit the most from integrating octocode into their **processes or flows**." This rules out the foundational MCP registration entry (it's an install-step, not a process). The ranking centers on **where octocode genuinely changes how the surface does its work** — net of overlap with auggie/serena/Context7/Tavily/`gh` CLI.

Three filters applied:

1. **Genuine value-add** — surface does cross-repo research, package discovery, PR archaeology, or external pattern lookup (octocode's 3 unique capabilities from `octocode-research.md` §5).
2. **Behavioral integration** — touching the process/flow itself, not just declaring a tool.
3. **Reach** — preference for surfaces invoked by many downstream consumers.

---

## Final Top 5 (Ranked)

| Rank | Target | Surface Type | Score | Why it benefits most |
|---|---|---|---|---|
| 1 | **`deep-research` agent** (`src/superclaude/agents/deep-research.md`) | Agent | 45 | Workhorse research agent used by tech-research, tech-reference, troubleshoot, brainstorm. One integration cascades to all downstream consumers. Tool Selection Policy already structured for axis-based routing. |
| 2 | **`tech-research` skill Phase 4 Web Research** (`src/superclaude/skills/tech-research/SKILL.md:415-419`) | Skill | 40 | Phase 4 explicitly names "GitHub issues and discussions" + "community solutions to similar problems" as research targets. Currently handled by generic Tavily web search. Octocode operationalizes the intent that already exists in the prompt. |
| 3 | **`sc:research` command** (`src/superclaude/commands/research.md`) | Command | 36 | Direct user-facing research command. Adding octocode genuinely expands what `/sc:research` can find (cross-repo code, package ecosystem, real-world implementations). High visibility = high signal-to-noise on whether octocode delivers value. |
| 4 | **`sc-brainstorm-protocol` Wave 2A enrichment** (`src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:179-187`) | Skill | 32 | Brainstorming benefits massively from external precedents ("how have other projects solved this?"). Wave 2A's enrichment routing matrix is already designed for parallel, fail-open sources — octocode slots in as a new row. |
| 5 | **`sc:troubleshoot` command** (`src/superclaude/commands/troubleshoot.md:93-100`) | Command | 28 | Root-cause investigation often hinges on "has anyone else hit this error?" — octocode's PR archaeology + GitHub issue search directly answers this. Existing Tavily search returns blog noise; octocode returns code-anchored evidence. |

---

## Targets Considered But NOT in Top 5

| Target | Why excluded |
|---|---|
| MCP server registration (`install_mcp.py:29`) | Foundational install step, not a process/flow — already noted as Phase 0 prerequisite in v1 |
| `sc-roadmap-protocol` Wave 1B | Score 24 — most roadmaps extracted from local specs, not cross-repo precedent. Marginal value. |
| `sc:auggie-review` | Score 18 — auggie already handles the codebase-retrieval axis; adding octocode duplicates rather than expands |
| `sc:design` | Score 18 — context7 already serves canonical framework patterns; octocode wins only on niche "show me real implementations" queries |
| `rf-task-researcher` agent | Score 14 — primarily explores LOCAL codebase; auggie covers this better |
| All audit-* agents (`audit-scanner`, `audit-analyzer`, etc.) | Local audit scope — no cross-repo benefit |
| `confidence-check`, `task`, `task-builder` skills | Local task-execution focus — no benefit |
| Hooks (PostToolUse / PreToolUse) | Adds latency on every tool use — v1 brainstorm #4 already explored and self-deferred |
| `sc:cleanup`, `sc:cleanup-audit` | Local-repo operations — auggie + serena cover |
| Persona-bound integration (architect/backend/etc.) | No runtime persona state in the framework — would be documentation theater (v1 brainstorm #3 acknowledged this) |

---

## Stage 3 v2 Assignments

Each of the 5 targets gets ONE parallel brainstorm agent. Each agent reads `octocode-research.md` + `octocode-fit-analysis.md` + the target's source file, then performs a `/sc:brainstorm`-style ideation:

- **Generate 3-5 candidate integration designs** for that specific target
- **Adversarially evaluate** each (pros/cons, risks, what-it-cannot-do)
- **Recommend a single best approach** with rationale
- **Produce a concrete diff sketch** showing the actual file change

**Output files:**

- `brainstorm/01-deep-research-agent.md`
- `brainstorm/02-tech-research-phase4.md`
- `brainstorm/03-sc-research-command.md`
- `brainstorm/04-sc-brainstorm-wave2a.md`
- `brainstorm/05-sc-troubleshoot-command.md`

---

**Status:** Complete
**Next:** Spawn 5 parallel brainstorm agents.
