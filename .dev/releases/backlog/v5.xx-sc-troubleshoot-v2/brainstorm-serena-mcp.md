# Brainstorm: Serena MCP Integration into sc:troubleshoot

> Generated: 2026-04-03 | Branch: feat/v3.65-prd-tdd-Refactor
> Method: /sc:brainstorm systematic exploration
> Status: PROPOSAL (pre-design)

## Problem Statement

The current `sc:troubleshoot` command (defined in `src/superclaude/commands/troubleshoot.md`) operates without any MCP server integration. Its `mcp-servers` field is an empty array. Every troubleshooting session starts from zero context -- the agent must re-discover project structure, re-trace symbol relationships, and re-learn patterns of past failures. This produces two measurable costs:

1. **Token waste**: Each session spends 2,000-5,000 tokens on context discovery (reading files, grepping for symbols, tracing call chains) before the actual diagnosis begins. For recurring or related issues, this discovery work is largely redundant.
2. **Reduced effectiveness**: Without symbol-level navigation, the troubleshoot flow relies on text-based grep patterns and manual file reads. This misses structural relationships (inheritance, call graphs, import chains) that are critical for root cause analysis.

The `diagnostic_chain.py` pipeline (used by sprint/roadmap runners) compounds this -- its four stages (troubleshoot, root_causes, solutions, summary) operate on string templates without access to the codebase's semantic structure.

## Serena MCP Capabilities (Relevant Subset)

| Tool | Purpose | Relevance to Troubleshooting |
|------|---------|------------------------------|
| `mcp__serena__activate_project` | Initialize project context | Required entry point for all other operations |
| `mcp__serena__find_symbol` | Locate symbol by name (file, type, parent hierarchy) | Trace error origins to exact definitions |
| `mcp__serena__get_symbols_overview` | File-level symbol map (classes, functions, methods) | Understand structural context around a bug |
| `mcp__serena__search_for_pattern` | Pattern-based codebase search with semantic awareness | Find related code paths beyond text matching |
| `mcp__serena__read_memory` | Retrieve persistent cross-session data | Load prior diagnostic history |
| `mcp__serena__write_memory` | Persist cross-session data | Store diagnostic findings for future sessions |

---

## Proposal 1: Symbol-Aware Diagnosis Pipeline

### Summary

Integrate `find_symbol`, `get_symbols_overview`, and `search_for_pattern` into the troubleshoot behavioral flow to replace text-based investigation with structural symbol navigation. This targets the "Investigate" and "Debug" phases of the existing 5-phase flow.

### Rationale

The current troubleshoot flow (Analyze -> Investigate -> Debug -> Propose -> Resolve) uses only Read, Bash, Grep, and Write. When a user reports "Null pointer exception in user service," the agent currently greps for class names, reads files sequentially, and manually traces call chains. With Serena's symbol tools, the agent can resolve the exact symbol definition, see its parent class hierarchy, and map all callers/callees -- producing a structural diagnosis rather than a textual one.

### Implementation Approach

**Phase 1: Command definition update** (`src/superclaude/commands/troubleshoot.md`)

- Add `mcp-servers: [serena]` to the frontmatter.
- Add `--serena` flag documentation (explicit opt-in, consistent with framework convention).
- Add Serena tools to the Tool Coordination section:
  - `find_symbol`: Symbol resolution during stack trace analysis and error origin tracing.
  - `get_symbols_overview`: Structural context loading for files identified in error traces.
  - `search_for_pattern`: Semantic pattern search to find related failure points beyond grep.
  - `activate_project`: Session initialization (called once at start of troubleshoot flow).

**Phase 2: Behavioral flow enhancement**

Update the 5-phase behavioral flow to incorporate symbol navigation:

```
1. Analyze:  (unchanged) Examine issue description, gather system state
2. Investigate:
   a. Call activate_project for the current repository
   b. Extract symbol names from error messages / stack traces / user description
   c. Call find_symbol for each extracted symbol (include_body=False for overview)
   d. Call get_symbols_overview on files containing key symbols
   e. Build a structural context map: symbol -> file -> parent -> callers
   f. Identify structural relationships (inheritance, composition, call chains)
3. Debug:
   a. Use search_for_pattern to find all usage sites of suspect symbols
   b. Narrow hypothesis based on structural context (not just text matches)
   c. Read only the specific code sections identified by symbol navigation
4. Propose:  (enhanced) Include structural evidence in root cause analysis
5. Resolve:  (unchanged) Apply fixes with verification
```

**Phase 3: Diagnostic chain integration** (`src/superclaude/cli/pipeline/diagnostic_chain.py`)

Extend the `_run_troubleshoot` and `_run_root_causes` stages to accept an optional `symbol_context` parameter. When Serena is available, the runner passes pre-resolved symbol data into the chain, enriching the template-based output with actual structural information.

```python
@dataclass
class SymbolContext:
    """Pre-resolved symbol data from Serena."""
    symbols: dict[str, dict]  # name -> {file, type, parent, line}
    file_overviews: dict[str, list[str]]  # file -> [symbol names]
    pattern_matches: list[str]  # related code locations
```

