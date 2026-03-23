# Adversarial Validation — Verdict & Findings Report

## Metadata
- Validation date: 2026-03-19
- Architecture: `architecture-design.md` v1.0.0
- Requirements: `deterministic-fidelity-gate-requirements.md` v1.0.0
- Depth: deep | Convergence target: 0.90
- Total findings: 22

---

## VERDICT: CONDITIONAL

**Rationale**: Axes 2, 3, and 5 score below 7 (averages: 5.0, 5.5, 4.75 respectively). The architecture demonstrates strong structural coverage of most FRs and a coherent overall design, but contains 3 CRITICAL/HIGH findings that would cause runtime failures or incorrect behavior if implemented as-is, plus several HIGH-severity gaps that would force developers to invent missing specifications.

**Action required**: Resolve all BLOCKING FINDINGS below, then re-validate before implementation begins.

---

## BLOCKING FINDINGS (Must resolve before implementation)

### BF-1: ACTIVE Status Crashes __post_init__ (CRITICAL)
- **Axis**: 5 (Module Gaps)
- **Evidence**: Architecture Sec 4.4.2 uses `status="ACTIVE"`. Codebase `models.py`: `VALID_FINDING_STATUSES = frozenset({"PENDING", "FIXED", "FAILED", "SKIPPED"})` with __post_init__ ValueError.
- **Impact**: Any registry operation creating a Finding with status="ACTIVE" crashes at runtime.
- **Resolution**: Add "ACTIVE" to `VALID_FINDING_STATUSES` in the architecture. Document in Phase 1 migration plan (Finding extension).

### BF-2: Dual Authority Conflict — Registry vs SPEC_FIDELITY_GATE (HIGH)
- **Axis**: 2 (Data Flow)
- **Evidence**: Architecture Sec 5.3 retains SPEC_FIDELITY_GATE; Design Principle #3 says registry is authoritative.
- **Impact**: Registry says PASS (0 active HIGHs after debate) but spec-fidelity.md report may show HIGHs → SPEC_FIDELITY_GATE fails → false gate failure.
- **Resolution**: Either (a) generate spec-fidelity.md FROM registry state (report reflects registry), (b) remove SPEC_FIDELITY_GATE from the new flow and use only registry, or (c) explicitly sequence: registry update → report generation → gate check.

### BF-3: Semantic Non-Determinism Contaminates Monotonic Progress (HIGH)
- **Axis**: 3 (Convergence)
- **Evidence**: Architecture Sec 4.5 step 6 checks total HIGHs. Semantic layer is LLM-based (non-deterministic).
- **Impact**: Temperature variation in semantic layer can trigger false regression → expensive 3-worktree flow → wasted budget.
- **Resolution**: Track structural_high_count and semantic_high_count separately. Monotonic enforcement on structural only. Semantic fluctuations don't trigger regression detection.

### BF-4: Worktree Isolation Doesn't Isolate Input Files (HIGH)
- **Axis**: 3 (Convergence)
- **Evidence**: Architecture Sec 4.5.1 creates git worktrees. Roadmap files are in output_dir (not git-tracked).
- **Impact**: 3 "isolated" agents all read the same shared output files → no actual isolation.
- **Resolution**: Copy output artifacts (roadmap.md, spec-fidelity.md) into each worktree's temp directory before agent execution. Or use temp directories instead of worktrees.

### BF-5: --allow-regeneration Flag Missing (HIGH)
- **Axis**: 4 (Remediation)
- **Evidence**: FR-9 AC: "Full regeneration only with explicit user consent (--allow-regeneration flag)." Architecture has zero coverage.
- **Impact**: Required feature cannot be implemented.
- **Resolution**: Add `allow_regeneration: bool = False` to `RoadmapConfig`/`PipelineConfig`. Add CLI argument `--allow-regeneration` to roadmap command. Add check in `apply_patches()`: if any patch's `diff_size_ratio > threshold` AND `allow_regeneration` is True → override guard.

