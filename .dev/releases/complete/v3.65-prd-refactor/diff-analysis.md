---
total_diff_points: 11
shared_assumptions_count: 14
---

## Shared Assumptions and Agreements

1. **Complexity rating**: Both assign MEDIUM (0.45) complexity score
2. **Output structure**: Both target the same 4 refs/ files with identical names and content mappings
3. **Line count target**: Both enforce 430–500 line SKILL.md ceiling
4. **Combined line count**: Both target 1,370–1,400 total lines
5. **Token budget**: Both reference ≤2,000 token soft target for SKILL.md
6. **Content preservation**: Both mandate word-for-word fidelity with zero semantic drift
7. **BUILD_REQUEST changes**: Both identify exactly 6 SKILL CONTEXT FILE path changes
8. **Loading point**: Both agree refs/ loading happens only at Stage A.7
9. **Max concurrent refs**: Both enforce ≤2 refs loaded simultaneously by orchestrator
10. **Atomic commit**: Both require single-commit implementation with `git revert` rollback
11. **Component sync**: Both require `make sync-dev` + `make verify-sync`
12. **Risk inventory**: Both identify the same 7 risks with matching severity ratings
13. **B05/B30 merge strategy**: Both use append-only merge without cosmetic normalization
14. **Reference implementation**: Both use `sc-adversarial-protocol` refs/ pattern as template

---

## Divergence Points

### 1. Phase Count and Granularity

- **Opus**: 4 phases (Preparation → Content Extraction → SKILL.md Restructuring → Verification/Commit)
- **Haiku**: 5 phases (Baseline Setup → refs/ Creation → SKILL.md Refactor → Fidelity/Regression → Release Packaging)
- **Impact**: Haiku separates "baseline setup" (Phase 0) and "release packaging" (Phase 4) as distinct phases. Opus bundles preparation into Phase 1 and verification+commit into Phase 4. Haiku's separation makes Phase 0 a cleaner gate but adds overhead. Opus's bundling is more pragmatic for a medium-complexity task.

### 2. Timeline Estimates — Drastically Different

- **Opus**: 4.5–7 hours total (same-day completion)
- **Haiku**: 3.5–4.5 working days
- **Impact**: This is the single largest divergence. Opus treats this as a focused single-session mechanical task. Haiku estimates multi-day effort with separate roles. For a precision decomposition with well-defined boundaries and a fidelity index already in hand, Opus's estimate is more realistic — this is copy-paste with verification, not novel architecture. Haiku's estimate implies unnecessary ceremony.

### 3. Staffing Model

- **Opus**: Implicit single-implementer model (no roles defined)
- **Haiku**: Explicit 3-role model (Architect/Lead editor, Verification reviewer, Optional QA)
- **Impact**: Haiku's multi-person model adds review rigor but is overkill for a mechanical decomposition with automated diff checks. Opus assumes the implementer self-verifies, which is sufficient given the automatable success criteria.

### 4. Task Sequencing Within Content Extraction

- **Opus**: Explicitly calls out that tasks 2.1–2.3 are parallelizable, task 2.4 must follow (dependency on knowing destination paths)
- **Haiku**: Lists tasks 1–4 sequentially without parallelism guidance
- **Impact**: Opus's explicit parallelism analysis enables faster execution. Haiku misses an optimization opportunity.

### 5. Integration Point Documentation Depth

- **Opus**: Provides two detailed dispatch tables (refs/ File Registry + BUILD_REQUEST Dispatch Table) with columns for Named Artifact, Purpose, Owning Phase, Wired Components, and Consuming Phase
- **Haiku**: Provides 5 named integration points (IP-1 through IP-5) in a narrative format
- **Impact**: Opus's tabular format is more actionable during implementation — you can trace any ref from creation to consumption. Haiku's narrative format is easier to read but harder to audit for completeness. Haiku does identify one integration point Opus omits: the fidelity index itself as IP-3.

### 6. Risk Burn-Down Tracking

- **Opus**: Lists risks with mitigation strategies but no phase-linked retirement schedule
- **Haiku**: Adds explicit "Risk burn-down checkpoints" showing which risks retire after each phase
- **Impact**: Haiku's burn-down checkpoints provide better progress visibility. An implementer knows after Phase 1 that risks 1, 5, 6 are retired. Opus requires mental mapping.