**Phase 4: Fallback behavior**

When Serena is unavailable, fall back to current behavior (Grep/Read-based investigation). This follows the framework's established fail-open pattern used by `sc-validate-roadmap-protocol`.

### Expected Benefits

| Metric | Current | With Symbol Navigation | Improvement |
|--------|---------|----------------------|-------------|
| Investigation tokens | ~2,000-3,000 per issue | ~500-1,000 (targeted reads) | 60-75% reduction |
| Root cause accuracy | Medium (text-pattern based) | High (structural evidence) | Qualitative improvement |
| Time to first hypothesis | 3-5 tool calls (grep, read, grep...) | 1-2 tool calls (find_symbol, get_overview) | 50-60% faster |
| False lead rate | High (grep returns noise) | Low (symbol resolution is precise) | Significant reduction |

### Trade-offs

- **Serena dependency**: Adds an MCP server dependency. Mitigated by fail-open fallback to current behavior.
- **Activation latency**: `activate_project` adds a one-time cost per session (~200-500ms). Amortized across the full troubleshoot flow, this is negligible.
- **Symbol resolution limits**: Serena's symbol navigation works best for statically-typed languages and well-structured codebases. Dynamic languages (plain JS, Python with heavy metaprogramming) may yield fewer structural insights. The fallback to grep/read covers these cases.
- **Complexity**: The troubleshoot command moves from "basic" complexity to "standard" complexity. This is justified by the token savings.

---

## Proposal 2: Diagnostic Memory -- Cross-Session Issue Knowledge Base

### Summary

Integrate `read_memory` and `write_memory` to build a persistent diagnostic knowledge base per project. Each troubleshoot session reads prior diagnostic history before investigating, and writes its findings (root cause, resolution, affected symbols) after completing. This eliminates redundant re-discovery for recurring issues and accelerates diagnosis of related problems.

### Rationale

In real-world development, issues cluster. A null pointer in the user service today often relates to the authentication refactor that caused a similar null pointer last week. Currently, each troubleshoot session is amnesic -- it cannot benefit from prior diagnostic work. The Serena memory API (already proven in `sc-validate-roadmap-protocol` and `sc:save`/`sc:load` commands) provides the persistence layer to accumulate diagnostic intelligence across sessions.

### Implementation Approach

**Phase 1: Memory schema design**

Define a structured memory format for diagnostic records, stored under a project-scoped key:

```
Memory Key: troubleshoot-history-{project-slug}
```

```json
{
  "version": 1,
  "project": "superclaude",
  "entries": [
    {
      "timestamp": "2026-04-03T14:30:00Z",
      "issue_summary": "Null pointer in UserService.authenticate()",
      "issue_type": "bug",
      "root_cause": "Missing null check on token parameter after OAuth refactor",
      "affected_symbols": ["UserService.authenticate", "OAuthProvider.getToken"],
      "affected_files": ["src/services/user.py", "src/auth/oauth.py"],
      "resolution": "Added null guard with early return and error logging",
      "related_entries": [],
      "tags": ["null-safety", "auth", "oauth"]
    }
  ],
  "patterns": {
    "null-safety": { "count": 3, "last_seen": "2026-04-03", "common_locations": ["src/services/"] },
    "auth": { "count": 2, "last_seen": "2026-04-03", "common_locations": ["src/auth/"] }
  }
}
```

Retention policy: Keep last 50 entries. Expire entries older than 180 days. Merge pattern statistics cumulatively.

**Phase 2: Pre-diagnosis context loading**

Add a "Phase 0" to the troubleshoot behavioral flow:

```
0. Context Load (NEW):
   a. Call activate_project (if not already active)
   b. Call read_memory with key troubleshoot-history-{project-slug}
   c. If history exists:
      - Extract pattern summary (top 5 recurring issue types)
      - Check if current issue description matches any prior entry (keyword overlap)
      - If match found: present prior diagnostic as starting hypothesis
      - Present: "This project has had {N} prior issues. {M} involved {pattern}."
   d. If no history: proceed normally (first-time troubleshoot)
```

This pre-loads diagnostic context in a single MCP call (~100 tokens of overhead), potentially saving thousands of tokens by providing an immediate starting hypothesis for recurring issues.

**Phase 3: Post-diagnosis persistence**

Add a completion hook after Phase 5 (Resolve) or after Phase 4 (Propose) if `--fix` was not used:

```
6. Persist (NEW):
   a. Call read_memory to load existing history
   b. Construct new entry from diagnostic findings:
      - issue_summary: from user input + analysis
      - root_cause: from Phase 4 proposal
      - affected_symbols: from Phase 2-3 investigation (or from Proposal 1's symbol context)
      - resolution: from Phase 5 (if --fix applied) or "proposed only"
   c. Append entry, enforce retention policy (50 entries, 180 days)
   d. Update pattern statistics
   e. Call write_memory with updated history
   f. If related to prior entries: link via related_entries field
```

**Phase 4: Diagnostic chain enhancement** (`diagnostic_chain.py`)

Add an optional `prior_diagnostics` parameter to `run_diagnostic_chain`:

