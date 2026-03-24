# Agent Decomposition Plan — v3.3 TurnLedger Validation

**Generated**: 2026-03-23
**Total agents**: 11 (7 domain + 4 cross-cutting)

## Domain Agents

### AGENT-D1: Wiring E2E
- domain: wiring-e2e
- requirements: REQ-001 through REQ-023, REQ-062, REQ-066, REQ-085
- requirement_count: 25
- spec_sections: FR-1.1–FR-1.21, SC-1, SC-5, Risk (subprocess)
- cross_cutting_reqs: REQ-035 (mode verification ACs from gate-modes)
- output: 01-agent-D1-wiring-e2e.md

### AGENT-D2: TurnLedger Lifecycle
- domain: turnledger-lifecycle
- requirements: REQ-024 through REQ-029, REQ-063
- requirement_count: 7
- spec_sections: FR-2.1–FR-2.4, SC-2
- cross_cutting_reqs: REQ-029 touches gate-modes (cross-path includes modes)
- output: 01-agent-D2-turnledger-lifecycle.md

### AGENT-D3: Gate Modes
- domain: gate-modes
- requirements: REQ-030 through REQ-040, REQ-064, REQ-067
- requirement_count: 13
- spec_sections: FR-3.1–FR-3.3, SC-3, SC-6
- cross_cutting_reqs: REQ-035 touches wiring-e2e
- output: 01-agent-D3-gate-modes.md

### AGENT-D4: Reachability
- domain: reachability
- requirements: REQ-041 through REQ-046, REQ-068, REQ-070, REQ-079, REQ-084
- requirement_count: 10
- spec_sections: FR-4.1–FR-4.4, Wiring Manifest, SC-7, SC-9
- cross_cutting_reqs: REQ-052 (FR-5.3 cross-ref from pipeline-fixes)
- output: 01-agent-D4-reachability.md

### AGENT-D5: Pipeline Fixes
- domain: pipeline-fixes
- requirements: REQ-047 through REQ-052, REQ-071, REQ-072, REQ-086, REQ-088
- requirement_count: 10
- spec_sections: FR-5.1–FR-5.3, SC-10, SC-11
- cross_cutting_reqs: REQ-050 touches convergence/checkers domain
- output: 01-agent-D5-pipeline-fixes.md

### AGENT-D6: Audit Trail
- domain: audit-trail
- requirements: REQ-059 through REQ-061, REQ-073, REQ-078, REQ-087
- requirement_count: 6
- spec_sections: FR-7.1–FR-7.3, SC-12
- cross_cutting_reqs: REQ-078 touches all test domains
- output: 01-agent-D6-audit-trail.md

### AGENT-D7: QA Gaps
- domain: qa-gaps
- requirements: REQ-053 through REQ-058, REQ-065, REQ-069
- requirement_count: 8
- spec_sections: FR-6.1–FR-6.2, SC-4, SC-8
- cross_cutting_reqs: REQ-065 (baseline regression) touches all domains
- output: 01-agent-D7-qa-gaps.md

## Cross-Cutting Agents

### AGENT-CC1: Internal Consistency (Roadmap)
- scope: Full roadmap
- checks: ID schema consistency, count consistency (frontmatter vs body), table-to-prose consistency, cross-reference validity, no duplicate IDs, no orphaned items
- output: 01-agent-CC1-internal-consistency-roadmap.md

### AGENT-CC2: Internal Consistency (Spec)
- scope: Full spec
- checks: Section cross-refs valid, requirement counts match, no contradictions, numeric values consistent
- output: 01-agent-CC2-internal-consistency-spec.md

### AGENT-CC3: Dependency & Ordering
- scope: Roadmap + spec
- checks: Spec dependency chains in roadmap ordering, no circular deps, infrastructure before features, irreversible ops gated
- requirements: REQ-080 through REQ-083
- output: 01-agent-CC3-dependency-ordering.md

### AGENT-CC4: Completeness Sweep
- scope: Everything
- checks: Re-scan for missed requirements, every REQ has coverage claim, implicit systems
- requirements: REQ-074 through REQ-077, REQ-089 (constraints not primary to any domain)
- output: 01-agent-CC4-completeness-sweep.md

## Cross-Cutting Concern Matrix

| Requirement | Primary Agent | Secondary Agents | Integration Risk |
|-------------|--------------|------------------|-----------------|
| REQ-002 (no mocks) | D1 | D2, D3, D7, CC4 | MEDIUM |
| REQ-035 (mode ACs) | D3 | D1 | LOW |
| REQ-050 (checker integration) | D5 | D2 (convergence) | MEDIUM |
| REQ-065 (regression baseline) | D7 | All domains | HIGH |
| REQ-078 (JSONL per test) | D6 | D1, D2, D3, D7 | MEDIUM |
| REQ-029 (cross-path) | D2 | D3 | LOW |
| REQ-052 (FR-5.3=FR-4) | D5 | D4 | LOW |

## Assignment Verification

Union of all domain agent requirements = 79 unique REQs.
CC3 covers REQ-080–083 (4 sequencing).
CC4 covers REQ-074–077, REQ-089 (5 constraints).
Total: 79 + 4 + 1 = 84. Matches requirement universe. ✓
