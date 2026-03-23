---
phase: 1
title: "Spec Rewrite"
tasks: 5
depends_on: []
parallelizable: true
---

# Phase 1: Spec Rewrite

All tasks modify `deterministic-fidelity-gate-requirements.md` only. No code changes.
Tasks are independent and can execute in parallel.

---

### T01: Reclassify existing modules from CREATE to MODIFY

**Tier**: simple
**File**: deterministic-fidelity-gate-requirements.md
**FR**: FR-4, FR-7, FR-8, FR-9

**Action**: In each FR section that claims a module should be created, change language to acknowledge the module already exists and describe extension work:

| FR | Current Language | New Language |
|----|-----------------|-------------|
| FR-4 | "build semantic layer module" | "complete existing semantic_layer.py: add validate_semantic_high() and run_semantic_layer() orchestrators" |
| FR-7 | "create convergence engine" | "extend existing convergence.py: add execute_fidelity_with_convergence() loop orchestrator" |
| FR-8 | "create temp-dir isolation" | "extend convergence.py: add handle_regression() using existing _create_validation_dirs/_cleanup infrastructure" |
| FR-9 | "create remediation" | "extend existing remediate_executor.py: add MorphLLM-compatible patch format, change threshold 50→30, per-file rollback" |

**Acceptance criteria**:
- [ ] No FR section claims convergence.py, semantic_layer.py, or remediate_executor.py as new modules
- [ ] Each section references existing code locations with line numbers
- [ ] Extension work is clearly distinguished from pre-existing functionality

---

### T02: Add "existing baseline from v3.0" section

**Tier**: simple
**File**: deterministic-fidelity-gate-requirements.md (new section between §1 and §2)

**Action**: Add a new section documenting what v3.0 already implemented:

```markdown
## 1.3 Pre-Existing Implementation Baseline (v3.0)

The following were implemented in v3.0 (commit f4d9035) and are available as-is:

### Modules
- convergence.py (323 lines): DeviationRegistry, compute_stable_id, ConvergenceResult, _check_regression, temp dir isolation
- semantic_layer.py (336 lines): RubricScores, build_semantic_prompt, score_argument, judge_verdict, budget enforcement
- remediate_executor.py (563 lines): snapshot/restore, allowlist, parallel execution, diff-size guard (50%)

### Model/Config Fields
- ACTIVE in VALID_FINDING_STATUSES (models.py:16)
- Finding.source_layer (models.py:44)
- RoadmapConfig.convergence_enabled (models.py:107)
- RoadmapConfig.allow_regeneration (models.py:108)

### Pipeline Wiring
- SPEC_FIDELITY_GATE conditional bypass (executor.py:521)
- WIRING_GATE in ALL_GATES (gates.py:944)
- --allow-regeneration CLI flag (commands.py:89-94)

### Run-to-Run Memory (FR-10)
- get_prior_findings_summary() (convergence.py:179-188)
- prior_findings_summary in semantic prompt (semantic_layer.py:140,215-221)
- first_seen_run/last_seen_run tracking (convergence.py:104-130)
```

**Acceptance criteria**:
- [ ] Section lists all 19 already-implemented requirements from CompatibilityReport §2
- [ ] Each item has file:line reference
- [ ] Section is placed before functional requirements

---

### T03: Document FR-10 as pre-implemented

**Tier**: simple
**File**: deterministic-fidelity-gate-requirements.md, FR-10 section

**Action**: Add a note at the top of FR-10 stating that all acceptance criteria are already satisfied by v3.0:

```markdown
> **Status**: Pre-implemented by v3.0. All acceptance criteria verified:
> - `get_prior_findings_summary()` at convergence.py:179-188
> - `prior_findings_summary` field in SemanticCheckRequest at semantic_layer.py:140
> - Prompt integration at semantic_layer.py:215-221
> - `first_seen_run`/`last_seen_run` tracking at convergence.py:104-130
```

**Acceptance criteria**:
- [ ] FR-10 clearly marked as pre-implemented
- [ ] Code references are accurate

---

### T04: Update spec relates_to and module map

**Tier**: simple
**File**: deterministic-fidelity-gate-requirements.md, YAML frontmatter + Appendix A

**Action**:
1. In frontmatter `relates_to`: remove `deviation_registry.py` (class is inside convergence.py, not a separate file)
2. In Appendix A architecture diagram: update to show convergence.py, semantic_layer.py, remediate_executor.py as MODIFY not CREATE
3. Add spec_patch.py to relates_to with note: "preserved legacy — accepted-deviation workflow coexists with v3.05"

**Acceptance criteria**:
- [ ] deviation_registry.py removed from relates_to (or marked as "class within convergence.py")
- [ ] spec_patch.py explicitly scoped
- [ ] Architecture diagram matches current reality

---

### T05: Add --convergence-enabled CLI flag exposure decision

**Tier**: simple
**File**: deterministic-fidelity-gate-requirements.md, FR-7 section

**Action**: The `convergence_enabled` config field exists (models.py:107) but has no CLI flag exposure. Add to FR-7:

```markdown
**CLI Exposure**: Add `--convergence-enabled` as a Click `is_flag=True` option on the `run` command,
mirroring the existing `--allow-regeneration` pattern (commands.py:89-94). Default: False (legacy behavior).
```

**Acceptance criteria**:
- [ ] FR-7 specifies CLI flag for convergence_enabled
- [ ] Default preserves legacy behavior
