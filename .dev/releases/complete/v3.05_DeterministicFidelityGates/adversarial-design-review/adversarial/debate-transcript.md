# Adversarial Validation Transcript — Pre-Implementation Architecture Gate

## Metadata
- Mode: VALIDATION (not standard compare-and-merge)
- Artifact A (CLAIM): `architecture-design.md` v1.0.0
- Artifact B (AUTHORITY): `deterministic-fidelity-gate-requirements.md` v1.0.0
- Depth: deep
- Convergence threshold: 0.90
- Focus: fr-nfr-coverage, data-flow, convergence, remediation, module-gaps, migration
- Axes evaluated: 6
- Validation date: 2026-03-19

---

## AXIS 1: FR/NFR Coverage Completeness (Traceability Gate)

### FR-by-FR Analysis

#### FR-1 (5 Structural Checkers) — COVERED
Architecture Section 4.2.2 defines all 5 checkers with complete rule tables. 17 rules in architecture vs 15 in requirements (2 additional rules: `id_missing`, `field_missing`). Extension is justified and non-breaking. Checker protocol, parallel execution, and registry are all specified.

#### FR-2 (Spec Parser) — PARTIAL COVERAGE
Two of 9 extraction targets lack corresponding SpecData fields:
- **Markdown tables by heading path**: Parser implementation notes mention table parsing, but no `tables_by_section` field in SpecData. Tables are parsed from `SpecSection.content` downstream, but this violates the "returns structured objects, not raw text" AC.
- **Fenced code blocks with language**: Only Python function signatures extracted. Generic code blocks (e.g., YAML, JSON, shell) are not preserved as structured data.

#### FR-3 (Anchored Severity) — COVERED
Rules defined in code as `SeverityRuleTable` dicts (module-level constants). Keyed by `mismatch_type → severity` per checker (dimension implicit from checker class). Functionally equivalent to `(dimension, mismatch_type) → severity`. Extensible by dict addition.

#### FR-4 (Residual Semantic Layer) — PARTIAL COVERAGE
Semantic layer defined with chunked input, structural findings as context, and adversarial debate for HIGHs. **Gap**: No algorithm for determining what's "uncovered" by structural checkers. The semantic layer receives "only dimensions/aspects not covered" but how this is computed is unspecified.

#### FR-5 (Sectional Comparison) — COVERED
`DIMENSION_SECTIONS` mapping covers all 5 dimensions. `get_sections_for_dimension()` handles supplementary sections via cross-references.

#### FR-6 (Deviation Registry) — COVERED (with status extension)
JSON schema includes all required fields. Architecture adds `ACTIVE` status not in requirements. Status extension is justified but creates backward compatibility issue with existing `VALID_FINDING_STATUSES`.

#### FR-7 (Convergence Gate) — COVERED
Registry-based evaluation with `active_high_count == 0` pass condition. 3-run budget enforced. Regression detection triggers FR-8. Progress logging implemented.

#### FR-8 (Regression Detection) — PARTIAL COVERAGE
3 worktree agents, merge by stable_id, adversarial debate on HIGHs all specified. **Gaps**: (1) Sorting by severity not explicitly mentioned in `handle_regression()`. (2) Debate variant contradicts resolved Q#2 — architecture says full /sc:adversarial for regression, requirements say lightweight.

#### FR-9 (Edit-Only Remediation) — PARTIAL COVERAGE
Patch model matches MorphLLM format. Diff-size guard, fallback applicator, per-file rollback all specified. **Gap**: `--allow-regeneration` flag has zero architectural coverage — no CLI surface, no config field, no enforcement point.

#### FR-10 (Run-to-Run Memory) — COVERED
`get_prior_findings_summary(max_entries=50)`, `first_seen_run`/`last_seen_run` tracking, oldest-first truncation all specified.

### NFR Compliance Challenges

