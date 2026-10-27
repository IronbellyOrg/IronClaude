

---
base_variant: A
variant_scores: "A:81 B:75"
---

# Scoring Criteria

Derived from the debate's 12 divergence points and the convergence assessment, weighted by impact on implementability:

| Criterion | Weight | Rationale |
|-----------|--------|-----------|
| **Execution readiness** | 25% | Can a sprint CLI consume this directly? (D03, D04) |
| **Scope discipline** | 20% | Does the roadmap stay within technical sequencing? (D09, D10, D11) |
| **Architectural precision** | 20% | File paths, CREATE/MODIFY annotations, dependency DAG (D04, D05) |
| **Risk mitigation quality** | 15% | Actionable mitigations vs framework overhead (D06, D10) |
| **Flexibility & resilience** | 10% | Handles single-implementer AND multi-session scenarios (D02, D08) |
| **Completeness of detail** | 10% | Report sections, type specs, milestone definitions (D05, D07) |

---

# Per-Criterion Scores

## 1. Execution Readiness (25%)

| Aspect | A (Opus) | B (Haiku) |
|--------|----------|-----------|
| Task IDs (T01–T15) | Yes — sprint CLI consumable | No — milestones only (M1.1–M6.4) |
| Dependency DAG | Explicit per-task | Phase-level only |
| File paths with CREATE/MODIFY | Every task | Absent |
| Parallelism annotations | Per-task (T01∥T02, T06∥T07) | Phase-level only |

**Scores**: A: 92, B: 65

Debate evidence: Haiku conceded in Round 3 that "task IDs are necessary for tooling" and "sprint CLI requires formal task identifiers." Opus's format is directly consumable; Haiku's requires a translation step.

## 2. Scope Discipline (20%)

| Aspect | A (Opus) | B (Haiku) |
|--------|----------|-----------|
| Staffing model | Absent (appropriate) | 4 engineer roles specified |
| Operational dependencies | Not in main body | Embedded in Phase 0 and Section 4 |
| Governance/promotion ownership | Deferred to project plan | In roadmap body |
| Roadmap scope boundary | Technical sequencing | Project plan hybrid |

**Scores**: A: 85, B: 68

Debate evidence: Haiku conceded staffing model is "over-specified" for Claude Code context. Opus correctly argued operational dependencies conflate "what to build" with "how to deploy." However, Haiku raises a valid point that governance gaps can block value delivery — this belongs in an appendix, not the core roadmap.

## 3. Architectural Precision (20%)

| Aspect | A (Opus) | B (Haiku) |
|--------|----------|-----------|
| File layout commitment | `audit/wiring_config.py` (CREATE) explicit | Deferred to Phase 0 |
| Module boundary decisions | Made upfront | Deferred |
| Import/layering constraints | Explicit (frontmatter regex duplication noted) | Mentioned but less specific |
| Cut decisions | T06 CUT-ELIGIBLE with clear criterion | Phase 5 deferrable, less precise |

**Scores**: A: 85, B: 72

Debate evidence: Haiku conceded "separate `wiring_config.py` is likely correct" and that Phase 0 confirmation is a safety check, not a genuine open question. Opus's upfront commitment enables earlier parallelism.

## 4. Risk Mitigation Quality (15%)

| Aspect | A (Opus) | B (Haiku) |
|--------|----------|-----------|
| Risk table format | Compact, actionable (Impact + Mitigation) | 4-layer model (Prevent→Detect→Contain→Recover) |
| Whitelist error handling | Strict from day one | Phase-aware warn→error |
| Specificity of mitigations | Concrete actions per risk | Framework categories |
| Merge coordination | Explicit recommendation (v3.0 first) | Mentioned but less specific |

**Scores**: A: 80, B: 73

Debate evidence: Haiku conceded "phase-aware warn→error adds complexity" and strict validation is simpler. Opus's flat table is more directly actionable. However, Haiku's 4-layer framing provides a useful completeness check — worth incorporating as a one-paragraph summary.

## 5. Flexibility & Resilience (10%)

| Aspect | A (Opus) | B (Haiku) |
|--------|----------|-----------|
| Phase 0 checkpoint | Conceded as lightweight gate | Full phase with exit criteria |
| Phase separation | 6 phases (bundled integration) | 7 phases (separated) |
| Multi-implementer support | Weak (assumes single session) | Stronger (parallel tracks explicit) |
| Cut flexibility | T06 + Phase 4 deferrable | Phase 5 deferrable |

