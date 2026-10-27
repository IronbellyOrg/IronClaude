# Deterministic Fidelity Gate -- Workflow Summary

**Total tasks**: 24 | **Groups**: 6 | **Generated**: 2026-03-19

---

## Task Index

### Group 1: Foundation -- models.py (No Dependencies)
- 1.1: Add ACTIVE to VALID_FINDING_STATUSES (BF-1)
- 1.2: Update Finding docstring lifecycle (BF-1)
- 1.3: Add source_layer field to Finding dataclass (BF-3)
- 1.4: Add convergence_enabled field to RoadmapConfig (BF-2)
- 1.5: Add allow_regeneration field to RoadmapConfig (BF-5)

### Group 2: Architecture Design Doc (No Code Dependencies)
- 2.1: Update Section 4.4 -- ACTIVE status clarification (BF-1)
- 2.2: Update Section 5.1 -- Conditional step 8 construction (BF-2)
- 2.3: Replace Section 5.3 -- Gate Authority Model (BF-2)
- 2.4: Amend Design Principle #3 (BF-2)
- 2.5: Update Section 4.5 -- Split structural/semantic tracking (BF-3)
- 2.6: Update FR-7 and FR-8 acceptance criteria (BF-3)
- 2.7: Replace Section 4.5.1 -- Temp directory isolation (BF-4)
- 2.8: Update Section 4.6.2 -- allow_regeneration parameter (BF-5)
- 2.9: Update Section 4.3 -- Debate protocol specification (BF-6)
- 2.10: Add Section 4.3.1 -- Prompt budget enforcement (BF-7)

### Group 3: Convergence Engine (Depends on Group 1)
- 3.1: Add split structural/semantic HIGH tracking to registry (BF-3)
- 3.2: Implement structural-only monotonic enforcement (BF-3)
- 3.3: Replace worktree isolation with temp directories (BF-4)
- 3.4: Implement registry-only gate evaluation in convergence mode (BF-2)

### Group 4: Semantic Layer / Debate (Depends on Group 3)
- 4.1: Implement lightweight debate protocol (BF-6)
- 4.2: Implement prompt budget enforcement (BF-7)
- 4.3: Wire debate verdicts into registry (BF-6)

### Group 5: Remediation Changes (Depends on Group 1)
- 5.1: Add --allow-regeneration CLI flag (BF-5)
- 5.2: Implement diff-size guard with override logic (BF-5)

### Group 6: Integration Tests (Depends on All Above)
- 6.1: BF-1 -- ACTIVE status tests
- 6.2: BF-2 -- Dual authority elimination tests
- 6.3: BF-3 -- Split tracking and regression tests
- 6.4: BF-4 -- Temp directory isolation tests
- 6.5: BF-5 -- Allow-regeneration tests
- 6.6: BF-6 -- Debate protocol tests
- 6.7: BF-7 -- Prompt budget tests

---

## Dependency Graph

```
Group 1: models.py
  |
  +---> Group 3: convergence.py + executor.py
  |       |
  |       +---> Group 4: semantic_layer.py
  |
  +---> Group 5: remediate_executor.py + commands.py
  |
  [Group 2: architecture-design.md -- parallel with any code group]
  |
  +---> Group 6: Integration tests (after all code groups)

Execution order:
  [Group 1] --+--> [Group 3] --> [Group 4]
              |
              +--> [Group 5]
              |
  [Group 2] --+--> [Group 6]
```

---

## BF Coverage Matrix

| BF | Group 1 | Group 2 | Group 3 | Group 4 | Group 5 | Group 6 |
|----|---------|---------|---------|---------|---------|---------|
| BF-1 | 1.1, 1.2 | 2.1 | -- | -- | -- | 6.1 |
| BF-2 | 1.4 | 2.2, 2.3, 2.4 | 3.4 | -- | -- | 6.2 |
| BF-3 | 1.3 | 2.5, 2.6 | 3.1, 3.2 | -- | -- | 6.3 |
| BF-4 | -- | 2.7 | 3.3 | -- | -- | 6.4 |
| BF-5 | 1.5 | 2.8 | -- | -- | 5.1, 5.2 | 6.5 |
| BF-6 | -- | 2.9 | -- | 4.1, 4.3 | -- | 6.6 |
| BF-7 | -- | 2.10 | -- | 4.2 | -- | 6.7 |
