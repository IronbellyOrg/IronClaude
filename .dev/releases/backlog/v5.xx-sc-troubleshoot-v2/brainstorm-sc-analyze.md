# Brainstorm: Integrating sc:analyze into sc:troubleshoot

**Date**: 2026-04-03
**Branch**: feat/v3.65-prd-tdd-Refactor
**Status**: Brainstorm / Backlog
**Goal**: Leverage sc:analyze's structured analysis capabilities to narrow the troubleshooting search space and reduce token waste on wrong hypotheses.

---

## Problem Statement

The current `sc:troubleshoot` command operates with a flat investigative flow: it receives an issue description, then immediately begins hypothesis generation and debugging. This approach has two costly failure modes:

1. **Blind hypothesis expansion** -- Without structural understanding of the codebase area under investigation, troubleshoot generates hypotheses that span the entire possibility space. Many of these are ruled out only after expensive Read/Grep operations, wasting tokens on dead-end paths.

2. **Redundant discovery work** -- Troubleshoot's Step 1 ("Analyze: Examine issue description and gather relevant system state information") duplicates a subset of what sc:analyze already does (file discovery, pattern recognition, dependency mapping), but in an ad-hoc, less structured way.

Meanwhile, `sc:analyze` produces structured outputs -- severity-rated findings, dependency maps, complexity assessments, and architectural context -- that would directly constrain and prioritize the troubleshooting search space if available as input.

---

## Proposal 1: Analyze-First Gate (Pre-Step Structural Narrowing)

### Summary

Add a new Phase 0 to sc:troubleshoot that runs a targeted, scope-limited sc:analyze pass before hypothesis generation begins. The analyze output becomes a structured context block that constrains all subsequent troubleshooting steps.

### Rationale

The insight is that most troubleshooting token waste comes from *exploring the wrong area of the codebase*. A focused analyze pass (scoped to the relevant module/directory, not the full project) produces:

- **Dependency graph** of the affected component, immediately revealing which files could plausibly contribute to the issue
- **Complexity hotspots** that statistically correlate with bug locations
- **Existing quality/security findings** that may directly explain the reported symptom
- **Architecture context** that prevents misunderstanding call flows

This information dramatically prunes the hypothesis space before a single debugging step occurs.

### Implementation Approach

**1. New `--analyze` flag on sc:troubleshoot (opt-in initially, default later)**

```
/sc:troubleshoot "API returns 500 on user creation" --type bug --analyze
```

When `--analyze` is present, troubleshoot inserts a Phase 0 before its existing Step 1.

**2. Phase 0: Scoped Analyze Pass**

- Parse the issue description to extract target scope (file paths, module names, error locations from stack traces).
- Run a `--depth quick --focus architecture` analyze pass scoped to the extracted target directory/module only (not the full project).
- Budget: cap the analyze pre-step at approximately 500-800 tokens of output (matching the codebase-context briefing pattern from sc:brainstorm).
- Output a structured context block:

```
## Structural Context (via sc:analyze)

**Scope**: src/services/user/
**Files**: 12 files, 2,340 LOC
**Dependency Chain**: UserService -> AuthProvider -> DatabasePool -> ConnectionManager
**Complexity Hotspots**: user_service.py:create_user (cyclomatic: 14), auth_provider.py:validate_token (cyclomatic: 9)
**Existing Findings**: 2 quality issues (unhandled exception paths in create_user), 1 security note (SQL parameter interpolation in user_queries.py)
**Architecture**: Request -> Router -> UserService -> [AuthProvider, UserRepository] -> Database
```

**3. Modified Step 2 (Investigate): Hypothesis Pruning**

- Existing findings from the analyze pass become *priority-1 hypotheses* (e.g., "unhandled exception in create_user" directly matches "API returns 500").
- The dependency chain constrains the investigation boundary -- files outside the chain are not explored unless priority-1 hypotheses are all eliminated.
- Complexity hotspots set the investigation order within the boundary.

**4. Behavioral flow becomes:**

```
0. Analyze (scoped)  -- structural narrowing, ~500-800 token output
1. Contextualize     -- merge issue description with structural context
2. Investigate       -- pruned hypothesis generation, ordered by analyze findings
3. Debug             -- targeted debugging within the narrowed scope
4. Propose           -- solution options with structural impact assessment
5. Resolve           -- (with --fix) apply and verify
```

**5. Command file changes:**

- Edit `src/superclaude/commands/troubleshoot.md` to add the `--analyze` flag, Phase 0 behavioral description, and the structured context block template.
- Add `Glob` to the Tool Coordination section (needed for the scoped analyze pass).
- Update the frontmatter to reference the analyzer persona.

