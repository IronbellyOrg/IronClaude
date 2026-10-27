# Validation Report: CompatibilityReport-Merged.md

**Verdict: CONDITIONAL**

The report may proceed to tasklist generation after fixing 3 completeness gaps and 10 actionability gaps.

---

## Criterion 1: COMPLETENESS — CONDITIONAL

Cross-reference of every spec FR against the merged report:

| FR | Covered in Report? | Section | Status |
|----|-------------------|---------|--------|
| FR-1 (Structural Checkers) | Yes | §4 row: structural_checkers.py | New code to build |
| FR-2 (Spec Parser) | Yes | §4 row: spec_parser.py | New code to build |
| **FR-3 (Severity Rules)** | **NO** | **Missing entirely** | **GAP** |
| FR-4 (Semantic Layer) | Yes | §1, §4 rows: run_semantic_layer, validate_semantic_high | Modify + new code |
| FR-4.1 (Debate Protocol) | Yes | §4 row: validate_semantic_high | New code |
| FR-4.2 (Prompt Budget) | Yes | §2 row: prompt budget constants | Already done |
| **FR-5 (Sectional/Chunked Comparison)** | **NO** | **Missing entirely** | **GAP** |
| FR-6 (Deviation Registry) | Yes | §2 rows: DeviationRegistry, compute_stable_id, etc. | Mostly done |
| FR-7 (Convergence Gate) | Yes | §4, §7a | Modify + new code |
| FR-8 (Regression Detection) | Yes | §2, §4 rows | Partially done + new code |
| FR-9 (Remediation) | Yes | §1, §3, §4, §7c | Modify + new code |
| FR-9.1 (--allow-regeneration) | Yes | §2 row | Already done |
| **FR-10 (Run-to-Run Memory)** | **NO** | **Missing entirely** | **GAP** |
| NFR-1 through NFR-7 | No | Not cross-referenced | Minor gap |
| US-1 through US-6 | No | Not cross-referenced | Minor gap (covered implicitly by FR mapping) |

### Completeness Findings

**GAP-C1 (BLOCKING)**: FR-3 (Anchored Severity Rules) is not mentioned anywhere in the report. This is a genuinely new component — every structural checker (FR-1) depends on it. The severity rule tables must be defined in code, not prompt text. This is a significant omission since it's a dependency of FR-1.

**GAP-C2 (BLOCKING)**: FR-5 (Sectional/Chunked Comparison) is not mentioned. This requirement describes replacing full-document inline embedding with per-section comparison. The report does not assess whether this capability exists, is partially implemented, or needs building. It depends on FR-2 (parser).

**GAP-C3 (BLOCKING)**: FR-10 (Run-to-Run Memory) is not mentioned. This describes how the semantic layer prompt includes prior findings summaries. It depends on FR-4 and FR-6. The report doesn't assess its implementation status.

**GAP-C4 (Minor)**: NFRs and User Stories are not explicitly cross-referenced. This is acceptable since FR coverage implicitly maps to them, but tasklist generation would benefit from explicit NFR traceability.

---

## Criterion 2: ACCURACY — PASS

Every verifiable claim in the report was re-checked against the codebase:

