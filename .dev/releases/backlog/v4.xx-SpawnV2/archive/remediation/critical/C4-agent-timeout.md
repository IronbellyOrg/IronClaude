# C4: Sub-Agent Timeout Specification — Remediation Proposal

## Problem
No timeout defined for delegated sub-agents. A hung agent blocks the entire parallel group and all dependent groups indefinitely.

## Step-by-Step Solution

### Step 1: Define tiered timeout system

Timeouts are determined by TWO factors: depth level and command type.

**Base timeouts by depth**:
| Depth | Base Timeout | Rationale |
|-------|-------------|-----------|
| `shallow` | 120s (2 min) | Quick assessment, minimal analysis |
| `normal` | 300s (5 min) | Standard task execution |
| `deep` | 600s (10 min) | Thorough analysis with MCP calls |

**Command-type multipliers**:
| Command Category | Multiplier | Rationale |
|-----------------|-----------|-----------|
| Design commands (`/sc:design`) | 1.0x | Standard complexity |
| Implementation (`/sc:implement`, `/sc:build`) | 1.5x | Code generation takes longer |
| Analysis (`/sc:analyze`, `/sc:cleanup`) | 1.0x | Read-heavy, bounded |
| Testing (`/sc:test`) | 1.5x | Test execution adds time |
| Research (`/sc:research`) | 2.0x | Web search has latency |
| General (`/sc:task`) | 1.0x | Default |
| Pipeline generate phase | 1.0x | Uses base timeout |
| Pipeline compare-merge | 2.0x | Adversarial pipeline is multi-step |

**Effective timeout** = `base_timeout[depth] × command_multiplier`

Examples:
- `/sc:design` at `normal` depth: 300s × 1.0 = 300s (5 min)
- `/sc:research` at `deep` depth: 600s × 2.0 = 1200s (20 min)
- `/sc:implement` at `shallow` depth: 120s × 1.5 = 180s (3 min)

### Step 2: Define timeout → retry → escalation flow

```
1. Dispatch agent with timeout_ms = effective_timeout × 1000
2. If agent completes within timeout → success, collect output
3. If timeout fires:
   a. Mark task as TIMED_OUT (not failed — distinction matters)
   b. Check for partial output at task's output_dir
   c. If partial output exists: save it as <task_id>/partial-output.md
   d. RETRY ONCE with timeout extended by 50%:
      retry_timeout = effective_timeout × 1.5
   e. If retry also times out:
      - Mark task as `manual`
      - Log: "Task <id> timed out after retry (<total_seconds>s).
        Marked as manual. Partial output at: <path>"
      - Continue with remaining tasks in the parallel group
4. Do NOT block the parallel group while retrying:
   - Retry runs in the NEXT dispatch cycle (after current batch)
   - Other tasks in the group continue unaffected
```

### Step 3: Handle partial output from timed-out agents

```
When a timeout fires:
1. The Task tool may have partial output in its working directory
2. Check if <output_dir>/tasks/<task_id>/output.md exists
3. If it exists but may be incomplete:
   - Rename to partial-output.md
   - Add header: "<!-- PARTIAL: Agent timed out after Ns. Content may be incomplete. -->"
4. If no output exists: create empty marker file
   - <task_id>/TIMED_OUT with timestamp and timeout value
```

### Step 4: Specify where timeout config lives

Timeout configuration lives in `refs/delegation-matrix.md` (loaded Wave 3), not in SKILL.md.

Add section to delegation-matrix.md:
```
## Timeout Configuration

### Base Timeouts (by depth)
| Depth | Timeout (seconds) |
|-------|------------------|
| shallow | 120 |
| normal | 300 |
| deep | 600 |

### Command Multipliers
[table from Step 1]

### Timeout Formula
effective_timeout = base_timeout[depth] × command_multiplier
retry_timeout = effective_timeout × 1.5
```

### Step 5: Add `--timeout` override flag (optional, not default)

Add to spawn.md flags:
```
| `--timeout` | — | Override timeout in seconds for all tasks (disables tiered system) |
```

When `--timeout N` is provided: all tasks use N seconds, ignoring the tiered system. This is an escape hatch for users who know their tasks need unusual time.

### Step 6: Update error handling matrix

Add rows:
```
| Sub-agent timeout (first attempt) | Retry once with 1.5× timeout | Save partial output |
| Sub-agent timeout (retry) | Mark as `manual`, continue | Log timeout, save partial |
```

## Files to Modify
- `refs/delegation-matrix.md`: Add Timeout Configuration section
- `SKILL.md`: Wave 3 Step 3 (Agent Dispatch) — add timeout to Task dispatch
- `SKILL.md`: Error handling matrix — add 2 rows
- `spawn.md`: Add `--timeout` optional override flag