| NFR | Compliance Matrix Claim | Challenge Result |
|-----|------------------------|-----------------|
| NFR-1 | "Pure functions; same inputs → same output" | ACCURATE for structural only. Semantic layer is non-deterministic by nature. Claim is correctly scoped. |
| NFR-2 | "max_runs=3 hard limit" | VERIFIED in convergence engine. |
| NFR-3 | "Section-level chunking; byte_size tracked" | INSUFFICIENT. Docstring promise only. No truncation mechanism, no error handling for over-budget prompts, no section-splitting logic. |
| NFR-4 | "Frozen dataclasses; no shared state" | MISLEADING. SpecData is frozen=True but contains mutable dict fields. Finding is NOT frozen. The compliance claim overstates the actual guarantee. |
| NFR-5 | "Per-patch diff_size_ratio()" | VERIFIED. Implementation matches requirement. |
| NFR-6 | "Every finding has rule_id or debate_verdict" | ACCURATE. Structural findings have rule_id; semantic findings have debate_verdict + transcript_reference. |
| NFR-7 | "Steps 1-7 untouched" | CONTRADICTED by Phase 5 which removes build_spec_fidelity_prompt from prompts.py. prompts.py is used by steps 1-7 even though the removed function is for step 8. |

### Axis 1 Scores
- Coverage completeness: **6/10** — 2 FRs with gaps (FR-2, FR-9), 2 with partial coverage (FR-4, FR-8)
- Internal consistency: **7/10** — Status extension justified; debate variant contradiction is serious
- Implementability: **6/10** — FR-2 table/code-block extraction unclear; FR-4 boundary undefined; FR-9 flag missing
- Risk identification: **5/10** — NFR-3 enforcement gap unacknowledged; NFR-4 misleading claim

---

## AXIS 2: Data Flow Assumptions (Soundness Gate)

### Finding: Frozen Dataclass with Mutable Dict Fields
**Evidence**: Architecture Sec 3.1, lines 112-125: `@dataclass(frozen=True) class SpecData` with `section_by_heading: dict` and `ids_by_family: dict` using `field(default_factory=dict)`.
**Analysis**: Python's `frozen=True` prevents attribute reassignment but NOT in-place dict mutation. `spec_data.section_by_heading["key"] = value` succeeds silently, violating Design Principle #2 ("immutable data flow"). The comment "Derived lookup indexes (computed in __post_init__ of mutable builder)" suggests awareness of the issue, but the stated solution (mutable builder) is not architecturally specified.
**Severity**: MEDIUM — Practically safe if checkers are well-behaved, but contradicts the stated immutability guarantee.

### Finding: Stable ID Bug (Duplicate Parameter)
**Evidence**: Architecture Sec 4.2.3, line 384-386: `compute_stable_id(f.dimension, f.rule_id, f.location, f.rule_id)` — `f.rule_id` passed for both `rule_id` and `mismatch_type` parameters.
**Analysis**: In current checker designs, `rule_id` equals `mismatch_type` (the dict key IS the rule_id). So this is a latent bug — no collisions today. But `compute_stable_id` signature explicitly separates these parameters for a reason. If a future checker uses rule_id ≠ mismatch_type, IDs would collide.
**Severity**: MEDIUM — Latent bug. Would become CRITICAL if checkers evolve to separate rule_id from mismatch_type.

### Finding: Post-Collection Mutation Violates Stated Principle
**Evidence**: Architecture Sec 4.2.3, lines 383-388: `for f in all_findings: f.stable_id = compute_stable_id(...)` after parallel collection.
**Analysis**: Finding is a regular (non-frozen) dataclass, so this works. But Design Principle #2 says "Parsers produce frozen dataclasses; checkers return new Finding lists — no shared mutable state." Finding IS shared mutable state that's mutated after parallel collection. The principle as stated is violated.
**Severity**: LOW — Code works. Documentation is misleading.

### Finding: Dual Authority Conflict (Registry vs SPEC_FIDELITY_GATE)
**Evidence**: Architecture Sec 5.3: "SPEC_FIDELITY_GATE is still used for per-run report validation." Design Principle #3: "The convergence gate reads the deviation registry, never raw scan output."
**Codebase evidence**: `SPEC_FIDELITY_GATE` checks `high_severity_count_zero` in spec-fidelity.md frontmatter. If registry says PASS (0 active HIGHs after debate downgrades) but spec-fidelity.md report was generated before registry updates, frontmatter may show `high_severity_count: 2` → SPEC_FIDELITY_GATE fails.
**Analysis**: Two independent authorities evaluating the same thing with potentially different answers. No defined resolution order.
**Severity**: HIGH — Runtime conflict that would cause false gate failures.

