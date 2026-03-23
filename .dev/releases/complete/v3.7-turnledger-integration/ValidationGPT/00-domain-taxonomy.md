# Domain Taxonomy

## Domains

| Domain | Scope | Requirement Count | Rationale |
|---|---|---:|---|
| D1 Wiring E2E | FR-1.x wiring-point coverage, KPI, wrapper-call, config derivation | 21 | Dense executor-path behavioral test surface |
| D2 Lifecycle & Modes | FR-2.x TurnLedger lifecycle + FR-3.x rollout and exhaustion scenarios | 14 | Shared budget/mode semantics and execution-path behavior |
| D3 Reachability & Pipeline | FR-4.x reachability framework, FR-5.x pipeline fixes, FR-6.x QA gap closure | 11 | Static-analysis, checker integration, and gap closure are tightly coupled |
| D4 Audit & Quality Gates | FR-7.x audit trail + NFR/SC release gates | 8 | Cross-cutting evidence, no-mock, UV-only, baseline and verifiability constraints |

## Cross-Cutting Requirements

| Requirement | Primary Domain | Secondary Review |
|---|---|---|
| NFR-1 no mocks on gate/core orchestration logic | D4 | D1, D2 |
| SC-12 third-party verifiable audit trail | D4 | D1, D2 |
| FR-4.4 broken wiring regression test | D3 | D1 |
| FR-5.2 checker integration in `_run_checkers()` | D3 | D2 |
| FR-6.1 / FR-6.2 QA gap closure | D3 | D1, D2 |

## Taxonomy Notes

- No prior taxonomy supplied.
- Four primary domains are sufficient; mandatory cross-cutting checks will cover consistency, dependency ordering, spec coherence, and completeness.
- Domain split is evidence-based from spec sectioning and roadmap phase structure.
