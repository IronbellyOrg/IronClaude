# Brainstorm: Deep Auggie-MCP Integration into sc:troubleshoot

**Date**: 2026-04-03
**Author**: RyanW + Claude (brainstorm session)
**Status**: PROPOSAL (backlog)
**Scope**: 2 concrete proposals for auggie-mcp integration into the troubleshoot pipeline

---

## Background

### Current State of sc:troubleshoot

The `sc:troubleshoot` command (`src/superclaude/commands/troubleshoot.md`) is a diagnosis-first utility that follows a 5-phase flow: Analyze, Investigate, Debug, Propose, Resolve. Its tool coordination is limited to basic primitives: Read, Bash, Grep, and Write. It has **zero MCP server integration** -- no auggie, no sequential, no context7. Its `mcp-servers` field is an empty array.

This means every troubleshooting session starts cold. The agent must manually discover project structure, locate relevant files, and build context through expensive sequential Read/Grep calls before it can even begin root cause analysis. For large codebases, this discovery phase can consume 30-60% of the session's token budget.

### What Auggie-MCP Provides

Auggie-MCP (`mcp__auggie-mcp__codebase-retrieval`) is a semantic codebase search server that:
- Accepts natural language queries about a codebase
- Returns relevant code, symbols, architecture, and integration points
- Operates at near-zero token cost (the retrieval itself is cheap; only the ~500-800 token briefing enters the context)
- Already proven in `sc:brainstorm` (Phase 0 codebase awareness) and `sc:task-unified` (STRICT/STANDARD tier pre-loading)

### Gap

`sc:troubleshoot` is the command that would benefit *most* from pre-loaded codebase context -- debugging is fundamentally about understanding how code connects -- yet it is the only major diagnostic command with no MCP integration at all.

---

## Proposal 1: Context-Primed Diagnosis (Phase 0 Injection)

### Summary

Add a mandatory "Phase 0: Context Loading" step to `sc:troubleshoot` that fires two parallel auggie-mcp queries before any diagnosis begins. This front-loads codebase understanding so the Investigate and Debug phases can skip expensive manual discovery.

### Rationale

The current troubleshoot flow assumes the agent starts from zero knowledge of the codebase. In practice, 80%+ of troubleshooting sessions involve code the agent has never seen. The agent spends significant tokens on exploratory Grep/Read calls just to orient itself -- calls that auggie can replace with a single semantic retrieval returning structured context.

The `sc:brainstorm` command already demonstrates this exact pattern (Phase 0 codebase awareness with two parallel queries). The `sc:task-unified` STRICT tier also loads context via `codebase-retrieval` as step 3. This proposal adapts the proven pattern to the troubleshooting domain.

### Implementation Approach

**1. Add auggie-mcp to the command frontmatter:**

```yaml
mcp-servers: [auggie-mcp]
personas: [analyzer]
```

**2. Insert Phase 0 before the existing Phase 1 (Analyze):**

```
Phase 0: Context Loading (automatic, pre-diagnosis)
  - Fire two parallel auggie queries:
    Query A (Issue-Specific):
      information_request: "{issue_description} - find relevant code, error handlers,
                            related components, recent changes, and test coverage"
      directory_path: "{cwd}"
    Query B (Architecture Scan):
      information_request: "Project architecture, error handling patterns, logging
                            infrastructure, and dependency graph related to {issue_domain}"
      directory_path: "{cwd}"
  - Synthesize into a structured briefing (500-800 tokens):
      Relevant Code: [file:line descriptions]
      Error Handling Patterns: [how the project handles errors in this area]
      Related Tests: [existing test files that cover this area]
      Recent Changes: [files recently modified in this area]
      Dependency Chain: [what calls what in this area]
```

**3. Modify Phase 1 (Analyze) to consume the briefing:**

Instead of starting with blind Grep/Read, the Analyze phase begins with the auggie briefing already in context. It can immediately focus on the specific files and patterns identified, skipping the discovery loop.

**4. Add fallback for auggie unavailability:**

```
If auggie unavailable:
  1. Serena: get_symbols_overview on project root (depth: 1)
  2. Grep: search for error message / stack trace keywords
  3. Glob: find files matching issue-related patterns
  Prefix diagnosis with: "Note: Limited codebase awareness (Auggie unavailable)"
```

### Expected Benefits

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Discovery tokens (orient in codebase) | 2,000-8,000 | 500-800 (briefing) | 60-90% reduction |
| Time to first hypothesis | 3-5 tool calls | 1 tool call (parallel) | 60-80% faster |
| Root cause accuracy (first attempt) | ~50% (cold start guessing) | ~75% (context-informed) | +25pp |
| Total session tokens (typical bug fix) | 8,000-15,000 | 5,000-10,000 | 30-40% reduction |