### Axis 2 Scores
- Coverage completeness: **7/10** — All data flow components defined
- Internal consistency: **4/10** — Frozen-but-mutable, duplicate parameter, dual authority
- Implementability: **6/10** — Stable ID bug would cause subtle issues; dual authority needs resolution
- Risk identification: **3/10** — None of these issues are acknowledged in the architecture's error handling (Section 7)

---

## AXIS 3: Convergence Engine Stress Test (Budget Arithmetic)

### Finding: Budget Arithmetic is Correct
**Evidence**: Architecture Sec 4.5, Sec 4.5.1: "This entire flow counts as one run toward the budget of 3."
**Analysis**: Run 2 regression with 3 worktree agents + debate is correctly accounted as a single run. The 3 worktree checker executions are within the run 2 scope. Budget arithmetic is sound.
**Severity**: LOW — Budget accounting is correct.

### Finding: Semantic Non-Determinism Contaminates Monotonic Progress
**Evidence**: Architecture Sec 4.5 step 6: "run_n+1.highs > run_n.highs? → REGRESSION". Sec 4.3: semantic layer uses LLM (ClaudeProcess).
**Analysis**: Structural checkers are deterministic. Semantic layer is not. If run 1's semantic layer finds 2 HIGHs and run 2's finds 4 (temperature variation on identical content), the total HIGH count increases → false regression → 3 expensive worktree agents + debate. The architecture has NO mechanism to separate deterministic from non-deterministic HIGH counts in the monotonic progress check.
**Mitigation proposed**: Track structural and semantic HIGHs separately. Monotonic enforcement on structural only. Semantic findings tracked but flagged, not triggering regression.
**Severity**: HIGH — False regression detection wastes budget runs and tokens.

### Finding: Worktree Isolation Doesn't Isolate What Matters
**Evidence**: Architecture Sec 4.5.1: "Create 3 git worktrees." `execute_fidelity_with_convergence()` takes `roadmap_path` parameter (in output_dir, not git-tracked).
**Analysis**: Git worktrees isolate the SOURCE CODE (Python modules). But fidelity checks compare spec (source, git-tracked) against roadmap (output_dir, NOT git-tracked). 3 worktree agents all reading the same `output_dir/roadmap.md` provides zero isolation for the input that matters. The only benefit is isolating the checker code itself from concurrent modification — but checkers are read-only.
**Severity**: HIGH — Worktrees provide false confidence in isolation. Should use temp directories with file copies instead, or acknowledge worktrees only isolate code execution.

### Finding: Semantic Layer Can Introduce Oscillation (Theoretical)
**Evidence**: Architecture Sec 4.5 step 3 runs semantic layer regardless of structural results.
**Analysis**: If structural finds 0 HIGHs, semantic could introduce HIGHs → remediate → structural still 0, semantic finds DIFFERENT HIGHs → remediate → loop until budget. Adversarial debate mitigates (downgrades false HIGHs) but doesn't eliminate. Theoretical risk.
**Severity**: MEDIUM — Unlikely with debate mitigant but architecturally possible.

### Axis 3 Scores
- Coverage completeness: **7/10** — Budget, progress, regression all defined
- Internal consistency: **5/10** — Worktree isolation claim doesn't hold; semantic contamination unaddressed
- Implementability: **7/10** — Algorithm is clear enough to implement
- Risk identification: **3/10** — None of these failure modes are in Section 7's edge case table

---

## AXIS 4: Patch Remediation Design (Safety Gate)

### Finding: fallback_apply() Is the Real Primary Path
**Evidence**: Architecture Sec 4.6.2: `check_morphllm_available()` probes MCP at runtime. `fallback_apply()` for when MorphLLM absent.
**Analysis**: Most environments won't have MorphLLM. The fallback IS the primary path in practice. Its specification (exact match → fuzzy match via "strip whitespace differences") lacks precision: what does "strip whitespace" mean? Leading/trailing? Internal normalization? Collapse newlines? The anchor matching algorithm needs a precise spec.
**Severity**: MEDIUM — Functional gap in specification, not design.

### Finding: Markdown Anchor Ambiguity in fallback_apply()
**Evidence**: Architecture Sec 4.6.2: `fallback_apply()` uses `original_code` as anchor for substring match.
**Analysis**: For large roadmap files with repeated structural patterns (phase headers, numbered lists), anchor matching could target the wrong section. The architecture doesn't specify minimum anchor size or disambiguation strategy.
**Severity**: MEDIUM — Risk of wrong-section patching in large files.

