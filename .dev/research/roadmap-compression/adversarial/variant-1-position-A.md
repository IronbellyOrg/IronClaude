# Position A: Structural Skeleton + Task Registry

## Strategy

Compress each roadmap into two components:
1. **Task Registry** — A compact YAML/JSON array of all task rows with fields: `[id, task_name, component, deps, effort, priority, phase]`
2. **Prose Skeleton** — Section headers + one-line summaries for non-table sections (Executive Summary, Risk, Resources, Timeline)

## Compression Mechanics

### What is PRESERVED (lossless)
- All task IDs (AUTH-001-TDD, FR-AUTH-001, COMP-001, etc.)
- All dependency chains (full DAG)
- Phase assignments and milestone gates
- Effort estimates (S/M/L) and priority levels (P0/P1/P2)
- Component assignments
- Section structure and ordering
- YAML frontmatter (verbatim)
- Integration point registries (named artifacts, wired components)

### What is STRIPPED (lossy)
- Acceptance criteria prose (the longest field per row, often 50-100 words)
- Verbose task descriptions (compressed to task_name keyword)
- Risk assessment rationale (kept: ID, risk name, probability, impact; stripped: mitigation prose)
- Resource requirement prose (kept: role, allocation; stripped: responsibilities narrative)
- Timeline narrative (kept: dates, durations; stripped: commentary)
- Success criteria descriptions (kept: metric, target; stripped: validation method prose)

### What the COMPRESSED OUTPUT looks like

```yaml
# Frontmatter preserved verbatim
---
spec_source: "test-tdd-user-auth.md"
complexity_score: 0.72
complexity_class: "HIGH"
total_entities: 144
estimated_task_rows: 166
actual_task_rows: 181
milestones: [M1, M2, M3, M4, M5]
phases: 6
---

# Executive Summary
JWT-based stateless auth with dual-token lifecycle. 181 tasks, 6 phases, GA by 2026-06-09. Complexity 0.72 HIGH.

# Phase 1: Foundation & Core Auth (28 rows, 2026-04-01 → 2026-04-14)
tasks:
  - {id: AUTH-001-TDD, name: "Baseline TDD", comp: Documentation, deps: [], effort: S, pri: P0}
  - {id: AUTH-PRD-001, name: "PRD traceability", comp: Documentation, deps: [AUTH-001-TDD], effort: S, pri: P0}
  - {id: SEC-POLICY-001, name: "Security policy review", comp: Security, deps: [AUTH-001-TDD], effort: S, pri: P0}
  - {id: INFRA-DB-001, name: "Provision PostgreSQL", comp: Infrastructure, deps: [], effort: M, pri: P0}
  # ... all 28 rows

integration_points:
  - {artifact: "AuthService DI container", wired: [TokenManager, PasswordHasher, UserRepo], phase: 1, xref: [2]}
  # ...

# Phase 2: Token Management (26 rows, 2026-04-15 → 2026-04-28)
# ... same pattern

# Risks (compressed)
risks:
  - {id: R-001, risk: "XSS token theft", prob: Medium, impact: High, phase: 3}
  - {id: R-002, risk: "Brute-force login", prob: High, impact: Medium, phase: 1}
  # ...

# Timeline (compressed)
timeline:
  - {phase: 1, start: 2026-04-01, end: 2026-04-14, duration: "2w"}
  # ...

critical_path: "INFRA-DB-001 → DM-001 → COMP-005 → COMP-001 → FR-AUTH-001 → M1 → COMP-003 → COMP-002 → FR-AUTH-003 → M2 → FR-AUTH-005 → M3 → COMP-006/007/008 → M4 → MIG-001 → MIG-002 → MIG-003 → M5"
```

## Estimated Compression

- Opus (60KB → ~12-15KB): ~75-80% reduction
- Haiku (76KB → ~15-19KB): ~75-80% reduction
- Combined for diff: ~27-34KB (from 136KB)

## Strengths

1. **Maximum compression ratio** — strips the most verbose content (acceptance criteria prose)
2. **Diff-optimal** — YAML task arrays produce clean line-by-line diffs on the fields that matter most (IDs, deps, effort, priority)
3. **Dependency graph preserved perfectly** — the primary structural data for merge decisions
4. **Deterministic** — same input always produces same output (no hashing, no pre-comparison)
5. **Independent compression** — each file compressed independently, no cross-file dependency
6. **Machine-readable** — YAML output can be programmatically parsed for automated merge tools

## Weaknesses

1. **Acceptance criteria loss** — the most detailed differentiation between roadmaps is in AC prose; stripping it loses nuance about HOW each roadmap approaches the same task
2. **Semantic flattening** — two tasks with the same ID but radically different acceptance criteria will look identical in the compressed form
3. **Non-recoverable** — once compressed, original prose cannot be reconstructed
4. **Narrative context lost** — risk mitigations, resource justifications, and timeline rationale are gone

## Diff Behavior

With YAML task registries, diff tools will show:
- Added/removed task IDs (clear)
- Changed dependencies (clear)
- Changed effort/priority (clear)
- Different component assignments (clear)
- Different phase assignments (clear)
- Different acceptance criteria (INVISIBLE — this is the primary risk)