### Expected Benefits

| Metric | Current | With Proposal 1 | Improvement |
|--------|---------|-----------------|-------------|
| Hypotheses generated before first correct one | 3-7 | 1-3 | 50-60% reduction |
| Files read during investigation | 8-20 | 3-8 | ~60% reduction |
| Total token consumption (median bug) | ~3,000-5,000 | ~1,800-3,200 | 35-45% reduction |
| Time to root cause | 4-6 tool rounds | 2-4 tool rounds | ~40% faster |

The 500-800 token investment in Phase 0 pays for itself if it eliminates even one wrong-hypothesis investigation cycle (typically 500-1,500 tokens each).

### Trade-offs

- **Latency overhead**: Adds 1-2 tool rounds before debugging begins. For trivial issues (typo, missing import), this is wasted effort.
  - *Mitigation*: Make `--analyze` opt-in initially. After validation, make it default but add `--no-analyze` to skip for known-simple issues. Also consider auto-skipping when the issue description already contains a specific file:line reference.
- **Scope extraction heuristics**: Parsing the issue description to determine the analyze target is imperfect. A bad scope (too broad or wrong module) wastes the pre-step budget.
  - *Mitigation*: Fall back to the `--type` flag for scope hints (e.g., `--type build` scopes to build config files). Allow explicit scope override: `--analyze src/services/user/`.
- **Double-reading risk**: If the analyze pass reads files that troubleshoot then re-reads during debugging, there is some token duplication.
  - *Mitigation*: The analyze output should be *summary-level* (findings and structure, not raw file content), so subsequent Read calls serve a different purpose (line-level inspection of specific findings).

---

## Proposal 2: Inline Analyze Checkpoints (Adaptive Mid-Investigation Narrowing)

### Summary

Instead of a fixed pre-step, embed sc:analyze as a callable checkpoint within the troubleshoot investigation loop. When troubleshoot's hypothesis confidence drops below a threshold (i.e., initial hypotheses are being eliminated without convergence), it triggers a targeted analyze pass on the area of current investigation to reorient.

### Rationale

Proposal 1 optimizes the common case but cannot help when the initial scope extraction is wrong or when the issue crosses module boundaries. The real token waste in troubleshooting happens during *hypothesis churn* -- the pattern where the agent reads a file, eliminates a hypothesis, reads another file, eliminates another hypothesis, and iterates without converging.

This proposal detects that churn pattern and intervenes with structural analysis at exactly the moment it would be most valuable -- when the agent is lost and about to waste significant tokens on unfocused exploration.

### Implementation Approach

**1. Hypothesis Tracking State**

Add internal state tracking to the troubleshoot behavioral flow:

```
hypothesis_count: 0          # total hypotheses generated
eliminated_count: 0          # hypotheses ruled out
files_inspected: []          # files read so far
convergence_score: 1.0       # starts high, decreases with eliminations
```

**2. Churn Detection Rule**

After each hypothesis elimination, evaluate:

```
IF eliminated_count >= 3 AND (eliminated_count / hypothesis_count) >= 0.75:
    TRIGGER inline analyze checkpoint
```

Translation: if 3 or more hypotheses have been tried and at least 75% of all hypotheses have been eliminated without finding the root cause, the investigation is churning.

**3. Inline Analyze Checkpoint**

When triggered, the checkpoint:

- Pauses hypothesis investigation.
- Runs sc:analyze with `--focus architecture --depth quick` scoped to the *union of directories* containing `files_inspected` so far.
- Produces a structural context block (same format as Proposal 1).
- Crucially, also produces a **differential insight**: what the analyze pass reveals that was NOT visible from the files already inspected (e.g., upstream callers, sibling dependencies, configuration files that affect behavior).
- Resets `convergence_score` and generates new hypotheses informed by the structural context.

```
## Analyze Checkpoint (triggered: 3/4 hypotheses eliminated)

**Investigation so far**: Inspected auth_provider.py, user_service.py, database_pool.py
**Structural discovery**: ConnectionManager has a retry_policy config loaded from env.yaml
  that was NOT in the inspection set. retry_policy.max_retries=0 would cause immediate
  failure on transient DB errors -- consistent with reported 500 errors.
**New hypothesis**: Environment configuration issue in retry_policy (priority: HIGH)
```

**4. Behavioral flow becomes:**

