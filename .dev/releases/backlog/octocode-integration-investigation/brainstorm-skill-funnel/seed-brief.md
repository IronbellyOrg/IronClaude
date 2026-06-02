---
topic: "Having all octocode usage flow through a separate unique skill designed specifically to dive into codebases that tech-research finds and look at the specific areas relevant to the work being done"
domain: architecture
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-05-30T06:38:00Z
---

# Seed Brief: octocode-skill-funnel

## Problem Statement

The current v2 octocode integration plan distributes octocode access across 6 different surfaces (T1 deep-research agent, T2 tech-research Phase 4, T3 /sc:research command, T4 sc-brainstorm Wave 2A, T5 /sc:troubleshoot, T6 /tdd). Each surface defines its own tool whitelist, anti-trigger rules, rate-limit handling, and failure semantics — leading to ~7 PRs and ~33-38 engineering hours of effort spread across the codebase.

The user is proposing an **alternative architectural pattern**: centralize ALL octocode access into a single dedicated skill (working name: `octocode-deep-dive` or similar) that other skills/agents/commands invoke when they need cross-repo investigation. Crucially, the new skill is invoked **downstream of tech-research** — tech-research identifies what external codebases/libraries are relevant to the work, then delegates targeted investigation of those codebases to the new skill.

This is essentially a **funnel pattern**: tech-research is the scoper, the new skill is the deep-diver, all consumers route through these two stages.

## Known Context

- **Existing investigation produced 6 distributed integration points** (T1-T6 in v2 roadmap) — this proposal is an alternative architectural pattern, not an additive one
- **Prior v1 brainstorm #5 explored a similar "sub-agent delegate" pattern** at the AGENT level (`github-pattern-researcher` agent). The current proposal lifts this to the SKILL level, which has different implications:
  - Skills can be invoked across multiple skills/commands/agents (broader reach than an agent)
  - Skills can hold richer state (MDTM task files, multi-phase pipelines)
  - Skills are heavier to invoke (more orchestration overhead per call)
- **Tech-research already has a Phase 2 scope discovery** that identifies external dependencies, libraries, and reference points — the natural handoff seam
- **Octocode's 14 tools cluster naturally into 3 categories**: cross-repo search (5 tools), local FS (4 tools), LSP (3 tools). The skill would whitelist cross-repo only (per `octocode-research.md` §6)
- **The framework already has the precedent for a dedicated research skill that wraps an MCP**: `tech-research` skill itself wraps Tavily/Context7. So a `octocode-deep-dive` skill wrapping octocode-mcp is structurally analogous

## Constraints

- Must NOT duplicate auggie/serena coverage of LOCAL codebase work (octocode tools restricted to cross-repo)
- Must honor Phase 0 install discipline: pinned version, `LOG=false`, `TOOLS_TO_RUN` whitelist, `ENABLE_LOCAL=false`
- Must integrate with existing MDTM task-file pattern if it spawns multi-phase work
- Must produce evidence-tagged outputs (`[PRECEDENT: owner/repo@path]`) per T6's hallucination safeguards
- Must respect GitHub Search API 30 req/min rate limit with budget tracking
- Must fail-open: caller skills proceed even if octocode-deep-dive returns nothing
- Must NOT require ALL caller skills to ship simultaneously — one skill replaces all of T1-T6 over time

## Success Criteria

- Single source of truth for octocode invocation (no duplicate tool whitelists across files)
- Caller skills (tech-research, troubleshoot, brainstorm, tdd, design) invoke via a clean contract — never touch octocode tools directly
- New skill scopes its investigation to "areas relevant to the work being done" — input contract carries enough context that the skill doesn't free-form search
- Net reduction in integration LoC vs the v2 plan (target: <50% of v2's ~510 LoC across 6 files)
- Failure modes centralized in one place (one rate-limit handler, one telemetry config, one fallback chain)
- Reusable across all top-5 v2 targets without per-caller customization

## Open Questions

1. **Trigger contract**: Does the new skill accept a list of "codebases to investigate" as input, or does it run its own discovery? If the former, what schema?
2. **Invocation cost**: Skills are heavier than direct tool calls. Is the orchestration overhead (spawning a skill, MDTM-style task file or simpler?) acceptable per-call, or does it need a lightweight mode?
3. **Stateful vs stateless**: Does the new skill persist findings (MDTM task file) or return findings synchronously to the caller?
4. **Tech-research dependency**: Is tech-research a HARD prerequisite (skill rejects invocation if no tech-research output is supplied), or can it be invoked standalone?
5. **Handoff back to caller**: How does the caller consume the skill's output? Single markdown file? Structured JSON? Streamed findings?
6. **Replacement vs additive to v2**: If this skill is adopted, do T1-T6 become deprecated, or do some retain direct octocode access for fast-path scenarios?
7. **Skill naming**: `octocode-deep-dive`? `external-codebase-research`? `cross-repo-investigation`? Names imply scope.

## Enrichment Context (Wave 2A)

The enrichment phase for this brainstorm references existing artifacts on disk rather than running fresh discovery:

| Source | Path | Quality Tier |
|---|---|---|
| Octocode capabilities + risks | `../octocode-research.md` | primary |
| Codebase fit analysis (40 agents × 24 skills × 41 commands) | `../octocode-fit-analysis.md` | primary |
| v1 sub-agent-delegate brainstorm (closest prior art) | `../brainstorm-v1-lenses-on-deep-research/05-sub-agent-delegate.md` | primary |
| v2 per-target brainstorms | `../brainstorm/01-deep-research-agent.md` through `06-tdd-skill.md` | primary |
| v2 final roadmap (the alternative this brainstorm critiques) | `../FINAL-RECOMMENDATIONS-v2.md` | primary |

All enrichment sources are pre-existing investigation artifacts. No fresh enrichment fetches performed.