The biggest win is in the "discovery loop" -- the repeated Grep-then-Read cycles where the agent searches for relevant code. Auggie replaces this entire loop with a single semantic query that returns the right files up front.

### Trade-offs

- **Adds ~500-800 tokens of context** to every troubleshoot session, even simple ones where the user already pointed at the exact file. Mitigation: the `--type` flag could gate the depth of the auggie query (e.g., `--type bug` gets full context, `--type build` gets lighter context since build issues are usually self-contained in config files).
- **Auggie dependency**: if the auggie server is down, the fallback path (Serena + Grep) is slower than just doing Grep directly, since it tries auggie first. Mitigation: circuit breaker pattern (already defined in MCP.md -- 3 failures, 45s timeout, fallback to Serena + Grep/Glob).
- **Query quality depends on issue description**: vague descriptions like "it's broken" yield poor auggie results. Mitigation: if the issue description is under 10 words, Phase 0 should ask a clarifying question before querying auggie, or broaden the query to a general architecture scan.

---

## Proposal 2: Iterative Hypothesis-Driven Retrieval (Auggie-in-the-Loop)

### Summary

Instead of a single front-loaded context load, embed auggie-mcp as a first-class tool within the Investigate and Debug phases. Each time the agent forms a hypothesis about the root cause, it fires a targeted auggie query to validate or refute that hypothesis before spending tokens on manual code reading. This creates a tight "hypothesize, retrieve, evaluate" loop that dramatically reduces wasted exploration.

### Rationale

Proposal 1 solves the cold-start problem but is still a one-shot context load. Real debugging is iterative -- the initial hypothesis often leads to a second area of the codebase, which leads to a third. Currently, each pivot requires a new round of Grep/Read exploration. With auggie-in-the-loop, each pivot is a cheap semantic query rather than an expensive multi-file Read sequence.

This mirrors how experienced developers debug: they form a mental model, check one area, pivot to another based on what they find, and repeat. Auggie acts as the "codebase memory" that makes each pivot nearly free.

### Implementation Approach

**1. Define a Hypothesis-Retrieval protocol in the troubleshoot behavioral flow:**

```
Phase 2 (Investigate) - Enhanced with Auggie-in-the-Loop:

  For each hypothesis:
    a. State the hypothesis clearly (e.g., "The NPE is caused by a null user
       object passed from AuthService.getUser()")
    b. Fire targeted auggie query:
       information_request: "AuthService.getUser() implementation, callers,
                            null checks, and related error handling"
       directory_path: "{cwd}"
    c. Evaluate auggie results against hypothesis:
       - CONFIRMED: auggie returned code showing the suspected path exists
         and lacks null handling -> proceed to Debug phase for this hypothesis
       - REFUTED: auggie shows the path has null guards, or the method
         signature prevents null -> discard hypothesis, form next one
       - INSUFFICIENT: auggie returned unrelated code -> fall back to
         targeted Grep for this specific query
    d. Record hypothesis + outcome for diagnostic report
```

**2. Add a query budget to prevent auggie overuse:**

```
Auggie Query Budget per troubleshoot session:
  --type bug:         max 5 queries (issue-specific + up to 4 hypothesis pivots)
  --type build:       max 3 queries (build issues are usually localized)
  --type performance: max 6 queries (perf issues often span multiple subsystems)
  --type deployment:  max 4 queries (env + config + service + dependency)

If budget exhausted: fall back to Grep/Read for remaining hypotheses.
Log: "Auggie budget exhausted ({n}/{max}), continuing with native tools"
```

**3. Integrate with the diagnostic report output:**

The final diagnostic report (produced when no `--fix` flag) gains a new section:

```
## Investigation Trail

| # | Hypothesis | Auggie Query | Result | Tokens Saved |
|---|-----------|-------------|--------|--------------|
| 1 | NPE from AuthService.getUser() | "AuthService.getUser null handling" | REFUTED (null guard at line 42) | ~1,200 |
| 2 | NPE from UserCache.lookup() | "UserCache.lookup return values" | CONFIRMED (returns null on miss) | ~800 |

**Total retrieval cost**: 2 queries (~400 tokens)
**Estimated savings**: ~2,000 tokens (vs. manual Grep/Read exploration)
```

This makes the troubleshooting process transparent and auditable -- the user can see exactly what hypotheses were tested and how the agent arrived at the root cause.

