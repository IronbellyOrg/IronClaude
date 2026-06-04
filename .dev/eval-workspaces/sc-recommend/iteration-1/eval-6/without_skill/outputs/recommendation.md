# Recommended Approach: `/sc:research` with parallel `tech-research` per skill

## Workflow

1. **Parallel comparative analysis** — Spawn 3 `tech-research` subagents (one per SKILL.md) to extract structure, triggers, MCP usage, sub-skill invocations, return contracts, and behavioral guarantees.
2. **Cross-skill synthesis** — Use `/sc:research` (or `sc-brainstorm-protocol`) to compare patterns: shared adversarial primitives, reflection hooks, tasklist generation seams, overlap/divergence.
3. **Grounding** — Use `mcp__auggie__codebase-retrieval` for cross-references (where each skill is invoked), `mcp__serena__find_symbol` for protocol callers, `Read` for exact citations.
4. **Output** — Structured research report under `.dev/research/` with findings, gap analysis, integration recommendations.

## Reason

These three SKILL.md files are large behavioral protocols that interlink (adversarial powers reflect and tasklist validation). Parallel fan-out beats sequential reading (3.5x faster, Wave -> Checkpoint -> Wave pattern), and `tech-research` produces the structured comparative report this kind of multi-artifact investigation requires. Auggie grounding prevents hallucinated cross-references.