| Claim | Report Citation | Verification | Verdict |
|-------|----------------|-------------|---------|
| convergence.py contains compute_stable_id | line 24 | `def compute_stable_id(` at line 24 | **VERIFIED** |
| convergence.py contains DeviationRegistry | line 50-225 | `class DeviationRegistry:` at line 50 | **VERIFIED** |
| convergence.py contains ConvergenceResult | line 228-237 | `class ConvergenceResult:` at line 229 | **VERIFIED** (off by 1 line) |
| convergence.py contains _check_regression | line 240-272 | `def _check_regression(` at line 240 | **VERIFIED** |
| semantic_layer.py contains RubricScores | yes | `class RubricScores:` at line 47 | **VERIFIED** |
| semantic_layer.py contains build_semantic_prompt | yes | `def build_semantic_prompt(` at line 171 | **VERIFIED** |
| semantic_layer.py contains score_argument | yes | `def score_argument(` at line 237 | **VERIFIED** |
| semantic_layer.py contains judge_verdict | yes | `def judge_verdict(` at line 284 | **VERIFIED** |
| validate_semantic_high() NOT defined | §4 gap | Only in docstring at line 321; no `def` | **VERIFIED** |
| _DIFF_SIZE_THRESHOLD_PCT = 50 | remediate_executor.py:45 | Exact match at line 45 | **VERIFIED** |
| ACTIVE in VALID_FINDING_STATUSES | models.py:16 | Exact match at line 16 | **VERIFIED** |
| Finding.source_layer | models.py:44 | `source_layer: str = "structural"` at line 44 | **VERIFIED** |
| RoadmapConfig.convergence_enabled | models.py:107 | Exact match at line 107 | **VERIFIED** |
| RoadmapConfig.allow_regeneration | models.py:108 | Exact match at line 108 | **VERIFIED** |
| WIRING_GATE in ALL_GATES | gates.py:944 | Exact match at line 944 | **VERIFIED** |
| SPEC_FIDELITY_GATE conditional bypass | executor.py:521 | `gate=None if config.convergence_enabled else SPEC_FIDELITY_GATE` at line 521 | **VERIFIED** |
| fidelity.py is dead code | §5 | `from .fidelity import` → 0 matches across codebase | **VERIFIED** |
| RunMetadata never instantiated | §5 | `RunMetadata(` → 0 matches | **VERIFIED** |
| spec_patch.py imported | commands.py:210, executor.py:1397 | Both imports confirmed | **VERIFIED** |
| spec_parser.py does not exist | §4 | Glob returns no match | **VERIFIED** |
| structural_checkers.py does not exist | §4 | Glob returns no match | **VERIFIED** |

**All 21 verifiable claims are accurate.** One minor line-number discrepancy (ConvergenceResult: 228 vs 229) is immaterial.

---

## Criterion 3: ACTIONABILITY — CONDITIONAL

Assessment of whether each item in §3 and §4 has sufficient detail to become a task.

### Section 3 (Modifications)

| Item | File | Verdict | Missing Detail |
|------|------|---------|----------------|
| Diff-size threshold 50%→30% | remediate_executor.py:45 | **SUFFICIENT** | Single constant change |
| Diff-size granularity per-file→per-patch | remediate_executor.py | **INSUFFICIENT** | No detail on current per-file logic or what "per-patch" means in this codebase. FR-9 specifies MorphLLM patches but report notes ClaudeProcess is used — which model defines "patch"? |
| Rollback scope all-or-nothing→per-file | remediate_executor.py | **INSUFFICIENT** | Report says "per-file rollback" but doesn't describe current rollback mechanism or what needs to change. Need to read current snapshot/restore code first. |
| TRUNCATION_MARKER heading | semantic_layer.py | **INSUFFICIENT** | No line reference, no description of current marker format, no example of desired format |

### Section 4 (New Code)

