# C2: Complexity Threshold Boundary Fix — Remediation Proposal

## Problem
The complexity guard uses `> 0.7` but scoring factors can produce exactly 0.7, creating ambiguous boundary behavior. The same `>` vs `>=` issue exists across multiple thresholds.

## Step-by-Step Solution

### Step 1: Audit all threshold comparisons in the spec

| Guard | Current | Threshold | Boundary Behavior | Fix |
|-------|---------|-----------|-------------------|-----|
| Complexity auto-upgrade | `> 0.7` | 0.7 | At 0.7: no upgrade | Change to `>= 0.7` |
| domain_count planner dispatch | `> 4` | 4 | At 4: no dispatch | Keep `> 4` (5+ triggers) |
| tasks_created orchestrator | `> 8` | 8 | At 8: no orchestrator | Keep `> 8` (9+ triggers) |
| cross_module_deps ref load | `> 5` | 5 | At 5: no load | Keep `> 5` (6+ triggers) |
| MAX_CONCURRENT | `> 10` (implicit) | 10 | At 10: no split | Keep (10 fits in one batch) |

**Rationale**:
- Complexity: 0.7 IS the documented "complex" threshold — it should trigger. Fix: `>=`
- domain_count: 4 domains is manageable inline. 5+ justifies planner agent. Keep `>`
- tasks_created: 8 tasks is manageable inline. 9+ justifies orchestrator. Keep `>`
- cross_module_deps: 5 deps is manageable. 6+ justifies Sequential MCP. Keep `>`

### Step 2: Cap complexity score at 1.0

Current scoring is additive with no cap:
- domain_count > 3: +0.3
- cross_module_deps > 5: +0.2
- estimated_files > 20: +0.2
- security_domain: +0.2

Maximum possible: 0.3 + 0.2 + 0.2 + 0.2 = 0.9 (cannot exceed 1.0 with current factors)

**Add explicit cap**: `complexity_score = min(1.0, sum_of_factors)`

This future-proofs against adding new factors that could push past 1.0.

### Step 3: Apply the fix to Wave 1 Step 4

Current text:
```
If complexity > 0.7 AND `--strategy auto`: auto-upgrade to `wave` strategy
```

Replace with:
```
If complexity >= 0.7 AND `--strategy auto`: auto-upgrade to `wave` strategy
```

### Step 4: Add scoring factor documentation

Add after the factor list:
```
**Scoring rules**:
- Factors are additive (each condition independently adds to score)
- Score is capped at 1.0: `complexity = min(1.0, sum_of_factors)`
- Threshold for wave auto-upgrade: >= 0.7
- All other thresholds in the spec use strict `>` (not `>=`)
```

## Files to Modify
- `SKILL.md`: Wave 1 Step 4 — change `>` to `>=` for complexity only
- `SKILL.md`: Wave 1 Step 4 — add `min(1.0, ...)` cap
- `refs/dependency-graph.md`: No changes (thresholds there are correct as `>`)
