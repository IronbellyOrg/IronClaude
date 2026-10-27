---
title: "Adversarial Design Validation Prompt — Deterministic Fidelity Gate"
type: prompt
created: 2026-03-19
target_command: "/sc:adversarial"
artifacts:
  - .dev/releases/current/v3.0_unified-audit-gating/architecture-design.md
  - .dev/releases/current/v3.0_unified-audit-gating/deterministic-fidelity-gate-requirements.md
---

# Ready-to-Execute Prompt

```
/sc:adversarial --compare /config/workspace/IronClaude/.dev/releases/backlog/v3.05_DeterministicFidelityGates/architecture-design.md,/config/workspace/IronClaude/.dev/releases/backlog/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md --depth deep --convergence 0.90 --focus "fr-nfr-coverage,data-flow,convergence,remediation,module-gaps,migration" --output /config/workspace/IronClaude/.dev/releases/backlog/v3.05_DeterministicFidelityGates/adversarial-design-review/

ADVERSARIAL VALIDATION BRIEF — Pre-Implementation Architecture Gate

This is NOT a standard compare-and-merge adversarial run. This is a VALIDATION run where:
- Artifact A (architecture-design.md) is the CLAIM — the proposed implementation blueprint
- Artifact B (deterministic-fidelity-gate-requirements.md) is the AUTHORITY — the ground-truth requirements spec with 10 FRs, 7 NFRs, 6 user stories, and 5 resolved questions

The goal is to surface gaps, contradictions, unstated assumptions, and design risks BEFORE code begins. Every finding must cite exact section references from both artifacts.

## AXIS 1: FR/NFR Coverage Completeness (Traceability Gate)

For each of the 10 FRs and 7 NFRs, verify the architecture provides a concrete, implementable mechanism:

- FR-1 (5 structural checkers): Does Section 4.2.2 define all 5 checkers with rule tables matching EVERY mismatch type from FR-3's severity rule table? Count the rules in FR-3 (15 rows) vs the rules in the 5 checker dicts. Flag any missing row.
- FR-2 (spec parser): Does SpecData (Section 3.1) cover ALL 9 extraction targets in FR-2's acceptance criteria? Cross-check: YAML frontmatter, markdown tables by heading path, fenced code blocks with language, requirement ID families (FR-\d+.\d+, NFR-\d+.\d+, SC-\d+, G-\d+, D\d+), Python function signatures, file paths from manifest tables (Sec 4.1/4.2/4.3), Literal[...] enum values, numeric threshold expressions. Flag any extraction target with no corresponding SpecData field.
- FR-3 (anchored severity): Are the rule tables defined in code (not prompt text) as required? Are they keyed by (dimension, mismatch_type) → severity as specified? Is there an extensibility mechanism for adding new rules without changing checker logic?
- FR-4 (residual semantic layer): How does the architecture determine what is "uncovered" by structural checkers? The requirements say checkers handle 55-85% structurally. Where is the boundary defined? Is it a static mapping or dynamic detection?
- FR-5 (sectional comparison): Does DIMENSION_SECTIONS in Section 4.1 cover all 5 dimensions? Does the supplementary section mechanism handle cross-references per resolved question #5?
- FR-6 (deviation registry): Does the JSON schema include all acceptance criteria fields: stable_id, first_seen_run, last_seen_run, FIXED status transitions, spec_hash reset, run metadata? Note: the requirements use statuses FIXED/SKIPPED/FAILED while the architecture adds ACTIVE. Is this extension justified or a gap?
- FR-7 (convergence gate): Does the architecture enforce monotonic progress (each run ≤ HIGHs than previous)? The algorithm says "check run_n+1.highs > run_n.highs → REGRESSION" — is this the same as monotonic enforcement or just detection?
- FR-8 (regression detection): Does handle_regression() satisfy all acceptance criteria? Particularly: "findings sorted by severity (HIGH → MEDIUM → LOW)", "this entire flow counts as one run toward the budget of 3", "adversarial debate validates severity of each HIGH", "debate verdicts update the deviation registry."
- FR-9 (edit-only remediation): Does the patch model match the MorphLLM lazy snippet format from resolved question #3? Where is the --allow-regeneration flag handled? Does fallback_apply() correctly handle "// ... existing code ..." context markers? Does per-file rollback match "Rollback is per-file (not all-or-nothing)"?
- FR-10 (run-to-run memory): Does get_prior_findings_summary(max_entries=50) match "max 50 prior findings in prompt, oldest first truncated"? Where are first_seen_run and last_seen_run tracked?
- NFR-1 through NFR-7: For each row in Section 10's compliance matrix, challenge whether the "How Satisfied" claim is backed by a concrete mechanism, not just an assertion.

## AXIS 2: Data Flow Assumptions (Soundness Gate)

Challenge the immutable data flow and parallel execution claims:

- FROZEN DATACLASS CONTRADICTION: SpecData (Section 3.1) is declared frozen=True but contains `section_by_heading: dict` and `ids_by_family: dict` with `field(default_factory=dict)`. Frozen dataclasses with mutable dict fields are NOT truly immutable — the dicts can be mutated in-place via `spec_data.section_by_heading["key"] = value`. This is a design contradiction with Design Principle #2 ("immutable data flow"). How severe is this? Does it actually break NFR-4?
- STABLE ID BUG: In Section 4.2.3, run_all_checkers() calls `compute_stable_id(f.dimension, f.rule_id, f.location, f.rule_id)` — passing `f.rule_id` for BOTH the `rule_id` and `mismatch_type` parameters. This means findings with different mismatch_types but the same rule_id would collide. Is this a bug or intentional?
- POST-COLLECTION MUTATION: run_all_checkers() assigns `f.stable_id = compute_stable_id(...)` after collecting findings from parallel futures. If Finding is a regular (non-frozen) dataclass, this is safe but violates the "immutable data flow" principle. If Finding were frozen, this would crash. Clarify the intended mutability contract.
- DUAL AUTHORITY CONFLICT: The convergence engine evaluates the registry for pass/fail (Design Principle #3). But Section 5.3 says "SPEC_FIDELITY_GATE is still used for per-run report validation." What happens if the registry says PASS (0 active HIGHs) but SPEC_FIDELITY_GATE says FAIL (e.g., missing frontmatter)? Which is authoritative? Is there an ordering dependency?

## AXIS 3: Convergence Engine Stress Test (Budget Arithmetic)

Challenge the 3-run budget under adversarial scenarios:

- BUDGET ARITHMETIC UNDER REGRESSION: Run 1 finds HIGHs → remediate → Run 2 regresses → handle_regression() spawns 3 worktrees + debate (this is "run 2") → remediate again → Run 3 is the final check. But handle_regression() includes its own checker execution (3 agents running full suites). Does that mean run 2 actually contains 4 total checker executions (1 original + 3 worktree)? Is this within the budget accounting?
- SEMANTIC NON-DETERMINISM CONTAMINATING MONOTONIC PROGRESS: Structural checkers are deterministic (same inputs → same findings). But the semantic layer is LLM-based and inherently non-deterministic. If run 1's semantic layer finds 2 HIGHs and run 2's semantic layer finds 3 HIGHs on IDENTICAL content (just LLM temperature variation), this triggers false regression detection → 3 expensive worktree agents → adversarial debate. How does the architecture isolate semantic non-determinism from the monotonic progress requirement?
- WORKTREE ISOLATION MISMATCH: The design creates git worktrees for parallel validation. But the fidelity check reads spec_path and roadmap_path from the OUTPUT DIRECTORY (config.output_dir), which is NOT git-tracked source code. Worktrees isolate the git-tracked repo but share the output directory. Do worktrees actually provide meaningful isolation for this use case?
- CONVERGENCE WITH ZERO SEMANTIC FINDINGS: If structural checkers find 0 HIGHs, does the semantic layer still run? If so, can it INTRODUCE HIGHs that structural checkers cleared? If yes, could the pipeline oscillate (structural clears → semantic adds → remediate → structural clears → semantic adds...)?

## AXIS 4: Patch Remediation Design (Safety Gate)

Challenge the MorphLLM-optional remediation pipeline:

- MORPHLLM AS "OPTIONAL PRIMARY": check_morphllm_available() probes MCP at runtime. The design makes MorphLLM the primary path but labels it optional. In practice, most users won't have MorphLLM installed. Is the fallback_apply() function robust enough to be the REAL primary path? Has it been designed with that assumption?
- FALLBACK ANCHOR MATCHING ON MARKDOWN: fallback_apply() does exact match then fuzzy match (strip whitespace differences) on original_code. For markdown roadmap files where many sections share similar structure (numbered lists, heading patterns), whitespace-stripped matching could match the WRONG section. How robust is this for large roadmaps?
- DIFF-SIZE DENOMINATOR CHOICE: The 30% threshold is per-patch, computed as `changed_lines / total_file_lines`. For a 1000-line file where a finding requires editing 5 lines in one section, the ratio is 0.5%. But those 5 lines could completely change a critical section's semantics. Is total_file_lines the right denominator? Should it be section_lines instead?
- ROLLBACK GRANULARITY TENSION: FR-9 says "Valid patches for the same file are applied sequentially" AND "Rollback is per-file." But Section 4.6.2 says "If any patch failed: rollback file from snapshot." This means if patches 1-3 succeed and patch 4 fails, ALL patches (including successful 1-3) are rolled back. Is this the intended behavior? It seems like successful patches should be preserved.
- MISSING --allow-regeneration: FR-9 requires "Full regeneration only with explicit user consent (--allow-regeneration flag)." The architecture does not define a CLI surface for this flag anywhere in the module map or integration section.

## AXIS 5: Module Map vs Requirements Gaps

Identify structural coverage gaps:

- UNDEFINED LIGHTWEIGHT DEBATE: The architecture says semantic HIGHs trigger a "lightweight adversarial debate" (Section 4.3) while regression uses "full /sc:adversarial" (Section 4.5). Resolved question #2 in the requirements distinguishes these. But the lightweight variant is described only as "Two-agent debate via ClaudeProcess" with no spec for prompt format, scoring, or verdict criteria. Is this sufficiently defined to implement?
- GOD MODULE RISK: convergence.py depends on ALL other new modules + executor (Appendix B). This is high fan-in. Is there a risk that convergence.py becomes a monolithic orchestrator that is difficult to test in isolation?
- PROMPT SIZE ENFORCEMENT: NFR-3 requires no prompt exceeds 30KB. build_semantic_prompt() mentions this in docstring but the architecture shows no explicit truncation mechanism, error handling for over-budget sections, or section-splitting logic when a single section exceeds 30KB.
- MISSING fidelity-regression-validation.md WRITER: FR-8 requires writing this file. The architecture mentions it in Section 5.2 (state integration) but doesn't specify which module/function creates it. Is it convergence.py's handle_regression() or somewhere else?
- FINDING DATACLASS EXTENSION: The architecture adds rule_id, spec_quote, roadmap_quote, stable_id to Finding. The existing Finding in models.py has status validation in __post_init__. Will adding fields with defaults preserve backward compatibility with existing code that constructs Finding objects?

## AXIS 6: Migration Plan Ordering & Dependencies

Challenge the 5-phase sequencing:

- PHASE 3/4 CIRCULAR DEPENDENCY: Phase 3 builds convergence.py, whose algorithm (Section 4.5) calls remediation at step 7. But patch remediation is Phase 4. If convergence.py is built in Phase 3 without remediation, it cannot execute its full loop. Should convergence be Phase 5 (after remediation) or should remediation be Phase 3?
- PHASE 5 CONTRADICTION: Phase 5 says "Remove old build_spec_fidelity_prompt from prompts.py (dead code)." But Section 2.3 lists prompts.py as UNCHANGED. These statements contradict. Which is correct?
- WITHIN-PHASE-1 ORDERING: Phase 1 builds spec_parser.py and deviation_registry.py together. But deviation_registry.py needs the extended Finding dataclass (with stable_id), which is also Phase 1. Is the Finding extension sequenced BEFORE deviation_registry.py within Phase 1?
- CONVERGENCE.PY FAN-IN: Appendix B says convergence.py depends on ALL other modules. But the dependency graph claims "no circular dependencies." Verify: does remediate_executor.py need to import from deviation_registry.py to update finding statuses? If so, does convergence.py → remediate_executor.py → deviation_registry.py create an indirect cycle through convergence?

## Scoring Criteria

Per finding:
- **CRITICAL**: Any FR/NFR with zero architectural coverage, any design bug that would cause incorrect behavior at runtime
- **HIGH**: Any measurement/calibration requirement with no mechanism, any dependency the migration plan gets wrong, any safety invariant with a gap
- **MEDIUM**: Internal consistency issues that don't affect correctness, LOC estimates off by >50%, ambiguous specifications that could be interpreted multiple ways
- **LOW**: Documentation gaps that don't affect implementation, naming inconsistencies

Per axis, score 0-10 on:
1. **Coverage completeness**: Does the architecture address every requirement in that axis?
2. **Internal consistency**: Does the design contradict itself?
3. **Implementability**: Can a developer build this without guessing?
4. **Risk identification**: Are failure modes acknowledged and handled?

## Verdict

Produce a final verdict:
- **APPROVED** (all axes ≥ 7): Proceed to implementation
- **CONDITIONAL** (any axis 4-6): Resolve blocking findings, then re-validate
- **REJECTED** (any axis ≤ 3): Fundamental redesign required

Include a mandatory BLOCKING FINDINGS list — issues that MUST be resolved before implementation begins, regardless of overall verdict.

Produce a structured findings report with columns: Finding ID | Axis | Severity | Evidence (exact section refs from both artifacts) | Recommended Resolution.
```