| Item | File | Verdict | Missing Detail |
|------|------|---------|----------------|
| spec_parser.py | New file | **SUFFICIENT** | FR-2 has detailed ACs: 10 specific extraction capabilities |
| structural_checkers.py | New file | **SUFFICIENT** | FR-1 specifies 5 checkers with dimensions; FR-3 has rule tables |
| validate_semantic_high() | semantic_layer.py | **INSUFFICIENT** | Report says "orchestrator" but doesn't specify: function signature, how it integrates with existing score_argument/judge_verdict, where ClaudeProcess calls happen, how results feed back to registry |
| run_semantic_layer() | semantic_layer.py | **INSUFFICIENT** | No detail beyond "top-level entry point." Signature? Parameters? How does it receive structural findings as context per FR-4? |
| execute_fidelity_with_convergence() | convergence.py | **INSUFFICIENT** | Report says "3-run convergence loop orchestrator" but no detail on: how it calls structural checkers → semantic layer → remediation within the loop, how it integrates with existing executor step model |
| handle_regression() | convergence.py | **INSUFFICIENT** | "Full regression flow" is a summary, not a spec. FR-8 has 16 ACs that need to be reflected. How does it spawn 3 agents? How does merge work? |
| RemediationPatch dataclass | remediate_executor.py | **SUFFICIENT** | FR-9 specifies 6 fields explicitly with JSON example |
| apply_patches() | remediate_executor.py | **INSUFFICIENT** | "Sequential per-file, per-patch diff guard" — but report acknowledges MorphLLM vs ClaudeProcess is an open decision. Can't task this until that's resolved. |
| fallback_apply() | remediate_executor.py | **INSUFFICIENT** | "Deterministic text replacement (anchor matching)" — FR-9 says "minimum anchor: 5 lines or 200 chars" but report doesn't surface this detail |
| check_morphllm_available() | remediate_executor.py | **INSUFFICIENT** | No detail on how to probe MCP runtime, what constitutes "available," fallback behavior |
| roadmap_run_step() convergence branch | executor.py | **INSUFFICIENT** | "Bypass Claude subprocess" — but where in executor.py? What does the branch look like? How does it delegate to convergence engine? |
| Finding field extensions | models.py | **SUFFICIENT** | FR-6 specifies: rule_id, spec_quote, roadmap_quote, stable_id with clear semantics |

### Actionability Summary

- **SUFFICIENT**: 5 of 16 items (31%)
- **INSUFFICIENT**: 11 of 16 items (69%)

However, most INSUFFICIENT items can be resolved by cross-referencing the original spec's acceptance criteria during tasklist generation. The report itself doesn't need to contain all this detail — the spec does. The real blockers are:

1. Items gated on the MorphLLM decision (apply_patches, fallback_apply, check_morphllm_available) — 3 items
2. Items lacking integration detail not in the spec (validate_semantic_high, run_semantic_layer, execute_fidelity_with_convergence, handle_regression, roadmap_run_step convergence branch) — 5 items

**Recommendation**: These 5 integration-detail items should have their integration points documented before tasklist generation, OR the tasklist should include research spikes for each.

---

## Criterion 4: RISK COVERAGE — CONDITIONAL

### Captured Risks (4)

| Risk | Coverage | Adequate? |
|------|----------|-----------|
| 7a: Convergence loop vs linear pipeline | Yes | Yes — identifies step-8 insertion and self-containment requirement |
| 7b: Remediation ownership | Yes | Yes — identifies within-loop vs post-pipeline tension |
| 7c: MorphLLM vs ClaudeProcess | Yes | Yes — frames as design decision with two options |
| 7d: SPEC_FIDELITY_GATE ordering | Yes | Adequate — notes no dependency but suggests documenting |

### Missing Risks

**GAP-R1 (HIGH)**: **FR-3 dependency chain risk**. Severity rules (FR-3) are entirely new and untested, yet every structural checker (FR-1) depends on them. If the rule tables are wrong, all 5 checkers produce incorrect findings. The report does not mention FR-3 at all (see GAP-C1). This is a foundational risk.

**GAP-R2 (MEDIUM)**: **spec_parser.py (FR-2) as critical path**. Both spec_parser.py and structural_checkers.py are genuinely new. FR-1 depends on FR-2. FR-4 depends on FR-1. FR-7 depends on FR-6 which consumes FR-1 output. The parser is on the critical path for the entire feature, but the report doesn't flag parser robustness as an integration risk. The spec itself notes this in "Key implementation risks" item 1, but the report doesn't surface it.

**GAP-R3 (MEDIUM)**: **Circular dependency between FR-7 and FR-8**. FR-7 (convergence gate) triggers FR-8 (regression detection) on structural regression. FR-8 depends on FR-7's budget tracking. The report notes both but doesn't flag the circular dependency as a risk requiring careful interface design.