### BF-6: Lightweight Debate Unspecified (HIGH)
- **Axis**: 5 (Module Gaps)
- **Evidence**: Architecture Sec 4.3 describes "Two-agent debate via ClaudeProcess" with no prompt format, scoring criteria, round count, or token budget.
- **Impact**: Developer cannot implement without guessing at the debate protocol.
- **Resolution**: Specify: (1) prosecutor/defender prompt templates, (2) judge verdict criteria with evidence thresholds, (3) single-round vs multi-round, (4) token budget per debate, (5) output format (verdict + confidence + transcript).

### BF-7: NFR-3 Prompt Size Has No Enforcement Mechanism (HIGH)
- **Axis**: 5 (Module Gaps)
- **Evidence**: `build_semantic_prompt()` docstring says "Enforces NFR-3" but no truncation, splitting, or error handling is specified.
- **Impact**: First oversized section would produce an over-budget prompt with undefined behavior.
- **Resolution**: Specify: (1) section budget allocation (e.g., 30KB ÷ sections_count per dimension), (2) truncation strategy for oversized sections (tail-truncate? summarize?), (3) error behavior if single section > 30KB (split into sub-sections? skip with warning?).

---

## COMPLETE FINDINGS TABLE

| Finding ID | Axis | Severity | Evidence (Architecture) | Evidence (Requirements) | Recommended Resolution |
|------------|------|----------|------------------------|------------------------|----------------------|
| F-001 | 1 | MEDIUM | Sec 3.1: SpecData has no tables_by_section field | FR-2 AC: "Extracts markdown tables by section (keyed by heading path)" | Add `tables: dict[str, list[list[str]]]` to SpecData keyed by heading path |
| F-002 | 1 | MEDIUM | Sec 3.1: Only FunctionSignature extracted from code blocks | FR-2 AC: "Extracts fenced code blocks with language annotation" | Add `code_blocks: tuple[CodeBlock, ...]` with language and content fields |
| F-003 | 1 | MEDIUM | Sec 4.3: "only uncovered aspects" with no algorithm | FR-4: "receives only dimensions/aspects not covered by structural checkers" | Define explicit boundary: structural checkers declare their mismatch_types; anything not in any checker's rule table is "uncovered" |
| F-004 | 1 | HIGH | Sec 4.3: semantic HIGHs → lightweight debate | Resolved Q#2: full adversarial for FR-4 semantic HIGH; lightweight for FR-8 regression | Align with requirements: semantic HIGH → full debate; regression → lightweight |
| F-005 | 1 | MEDIUM | Sec 4.4.2: Adds ACTIVE status to registry | FR-6: "Statuses: FIXED, SKIPPED, FAILED" | Document ACTIVE as justified extension with compatibility update |
| F-006 | 1 | MEDIUM | Sec 10: NFR-7 "Steps 1-7 untouched" | Phase 5: removes build_spec_fidelity_prompt from prompts.py | Clarify: prompts.py removal doesn't affect steps 1-7 (only step 8 used it) |
| F-007 | 2 | MEDIUM | Sec 3.1: frozen=True with mutable dict fields | Design Principle #2: "immutable data flow" | Use tuple-of-tuples or MappingProxyType for lookup indexes |
| F-008 | 2 | MEDIUM | Sec 4.2.3: compute_stable_id(f.dimension, f.rule_id, f.location, **f.rule_id**) | FR-6: stable_id from (dimension, rule_id, spec_location, **mismatch_type**) | Fix call: `compute_stable_id(f.dimension, f.rule_id, f.location, f.mismatch_type)` — requires Finding to have mismatch_type field |
| F-009 | 2 | LOW | Sec 4.2.3: f.stable_id = ... after parallel collection | Design Principle #2: "immutable data flow" | Assign stable_id during Finding construction in each checker |
| F-010 | 2 | HIGH | Sec 5.3: SPEC_FIDELITY_GATE retained | Design Principle #3: "registry-centric gate" | **BLOCKING** — See BF-2 |
| F-011 | 3 | LOW | Sec 4.5: budget arithmetic | FR-8: "this entire flow counts as one run" | Correct — no action needed |
| F-012 | 3 | HIGH | Sec 4.5: monotonic check on total HIGHs | NFR-1: structural determinism | **BLOCKING** — See BF-3 |
| F-013 | 3 | HIGH | Sec 4.5.1: git worktrees for isolation | FR-8: "each in its own git worktree" | **BLOCKING** — See BF-4 |
| F-014 | 3 | MEDIUM | Sec 4.5: semantic layer runs regardless of structural results | No explicit requirement | Add short-circuit: skip semantic layer if structural HIGHs = 0 AND all dimensions checked |
| F-015 | 4 | MEDIUM | Sec 4.6.2: fallback_apply() fuzzy matching underspecified | FR-9 AC: "deterministic Python text replacement" | Specify exact fuzzy algorithm: strip leading whitespace per line, normalize line endings, then exact match |
| F-016 | 4 | MEDIUM | Sec 4.6.2: no minimum anchor size | FR-9: original_code as anchor | Recommend minimum anchor of 5 lines or 200 chars to reduce ambiguity |
| F-017 | 4 | HIGH | No coverage | FR-9 AC: "--allow-regeneration flag" | **BLOCKING** — See BF-5 |
| F-018 | 5 | HIGH | Sec 4.3: 3-role description for "2-agent" debate, no spec | Resolved Q#2: distinguishes lightweight vs full | **BLOCKING** — See BF-6 |
| F-019 | 5 | MEDIUM | Appendix B: convergence.py → all modules | N/A (design concern) | Extract orchestration algorithm to accept pre-built components as parameters |
| F-020 | 5 | HIGH | Sec 4.3: docstring only for 30KB enforcement | NFR-3: "No single prompt exceeds 30KB" | **BLOCKING** — See BF-7 |
| F-021 | 5 | CRITICAL | Sec 4.4.2: status="ACTIVE" | Codebase: VALID_FINDING_STATUSES excludes ACTIVE | **BLOCKING** — See BF-1 |
| F-022 | 6 | MEDIUM | Phase 5 item 12 vs Sec 2.3 | Internal contradiction | Update Sec 2.3: prompts.py is MODIFIED (dead code removal) |