```
1. Analyze      -- initial issue examination (existing behavior)
2. Investigate  -- hypothesis generation and testing
   |
   +--[churn detected]--> Analyze Checkpoint --> regenerate hypotheses --> resume
   |
3. Debug        -- targeted debugging on converged hypothesis
4. Propose      -- solution with impact assessment
5. Resolve      -- (with --fix) apply and verify
```

**5. Command file changes:**

- Edit `src/superclaude/commands/troubleshoot.md` to add the churn-detection behavioral rule, the checkpoint trigger conditions, and the checkpoint output template.
- Add a new Key Pattern: **Adaptive Narrowing**: hypothesis churn detection -> structural analysis checkpoint -> re-scoped investigation.
- No new flags needed -- this is always-on adaptive behavior.

### Expected Benefits

| Metric | Current | With Proposal 2 | Improvement |
|--------|---------|-----------------|-------------|
| Token waste on wrong hypotheses (worst case) | 3,000-8,000 | 1,000-3,000 | 60-70% reduction |
| Recovery from wrong initial scope | Manual (user redirects) | Automatic checkpoint | Eliminates user intervention |
| Cross-module issue resolution | Often fails or requires hints | Structural discovery finds cross-boundary causes | Handles new class of issues |
| Total token consumption (hard bugs) | 5,000-12,000 | 3,000-7,000 | 40-50% reduction |

The key advantage over Proposal 1 is that this approach is *reactive* -- it invests zero tokens on structural analysis when hypotheses converge quickly, and invests heavily exactly when the investigation is stalling.

### Trade-offs

- **Implementation complexity**: Requires the troubleshoot command to maintain internal state across tool rounds (hypothesis tracking, convergence scoring). This is more complex than a simple pre-step.
  - *Mitigation*: The state is lightweight (counts and a file list) and can be maintained as a behavioral instruction ("after each hypothesis elimination, update your internal count and evaluate the churn rule").
- **Threshold calibration**: The `eliminated >= 3 AND ratio >= 0.75` threshold is a starting heuristic. Too sensitive triggers unnecessary checkpoints; too conservative lets churn continue.
  - *Mitigation*: Start with the 3/75% heuristic. Add `--analyze-threshold N` flag for power users. Collect usage data via reflexion pattern to calibrate over time.
- **Checkpoint cost on false trigger**: If churn is detected but the issue is genuinely in the already-inspected files (just hard to find), the checkpoint wastes ~500-800 tokens on structural analysis that adds no new information.
  - *Mitigation*: The checkpoint's differential insight step explicitly compares against already-inspected files. If no new files/connections are discovered, the checkpoint output says "no structural expansion found" and investigation continues without generating new hypotheses from the checkpoint.
- **No benefit for simple bugs**: Unlike Proposal 1, this provides zero value for bugs that are found on the first or second hypothesis. But it also costs zero tokens in those cases -- a favorable asymmetry.

---

## Comparison Matrix

| Dimension | Proposal 1: Analyze-First Gate | Proposal 2: Inline Checkpoints |
|-----------|-------------------------------|-------------------------------|
| **When it helps** | All bugs (constant overhead, consistent benefit) | Hard bugs only (zero overhead for easy bugs, large benefit for hard ones) |
| **Token investment** | Fixed ~500-800 upfront | Variable: 0 for easy bugs, ~500-800 per checkpoint for hard bugs |
| **Implementation effort** | Low (add Phase 0, new flag) | Medium (state tracking, churn detection rule) |
| **Risk of wasted tokens** | Higher (pre-step may be unnecessary for simple issues) | Lower (only triggers when investigation is actually stalling) |
| **Scope accuracy** | Depends on issue-description parsing | Depends on churn-detection threshold |
| **Cross-module discovery** | Only if initial scope is correct | Yes -- checkpoint re-scopes based on investigation trajectory |
| **Composability** | Proposals 1 and 2 are composable -- use Analyze-First for initial scoping AND Inline Checkpoints for mid-investigation recovery |

## Recommendation

**Implement both, in phases:**

1. **Phase A**: Ship Proposal 1 (`--analyze` flag) as it is simpler and provides immediate, measurable benefit.
2. **Phase B**: Ship Proposal 2 (inline checkpoints) as always-on behavior, which catches the cases Proposal 1 misses.
3. **Phase C**: When both are active, the analyze-first gate reduces the likelihood of triggering inline checkpoints (because the initial scope is better), creating a complementary layered system.

## Next Steps

- `/sc:design` -- Design the Phase 0 integration architecture and state management approach
- `/sc:tdd` -- Write a TDD spec for the `--analyze` flag behavior and churn detection thresholds
- `/sc:workflow` -- Plan the implementation sequence across the troubleshoot command file and any supporting skill files