### Finding: Diff-Size Denominator Is Correct
**Evidence**: Architecture Sec 4.6.1: `changed_lines / total_file_lines`, threshold 30%.
**Analysis**: The denominator choice correctly targets the regeneration prevention goal. Using section_lines would make the guard overly sensitive to small, targeted fixes.
**Severity**: N/A — Design is correct.

### Finding: Per-File Rollback Behavior Is Correct
**Evidence**: Architecture Sec 4.6.2: "If any patch failed: rollback file from snapshot." FR-9: "Rollback is per-file (not all-or-nothing)."
**Analysis**: FR-9's "per-file" means file-level granularity (file A independent of file B), not patch-level granularity within a file. Rolling back all patches within a failed file prevents inconsistent partial states. This matches intent.
**Severity**: N/A — Design is correct.

### Finding: --allow-regeneration Flag Missing
**Evidence**: FR-9 AC: "Full regeneration only with explicit user consent (--allow-regeneration flag)." Architecture has no mention of this flag in module map (Sec 2), integration (Sec 5), data model (Sec 3), or convergence engine (Sec 4.5).
**Analysis**: A required feature with zero coverage. No CLI argument, no config field, no enforcement check. The diff-size guard implicitly prevents regeneration (30% cap), but the explicit user-consent mechanism is absent.
**Severity**: HIGH — Required AC with no architectural mechanism.

### Axis 4 Scores
- Coverage completeness: **6/10** — Core patch pipeline complete, but --allow-regeneration missing entirely
- Internal consistency: **8/10** — Rollback and guard logic are internally consistent
- Implementability: **6/10** — fallback_apply() fuzzy matching underspecified
- Risk identification: **7/10** — Diff-size guard and rollback well-specified; anchor ambiguity not addressed

---

## AXIS 5: Module Map vs Requirements Gaps

### Finding: Lightweight Debate Completely Unspecified
**Evidence**: Architecture Sec 4.3: `validate_semantic_high()` described as "Two-agent debate via ClaudeProcess: Agent A (prosecutor), Agent B (defender), Judge." Requirements resolved Q#2 distinguishes lightweight vs full debate.
**Analysis**: The "lightweight" debate is a new pipeline primitive with no specification for:
- Prompt format for prosecutor/defender/judge
- Number of rounds
- Scoring criteria for verdict (CONFIRM_HIGH / DOWNGRADE_TO_MEDIUM / DOWNGRADE_TO_LOW)
- Token budget
- Evidence standards for each verdict
Additionally, architecture REVERSES the assignment from resolved Q#2: architecture gives semantic HIGHs the lightweight variant and regression the full variant; requirements say the opposite.
**Severity**: HIGH — Cannot implement without guessing. Debate variant assignment contradicts authority document.

### Finding: convergence.py God Module Risk
**Evidence**: Appendix B: convergence.py depends on ALL other new modules + executor.
**Analysis**: 5 direct dependencies, high fan-in. Testing requires mocking 5 modules. Mitigable via dependency injection.
**Severity**: MEDIUM — Design concern, not blocking.

### Finding: NFR-3 Prompt Size Has No Enforcement Mechanism
**Evidence**: Architecture Sec 4.3: `build_semantic_prompt()` docstring says "Enforces NFR-3: prompt size ≤ 30KB." SpecSection tracks `byte_size`.
**Analysis**: Tracking byte_size is necessary but not sufficient. The architecture shows no:
- Truncation algorithm when sections exceed budget
- Section-splitting logic for oversized sections
- Error handling or fallback when a single dimension's sections total >30KB
- What to do when a single SpecSection.byte_size > 30KB
**Severity**: HIGH — Hard requirement with only a docstring promise.

### Finding: fidelity-regression-validation.md Writer Unassigned
**Evidence**: FR-8 AC: consolidated report written to `fidelity-regression-validation.md`. Architecture Sec 4.5.1 step 6 mentions writing it. Sec 5.2 lists it in output directory.
**Analysis**: `handle_regression()` signature returns `list[Finding]` but prose says it writes the file in step 6. The file writing is a side effect not reflected in the API. Minor gap — intent is clear.
**Severity**: LOW.

