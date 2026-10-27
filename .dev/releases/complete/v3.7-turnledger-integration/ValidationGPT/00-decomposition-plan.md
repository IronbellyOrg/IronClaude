# Decomposition Plan

## Domain Agent Assignments

| Agent | Domain | Requirement Scope | Output |
|---|---|---|---|
| D1 | Wiring E2E | REQ-001–REQ-021 | `01-agent-D1-wiring-e2e.md` |
| D2 | Lifecycle & Modes | REQ-022–REQ-035 | `01-agent-D2-lifecycle-and-modes.md` |
| D3 | Reachability & Pipeline | REQ-036–REQ-043, REQ-050–REQ-053 | `01-agent-D3-reachability-and-pipeline.md` |
| D4 | Audit & Quality Gates | REQ-044–REQ-049, REQ-054 | `01-agent-D4-audit-and-quality-gates.md` |

## Mandatory Cross-Cutting Agents

| Agent | Purpose | Output |
|---|---|---|
| CC1 | Roadmap internal consistency | `01-agent-CC1-roadmap-consistency.md` |
| CC2 | Spec internal consistency | `01-agent-CC2-spec-consistency.md` |
| CC3 | Dependency and ordering | `01-agent-CC3-dependency-ordering.md` |
| CC4 | Completeness sweep | `01-agent-CC4-completeness-sweep.md` |

## Cross-Cutting Concern Matrix

| Requirement / Concern | Primary Agent | Secondary Agents | Integration Risk |
|---|---|---|---|
| FR-4.4 reachability regression | D3 | D1, CC3 | HIGH |
| FR-5.2 `_run_checkers()` integration | D3 | D2, CC1 | HIGH |
| NFR-1 no-mock realism | D4 | D1, D2, CC4 | HIGH |
| SC-12 audit verifiability | D4 | D1, D2 | MEDIUM |
| FR-6 gap closure items | D3 | D1, D2, CC4 | MEDIUM |

## Assignment Integrity Check

- Full extracted universe assigned across D1-D4.
- CC4 also re-checks missed/orphan requirements and any extraction boundary gaps.
- Known likely misses to challenge in consolidation: FR-1.19, FR-1.20, FR-1.21, FR-2.1a, explicit stop-condition requirements on checkpoints.