**Scores**: A: 68, B: 82

Haiku's separated phases and explicit parallel tracks are genuinely more resilient to multi-session scenarios. Opus optimizes for the common case (single implementer) but is less adaptable.

## 6. Completeness of Detail (10%)

| Aspect | A (Opus) | B (Haiku) |
|--------|----------|-----------|
| Report body sections | Not enumerated | All 7 listed in order |
| `SprintConfig` type | Not specified | `Literal["off", "shadow", "soft", "full"]` |
| Public API signatures | Mentioned | Explicitly listed with params |
| Promotion gate thresholds | Present | Present with more detail |

**Scores**: A: 65, B: 88

Debate evidence: Opus conceded both report section enumeration and the `Literal` type specification. Haiku is stronger here.

---

# Overall Scores

| Criterion | Weight | A (Opus) | B (Haiku) | A Weighted | B Weighted |
|-----------|--------|----------|-----------|------------|------------|
| Execution readiness | 25% | 92 | 65 | 23.0 | 16.3 |
| Scope discipline | 20% | 85 | 68 | 17.0 | 13.6 |
| Architectural precision | 20% | 85 | 72 | 17.0 | 14.4 |
| Risk mitigation quality | 15% | 80 | 73 | 12.0 | 11.0 |
| Flexibility & resilience | 10% | 68 | 82 | 6.8 | 8.2 |
| Completeness of detail | 10% | 65 | 88 | 6.5 | 8.8 |
| **Total** | **100%** | | | **82.3** | **72.3** |

**Rounded: A: 82, B: 72**

---

# Base Variant Selection Rationale

**Variant A (Opus)** is selected as the merge base for three reasons:

1. **Sprint CLI compatibility**: The T01–T15 task ID scheme with file paths, CREATE/MODIFY annotations, and explicit dependency DAG is directly consumable by the tasklist generator. Haiku's milestone-only format would require restructuring the entire organizational scheme.

2. **Structural simplicity**: Opus's 6-phase structure with compact risk tables and focused technical scope requires less refactoring to merge than Haiku's 7-phase governance-heavy structure would need to be trimmed.

3. **Debate trajectory**: Haiku made more concessions (4) than Opus (4), but Haiku's concessions were on more structurally significant points (task IDs are necessary, strict validation is simpler, staffing is over-specified, separate config file is correct). Opus's concessions (Phase 0 checkpoint, report sections, Literal type, operational appendix) are all additive patches to an otherwise solid structure.

---

# Specific Improvements to Incorporate from Variant B (Haiku)

These should be merged into Variant A during the merge step:

1. **Phase 0 checkpoint with exit criteria** (D01): Add a named "Phase 0: Architecture Confirmation" section before Phase 1 with Haiku's M0.1–M0.3 milestones and timeboxed to 0.5–1 session. Use Haiku's 5-point confirmation checklist but keep it as a gate, not a full implementation phase.

2. **Report body section enumeration** (D05, conceded): Add the 7 body section names to the T04 description in Phase 1.

3. **`Literal["off", "shadow", "soft", "full"]` type specification** (D07, conceded): Add to T09's description in Phase 3.

4. **Public API signatures** (from Haiku's Phase 0): Add `run_wiring_analysis(target_dir, config?) -> WiringReport`, `emit_report(report, output_path, enforcement_mode)`, and `ast_analyze_file(file_path, content) -> FileAnalysis` as the acceptance contract.

5. **4-layer risk framing paragraph** (D10): Add a single paragraph before Opus's risk table introducing the Prevent→Detect→Contain→Recover model as a completeness check, then keep Opus's actionable flat table.

6. **Operational dependencies appendix** (D09, compromise): Add a new Section 8 "Deployment Readiness Prerequisites" listing Haiku's 5 operational dependencies (provider_dir_names confirmation, whitelist governance owner, promotion review owner, merge coordination plan, shadow telemetry process).

7. **Separated sprint integration note** (D02): Add a note to Phase 3 that in multi-implementer scenarios, T09 can be separated into its own phase and started after Phase 1 stabilizes.

8. **Phase-level critical path** (D12): Add Haiku's phase-level critical path (Phase 0→1→2→3→6, Phase 4 after Phase 1, Phase 5 off critical path) alongside Opus's existing task-level critical path.