### 7. B05/B30 Merge — Phase Assignment

- **Opus**: Assigns B05/B30 merge to Phase 3 (task 3.4, during SKILL.md restructuring)
- **Haiku**: Assigns it to Phase 1 (during refs/ creation, as IP-4)
- **Impact**: Opus's placement is more logical — the merge modifies content that stays in SKILL.md (B05), so it belongs with SKILL.md restructuring. Haiku's Phase 1 placement would require touching SKILL.md before the extraction phase is complete, creating an ordering dependency.

### 8. Open Questions Treatment

- **Opus**: Resolves OQ-1 and OQ-4 with concrete recommendations; confirms OQ-3 as non-issue
- **Haiku**: Lists all 4 open questions as unresolved, requiring sign-off before final delivery
- **Impact**: Opus is more decisive — providing recommendations inline reduces decision-making overhead. Haiku's approach is more conservative but risks blocking progress on questions that have obvious answers (e.g., OQ-3 is confirmed resolved by both variants).

### 9. Success Criteria Presentation

- **Opus**: Single table mapping all 12 criteria to check methods and pass conditions
- **Haiku**: Splits into requirement-level validation matrix (7 FR items) + non-functional validation (4 NFR items) + evidence artifacts list
- **Impact**: Opus's unified table is more actionable as a checklist. Haiku's structure traces back to spec requirements more cleanly but is harder to use as a pass/fail runsheet.

### 10. Frontmatter Completeness

- **Opus**: Includes `phases`, `total_tasks`, `estimated_effort`, `generated`, `generator` fields
- **Haiku**: Minimal frontmatter — only `spec_source`, `complexity_score`, `primary_persona`
- **Impact**: Opus's richer frontmatter enables automated tooling to parse and validate the roadmap. Haiku's sparse frontmatter loses machine-readability.

### 11. Evidence Artifact Specification

- **Opus**: Implicitly generates evidence through verification tasks
- **Haiku**: Explicitly lists 4 evidence artifact types (fidelity index, diff logs, grep outputs, E2E transcript)
- **Impact**: Haiku's explicit evidence list creates a clearer audit trail. Opus assumes evidence is a byproduct of verification tasks.

---

## Areas Where One Variant Is Clearly Stronger

### Opus is stronger in:
- **Timeline realism**: Hours not days — appropriate for mechanical decomposition
- **Parallelism analysis**: Explicit identification of parallelizable tasks
- **Decisiveness on open questions**: Provides concrete recommendations instead of deferring
- **Dispatch tables**: Tabular integration point documentation enables precise tracing
- **Frontmatter completeness**: Machine-readable metadata for tooling
- **Task granularity**: 18 named tasks with clear sequencing vs. Haiku's broader strokes
- **Success criteria as runsheet**: Single actionable checklist

### Haiku is stronger in:
- **Risk burn-down tracking**: Phase-linked risk retirement schedule
- **Evidence artifact specification**: Explicit deliverable list for audit trail
- **Fidelity index as integration point**: Recognizes the index itself as a wired artifact (IP-3)
- **Requirement traceability**: Each task explicitly names the FR/NFR it addresses

---

## Areas Requiring Debate to Resolve

1. **Timeline**: 4.5–7 hours vs. 3.5–4.5 days. Need to decide: is this a single-session focused task or a multi-day effort with review gates? The mechanical nature of the work (copy, verify, update 6 paths) favors Opus's estimate, but if independent review is required, Haiku's phasing is more appropriate.

2. **B05/B30 merge phase**: Phase 1 (Haiku) vs. Phase 3 (Opus). The merge modifies content staying in SKILL.md, which argues for Phase 3. But if refs/ files reference the merged table, it may need to happen earlier. Requires checking whether any refs/ file depends on B05 content.

3. **Open question resolution authority**: Should the roadmap resolve OQ-1 and OQ-4 inline (Opus) or defer to stakeholder sign-off (Haiku)? For a medium-complexity refactoring with clear precedent, inline resolution reduces friction. But if this roadmap feeds into a formal approval process, deferral may be required.

4. **Staffing model**: Single implementer with self-verification (Opus) vs. dedicated verification reviewer (Haiku). If the fidelity checks are fully automatable (they appear to be — diffs, greps, line counts), a single implementer is sufficient. If organizational policy requires independent review, Haiku's model applies.