**4. Combine with Proposal 1 (Phase 0 + In-the-Loop):**

These proposals are complementary. The recommended implementation is:
- Phase 0 (Proposal 1): front-load general codebase context (architecture, patterns, related tests)
- Phase 2-3 (Proposal 2): use targeted auggie queries for hypothesis validation during investigation

This gives both breadth (Phase 0 architecture awareness) and depth (in-the-loop targeted retrieval).

### Expected Benefits

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Hypothesis validation cost | 1,000-3,000 tokens/hypothesis (Grep+Read) | 200-400 tokens/hypothesis (auggie query) | 70-85% reduction |
| False-path exploration | 2-4 wasted pivots per session | 0-1 wasted pivots (auggie refutes early) | 50-75% reduction |
| Total session tokens (complex bug) | 12,000-20,000 | 6,000-12,000 | 40-50% reduction |
| Diagnostic report quality | Implicit reasoning | Explicit hypothesis trail | Qualitatively better |

The biggest win here is in **eliminated false paths**. Without auggie, when the agent suspects AuthService is the problem, it must Read 2-3 files (500-1,500 tokens each) to confirm or refute. With auggie, a single query (~200 tokens) can reveal the null guard that refutes the hypothesis instantly. Over a typical debugging session with 3-5 hypotheses, this compounds to massive savings.

### Trade-offs

- **More complex behavioral specification**: the troubleshoot command goes from a simple 5-phase flow to a protocol with query budgets, hypothesis-retrieval loops, and result evaluation logic. This increases the command definition size and cognitive load for maintainers.
- **Query budget tuning**: the per-type budgets (5/3/6/4) are estimates. Too low and the agent falls back to expensive native tools prematurely; too high and we waste auggie calls on diminishing-return queries. Mitigation: start with these defaults, add telemetry to the diagnostic report (query count, tokens saved), and tune based on real usage data.
- **Auggie result evaluation is non-trivial**: the agent must decide whether auggie results CONFIRM, REFUTE, or are INSUFFICIENT for a hypothesis. This is a judgment call that could go wrong (e.g., auggie returns tangentially related code that the agent misinterprets as confirmation). Mitigation: the explicit hypothesis-outcome logging in the diagnostic report makes errors auditable, and the `--trace` flag could increase auggie context window for harder cases.
- **Latency**: each auggie query adds a round-trip. For time-sensitive debugging (production incidents), the latency of 3-5 auggie queries could matter. Mitigation: the `--type deployment` budget is intentionally lower, and a future `--fast` flag could skip auggie entirely for emergency triage.

---

## Comparison Matrix

| Dimension | Proposal 1 (Phase 0) | Proposal 2 (In-the-Loop) | Combined |
|-----------|----------------------|--------------------------|----------|
| Complexity to implement | Low (add phase + 2 queries) | Medium (protocol + budgets + eval) | Medium |
| Token savings (simple bug) | 30-40% | 20-30% | 35-45% |
| Token savings (complex bug) | 20-30% | 40-50% | 50-60% |
| Auggie queries per session | 2 (fixed) | 3-6 (variable) | 4-8 (variable) |
| Diagnostic report improvement | Minimal | Significant (hypothesis trail) | Significant |
| Risk of over-engineering | Low | Medium | Medium |
| Recommended priority | P1 (implement first) | P2 (implement after P1 proven) | -- |

## Recommendation

**Implement Proposal 1 first** as a low-risk, high-impact change. It requires minimal modification to the troubleshoot command (add frontmatter, insert Phase 0, add fallback). Once Proposal 1 is validated in real usage, **layer Proposal 2 on top** to capture the iterative debugging savings.

The combined approach gives sc:troubleshoot the same level of auggie integration that sc:brainstorm (Phase 0 awareness) and sc:task-unified (context-primed execution) already enjoy, while adding a novel hypothesis-driven retrieval pattern that could later be adopted by other diagnostic commands like sc:analyze.

---

## Next Steps

1. Update `src/superclaude/commands/troubleshoot.md` frontmatter and behavioral flow (Proposal 1)
2. Create a troubleshoot skill package at `src/superclaude/skills/sc-troubleshoot-protocol/` if the protocol complexity warrants it (Proposal 2)
3. Update `src/superclaude/core/MCP.md` to list troubleshoot in auggie's integration commands (it is already listed but only as a keyword -- formalize the integration pattern)
4. Add troubleshoot-specific auggie query templates to the skill's `refs/` directory
5. Test with real debugging scenarios across bug, build, performance, and deployment types
