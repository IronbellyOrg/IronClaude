---
name: research
description: Deep web research with adaptive planning and intelligent search
category: command
complexity: advanced
mcp-servers: [litellm, tavily, playwright]
personas: [deep-research-agent]
---

# /sc:research - Deep Research Command

> **Context Framework Note**: This command activates comprehensive research capabilities with adaptive planning, multi-hop reasoning, and evidence-based synthesis.

## Triggers

- Research questions beyond knowledge cutoff
- Complex research questions
- Current events and real-time information
- Academic or technical research requirements
- Market analysis and competitive intelligence

## Context Trigger Pattern

```text
/sc:research "[query]" [--depth quick|standard|deep|exhaustive] [--strategy planning|intent|unified]
/sc:research "[query]" [--unattended] [--report-dir <dir>]
```

## Behavioral Flow

### 1. Understand (5-10% effort)

- Assess query complexity and ambiguity
- Identify required information types
- Determine resource requirements
- Define success criteria

### 2. Plan (10-15% effort)

- Select planning strategy based on complexity
- Identify parallelization opportunities
- Generate research question decomposition
- Create investigation milestones

### 3. TodoWrite (5% effort)

- Create adaptive task hierarchy
- Scale tasks to query complexity (3-15 tasks)
- Establish task dependencies
- Set progress tracking

### 4. Execute (50-60% effort)

- **Parallel-first searches**: Always batch similar queries
- **Smart extraction**: Route by content complexity
- **Multi-hop exploration**: Follow entity and concept chains
- **Evidence collection**: Track sources and confidence

### 5. Track (Continuous)

- Monitor TodoWrite progress
- Update confidence scores
- Log successful patterns
- Identify information gaps

### 6. Validate (10-15% effort)

- Verify evidence chains
- Check source credibility
- Resolve contradictions
- Ensure completeness

## Key Patterns

### Parallel Execution

- Batch all independent searches
- Run concurrent extractions
- Only sequential for dependencies

### Evidence Management

- Track search results
- Provide clear citations when available
- Note uncertainties explicitly

### Adaptive Depth

- **Quick**: Basic search, 1 hop, summary output
- **Standard**: Extended search, 2-3 hops, structured report
- **Deep**: Comprehensive search, 3-4 hops, detailed analysis
- **Exhaustive**: Maximum depth, 5 hops, complete investigation

Per-tier `search_depth`/`extract_depth` and map/crawl selection are defined by the research engine — see RESEARCH_CONFIG.md Depth Profiles.

## MCP Integration

- **Tavily**: Primary search, extraction, site-mapping (`tavily-map`) and domain-crawl (`tavily-crawl`) engine — see deep-research-agent / RESEARCH_CONFIG.md for routing
- **Native reasoning**: Complex reasoning and synthesis
- **Playwright**: JavaScript-heavy content extraction

## Output Standards

- Save reports to `claudedocs/research_[topic]_[timestamp].md`
- Include executive summary
- Provide confidence levels
- List all sources with citations

## Examples

```text
/sc:research "latest developments in quantum computing 2024"
/sc:research "competitive analysis of AI coding assistants" --depth deep
/sc:research "best practices for distributed systems" --strategy unified
```

## Unattended mode

The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:research` resolves itself.

- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument (the query is a quoted argument); otherwise nothing here applies and no worker contract is written.
- **Report directory.** `--report-dir <dir>` only. Without it the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome. `report_path` is the generated `claudedocs/research_<topic>_<timestamp>.md` file. `artifacts` lists any other file the run wrote; paths git ignores are left out (WC-4), and it is `[]` when nothing else listable was written. The run is succeeded when the report is written, and failed otherwise.
- **Person-mode flags.** Only `--strategy planning` runs without clarification, so an explicit `--strategy intent` or `--strategy unified` is refused before any work (contract `worker_status: failed`, the flag in `reason`).
- **Gates.** Under `--unattended` the strategy is `--strategy planning`, the strategy that runs without clarification; a run with no `--strategy` uses it. There is no other gate.
- **Nested invocations.** None.
- **Outward actions.** It pushes, commits and stages nothing.

## Boundaries

**Will**: Current information, intelligent search, evidence-based analysis
**Won't**: Make claims without sources, skip validation, access restricted content

## CRITICAL BOUNDARIES

**STOP AFTER RESEARCH REPORT**

This command produces a RESEARCH REPORT ONLY - no implementation.

**Explicitly Will NOT**:

- Implement findings or recommendations
- Write code based on research
- Make architectural decisions
- Create system changes based on research

**Output**: Research report (`claudedocs/research_*.md`) containing:

- Findings with sources
- Evidence-based analysis
- Recommendations (for human decision)
- Cited references

**Next Step**: After research completes, user decides next action. Use `/sc:design` for architecture or `/sc:implement` for coding.