```python
def run_diagnostic_chain(
    step_id: str,
    failure_reason: str,
    remediation_output: str = "",
    prior_diagnostics: list[dict] | None = None,  # NEW
) -> DiagnosticReport:
```

When `prior_diagnostics` is provided, `_run_root_causes` can reference prior root causes for similar failures, and `_run_solutions` can reference prior resolutions that worked.

**Phase 5: Command flag additions**

- `--history`: Show diagnostic history for the current project without running a new diagnosis.
- `--no-memory`: Opt out of memory persistence for a specific troubleshoot run.
- `--clear-history`: Reset diagnostic history for the project (with confirmation).

### Expected Benefits

| Metric | Current | With Diagnostic Memory | Improvement |
|--------|---------|----------------------|-------------|
| Recurring issue diagnosis | Full re-investigation each time | Instant hypothesis from prior findings | 80-90% token reduction for known patterns |
| Cross-session continuity | None (amnesic) | Full diagnostic history available | Qualitative leap |
| Pattern detection | Per-session only | Cumulative across all sessions | Identifies systemic issues |
| Onboarding cost | New sessions start cold | Prior diagnostic context loaded automatically | Faster ramp-up |
| Memory overhead per session | 0 | ~100-200 tokens (read) + ~100-200 tokens (write) | Negligible |

### Trade-offs

- **Serena hard dependency for memory features**: Memory read/write requires Serena. Mitigated by fail-open: if Serena is unavailable, the troubleshoot flow runs exactly as it does today (no memory, no persistence). The `--no-memory` flag provides explicit opt-out.
- **Memory staleness**: Diagnostic entries may reference code that has since been refactored. Mitigated by the 180-day expiry and the 50-entry cap. Additionally, Proposal 1's symbol resolution will naturally detect when a referenced symbol no longer exists.
- **Memory size growth**: At ~200 bytes per entry, 50 entries is ~10KB -- well within Serena's memory limits.
- **Privacy considerations**: Diagnostic history may contain sensitive error details. The `--clear-history` flag and project-scoped keys ensure users maintain control. No data leaves the local Serena instance.
- **Complementarity with Proposal 1**: These two proposals are designed to compose. Proposal 1 provides the symbol-level precision for each individual diagnosis. Proposal 2 provides the cross-session memory that accumulates those diagnoses into project-wide intelligence. Together, they transform troubleshoot from a stateless grep-based tool into a learning, structurally-aware diagnostic system.

---

## Combined Impact Assessment

### When both proposals are implemented together

| Scenario | Tokens (Current) | Tokens (Proposal 1 only) | Tokens (Both Proposals) |
|----------|-------------------|--------------------------|------------------------|
| First-time novel bug | ~5,000 | ~2,000 | ~2,200 (slight overhead for empty memory read) |
| Recurring bug pattern | ~5,000 | ~2,000 | ~500 (prior history provides immediate hypothesis) |
| Related but distinct bug | ~5,000 | ~2,000 | ~1,000 (partial match accelerates investigation) |
| Performance diagnosis | ~8,000 | ~4,000 | ~2,000 (prior bottleneck patterns inform search) |

### Implementation Priority

**Proposal 1 (Symbol-Aware Diagnosis)** should be implemented first. It has no dependency on Proposal 2 and provides immediate token savings for every troubleshoot invocation. It also produces the `affected_symbols` data that Proposal 2's memory entries consume.

**Proposal 2 (Diagnostic Memory)** should follow. It builds on Proposal 1's output and provides compounding returns over time as the diagnostic knowledge base grows.

### Changes Required

| File | Proposal 1 | Proposal 2 |
|------|-----------|-----------|
| `src/superclaude/commands/troubleshoot.md` | Update frontmatter, behavioral flow, tool coordination | Add Phase 0/6, new flags |
| `src/superclaude/cli/pipeline/diagnostic_chain.py` | Add `SymbolContext` dataclass, update stage functions | Add `prior_diagnostics` parameter |
| `src/superclaude/core/MCP.md` | Add troubleshoot to Serena integration docs | Same |
| `src/superclaude/core/COMMANDS.md` | Update troubleshoot entry with MCP references | Same |

### Open Questions for Design Phase

1. Should the troubleshoot command also integrate Auggie MCP for broad codebase search alongside Serena's symbol-specific tools, or is Serena sufficient?
2. Should diagnostic memory entries be shared across worktrees (same project, different branches), or scoped per branch?
3. What is the interaction model if `sc:troubleshoot` is invoked inside an `sc:pm` session that already has Serena activated -- should it reuse the existing project activation?
4. Should the diagnostic chain in `diagnostic_chain.py` call Serena directly (adding an MCP dependency to the CLI pipeline), or should it receive pre-resolved data from the command layer?

---

## Next Steps

- `/sc:design` -- Architecture for the symbol-aware diagnosis pipeline (Proposal 1)
- `/sc:tdd` -- Technical design document covering memory schema and API contracts (Proposal 2)
- `/sc:adversarial` -- Challenge both proposals for edge cases and failure modes