### Finding: ACTIVE Status Crashes Existing __post_init__ Validation
**Evidence**: Architecture Sec 4.4.2: registry uses status "ACTIVE". Codebase: `VALID_FINDING_STATUSES = frozenset({"PENDING", "FIXED", "FAILED", "SKIPPED"})` with `__post_init__` validation raising ValueError.
**Analysis**: Creating a Finding with `status="ACTIVE"` via the existing codebase would raise `ValueError: Invalid Finding status 'ACTIVE'. Must be one of: FAILED, FIXED, PENDING, SKIPPED`. The architecture does NOT mention updating `VALID_FINDING_STATUSES`. This is a guaranteed runtime crash on the first registry operation that creates or loads an ACTIVE finding.
**Severity**: CRITICAL — Runtime crash. Architecture must specify adding "ACTIVE" to VALID_FINDING_STATUSES.

### Axis 5 Scores
- Coverage completeness: **5/10** — Lightweight debate unspecified, prompt enforcement missing, status crash
- Internal consistency: **6/10** — Debate variant contradiction, status extension uncoordinated
- Implementability: **4/10** — Lightweight debate, prompt truncation, and status update all require invention
- Risk identification: **4/10** — ACTIVE status crash not identified; prompt overflow not addressed

---

## AXIS 6: Migration Plan Ordering & Dependencies

### Finding: Phase 3/4 Soft Dependency (Manageable)
**Evidence**: Phase 3 builds convergence.py which calls remediation (Phase 4). But `remediate_executor.py` already exists — Phase 4 MODIFIES it.
**Analysis**: convergence.py can import from the existing remediate_executor.py. Phase 4 enhances it with MorphLLM. The dependency is soft: convergence.py works with the pre-Phase-4 remediate_executor. Migration plan should note this explicitly.
**Severity**: MEDIUM — Manageable but the plan should acknowledge the dependency.

### Finding: Phase 5 / Section 2.3 Contradiction
**Evidence**: Phase 5 item 12: "Remove old build_spec_fidelity_prompt from prompts.py." Section 2.3: "prompts.py" listed as UNCHANGED.
**Analysis**: Direct contradiction. prompts.py IS changed (dead code removal). Section 2.3 must be updated.
**Severity**: MEDIUM — Internal inconsistency.

### Finding: Within-Phase-1 Ordering Should Be Explicit
**Evidence**: Phase 1 lists: (1) spec_parser.py, (2) deviation_registry.py, (3) Extend Finding.
**Analysis**: Finding extension (item 3) should precede deviation_registry.py (item 2) because registry's `merge_findings()` accepts `list[Finding]` with `stable_id` field. Suggested order: (3) → (1) → (2) or (1) → (3) → (2).
**Severity**: LOW — Any order works with integration testing; explicit ordering improves clarity.

### Finding: No Circular Dependencies (Confirmed)
**Evidence**: Appendix B dependency graph. Analysis: convergence → remediate_executor → deviation_registry (chain, no cycle). deviation_registry depends on stdlib only.
**Analysis**: Diamond dependency exists (convergence depends on both remediate_executor and deviation_registry directly), but no cycles. Fan-in is high but acyclic.
**Severity**: LOW — Architecture claim is correct.

### Axis 6 Scores
- Coverage completeness: **7/10** — 5-phase plan covers all modules
- Internal consistency: **6/10** — Phase 5 contradiction, soft dependency unacknowledged
- Implementability: **7/10** — Plan is followable with the noted corrections
- Risk identification: **6/10** — Phase ordering risks partially addressed

---

## Scoring Matrix

| Axis | Coverage | Consistency | Implementability | Risk ID | Average |
|------|----------|-------------|-----------------|---------|---------|
| 1. FR/NFR Coverage | 6 | 7 | 6 | 5 | **6.0** |
| 2. Data Flow | 7 | 4 | 6 | 3 | **5.0** |
| 3. Convergence | 7 | 5 | 7 | 3 | **5.5** |
| 4. Remediation | 6 | 8 | 6 | 7 | **6.75** |
| 5. Module Gaps | 5 | 6 | 4 | 4 | **4.75** |
| 6. Migration | 7 | 6 | 7 | 6 | **6.5** |
| **Weighted Average** | **6.3** | **6.0** | **6.0** | **4.7** | **5.75** |
