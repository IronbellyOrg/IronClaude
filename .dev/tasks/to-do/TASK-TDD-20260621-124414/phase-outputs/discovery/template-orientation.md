# TDD Template Orientation — FR-DRS Heavyweight TDD

**Source template:** `src/superclaude/examples/tdd_template.md` (v1.2, read in full)
**Status:** Complete
**Date:** 2026-06-21

## (a) The 28 ordered section headers (verbatim from template)

1. Executive Summary
2. Problem Statement & Context
3. Goals & Non-Goals
4. Success Metrics
5. Technical Requirements
6. Architecture
7. Data Models
8. API Specifications
9. State Management
10. Component Inventory
11. User Flows & Interactions
12. Error Handling & Edge Cases
13. Security Considerations
14. Observability & Monitoring
15. Testing Strategy
16. Accessibility Requirements
17. Performance Budgets
18. Dependencies
19. Migration & Rollout Plan
20. Risks & Mitigations
21. Alternatives Considered
22. Open Questions
23. Timeline & Milestones
24. Release Criteria
25. Operational Readiness
26. Cost & Resource Estimation
27. References & Resources
28. Glossary

Preceding the numbered sections: frontmatter (YAML), Document Information table, Approvers table,
Completeness Status (checklist + Contract Table), Table of Contents. Trailing: Appendices A–D,
Document History.

## (b) Backend/library tailoring decisions for THIS TDD

- **§9 State Management** — **N/A with rationale:** backend/library + CLI component, no frontend/client-side state.
- **§10 Component Inventory** — **N/A with rationale:** backend/library + CLI component, no UI page/route/component tree.
- **§16 Accessibility Requirements** — **N/A with rationale:** backend/library + CLI component, no user-facing UI surface.
- **§8 API Specifications** — **REPURPOSED** as the **module/function API** of the sweep (public functions,
  signatures) + the **six `runtime_surface_*` contract scalars** and `RuntimeSurfaceLedgerRow` TypedDict.
  NOT HTTP endpoints. Use the §8 versioning/governance sub-tables to express the additive-only contract
  versioning posture (OQ-DRS.3: producer change, likely no version bump from 1.6.0).
- **§7 Data Models** — the `runtime-surface-ledger.yaml` schema (one row per evaluated edge),
  `RuntimeSurfaceLedgerRow` TypedDict field-by-field, the per-symbol reduction precedence
  (`DEGRADE-on-any-incompleteness > UNREACHED > REACHED`), and the count invariant
  `len(unreached_surfaces) == runtime_surface_unreached`.
- **§13 Security Considerations** — **LIGHT:** local-only file writes under `<output>/`, no network, no
  prod service, no auth/PII. Threat surface = path traversal / writing outside `<output>/` (mitigated by
  atomic writes scoped to the output dir).
- **§17 Performance Budgets** — **LIGHT:** the sweep extends already-fetched referrers (no second fetch);
  budget framed as "zero added cost on non-surface diffs; bounded ripgrep/AST passes on surface diffs."
- **§26 Cost & Resource Estimation** — **LIGHT / mostly N/A:** no infra cost; local compute only.

## (c) MANDATORY output-path override

The final assembled TDD goes to:
`/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect-hardening/issue-3-deterministic-runtime-surface-sweep/tdd.md`
— **NOT** the template default `docs/[domain]/TDD_[COMPONENT-NAME].md`. Sibling to spec.md, matching the
issue-2-headless-ensemble pattern. This is a worktree; all paths resolve to the worktree absolute root.

## (d) Line budget

Heavyweight: **1,200–1,800 lines, hard cap 2,000.** A document over the ceiling needs editing, not a larger
tier. N/A sections (§9/§10/§16) are one-liners-with-rationale, conserving budget for §5/§6/§7/§8/§12/§15/§21.