**GAP-R4 (LOW)**: **FR-10 (run-to-run memory) integration risk**. The semantic layer prompt must include prior findings, but the report doesn't assess whether the existing `build_semantic_prompt()` supports this or needs modification.

---

## Criterion 5: DECISION COMPLETENESS — CONDITIONAL

### Decision 1: Diff threshold 30% or 50%?

| Aspect | Assessment |
|--------|-----------|
| Context provided? | Yes — spec says 30%, code has 50%, both sources cited |
| Enough to decide? | **YES** — the spec was written with adversarial review (BF-5 resolved this explicitly). The spec value (30%) should be authoritative unless there's evidence the 50% was deliberate. |
| Recommendation | Accept 30% per spec. The spec went through adversarial design review; this was a considered decision. |

### Decision 2: MorphLLM or ClaudeProcess?

| Aspect | Assessment |
|--------|-----------|
| Context provided? | Yes — report identifies the mismatch clearly |
| Enough to decide? | **NO** — needs investigation: Is MorphLLM actually available as an MCP server in this environment? If not, designing for it is speculative. The spec's Resolved Q#3 describes MorphLLM's lazy edit format in detail, but the report doesn't check whether MorphLLM is accessible. |
| Investigation needed | Check whether MorphLLM MCP server is configured/available. If not, keep ClaudeProcess with MorphLLM-compatible patch format for future migration. |

### Decision 3: validate_semantic_high() entrypoint

| Aspect | Assessment |
|--------|-----------|
| Context provided? | Partially — report confirms it's referenced but not defined |
| Enough to decide? | **NO** — this isn't really a "decision" — it's a gap to fill. FR-4.1 fully specifies the debate protocol (prosecutor/defender/judge). The question is WHERE it lives (semantic_layer.py or new file) and HOW it integrates with existing primitives. |
| Investigation needed | Read semantic_layer.py in full to understand the existing architecture and determine natural insertion point. |

### Decision 4: Prosecutor/defender execution location

| Aspect | Assessment |
|--------|-----------|
| Context provided? | No — report doesn't discuss this |
| Enough to decide? | **NO** — FR-4.1 specifies ClaudeProcess for prosecutor/defender. The report doesn't assess where ClaudeProcess is currently used in the codebase or how the debate fits into the existing architecture. |
| Investigation needed | Grep for ClaudeProcess usage in the roadmap module to understand existing patterns. |

---

## Summary

| Criterion | Verdict | Blocking Issues |
|-----------|---------|-----------------|
| 1. Completeness | **CONDITIONAL** | 3 FRs missing: FR-3, FR-5, FR-10 |
| 2. Accuracy | **PASS** | All 21 claims verified |
| 3. Actionability | **CONDITIONAL** | 11/16 items need more detail (5 need integration research, 3 blocked on Decision 2) |
| 4. Risk Coverage | **CONDITIONAL** | 2 missing risks: FR-3 dependency chain, spec_parser critical path |
| 5. Decision Completeness | **CONDITIONAL** | 2 of 4 decisions need investigation (MorphLLM availability, ClaudeProcess patterns) |

## Required Fixes Before Tasklist Generation

### Must Fix (3 items)

1. **Add FR-3, FR-5, FR-10 to the report** — assess whether they are already implemented, need modification, or need building. FR-3 (severity rules) is especially critical as it's a dependency of FR-1.

2. **Add FR-3 dependency chain to §7 risks** — severity rules are the foundation of deterministic checking. If they're wrong, everything is wrong.

3. **Investigate MorphLLM availability** — one grep/check to determine if MorphLLM MCP server exists in the environment. Result resolves Decision 2 and unblocks 3 action items.

### Should Fix (2 items)

4. **Add integration notes for 5 new orchestration functions** — validate_semantic_high, run_semantic_layer, execute_fidelity_with_convergence, handle_regression, roadmap_run_step convergence branch. These can alternatively be handled as research spikes in the tasklist.

5. **Add spec_parser.py critical path risk** — it's the foundation for FR-1 and transitively for FR-4, FR-7.