## Findings Summary by Severity

| Severity | Count | Blocking |
|----------|-------|----------|
| CRITICAL | 1 | 1 (BF-1) |
| HIGH | 7 | 6 (BF-2 through BF-7) |
| MEDIUM | 12 | 0 |
| LOW | 2 | 0 |
| **Total** | **22** | **7** |

## Per-Axis Score Summary

| Axis | Coverage | Consistency | Implementability | Risk ID | Average | Verdict |
|------|----------|-------------|-----------------|---------|---------|---------|
| 1. FR/NFR Coverage | 6 | 7 | 6 | 5 | 6.0 | CONDITIONAL |
| 2. Data Flow | 7 | 4 | 6 | 3 | 5.0 | CONDITIONAL |
| 3. Convergence | 7 | 5 | 7 | 3 | 5.5 | CONDITIONAL |
| 4. Remediation | 6 | 8 | 6 | 7 | 6.75 | CONDITIONAL |
| 5. Module Gaps | 5 | 6 | 4 | 4 | 4.75 | CONDITIONAL |
| 6. Migration | 7 | 6 | 7 | 6 | 6.5 | CONDITIONAL |

**No axis reaches ≥ 7 average** → CONDITIONAL verdict.
**No axis drops ≤ 3 average** → Not rejected.

---

## Recommended Resolution Priority

1. **BF-1** (CRITICAL, 5 min fix): Add "ACTIVE" to VALID_FINDING_STATUSES
2. **BF-2** (HIGH, design decision): Resolve dual authority — recommend option (c): registry update → report generation → gate check
3. **BF-3** (HIGH, algorithm change): Separate structural/semantic HIGH tracking in convergence engine
4. **BF-4** (HIGH, implementation detail): Copy output files to temp dirs per worktree agent
5. **BF-5** (HIGH, new feature): Add --allow-regeneration to config + CLI + guard
6. **BF-6** (HIGH, spec work): Fully specify lightweight debate protocol
7. **BF-7** (HIGH, algorithm design): Specify prompt truncation/splitting mechanism

After resolving all 7 blocking findings, re-run this validation to confirm axis scores reach ≥ 7.
